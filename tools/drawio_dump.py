#!/usr/bin/env python3
"""draw.io sayfa ve etiket dokumu (sikistirilmis sayfalar dahil).
Kullanim: python3 -I tools/drawio_dump.py docs/esc55a.drawio ..."""
import sys, re, base64, zlib, urllib.parse, html
import xml.etree.ElementTree as ET
def pages(path):
    root = ET.parse(path).getroot()
    for d in root.iter('diagram'):
        name = d.get('name')
        m = d.find('mxGraphModel')
        if m is None:
            txt = (d.text or '').strip()
            if not txt: continue
            raw = zlib.decompress(base64.b64decode(txt), -15)
            m = ET.fromstring(urllib.parse.unquote(raw.decode()))
        yield name, m
for path in sys.argv[1:]:
    print('#####', path)
    for name, m in pages(path):
        cells = list(m.iter('mxCell'))
        imgs = sum(1 for c in cells if 'image' in (c.get('style') or ''))
        print(f'== page "{name}": {len(cells)} cells, {imgs} image')
        for c in cells:
            v = c.get('value') or ''
            if not v: 
                # also UserObject label
                continue
            t = re.sub(r'<br\s*/?>', ' / ', v)
            t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
            t = re.sub(r'\s+', ' ', t).strip()
            if t: print('  -', t[:300])
        for u in m.iter('UserObject'):
            t = html.unescape(re.sub(r'<[^>]+>', ' ', u.get('label') or ''))
            t = re.sub(r'\s+',' ',t).strip()
            if t: print('  U-', t[:300])
