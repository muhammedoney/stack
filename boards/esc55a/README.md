# esc55a — 4’ü 1 arada 55 A ESC

Dört kanallı BLHeli_S tipi ESC. Kanal başına EFM8BB21F16G (QFN20) → FD6288Q (QFN24) → 6 × ME7170 N-MOS (8DFN 5 × 6). JW5026 buck → 8.07 V (PVDD) → AMS1117 → 3V3. Yüksek taraf shunt 2 × 1 mΩ 2512 + INA199C1 → J0.1 CUR. FMU bağlantısı J0 SM08B-SRSS-TB.

- Kaynak: Altium [`altium/esc55a.PrjPcb`](altium/esc55a.PrjPcb) — `main.SchDoc` (güç, MOSFET’ler, konnektör), `mcu2.SchDoc` (kanal 1–2), `mcu.SchDoc` (kanal 3–4), `ESC_v0.PcbDoc`. `FPV_Template.PcbDoc` projede yok (eski taslak); `escPan.PcbDoc` boş 100 × 100 mm panel (cezeri 2025-05-29: “maliyet avantajı olmadı”).
- PCB: 4 katman (dış ≈ 2 oz, iç 0.5 oz), 1.67 mm, 41.25 × 47.75 mm, montaj 30.5 × 30.5 mm M3. 224 ayak izi, 1730 yol parçası, 210 via, 34 bölge; bağlanmamış 0.
- KiCad: taşınmadı.

## J0 (SM08B-SRSS-TB)

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Ağ | CUR | NC | M4 | M3 | M2 | M1 | VBAT (PWR) | GND |

## Kontrol — Altium içe aktarma (2026-11-06)

| | Sonuç |
|---|---|
| DRC (KiCad varsayılan kurallar) | Bağlanmamış 0. 499 açıklık, 199 via çapı, 199 delik, 114 bakır–kenar: Altium kuralları içe aktarılmadığı için; taşımada kurallar yazılacak |
| Dış hat | 4 çok kısa parça (≤ 0.86 µm) |
| Şematik | 4 × `R?` numarasız (mcu, mcu2) |

Bulgular E1–E12: [`docs/inceleme.md`](../../docs/inceleme.md) §2.3.
