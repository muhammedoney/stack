#!/usr/bin/env python3
"""FMU netlist <-> docs/pin-haritasi.md §1 check.

  LC_ALL=C.UTF-8 kicad-cli sch export netlist -o /tmp/fmu.net boards/fmu/fmu/fmu.kicad_sch
  python3 tools/pinmap_check.py . /tmp/fmu.net

1. Every LQFP64 pin of U201: pin name (netlist pinfunction) and net equal the
   pin map (§1.1 table + "Güç pinleri" line). Expected net names are derived
   from the İşlev column by the RULES table below.
2. FMU<->ESC rules (§3): M1-M4 -> J502, M5-M8 -> J503, CUR1 -> PC1, CUR2 -> PC5,
   TLM J502 -> PD2, J503 TLM NC, J503 VBAT not on VBAT (DNP 0R).
3. KRR-012: VCAP1 / VCAP2 nets carry only U201 pin 31 / 47 and one capacitor.
Exit code = number of differences.

AT32F435 (KRR-012, 2026-11-13): U201 is the AT32F435RGTx symbol whose pins
31 / 47 are named "VCAP_1/PH3" / "VCAP_2/PH2" (STM32F405/APM32F405 VCAP,
AT32F435 PH3/PH2 on the same pad, docs/rapor/mcu-secimi.md §3.1). The pin map
keeps the STM32 names (VCAP_1, VCAP_2), so PIN_ALIAS maps the symbol name back
to the pin map name; every other pin name is compared unchanged.
"""
import re
import sys
from pathlib import Path

repo, netf = Path(sys.argv[1]), Path(sys.argv[2])
doc = (repo / "docs/pin-haritasi.md").read_text(encoding="utf-8")
sec = doc[doc.index("### 1.1"):doc.index("### 1.2")]

RULES = [  # (regex on İşlev, net or callable)
    (r"^LED0", "LED0"), (r"Flash CS", "FLASH_CS"), (r"^Buzzer", "BEEPER"),
    (r"VBAT ölçümü", "ADC_VBAT"), (r"^Akım 1", "ADC_CURR1"), (r"Akım 2", "ADC_CURR2"),
    (r"^(SPI\d) (SCK|MISO|MOSI)", lambda m: f"{m.group(1)}_{m.group(2)}"),
    (r"^(UART\d) (TX|RX)", lambda m: f"{m.group(1)}_{m.group(2)}"),
    (r"^IMU CS", "IMU_CS"), (r"^IMU INT1", "IMU_INT1"), (r"^\*\*(M\d)\*\*", lambda m: m.group(1)),
    (r"^BOOT1", "BOOT1"), (r"^PINIO1", "PINIO1"), (r"^OSD CS", "OSD_CS"), (r"^Kamera kontrol", "CAM_CC"),
    (r"^Servo 1", "SERVO1"), (r"^LED şerit", "LED_STRIP"), (r"^USB D−", "USB_DM"), (r"^USB D\+", "USB_DP"),
    (r"^SWDIO", "SWDIO"), (r"^SWCLK", "SWCLK"), (r"^BOOT düğmesi", "BOOT0"),
    (r"^(I2C1) (SCL|SDA)", lambda m: f"{m.group(1)}_{m.group(2)}"),
]
expect = {}  # pin number -> (pin name, net)
for line in sec.splitlines():
    c = [x.strip() for x in line.split("|")]
    if len(c) < 5 or not re.match(r"^\d+(/\d+)?$", c[1]):
        continue
    nums, pins, func = c[1].split("/"), c[2].split("/"), c[3].replace("**", "**")
    if pins == ["PH0", "PH1"]:
        expect["5"], expect["6"] = ("PH0", "OSC_IN"), ("PH1", "OSC_OUT")
        continue
    f = func.replace("**", "") if not re.match(r"^\*\*M\d\*\*", func) else func
    for rx, net in RULES:
        m = re.search(rx, f if not callable(net) or "M\\d" not in rx else func)
        if m:
            expect[nums[0]] = (pins[0], net(m) if callable(net) else net)
            break
    else:
        expect[nums[0]] = (pins[0], f"?UNMAPPED:{func}")
pw = re.search(r"Güç pinleri: (.*)", sec).group(1)
for nums, name, net in (("1", "VBAT", "+3V3"), ("7", "NRST", "NRST"), ("12", "VSSA", "GND"), ("13", "VDDA", "VDDA"),
                        ("18/63", "VSS", "GND"), ("19/32/48/64", "VDD", "+3V3"), ("31", "VCAP_1", "VCAP1"),
                        ("47", "VCAP_2", "VCAP2")):
    assert re.search(r"\b%s %s\b" % (re.escape(nums), re.escape(name)), pw), (nums, name, pw)
    for n in nums.split("/"):
        expect[n] = (name, net)

# netlist
t = netf.read_text(encoding="utf-8")
nodes = {}  # (ref, pin) -> (net, pinfunction)
for nm in re.finditer(r'\(net\s+\(code "\d+"\)\s+\(name "([^"]*)"\)([\s\S]*?)\n\t\t\)', t):
    net = nm.group(1).rsplit("/", 1)[-1]
    for nd in re.finditer(r'\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)\s+(?:\(pinfunction "([^"]*)"\))?', nm.group(2)):
        nodes[(nd.group(1), nd.group(2))] = (net, (nd.group(3) or "").rsplit("_", 1)[0])
PIN_ALIAS = {"VCAP_1/PH3": "VCAP_1", "VCAP_2/PH2": "VCAP_2"}
diff = 0
rows = []
for n in sorted(expect, key=int):
    ename, enet = expect[n]
    net, func = nodes.get(("U201", n), ("<yok>", "<yok>"))
    func = PIN_ALIAS.get(func, func)
    ok = (func == ename and net == enet)
    diff += not ok
    rows.append(f"{n:>3} {func:<8} {net:<12} {'OK' if ok else 'FARK: beklenen ' + ename + ' ' + enet}")
missing = [p for (r, p) in nodes if r == "U201" and p not in expect]
for p in missing:
    rows.append(f"{p:>3} belgede yok")
    diff += 1
print("\n".join(rows))
print(f"MCU: {len(expect)} pin belgeden, {sum(1 for (r, p) in nodes if r == 'U201')} pin netlistte, fark {diff}")

# ESC connector rules
pin_of = lambda net: sorted(f"{r}.{p}" for (r, p), (nn, _) in nodes.items() if nn == net)
checks = []
mcu_pin = lambda net: [p for (r, p), (nn, _) in nodes.items() if r == "U201" and nn == net]
for k, net in enumerate(("M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8")):
    conn = "J502" if k < 4 else "J503"
    checks.append((f"{net} → {conn}", any(x.startswith(conn + ".") for x in pin_of(net))))
checks.append(("J502 CUR → R114 → PC1 (ADC_CURR1)", "R114.1" in pin_of(nodes[("J502", "1")][0]) and mcu_pin("ADC_CURR1") == ["9"]))
checks.append(("J503 CUR → R115 → PC5 (ADC_CURR2)", "R115.1" in pin_of(nodes[("J503", "1")][0]) and mcu_pin("ADC_CURR2") == ["25"]))
checks.append(("J502 TLM → PD2", nodes[("J502", "2")][0] == nodes[("U201", "54")][0]))
checks.append(("J503 TLM NC", nodes.get(("J503", "2"), ("unconnected",))[0].startswith("unconnected")))
checks.append(("J503 VBAT ≠ VBAT (0R DNP)", nodes[("J503", "7")][0] != "VBAT"))
checks.append(("J502 VBAT = BAT+ pedi = F101 girişi", nodes[("J502", "7")][0] == nodes[("J101", "1")][0] == nodes[("F101", "1")][0]))
for net, pin in (("VCAP1", "31"), ("VCAP2", "47")):
    members = pin_of(net)
    checks.append((f"{net}: yalnız U201.{pin} + bir kondansatör ({', '.join(members)})",
                   len(members) == 2 and f"U201.{pin}" in members and any(m.startswith("C2") for m in members)))
for name, ok in checks:
    print(("OK   " if ok else "FARK ") + name)
    diff += not ok
print("TOPLAM FARK", diff)
sys.exit(diff)
