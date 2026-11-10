#!/usr/bin/env python3
"""Rename a board's nets to the names its schematic netlist uses.

After an Altium import the board and the schematic name the same nets
differently ("RD" on the board, "/RD" in the schematic). This script maps each
board net to the schematic net of its pads and moves every item on it (pads,
tracks, vias, zones) to the schematic name. A board net whose pads fall into
more than one schematic net is a real connectivity difference: it is listed
and left alone.

Usage (KiCad's Python, PCB editor closed):
  kicad-cli sch export netlist -o /tmp/x.net boards/B/B/B.kicad_sch
  python3 tools/net_rename.py boards/B/B/B.kicad_pcb /tmp/x.net
"""

import re
import sys
from collections import defaultdict

import pcbnew


def netlist_pins(path):
    text = open(path, encoding="utf-8").read()
    pins = {}
    for chunk in re.split(r"\(net\s+\(code", text.split("(nets", 1)[1])[1:]:
        name = re.search(r'\(name "([^"]*)"\)', chunk).group(1)
        for ref, pin in re.findall(r'\(node\s+\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', chunk):
            pins[(ref, pin)] = name
    return pins


def main():
    pcb_path, net_path = sys.argv[1:3]
    pins = netlist_pins(net_path)
    board = pcbnew.LoadBoard(pcb_path)

    targets = defaultdict(set)
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            old = pad.GetNetname()
            new = pins.get((fp.GetReference(), pad.GetNumber()))
            if old and new:
                targets[old].add(new)

    mapping, split = {}, {}
    for old, news in targets.items():
        if len(news) == 1:
            new = next(iter(news))
            if new != old:
                mapping[old] = new
        else:
            split[old] = sorted(news)

    nets = {}

    def net(name):
        if name not in nets:
            n = board.FindNet(name)
            if n is None:
                n = pcbnew.NETINFO_ITEM(board, name)
                board.Add(n)
            nets[name] = n
        return nets[name]

    # Pins the schematic leaves open get their own "unconnected-(...)" net there
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            new = pins.get((fp.GetReference(), pad.GetNumber()), "")
            if not pad.GetNetname() and new.startswith("unconnected-"):
                pad.SetNet(net(new))

    moved = 0
    items = list(board.GetTracks()) + list(board.Zones())
    for fp in board.GetFootprints():
        items += list(fp.Pads())
    for item in items:
        new = mapping.get(item.GetNetname())
        if new:
            item.SetNet(net(new))
            moved += 1

    board.BuildConnectivity()
    pcbnew.SaveBoard(pcb_path, board)
    print("%d nets renamed, %d items moved" % (len(mapping), moved))
    for old, news in sorted(split.items()):
        print("  split: board net %s -> schematic %s" % (old, ", ".join(news)))


if __name__ == "__main__":
    main()
