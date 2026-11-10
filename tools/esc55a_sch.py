#!/usr/bin/env python3
"""Turn KiCad's Altium import of esc55a into a hierarchical KiCad project.

KiCad 10 (Kicad -> File -> Import Non-KiCad Project -> Altium Project, run
with LC_ALL=C.UTF-8) imports esc55a.PrjPcb as three top-level sheets:
esc55a.kicad_sch (= main.SchDoc), mcu.kicad_sch, mcu2.kicad_sch. This script
reads that raw import and writes boards/esc55a/esc55a/:

  esc55a.kicad_sch   root: three sheet symbols (main, mcu2 = ch 1-2, mcu = ch 3-4)
  main.kicad_sch     main.SchDoc (power, MOSFETs, connector)
  mcu2.kicad_sch     mcu2.SchDoc
  mcu.kicad_sch      mcu.SchDoc

and on the way:

  - Net labels whose name appears on more than one sheet become global labels.
    The Altium project has no ports or sheet entries, so its net labels are
    global (net identifier scope "Automatic"); KiCad's importer makes them
    local and the sheets would fall apart.
  - Symbol instance paths move under the root sheet.
  - "?" references are numbered: R? -> next free R numbers, #PWR? -> #PWR01...
  - No-connect flags on the pins that are open on both the schematic and the
    Altium PCB (NO_CONNECT).
  - PWR_FLAG on nets fed from pads or passive regulator pins (PWR_FLAGS).
  - Footprint "esc55a-import-fps:X" (parts that are not on the PCB, so
    tools/altium_libs.py cannot link them) -> the lib/*.pretty holding X.
  - .kicad_pro: schematic.top_level_sheets and sheets point to the new root;
    the board settings are left as they are.

The root sheet UUID is fixed, so running it again on the same import gives the
same files.

Usage:  python3 tools/esc55a_sch.py <raw import dir>
        python3 tools/altium_libs.py
"""

import json
import os
import re
import sys
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "boards", "esc55a", "esc55a")
ROOT_UUID = str(uuid.uuid5(uuid.NAMESPACE_URL, "stack/boards/esc55a/root"))
# (source file in the raw import, destination file, sheet name, page)
SHEETS = [
    ("esc55a.kicad_sch", "main.kicad_sch", "main", "2"),
    ("mcu2.kicad_sch", "mcu2.kicad_sch", "mcu2", "3"),
    ("mcu.kicad_sch", "mcu.kicad_sch", "mcu", "4"),
]
# Pins that are open on the schematic and on the Altium PCB: no-connect flag.
NO_CONNECT = {
    "mcu2": {"U11": "789", "U21": "789", "U12": ["5", "7", "8", "21"], "U22": ["5", "7", "8", "21"]},
    "mcu": {"U31": "789", "U41": "789", "U32": ["5", "7", "8", "21"], "U42": ["5", "7", "8", "21"]},
    "main": {"J0": ["GND"]},
}
# Nets fed from outside (battery pad, J0) or from regulator pins the Altium
# symbols mark passive: PWR_FLAG on a pin of the net. ("ref", R, pin) or
# ("value", power-symbol value).
PWR_FLAGS = {
    "main": [("ref", "P%d%s" % (n, p), "P$1") for n in (1, 2, 3, 4) for p in "abc"]
            + [("value", "GND"), ("value", "+8V"), ("value", "+3V3")],
    "mcu2": [("value", "+VD")],
}
PWR_FLAG_LIB = "/usr/share/kicad/symbols/power.kicad_sym"
SHEET_TEXT = {
    "main": "Güç, MOSFET'ler, J0",
    "mcu2": "Kanal 1-2 (EFM8BB21 + FD6288Q)",
    "mcu": "Kanal 3-4 (EFM8BB21 + FD6288Q)",
}


def sexpr_end(text, start):
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


def blocks(text, head):
    """(start, end) of every top-level block that starts with '\\n\\t(<head>'."""
    out = []
    for m in re.finditer(r"\n\t\(%s[\s\n]" % re.escape(head), text):
        s = m.start() + 2
        out.append((s, sexpr_end(text, s)))
    return out


def replace_blocks(text, head, fn):
    out, pos = [], 0
    for s, e in blocks(text, head):
        out.append(text[pos:s] + fn(text[s:e]))
        pos = e
    out.append(text[pos:])
    return "".join(out)


def to_global(body):
    """(label "X" (at ..) (effects .. (justify left bottom)) (uuid ..)) -> global_label."""
    name = re.match(r'\(label ("[^"]*")', body).group(1)
    at = re.search(r"\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)", body)
    just = "right" if re.search(r"\(justify right", body) else "left"
    uid = re.search(r'\(uuid "([^"]+)"\)', body).group(1)
    size = re.search(r"\(size ([\d.]+) ([\d.]+)\)", body)
    sz = "%s %s" % (size.group(1), size.group(2)) if size else "1.27 1.27"
    return ('(global_label %s\n\t\t(shape passive)\n\t\t(at %s %s %s)\n'
            '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size %s)\n\t\t\t)\n\t\t\t(justify %s)\n\t\t)\n'
            '\t\t(uuid "%s")\n'
            '\t\t(property "Intersheetrefs" "${INTERSHEET_REFS}"\n\t\t\t(at %s %s 0)\n'
            '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size %s)\n\t\t\t\t)\n\t\t\t\t(justify %s)\n'
            '\t\t\t\t(hide yes)\n\t\t\t)\n\t\t)\n\t)'
            % (name, at.group(1), at.group(2), at.group(3), sz, just, uid,
               at.group(1), at.group(2), sz, just))


def pin_xy(text, inst, number):
    """Connection point of pin <number> of a placed symbol (schematic mm, y down)."""
    lib = re.search(r'\(lib_name "([^"]+)"\)', inst) or re.search(r'\(lib_id "([^"]+)"\)', inst)
    start = text.index('\n\t\t(symbol "%s"' % lib.group(1)) + 3
    body = text[start:sexpr_end(text, start)]
    m = re.search(r'\(pin \w+ \w+\s+\(at ([-\d.]+) ([-\d.]+)[^)]*\)(?:(?!\(pin ).)*?\(number "%s"'
                  % re.escape(number), body, re.S)
    px, py = float(m.group(1)), -float(m.group(2))
    at = re.search(r"\n\t\t\(at ([-\d.]+) ([-\d.]+) ([-\d.]+)\)", inst)
    x0, y0, rot = float(at.group(1)), float(at.group(2)), int(float(at.group(3))) % 360
    for _ in range(rot // 90):
        px, py = py, -px
    mirror = re.search(r"\n\t\t\(mirror ([xy])\)", inst)
    if mirror:
        px, py = (px, -py) if mirror.group(1) == "x" else (-px, py)
    return round(x0 + px, 4), round(y0 + py, 4)


def add_no_connects(text, sheet):
    want = NO_CONNECT.get(sheet, {})
    marks = []
    for s, e in blocks(text, "symbol"):
        inst = text[s:e]
        ref = re.search(r'\(property "Reference" "([^"]*)"', inst).group(1)
        for pin in want.get(ref, []):
            x, y = pin_xy(text, inst, pin)
            if "(no_connect\n\t\t(at %g %g)" % (x, y) in text:
                continue
            uid = uuid.uuid5(uuid.NAMESPACE_URL, "stack/boards/esc55a/nc/%s/%s" % (ref, pin))
            marks.append('\t(no_connect\n\t\t(at %g %g)\n\t\t(uuid "%s")\n\t)\n' % (x, y, uid))
    end = text.rindex("\n)") + 1
    return text[:end] + "".join(marks) + text[end:], len(marks)


def pwr_flag_libsym():
    text = open(PWR_FLAG_LIB, encoding="utf-8").read()
    s = text.index('\t(symbol "PWR_FLAG"') + 1
    body = text[s:sexpr_end(text, s)]
    body = body.replace('(symbol "PWR_FLAG"', '(symbol "stack:PWR_FLAG"', 1)
    return "\t\t" + body.replace("\n\t", "\n\t\t") + "\n"


def add_pwr_flags(text, sheet, inst_path, counter):
    targets = PWR_FLAGS.get(sheet, [])
    if not targets:
        return text
    found = {}
    for s, e in blocks(text, "symbol"):
        inst = text[s:e]
        ref = re.search(r'\(property "Reference" "([^"]*)"', inst).group(1)
        val = re.search(r'\(property "Value" "([^"]*)"', inst).group(1)
        for t in targets:
            if t in found:
                continue
            if t[0] == "ref" and ref == t[1]:
                found[t] = pin_xy(text, inst, t[2])
            elif t[0] == "value" and ref.startswith("#PWR") and val == t[1]:
                found[t] = pin_xy(text, inst, "")
    missing = [t for t in targets if t not in found]
    if missing:
        raise SystemExit("PWR_FLAG target not found on %s: %s" % (sheet, missing))
    if '(symbol "stack:PWR_FLAG"' not in text:
        i = text.index("\t(lib_symbols\n") + len("\t(lib_symbols\n")
        text = text[:i] + pwr_flag_libsym() + text[i:]
    parts = []
    for t in targets:
        x, y = found[t]
        counter[0] += 1
        ref = "#FLG%02d" % counter[0]
        key = "stack/boards/esc55a/flag/%s/%s" % (sheet, "/".join(t))
        uid = uuid.uuid5(uuid.NAMESPACE_URL, key)
        puid = uuid.uuid5(uuid.NAMESPACE_URL, key + "/pin")
        fields = "".join(
            '\t\t(property "%s" "%s"\n\t\t\t(at %g %g 0)\n%s\t\t\t(effects\n\t\t\t\t(font\n'
            '\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n'
            % (k, v, x, y - dy, "" if k == "Value" else "\t\t\t(hide yes)\n")
            for k, v, dy in (("Reference", ref, 1.905), ("Value", "PWR_FLAG", 3.81),
                             ("Footprint", "", 0), ("Datasheet", "", 0), ("Description", "", 0)))
        parts.append(
            '\t(symbol\n\t\t(lib_id "stack:PWR_FLAG")\n\t\t(at %g %g 0)\n\t\t(unit 1)\n'
            '\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n'
            '\t\t(in_pos_files yes)\n\t\t(dnp no)\n\t\t(uuid "%s")\n%s'
            '\t\t(pin "1"\n\t\t\t(uuid "%s")\n\t\t)\n'
            '\t\t(instances\n\t\t\t(project "esc55a"\n\t\t\t\t(path "%s"\n'
            '\t\t\t\t\t(reference "%s")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
            % (x, y, uid, fields, puid, inst_path, ref))
    end = text.rindex("\n)") + 1
    return text[:end] + "".join(parts) + text[end:]


def fix_footprint_libs(text):
    """esc55a-import-fps:NAME (parts not on the PCB) -> the lib/*.pretty that has NAME."""
    pretty = {}
    lib = os.path.join(ROOT, "lib")
    for d in os.listdir(lib):
        if d.endswith(".pretty"):
            for f in os.listdir(os.path.join(lib, d)):
                pretty.setdefault(f[:-10], d[:-7])
    return re.sub(r'"esc55a-import-fps:([^"]+)"',
                  lambda m: '"%s:%s"' % (pretty[m.group(1)], m.group(1)) if m.group(1) in pretty else m.group(0),
                  text)


def sheet_symbol(name, fname, page, x, y, w=50.8, h=25.4):
    uid = str(uuid.uuid5(uuid.NAMESPACE_URL, "stack/boards/esc55a/sheet/" + name))
    return uid, (
        '\t(sheet\n\t\t(at %g %g)\n\t\t(size %g %g)\n\t\t(exclude_from_sim no)\n'
        '\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n'
        '\t\t(stroke\n\t\t\t(width 0.1524)\n\t\t\t(type solid)\n\t\t)\n'
        '\t\t(fill\n\t\t\t(color 0 0 0 0.0000)\n\t\t)\n\t\t(uuid "%s")\n'
        '\t\t(property "Sheetname" "%s"\n\t\t\t(at %g %g 0)\n'
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left bottom)\n\t\t\t)\n\t\t)\n'
        '\t\t(property "Sheetfile" "%s"\n\t\t\t(at %g %g 0)\n'
        '\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify left top)\n\t\t\t)\n\t\t)\n'
        '\t\t(instances\n\t\t\t(project "esc55a"\n\t\t\t\t(path "/%s"\n\t\t\t\t\t(page "%s")\n'
        '\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
        % (x, y, w, h, uid, name, x, y - 0.7, fname, x, y + h + 0.7, ROOT_UUID, page))


def root_sheet(sheet_uuids):
    parts = []
    x = 30.48
    for (src, dst, name, page) in SHEETS:
        uid, text = sheet_symbol(name, dst, page, x, 50.8)
        assert uid == sheet_uuids[name]
        parts.append(text)
        parts.append(
            '\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %g %g 0)\n'
            '\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n'
            '\t\t(uuid "%s")\n\t)\n'
            % (SHEET_TEXT[name], x, 50.8 + 25.4 + 6,
               uuid.uuid5(uuid.NAMESPACE_URL, "stack/boards/esc55a/text/" + name)))
        x += 76.2
    return ('(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
            '\t(uuid "%s")\n\t(paper "A4")\n'
            '\t(title_block\n\t\t(title "esc55a - 4in1 55 A ESC")\n\t\t(comment 1 "Altium esc55a.PrjPcb -> KiCad 10 (tools/esc55a_sch.py)")\n\t)\n'
            '\t(lib_symbols)\n%s'
            '\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n'
            '\t(embedded_fonts no)\n)\n' % (ROOT_UUID, "".join(parts)))


def main(src):
    texts, old_uuid = {}, {}
    pro_src = json.load(open(os.path.join(src, "esc55a.kicad_pro"), encoding="utf-8"))
    for tl in pro_src["schematic"]["top_level_sheets"]:
        old_uuid[tl["filename"]] = tl["uuid"]
    for s, d, name, page in SHEETS:
        texts[name] = open(os.path.join(src, s), encoding="utf-8").read()

    # labels used on more than one sheet -> global
    names = {n: set(re.findall(r'\n\t\(label "([^"]*)"', t)) for n, t in texts.items()}
    shared = set()
    for a in names:
        for b in names:
            if a != b:
                shared |= names[a] & names[b]
    for n in texts:
        texts[n] = replace_blocks(
            texts[n], "label",
            lambda b: to_global(b) if re.match(r'\(label "([^"]*)"', b).group(1) in shared else b)

    # instance paths under the root; the new sheet UUIDs replace the import's
    sheet_uuids = {}
    for s, d, name, page in SHEETS:
        sheet_uuids[name] = sheet_symbol(name, d, page, 0, 0)[0]
        texts[name] = texts[name].replace('(path "/%s"' % old_uuid[s],
                                          '(path "/%s/%s"' % (ROOT_UUID, sheet_uuids[name]))
        # only the root carries sheet_instances
        for st, en in reversed(blocks(texts[name], "sheet_instances")):
            texts[name] = texts[name][:st - 1] + texts[name][en:]

    # number "?" references
    used = {}
    for t in texts.values():
        for r in re.findall(r'\(reference "([A-Z#]+)(\d+)"\)', t):
            used.setdefault(r[0], set()).add(int(r[1]))
    counters = {}

    def annotate(body):
        m = re.search(r'\(property "Reference" "([A-Z#]+)\?"', body)
        if not m:
            return body
        prefix = m.group(1)
        k = counters.get(prefix, max(used.get(prefix, {0})))
        k += 1
        while k in used.get(prefix, set()):
            k += 1
        counters[prefix] = k
        ref = "%s%02d" % (prefix, k) if prefix.startswith("#") else "%s%d" % (prefix, k)
        body = body.replace('(property "Reference" "%s?"' % prefix, '(property "Reference" "%s"' % ref)
        return body.replace('(reference "%s?")' % prefix, '(reference "%s")' % ref)

    nc, flags = 0, [0]
    for s, d, name, page in SHEETS:
        texts[name] = replace_blocks(texts[name], "symbol", annotate)
        texts[name] = add_pwr_flags(texts[name], name, "/%s/%s" % (ROOT_UUID, sheet_uuids[name]), flags)
        texts[name], k = add_no_connects(texts[name], name)
        texts[name] = fix_footprint_libs(texts[name])
        nc += k

    for s, d, name, page in SHEETS:
        open(os.path.join(DST, d), "w", encoding="utf-8").write(texts[name])
    open(os.path.join(DST, "esc55a.kicad_sch"), "w", encoding="utf-8").write(root_sheet(sheet_uuids))

    pro_path = os.path.join(DST, "esc55a.kicad_pro")
    pro = json.load(open(pro_path, encoding="utf-8"))
    sch = dict(pro_src["schematic"])
    sch["top_level_sheets"] = [{"filename": "esc55a.kicad_sch", "name": "", "uuid": ROOT_UUID}]
    pro["schematic"] = sch
    pro["sheets"] = [[ROOT_UUID, "Root"]] + [[sheet_uuids[n], n] for s, d, n, p in SHEETS]
    pro.setdefault("meta", {})["filename"] = "esc55a.kicad_pro"
    json.dump(pro, open(pro_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(pro_path, "a").write("\n")

    print("global labels: %d names (%s ...)" % (len(shared), ", ".join(sorted(shared)[:6])))
    print("annotated: %s" % ", ".join("%s..%d" % (p, k) for p, k in sorted(counters.items())))
    print("no-connect flags: %d, PWR_FLAG: %d" % (nc, flags[0]))
    print("root %s, sheets %s" % (ROOT_UUID, ", ".join(d for s, d, n, p in SHEETS)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, ".tmp_imp", "out"))
