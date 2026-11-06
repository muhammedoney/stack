#!/usr/bin/env python3
"""Altium .SchDoc parca, ag etiketi ve not dokumu (olefile).
Kullanim: python3 -I tools/altium_sch_dump.py boards/esc55a/altium/main.SchDoc ...
Cikti: ref | kutuphane | deger | ayak izi | tedarikci kodu; ag etiketleri, guc portlari, metinler."""
import sys, olefile, collections
def records(path):
    ole = olefile.OleFileIO(path)
    data = ole.openstream('FileHeader').read()
    i = 0; out = []
    while i + 4 <= len(data):
        ln = int.from_bytes(data[i:i+2], 'little'); typ = data[i+3]; i += 4
        blob = data[i:i+ln]; i += ln
        if typ != 0: continue
        s = blob.rstrip(b'\0').decode('latin-1')
        d = {}
        for kv in s.split('|'):
            if '=' in kv:
                k, v = kv.split('=', 1); d[k.upper()] = v
        out.append(d)
    return out
for path in sys.argv[1:]:
    recs = records(path)
    print('#####', path, len(recs), 'records')
    comps = {}
    idx_of = {}
    for n, r in enumerate(recs):
        if r.get('RECORD') == '1':
            comps[n-1] = {'lib': r.get('LIBREFERENCE'), 'desc': r.get('COMPONENTDESCRIPTION',''), 'params': {}}
    # owner index refers to record index (excluding header). header is recs[0]
    for n, r in enumerate(recs):
        o = r.get('OWNERINDEX')
        if o is None: continue
        o = int(o)
        if o in comps:
            if r.get('RECORD') == '34': comps[o]['ref'] = r.get('TEXT')
            elif r.get('RECORD') == '41':
                comps[o]['params'][r.get('NAME')] = r.get('TEXT')
    rows = []
    for c in comps.values():
        p = c['params']
        val = p.get('Comment') or p.get('Value') or ''
        rows.append((c.get('ref','?'), c['lib'], val, p.get('Footprint',''), p.get('LCSC') or p.get('Supplier Part Number 1') or p.get('Manufacturer Part Number 1','') or p.get('MPN','')))
    # comment designator may be RECORD 41 name Comment; also footprint in RECORD 45 implementation
    for n, r in enumerate(recs):
        if r.get('RECORD') == '45' and r.get('ITEMISCURRENT') == 'T':
            pass
    rows.sort(key=lambda x: (x[0].rstrip('0123456789'), int(''.join(ch for ch in x[0] if ch.isdigit()) or 0)))
    print('components:', len(rows))
    for row in rows: print('  ', ' | '.join(x or '' for x in row))
    nets = collections.Counter(r.get('TEXT') for r in recs if r.get('RECORD') == '25')
    ports = collections.Counter(r.get('NAME') for r in recs if r.get('RECORD') == '18')
    pwr = collections.Counter(r.get('TEXT') for r in recs if r.get('RECORD') == '17')
    sheets = [r.get('TEXT') for r in recs if r.get('RECORD') in ('32','33')]
    notes = [r.get('TEXT') for r in recs if r.get('RECORD') in ('4','28','209') and r.get('TEXT')]
    print('netlabels:', len(nets), sorted(k for k in nets if k))
    print('ports:', sorted(k for k in ports if k))
    print('power:', dict(pwr))
    print('sheet sym/files:', sheets)
    print('texts:', [t[:80] for t in notes][:80])
