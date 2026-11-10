#!/usr/bin/env python3
"""Copy each symbol's value and fields from the schematic netlist to its footprint.

The Altium import leaves the board's footprints without the schematic's part
fields (manufacturer number, LCSC number, package ...) and pointing at the old
Altium sheet name. This writes Value, Description and every other field
(hidden) onto the footprint with the same reference, and points the footprint
at the root sheet of the KiCad schematic. Placement, pads and nets are not
touched.

Usage (KiCad's Python, PCB editor closed):
  kicad-cli sch export netlist -o /tmp/x.net boards/B/B/B.kicad_sch
  python3 tools/pcb_fields.py boards/B/B/B.kicad_pcb /tmp/x.net
"""

import os
import re
import sys

import pcbnew

SKIP = {"Reference", "Value", "Footprint", "Datasheet"}


def unquote(s):
    return s.replace('\\"', '"').replace("\\\\", "\\")


def components(path):
    text = open(path, encoding="utf-8").read()
    comps = text.split("(components", 1)[1].split("(libparts", 1)[0]
    out = {}
    for chunk in comps.split("(comp\n")[1:]:
        ref = re.search(r'\(ref "([^"]+)"\)', chunk).group(1)
        value = re.search(r'\(value "((?:[^"\\]|\\.)*)"\)', chunk)
        fields = {}
        for name, val in re.findall(r'\(name "([^"]+)"\)\s*"((?:[^"\\]|\\.)*)"\)', chunk):
            fields[name] = unquote(val)
        out[ref] = (unquote(value.group(1)) if value else "", fields)
    return out


def main():
    pcb_path, net_path = sys.argv[1:3]
    comps = components(net_path)
    sheetfile = os.path.basename(pcb_path).replace(".kicad_pcb", ".kicad_sch")
    board = pcbnew.LoadBoard(pcb_path)
    n = 0
    for fp in board.GetFootprints():
        fp.SetSheetname("/")
        fp.SetSheetfile(sheetfile)
        entry = comps.get(fp.GetReference())
        if not entry:
            continue
        value, fields = entry
        fp.SetValue(value)
        for name, val in fields.items():
            if name in SKIP:
                continue
            if fp.HasField(name):
                fp.GetField(name).SetText(val)
            else:
                f = pcbnew.PCB_FIELD(fp, pcbnew.FIELD_T_USER, name)
                f.SetText(val)
                f.SetVisible(False)
                f.SetLayer(pcbnew.F_Fab)
                f.SetPosition(fp.GetPosition())
                fp.Add(f)
        n += 1
    pcbnew.SaveBoard(pcb_path, board)
    print("%d footprints updated from the schematic" % n)


if __name__ == "__main__":
    main()
