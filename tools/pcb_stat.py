#!/usr/bin/env python3
"""Ice aktarilmis .kicad_pcb ozeti: katmanlar, dis hat, ayak izi, yol, via, bolge.
KiCad 9 (tek satir, net tablosu) ve KiCad 10 (cok satir, (net "ad")) bicimlerini okur.
Once: LC_ALL=C.UTF-8 kicad-cli pcb import --format altium -o /gecici/x.kicad_pcb boards/esc55a/altium/ESC_v0.PcbDoc
Kullanim: python3 -I tools/pcb_stat.py /gecici/x.kicad_pcb"""
import sys, re, collections
for p in sys.argv[1:]:
    s = open(p, encoding='utf-8').read()
    layers = re.findall(r'^\s*\(\d+ "([^"]+)" (signal|power|mixed)', s, re.M)
    fps = re.findall(r'\(footprint "([^"]+)"', s)
    refs = re.findall(r'\(property "Reference" "([^"]+)"', s)
    vals = re.findall(r'\(property "Value" "([^"]+)"', s)
    segs = len(re.findall(r'\(segment\s', s)); vias = len(re.findall(r'\(via\s', s)); zones = len(re.findall(r'\(zone\s', s))
    arcs = len(re.findall(r'^\t\(arc\s', s, re.M))
    nets = set(re.findall(r'\(net (?:\d+ )?"([^"]+)"\)', s))
    th = re.search(r'\(thickness ([\d.]+)\)', s)
    xs=[];ys=[]
    # yalniz kart duzeyindeki gr_* bloklari (bir sekme girintili); ayak izi icindekiler haric
    for m in re.finditer(r'^\t\(gr_(?:line|arc|rect|circle|poly)\b(.*?)^\t\)', s, re.S | re.M):
        if '(layer "Edge.Cuts")' not in m.group(1): continue
        for x,y in re.findall(r'\((?:start|end|mid|xy|center) ([-\d.]+) ([-\d.]+)\)', m.group(1)):
            xs.append(float(x)); ys.append(float(y))
    print('#####', p)
    print(' layers:', [l[0] for l in layers], 'thickness', th.group(1) if th else '?')
    if xs: print(' edge bbox: %.2f x %.2f mm' % (max(xs)-min(xs), max(ys)-min(ys)))
    print(' footprints', len(fps), 'segments', segs, 'arcs', arcs, 'vias', vias, 'zones', zones, 'nets', len(nets))
    c = collections.Counter(fps); print(' fp types:', c.most_common(40))
    print(' refs sample:', sorted(refs)[:200])
