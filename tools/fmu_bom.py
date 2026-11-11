#!/usr/bin/env python3
"""boards/fmu/bom-revb.csv from tools/fmu_schematic.py parts + JLC prices (jlc_cache.json, 2026-11-11)."""
import csv, json, re, sys
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
D = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO / "tools"))
sys.path.insert(0, str(D))
import fmu_schematic as F
import jlc
F.build_symbols(); F.define_parts()

def pads(fp):
    name = fp.split(":", 1)[1]
    t = (REPO / "lib/stack.pretty" / f"{name}.kicad_mod").read_text()
    return len([m for m in re.finditer(r'\(pad "([^"]*)" smd', t) if m.group(1)])

groups = {}
for ref, p in F.PARTS.items():
    if not p["bom"]:
        continue
    key = (p["lcsc"], p["value"], p["dnp"], ref == "J503")
    groups.setdefault(key, []).append(ref)
rows = []
tot = {"std": 0.0, "dual": 0.0}
ext_types, joints = set(), 0
for (lcsc, val, dnp, dual), refs in sorted(groups.items(), key=lambda kv: (kv[1][0][0], int(re.sub(r"\D", "", kv[1][0]) or 0))):
    p = F.PARTS[refs[0]]
    i = jlc.info(lcsc)
    n = len(refs)
    unit = jlc.price(lcsc, n * 100)
    card = round(unit * n, 4)
    pk = pads(p["fp"])
    kind = {"base": "basic", "expand": "extended"}.get(i.get("jlc_type"), i.get("jlc_type"))
    if dual:
        sku = "Dual SKU (std: DNP)"
        tot["dual"] += card
    elif dnp:
        sku = "DNP"
    else:
        sku = "std"
        tot["std"] += card
        joints += pk * n
        if kind == "extended" and not i.get("pref"):
            ext_types.add(lcsc)
    rows.append(dict(ref=",".join(sorted(refs, key=lambda r: (r[0], int(re.sub(r"\D", "", r))))), adet=n, deger=val,
                     kilif=p["fp"].split(":")[1], lcsc=lcsc, uretici=p["mfr"], mpn=p["mpn"], jlc_tur=kind,
                     stok=i.get("stock"), stok_yeter="evet" if (i.get("stock") or 0) >= 2 * 100 * n else "HAYIR",
                     birim_100set=unit, kart_100set=card if sku != "DNP" else 0.0, sku=sku,
                     lehim_noktasi=pk * n, sicaklik=p["temp"],
                     alt_lcsc=p["alt"].get("ALT LCSC", ""), alt_mpn=p["alt"].get("ALT MPN", ""),
                     not8s=p["extra"].get("8S", ""), aciklama=p["desc"]))
out = REPO / "boards/fmu/bom-revb.csv"
with out.open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
    w.writerow(dict(ref="TOPLAM (std SKU, 100 set)", adet=sum(r["adet"] for r in rows if r["sku"] == "std"),
                    kart_100set=round(tot["std"], 2), lehim_noktasi=joints,
                    aciklama=f"extended tür {len(ext_types)}; Dual SKU farkı J503 +{tot['dual']:.3f} $; "
                             "fiyat/stok JLCPCB parça API 2026-11-11, sıcaklık LCSC parametresi / veri sayfası"))
pcb = 0.25
asm = (8.18 + 1.53 + len(ext_types) * 3.07 + joints * 100 * 0.0016) / 100
print(f"parts std {tot['std']:.2f} $/kart, dual +{tot['dual']:.3f}; ext types {len(ext_types)}; joints {joints}")
print(f"PCB {pcb:.2f}  dizgi {asm:.2f}  -> FMU kart {tot['std'] + pcb + asm:.2f} $ ; stack (+ESC 17.20) {tot['std'] + pcb + asm + 17.20:.2f} $")
print("stok yetmeyen:", [(r['ref'], r['lcsc'], r['stok']) for r in rows if r['stok_yeter'] != 'evet'])
for r in sorted(rows, key=lambda r: -r["kart_100set"])[:12]:
    print(f"  {r['kart_100set']:7.3f}  {r['ref']:<20} {r['mpn']} ({r['lcsc']}) stok {r['stok']}")
