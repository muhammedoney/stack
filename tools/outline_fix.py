#!/usr/bin/env python3
"""Remove near-zero-length Edge.Cuts lines/arcs left by the Altium import.

KiCad DRC reports them as "invalid_outline" (segment length 2 nm - 0.86 um on
esc55a). Pieces shorter than LIMIT are deleted; the outline stays closed because
their two ends coincide within KiCad's outline tolerance.

Usage (PCB editor closed):  python3 tools/outline_fix.py boards/esc55a/esc55a/esc55a.kicad_pcb
"""

import sys

import pcbnew

LIMIT = pcbnew.FromMM(0.001)  # 1 um


def main(path):
    board = pcbnew.LoadBoard(path)
    gone = []
    for item in list(board.GetDrawings()):
        if item.GetLayer() != pcbnew.Edge_Cuts or not isinstance(item, pcbnew.PCB_SHAPE):
            continue
        if item.GetShape() in (pcbnew.SHAPE_T_SEGMENT, pcbnew.SHAPE_T_ARC) and item.GetLength() < LIMIT:
            gone.append(item.GetLength())
            board.Remove(item)
    board.Save(path)
    print("%d outline pieces removed (lengths nm: %s)" % (len(gone), ", ".join(str(int(g)) for g in gone)))


if __name__ == "__main__":
    main(sys.argv[1])
