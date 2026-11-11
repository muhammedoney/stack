# esc55a — 4’ü 1 arada 55 A ESC

Dört kanallı BLHeli_S tipi ESC. Kanal başına EFM8BB21F16G (QFN20) → FD6288Q (QFN24) → 6 × ME7170 N-MOS (8DFN 5 × 6). JW5026 buck → 8.07 V (PVDD) → AMS1117 → 3V3. Yüksek taraf shunt 2 × 1 mΩ 2512 + INA199C1 → J0.1 CUR. FMU bağlantısı J0 SM08B-SRSS-TB. (Altium / İP-04 durumu; **şematik Rev B’de** sürücü JSM6288Q1, MOSFET BLP016N04LC-Q 40 V, akım ölçümü 0.1 mΩ 3920 + INA240A3; yüksek sıcaklık (2026-11-11): MCU EFM8BB21F16**I** 125 °C, X5R yok — bkz. [Rev B şematik](#rev-b-şematik-2026-11-10). PCB henüz Rev A.)

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
| R99–R106 (eski `R?`): kanal başına 3 k → +VD, 1 k → GND, Ux1 pin 1’e (bölücü) | Var (Rev B: DNP, kartta yok) | **Yok** (224 ayak izi); Ux1 pin 1 boşta |
| J0 `GND` pini (sembol) | Pin adı `GND`, boşta (NC) | Ayak izinde `GND` pedi yok (P1/P2 montaj pedleri ağsız) |
| R99–R106 değer adı | `RES0402_3k_????` / `RES0402_1k_????` (Altium’da da bozuk karakter) | — |

## Rev B şematik (2026-11-10)

Kaynak: [`docs/rapor/guc-ip03.md`](../../docs/rapor/guc-ip03.md) önerileri; parça kodları `bom-maliyet.csv` / `bom-revb.csv`. Betik: `python3 tools/esc55a_revb.py` (idempotent: ikinci çalıştırma dosyaları değiştirmez; yeni UUID’ler sabit adlardan). Yardımcı: `tools/sch_edit.py` (fiber’den kopya, belirlenimci UUID eklendi). **PCB değiştirilmedi** (aşağıda senkron notu).

| # | Bulgu / SYS | Değişiklik | Referanslar |
|---|---|---|---|
| 1 | G1 · SYS-014, 010 | ME7170 30 V → **BLP016N04LC-Q** 40 V 1.6 mΩ (C49328363); ALT **NTMFS5C430NLT1G** (C194661). Ayak izi aynı `MOS:8DFN4.9X5.8` (DFN5×6, 1-3 S / 4 G / 5-8 D) | M1aH…M4cL (24) |
| 2 | G3 · SYS-016 | FD6288Q → **JSM6288Q1** (C52196409, UVLO 4.5 V); ALT FD6288Q (C328453). Pin/ayak izi aynı | U12, U22, U32, U42 |
| 3 | G4 · SYS-020, 021, 013, 014 | R00 ‖ R000 (2 × 1 mΩ 2512) → **R00 0.1 mΩ 3920 10 W** (HoLRS3920, C55113241), 4 uçlu Kelvin; INA199C1 → **INA240A3DR** (×100, SOIC-8, C2060584). U2 girişleri yeni **isns_p / isns_n** ağlarında (R00 pin 2 / 3); C05 1 nF bu ikisi arasında; REF1 = REF2 = GND, pin 4 (NC) GND; çıkış filtresi R03/R04 22 Ω → curr_sens → J0.1 aynen. Yeni **C06** 100 nF U2 VS. **CUR = 10 mV/A → Betaflight `ibata_scale = 100`, `ibata_offset = 0`**; tam ölçek ≈ 310 A (3.1 V) | R00, U2, C05, C06; R000 çıktı |
| 4 | G5 · SYS-014 | SMDJ28CA → **SMDJ24CA** (DOWO C284061), SMC aynı | D00 |
| 5 | G6 · SYS-014, 083 | Bulk 29 × 22 µF 35 V X5R → **15 × 10 µF 50 V X7R 1206** (C89632). Kalan: **C1–C10, C16–C19, C48**. Çıkan (14): C26, C27, C28, C29, C30, C36, C37, C38, C39, C40, C46, C47, C50, C60. C02 4.7 µF 35 V 0603 → **4.7 µF 50 V 0805** (C98192). Set kondansatörü (≥ 470 µF, ESR ≤ 50 mΩ) kutuda zorunlu — şematik notu | C1…C60, C02 |
| 6 | G11 · SYS-016 | L00 6.8 µH 1210 → **SWPA3015S100MT** 10 µH 3 × 3 mm (C45403), yeni ayak izi | L00 |
| 7 | G12 · SYS-016 | Yeni **C07** 10 µF 16 V 0603 (C70225) +3V3 (U0 çıkışı) | C07 |
| 8 | G13 · SYS-016 | Yeni **C120/C220/C320/C420** 1 µF 25 V 0402 (C52923) her sürücü VCC (PVDD)–GND; C03 10 µF 10 V 0402 → **10 µF 16 V 0603** (C70225) | C120…C420, C03 |
| 9 | G14 · SYS-010, 070 | 24 kapı direnci 22 Ω → **10 Ω** (0402WGF100JTCE, C25077, basic). Bluejay ölü zaman ≥ 200 ns ek (`gomulu-yazilim`) | R21–R24, R26, R28 (ve R4x, R6x, R8x aynı düzen) |
| 10 | E6 / G20 · SYS-015 | R99–R106 → **DNP**, “kartta yok” (on_board = no, BOM dışı); değerler 3 k (R100, R102, R105, R106 → +VD) / 1 k (R99, R101, R103, R104 → GND); +VD ağı boşta, Ux1 P0.1 boşta | R99–R106 |
| 11 | G25 · SYS-016 | “max 15V” notu → “PVDD ≤ 12 V (U0 LDO girişi)” | not |
| 12 | SYS-091 | Tüm parçalarda Value (= sembol adı), Footprint, Datasheet (`lib/datasheet/*_<LCSC>.pdf` varsa, yoksa LCSC/TI bağlantısı), MPN, Manufacturer, LCSC; yedekli parçalarda ALT MPN / ALT Manufacturer / ALT LCSC. Altium alanları (MANUFACTURER PRODUCT NUMBER, LSCS PART NUMBER, DIGIKEY …; eski kodlar yanlıştı) silindi. Pedler ve logo BOM/dizgi dışı | hepsi |

Değişmeyenler (Rev B ilk sürüm; yüksek sıcaklıkta değişenler [aşağıda](#yüksek-sıcaklık-güncellemesi-2026-11-11)): EFM8BB21 (C80713; S1b A3 BB51 uygulanmadı — pin dizilimi farklı, onay yok), JW5026, AMS1117-3.3 (UMW), 1N4148WT, J0 (XYECONN C54582896; ALT JST C160407, ayak izi aynı varsayıldı), pasif değerler (R03/R04 22 Ω, 90.9 k, 10 k, 3.3 k, 1 k, 220 Ω). ESC ters kutup koruması yok (SOR-010, SYS-074): + / − ipek baskı PCB işi.

**Yeni semboller** (`lib/`): `MOS:NMOS 40V BLP016N04LC-Q`, `MOS:IC MOSDRV JSM6288Q1 24QFN` (kopyalar, pinler aynı); `IC:IC PWR INA240A3D SOIC-8` (INA199 kutusu, pin numaraları SOIC-8’e göre: 1 IN−, 2 GND, 3 REF2, 4 NC, 5 OUT, 6 VS, 7 REF1, 8 IN+ — TI SBOS662 Tablo 6-1); `RLC:RES3920_0m1_KELVIN` (KiCad `Device:R_Shunt`: 1/4 güç, 2/3 algılama); `RLC:` DTVS_SMDJ24CA, IND3015_10u, CAP1206_10u_50V_X7R, CAP0805_4u7_50V_X5R, CAP0603_10u_16V_X5R, CAP0402_1u_25V_X5R, RES0402_10, RES0402_3k. CAP0402_0u1_16V/50V_X7R kütüphane kopyası şematikle eşitlendi (yalnız çizim).
**Yeni ayak izleri** (`lib/stack.pretty`, `fp-lib-table`’a `stack`): `R_3920_Kelvin_HoLRS3920` (Milliohm DS s.6 önerilen ped L 11 / A 6.2 / B 5.6 mm → ped 2.7 × 6.2 mm, merkez ±4.15 mm; algılama pedleri 2/3 0.5 × 0.5 mm, ped 1/4 iç kenarının üst köşesinde, `net_tie_pad_groups "1, 2" "3, 4"`), KiCad kopyaları `SOIC-8_3.9x4.9mm_P1.27mm`, `C_0805_2012Metric`, `L_Sunlord_SWPA3015S`. (`tools/altium_libs.py` yeniden çalıştırılırsa `stack.pretty` korunur; diğer `.pretty`’ler PCB’den yeniden yazılır.)

| Kontrol (Rev B) | Sonuç |
|---|---|
| ERC (`LC_ALL=C.UTF-8 kicad-cli sch erc`) | **0 hata, 2 uyarı** (önce 8): 2 × `multiple_net_names` PVDD global etiket = +8V güç sembolü (Altium’dan; ağ adı PVDD, PCB ile aynı — bilinçli bırakıldı). CK1–CK4 sarkan tel uçları (4) silindi; 2 sembol–kütüphane farkı giderildi. Referans “annotation” bildirimi Altium adlarından (M1aH, P1a …), Annotate çalıştırılmamalı |
| Netlist (Rev A ↔ Rev B, pin → ağ bölümlemesi, 708 ortak pin) | Beklenmeyen ağ değişimi **yok**. Beklenenler: VBAT yalnız BAT + R00.1; yeni ağlar `/main/isns_p` (R00.2, U2.8, C05.1), `/main/isns_n` (R00.3, U2.1, C05.2); PWR 88 → 71 pin (14 bulk, R000, C05, U2 çıktı; R00.4 girdi); PVDD +4, +3V3 +2, GND +6 −14 −4; R99–R106 netlistte yok (kartta yok) → Ux1 P0.1 tek pinli ağ. U2 pin numaraları yeni pakete göre |
| Parça | Şematik 223 (−15 +6), kartta 215 (R99–R106 hariç); PCB’de 224 ayak izi (Rev A) |

**PCB senkron notu (`pcb-muhendisi`, PCB Rev B):**
1. *Update PCB from Schematic*: çıkan ayak izleri C26–C30, C36–C40, C46, C47, C50, C60, R000; yeni C06, C07 (0603), C120, C220, C320, C420 (0402). Hangi bulk kondansatörlerin kalacağı yerleşime göre değişebilir — o zaman şematikte ref takası yapılır (bana bildir).
2. Ayak izi değişen: R00 2512 → `stack:R_3920_Kelvin_HoLRS3920` (10 × 5.2 mm, 4 ped); U2 SC70-6 → SOIC-8 (pin numaraları değişti); C02 0603 → 0805; C03 0603; L00 1210 → 3 × 3 mm. MOSFET’ler aynı ayak izi: BLP016 / NTMFS önerilen pedlerine göre (pin ped genişliği 0.46 mm, dren pedi) kontrol edilmeli.
3. **Kelvin (G4):** isns_p / isns_n R00 ped 2/3’ten (ped iç kenarı) ayrı, ince, yan yana çift yol olarak U2’ye; güç akımı bu yollardan geçmez; HoLRS3920 açık alaşım gövde altından yol/via geçmez; C05 ve C06 U2’nin dibinde. Pil yolu 0.1 mΩ ≈ 2 oz bakırın 0.4 karesi — şönt bağlantı bakırı kısa ve geniş.
4. C07 U0 VOUT’a, C120…C420 ilgili sürücünün VCC (pin 4)–COM (pin 6) pinlerine yakın.
5. R99–R106 kartta yok (değişiklik yok). Alanlar için *Update* sonrası `tools/pcb_fields.py`.
6. İpek baskı: BAT pedinde + / − (SOR-010, SYS-074); DOG-074.
7. SYS-093 test noktaları: mevcut pedler 3v (+3V3), VCC (PWR = VBAT), gnd/GNDd, CURR, CH1–CH4, NC; **PVDD pedi yok**. `test/` listesi gelince eklenecek (şematikte eklenmedi).

SYS-054: C2 pedleri CK1–CK4 (C2CK, 10 k → +3V3) ve CD1–CD4 (C2D) şematikte, ağları doğru; +3V3 / GND için 3v ve gnd pedleri. Ped çapı PAD.04 = 1.016 mm; aralık PCB’de kontrol.

### Yüksek sıcaklık güncellemesi (2026-11-11)

Müşteri 2026-11-11: “Kart yüksek derecelere çıkar.” Kural [öneri, `gereksinim-muhendisi`]: her parça ≥ 125 °C hedef, en az 105 °C; seramik en az X7R (X5R yok); elektrolitik yok. Isıl girdi `guc-ip03` §2.5: kart ≈ 95 °C, MOSFET kılıfı ≤ 110 °C. Aynı betik: `python3 tools/esc55a_revb.py` (Rev A'dan da, Rev B'den de aynı dosyaları üretir; ikinci çalıştırma değiştirmez). Her parçada yeni gizli alan **`Temperature`** (sınıf + kaynak). Maliyet: [`docs/bom-maliyet.md`](../../docs/bom-maliyet.md) §9.10, satırlar `bom-revb.csv` (`sicaklik_C`, `revb2_*`).

| Parça (ref) | LCSC | Sınıf önce | Sonra | Durum |
|---|---|---|---|---|
| BLP016N04LC-Q (M1aH…M4cL), ALT NTMFS5C430NL | C49328363 / C194661 | T_J −55…175 °C | aynı | ✓ (kılıf ≤ 110 °C hedefi `guc-ip03`) |
| JSM6288Q1 (U12…U42) | C52196409 | −40…125 °C (LCSC) | aynı | ✓ |
| **EFM8BB21 (U11…U41)** | C80713 → **C2053222** | **G: T_A −40…85 °C ✗** | **EFM8BB21F16I-C-QFN20R**: T_A −40…125 °C, T_J ≤ 130 °C (DS Tablo 4.1, 4.15) | ✓ aynı QFN20, aynı pinler ve ayak izi |
| INA240A3DR (U2) | C2060584 | T_A −40…125 °C, T_J 150 | aynı | ✓ |
| JW5026 (U1) | C185109 | T_J −40…125 °C (LCSC) | aynı | ✓ sınırda — `guc-elektronigi` |
| AMS1117-3.3 UMW (U0) | C347256 | −40…125 °C (LCSC) | aynı | ✓; P ≈ (8.07 − 3.3) V × I_3V3, kart 95 °C'de T_J payı — `guc-elektronigi` |
| SMDJ24CA (D00) | C284061 | T_J −55…150 °C | aynı | ✓ |
| 1N4148WT (D13…D45) | C27748 | T_J −65…150 °C | aynı | ✓ |
| SWPA3015S100MT (L00) | C45403 | −40…125 °C (öz ısınma dahil) | aynı | ✓ |
| HoLRS3920 0.1 mΩ (R00) | C55113241 | −55…170 °C | aynı | ✓ (güç azaltma DS s.4) |
| **J0** XY-SM08B-SRSS-TB (ALT JST) | C54582896 / C160407 | **−40…85 °C (JST −25…85)** | **aynı — açık konu** | ✗ SH ailesinde ≥ 105 °C yok |
| Bulk 10 µF 50 V X7R (15), 100 nF X7R (C00/C01, C04/C06/C11…C42), 1 nF X7R (C05) | C89632, C307331, C1525, C1523 | X7R −55…125 °C | aynı | ✓ |
| **C02** 4.7 µF 50 V 0805 | C98192 → **C6119944** | X5R 85 °C ✗ | **HRE CGA0805X7R475K500MT** X7R, ayak izi aynı (ALT CCTC C20416422) | ✓ |
| **C03, C07** 10 µF 16 V | C70225 → **C380347** | X5R 85 °C ✗ | **CCTC TCC0805X7R106K160FT** X7R, **0603 → 0805** `stack:C_0805_2012Metric` (ALT Samsung CL21B106KOQNNNE C95841) | ✓ |
| **C13…C45, C120…C420** (16) 1 µF | C52923 → **C49210445** | X5R 85 °C ✗ | **CCTC TCC0402X7R105K160AT** 1 µF **16 V** X7R 0402, ayak izi aynı (ALT 25 V C53426846) | ✓ |
| Dirençler UNI-ROYAL 0402WGF (7 kod) | | −55…155 °C | aynı | ✓ |
| R99–R106 | — | DNP | — | kartta yok |

**Yeni semboller:** `IC:IC MCU EFM8BB21F16I-C 20QFN` (G sembolünün kopyası, pinler aynı), `RLC:CAP0805_4u7_50V_X7R`, `RLC:CAP0805_10u_16V_X7R`, `RLC:CAP0402_1u_16V_X7R`. Kaldırılan (yalnız bu betik kullanıyordu): `RLC:CAP0805_4u7_50V_X5R`, `CAP0603_10u_16V_X5R`, `CAP0402_1u_25V_X5R`. `lib/stack.*` değişmedi. Şematik önbellek sembolleri ada göre sıralı (eeschema düzeni); alan sırası sabit (… ALT LCSC, Temperature). Kök sayfa başlık bloğu yorum 3.

| Kontrol (yüksek sıcaklık) | Sonuç |
|---|---|
| ERC | **0 hata, 2 uyarı** (aynı: 2 × `multiple_net_names` PVDD / +8V) |
| Netlist (önce ↔ sonra, 726 pin) | pin → ağ farkı **0**, bölümleme aynı; yalnız değer / ayak izi / alanlar |
| İdempotent | ikinci çalıştırmada 4 şematik + `lib/*.kicad_sym` md5 aynı; Rev A (44e8e21) + betik = çalışma ağacı (14 dosya aynı) |

**`guc-elektronigi` incelemeli:** (1) 1 µF 16 V X7R bootstrap/VCC (PVDD 8.07 V, ≤ 12 V): 25 V X5R'den 16 V X7R'ye; DC öngerilimde etkin kapasite (Q_g 61 nC için ≥ 0.3 µF yeterli, `guc-ip03` §3.2–3.3) — gerekirse ALT 25 V C53426846 (+0.29 $/kart). (2) C03 (PVDD) ve C07 (U0 çıkışı, AMS1117 kararlılığı) 0805 X7R. (3) C02 4.7 µF 50 V X7R 0805 JW5026 girişinde 26 V öngerilim; daha iyi seçenek 1206 Samsung CL31B475KBHNNNE C51205 (ayak izi değişir). (4) U0 ve U1 T_J payı kart 95 °C'de. Bobin L00 değişmedi (125 °C ✓).

**PCB senkron notu (ek):** C03 ve C07 ayak izi `stack:C_0805_2012Metric` (C07 zaten yeni; C03 0402 → 0805). Diğer değişenler ayak izi aynı. J0'ı MOSFET'lerden uzak, serin kenara yerleştirme önerisi (açık konu: J0 85 °C).

**J0 açık konu:** 15 SH 1.0 mm 8P klon (−25/−40…85 °C) tarandı; 105 °C seçenek Molex Pico-Clasp 501568-0807 (C587867) SH ile geçmez → FMU konnektörü ve kablo değişir (`sistem-mimari` kararı). Önerilen: prototip ısıl ölçümünde J0 sıcaklığı ölçülsün.

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
