#!/usr/bin/env python3
"""esc55a schematic Rev B: guc-ip03 findings G1, G3-G6, G11-G14, E6/G20, G25.

Reads and rewrites boards/esc55a/esc55a/{esc55a,main,mcu2,mcu}.kicad_sch,
adds the new symbols to lib/{MOS,IC,RLC}.kicad_sym, the new footprints to
lib/stack.pretty and that library to the project's fp-lib-table. The PCB is
not touched (see boards/esc55a/README.md, "Rev B şematik").

  G1   24 MOSFET ME7170 (30 V) -> BLP016N04LC-Q 40 V (ALT NTMFS5C430NLT1G),
       same DFN5x6 footprint MOS:8DFN4.9X5.8
  G3   U12/U22/U32/U42 FD6288Q -> JSM6288Q1 (ALT FD6288Q), same QFN-24
  G4   R00 || R000 (2 x 1 mOhm 2512) -> R00 0.1 mOhm 3920 with Kelvin pads
       (net-tie 1-2 / 3-4); U2 INA199C1 -> INA240A3DR (SOIC-8); U2 inputs
       move to the sense nets isns_p / isns_n (C05 1 nF stays across them);
       REF1 = REF2 = GND, NC pin 4 -> GND; new C06 100 nF on U2 VS
  G5   D00 SMDJ28CA -> SMDJ24CA
  G6   bulk 29 x 22 uF 35 V -> 15 x 10 uF 50 V X7R 1206 (14 removed);
       C02 4.7 uF 35 V 0603 -> 4.7 uF 50 V 0805
  G11  L00 6.8 uH 1210 -> SWPA3015S100MT 10 uH
  G12  new C07 10 uF 16 V 0603 on +3V3 (AMS1117 U0 output)
  G13  new C120/C220/C320/C420 1 uF 25 V 0402 on each driver VCC (PVDD);
       C03 10 uF 10 V 0402 -> 10 uF 16 V 0603
  G14  24 gate resistors 22 Ohm -> 10 Ohm
  E6   R99-R106 (+VD divider, not on the PCB) -> DNP, not on board, values
       3k / 1k
  G25  "max 15V" note -> "PVDD <= 12 V (U0 LDO)"
  all  Value = symbol name, Footprint, Datasheet, MPN, Manufacturer, LCSC
       (and ALT MPN / ALT Manufacturer / ALT LCSC) on every part; the Altium
       fields (MANUFACTURER PRODUCT NUMBER, LSCS PART NUMBER, DIGIKEY ...)
       are removed. Datasheet = lib/datasheet/*_<LCSC>.pdf if present, else
       the LCSC / TI link. Codes: boards/esc55a/bom-maliyet.csv, docs/rapor/guc-ip03.md.

Every step checks the current state first, so running it again changes
nothing; new UUIDs are uuid5 of fixed names, so a run from the same input
gives the same files.

Usage:  python3 tools/esc55a_revb.py
        LC_ALL=C.UTF-8 kicad-cli sch erc boards/esc55a/esc55a/esc55a.kicad_sch
"""

import copy
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sch_edit import Schematic, Str, dump, find, find_all, parse, prop, r4, seed_uuids, new_uuid  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRJ = os.path.join(ROOT, "boards", "esc55a", "esc55a")
LIB = os.path.join(ROOT, "lib")
KICAD_SYM = "/usr/share/kicad/symbols"
KICAD_FP = "/usr/share/kicad/footprints"
LDS = "${KIPRJMOD}/../../../lib/datasheet/"
DS = "https://datasheet.lcsc.com/datasheet/pdf/%s.pdf"
PROJECT = "esc55a"

# ------------------------------------------------------------------ parts
UNIROYAL = DS % "0a975aaa49b7c97f38a963127be4a823"
SAMSUNG = DS % "02336ea48ea44ca18c72517dd3cb7b47"
FH = DS % "09fe2daf22580a99fa7fea93ccb20fb7"


def R(sym, mpn, lcsc, descr):
    return dict(sym=sym, fp="RLC:0402-RES", mpn=mpn, mfr="UNI-ROYAL", lcsc=lcsc, ds=UNIROYAL, descr=descr)


PARTS = {
    "mos": dict(sym="MOS:NMOS 40V BLP016N04LC-Q", fp="MOS:8DFN4.9X5.8", mpn="BLP016N04LC-Q",
                mfr="BL (Shanghai Belling)", lcsc="C49328363", ds=DS % "60e9b7bb6d64f081d184b353ffc14825",
                descr="N-MOSFET 40 V, R_DS(on) 1.6 mΩ maks @10 V, PDFN5x6 (1-3 S, 4 G, 5-8 D); G1, SYS-014",
                alt=("NTMFS5C430NLT1G", "onsemi", "C194661")),
    "drv": dict(sym="MOS:IC MOSDRV JSM6288Q1 24QFN", fp="MOS:QFN-24(4x4)", mpn="JSM6288Q1", mfr="JSMSEMI",
                lcsc="C52196409", ds=DS % "8e66a7cf2679ad9374949075990da53d",
                descr="3 faz kapı sürücü, VCC 5-20 V, UVLO 4.5 V, ölü zaman 200 ns, QFN-24 4x4 (FD6288Q pin uyumlu); G3, SYS-016",
                alt=("FD6288Q", "Fortior Tech", "C328453")),
    "mcu": dict(sym=None, fp="IC:QFN20_3X3_SIL", mpn="EFM8BB21F16G-C-QFN20R", mfr="Silicon Labs", lcsc="C80713",
                ds=LDS + "EFM8BB21F16G-C-QFN20R_C80713.pdf", descr="8 bit MCU 16 kB flash, QFN-20 3x3"),
    "buck": dict(sym=None, fp="IC:SOT23-6", mpn="JW5026SOTB#TRPBF", mfr="JoulWatt", lcsc="C185109",
                 ds=DS % "f83872ed2237628ee0705043f9e45a8d",
                 descr="Buck 1 A, V_IN 4.7-40 V (44 V mutlak), SOT-23-6; PVDD 8.07 V"),
    "ldo": dict(sym=None, fp="IC:SOT89-3", mpn="AMS1117-3.3S", mfr="UMW", lcsc="C347256",
                ds=DS % "40abec897f3661104e2a4d1ebd8e7463",
                descr="LDO 3.3 V 1 A, SOT-89-3; giriş PVDD ≤ 12 V önerilen (15 V mutlak); çıkışta C07 10 µF (G12)"),
    "ina": dict(sym="IC:IC PWR INA240A3D SOIC-8", fp="stack:SOIC-8_3.9x4.9mm_P1.27mm", mpn="INA240A3DR",
                mfr="Texas Instruments", lcsc="C2060584", ds="https://www.ti.com/lit/ds/symlink/ina240.pdf",
                descr="Akım algılama yükselteci x100, V_CM -4...80 V, SOIC-8; R00 0.1 mΩ ile 10 mV/A (ibata_scale 100); G4, SYS-020/021"),
    "shunt": dict(sym="RLC:RES3920_0m1_KELVIN", fp="stack:R_3920_Kelvin_HoLRS3920", mpn="HoLRS3920-10W-0.1mR-1%",
                  mfr="Milliohm", lcsc="C55113241", ds=DS % "f0d59f0eaa1bba956e553f01ceae8df7",
                  descr="Akım şöntü 0.1 mΩ ±%1 10 W 3920, ±100 ppm/K; Kelvin: 2 = isns_p (VBAT ucu), 3 = isns_n (PWR ucu); G4"),
    "tvs": dict(sym="RLC:DTVS_SMDJ24CA", fp="RLC:SMC-TVS", mpn="SMDJ24CA", mfr="DOWO", lcsc="C284061",
                ds=DS % "f3a866763da2bf38848a6c16e1beeff3",
                descr="TVS 3 kW çift yönlü, V_RWM 24 V, V_BR 26.7-29.5 V, V_C 38.9 V @77 A, SMC; G5, SYS-014"),
    "ind": dict(sym="RLC:IND3015_10u", fp="stack:L_Sunlord_SWPA3015S", mpn="SWPA3015S100MT", mfr="Sunlord",
                lcsc="C45403", ds="https://jlcpcb.com/partdetail/C45403",
                descr="10 µH ±%20, I_sat 0.92 A, 3 x 3 x 1.5 mm; G11"),
    "conn": dict(sym=None, fp="CONN:JST_SM08B-SRSS-TB", mpn="XY-SM08B-SRSS-TB", mfr="XYECONN", lcsc="C54582896",
                 ds=DS % "910e382ac20e49fa8135c8269a1a8fef",
                 descr="SH 1.0 mm 8 pin yatay SMD (SM08B-SRSS-TB muadili)",
                 alt=("SM08B-SRSS-TB(LF)(SN)", "JST", "C160407")),
    "diode": dict(sym=None, fp="RLC:SOD-523_0P9X1P3", mpn="1N4148WT", mfr="ST(Semtech)", lcsc="C27748",
                  ds=DS % "d78fb31904624a51a63f8a5d98d2dc04", descr="Hızlı diyot 100 V 150 mA SOD-523 (bootstrap)"),
    "bulk": dict(sym="RLC:CAP1206_10u_50V_X7R", fp="RLC:1206-CAP", mpn="CL31B106KBHNNNE", mfr="Samsung Electro-Mechanics",
                 lcsc="C89632", ds=DS % "a1390a51092e4f3c84866ab492516a00",
                 descr="10 µF ±%10 50 V X7R 1206, bulk (15 adet); G6, SYS-014"),
    "c100n50": dict(sym=None, fp="RLC:0402-CAP", mpn="CL05B104KB54PNC", mfr="Samsung Electro-Mechanics",
                    lcsc="C307331", ds=SAMSUNG, descr="100 nF ±%10 50 V X7R 0402"),
    "c02": dict(sym="RLC:CAP0805_4u7_50V_X5R", fp="stack:C_0805_2012Metric", mpn="CL21A475KBQNNNE",
                mfr="Samsung Electro-Mechanics", lcsc="C98192", ds=DS % "02336ea48ea44ca18c72517dd3cb7b47",
                descr="4.7 µF ±%10 50 V X5R 0805 (JW5026 girişi); G6"),
    "c10u16": dict(sym="RLC:CAP0603_10u_16V_X5R", fp="RLC:0603-CAP", mpn="0603X106K160NT", mfr="FH",
                   lcsc="C70225", ds=FH, descr="10 µF ±%10 16 V X5R 0603; G12/G13"),
    "c100n16": dict(sym="RLC:CAP0402_0u1_16V_X7R", fp="RLC:0402-CAP", mpn="CL05B104KO5NNNC", mfr="Samsung Electro-Mechanics",
                    lcsc="C1525", ds=SAMSUNG, descr="100 nF ±%10 16 V X7R 0402"),
    "c1n": dict(sym=None, fp="RLC:0402-CAP", mpn="0402B102K500NT", mfr="FH", lcsc="C1523", ds=FH,
                descr="1 nF ±%10 50 V X7R 0402 (U2 giriş farkı, isns_p-isns_n)"),
    "c1u": dict(sym="RLC:CAP0402_1u_25V_X5R", fp="RLC:0402-CAP", mpn="CL05A105KA5NQNC",
                mfr="Samsung Electro-Mechanics", lcsc="C52923", ds=SAMSUNG, descr="1 µF ±%10 25 V X5R 0402"),
    "r90k9": R(None, "0402WGF9092TCE", "C26989", "90.9 kΩ ±%1 0402"),
    "r10k": R(None, "0402WGF1002TCE", "C25744", "10 kΩ ±%1 0402"),
    "r220": R(None, "0402WGF2200TCE", "C25091", "220 Ω ±%1 0402"),
    "r22": R(None, "0402WGF220JTCE", "C25092", "22 Ω ±%5 0402"),
    "rgate": R("RLC:RES0402_10", "0402WGF100JTCE", "C25077", "10 Ω ±%5 0402, kapı direnci; G14"),
    "r3k3": R(None, "0402WGF3301TCE", "C25890", "3.3 kΩ ±%1 0402"),
    "r1k": R(None, "0402WGF1001TCE", "C11702", "1 kΩ ±%1 0402"),
    "r3k_dnp": R("RLC:RES0402_3k", "0402WGF3001TCE", "C25784",
                 "3 kΩ ±%1 0402 - DNP (E6/G20): +VD boşta, PCB'de yok"),
    "r1k_dnp": R("RLC:RES0402_1k", "0402WGF1001TCE", "C11702",
                 "1 kΩ ±%1 0402 - DNP (E6/G20): +VD boşta, PCB'de yok"),
    "pad": dict(sym=None, fp=None, mpn="—", mfr="—", lcsc="—", ds="", descr="PCB pedi (dizgi yok)"),
}
NEW_FIELDS = ("MPN", "Manufacturer", "LCSC", "ALT MPN", "ALT Manufacturer", "ALT LCSC")
KEEP_FIELDS = ("Reference", "Value", "Footprint", "Datasheet", "Description") + NEW_FIELDS

BULK_KEEP = ["C%d" % n for n in range(1, 11)] + ["C16", "C17", "C18", "C19", "C48"]
BULK_REMOVE = ["C39", "C36", "C46", "C47", "C38", "C26", "C28", "C27", "C29", "C30", "C37", "C40", "C60", "C50"]
DNP_3K = ["R100", "R102", "R105", "R106"]
DNP_1K = ["R99", "R101", "R103", "R104"]
DRV_CAPS = {"mcu2": [("C120", "C12"), ("C220", "C22")], "mcu": [("C320", "C32"), ("C420", "C42")]}


def classify(ref, lib_id):
    name = lib_id.split(":", 1)[1]
    if ref in ("LOGO",) or lib_id.startswith("CONN:X "):
        return "pad"
    if "ME7170" in name or "BLP016" in name:
        return "mos"
    if "6288Q" in name:
        return "drv"
    for key, word in (("mcu", "EFM8BB21"), ("buck", "JW5026"), ("ldo", "AMS1117"), ("ina", "INA2"), ("ina", "INA199"),
                      ("tvs", "SMDJ"), ("diode", "1N4148")):
        if word in name:
            return key
    fixed = {"R00": "shunt", "L00": "ind", "J0": "conn", "C00": "c100n50", "C01": "c100n50", "C02": "c02",
             "C03": "c10u16", "C07": "c10u16", "C05": "c1n", "C06": "c100n16", "R03": "r22", "R04": "r22"}
    if ref in fixed:
        return fixed[ref]
    if ref in DNP_3K:
        return "r3k_dnp"
    if ref in DNP_1K:
        return "r1k_dnp"
    if ref in BULK_KEEP:
        return "bulk"
    if ref in ("C120", "C220", "C320", "C420") or name.startswith("CAP0402_1u_"):
        return "c1u"
    if "0u1_16V" in name:
        return "c100n16"
    for key, sym in (("r90k9", "RES0402_90k9"), ("r10k", "RES0402_10k"), ("r220", "RES0402_220"),
                     ("rgate", "RES0402_22"), ("rgate", "RES0402_10"), ("r3k3", "RES0402_3k3"), ("r1k", "RES0402_1k")):
        if name == sym:
            return key
    raise SystemExit("unclassified part %s (%s)" % (ref, lib_id))


# ------------------------------------------------------------------ s-expression text helpers

def sexpr_end(text, start):
    depth, i = 0, start
    while True:
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


def lib_get(path, name):
    """Parsed top-level symbol NAME from a .kicad_sym file (None if absent)."""
    text = open(path, encoding="utf-8").read()
    m = re.search(r'\n\t\(symbol "%s"\n' % re.escape(name), text)
    if not m:
        return None
    s = m.start() + 2
    return parse(text[s:sexpr_end(text, s)])


def lib_put(path, node):
    """Write NODE into a .kicad_sym file (replace the symbol of the same name)."""
    text = open(path, encoding="utf-8").read()
    body = dump(node, 1)
    m = re.search(r'\n\t\(symbol "%s"\n' % re.escape(node[1]), text)
    if m:
        s = m.start() + 1
        e = sexpr_end(text, s + 1)
        new = text[:s] + body + text[e:]
    else:
        end = text.rindex("\n)")
        new = text[:end] + "\n" + body + text[end:]
    if new != text:
        open(path, "w", encoding="utf-8").write(new)


def clone_sym(node, old, new, props):
    n = copy.deepcopy(node)
    n[1] = Str(new)
    for sub in find_all(n, "symbol"):
        if sub[1].startswith(old):
            sub[1] = Str(new + sub[1][len(old):])
    for k, v in props.items():
        p = prop(n, k)
        if p is not None:
            p[2] = Str(v)
    return n


# ------------------------------------------------------------------ library symbols

def build_symbols():
    """{"LIB:NAME": node named NAME} for every new symbol; written to lib/LIB.kicad_sym."""
    libp = lambda l: os.path.join(LIB, l + ".kicad_sym")  # noqa: E731
    out = {}

    def add(lib, src_lib, src, name, descr, fp, extra=None):
        node = lib_get(libp(src_lib), src) if src_lib else src
        node = clone_sym(node, node[1], name, {"Value": name, "Description": descr, "Footprint": fp})
        if extra:
            extra(node)
        out["%s:%s" % (lib, name)] = node

    p = PARTS
    add("MOS", "MOS", "NMOS PWR ME7170", p["mos"]["sym"].split(":")[1], p["mos"]["descr"], p["mos"]["fp"])
    add("MOS", "MOS", "IC MOSDRV FD6288Q 24QFN", p["drv"]["sym"].split(":")[1], p["drv"]["descr"], p["drv"]["fp"])

    def ina_pins(node):
        # INA199 (SC70-6) box -> INA240 SOIC-8 numbering; same pin places, two new pins
        remap = {"1": ("7", "REF1"), "2": ("2", "GND"), "3": ("6", "VS"), "4": ("8", "IN+"),
                 "5": ("1", "IN-"), "6": ("5", "OUT")}
        for sub in find_all(node, "symbol"):
            pins = find_all(sub, "pin")
            if not pins:
                continue
            nums = {find(q, "number")[1] for q in pins}
            if "3" in nums and "4" in nums and len(pins) == 8:
                return  # already INA240
            left = right = None
            for q in pins:
                num = find(q, "number")
                new, name = remap[num[1]]
                num[1] = Str(new)
                find(q, "name")[1] = Str(name)
                if new == "7":
                    left = q
                if new == "2":
                    right = q
            for src, num, name in ((left, "3", "REF2"), (right, "4", "NC")):
                q = copy.deepcopy(src)
                at = find(q, "at")
                at[2] = "-5.08"
                find(q, "number")[1] = Str(num)
                find(q, "name")[1] = Str(name)
                sub.append(q)
    add("IC", "IC", "IC PWR INA199C1DCKR SC70-6", p["ina"]["sym"].split(":")[1], p["ina"]["descr"], p["ina"]["fp"],
        ina_pins)

    shunt = lib_get(os.path.join(KICAD_SYM, "Device.kicad_sym"), "R_Shunt")
    add("RLC", None, shunt, "RES3920_0m1_KELVIN", p["shunt"]["descr"], p["shunt"]["fp"])
    for key, src in (("tvs", "DTVS_SMDJ28CA"), ("ind", "IND1210_6u8"), ("bulk", "CAP1206_22u_35V_X5R"),
                     ("c02", "CAP0603_4u7_35V_X5R"), ("c10u16", "CAP0402_10u_10V_X5R"),
                     ("c1u", "CAP0402_1u_16V_X5R"), ("rgate", "RES0402_22"), ("r3k_dnp", "RES0402_3k_????")):
        add("RLC", "RLC", src, p[key]["sym"].split(":")[1], p[key]["descr"], p[key]["fp"])
    for lib_id, node in out.items():
        lib_put(libp(lib_id.split(":")[0]), node)
    return out


# ------------------------------------------------------------------ footprints

KELVIN_FP = """(footprint "R_3920_Kelvin_HoLRS3920"
	(version 20260206)
	(generator "stack_esc55a_revb")
	(layer "F.Cu")
	(descr "Akim sontu 3920 (10 x 5.2 mm), Milliohm HoLRS3920-10W-0.1mR; ped DS s.6 (L 11, A 6.2, B 5.6 mm). Kelvin: 2 / 3 algilama pedleri pad 1 / 4 ic kenarinin ust kosesinde, net-tie 1-2 / 3-4; govde altindan iz gecmez (aciktaki alasim)")
	(tags "shunt kelvin 3920 HoLRS3920")
	(property "Reference" "REF**"
		(at 0 -4.3 0)
		(layer "F.SilkS")
		(effects
			(font
				(size 1 1)
				(thickness 0.15)
			)
		)
	)
	(property "Value" "R_3920_Kelvin_HoLRS3920"
		(at 0 4.3 0)
		(layer "F.Fab")
		(effects
			(font
				(size 1 1)
				(thickness 0.15)
			)
		)
	)
	(attr smd)
	(net_tie_pad_groups "1, 2" "3, 4")
	(duplicate_pad_numbers_are_jumpers no)
	(fp_line
		(start -2.4 -3.4)
		(end 2.4 -3.4)
		(stroke
			(width 0.12)
			(type solid)
		)
		(layer "F.SilkS")
	)
	(fp_line
		(start -2.4 3.4)
		(end 2.4 3.4)
		(stroke
			(width 0.12)
			(type solid)
		)
		(layer "F.SilkS")
	)
	(fp_rect
		(start -5 -2.6)
		(end 5 2.6)
		(stroke
			(width 0.1)
			(type solid)
		)
		(fill no)
		(layer "F.Fab")
	)
	(fp_rect
		(start -5.75 -3.6)
		(end 5.75 3.6)
		(stroke
			(width 0.05)
			(type solid)
		)
		(fill no)
		(layer "F.CrtYd")
	)
	(fp_text user "${REFERENCE}"
		(at 0 0 0)
		(layer "F.Fab")
		(effects
			(font
				(size 1 1)
				(thickness 0.15)
			)
		)
	)
	(pad "1" smd rect
		(at -4.15 0)
		(size 2.7 6.2)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(pad "2" smd rect
		(at -3.05 -2.85)
		(size 0.5 0.5)
		(layers "F.Cu")
	)
	(pad "3" smd rect
		(at 3.05 -2.85)
		(size 0.5 0.5)
		(layers "F.Cu")
	)
	(pad "4" smd rect
		(at 4.15 0)
		(size 2.7 6.2)
		(layers "F.Cu" "F.Mask" "F.Paste")
	)
	(embedded_fonts no)
)
"""
FP_COPY = [("Capacitor_SMD", "C_0805_2012Metric"), ("Package_SO", "SOIC-8_3.9x4.9mm_P1.27mm"),
           ("Inductor_SMD", "L_Sunlord_SWPA3015S")]


def write_if_changed(path, text):
    if not os.path.exists(path) or open(path, encoding="utf-8").read() != text:
        open(path, "w", encoding="utf-8").write(text)


def footprints():
    d = os.path.join(LIB, "stack.pretty")
    os.makedirs(d, exist_ok=True)
    for lib, name in FP_COPY:
        write_if_changed(os.path.join(d, name + ".kicad_mod"),
                         open(os.path.join(KICAD_FP, lib + ".pretty", name + ".kicad_mod"), encoding="utf-8").read())
    write_if_changed(os.path.join(d, "R_3920_Kelvin_HoLRS3920.kicad_mod"), KELVIN_FP)
    table = os.path.join(PRJ, "fp-lib-table")
    text = open(table, encoding="utf-8").read()
    if '(name "stack")' not in text:
        line = ('\t(lib (name "stack")(type "KiCad")(uri "${KIPRJMOD}/../../../lib/stack.pretty")'
                '(options "")(descr "Stack footprints (KiCad copies, Rev B)"))\n')
        text = text[:text.rindex(")")] + line + ")\n"
        open(table, "w", encoding="utf-8").write(text)


# ------------------------------------------------------------------ instance helpers

def ref_of(inst):
    return prop(inst, "Reference")[2]


def has(s, ref):
    try:
        s.inst(ref)
        return True
    except KeyError:
        return False


def libsym_by_id(s, lib_id):
    for n in find_all(s.libsyms, "symbol"):
        if n[1] == lib_id:
            return n
    return None


def sym_pins(node):
    out = []
    for sub in find_all(node, "symbol"):
        for q in find_all(sub, "pin"):
            out.append(str(find(q, "number")[1]))
    return out


def set_lib(s, inst, lib_id, symbols):
    find(inst, "lib_id")[1] = Str(lib_id)
    ln = find(inst, "lib_name")
    if ln:
        inst.remove(ln)
    if lib_id in symbols:
        ensure_cache(s, lib_id, symbols[lib_id])
    node = libsym_by_id(s, lib_id)
    # pin entries follow the symbol's pin numbers (existing UUIDs kept)
    want = sym_pins(node)
    have = {str(q[1]): q for q in find_all(inst, "pin")}
    if sorted(have) == sorted(want):
        return
    pos = inst.index(find_all(inst, "pin")[0]) if have else inst.index(find(inst, "instances"))
    for q in have.values():
        inst.remove(q)
    for i, num in enumerate(want):
        q = have.get(num) or ["pin", Str(num), ["uuid", new_uuid()]]
        inst.insert(pos + i, q)


def ensure_cache(s, lib_id, node):
    n = copy.deepcopy(node)
    n[1] = Str(lib_id)
    old = libsym_by_id(s, lib_id)
    if old is not None:
        if dump(old) == dump(n):
            return
        s.libsyms[s.libsyms.index(old)] = n
    else:
        s.libsyms.append(n)


def set_prop(inst, name, value, hidden=True):
    p = prop(inst, name)
    if p is None:
        at = find(inst, "at")
        p = ["property", Str(name), Str(value), ["at", at[1], at[2], 0]]
        if hidden:
            p.append(["hide", "yes"])
        p += [["show_name", "no"], ["do_not_autoplace", "no"], ["effects", ["font", ["size", 1.27, 1.27]]]]
        last = [q for q in inst if isinstance(q, list) and q[0] == "property"][-1]
        inst.insert(inst.index(last) + 1, p)
    else:
        p[2] = Str(value)


def set_flag(inst, key, value):
    f = find(inst, key)
    f[1] = value


def datasheet(part):
    """lib/datasheet/<...>_<LCSC>.pdf when the repo has it, else the web link."""
    d = os.path.join(LIB, "datasheet")
    if part["lcsc"].startswith("C") and os.path.isdir(d):
        hits = sorted(f for f in os.listdir(d) if f.endswith("_%s.pdf" % part["lcsc"]))
        if hits:
            return LDS + hits[0]
    return part["ds"]


def apply_part(s, inst, symbols):
    ref = ref_of(inst)
    key = classify(ref, find(inst, "lib_id")[1])
    part = PARTS[key]
    if part["sym"] and find(inst, "lib_id")[1] != part["sym"]:
        set_lib(s, inst, part["sym"], symbols)
    lib_id = find(inst, "lib_id")[1]
    # per-instance symbol copy (lib_name) that differs from the library only in drawing -> library symbol
    ln = find(inst, "lib_name")
    if ln and libsym_by_id(s, lib_id) is not None:
        def pin_geo(node):
            return sorted((str(find(q, "number")[1]), tuple(find(q, "at")[1:]))
                          for sub in find_all(node, "symbol") for q in find_all(sub, "pin"))
        if pin_geo(libsym_by_id(s, ln[1])) == pin_geo(libsym_by_id(s, lib_id)):
            inst.remove(ln)
    # drop the Altium fields
    for p in [q for q in inst if isinstance(q, list) and q[0] == "property"]:
        if p[1] not in KEEP_FIELDS:
            inst.remove(p)
    alt = part.get("alt")
    if key != "pad":
        set_prop(inst, "Value", lib_id.split(":", 1)[1], hidden=prop(inst, "Value") is None)
        set_prop(inst, "Footprint", part["fp"])
    set_prop(inst, "Datasheet", datasheet(part))
    set_prop(inst, "Description", part["descr"])
    vals = dict(zip(NEW_FIELDS, (part["mpn"], part["mfr"], part["lcsc"]) + (alt if alt else ("", "", ""))))
    for k in NEW_FIELDS:
        if vals[k]:
            set_prop(inst, k, vals[k])
        elif prop(inst, k) is not None:
            inst.remove(prop(inst, k))
    if key in ("r3k_dnp", "r1k_dnp"):
        set_flag(inst, "dnp", "yes")
        set_flag(inst, "on_board", "no")
        set_flag(inst, "in_bom", "no")
    if key == "pad":
        set_flag(inst, "in_bom", "no")
        set_flag(inst, "in_pos_files", "no")
    return key


def clone_inst(s, tmpl_ref, ref, x, y, rot=None):
    """Copy of a placed symbol at (x, y); properties move with it."""
    t = s.inst(tmpl_ref)
    n = copy.deepcopy(t)
    at = find(n, "at")
    dx, dy = x - float(at[1]), y - float(at[2])
    at[1], at[2] = r4(x), r4(y)
    if rot is not None:
        at[3] = rot
    for p in find_all(n, "property"):
        pa = find(p, "at")
        pa[1], pa[2] = r4(float(pa[1]) + dx), r4(float(pa[2]) + dy)
    find(n, "uuid")[1] = new_uuid()
    for q in find_all(n, "pin"):
        find(q, "uuid")[1] = new_uuid()
    prop(n, "Reference")[2] = Str(ref)
    path = find(find(find(n, "instances"), "project"), "path")
    find(path, "reference")[1] = Str(ref)
    s._insert(n)
    return n


def power_template(s, lib_id, rot):
    for i in s.instances():
        at = find(i, "at")
        if find(i, "lib_id")[1] == lib_id and int(float(at[3])) == rot:
            return ref_of(i)
    raise SystemExit("no %s rot %d on %s" % (lib_id, rot, s.path))


def next_pwr(s, base):
    used = {ref_of(i) for i in s.instances()}
    k = base
    while "#PWR%d" % k in used:
        k += 1
    return "#PWR%d" % k


def add_cap(s, ref, tmpl, x, y, top_net, pwr_base):
    """Vertical capacitor at (x, y) with a power symbol on each pin (top: TOP_NET, bottom: GND)."""
    if has(s, ref):
        return False
    c = clone_inst(s, tmpl, ref, x, y, 0)
    vp = prop(c, "Value")
    if find(vp, "hide") is None:
        vp.insert(4, ["hide", "yes"])
    pins = s.pins(c)
    top = min(pins.values(), key=lambda p: p[1])
    bot = max(pins.values(), key=lambda p: p[1])
    lib_top = {"+8V": "stack:+8V_BAR", "+3V3": "stack:+3V3_BAR"}[top_net]
    clone_inst(s, power_template(s, lib_top, 180), next_pwr(s, pwr_base), top[0], top[1])
    clone_inst(s, power_template(s, "stack:GND_POWER_GROUND", 0), next_pwr(s, pwr_base), bot[0], bot[1])
    return True


def set_text(s, old, new):
    n = 0
    for t in s.items("text"):
        if t[1] == old:
            t[1] = Str(new)
            n += 1
    return n


def has_wire(s, a, b):
    for w in s.items("wire"):
        p = [(r4(float(q[1])), r4(float(q[2]))) for q in find(w, "pts")[1:]]
        if set(p) == {a, b}:
            return True
    return False


def has_text(s, prefix):
    return any(t[1].startswith(prefix) for t in s.items("text"))


def drop_unused_cache(s):
    used = set()
    for i in s.instances():
        ln = find(i, "lib_name")
        used.add(ln[1] if ln else find(i, "lib_id")[1])
    for n in list(find_all(s.libsyms, "symbol")):
        if n[1] not in used:
            s.libsyms.remove(n)


# ------------------------------------------------------------------ sheets

def edit_main(s, symbols, log):
    for r in BULK_REMOVE + ["R000"]:
        if has(s, r):
            s.remove(r)
            log.append("main: %s kaldırıldı" % r)
    # R00 -> Kelvin shunt, vertical (pin 1 top = VBAT, 4 bottom = PWR, 2/3 sense on the right)
    r00 = s.inst("R00")
    at = find(r00, "at")
    if int(float(at[3])) != 0:
        at[3] = 0
        x, y = float(at[1]), float(at[2])
        rp, vp = prop(r00, "Reference"), prop(r00, "Value")
        rp[3] = ["at", r4(x - 2.54), r4(y - 1.27), 0]
        vp[3] = ["at", r4(x - 2.54), r4(y + 1.27), 0]
        for p in (rp, vp):
            eff = find(p, "effects")
            j = find(eff, "justify")
            if j:
                eff.remove(j)
            eff.append(["justify", "right"])
            h = find(p, "hide")
            if h:
                p.remove(h)
    apply_part(s, r00, symbols)
    apply_part(s, s.inst("U2"), symbols)
    removed = s.prune()
    if removed:
        log.append("main: %d sarkan tel/etiket/bağlantı noktası temizlendi" % removed)
    base = s.geometry()
    pins = s.pins(s.inst("R00"))
    for num, net in (("2", "isns_p"), ("3", "isns_n")):
        x, y, _ = pins[num]
        if not any(l[1] == net and (r4(float(find(l, "at")[1])), r4(float(find(l, "at")[2]))) == (r4(x + 2.54), y)
                   for l in s.items("label")):
            s.wire((x, y), (x + 2.54, y))
            s.label(net, x + 2.54, y, 0)
    # U2 inputs: VBAT/PWR labels at the INA -> sense nets
    for l in s.items("label"):
        a = find(l, "at")
        xy = (r4(float(a[1])), r4(float(a[2])))
        if l[1] == "VBAT" and xy == (121.92, 143.51):
            l[1] = Str("isns_p")
        if l[1] == "PWR" and xy == (121.92, 151.13):
            l[1] = Str("isns_n")
    u2 = s.pins(s.inst("U2"))
    for a, b in (("3", "7"), ("4", "2")):  # REF2 -> REF1 (GND), NC -> GND
        pa, pb = u2[a][:2], u2[b][:2]
        if not has_wire(s, pa, pb):
            s.wire(pa, pb)
    # C06 (U2 VS) and C07 (U0 output), free corner left of U2
    if add_cap(s, "C06", "C03", 119.38, 172.72, "+3V3", 101):
        log.append("main: C06 eklendi")
    if add_cap(s, "C07", "C03", 129.54, 172.72, "+3V3", 101):
        log.append("main: C07 eklendi")
    hits = s.collisions(base)
    texts = [
        ("1 tane 1206 cap", "Bulk (Rev B, G6): 15 x 10 µF 50 V X7R 1206"),
        ("23 tane 1206 cap var", "C1-C10, C16-C19, C48"),
        ("low ESR", "Set kondansatörü ≥ 470 µF 35 V, ESR ≤ 50 mΩ"),
        ("22uF 50V", "pil pedinde zorunlu (kutuda, SYS-014)"),
        ("max 15V", "PVDD ≤ 12 V (U0 LDO girişi; G25)"),
    ]
    for old, new in texts:
        set_text(s, old, new)
    if not has_text(s, "R00 Kelvin"):
        s.text("R00 Kelvin (G4): 4 uçlu ayak izi, net-tie 1-2 / 3-4.\n"
               "isns_p / isns_n: R00 ped iç kenarından ayrı ince çift yol,\n"
               "U2 IN+ / IN- (C05 U2'ye yakın). Gövde altından iz yok.\n"
               "CUR = 10 mV/A -> Betaflight ibata_scale 100, offset 0", 115.57, 80.01)
    if not has_text(s, "C06: U2 VS"):
        s.text("C06: U2 VS dekuplaj\nC07: U0 çıkışı (G12)", 134.62, 175.26)
    return hits


def edit_mcu(s, sheet, symbols, log):
    removed = s.prune()
    if removed:
        log.append("%s: %d sarkan tel temizlendi" % (sheet, removed))
    base = s.geometry()
    for ref, near in DRV_CAPS[sheet]:
        x = float(find(s.inst(near), "at")[1]) + 76.2
        if add_cap(s, ref, near, x, 95.25, "+8V", 111 if sheet == "mcu2" else 121):
            log.append("%s: %s eklendi" % (sheet, ref))
        drv = {"C120": "U12", "C220": "U22", "C320": "U32", "C420": "U42"}[ref]
        if not has_text(s, ref + ":"):
            s.text("%s: %s VCC-COM, 1 µF (G13)" % (ref, drv), x - 5.08, 102.87)
    hits = s.collisions(base)
    set_text(s, "Bu direnclere anlam veremedim", "DNP (E6/G20): +VD boşta, PCB'de yok")
    set_text(s, "5-20V ile beslenebiliyor", "JSM6288Q1: VCC 5-20 V, UVLO 4.5 V (G3)")
    return hits


def edit_root(path):
    s = Schematic(path, PROJECT)
    for t in s.items("text"):
        t[1] = Str(t[1].replace("FD6288Q", "JSM6288Q1"))
    tb = find(s.root, "title_block")
    if find(tb, "rev") is None:
        tb.insert(2, ["rev", Str("B")])
    if not [c for c in find_all(tb, "comment") if c[1] == "2"]:
        tb.append(["comment", "2", Str("Rev B şematik: tools/esc55a_revb.py (guc-ip03 G1, G3-G6, G11-G14, E6)")])
    s.save()


def main():
    footprints()
    symbols = build_symbols()
    # lib_symbol_mismatch (Altium import): one copy of these in lib and every cache
    sheets = {}
    for name in ("main", "mcu2", "mcu"):
        path = os.path.join(PRJ, name + ".kicad_sch")
        first = find(Schematic(path, PROJECT).instances()[0], "instances")
        inst_path = find(find(first, "project"), "path")[1]
        sheets[name] = Schematic(path, PROJECT, inst_path)
    for lib_id in ("RLC:CAP0402_0u1_16V_X7R", "RLC:CAP0402_0u1_50V_X7R"):
        node = copy.deepcopy(libsym_by_id(sheets["main"], lib_id))
        node[1] = Str(lib_id.split(":")[1])
        lib_put(os.path.join(LIB, "RLC.kicad_sym"), node)
        symbols[lib_id] = node
        for s in sheets.values():
            if libsym_by_id(s, lib_id) is not None:
                ensure_cache(s, lib_id, node)

    log, counts, hits = [], {}, {}
    for name, s in sheets.items():
        seed_uuids("stack/boards/esc55a/revb/" + name)
        if name == "main":
            hits[name] = edit_main(s, symbols, log)
        else:
            hits[name] = edit_mcu(s, name, symbols, log)
        for inst in s.instances():
            if ref_of(inst).startswith("#"):
                continue
            k = apply_part(s, inst, symbols)
            counts[k] = counts.get(k, 0) + 1
        drop_unused_cache(s)
        s.save()
    edit_root(os.path.join(PRJ, "esc55a.kicad_sch"))

    for line in log:
        print(line)
    print("parça grupları: " + ", ".join("%s %d" % kv for kv in sorted(counts.items())))
    for name, h in hits.items():
        for x in h:
            print("temas (%s): %s" % (name, x))


if __name__ == "__main__":
    main()
