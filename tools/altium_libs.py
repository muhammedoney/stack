#!/usr/bin/env python3
"""Build lib/ from boards imported from Altium, and link the boards to it.

KiCad's Altium import keeps every symbol inside the schematic and every
footprint inside the board. This script:

  1. Copies the cached symbols of every sheet of the project (root and
     sub-sheets) into lib/<LIB>.kicad_sym, where
     <LIB> is the Altium library name (RLC, IC, CONN, MOS, Module). Symbols the
     importer made itself (power ports, "<board>-altium-import:") go to
     lib/stack.kicad_sym and the schematic is relinked to "stack:".
  2. Copies each board's footprints into lib/<LIB>.pretty (front side,
     0 degrees, at the origin).
  3. Writes the board's Footprint field from the PCB (by reference), so the
     schematic and the board match.
  4. Writes sym-lib-table and fp-lib-table next to each project.

When two boards carry a symbol or footprint with the same name but different
contents, the board listed later in BOARDS wins. A board without a schematic
or PCB yet (fmu has no PCB) is skipped for that part.

Usage:  python3 tools/altium_libs.py
"""

import os
import re
import shutil
import tempfile

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, "lib")
BOARDS = ["esc55a", "fmu"]
SYM_HEADER = '(kicad_symbol_lib\n\t(version 20251024)\n\t(generator "stack_altium_libs")\n\t(generator_version "10.0")\n'


def project(board):
    return os.path.join(ROOT, "boards", board, board)


def sexpr_end(text, start):
    """Index just past the s-expression that opens at text[start] == '('."""
    depth, i, n = 0, start, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            i += 1
            while text[i] != '"':
                i += 2 if text[i] == "\\" else 1
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced s-expression")


def lib_symbols(sch_text):
    """{"LIB:NAME": text} for the top-level symbols in (lib_symbols ...)."""
    start = sch_text.index("\t(lib_symbols")
    end = sexpr_end(sch_text, start + 1)
    out = {}
    for m in re.finditer(r'\n\t\t\(symbol "([^"]+)"', sch_text[start:end]):
        s = start + m.start() + 3
        out[m.group(1)] = sch_text[s:sexpr_end(sch_text, s)]
    return out


def sheets(board):
    """Every .kicad_sch of the project (root and sub-sheets)."""
    d = project(board)
    if not os.path.exists(os.path.join(d, board + ".kicad_sch")):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".kicad_sch"))


def extract_symbols():
    libs = {}
    for board in BOARDS:
        if not sheets(board):
            print("%-12s no schematic, skipped" % board)
        for path in sheets(board):
            text = open(path, encoding="utf-8").read()
            text = text.replace('"%s-altium-import:' % board, '"stack:')
            open(path, "w", encoding="utf-8").write(text)
            if "\t(lib_symbols\n" not in text:
                continue
            for full, body in lib_symbols(text).items():
                if ":" not in full:
                    continue  # per-instance variants (lib_name); they stay in the schematic
                lib, name = full.split(":", 1)
                body = body.replace('(symbol "%s"' % full, '(symbol "%s"' % name, 1)
                libs.setdefault(lib, {})[name] = body
    for lib, syms in libs.items():
        with open(os.path.join(LIB, lib + ".kicad_sym"), "w", encoding="utf-8") as f:
            f.write(SYM_HEADER)
            for name in sorted(syms):
                f.write("\t" + syms[name].replace("\n\t\t", "\n\t") + "\n")
            f.write(")\n")
        print("%-8s %3d symbols" % (lib, len(syms)))
    return sorted(libs)


def extract_footprints():
    tmp = tempfile.mkdtemp()
    io = pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP)
    libs, refs = {}, {}
    for board in BOARDS:
        refs[board] = {}
        path = os.path.join(project(board), board + ".kicad_pcb")
        if not os.path.exists(path):
            print("%-12s no PCB, skipped" % board)
            continue
        pcb = pcbnew.LoadBoard(path)
        for fp in pcb.GetFootprints():
            fpid = fp.GetFPID()
            lib, name = str(fpid.GetLibNickname()), str(fpid.GetLibItemName())
            refs[board][fp.GetReference()] = "%s:%s" % (lib, name)
            copy = pcbnew.FOOTPRINT(fp)
            if copy.IsFlipped():
                copy.Flip(copy.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
            copy.SetOrientationDegrees(0)
            copy.SetPosition(pcbnew.VECTOR2I(0, 0))
            copy.SetReference("REF**")
            copy.SetSheetname("")
            copy.SetSheetfile("")
            copy.SetPath(pcbnew.KIID_PATH())
            tdir = os.path.join(tmp, lib + ".pretty")
            os.makedirs(tdir, exist_ok=True)
            io.FootprintSave(tdir, copy)
            libs.setdefault(lib, set()).add(name)
    for lib in libs:  # only libraries seen on a board are rewritten
        dst = os.path.join(LIB, lib + ".pretty")
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(os.path.join(tmp, lib + ".pretty"), dst)
        print("%-8s %3d footprints" % (lib, len(libs[lib])))
    shutil.rmtree(tmp)
    return sorted(libs), refs


def link_footprints(board, refs):
    """Footprint field = PCB footprint, matched by the instance's Reference."""
    if not refs:
        return
    n = 0
    for path in sheets(board):
        text = open(path, encoding="utf-8").read()
        out, pos = [], 0
        for m in re.finditer(r'\n\t\(symbol\n', text):
            s = m.start() + 2
            e = sexpr_end(text, s)
            body = text[s:e]
            ref = re.search(r'\(property "Reference" "([^"]*)"', body)
            if ref and ref.group(1) in refs:
                new = re.sub(r'\(property "Footprint" "[^"]*"',
                             '(property "Footprint" "%s"' % refs[ref.group(1)], body, 1)
                n += new != body
                body = new
            out.append(text[pos:s] + body)
            pos = e
        out.append(text[pos:])
        open(path, "w", encoding="utf-8").write("".join(out))
    print("%-12s %3d footprint fields linked" % (board, n))


def write_tables(board, sym_libs, fp_libs):
    sym_libs = sorted(set(sym_libs) | {l[:-10] for l in os.listdir(LIB) if l.endswith(".kicad_sym")})
    fp_libs = sorted(set(fp_libs) | {l[:-7] for l in os.listdir(LIB) if l.endswith(".pretty")})
    rel = "${KIPRJMOD}/../../../lib/"
    with open(os.path.join(project(board), "sym-lib-table"), "w") as f:
        f.write("(sym_lib_table\n\t(version 7)\n")
        for lib in sym_libs:
            f.write('\t(lib (name "%s")(type "KiCad")(uri "%s%s.kicad_sym")(options "")(descr "Stack %s symbols"))\n' % (lib, rel, lib, lib))
        f.write(")\n")
    with open(os.path.join(project(board), "fp-lib-table"), "w") as f:
        f.write("(fp_lib_table\n\t(version 7)\n")
        for lib in fp_libs:
            f.write('\t(lib (name "%s")(type "KiCad")(uri "%s%s.pretty")(options "")(descr "Stack %s footprints"))\n' % (lib, rel, lib, lib))
        f.write(")\n")


def main():
    os.makedirs(LIB, exist_ok=True)
    sym_libs = extract_symbols()
    fp_libs, refs = extract_footprints()
    for board in BOARDS:
        link_footprints(board, refs[board])
        write_tables(board, sym_libs, fp_libs)


if __name__ == "__main__":
    main()
