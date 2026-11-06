#!/usr/bin/env python3
"""Ice aktarilmis .kicad_pcb ozeti: katmanlar, dis hat, ayak izi, yol, via, bolge.
Once: LC_ALL=C.UTF-8 kicad-cli pcb import --format altium -o /gecici/x.kicad_pcb boards/esc55a/altium/ESC_v0.PcbDoc
Kullanim: python3 -I tools/pcb_stat.py /gecici/x.kicad_pcb"""
import sys, re, collections
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    layers = re.findall(r'^\s*\(\d+ "([^"]+)" (signal|power|mixed)', s, re.M)
    fps = re.findall(r'\(footprint "([^"]+)"', s)
    refs = re.findall(r'\(property "Reference" "([^"]+)"', s)
    vals = re.findall(r'\(property "Value" "([^"]+)"', s)
    segs = len(re.findall(r'\(segment ', s)); vias = len(re.findall(r'\(via ', s)); zones = len(re.findall(r'\(zone ', s))
    arcs = len(re.findall(r'\(arc ', s))
    nets = re.findall(r'^\s*\(net \d+ "([^"]*)"\)', s, re.M)
    th = re.search(r'\(thickness ([\d.]+)\)', s)
    xs=[];ys=[]
    for m in re.finditer(r'\(gr_(line|arc|rect|circle|poly)(.*?)\(layer "Edge.Cuts"\)', s, re.S):
        for x,y in re.findall(r'\((?:start|end|mid|xy|center) ([-\d.]+) ([-\d.]+)\)', m.group(2)):
            xs.append(float(x)); ys.append(float(y))
    print('#####', p)
    print(' layers:', [l[0] for l in layers], 'thickness', th.group(1) if th else '?')
    if xs: print(' edge bbox: %.2f x %.2f mm' % (max(xs)-min(xs), max(ys)-min(ys)))
    print(' footprints', len(fps), 'segments', segs, 'arcs', arcs, 'vias', vias, 'zones', zones, 'nets', len(nets))
    c = collections.Counter(fps); print(' fp types:', c.most_common(40))
    print(' refs sample:', sorted(refs)[:200])
