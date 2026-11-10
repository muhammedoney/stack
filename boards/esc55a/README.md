# esc55a — 4’ü 1 arada 55 A ESC

Dört kanallı BLHeli_S tipi ESC. Kanal başına EFM8BB21F16G (QFN20) → FD6288Q (QFN24) → 6 × ME7170 N-MOS (8DFN 5 × 6). JW5026 buck → 8.07 V (PVDD) → AMS1117 → 3V3. Yüksek taraf shunt 2 × 1 mΩ 2512 + INA199C1 → J0.1 CUR. FMU bağlantısı J0 SM08B-SRSS-TB.

- Kaynak: Altium [`altium/esc55a.PrjPcb`](altium/esc55a.PrjPcb) — `main.SchDoc` (güç, MOSFET’ler, konnektör), `mcu2.SchDoc` (kanal 1–2), `mcu.SchDoc` (kanal 3–4), `ESC_v0.PcbDoc`. `FPV_Template.PcbDoc` projede yok (eski taslak); `escPan.PcbDoc` boş 100 × 100 mm panel (cezeri 2025-05-29: “maliyet avantajı olmadı”).
- PCB: 4 katman (dış ≈ 2 oz, iç 0.5 oz), 1.67 mm, 41.25 × 47.75 mm, montaj 30.5 × 30.5 mm M3. 224 ayak izi, 1730 yol parçası, 210 via, 34 bölge; bağlanmamış 0.
- KiCad (İP-04, 2026-11-10): PCB [`esc55a/esc55a.kicad_pcb`](esc55a/esc55a.kicad_pcb) `kicad-cli pcb import` ile alındı; Altium kuralları `.kicad_pro`’da (açıklık/iz 0.1 mm, via 0.45 / 0.2 mm, halka 0.1 mm, kenar 0.2 mm); ayak izleri `lib/{RLC,MOS,IC,CONN}.pretty` (`tools/altium_libs.py`); dış hattaki 4 sıfıra yakın parça silindi (`tools/outline_fix.py`). Proje klasörü `esc55a/`: `esc55a.kicad_pcb`, `.kicad_pro` (kurallar + şematik sayfaları), `.kicad_prl`, `fp-lib-table`, `sym-lib-table`, şematik (aşağıda).

## Şematik (İP-04, 2026-11-10)

Hiyerarşik: kök [`esc55a/esc55a.kicad_sch`](esc55a/esc55a.kicad_sch) → 3 alt sayfa.

| Sayfa | Dosya | Altium kaynağı | İçerik |
|---|---|---|---|
| main (s. 2) | `main.kicad_sch` | `main.SchDoc` | Güç (JW5026, AMS1117, INA199, shunt), 24 × ME7170, J0, pedler |
| mcu2 (s. 3) | `mcu2.kicad_sch` | `mcu2.SchDoc` | Kanal 1–2: U11/U21 EFM8BB21, U12/U22 FD6288Q |
| mcu (s. 4) | `mcu.kicad_sch` | `mcu.SchDoc` | Kanal 3–4: U31/U41 EFM8BB21, U32/U42 FD6288Q |

Taşıma adımları (tekrar için):

1. `LC_ALL=C.UTF-8 LANG=C.UTF-8 kicad` → *File → Import Non-KiCad Project → Altium Project* → `altium/esc55a.PrjPcb`, hedef boş bir klasör (ör. `.tmp_imp/out/`); PCB sorusuna “No” (PCB ayrı alındı). Türkçe dil ayarında okuyucu `Location` → `LOCATİON` yapıp çöker; dil ayarı zorunlu. KiCad 10 üç sayfayı üç üst düzey sayfa olarak yazar, ağ etiketlerini yerel yapar.
2. `python3 tools/esc55a_sch.py .tmp_imp/out` — kök + alt sayfa hiyerarşisi; birden çok sayfada geçen 41 ağ etiketi global etiket (Altium projesinde port/sayfa girişi yok → etiketler global); `R?` → R99–R106, `#PWR?` numaralandı; 29 NC işareti, 16 PWR_FLAG; `.kicad_pro` sayfa listesi.
3. `python3 tools/altium_libs.py` — semboller `lib/{RLC,IC,MOS,CONN,stack}.kicad_sym`, Footprint alanları PCB’den.

| Kontrol | Sonuç |
|---|---|
| Netlist ↔ PCB (pin → ağ, 707 ortak pin) | Ağ bölünmesi/birleşmesi 0; yalnız isimsiz ağların adı farklı (`Net-(C00-1)` ↔ `NetC00_P$1`) |
| ERC (`kicad-cli sch erc`) | 0 hata, 8 uyarı: 4 sarkan 2.54 mm tel ucu (CK1–CK4 pedi, Altium artığı, elektriksel etkisi yok); 2 çoklu ağ adı (PVDD etiketi = +8V güç portu; PCB’de ağ adı PVDD); 2 sembol–kütüphane farkı (C00, C04: dikdörtgen köşe sırası, yalnız çizim) |
| Referanslar | Benzersiz. `M1aH`, `P1a`, `BAT`, `gnd`, `3v`… Altium adları PCB ile eşleşsin diye korundu (rakamla bitmediği için KiCad “annotation” uyarısı verir; **Annotate çalıştırılmamalı**) |

Şematik ↔ PCB farkları (Altium’dan gelen, değiştirilmedi):

| Konu | Şematik | PCB |
|---|---|---|
| R99–R106 (eski `R?`): kanal başına 3 k → +VD, 1 k → GND, Ux1 pin 1’e (bölücü) | Var | **Yok** (224 ayak izi); Ux1 pin 1 boşta |
| J0 `GND` pini (sembol) | Pin adı `GND`, boşta (NC) | Ayak izinde `GND` pedi yok (P1/P2 montaj pedleri ağsız) |
| R99–R106 değer adı | `RES0402_3k_????` / `RES0402_1k_????` (Altium’da da bozuk karakter) | — |

## J0 (SM08B-SRSS-TB)

| Pin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Ağ | CUR | NC | M4 | M3 | M2 | M1 | VBAT (PWR) | GND |

## Kontrol — KiCad PCB, Altium kurallarıyla (2026-11-10)

| | Sonuç |
|---|---|
| Bağlantı | Bağlanmamış 0 |
| Açıklık | 7: bölge–bölge 0.101599 < 0.1016 mm (yuvarlama, gerçek değil) |
| Kart kenarı | 73: bakır kenara 0.127 mm (kural 0.2 mm; JLC en az 0.2 mm) — Rev B’de düzeltilecek (`pcb-muhendisi`) |
| Halka | 4 via 0.075 mm halka (< 0.1 mm) |
| Yol kesişmesi | 1: In1.Cu’da 0 mm M1c yol parçası ch1_ho2 yolu üzerinde (143.74, 106.45) — içe aktarma artığı olabilir, incelenecek (`pcb-muhendisi`) |
| Diğer | 199 aç ısıl bağlantı (starved_thermal), 163 kütüphane farkı (normalize edilmiş kopya; şematik sonrası `pcb_fields.py` ile), 32 ipek–bakır, 19 yalıtık bakır, 15 küçük ipek yazı, 6 maske köprüsü, 19 padstack uyarısı (pastasız ped), 2 alt ipekte aynalanmamış yazı |

## Kontrol — Altium içe aktarma, KiCad varsayılan kuralları (2026-11-06)

| | Sonuç |
|---|---|
| DRC (KiCad varsayılan kurallar) | Bağlanmamış 0. 499 açıklık, 199 via çapı, 199 delik, 114 bakır–kenar: Altium kuralları içe aktarılmadığı için; taşımada kurallar yazılacak |
| Dış hat | 4 çok kısa parça (≤ 0.86 µm) |
| Şematik | 8 × `R?` numarasız (mcu, mcu2 × 4) → KiCad’de R99–R106 |

Bulgular E1–E12: [`docs/inceleme.md`](../../docs/inceleme.md) §2.3.
