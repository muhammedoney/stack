#!/usr/bin/env python3
"""M1 F405 FMU schematic, drawn from scratch (İP-05).

Writes boards/fmu/fmu/fmu.kicad_sch (root) and the hierarchical pages
power / mcu / sensors / osd / io, adds the symbols it needs to
lib/stack.kicad_sym and the footprints to lib/stack.pretty, and points the
project's sym-lib-table / fp-lib-table at them. boards/fmu/fmu/fmu.kicad_pro
(ERC rules) is not touched. No PCB.

Sources (KRR-006: nothing is copied from reference designs):
  pins / timers      docs/pin-haritasi.md §1 (single source), §2.1, §3
  architecture       docs/mimari-fmu.md §4
  power              docs/rapor/guc-ip03.md §8, G7-G10, G15-G18
  requirements       docs/gereksinimler/sistem.md (SYS-022/023/030...046/050/
                     055...057/060...065/074/087/093/095), KRR-005...008,
                     KRR-011 (ALT rule), KRR-012 (AT32F435 + variants),
                     KRR-013 (LSM6DSV16X)
  target BOM         boards/fmu/bom-hedef.csv + docs/muadil.md §2, §6 (5th step,
                     2026-11-13): TLV62569 3.3 V buck, USB load switch
                     (docs/rapor/guc-tasarruf.md §3.2, §4, §7), B5819W,
                     5 V FB 15 k / 2 k, R111 22 Ω; AT32 pin 31/47
                     (docs/rapor/mcu-secimi.md §3, §4.3)
  symbols            KiCad 10 standard library (/usr/share/kicad/symbols,
                     licence allows reuse) copied into lib/stack.kicad_sym
                     (AT32F435RGTx = KiCad STM32F405RGTx with pins 31/47
                     renamed VCAP_1/PH3, VCAP_2/PH2); SY8303A, AT7456E,
                     LSM6DSV16X (DS13510 Rev 4 Table 2), SPA06-003 (Goertek
                     DS Ver2.0 Table 11) drawn from their data sheets
  footprints         KiCad 10 standard library copied into lib/stack.pretty
  part numbers       boards/fmu/bom-hedef.csv (JLCPCB / LCSC part API,
                     2026-11-13); fields MPN / Manufacturer / LCSC, ALT MPN /
                     ALT Manufacturer / ALT LCSC, ALT2 ..., ALT Note,
                     Temperature, Critical, Exception, Procurement (same
                     names as tools/esc55a_revb.py); BOM: tools/fmu_bom.py

The FMU<->ESC 8 pin order lives in ESC_PINOUT (one table, İP-10 will confirm
it against SpeedyBee F405 V4); change it there and rerun.

Deterministic: every UUID is uuid5 of a fixed name, nothing depends on time
or dict order, so a second run writes byte-identical files.

Usage:  python3 tools/fmu_schematic.py
        LC_ALL=C.UTF-8 kicad-cli sch erc boards/fmu/fmu/fmu.kicad_sch
"""
import math
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "boards/fmu/fmu"
LIB = ROOT / "lib"
KSYM = Path("/usr/share/kicad/symbols")
KFP = Path("/usr/share/kicad/footprints")
PROJECT = "fmu"
DATE = "2026-11-13"
NS = uuid.UUID("6b1f0c52-3c55-4d1e-9a51-6f6d75f40501")


def U(*key):
    return str(uuid.uuid5(NS, "/".join(str(k) for k in key)))


def f(v):
    v = round(v, 3)
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def span(s, i):
    depth, q, j = 0, False, i
    while j < len(s):
        c = s[j]
        if q:
            if c == "\\":
                j += 1
            elif c == '"':
                q = False
        elif c == '"':
            q = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return j + 1
        j += 1
    raise ValueError("unbalanced")


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


# =========================================================== FMU <-> ESC pins
# One table for both ESC connectors (SM08B-SRSS-TB). Today = esc55a J0 order
# (docs/pin-haritasi.md §2.1, "D (şemadan)"); İP-10 / KRR-004 (SpeedyBee F405
# V4) will confirm or change it. Change the order here only.
ESC_PINOUT = (
    (1, "CUR"),
    (2, "TLM"),
    (3, "M4"),
    (4, "M3"),
    (5, "M2"),
    (6, "M1"),
    (7, "VBAT"),
    (8, "GND"),
)
# signal -> net, per connector (pin-haritasi §3 rules)
J_ESC1_NETS = {"CUR": "ESC1_CUR", "TLM": "UART5_RX", "M1": "M1", "M2": "M2", "M3": "M3", "M4": "M4",
               "VBAT": "VBAT", "GND": "GND"}
J_ESC2_NETS = {"CUR": "ESC2_CUR", "TLM": "NC", "M1": "M5", "M2": "M6", "M3": "M7", "M4": "M8",
               "VBAT": "ESC2_VBAT", "GND": "GND"}

# other connectors (FMU side net per pin; device-side order to be confirmed, SYS-065)
J_RX_PINS = ("GND", "+5V", "UART2_RX", "UART2_TX")                       # ELRS/CRSF SH 4
J_DJI_PINS = ("+9V", "GND", "UART1_TX", "UART1_RX", "GND", "SBUS_IN")    # DJI O3/O4 SH 6
J_GPS_PINS = ("+5V", "GND", "UART6_TX", "UART6_RX", "I2C1_SDA", "I2C1_SCL")  # GPS + compass SH 6

# ================================================================== libraries
RAILS = ("GND", "+3V3", "+3V3_IMU", "+5V", "+9V", "VIN", "VBAT", "VBUS")

LCSC_PDF = {
    "C107365": "02336ea48ea44ca18c72517dd3cb7b47", "C11702": "0a975aaa49b7c97f38a963127be4a823",
    "C1337199": "75003a9f5e1e0bf6bd13f6df77b2d757", "C14663": "23ccee80ee542e7cf156a772bb589942",
    "C15127": "fee353dd1e9e0bc90b295f14f381aa4c", "C1524": "09fe2daf22580a99fa7fea93ccb20fb7",
    "C1525": "02336ea48ea44ca18c72517dd3cb7b47", "C1549": "09fe2daf22580a99fa7fea93ccb20fb7",
    "C163128": "74939aaca6654e47bc79adb0bc0bd0a1", "C165948": "9e56b777c022540fcce7c7f67825f55e",
    "C19268151": "e756687f14dbf46d5677223c86053278", "C20917": "130876b936da464599428c58fd8de8f6",
    "C21189": "f42da6c80a0747bae77c2f98f4e46d1d", "C22404005": "33961c2a83e6472c087f377dc608bbe8",
    "C2286": "011ec3e8cb1e825f6961d29bc4db4c7a", "C25076": "0a975aaa49b7c97f38a963127be4a823",
    "C25077": "0a975aaa49b7c97f38a963127be4a823", "C25133": "0a975aaa49b7c97f38a963127be4a823",
    "C25741": "0a975aaa49b7c97f38a963127be4a823", "C25744": "0a975aaa49b7c97f38a963127be4a823",
    "C25764": "0a975aaa49b7c97f38a963127be4a823", "C25854": "0a975aaa49b7c97f38a963127be4a823",
    "C25879": "0a975aaa49b7c97f38a963127be4a823", "C25905": "0a975aaa49b7c97f38a963127be4a823",
    "C2686465": "ec3e308e963624b453a77b63220f4bbf", "C270586": "0a975aaa49b7c97f38a963127be4a823",
    "C27748": "d78fb31904624a51a63f8a5d98d2dc04", "C2827654": "fc4eb899b8e4021ee1843f8c3ea5a928",
    "C2918511": "0f989b6c958f64261e0d3d7b089adbb4", "C2937216": "65ea9869e3fbc8e85f9b73c0af83e582",
    "C307331": "02336ea48ea44ca18c72517dd3cb7b47", "C3232508": "15dca0e4559452abfe61522499f4c603",
    "C380347": "71a9f8eccc4da164324d4a716182c5e3", "C407753": "0a975aaa49b7c97f38a963127be4a823",
    "C42370498": "6fc1fd66376889b0c550201390219a2a", "C49210445": "71a9f8eccc4da164324d4a716182c5e3",
    "C5179501": "c2088cc856fc847412095aab687dd9df", "C51940130": "6afda00944d3960d9ce959d1bdef62f4",
    "C5252682": "ca4d6c85966a5af7ff669d92a1dcc834", "C5360821": "71a9f8eccc4da164324d4a716182c5e3",
    "C54308212": "7a03aa93fd81d2bed1a22512fe4360f9", "C54582896": "910e382ac20e49fa8135c8269a1a8fef",
    "C56123098": "c62fe977e6b7181303e0a13337fff63b", "C6186": "e6935943fc6b1bbf350a1a0f3e90dc4a",
    "C720477": "0475ac02febf455ca9ddcfb380b0df0d", "C7827": "cbb5b11e6f66448a899553349c0f7b2e",
    "C78416": "583465af594625444c284b862ae2ab69", "C82351": "05e3e037fbf1dab52895a7a9e3a9c97c",
    "C89632": "a1390a51092e4f3c84866ab492516a00", "C9008": "a84bd8d530dd46e4b0f6d0ee59d8a89c",
    "C8598": "4ac2c059be7c462694ab0715ce987a85", "C2128": "460cf88f750c4519b4ed435068ee729e",
    "C30589048": "f11af3d36680da63e45f00c5b1db2c97", "C25756": "0a975aaa49b7c97f38a963127be4a823",
    "C4109": "0a975aaa49b7c97f38a963127be4a823", "C25768": "0a975aaa49b7c97f38a963127be4a823",
    "C25092": "0a975aaa49b7c97f38a963127be4a823",
}
LDS = "${KIPRJMOD}/../../../lib/datasheet/"
LOCAL_DS = {
    "C15742": LDS + "STM32F405RGT6.pdf",     # STACKF405 variant of U201
    "C141836": "https://www.ti.com/lit/ds/symlink/tlv62569.pdf",
    "C5267406": "https://www.st.com/resource/en/datasheet/lsm6dsv16x.pdf",
    "C82351": LDS + "MAX7456_AT7456E.pdf",
    "C57254": LDS + "Sunlord-SWPA-series_SWPA3015S100MT_C45403.pdf",
    "C84608": LDS + "Sunlord-SWPA-series_SWPA3015S100MT_C45403.pdf",
}


def datasheet(lcsc):
    if lcsc in LOCAL_DS:
        return LOCAL_DS[lcsc]
    if lcsc in LCSC_PDF:
        return f"https://datasheet.lcsc.com/datasheet/pdf/{LCSC_PDF[lcsc]}.pdf"
    return f"https://www.lcsc.com/product-detail/{lcsc}.html" if lcsc else "~"


# KiCad footprints copied into lib/stack.pretty (key -> (KiCad library, name))
FP = {
    "R0402": ("Resistor_SMD", "R_0402_1005Metric"),
    "R0603": ("Resistor_SMD", "R_0603_1608Metric"),
    "C0402": ("Capacitor_SMD", "C_0402_1005Metric"),
    "C0603": ("Capacitor_SMD", "C_0603_1608Metric"),
    "C0805": ("Capacitor_SMD", "C_0805_2012Metric"),
    "C1206": ("Capacitor_SMD", "C_1206_3216Metric"),
    "C1210": ("Capacitor_SMD", "C_1210_3225Metric"),
    "L0603": ("Inductor_SMD", "L_0603_1608Metric"),
    "LED0603": ("LED_SMD", "LED_0603_1608Metric"),
    "SOD123": ("Diode_SMD", "D_SOD-123"),
    "SOD323": ("Diode_SMD", "D_SOD-323"),
    "SMB": ("Diode_SMD", "D_SMB"),
    "F1206": ("Fuse", "Fuse_1206_3216Metric"),
    "SOT23": ("Package_TO_SOT_SMD", "SOT-23"),
    "SOT23-5": ("Package_TO_SOT_SMD", "SOT-23-5"),
    "SOT23-6": ("Package_TO_SOT_SMD", "SOT-23-6"),
    "TSOT23-8": ("Package_TO_SOT_SMD", "TSOT-23-8"),
    "LQFP64": ("Package_QFP", "LQFP-64_10x10mm_P0.5mm"),
    "SOIC8W": ("Package_SO", "SOIC-8_5.3x5.3mm_P1.27mm"),
    "HTSSOP28": ("Package_SO", "HTSSOP-28-1EP_4.4x9.7mm_P0.65mm_EP2.85x5.4mm"),
    "LGA14": ("Package_LGA", "LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y"),
    "LGA8": ("Package_LGA", "Bosch_LGA-8_2x2.5mm_P0.65mm_ClockwisePinNumbering"),
    "XTAL3225": ("Crystal", "Crystal_SMD_3225-4Pin_3.2x2.5mm"),
    "USBC": ("Connector_USB", "USB_C_Receptacle_HRO_TYPE-C-31-M-12"),
    "SH4": ("Connector_JST", "JST_SH_SM04B-SRSS-TB_1x04-1MP_P1.00mm_Horizontal"),
    "SH6": ("Connector_JST", "JST_SH_SM06B-SRSS-TB_1x06-1MP_P1.00mm_Horizontal"),
    "SH8": ("Connector_JST", "JST_SH_SM08B-SRSS-TB_1x08-1MP_P1.00mm_Horizontal"),
    "SWPA6045": ("Inductor_SMD", "L_Sunlord_SWPA6045S"),
    "SWPA5040": ("Inductor_SMD", "L_Sunlord_SWPA5040S"),
    "L2016": ("Inductor_SMD", "L_Murata_DFE201610P"),
    "BTN": ("Button_Switch_SMD", "SW_SPST_TS-1088-xR020"),
    "TP10": ("TestPoint", "TestPoint_Pad_D1.0mm"),
    "PAD15": ("TestPoint", "TestPoint_Pad_1.5x1.5mm"),
    "PAD25": ("TestPoint", "TestPoint_Pad_2.5x2.5mm"),
    "SJ": ("Jumper", "SolderJumper-2_P1.3mm_Open_RoundedPad1.0x1.5mm"),
}


def fpname(key):
    return "stack:" + FP[key][1]


# --------------------------------------------------------------- KiCad symbols
_KFILES = {}


def _klib(lib):
    if lib not in _KFILES:
        t = (KSYM / f"{lib}.kicad_sym").read_text(encoding="utf-8")
        out, j = {}, t.index("(kicad_symbol_lib") + 1
        while True:
            k = t.find("\n\t(symbol ", j)
            if k < 0:
                break
            k += 2
            e = span(t, k)
            out[re.match(r'\(symbol "([^"]+)"', t[k:]).group(1)] = t[k:e]
            j = e
        _KFILES[lib] = out
    return _KFILES[lib]


def _children(blk):
    out, j = [], blk.index('"', blk.index('"') + 1) + 1
    while True:
        k = blk.find("(", j)
        if k < 0 or k >= len(blk) - 1:
            break
        e = span(blk, k)
        out.append(blk[k:e])
        j = e
    return out


def set_prop(blk, key, value):
    return re.sub(r'(\(property "%s" )"(?:[^"\\]|\\.)*"' % re.escape(key), lambda m: m.group(1) + f'"{esc(value)}"', blk, count=1)


def ksymbol(lib, name, newname, footprint=None):
    """KiCad library symbol, 'extends' flattened, renamed to newname (lib-file form)."""
    syms = _klib(lib)
    blk = syms[name]
    m = re.search(r'\(extends "([^"]+)"\)', blk)
    if m:
        parent = syms[m.group(1)]
        props = [c for c in _children(blk) if c.startswith("(property")]
        pk = [c.replace(f'(symbol "{m.group(1)}_', f'(symbol "{name}_') for c in _children(parent)
              if not c.startswith("(property")]
        blk = f'(symbol "{name}"\n\t\t' + "\n\t\t".join(
            [c for c in pk if not c.startswith("(symbol") and not c.startswith("(embedded_fonts")] + props
            + [c for c in pk if c.startswith("(symbol")] + ["(embedded_fonts no)"]) + "\n\t)"
    blk = blk.replace(f'(symbol "{name}_', f'(symbol "{newname}_').replace(f'(symbol "{name}"', f'(symbol "{newname}"', 1)
    if footprint is not None:
        blk = set_prop(blk, "Footprint", footprint)
    return blk


def power_sym(net):
    if net == "GND":
        return ksymbol("power", "GND", "GND")
    blk = ksymbol("power", "+5V", net)
    blk = set_prop(blk, "Value", net)
    blk = blk.replace('(name "+5V"', f'(name "{net}"')
    return set_prop(blk, "Description", f'Power symbol creates a global label with name "{net}"')


def _pin(etype, x, y, ang, name, num, hide_name=False):
    return (f'\t\t\t(pin {etype} line\n\t\t\t\t(at {f(x)} {f(y)} {ang})\n\t\t\t\t(length 2.54)\n'
            f'\t\t\t\t(name "{esc(name)}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t(size 1.27 1.27)\n'
            f'\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t\t(number "{num}"\n\t\t\t\t\t(effects\n\t\t\t\t\t\t(font\n'
            f'\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)\n')


def _lprop(key, value, x, y, hide=False, just=None):
    j = f"\n\t\t\t\t(justify {just})" if just else ""
    return (f'\t\t(property "{key}" "{esc(value)}"\n\t\t\t(at {f(x)} {f(y)} 0)\n'
            + ("\t\t\t(hide yes)\n" if hide else "")
            + f"\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n"
              f"\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t){j}\n\t\t\t)\n\t\t)\n")


def box_symbol(name, ref, fp, desc, left=(), right=(), top=(), bottom=(), width=20.32):
    """Rectangle symbol drawn from a data sheet. Sides: [(num, name, type) | None (gap)]."""
    rows = max(len(left), len(right), 1)
    h = (rows + 1) * 2.54
    w = max(width, (max(len(top), len(bottom), 1) + 1) * 2.54)
    hw, hh = w / 2, h / 2
    hw, hh = math.ceil(hw / 2.54) * 2.54, math.ceil(hh / 2.54) * 2.54
    pins = ""
    for i, p in enumerate(left):
        if p:
            pins += _pin(p[2], -hw - 2.54, hh - 2.54 * (i + 1), 0, p[1], p[0])
    for i, p in enumerate(right):
        if p:
            pins += _pin(p[2], hw + 2.54, hh - 2.54 * (i + 1), 180, p[1], p[0])
    for i, p in enumerate(top):
        if p:
            pins += _pin(p[2], -hw + 2.54 * (i + 1), hh + 2.54, 270, p[1], p[0])
    for i, p in enumerate(bottom):
        if p:
            pins += _pin(p[2], -hw + 2.54 * (i + 1), -hh - 2.54, 90, p[1], p[0])
    return (f'(symbol "{name}"\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n'
            f"\t\t(in_pos_files yes)\n\t\t(duplicate_pin_numbers_are_jumpers no)\n"
            + _lprop("Reference", ref, -hw, hh + 1.27, just="left bottom")
            + _lprop("Value", name, -hw, -hh - 1.27, just="left top")
            + _lprop("Footprint", fp, 0, 0, hide=True)
            + _lprop("Datasheet", "", 0, 0, hide=True)
            + _lprop("Description", desc, 0, 0, hide=True)
            + f'\t\t(symbol "{name}_0_1"\n\t\t\t(rectangle\n\t\t\t\t(start {f(-hw)} {f(hh)})\n\t\t\t\t(end {f(hw)} {f(-hh)})\n'
              f"\t\t\t\t(stroke\n\t\t\t\t\t(width 0.254)\n\t\t\t\t\t(type default)\n\t\t\t\t)\n\t\t\t\t(fill\n"
              f"\t\t\t\t\t(type background)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n"
            + f'\t\t(symbol "{name}_1_1"\n{pins}\t\t)\n\t\t(embedded_fonts no)\n\t)')


PI, PO, BI, PW, PWO, PS, NCT, OC = ("input", "output", "bidirectional", "power_in", "power_out", "passive",
                                    "no_connect", "open_collector")

SYMBOLS = {}  # name -> lib-file block (managed by this script)
EXTERNAL = {}  # symbols already in lib/stack.kicad_sym, used as they are (PWR_FLAG)


def existing_symbol(name):
    t = (LIB / "stack.kicad_sym").read_text(encoding="utf-8")
    a = t.index(f'\n\t(symbol "{name}"\n') + 2
    EXTERNAL[name] = t[a:span(t, a)]


def build_symbols():
    k = {
        "R": ("Device", "R"), "C": ("Device", "C"), "L": ("Device", "L"),
        "FerriteBead_Small": ("Device", "FerriteBead_Small"), "D_Schottky": ("Device", "D_Schottky"),
        "D_Zener": ("Device", "D_Zener"), "D_TVS": ("Device", "D_TVS"), "D": ("Device", "D"),
        "LED": ("Device", "LED"), "Fuse": ("Device", "Fuse"), "Crystal_GND24": ("Device", "Crystal_GND24"),
        "TestPoint": ("Connector", "TestPoint"), "SolderJumper_2_Open": ("Jumper", "SolderJumper_2_Open"),
        "SW_Push": ("Switch", "SW_Push"), "Conn_01x04": ("Connector_Generic", "Conn_01x04"),
        "Conn_01x06": ("Connector_Generic", "Conn_01x06"), "Conn_01x08": ("Connector_Generic", "Conn_01x08"),
        "AO3401A": ("Transistor_FET", "AO3401A"), "AO3400A": ("Transistor_FET", "AO3400A"),
        "MMBT3904": ("Transistor_BJT", "MMBT3904"),
        "TLV62569DBV": ("Regulator_Switching", "TLV62569DBV"), "USBLC6-2SC6": ("Power_Protection", "USBLC6-2SC6"),
        "USB_C_Receptacle_USB2.0_16P": ("Connector", "USB_C_Receptacle_USB2.0_16P"),
        "74LVC1G04": ("74xGxx", "74LVC1G04"), "W25Q128JVS": ("Memory_Flash", "W25Q128JVS"),
    }
    fpd = {"AO3401A": "SOT23", "AO3400A": "SOT23", "MMBT3904": "SOT23", "TLV62569DBV": "SOT23-5",
           "USBLC6-2SC6": "SOT23-6", "USB_C_Receptacle_USB2.0_16P": "USBC", "74LVC1G04": "SOT23-5",
           "W25Q128JVS": "SOIC8W"}
    for name, (lib, src) in k.items():
        SYMBOLS[name] = ksymbol(lib, src, name, fpname(fpd[name]) if name in fpd else None)
    # MCU (KRR-012): KiCad STM32F405RGTx, pins 31/47 carry both names. AT32F435RGT7 has PH3/PH2 there
    # (AT32F435/437 DS v2.01 pin table, LQFP64 31 PH3, 47 PH2); STM32F405RG / APM32F405RG VCAP_1/VCAP_2.
    blk = ksymbol("MCU_ST_STM32F4", "STM32F405RGTx", "AT32F435RGTx", fpname("LQFP64"))
    for old, new in (("VCAP_1", "VCAP_1/PH3"), ("VCAP_2", "VCAP_2/PH2")):
        assert blk.count(f'(name "{old}"') == 1
        blk = blk.replace(f'(name "{old}"', f'(name "{new}"')
    blk = set_prop(blk, "Value", "AT32F435RGTx")
    blk = set_prop(blk, "Datasheet", "https://www.lcsc.com/product-detail/C3029577.html")
    blk = set_prop(blk, "Description",
                   "Artery AT32F435RGT7 Arm Cortex-M4F 288 MHz, 1 MB flash, 384 KB RAM, LQFP64; same footprint "
                   "and pins as STM32F405RG / APM32F405RG except pin 31 VCAP_1/PH3, pin 47 VCAP_2/PH2 "
                   "(derived from KiCad STM32F405RGTx, mcu-secimi §3.1)")
    blk = set_prop(blk, "ki_keywords", "Arm Cortex-M4 AT32F435 STM32F405 APM32F405")
    SYMBOLS["AT32F435RGTx"] = blk
    for net in RAILS:
        SYMBOLS[net] = power_sym(net)
    existing_symbol("PWR_FLAG")
    # ---- drawn from data sheets
    SYMBOLS["SY8303A"] = box_symbol(
        "SY8303A", "U", fpname("TSOT23-8"),
        "Silergy SY8303A 40 V 3 A sync buck, TSOT23-8 (DS Rev 0.9A pinout p.2; VFB 0.6 V, Fsw = 1e5/RFS[k])",
        left=[(5, "IN", PW), (8, "EN", PI), (2, "FS", PS)],
        right=[(7, "BS", PS), (6, "LX", PWO), (1, "FB", PI)],
        bottom=[(3, "GND", PW), (4, "GND", PS)], width=12.7)
    SYMBOLS["AT7456E"] = box_symbol(
        "AT7456E", "U", fpname("HTSSOP28"),
        "AT7456E (MAX7456 pin compatible) OSD, TSSOP-28 + EP (MAX7456 DS pin description p.9)",
        left=[(8, "~{CS}", PI), (10, "SCLK", PI), (9, "SDIN", PI), (11, "SDOUT", "tri_state"), (19, "~{RESET}", PI),
              None, (5, "CLKIN", PI), (6, "XFB", PO), (7, "CLKOUT", PO), None, (1, "NC", NCT), (2, "NC", NCT),
              (13, "NC", NCT), (14, "NC", NCT)],
        right=[(22, "VIN", PI), (26, "VOUT", PO), (25, "SAG", PI), None, (12, "LOS", OC), (17, "~{VSYNC}", OC),
               (18, "~{HSYNC}", OC), None, None, None, (15, "NC", NCT), (16, "NC", NCT), (27, "NC", NCT),
               (28, "NC", NCT)],
        top=[(3, "DVDD", PW), (21, "AVDD", PW), (24, "PVDD", PW)],
        bottom=[(4, "DGND", PW), (20, "AGND", PW), (23, "PGND", PW), (29, "EP", PS)], width=17.78)
    SYMBOLS["LSM6DSV16X"] = box_symbol(
        "LSM6DSV16X", "U", fpname("LGA14"),
        "ST LSM6DSV16X 6-axis IMU, LGA-14L 2.5x3x0.83 (DS13510 Rev 4 §3 Fig. 5, Table 2); same pinout "
        "LSM6DSK320X (DB5732 Rev 1 Table 1)",
        left=[(12, "CS", PI), (13, "SCL/SPC", PI), (14, "SDA/SDI", BI), (1, "SDO/SA0", PO)],
        right=[(4, "INT1", PO), (9, "INT2", PO), None, (2, "SDx", PS), (3, "SCx", PS), (10, "OCS_Aux", PS),
               (11, "SDO_Aux", PS)],
        top=[(8, "Vdd", PW), (5, "Vdd_IO", PW)],
        bottom=[(6, "GND", PW), (7, "GND", PW)], width=17.78)
    SYMBOLS["SPA06-003"] = box_symbol(
        "SPA06-003", "U", fpname("LGA8"),
        "Goertek SPA06-003 barometer, LGA-8 2.0x2.5 P0.65 (DS Ver2.0 §8.1 Table 11); same pinout "
        "Tokmas DPS368 / Infineon DPS368",
        left=[(2, "CSB", PI), (4, "SCK", PI), (3, "SDA", BI), (5, "SDO", BI)],
        top=[(8, "VDD", PW), (6, "VDDIO", PW)],
        bottom=[(1, "GND", PW), (7, "GND", PW)], width=12.7)


def lib_pins(name):
    """pin number -> (x, y, angle, type) for unit 1 (and common unit 0)."""
    blk = SYMBOLS[name]
    out = {}
    for sm in re.finditer(r'\(symbol "[^"]*_(\d+)_(\d+)"', blk):
        if sm.group(1) not in ("0", "1"):
            continue
        sub = blk[sm.start():span(blk, sm.start())]
        for m in re.finditer(r'\(pin (\w+) \w+\s*\(at ([-\d.]+) ([-\d.]+) (\d+)\)[\s\S]*?\(number "([^"]+)"', sub):
            out[m.group(5)] = (float(m.group(2)), float(m.group(3)), int(m.group(4)), m.group(1))
    return out


def write_library():
    path = LIB / "stack.kicad_sym"
    t = path.read_text(encoding="utf-8")
    for name in sorted(SYMBOLS):
        blk = SYMBOLS[name]
        m = re.search(r'\n\t\(symbol "%s"\n' % re.escape(name), t)
        if m:
            a = m.start() + 2
            e = span(t, a)
            if t[a:e] != blk:
                t = t[:a] + blk + t[e:]
        else:
            end = t.rstrip().rindex(")")
            t = t[:end].rstrip("\n") + "\n\t" + blk + "\n" + t[end:]
    write_if_changed(path, t)


def write_footprints():
    out = LIB / "stack.pretty"
    for lib, name in FP.values():
        dst = out / f"{name}.kicad_mod"
        if dst.exists():
            continue  # keep what is there (e.g. C_0805_2012Metric from the esc55a work)
        dst.write_text((KFP / f"{lib}.pretty" / f"{name}.kicad_mod").read_text(encoding="utf-8"), encoding="utf-8")


def write_if_changed(path, text):
    path = Path(path)
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")


def write_lib_tables():
    sym = BOARD / "sym-lib-table"
    t = sym.read_text(encoding="utf-8")
    if '(name "stack")' not in t:
        t = t.rstrip().rstrip(")") + ('\t(lib (name "stack")(type "KiCad")(uri "${KIPRJMOD}/../../../lib/stack.kicad_sym")'
                                      '(options "")(descr "Stack stack symbols"))\n)\n')
        write_if_changed(sym, t)
    fpt = BOARD / "fp-lib-table"
    t = fpt.read_text(encoding="utf-8")
    if '(name "stack")' not in t:
        t = t.rstrip().rstrip(")") + ('\t(lib (name "stack")(type "KiCad")(uri "${KIPRJMOD}/../../../lib/stack.pretty")'
                                      '(options "")(descr "Stack footprints (KiCad standard copies + own)"))\n)\n')
        write_if_changed(fpt, t)


# ====================================================================== parts
T_R = "-55…+155 °C (UNI-ROYAL thick film, LCSC)"
T_X7R = "X7R -55…+125 °C (EIA)"
T_C0G = "C0G -55…+125 °C (EIA)"
PARTS = {}


# Field names and order as tools/esc55a_revb.py (hedef BOM, KRR-011)
ALT_FIELDS = ("ALT MPN", "ALT Manufacturer", "ALT LCSC", "ALT2 MPN", "ALT2 Manufacturer", "ALT2 LCSC", "ALT Note")
TAIL_FIELDS = ("Temperature", "Critical", "Exception", "Procurement")


def ALT(mpn, mfr, lcsc, note="", alt2=None):
    """ALT fields (boards/fmu/bom-hedef.csv alt_mpn / alt_uretici / alt_lcsc; ALT2 from drop_in_kaniti)."""
    d = {"ALT MPN": mpn, "ALT Manufacturer": mfr, "ALT LCSC": lcsc, "ALT Note": note}
    if alt2:
        d.update(zip(("ALT2 MPN", "ALT2 Manufacturer", "ALT2 LCSC"), alt2))
    return {k: v for k, v in d.items() if v}


def part(ref, sym, value, fpkey, lcsc, mpn, mfr, temp, desc="", dnp=False, bom=True, alt=None, extra=None,
         crit=False, exc="", proc=""):
    assert ref not in PARTS, f"duplicate reference {ref}"
    assert re.fullmatch(r"(U|C|R|L|D|Q|J|F|Y|FB|SW|SJ|TP)[1-5]\d\d", ref), f"reference {ref} not 1xx…5xx"
    PARTS[ref] = dict(sym=sym, value=value, fp=fpname(fpkey) if fpkey else "", lcsc=lcsc, mpn=mpn, mfr=mfr,
                      temp=temp, desc=desc, dnp=dnp, bom=bom, alt=alt or {}, extra=extra or {}, ds=datasheet(lcsc),
                      crit=crit, exc=exc, proc=proc)


RES = {  # value -> (lcsc, mpn, footprint)
    "75": ("C25133", "0402WGF750JTCE", "R0402"),
    "100": ("C25076", "0402WGF1000TCE", "R0402"), "1k": ("C11702", "0402WGF1001TCE", "R0402"),
    "2.2k": ("C25879", "0402WGF2201TCE", "R0402"), "5.1k": ("C25905", "0402WGF5101TCE", "R0402"),
    "7.15k": ("C270586", "0402WGF7151TCE", "R0402"), "10k": ("C25744", "0402WGF1002TCE", "R0402"),
    "15k": ("C25756", "0402WGF1502TCE", "R0402"), "2k": ("C4109", "0402WGF2001TCE", "R0402"),
    "22k": ("C25768", "0402WGF2202TCE", "R0402"), "22": ("C25092", "0402WGF220JTCE", "R0402"),
    "100k": ("C25741", "0402WGF1003TCE", "R0402"),
    "200k": ("C25764", "0402WGF2003TCE", "R0402"), "10k 0.5%": ("C407753", "0402WGD1002TCE", "R0402"),
}


def R(ref, value, desc="", **kw):
    if value == "140k 0.5%":
        part(ref, "R", value, "R0402", "C2686465", "ARG02DTC1403", "Viking Tech",
             "-55…+155 °C (Viking ARG thin film, LCSC)", desc, **kw)
        return
    if value == "0":
        part(ref, "R", "0", "R0603", "C21189", "0603WAF0000T5E", "UNI-ROYAL", T_R, desc, **kw)
        return
    lcsc, mpn, fp = RES[value]
    part(ref, "R", value, fp, lcsc, mpn, "UNI-ROYAL", T_R, desc, **kw)


CAPS = {  # value -> (lcsc, mpn, manufacturer, footprint, temp)
    "100nF 16V": ("C1525", "CL05B104KO5NNNC", "Samsung", "C0402", T_X7R),
    "100nF 50V": ("C307331", "CL05B104KB54PNC", "Samsung", "C0402", T_X7R),
    "100nF 50V 0603": ("C14663", "CC0603KRX7R9BB104", "YAGEO", "C0603", T_X7R),
    "18pF C0G": ("C1549", "0402CG180J500NT", "FH", "C0402", T_C0G),
    "22pF C0G": ("C1555", "0402CG220J500NT", "FH", "C0402", T_C0G),
    "2.2uF 16V": ("C5360821", "TCC0603X7R225K160CT", "CCTC", "C0603", T_X7R),
    "10uF 16V": ("C380347", "TCC0805X7R106K160FT", "CCTC", "C0805", T_X7R),
    "10uF 50V": ("C89632", "CL31B106KBHNNNE", "Samsung", "C1206", T_X7R),
    "22uF 16V": ("C5252682", "CS3216X7R226K160NRI", "Samwha", "C1206", T_X7R),
    "22uF 25V": ("C2918511", "CS3225X7R226K250NRL", "Samwha", "C1210", T_X7R),
}


def C(ref, value, desc="", **kw):
    lcsc, mpn, mfr, fp, temp = CAPS[value]
    v = value.replace(" 0603", "") + (" X7R" if "C0G" not in value else "")
    part(ref, "C", v, fp, lcsc, mpn, mfr, temp, desc, **kw)


def TP(ref, value, fpkey="TP10", desc=""):
    part(ref, "TestPoint", value, fpkey, "", "", "", "—", desc or "Ped / test noktası (BOM dışı)", bom=False)


V8S = "8S BOM varyantı (KRR-007, SYS-046): "


def define_parts():
    # ---------------------------------------------------------------- power
    TP("J101", "BAT+", "PAD25", "Pil + lehim pedi, F101/Q101 ÖNCESİ, J_ESC1.VBAT ile aynı düğüm (SYS-062, G16/G17), 22 AWG")
    TP("J102", "BAT-", "PAD25", "Pil − lehim pedi (GND), 22 AWG")
    part("F101", "Fuse", "5A 32V", "F1206", "C163128", "CFS12V3T5R0", "TA-I Tech", "-20…+105 °C (LCSC)",
         "Hızlı sigorta 5 A, 32 V DC, kesme 50 A (guc-ip03 §8.1). 3S tam yük 3.0 A = %60",
         alt=ALT("0466005.NRHF", "Littelfuse", "C57525", "1206, 5 A, 32 V, kesme 50 A, −55…90 °C (TA-I CFS12 DS / "
                 "Littelfuse 0466 DS)"), crit=True,
         extra={"8S": V8S + "≥ 50 V DC sigorta, aynı 1206 ayak izi aranacak (bom-tedarik)"})
    ao3401 = dict(lcsc="C15127", mpn="AO3401A", mfr="Alpha & Omega Semicon", temp="T_J -55…+150 °C (DS)",
                  alt=ALT("AO3401A", "UMW(Youtai Semiconductor Co., Ltd.)", "C347476",
                          "SOT-23 1 G 2 S 3 D, −30 V, 50 mΩ @10 V (AOS DS / UMW DS)"), crit=True)
    part("Q101", "AO3401A", "AO3401A", "SOT23",
         desc="Ters kutup P-MOS: D pil (F101) tarafında, S VIN'de (G8). V_DS -30 V ≥ 26.1 V (SYS-074). 3S tam yükte "
              "0.45 W → ped yolu (G16); JSM7409 (DFN3.3) ayak izi farklı, ALT değil",
         extra={"8S": V8S + "-40…-60 V P-MOS (aday seçilecek)"}, **ao3401)
    part("D101", "D_Zener", "10V", "SOD323", "C42370498", "MM3Z10VT1G-TP", "TECH PUBLIC", "T_J -55…+150 °C (LCSC)",
         "Q101 V_GS kıskacı: K = S (VIN), A = G; |V_GS| ≤ 10.6 V < 12 V",
         alt=ALT("MM3Z10VT1G", "onsemi", "C39057"))
    R("R101", "100k", "Q101 kapı → GND (açılış); zener akımı (35-10)/100k = 0.25 mA")
    part("D102", "D_TVS", "SMBJ24CA", "SMB", "C78416", "SMBJ24CA", "Brightking", "T_J -55…+150 °C (DS)",
         "VIN geçici bastırıcı, çift yönlü, V_RWM 24 V, V_BR ≥ 26.7 V, V_C 38.9 V < 40 V (SYS-044)",
         alt=ALT("SMBJ24CA", "Littelfuse", "C83268", "SMB, V_C 38.9 V @15.5 A < 40 V (Brightking / Littelfuse DS)"),
         crit=True, extra={"8S": V8S + "SMBJ36CA sınıfı (V_C ≈ 58 V, 60 V buck ile)"})
    for ref in ("C101", "C102"):
        C(ref, "10uF 50V", "VIN, her SY8303 IN pinine yakın (≥ 4.7 µF, DS)",
          extra={"8S": V8S + "63-100 V 1206/1210 X7R"})
    C("C103", "100nF 50V 0603", "VIN giriş HF", extra={"8S": V8S + "100 V"})
    C("C104", "100nF 50V", "U101 IN HF")
    C("C105", "100nF 50V", "U102 IN HF")
    sy = dict(lcsc="C2937216", mpn="SY8303AAIC", mfr="Silergy Corp", temp="T_A -40…+105 °C, T_J 150 °C (DS, LCSC)",
              alt=ALT("SY8303AIC", "Silergy Corp", "C97054",
                      "Aynı pin (FB, FS, GND, GND, IN, LX, BS, EN), V_REF 0.591–0.609 V, F_SW = 105/R_FS "
                      "(SY8303A DS s.1–4 / SY8303AIC DS s.1–3)"),
              crit=True, exc="İSTİSNA (tek üretici Silergy): FS pinli TSOT-23-8 40 V 3 A başka üretici yok; ALT farklı "
                             "sipariş kodu (muadil §3 İ4)",
              proc="İsteğe bağlı 220 adet peşin alım (muadil §4); stok izleme")
    part("U101", "SY8303A", "SY8303AAIC", "TSOT23-8", desc="5 V / 2 A BEC (G7, B4). VFB 0.600 V ±1.5 %; "
         "Vout = 0.6 × (1 + 15k/2k) = 5.10 V (+5V_BUCK, Q102 yük anahtarından önce); RFS 200k → 500 kHz",
         extra={"8S": V8S + "60-65 V buck (TPS54360B / LMR16030 / MP9486A), ayak izi farklı → PCB yer payı"}, **sy)
    part("U102", "SY8303A", "SY8303AAIC", "TSOT23-8", desc="9 V / 1.5 A BEC (G7). Vout = 0.6 × (1 + 100k/7.15k) = "
         "8.99 V; EN ← PB11 PINIO1 (yüksek = açık, 100k çekme ile varsayılan açık)",
         extra={"8S": V8S + "60-65 V buck, U101 ile aynı"}, **sy)
    R("R102", "100k", "U101 EN → VIN (her zaman açık; EN mutlak 40 V)")
    R("R103", "200k", "U101 FS: 500 kHz")
    R("R104", "15k", "U101 FB üst (+5V_BUCK) — B4 (guc-tasarruf §4)")
    R("R105", "2k", "U101 FB alt → 5.10 V (en kötü 4.94–5.27 V, RSS 4.98–5.22 V; guc-tasarruf §4)")
    C("C106", "100nF 16V", "U101 BS-LX")
    part("L101", "L", "6.8uH", "SWPA6045", "C57254", "SWPA6045S6R8MT", "Sunlord", "-40…+125 °C öz ısınma dahil (DS)",
         "5 V bobini: I_sat 4.3 A, I_rms 3 A, 31 mΩ; tepe 2.6 A (%60) (G10)",
         alt=ALT("FNR6045S6R8MT", "cjiang (Changjiang Microelectronics Tech)", "C168072",
                 "6×6, 6.8 µH, I_sat 4.3 A, 40 mΩ (Sunlord SWPA DS / cjiang FNR DS s.1)"), crit=True)
    C("C107", "22uF 16V", "+5V_BUCK çıkış (buck tarafı, FB burada — döngü değişmez)")
    C("C108", "22uF 16V", "+5V_BUCK çıkış")
    R("R106", "100k", "EN_9V → +3V3: MCU sıfırda 9 V açık (PINIO1 varsayılanı)")
    R("R107", "1k", "PB11 → EN_9V seri koruma")
    R("R108", "200k", "U102 FS: 500 kHz")
    R("R109", "100k", "U102 FB üst")
    R("R110", "7.15k", "U102 FB alt → 8.99 V")
    C("C109", "100nF 16V", "U102 BS-LX")
    part("L102", "L", "10uH", "SWPA5040", "C84608", "SWPA5040S100MT", "Sunlord", "-40…+125 °C öz ısınma dahil (DS)",
         "9 V bobini: I_sat 2.9 A, I_rms 2.1 A, 83 mΩ; tepe %72 (G10)",
         alt=ALT("FNR5040S100MT", "cjiang (Changjiang Microelectronics Tech)", "C167967",
                 "KOŞULLU: 5×5, 10 µH, 83 mΩ; FNR5040 I_sat 2.35/2.7 A teyit edilecek (tepe 2.09 A)"), crit=True)
    C("C110", "22uF 25V", "+9V çıkış")
    C("C111", "22uF 25V", "+9V çıkış")
    # USB load switch (guc-tasarruf §3.2): R_a = R117, R_b = R118 in bom-hedef.csv
    part("Q102", "AO3401A", "AO3401A", "SOT23",
         desc="5 V yük anahtarı (guc-tasarruf §3.2): D (3) = +5V_BUCK, S (2) = +5V rayı; gövde diyodu buck → ray "
              "iletir, ray → buck bloke eder → yalnız USB'de VIN = 0 V. 2 A'da 0.12 V, 0.24 W", **ao3401)
    part("Q103", "MMBT3904", "MMBT3904", "SOT23", "C20526", "MMBT3904(RANGE:100-300)",
         "Jiangsu Changjing Electronics Technology Co., Ltd.", "T_J -55…+150 °C (LCSC)",
         "Q102 kapı sürücü: C = Q102.G, E = GND, B ← R118 ← VIN; VIN ≥ 1.5 V → Q102 açık (V_GS ≈ −5 V)",
         alt=ALT("MMBT3904LT1G", "onsemi", "C81464", "SOT-23 1 B 2 E 3 C, 40 V (CJ / onsemi DS)"))
    R("R117", "100k", "R_a (bom-hedef): Q102 G–S (+5V), anahtarı kapalı tutar")
    R("R118", "100k", "R_b (bom-hedef): VIN → Q103 baz; I_B 83 µA @3S, 0.34 mA @35 V")
    # 3.3 V buck (guc-tasarruf §7.2): R_FB3V3H = R119, R_FB3V3L = R120 in bom-hedef.csv
    part("U103", "TLV62569DBV", "TLV62569DBVR", "SOT23-5", "C141836", "TLV62569DBVR", "Texas Instruments",
         "T_J -40…+125 °C (DS SLVSDG1C)",
         "3.3 V senk. buck 2 A, 1.5 MHz, V_IN 2.5–5.5 V; 1 EN 2 GND 3 SW 4 VIN 5 FB; V_FB 0.6 V → "
         "0.6 × (1 + 100k/22k) = 3.327 V (3.21–3.45 V); yük ≈ 240 mA + AT32 payı (guc-tasarruf §7, mcu-secimi §4.3-8)",
         alt=ALT("SY8089A1AAC", "Silergy Corp", "C479074",
                 "SOT-23-5 1 EN 2 GND 3 LX 4 IN 5 FB (TLV62569 SLVSDG1C §5 / SY8089A1 DS s.1); V_FB 0.6 V; aynı "
                 "2.2 µH + 22 µF + 100 k/22 k (guc-tasarruf §7.2)"), crit=True)
    part("L103", "L", "2.2uH", "L2016", "C97005", "WPN201610H2R2MT", "Sunlord", "-40…+125 °C (LCSC)",
         "3.3 V buck bobini 2.2 µH, I_sat 2.15 A, I_r 1.45 A, 170 mΩ; tepe 0.48 A (%23). Ayak izi KiCad "
         "DFE201610P (2016) — Sunlord WPN ped kesişimi pcb-muhendisi",
         alt=ALT("DFE201612P-2R2M=P2", "Murata Electronics", "C79317",
                 "2.0×1.6 mm, 2.2 µH, I_sat 2.15/2.1 A (Sunlord WPN DS / Murata DFE201612P DS; ped kesişimi pcb)"),
         crit=True)
    C("C112", "10uF 16V", "U103 C_IN (VIN pinine yakın)")
    C("C113", "22uF 16V", "U103 C_OUT (3.3 V'ta ≈ 15 µF etkin; TI ve SY tablolarının kesişimi)")
    R("R119", "100k", "R_FB3V3H (bom-hedef): U103 FB üst")
    R("R120", "22k", "R_FB3V3L (bom-hedef): U103 FB alt → 3.327 V")
    C("C119", "22pF C0G", "C_FF pedi, DNP (TI 6.8 pF / SY 22 pF isteğe bağlı; guc-tasarruf §7.2)", dnp=True)
    R("R111", "22", "IMU besleme süzgeci 22 Ω × 2.2 µF → 3.3 kHz (guc-tasarruf §7.3, SYS-042)")
    C("C114", "2.2uF 16V", "IMU süzgeci +3V3_IMU toplu (R111 ile f_c 3.3 kHz)")
    C("C115", "100nF 16V", "LSM6DSV16X Vdd_IO (pin 5) C2 100 nF — pin 5'e yakın (DS13510 §7.1)")
    R("R112", "140k 0.5%", "VBAT bölücü üst: 15:1, tam ölçek 49.5 V (SYS-022, ≥ 45 V)")
    R("R113", "10k 0.5%", "VBAT bölücü alt")
    C("C116", "100nF 16V", "ADC_VBAT süzgeci (PC0)")
    R("R114", "10k", "ESC1 akım → PC1 (SJ101 kapalıyken 10k/10k ortalama)")
    C("C117", "100nF 16V", "ADC_CURR1 süzgeci")
    R("R115", "1k", "ESC2 akım → PC5 seri (SYS-023, MCU koruma: (5-3.6)/1k = 1.4 mA)")
    C("C118", "100nF 16V", "ADC_CURR2 süzgeci")
    part("SJ101", "SolderJumper_2_Open", "SJ_CUR_AVG", "SJ", "", "", "", "—",
         "Varsayılan AÇIK. Kapatılırsa CUR2 → 10k → PC1: Betaflight tek girişte iki ESC ortalaması (SYS-023)", bom=False)
    R("R116", "10k", "SJ101 → PC1 ortalama direnci")
    TP("TP101", "VBAT", desc="Test noktası VIN (koruma sonrası pil) (SYS-093)")
    TP("TP102", "5V", desc="Test noktası +5V")
    TP("TP103", "9V", desc="Test noktası +9V")
    TP("TP104", "3V3", desc="Test noktası +3V3")
    TP("TP105", "GND", desc="Test noktası GND")

    # ------------------------------------------------------------------ mcu
    part("U201", "AT32F435RGTx", "AT32F435RGT7", "LQFP64", "C3029577", "AT32F435RGT7", "ARTERY",
         "−40…85 °C @288 MHz (DS Tablo 16; 105 °C yalnız ≤ 240 MHz); varyantlar STM32F405RGT6 / APM32F405RGT6 "
         "−40…85 °C (KRR-008 FMU MCU muaf)",
         "FMU MCU, LQFP64, HSE 8 MHz (SYS-030, KRR-012). Pin 31 VCAP_1/PH3, 47 VCAP_2/PH2: AT32'de G/Ç, "
         "STM32/APM32'de VCAP; VCAP 2.2 µF her varyantta takılı. Her MCU ayrı yazılım derlemesi (SYS-095 d)",
         alt=ALT("AT32F435RMT7", "ARTERY", "C5178940",
                 "Aynı aile, pin birebir (mcu-secimi §1), ayrı derleme AT32F435M, stok 128 < 200. Farklı üretici "
                 "muadil = Variant alanı (STM32F405RGT6 C15742, APM32F405RGT6 C5290473; 62/64 pin aynı, "
                 "31/47 VCAP↔PH3/PH2, mcu-secimi §3.1–3.2)"),
         crit=True,
         exc="MCU istisnası SYS-095 (d), KRR-012: varyant başına ayrı derleme; RMT7 stok 128 < 200 (muadil §3 İ2)",
         proc="200 adet peşin alım (İ2: 2 × 100 set, 160 kademesi; muadil §4)",
         extra={"Variant": "STACKF435 (ana): AT32F435RGT7 C3029577 · STACKF405 (ArduPilot): STM32F405RGT6 C15742 · "
                           "STACKF405A (tedarik krizi): APM32F405RGT6 C5290473 — PCB/pasifler aynı, MCU türü ipek "
                           "baskı kutusunda (F435/F405/A405)"})
    for ref in ("C201", "C202", "C203", "C204"):
        C(ref, "100nF 16V", "VDD dekuplaj (pin 19/32/48/64)")
    C("C205", "10uF 16V", "VDD toplu (§10 A5; 4.7 µF yerine)")
    part("FB201", "FerriteBead_Small", "600R@100MHz", "L0603", "C1002", "GZ1608D601TF", "Sunlord",
         "-55…+125 °C (LCSC)", "VDDA süzgeci (pin 13). AT32: VDDA = VDD şart (DS Tablo 15) — ferrit DC düşümü ihmal")
    C("C206", "2.2uF 16V", "VDDA (§10 A4; 1 µF yerine)")
    C("C207", "100nF 16V", "VDDA")
    C("C208", "2.2uF 16V", "Pin 31 VCAP_1 (STM32/APM32), düşük ESR; AT32'de PH3 G/Ç — kondansatör zararsız, her "
                           "varyantta takılı (mcu-secimi §3.2, KRR-012)")
    C("C209", "2.2uF 16V", "Pin 47 VCAP_2 (STM32/APM32), düşük ESR; AT32'de PH2 G/Ç — kondansatör zararsız, her "
                           "varyantta takılı (mcu-secimi §3.2, KRR-012)")
    C("C210", "100nF 16V", "NRST")
    R("R201", "10k", "BOOT0 → GND")
    part("SW201", "SW_Push", "BOOT", "BTN", "C720477", "TS-1088-AR02016", "XUNPU",
         "-30…+80 °C (LCSC) — 85 °C istisnası (SYS-087): yalnız açılışta basılır", "BOOT0 → 3V3, DFU (SYS-055); "
         "AT32 ROM DFU da BOOT0 = 1, BOOT1 = 0")
    R("R202", "10k", "PB2/BOOT1 → GND")
    part("Y201", "Crystal_GND24", "8MHz", "XTAL3225", "C5179501", "XC32M4-8.000-F12LGDWL", "HCI",
         "-40…+105 °C (LCSC)", "HSE 8 MHz, CL 12 pF, ESR ≤ 100 Ω (SYS-050). Betaflight AT32 saati 8 MHz'e sabit "
         "(pll_ns 72, pll_ms 1) — DEĞİŞTİRME (mcu-secimi §0-7, KRR-012)",
         alt=ALT("3X008000BP", "huaxindianzi", "C19723344",
                 "3225-4P, 8 MHz, CL 12 pF, ESR 60 Ω ≤ 100 Ω, −40…85 °C (HCI XC32M4 DS s.1 / huaxin 3X DS; "
                 "pin 1-3 kristal, 2-4 GND pcb teyit)"), crit=True)
    C("C211", "18pF C0G", "HSE yük: 2 × (12 - 3) pF")
    C("C212", "18pF C0G", "HSE yük")
    part("D201", "LED", "RED", "LED0603", "C2286", "KT-0603R", "Hubei KENTO Elec", "-40…+85 °C (LCSC)",
         "LED0 durum (PC13 batırır, ≈ 1.3 mA ≤ 3 mA)")
    R("R203", "1k", "LED0 akım")
    part("Q201", "AO3400A", "AO3400A", "SOT23", "C20917", "AO3400A", "Alpha & Omega Semicon", "T_J -55…+150 °C (LCSC)",
         "Buzzer sürücü (PC15, BEEPER_INVERTED: yüksek = öter)")
    R("R204", "100", "Q201 kapı seri")
    R("R205", "100k", "Q201 kapı → GND")
    part("D202", "D", "1N4148WS", "SOD323", "C2128", "1N4148WS", "Jiangsu Changjing Electronics Technology Co., Ltd.",
         "T_J 150 °C (CJ DS)", "Buzzer serbest geçiş diyodu (§10 A; 1N4148WT SOD-523 yerine, basic)",
         alt=ALT("1N4148WS", "Yangzhou Yangjie Elec Tech", "C389058"))
    TP("J201", "BZ+", "PAD15", "Buzzer + pedi (+5V)")
    TP("J202", "BZ-", "PAD15", "Buzzer − pedi")
    TP("TP201", "SWDIO", desc="SWD pedi Ø1.0 (SYS-057)")
    TP("TP202", "SWCLK", desc="SWD pedi Ø1.0 (SYS-057)")
    TP("TP203", "NRST", desc="SWD pedi Ø1.0 (SYS-057)")
    TP("TP204", "GND", desc="SWD pedi Ø1.0 (SYS-057)")
    TP("TP205", "3V3", desc="SWD pedi Ø1.0 (SYS-057)")

    # -------------------------------------------------------------- sensors
    part("U301", "LSM6DSV16X", "LSM6DSV16XTR", "LGA14", "C5267406", "LSM6DSV16XTR", "STMicroelectronics",
         "-40…+85 °C (DS13510 §4 T_op) — FMU ≥ 85 °C ✓ (SYS-087)",
         "IMU SPI1 4 telli (mod 1), CS PA4, INT1 PC4 (SYS-031, KRR-013); WHO_AM_I 0x70. SDx/SCx → GND, "
         "INT2/OCS_Aux/SDO_Aux boş (lehimli), Vdd/Vdd_IO 100 nF (DS Tablo 2, §7.1)",
         alt=ALT("LSM6DSK320XTR", "STMicroelectronics", "C53025794",
                 "KOŞULLU ALT — yalnız STACKF435, Betaflight ≥ 2026.6 (config'te USE_ACCGYRO_LSM6DSK320X) / INAV ≥ 9.1; "
                 "ArduPilot kararlı sürümde yok → STACKF405'te dizilmez. Pin 1–14 ve LGA-14L 2.5×3×0.83 aynı "
                 "(LSM6DSV16X DS13510 §3 / LSM6DSK320X DB5732 Tablo 1); WHO_AM_I 0x75 (muadil §2.1)"),
         crit=True, exc="Koşullu: ALT aynı üretici (ST, farklı üretici yok) ve yazılım sürümü şartlı (muadil §3)",
         proc="İsteğe bağlı 110 adet peşin alım (muadil §4)")
    C("C301", "100nF 16V", "LSM6DSV16X Vdd (pin 8) C1 100 nF — pin 8'e yakın (DS13510 §7.1)")
    part("U302", "SPA06-003", "SPA06-003", "LGA8", "C30589048", "SPA06-003", "Goertek", "-40…+85 °C (DS)",
         "Baro I2C1 0x76 (SDO → 100k → GND), ID 0x11: Betaflight barometer_dps310 (her sürüm), ArduPilot "
         "AP_Baro_SPL06 ≥ 4.6 (SYS-032, yazilim-inceleme §2)",
         alt=ALT("DPS368XTSA1(TOKMAS)", "Tokmas", "C55090144",
                 "Pin 1 GND 2 CSB 3 SDA 4 SCK 5 SDO 6 VDDIO 7 GND 8 VDD aynı (SPA06-003 DS Ver2.0 / Tokmas DPS368 DS); "
                 "ID 0x11. ALT2 Infineon DPS368 ID 0x10 (AP hwdef iki BARO satırı)",
                 alt2=("DPS368XTSA1", "Infineon", "C3232508")), crit=True)
    C("C303", "100nF 16V", "Baro VDD/VDDIO (pin 8 / 6)")
    R("R301", "100k", "Baro SDO → GND: adres 0x76 (SPA06 DS §4.3.1, R3 5–100 k)")
    R("R302", "2.2k", "I2C1 SCL çekme (pin-haritasi §1.1)")
    R("R303", "2.2k", "I2C1 SDA çekme")
    part("U303", "W25Q128JVS", "W25Q128JVSIQ", "SOIC8W", "C97521", "W25Q128JVSIQ", "Winbond Elec",
         "-40…+85 °C (DS) — FMU 85 °C sınıfı yeterli (KRR-008)",
         "Blackbox flash 16 MB SPI3, CS PC14 (SYS-033). JEDEC 0xEF4018: Betaflight flash_m25p16 + ArduPilot "
         "AP_Logger_Flash_JEDEC",
         alt=ALT("W25Q128JVSIM", "Winbond Elec", "C401671",
                 "Aynı kalıp/kılıf SOIC-8 208 mil (Winbond DS §3.1), JEDEC 0xEF7018 BF + AP ✓ (yazilim-inceleme §4); "
                 "ALT aynı üretici (KRR-011 k.3: stoklu farklı üretici yalnız Micron, 10 $)",
                 alt2=("MT25QL128ABA1ESE", "Micron", "C41359590")), crit=True)
    C("C304", "100nF 16V", "Flash VCC")
    R("R304", "10k", "FLASH_CS → 3V3 (açılışta seçili değil)")
    R("R305", "10k", "~WP ve ~HOLD → 3V3 (tek SPI, QSPI kullanılmaz)")

    # ------------------------------------------------------------------ osd
    part("U401", "AT7456E", "AT7456E", "HTSSOP28", "C82351", "AT7456E", "ZHONGKEWEI",
         "-40…+85 °C (LCSC)", "Analog OSD SPI2, CS PB12, 5 V (SYS-034)", crit=True,
         alt=ALT("", "", "", "Stoklu drop-in yok: MAX7456EUI C5346361 yazılımca ✓ ve pin uyumlu ama stok 0; AT7456 "
                             "C82523 stok 0; AT7456ELAH LGA-16 farklı kılıf"),
         exc="İSTİSNA: stoklu muadil yok; peşin alım + MAX7456 stok izleme (muadil §3 İ3)",
         proc="110 adet peşin alım (İ3; muadil §4)")
    C("C401", "100nF 16V", "DVDD")
    C("C402", "100nF 16V", "AVDD")
    C("C403", "100nF 16V", "PVDD")
    C("C404", "10uF 16V", "OSD +5V toplu (PVDD 80 mA darbe)")
    part("Y401", "Crystal_GND24", "27MHz", "XTAL3225", "C9008", "X322527MSB4SI", "YXC Crystal Oscillators",
         "-40…+85 °C (LCSC)", "OSD saat; MAX7456 DS: harici yük kondansatörü yok",
         alt=ALT("K3A270002010", "KYX", "C368745", "3225-4P, 27 MHz, CL 20 pF, ESR 30 Ω ≤ 50 Ω, −40…85 °C "
                 "(YXC X322527MSB4SI DS / KYX K3A DS)"), crit=True)
    R("R401", "10k", "~RESET → +5V")
    C("C405", "100nF 50V", "CVBS giriş kuplajı 0.1 µF (DS Şekil 2)")
    R("R402", "75", "CVBS giriş sonlandırma 75 Ω (SYS-034)")
    R("R403", "75", "CVBS çıkış seri 75 Ω, SAG = VOUT (DS Şekil 2)")

    # ------------------------------------------------------------------- io
    part("J501", "USB_C_Receptacle_USB2.0_16P", "USB-C", "USBC", "C165948", "TYPE-C-31-M-12", "Korean Hroparts Elec",
         "-30…+80 °C (LCSC)", "USB 2.0 FS, VCP + DFU (SYS-036)",
         alt=ALT("TYPE-C 16PIN 2MD(073)", "SHOU HAN", "C2765186",
                 "16 ped 0.5 aralık, 4 kabuk yuvası 0.6, 8.64/5.78 = HRO 8.65/5.78 (HRO 'Recommend PCB layout' / "
                 "Shou Han DS s.1); pim ø0.65/ø0.60 → ortak ped pcb; −25…85 °C ✓ (ana/ALT yer değiştirme önerisi M2)"),
         crit=True, exc="Sıcaklık: ana HRO −30…80 °C < 85 °C (SYS-087); ALT Shou Han −25…85 °C ✓ (muadil §3)")
    R("R501", "5.1k", "CC1 → GND (C-C kablo)")
    R("R502", "5.1k", "CC2 → GND")
    part("U501", "USBLC6-2SC6", "USBLC6-2SC6", "SOT23-6", "C2827654", "USBLC6-2SC6", "TECH PUBLIC",
         "-55…+125 °C (LCSC)", "USB ESD",
         alt=ALT("USBLC6-2SC6", "STMicroelectronics", "C7519",
                 "ST orijinali, aynı pin (1 I/O1 2 GND 3 I/O2 4 I/O2 5 VBUS 6 I/O1)"), crit=True)
    part("D501", "D_Schottky", "B5819W", "SOD123", "C8598", "B5819W SL", "Jiangsu Changjing Electronics Technology Co., Ltd.",
         "T_J 125 °C maks (CJ DS) ≥ 85 ✓", "VBUS → +5V; 5 V'tan VBUS'a geri besleme yok (SYS-036). 40 V 1 A, "
         "V_F ≈ 0.45 V @0.4 A (B3, guc-tasarruf §3.1)",
         alt=ALT("B5819W", "MDD(Microdiode Semiconductor)", "C64885",
                 "SOD-123, 40 V 1 A, V_F 0.6 V @1 A (CJ DS / MDD DS); ALT2 PMEG3020EH SOD-123F ortak ped (pcb)",
                 alt2=("PMEG3020EH", "TECH PUBLIC", "C19268151")), crit=True)
    sh_exc = "Sıcaklık istisnası (SYS-087): SH 1.0 ailesinde ≥ 85 °C üstü yok; serin kenar + DOG-105/108 ölçümü"
    sh8 = dict(lcsc="C54582896", mpn="XY-SM08B-SRSS-TB", mfr="XYECONN", temp="-40…+85 °C (LCSC)",
               alt=ALT("SM08B-SRSS-TB(LF)(SN)", "JST", "C160407", "JST orijinali; ESC J0 ile aynı kanıt (muadil §1)"),
               crit=True, exc=sh_exc)
    part("J502", "Conn_01x08", "J_ESC1", "SH8", desc="ESC 1 (M1-M4), dizilim ESC_PINOUT (İP-10 doğrulayacak, SYS-060)",
         **sh8)
    part("J503", "Conn_01x08", "J_ESC2", "SH8", desc="ESC 2 (M5-M8), yalnız Dual SKU'da takılı (SYS-037, M4a)",
         dnp=True, extra={"Variant": "Standart SKU: DNP; Dual SKU: takılı"}, **sh8)
    R("R503", "0", "J_ESC2.VBAT → VBAT, DNP: FMU'da bağlı değil (SYS-062)", dnp=True)
    sh4 = dict(lcsc="C51940130", mpn="XY-SM04B-SRSS-TB", mfr="XYECONN", temp="-25…+85 °C (LCSC)",
               alt=ALT("SM04B-SRSS-TB(LF)(SN)", "JST", "C160404", "JST SM04B-SRSS-TB orijinali (JST SH DS)"),
               crit=True, exc=sh_exc)
    sh6 = dict(lcsc="C56123098", mpn="XY-SM06B-SRSS-TB", mfr="XYECONN", temp="-25…+85 °C (JST eşdeğeri)",
               alt=ALT("SM06B-SRSS-TB(LF)(SN)", "JST", "C160405", "JST SM06B-SRSS-TB orijinali (JST SH DS)"),
               crit=True, exc=sh_exc)
    part("J504", "Conn_01x04", "RX", "SH4", desc="Alıcı (ELRS/CRSF) UART2, SH 4 (SYS-065)", **sh4)
    part("J505", "Conn_01x06", "DJI", "SH6", desc="Dijital VTX UART1 + 9 V + SBUS, SH 6 (SYS-065)", **sh6)
    part("J506", "Conn_01x06", "GPS", "SH6", desc="GPS UART6 + dış I2C1 (pusula) + 5 V, SH 6 (mimari §4.2)", **sh6)
    part("U502", "74LVC1G04", "SN74LVC1G04DBVR", "SOT23-5", "C7827", "SN74LVC1G04DBVR", "Texas Instruments",
         "-40…+125 °C (LCSC)", "SBUS ters çevirici → 1k → PA3 (SYS-035)",
         alt=ALT("74LVC1G04GV,125", "Nexperia", "C12509",
                 "SOT-23-5 1 NC 2 A 3 GND 4 Y 5 VCC (TI DBV DS §5 / Nexperia 74LVC1G04 DS §5)"), crit=True)
    C("C501", "100nF 16V", "U502 VCC")
    R("R504", "10k", "SBUS_IN aşağı çekme (boşta)")
    R("R505", "1k", "SBUS_INV → UART2_RX (CRSF alıcı pinini ezmez)")
    for ref, val, desc in (
            ("TP501", "SBUS", "SBUS pedi (ters SBUS girişi)"),
            ("TP502", "TX3", "UART3 TX pedi"), ("TP503", "RX3", "UART3 RX pedi"),
            ("TP504", "RX4", "UART4 RX pedi"),
            ("TP505", "TX5", "UART5 TX pedi"), ("TP506", "RX5", "UART5 RX pedi (ESC TLM)"),
            ("TP507", "M5", "Motor 5 pedi (standart SKU)"), ("TP508", "M6", "Motor 6 pedi"),
            ("TP509", "M7", "Motor 7 pedi"), ("TP510", "M8", "Motor 8 pedi"),
            ("TP511", "9V", "Analog VTX +9V"), ("TP512", "GND", "Analog VTX GND"),
            ("TP513", "VTX", "Analog VTX CVBS çıkışı"), ("TP514", "SA", "SmartAudio/Tramp UART4 TX"),
            ("TP515", "5V", "Kamera +5V"), ("TP516", "GND", "Kamera GND"),
            ("TP517", "CAM", "Kamera CVBS girişi"), ("TP518", "CC", "Kamera kontrol PB14"),
            ("TP519", "5V", "LED şerit +5V"), ("TP520", "GND", "LED şerit GND"),
            ("TP521", "LED", "LED şerit verisi PA8"), ("TP522", "S9", "Servo 1 PB15")):
        TP(ref, val, "PAD15", desc)


# ===================================================================== sheets
PWR_N = [0]


def snap(v):
    return round(round(v / 1.27) * 1.27, 2)


class Sheet:
    def __init__(self, title, file, page, comment, paper="A3"):
        self.title, self.file, self.page, self.comment, self.paper = title, file, page, comment, paper
        self.uuid = U("sheet", file)
        self.sym_uuid = U("sheetsym", file)
        self.items, self.libs, self.wires, self.conns, self.texts = [], set(), [], [], []
        self.n = 0
        self.points = {}

    def uid(self):
        self.n += 1
        return U(self.file, self.n)

    @staticmethod
    def xform(px, py, rot):
        r = math.radians(rot)
        rx = px * math.cos(r) - py * math.sin(r)
        ry = px * math.sin(r) + py * math.cos(r)
        return round(rx, 3), round(-ry, 3)

    def claim(self, p, who):
        p = (round(p[0], 2), round(p[1], 2))
        assert p not in self.points, (self.file, p, who, self.points[p])
        self.points[p] = who

    def place(self, ref, x, y, conn, rot=0, text=None):
        x, y = snap(x), snap(y)
        p = PARTS[ref]
        name = p["sym"]
        self.libs.add(name)
        meta = lib_pins(name)
        groups = {}
        for num, (px, py, a, kind) in meta.items():
            sx, sy = self.xform(px, py, rot)
            groups.setdefault((round(x + sx, 2), round(y + sy, 2)), []).append((num, a, kind))
        missing = [n for n, v in meta.items() if v[3] != "no_connect" and n not in conn]
        assert not missing, (ref, "pins without net", missing)
        assert not set(conn) - set(meta), (ref, "unknown pins", set(conn) - set(meta))
        xs = [q[0] for q in groups] + [x]
        ys = [q[1] for q in groups] + [y]
        for pos, pins in sorted(groups.items()):
            nets = {conn[n] for n, a, k in pins if n in conn}
            if not nets:
                continue
            assert len(nets) == 1, (ref, pins, nets)
            net = nets.pop()
            a = pins[0][1]
            vx, vy = {0: (-1, 0), 180: (1, 0), 90: (0, -1), 270: (0, 1)}[a]
            dx, dy = self.xform(vx, vy, rot)
            self.claim(pos, ref)
            self.conns.append((pos, (int(round(dx)), int(round(dy))), net, ref))
        if text is None:
            text = "right" if len(meta) <= 3 else "above"
        if text == "right":
            rpos, vpos, just = (x + 2.54, y - 1.27), (x + 2.54, y + 1.27), "left"
        elif text == "left":
            rpos, vpos, just = (x - 2.54, y - 1.27), (x - 2.54, y + 1.27), "right"
        else:
            rpos, vpos, just = (x, min(ys) - 8.89), (x, max(ys) + 10.16), None
        tail = {"Temperature": p["temp"], "Critical": ("evet" if p["crit"] else "hayır") if p["bom"] else "",
                "Exception": p["exc"], "Procurement": p["proc"]}
        fields = ([("Reference", ref), ("Value", p["value"]), ("Footprint", p["fp"]), ("Datasheet", p["ds"]),
                   ("Description", p["desc"]), ("MPN", p["mpn"]), ("Manufacturer", p["mfr"]), ("LCSC", p["lcsc"])]
                  + [(k, p["alt"][k]) for k in ALT_FIELDS if p["alt"].get(k)]
                  + [(k, tail[k]) for k in TAIL_FIELDS if tail[k]] + sorted(p["extra"].items()))
        assert not set(p["alt"]) - set(ALT_FIELDS), (ref, p["alt"])
        props = ""
        for kname, v in fields:
            if kname == "Reference":
                at, hide = rpos, False
            elif kname == "Value":
                at, hide = vpos, False
            else:
                at, hide = (x, y), True
            j = f"\n\t\t\t\t(justify {just})" if (just and not hide) else ""
            props += (f'\t\t(property "{kname}" "{esc(v)}"\n\t\t\t(at {f(at[0])} {f(at[1])} 0)\n'
                      + ("\t\t\t(hide yes)\n" if hide else "")
                      + "\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n"
                        f"\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t){j}\n\t\t\t)\n\t\t)\n")
        pinlines = "".join(f'\t\t(pin "{n}"\n\t\t\t(uuid "{U("pin", ref, n)}")\n\t\t)\n' for n in sorted(meta))
        self.items.append(
            f'\t(symbol\n\t\t(lib_id "stack:{name}")\n\t\t(at {f(x)} {f(y)} {rot})\n\t\t(unit 1)\n'
            f"\t\t(body_style 1)\n\t\t(exclude_from_sim no)\n\t\t(in_bom {'yes' if p['bom'] else 'no'})\n"
            f"\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp {'yes' if p['dnp'] else 'no'})\n"
            f'\t\t(uuid "{U("sym", ref)}")\n{props}{pinlines}'
            f'\t\t(instances\n\t\t\t(project "{PROJECT}"\n\t\t\t\t(path "/{ROOT_UUID}/{self.sym_uuid}"\n'
            f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
        p["sheet"] = self.file

    # two-terminal helpers -------------------------------------------------
    def v2(self, ref, x, y, top, bottom):
        """Vertical R/C/L/F: pin 1 on top."""
        self.place(ref, x, y, {"1": top, "2": bottom})

    def flag(self, net, x, y):
        """PWR_FLAG on a net: flag at (x, y), stub down, net terminator at the stub end."""
        self.libs.add("PWR_FLAG")
        x, y = snap(x), snap(y)
        PWR_N[0] += 1
        ref = f"#FLG{PWR_N[0]:03d}"
        self.claim((x, y), ref)
        self.items.append(self._power_block("PWR_FLAG", ref, "PWR_FLAG", x, y, 0, hide_value=True))
        self.conns.append(((x, y), (0, 1), net, ref))

    def note(self, s, x, y, size=1.27, bold=False):
        self.texts.append((s, x, y, size, bold))

    def _power_block(self, name, ref, value, x, y, rot, hide_value=False):
        vy = y - 3.81 if name != "GND" else y + 3.81
        vx = x
        if rot == 90:
            vx, vy = x - 3.81, y
        elif rot == 270:
            vx, vy = x + 3.81, y
        if name == "GND" and rot == 180:
            vy = y - 3.81
        if name != "GND" and name != "PWR_FLAG" and rot == 180:
            vy = y + 3.81
        u = self.uid()
        return (f'\t(symbol\n\t\t(lib_id "stack:{name}")\n\t\t(at {f(x)} {f(y)} {rot})\n\t\t(unit 1)\n\t\t(body_style 1)\n'
                f"\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n\t\t(dnp no)\n"
                f'\t\t(uuid "{u}")\n'
                f'\t\t(property "Reference" "{ref}"\n\t\t\t(at {f(x)} {f(y + 2.54)} 0)\n\t\t\t(hide yes)\n'
                "\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n"
                "\t\t\t\t)\n\t\t\t)\n\t\t)\n"
                f'\t\t(property "Value" "{value}"\n\t\t\t(at {f(vx)} {f(vy)} 0)\n'
                + ("\t\t\t(hide yes)\n" if hide_value else "")
                + "\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n"
                  "\t\t\t\t)\n\t\t\t)\n\t\t)\n"
                f'\t\t(property "Footprint" ""\n\t\t\t(at {f(x)} {f(y)} 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
                "\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n"
                f'\t\t(property "Datasheet" ""\n\t\t\t(at {f(x)} {f(y)} 0)\n\t\t\t(hide yes)\n\t\t\t(show_name no)\n'
                "\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n"
                f'\t\t(pin "1"\n\t\t\t(uuid "{U(u, "pin")}")\n\t\t)\n'
                f'\t\t(instances\n\t\t\t(project "{PROJECT}"\n\t\t\t\t(path "/{ROOT_UUID}/{self.sym_uuid}"\n'
                f'\t\t\t\t\t(reference "{ref}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')

    # rendering ----------------------------------------------------------
    def render(self, scope):
        out = []
        wires = []
        for (x, y), (dx, dy), net, who in self.conns:
            if net == "NC":
                out.append(f'\t(no_connect\n\t\t(at {f(x)} {f(y)})\n\t\t(uuid "{self.uid()}")\n\t)\n')
                continue
            ex, ey = round(x + dx * 2.54, 2), round(y + dy * 2.54, 2)
            self.claim((ex, ey), f"{who}:{net}")
            wires.append(((x, y), (ex, ey)))
            ang = {(1, 0): 0, (-1, 0): 180, (0, -1): 90, (0, 1): 270}[(dx, dy)]
            if net in RAILS:
                PWR_N[0] += 1
                if net == "GND":
                    rot = {(1, 0): 90, (-1, 0): 270, (0, 1): 0, (0, -1): 180}[(dx, dy)]
                else:
                    rot = {(1, 0): 270, (-1, 0): 90, (0, -1): 0, (0, 1): 180}[(dx, dy)]
                self.libs.add(net)
                out.append(self._power_block(net, f"#PWR{PWR_N[0]:03d}", net, ex, ey, rot))
            elif scope[net] == "global":
                j = "left" if ang in (0, 90) else "right"
                out.append(
                    f'\t(global_label "{net}"\n\t\t(shape bidirectional)\n\t\t(at {f(ex)} {f(ey)} {ang})\n'
                    f"\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {j})\n\t\t)\n"
                    f'\t\t(uuid "{self.uid()}")\n'
                    f'\t\t(property "Intersheetrefs" "${{INTERSHEET_REFS}}"\n\t\t\t(at {f(ex)} {f(ey)} 0)\n'
                    "\t\t\t(hide yes)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t(effects\n\t\t\t\t(font\n"
                    "\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n")
            else:
                j = "left bottom" if ang in (0, 90) else "right bottom"
                out.append(f'\t(label "{net}"\n\t\t(at {f(ex)} {f(ey)} {ang})\n\t\t(effects\n\t\t\t(font\n'
                           f'\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify {j})\n\t\t)\n\t\t(uuid "{self.uid()}")\n\t)\n')
        for s, x, y, size, bold in self.texts:
            b = "\n\t\t\t\t(bold yes)" if bold else ""
            out.append(f'\t(text "{esc(s)}"\n\t\t(exclude_from_sim no)\n\t\t(at {f(x)} {f(y)} 0)\n\t\t(effects\n'
                       f"\t\t\t(font\n\t\t\t\t(size {size} {size}){b}\n\t\t\t)\n\t\t\t(justify left top)\n\t\t)\n"
                       f'\t\t(uuid "{self.uid()}")\n\t)\n')
        wtxt = "".join(f"\t(wire\n\t\t(pts\n\t\t\t(xy {f(a[0])} {f(a[1])}) (xy {f(b[0])} {f(b[1])})\n\t\t)\n"
                       f"\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid \"{self.uid()}\")\n\t)\n"
                       for a, b in wires)
        libs = "".join("\t\t" + {**SYMBOLS, **EXTERNAL}[n].replace(f'(symbol "{n}"', f'(symbol "stack:{n}"', 1) + "\n"
                       for n in sorted(self.libs))
        return (f'(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
                f'\t(uuid "{self.uuid}")\n\t(paper "{self.paper}")\n\t(title_block\n\t\t(title "{esc(self.title)}")\n'
                f'\t\t(date "{DATE}")\n\t\t(rev "B")\n\t\t(company "Stack")\n'
                f'\t\t(comment 1 "{esc(self.comment)}")\n\t\t(comment 2 "tools/fmu_schematic.py ile üretildi, elle düzenlemeyin")\n\t)\n'
                f"\t(lib_symbols\n{libs}\t)\n{''.join(self.items)}{''.join(out)}{wtxt}\t(embedded_fonts no)\n)\n")


ROOT_UUID = U("root")
SHEETS = []


def sheet(*a, **kw):
    s = Sheet(*a, **kw)
    SHEETS.append(s)
    return s


def grid(s, items, x0, y0, dx=17.78, dy=27.94, cols=8):
    """items: (ref, top_net, bottom_net) vertical two-terminal parts in a grid."""
    for i, (ref, a, b) in enumerate(items):
        s.v2(ref, x0 + dx * (i % cols), y0 + dy * (i // cols), a, b)


# ------------------------------------------------------------------- pages
def page_power():
    s = sheet("Power", "power.kicad_sch", 2, "BAT pedleri, sigorta, ters kutup, TVS, SY8303 × 2 (5 V / 9 V), "
              "5 V yük anahtarı, TLV62569 3.3 V buck, IMU süzgeci, VBAT/CUR ölçümü")
    s.note("GÜÇ — giriş koruması (SYS-044, SYS-062, SYS-074; guc-ip03 G8, G16, G17)", 20, 22, 2, True)
    s.place("J101", 25.4, 50.8, {"1": "VBAT"}, text="right")
    s.place("J102", 25.4, 71.12, {"1": "GND"}, text="right")
    s.place("F101", 50.8, 55.88, {"1": "VBAT", "2": "VBAT_F"})
    s.place("Q101", 76.2, 55.88, {"1": "PMOS_G", "3": "VBAT_F", "2": "VIN"})
    s.place("D101", 101.6, 55.88, {"1": "VIN", "2": "PMOS_G"}, text="above")
    s.v2("R101", 101.6, 76.2, "PMOS_G", "GND")
    s.place("D102", 127, 55.88, {"1": "VIN", "2": "GND"}, text="above")
    grid(s, [("C101", "VIN", "GND"), ("C102", "VIN", "GND"), ("C103", "VIN", "GND")], 149.86, 55.88, dx=17.78)
    s.flag("VBAT", 40.64, 76.2)
    s.flag("VIN", 205.74, 50.8)
    s.flag("GND", 218.44, 50.8)
    s.note("Q101 AO3401A: D (pin 3) pil tarafında, S (pin 2) VIN'de; D101 10 V zener G–S (G8).\n"
           "BAT+/BAT− pedleri F101/Q101 öncesinde, J_ESC1.VBAT ile aynı VBAT düğümü (G16, G17).\n"
           "J_ESC2.VBAT FMU'da bağlı değil (R503 0 Ω DNP, io sayfası).\n"
           "8S BOM varyantı (KRR-007): F101, Q101, D102, C101…C103, U101/U102 → alan 8S (≥ 45 V) notu.",
           20, 92, 1.27)

    s.note("5 V / 2 A BEC — SY8303AAIC (G7, G10, B4; SYS-040, SYS-045)", 20, 112, 2, True)
    s.place("U101", 63.5, 140, {"5": "VIN", "8": "EN_5V", "2": "FS_5V", "7": "BS_5V", "6": "SW_5V", "1": "FB_5V",
                                "3": "GND", "4": "GND"})
    grid(s, [("C104", "VIN", "GND"), ("R102", "VIN", "EN_5V"), ("R103", "FS_5V", "GND")], 101.6, 132.08, dx=17.78)
    s.place("C106", 147.32, 132.08, {"1": "BS_5V", "2": "SW_5V"})
    s.place("L101", 165.1, 132.08, {"1": "SW_5V", "2": "+5V_BUCK"})
    grid(s, [("R104", "+5V_BUCK", "FB_5V"), ("R105", "FB_5V", "GND"), ("C107", "+5V_BUCK", "GND"),
             ("C108", "+5V_BUCK", "GND")], 182.88, 132.08, dx=17.78)
    s.flag("+5V", 254, 127)
    s.note("Vout = 0.600 V × (1 + 15k / 2k) = 5.10 V (DS: VFB 0.591…0.609 V → en kötü 4.94…5.27 V, RSS 4.98…5.22 V);\n"
           "+5V_BUCK → Q102 yük anahtarı (−0.12 V @2 A) → +5V: 4.82…5.15 V (guc-tasarruf §4, B4).\n"
           "f_sw = 1e5 / R_FS[kΩ] = 500 kHz (R_FS 200 k). EN → 100 k → VIN (EN mutlak 40 V).",
           20, 158, 1.27)

    s.note("9 V / 1.5 A BEC — SY8303AAIC, EN ← PB11 (PINIO1)", 20, 177, 2, True)
    s.place("U102", 63.5, 205, {"5": "VIN", "8": "EN_9V", "2": "FS_9V", "7": "BS_9V", "6": "SW_9V", "1": "FB_9V",
                                "3": "GND", "4": "GND"})
    grid(s, [("C105", "VIN", "GND"), ("R106", "+3V3", "EN_9V"), ("R107", "PINIO1", "EN_9V"), ("R108", "FS_9V", "GND")],
         101.6, 197.12, dx=17.78)
    s.place("C109", 165.1, 197.12, {"1": "BS_9V", "2": "SW_9V"})
    s.place("L102", 182.88, 197.12, {"1": "SW_9V", "2": "+9V"})
    grid(s, [("R109", "+9V", "FB_9V"), ("R110", "FB_9V", "GND"), ("C110", "+9V", "GND"), ("C111", "+9V", "GND")],
         200.66, 197.12, dx=17.78)
    s.flag("+9V", 271.78, 191.77)
    s.note("Vout = 0.600 V × (1 + 100k / 7.15k) = 8.99 V (8.69…9.30 V). PB11 yüksek veya MCU sıfırda (R106) → 9 V açık;\n"
           "Betaflight PINIO1_CONFIG 129 (ters): PINIO kutusu kapalı → pin yüksek → 9 V açık. Yalnız USB'de VIN yok → 9 V yok (SYS-036).",
           20, 225, 1.27)

    s.note("3.3 V — TLV62569 buck (guc-tasarruf §7.2, SYS-042), IMU süzgeci", 290, 22, 2, True)
    s.place("U103", 299.72, 50.8, {"4": "+5V", "1": "+5V", "3": "SW_3V3", "5": "FB_3V3", "2": "GND"})
    s.place("L103", 320.04, 45.72, {"1": "SW_3V3", "2": "+3V3"})
    grid(s, [("C112", "+5V", "GND"), ("C113", "+3V3", "GND")], 337.82, 45.72, dx=17.78)
    grid(s, [("R119", "+3V3", "FB_3V3"), ("R120", "FB_3V3", "GND"), ("C119", "+3V3", "FB_3V3")], 337.82, 71.12,
         dx=17.78)
    s.flag("+3V3", 381, 40.64)
    s.place("R111", 302.26, 96.52, {"1": "+3V3", "2": "+3V3_IMU"})
    grid(s, [("C114", "+3V3_IMU", "GND"), ("C115", "+3V3_IMU", "GND")], 320.04, 96.52, dx=17.78)
    s.flag("+3V3_IMU", 365.76, 91.44)
    s.note("Vout = 0.6 × (1 + 100k/22k) = 3.327 V (en kötü 3.21…3.45 V); EN → +5V; C_FF (C119) pedi DNP.\n"
           "Ortak pasifler TLV62569 ↔ SY8089A1 (KRR-011 k.4): 2.2 µH, C_IN 10 µF, C_OUT 22 µF, 100 k / 22 k.\n"
           "IMU dalı 22 Ω × 2.2 µF → 3.3 kHz (PSM dalgalanması ≈ 3 mVpp, guc-tasarruf §7.3); C115 = Vdd_IO 100 nF.",
           290, 111, 1.27)

    s.note("VBAT ve akım ölçümü (SYS-022, SYS-023; G15, G23)", 290, 124, 2, True)
    grid(s, [("R112", "VIN", "ADC_VBAT"), ("R113", "ADC_VBAT", "GND"), ("C116", "ADC_VBAT", "GND")], 297.18, 144.78,
         dx=17.78)
    grid(s, [("R114", "ESC1_CUR", "ADC_CURR1"), ("C117", "ADC_CURR1", "GND"),
             ("R115", "ESC2_CUR", "ADC_CURR2"), ("C118", "ADC_CURR2", "GND"), ("R116", "CUR2_SJ", "ADC_CURR1")],
         297.18, 180.34, dx=17.78)
    s.place("SJ101", 309.88, 205.74, {"1": "ESC2_CUR", "2": "CUR2_SJ"}, text="above")
    s.note("VBAT: VIN × 10k / 150k (15:1) → PC0; tam ölçek 3.3 × 15 = 49.5 V; Betaflight vbat_scale 150.\n"
           "CUR1 (J_ESC1) → 10k → PC1; CUR2 (J_ESC2) → 1k → PC5 (ArduPilot BATT2).\n"
           "SJ101 açık (varsayılan). Kapatılırsa PC1 = (CUR1 + CUR2)/2 (10k/10k) → Betaflight ölçek ×2.",
           290, 218, 1.27)

    s.note("USB yük anahtarı — yalnız USB'de VIN sızıntısını keser (guc-tasarruf §3.2, B3)", 20, 240, 2, True)
    s.place("Q102", 40.64, 264.16, {"3": "+5V_BUCK", "2": "+5V", "1": "LSW_G"})
    s.place("R117", 66.04, 264.16, {"1": "+5V", "2": "LSW_G"})
    s.place("Q103", 91.44, 264.16, {"3": "LSW_G", "2": "GND", "1": "LSW_B"})
    s.place("R118", 116.84, 264.16, {"1": "VIN", "2": "LSW_B"})
    s.note("Q102 AO3401A: D = +5V_BUCK, S = +5V; gövde diyodu buck → ray. Pil yokken (yalnız USB) Q103 kapalı,\n"
           "R117 Q102'yi kapalı tutar → +5V'tan U101 LX'e geri besleme yok, VIN = 0 V (Q101 kapalı, ESC beslenmez).\n"
           "VIN ≥ 1.5 V → Q103 doyar → Q102 V_GS ≈ −5 V, R_DS(on) ≤ 60 mΩ. 8S'te de değişiklik gerekmez.",
           20, 276, 1.27)
    s.note("Test noktaları (SYS-093)", 160, 238, 2, True)
    for i, (ref, net) in enumerate((("TP101", "VIN"), ("TP102", "+5V"), ("TP103", "+9V"), ("TP104", "+3V3"),
                                    ("TP105", "GND"))):
        s.place(ref, 165.1 + 20.32 * i, 254, {"1": net})
    return s


def page_mcu():
    s = sheet("MCU", "mcu.kicad_sch", 3, "AT32F435RGT7 (STM32F405RGT6 / APM32F405RGT6 varyant) LQFP64, HSE 8 MHz, "
              "VCAP, VDDA, BOOT0, NRST, SWD, LED0, buzzer")
    mcu = {
        "1": "+3V3", "2": "LED0", "3": "FLASH_CS", "4": "BEEPER", "5": "OSC_IN", "6": "OSC_OUT", "7": "NRST",
        "8": "ADC_VBAT", "9": "ADC_CURR1", "10": "SPI2_MISO", "11": "SPI2_MOSI", "12": "GND", "13": "VDDA",
        "14": "UART4_TX", "15": "UART4_RX", "16": "UART2_TX", "17": "UART2_RX", "18": "GND", "19": "+3V3",
        "20": "IMU_CS", "21": "SPI1_SCK", "22": "SPI1_MISO", "23": "SPI1_MOSI", "24": "IMU_INT1", "25": "ADC_CURR2",
        "26": "M3", "27": "M4", "28": "BOOT1", "29": "M7", "30": "PINIO1", "31": "VCAP1", "32": "+3V3",
        "33": "OSD_CS", "34": "SPI2_SCK", "35": "CAM_CC", "36": "SERVO1", "37": "UART6_TX", "38": "UART6_RX",
        "39": "M5", "40": "M6", "41": "LED_STRIP", "42": "UART1_TX", "43": "UART1_RX", "44": "USB_DM",
        "45": "USB_DP", "46": "SWDIO", "47": "VCAP2", "48": "+3V3", "49": "SWCLK", "50": "M8", "51": "UART3_TX",
        "52": "UART3_RX", "53": "UART5_TX", "54": "UART5_RX", "55": "SPI3_SCK", "56": "SPI3_MISO",
        "57": "SPI3_MOSI", "58": "M1", "59": "M2", "60": "BOOT0", "61": "I2C1_SCL", "62": "I2C1_SDA", "63": "GND",
        "64": "+3V3",
    }
    s.note("MCU — AT32F435RGT7 / STM32F405RGT6 / APM32F405RGT6 (SYS-030, SYS-050, KRR-005, KRR-012); "
           "pinler docs/pin-haritasi.md §1.1", 20, 22, 2, True)
    s.place("U201", 210.82, 139.7, mcu)
    s.note("Boş GPIO yok: LQFP64'ün 51 G/Ç'sinin tamamı kullanılıyor (pin-haritasi §1.1).\n"
           "DMA: ADC1 DMA2 S4 (ADC1_DMA_OPT 1), SPI1 DMA2 S0/S3; SPI2 (OSD) ve SPI3 (flash) DMA'sız (§1.3).\n"
           "Varyant (U201 Variant alanı): STACKF435 AT32F435RGT7 · STACKF405 STM32F405RGT6 · STACKF405A APM32F405RGT6;\n"
           "PCB, pasifler ve pin ataması aynı; her MCU ayrı yazılım derlemesi (KRR-012, SYS-095 d).",
           20, 30, 1.27)
    s.note("Besleme dekuplajı", 20, 45, 2, True)
    grid(s, [("C201", "+3V3", "GND"), ("C202", "+3V3", "GND"), ("C203", "+3V3", "GND"), ("C204", "+3V3", "GND"),
             ("C205", "+3V3", "GND")], 25.4, 66.04, dx=17.78)
    s.place("FB201", 30.48, 106.68, {"1": "+3V3", "2": "VDDA"})
    grid(s, [("C206", "VDDA", "GND"), ("C207", "VDDA", "GND")], 50.8, 106.68, dx=17.78)
    s.flag("VDDA", 86.36, 101.6)
    grid(s, [("C208", "VCAP1", "GND"), ("C209", "VCAP2", "GND")], 101.6, 106.68, dx=17.78)
    s.note("VDD 4 × 100 nF + 10 µF; VBAT (pin 1) → 3V3; VDDA ferrit + 2.2 µF + 100 nF (AT32: VDDA = VDD şart, DS Tablo 15).\n"
           "Pin 31 VCAP_1/PH3, 47 VCAP_2/PH2: 2 × 2.2 µF X7R her varyantta takılı; AT32'de PH3/PH2 G/Ç, kondansatör\n"
           "zararsız (mcu-secimi §3.2). VCAP1/VCAP2 ağları başka hiçbir yere bağlanmaz; PH2/PH3 hiçbir derlemede çıkış değil.",
           20, 122, 1.27)
    s.note("Saat, sıfırlama, önyükleme (SYS-055)", 20, 137, 2, True)
    s.place("Y201", 35.56, 160.02, {"1": "OSC_IN", "3": "OSC_OUT", "2": "GND", "4": "GND"}, text="above")
    grid(s, [("C211", "OSC_IN", "GND"), ("C212", "OSC_OUT", "GND")], 55.88, 160.02, dx=17.78)
    grid(s, [("C210", "NRST", "GND"), ("R201", "BOOT0", "GND"), ("R202", "BOOT1", "GND")], 91.44, 160.02, dx=17.78)
    s.place("SW201", 45.72, 190.5, {"1": "+3V3", "2": "BOOT0"}, text="above")
    s.note("BOOT düğmesi basılıyken açılış → USB DFU (AT32 ROM DFU da BOOT0 = 1, BOOT1 = 0).\n"
           "HSE 8 MHz SABİT: Betaflight AT32 saati yalnız 8 MHz kristalle 288 MHz verir — değiştirme (KRR-012).",
           20, 200, 1.27)
    s.note("LED0, buzzer (SYS-038)", 300, 22, 2, True)
    s.place("R203", 307.34, 45.72, {"1": "+3V3", "2": "LED0_A"})
    s.place("D201", 322.58, 55.88, {"2": "LED0_A", "1": "LED0"}, text="above")
    s.place("R204", 345.44, 45.72, {"1": "BEEPER", "2": "BZ_G"})
    s.place("Q201", 365.76, 60.96, {"1": "BZ_G", "3": "BUZZER_N", "2": "GND"})
    s.place("R205", 345.44, 71.12, {"1": "BZ_G", "2": "GND"})
    s.place("D202", 383.54, 45.72, {"1": "+5V", "2": "BUZZER_N"}, text="above")
    s.place("J201", 312.42, 86.36, {"1": "+5V"})
    s.place("J202", 332.74, 86.36, {"1": "BUZZER_N"})
    s.note("SWD pedleri Ø1.0 mm, tek yüz (SYS-057)", 300, 105, 2, True)
    for i, (ref, net) in enumerate((("TP201", "SWDIO"), ("TP202", "SWCLK"), ("TP203", "NRST"), ("TP204", "GND"),
                                    ("TP205", "+3V3"))):
        s.place(ref, 307.34 + 20.32 * i, 127, {"1": net})
    return s


def page_sensors():
    s = sheet("Sensors", "sensors.kicad_sch", 4, "LSM6DSV16X IMU (SPI1), SPA06-003 baro (I2C1 0x76), W25Q128JV flash (SPI3)")
    s.note("IMU — LSM6DSV16X, SPI1, CS PA4, INT1 PC4 (SYS-031, SYS-042, KRR-013)", 20, 22, 2, True)
    s.place("U301", 73.66, 71.12, {"12": "IMU_CS", "13": "SPI1_SCK", "14": "SPI1_MOSI", "1": "SPI1_MISO",
                                   "4": "IMU_INT1", "9": "NC", "2": "GND", "3": "GND", "10": "NC", "11": "NC",
                                   "8": "+3V3_IMU", "5": "+3V3_IMU", "6": "GND", "7": "GND"})
    grid(s, [("C301", "+3V3_IMU", "GND")], 124.46, 66.04, dx=17.78)
    s.note("Mod 1, SPI 4 telli (DS13510 Tablo 2): SDx (2), SCx (3) → GND; INT2 (9), OCS_Aux (10), SDO_Aux (11) boş\n"
           "(elektriksel bağlantısız, lehimli). Vdd + Vdd_IO ← +3V3_IMU (22 Ω + 2.2 µF süzgeç, power sayfası);\n"
           "C301 = Vdd C1 100 nF (pin 8), C115 = Vdd_IO C2 100 nF (pin 5, power sayfası) — DS §7.1. ICM'e özgü 10 nF (C302) kaldırıldı.\n"
           "ALT LSM6DSK320X (aynı pin/kılıf, DB5732 Tablo 1): yalnız STACKF435, BF ≥ 2026.6 (U301 ALT Note).\n"
           "Yerleşim: IMU kart merkezine yakın, BEC'lerden uzak (pcb-muhendisi).",
           20, 98, 1.27)
    s.note("Baro — SPA06-003, I2C1 PB8/PB9, adres 0x76 (SYS-032)", 20, 125, 2, True)
    s.place("U302", 73.66, 160.02, {"2": "+3V3", "4": "I2C1_SCL", "3": "I2C1_SDA", "5": "BARO_SDO",
                                    "8": "+3V3", "6": "+3V3", "1": "GND", "7": "GND"})
    grid(s, [("C303", "+3V3", "GND"), ("R301", "BARO_SDO", "GND"), ("R302", "+3V3", "I2C1_SCL"),
             ("R303", "+3V3", "I2C1_SDA")], 119.38, 152.4, dx=17.78)
    s.note("CSB → VDDIO: I2C. SDO → 100k → GND: 0x76. 2.2 k çekmeler dış I2C (GPS/pusula) ile ortak.\n"
           "Betaflight: barometer_dps310 (ID 0x11 SPA06 / 0x10 DPS368); ArduPilot ≥ 4.6: AP_Baro_SPL06 (0x11) + DPS280 (0x10).\n"
           "ALT Tokmas DPS368 (0x11), ALT2 Infineon DPS368 (0x10) — aynı LGA-8 dizilimi.",
           20, 185, 1.27)
    s.note("Blackbox flash — 16 MB, SPI3, CS PC14 (SYS-033, SYS-056)", 230, 22, 2, True)
    s.place("U303", 271.78, 71.12, {"1": "FLASH_CS", "6": "SPI3_SCK", "5": "SPI3_MOSI", "2": "SPI3_MISO",
                                    "3": "FLASH_WPH", "7": "FLASH_WPH", "8": "+3V3", "4": "GND"})
    grid(s, [("C304", "+3V3", "GND"), ("R304", "+3V3", "FLASH_CS"), ("R305", "+3V3", "FLASH_WPH")], 309.88, 66.04,
         dx=17.78)
    s.note("W25Q128JVSIQ (0xEF4018); ALT W25Q128JVSIM (0xEF7018), ALT2 Micron MT25QL128 (0x20BA18) — aynı SOIC-8 208 mil.\n"
           "Betaflight USE_FLASH_M25P16; ArduPilot AP_Logger_Flash_JEDEC üçünü de tanır (yazilim-inceleme §4).",
           230, 100, 1.27)
    return s


def page_osd():
    s = sheet("OSD", "osd.kicad_sch", 5, "AT7456E analog OSD, SPI2, 27 MHz, CVBS 75 Ω, 5 V")
    s.note("OSD — AT7456E (MAX7456 uyumlu), SPI2, CS PB12 (SYS-034)", 20, 22, 2, True)
    s.place("U401", 101.6, 101.6, {
        "8": "OSD_CS", "10": "SPI2_SCK", "9": "SPI2_MOSI", "11": "SPI2_MISO", "19": "OSD_RESET",
        "5": "OSD_XI", "6": "OSD_XO", "7": "NC", "22": "OSD_VIN", "26": "OSD_VOUT", "25": "OSD_VOUT",
        "12": "NC", "17": "NC", "18": "NC", "3": "+5V", "21": "+5V", "24": "+5V",
        "4": "GND", "20": "GND", "23": "GND", "29": "GND"})
    s.place("Y401", 45.72, 157.48, {"1": "OSD_XI", "3": "OSD_XO", "2": "GND", "4": "GND"}, text="above")
    grid(s, [("C401", "+5V", "GND"), ("C402", "+5V", "GND"), ("C403", "+5V", "GND"), ("C404", "+5V", "GND"),
             ("R401", "+5V", "OSD_RESET")], 165.1, 66.04, dx=17.78)
    s.place("C405", 172.72, 116.84, {"1": "CAM_VIDEO", "2": "OSD_VIN"})
    s.place("R402", 190.5, 116.84, {"1": "CAM_VIDEO", "2": "GND"})
    s.place("R403", 208.28, 116.84, {"1": "OSD_VOUT", "2": "VTX_VIDEO"})
    s.note("Kamera CVBS → 0.1 µF → VIN, girişte 75 Ω sonlandırma; VOUT (SAG = VOUT) → 75 Ω → VTX (DS Şekil 2).\n"
           "27 MHz kristal doğrudan CLKIN–XFB (DS: harici yük kondansatörü gerekmez). LOS/VSYNC/HSYNC/CLKOUT boş.\n"
           "SPI girişleri V_IH 2.0 V → 3.3 V MCU uyumlu; SDOUT 5 V → PC2 FT (5 V toleranslı, DS Tablo 7).",
           20, 185, 1.27)
    return s


def page_io():
    s = sheet("IO", "io.kicad_sch", 6, "USB-C, ESC konnektörleri, UART konnektör/pedleri, SBUS çevirici, VTX/kamera, "
              "LED şerit, servo")
    s.note("USB-C (SYS-036)", 20, 22, 2, True)
    usb = {"A4": "VBUS", "A9": "VBUS", "B4": "VBUS", "B9": "VBUS", "A1": "GND", "A12": "GND", "B1": "GND",
           "B12": "GND", "SH": "GND", "A5": "USB_CC1", "B5": "USB_CC2", "A6": "USB_DP", "B6": "USB_DP",
           "A7": "USB_DM", "B7": "USB_DM", "A8": "NC", "B8": "NC"}
    s.place("J501", 45.72, 76.2, usb)
    grid(s, [("R501", "USB_CC1", "GND"), ("R502", "USB_CC2", "GND")], 91.44, 60.96, dx=17.78)
    s.place("U501", 101.6, 101.6, {"1": "USB_DP", "6": "USB_DP", "3": "USB_DM", "4": "USB_DM", "5": "VBUS",
                                   "2": "GND"})
    s.place("D501", 139.7, 55.88, {"2": "VBUS", "1": "+5V"}, text="above")
    s.flag("VBUS", 157.48, 66.04)
    s.note("VBUS → B5819W → +5V: yalnız USB'de MCU, sensörler, OSD ve 5 V çalışır; 5 V'tan VBUS'a geri besleme yok.\n"
           "Q102 yük anahtarı (power sayfası) +5V'tan buck'a/VIN'e sızıntıyı keser.\n"
           "USBLC6 pin 1/6 ve 3/4 aynı hat (geçişli). PA9 VBUS algılama kullanılmaz (UART1).",
           20, 120, 1.27)

    s.note("ESC konnektörleri SM08B (SYS-037, SYS-060…062; dizilim tablosu ESC_PINOUT, İP-10)", 200, 22, 2, True)
    j1 = {str(n): J_ESC1_NETS[sig] for n, sig in ESC_PINOUT}
    j2 = {str(n): J_ESC2_NETS[sig] for n, sig in ESC_PINOUT}
    s.place("J502", 223.52, 63.5, j1)
    s.place("J503", 284.48, 63.5, j2)
    s.place("R503", 314.96, 63.5, {"1": "ESC2_VBAT", "2": "VBAT"})
    pin_tbl = "  ".join(f"{n}:{sig}" for n, sig in ESC_PINOUT)
    s.note(f"Dizilim (esc55a J0, doğrulanacak): {pin_tbl}\nJ_ESC1: CUR → ESC1_CUR → PC1, TLM → UART5_RX (PD2), M1–M4.\n"
           "J_ESC2 (Dual SKU, standart SKU'da DNP): CUR → PC5, TLM boş, M5–M8; VBAT → R503 0 Ω DNP.",
           200, 86, 1.27)
    for i, (ref, net) in enumerate((("TP507", "M5"), ("TP508", "M6"), ("TP509", "M7"), ("TP510", "M8"))):
        s.place(ref, 340.36 + 15.24 * i, 63.5, {"1": net})

    s.note("Alıcı, DJI, GPS konnektörleri (SYS-035, SYS-065) — cihaz tarafı dizilimi doğrulanacak", 20, 140, 2, True)
    s.place("J504", 40.64, 167.64, {str(i + 1): n for i, n in enumerate(J_RX_PINS)})
    s.place("J505", 96.52, 167.64, {str(i + 1): n for i, n in enumerate(J_DJI_PINS)})
    s.place("J506", 152.4, 167.64, {str(i + 1): n for i, n in enumerate(J_GPS_PINS)})

    s.note("SBUS ters çevirici (SYS-035)", 200, 140, 2, True)
    s.place("TP501", 208.28, 170.18, {"1": "SBUS_IN"})
    s.place("R504", 223.52, 175.26, {"1": "SBUS_IN", "2": "GND"})
    s.place("U502", 254, 170.18, {"2": "SBUS_IN", "4": "SBUS_INV", "5": "+3V3", "3": "GND"})
    s.place("C501", 287.02, 175.26, {"1": "+3V3", "2": "GND"})
    s.place("R505", 302.26, 175.26, {"1": "SBUS_INV", "2": "UART2_RX"})
    s.note("SBUS pedi (veya DJI pin 6) → 74LVC1G04 → 1k → PA3 (UART2 RX). CRSF alıcı doğrudan RX2'yi\n"
           "sürer; 1k çevirici çıkışını ezmesine izin verir.", 200, 193, 1.27)

    s.note("UART pedleri, analog VTX / kamera, LED şerit, servo", 20, 210, 2, True)
    pads = (("TP502", "UART3_TX"), ("TP503", "UART3_RX"), ("TP504", "UART4_RX"), ("TP505", "UART5_TX"),
            ("TP506", "UART5_RX"), ("TP511", "+9V"), ("TP512", "GND"), ("TP513", "VTX_VIDEO"), ("TP514", "UART4_TX"),
            ("TP515", "+5V"), ("TP516", "GND"), ("TP517", "CAM_VIDEO"), ("TP518", "CAM_CC"), ("TP519", "+5V"),
            ("TP520", "GND"), ("TP521", "LED_STRIP"), ("TP522", "SERVO1"))
    for i, (ref, net) in enumerate(pads):
        s.place(ref, 25.4 + 22.86 * (i % 9), 233.68 + 25.4 * (i // 9), {"1": net})
    return s


def write_all():
    scope_count = {}
    for s in SHEETS:
        for _, _, net, who in s.conns:
            scope_count.setdefault(net, {}).setdefault(s.file, 0)
            scope_count[net][s.file] += 1
    scope = {}
    for net, per in scope_count.items():
        if net in RAILS or net == "NC":
            continue
        total = sum(per.values())
        assert total >= 2, f"net {net} has a single connection"
        scope[net] = "global" if len(per) > 1 else "local"
    placed = {r for r, p in PARTS.items() if "sheet" in p}
    assert placed == set(PARTS), sorted(set(PARTS) - placed)
    for s in SHEETS:
        write_if_changed(BOARD / s.file, s.render(scope))
    # root page
    items = []
    n = [0]

    def rtext(t, x, y, size=1.27, bold=False):
        n[0] += 1
        b = "\n\t\t\t\t(bold yes)" if bold else ""
        items.append(f'\t(text "{esc(t)}"\n\t\t(exclude_from_sim no)\n\t\t(at {f(x)} {f(y)} 0)\n\t\t(effects\n\t\t\t(font\n'
                     f"\t\t\t\t(size {size} {size}){b}\n\t\t\t)\n\t\t\t(justify left top)\n\t\t)\n"
                     f'\t\t(uuid "{U("root-text", n[0])}")\n\t)\n')

    rtext("Stack FMU — M1 F405 uçuş kontrol kartı (Rev B, sıfırdan)", 20, 25, 3, True)
    rtext("AT32F435RGT7 (varyant STM32F405RGT6 / APM32F405RGT6) · LSM6DSV16X · SPA06-003 · W25Q128JV · AT7456E · "
          "SY8303 × 2 (5 V / 9 V) · TLV62569 · USB-C · 2 × SM08B ESC (8 motor)", 20, 33, 1.5)
    rtext("Pin haritası: docs/pin-haritasi.md §1 (tek kaynak) · Mimari: docs/mimari-fmu.md §4 · Güç: docs/rapor/guc-ip03.md §8\n"
          "Kaynak: tools/fmu_schematic.py (tekrar çalıştırılabilir, sabit UUID). Referanslardan dosya kopyalanmadı (KRR-006).\n"
          "Sayfalar arası bağlantı global etiketlerle; raylar (GND, +3V3, +3V3_IMU, +5V, +9V, VIN, VBAT, VBUS) güç sembolüyle.\n"
          "Referans numaraları sayfaya göre: 1xx power, 2xx mcu, 3xx sensors, 4xx osd, 5xx io.", 20, 40, 1.27)
    rtext("Blok akışı:  BAT+/− & J_ESC1.VBAT → F101 → Q101 (ters kutup) → VIN → { D102 TVS, VBAT ölçüm, U101 5 V, U102 9 V }\n"
          "U101 → +5V_BUCK → Q102 yük anahtarı (VIN'den kapılı) → +5V (+ USB VBUS → B5819W) → U103 buck → +3V3 → { MCU, flash, "
          "baro, 22 Ω → +3V3_IMU → IMU };\n+5V → OSD, LED şerit, alıcı, GPS, buzzer;  +9V → DJI, analog VTX.  "
          "Hedef BOM 2026-11-13: boards/fmu/bom-hedef.csv, docs/muadil.md §6.", 20, 62, 1.27)
    blocks = ""
    for k, sh in enumerate(SHEETS):
        x, y = 25 + (k % 5) * 70, 100
        blocks += (
            f"\t(sheet\n\t\t(at {f(x)} {f(y)})\n\t\t(size 60 20)\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n"
            f"\t\t(dnp no)\n\t\t(stroke\n\t\t\t(width 0.1524)\n\t\t\t(type solid)\n\t\t)\n\t\t(fill\n\t\t\t(color 0 0 0 0.0000)\n\t\t)\n"
            f'\t\t(uuid "{sh.sym_uuid}")\n'
            f'\t\t(property "Sheetname" "{sh.title}"\n\t\t\t(at {f(x)} {f(y - 0.7)} 0)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t(bold yes)\n\t\t\t\t)\n\t\t\t\t(justify left bottom)\n\t\t\t)\n\t\t)\n"
            f'\t\t(property "Sheetfile" "{sh.file}"\n\t\t\t(at {f(x)} {f(y + 20.6)} 0)\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n'
            f"\t\t\t(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1 1)\n\t\t\t\t)\n\t\t\t\t(justify left top)\n\t\t\t)\n\t\t)\n"
            f'\t\t(instances\n\t\t\t(project "{PROJECT}"\n\t\t\t\t(path "/{ROOT_UUID}"\n\t\t\t\t\t(page "{sh.page}")\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n')
        rtext(sh.comment, x, y + 24, 1.0)
    root = (f'(kicad_sch\n\t(version 20260306)\n\t(generator "eeschema")\n\t(generator_version "10.0")\n'
            f'\t(uuid "{ROOT_UUID}")\n\t(paper "A3")\n\t(title_block\n\t\t(title "FMU F405 — kök")\n\t\t(date "{DATE}")\n'
            f'\t\t(rev "B")\n\t\t(company "Stack")\n\t\t(comment 1 "tools/fmu_schematic.py ile üretildi")\n\t)\n'
            f'\t(lib_symbols)\n{"".join(items)}{blocks}'
            f'\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n\t(embedded_fonts no)\n)\n')
    write_if_changed(BOARD / f"{PROJECT}.kicad_sch", root)


def main():
    build_symbols()
    define_parts()
    page_power()
    page_mcu()
    page_sensors()
    page_osd()
    page_io()
    write_library()
    write_footprints()
    write_lib_tables()
    write_all()
    n_bom = sum(1 for p in PARTS.values() if p["bom"])
    print(f"wrote {1 + len(SHEETS)} sheets, {len(PARTS)} parts ({n_bom} BOM, "
          f"{sum(1 for p in PARTS.values() if p['dnp'])} DNP)")


if __name__ == "__main__":
    main()
