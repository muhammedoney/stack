# fmu — F405 uçuş kontrol kartı (M1)

KiCad şematiği **sıfırdan** çizildi (İP-05, 2026-11-11): `tools/fmu_schematic.py`. Altium şeması (`altium/fmu.SchDoc`, Mamba F405 MK2 tersine mühendisliği, 143 parça) yalnız karşılaştırma girdisidir; hiçbir sembol, ayak izi veya sayfa referans tasarımlardan alınmadı (KRR-006). PCB **yok**.

- Kaynaklar: pin/zamanlayıcı/DMA [`docs/pin-haritasi.md`](../../docs/pin-haritasi.md) §1 (tek kaynak), mimari [`docs/mimari-fmu.md`](../../docs/mimari-fmu.md) §4, güç [`docs/rapor/guc-ip03.md`](../../docs/rapor/guc-ip03.md) §8 (G7–G10, G15–G18), KRR-005…008.
- Semboller: KiCad 10 standart kütüphanesinden `lib/stack.kicad_sym`'ye kopya; SY8303A, AT7456E, ICM-42688-P, DPS368 veri sayfasından çizildi. Ayak izleri: KiCad 10 standart kopyaları `lib/stack.pretty/` (35 yeni dosya). `lib/RLC|IC|MOS|CONN` değişmedi.
- Üretme: `python3 tools/fmu_schematic.py` — tekrar çalıştırılabilir; UUID'ler sabit (uuid5), ikinci çalıştırmada ve dosyalar silinip yeniden üretildiğinde md5 aynı.

## Şematik yapısı

| Sayfa | Dosya | Bloklar | Ref. |
|---|---|---|---|
| 1 | `fmu/fmu.kicad_sch` | Kök: blok akışı, sayfa sembolleri | — |
| 2 | `fmu/power.kicad_sch` | BAT+/− pedleri (F101/Q101 öncesi, J_ESC1.VBAT ile aynı düğüm), F101 5 A, Q101 AO3401A (D pil, S VIN) + 10 V zener + 100 k, D102 SMBJ24CA, 2 × 10 µF 50 V + 3 × 100 nF; U101 SY8303 5 V/2 A (L 6.8 µH SWPA6045), U102 SY8303 9 V/1.5 A (L 10 µH SWPA5040, EN ← PB11), U103 AMS1117-3.3 (22 µF), IMU süzgeci 10 Ω + 2.2 µF + 100 nF, VBAT 140 k/10 k %0.5 + 100 nF → PC0, CUR1 10 k + 100 nF → PC1, CUR2 1 k + 100 nF → PC5, SJ101 + 10 k (ortalama), test noktaları | 1xx |
| 3 | `fmu/mcu.kicad_sch` | STM32F405RGT6, VDD 4 × 100 nF + 4.7 µF, VDDA ferrit + 1 µF + 100 nF, VCAP 2 × 2.2 µF, NRST 100 nF, BOOT0 düğmesi + 10 k, BOOT1 10 k, HSE 8 MHz + 2 × 18 pF, LED0 (PC13), buzzer AO3400A (PC15) + pedler, SWD pedleri | 2xx |
| 4 | `fmu/sensors.kicad_sch` | ICM-42688-P SPI1 (CS PA4, INT1 PC4), DPS368 I2C1 0x76 + 2 × 2.2 k, W25Q128JV SPI3 (CS PC14) | 3xx |
| 5 | `fmu/osd.kicad_sch` | AT7456E SPI2 (CS PB12), 27 MHz, 5 V, CVBS giriş 0.1 µF + 75 Ω, çıkış 75 Ω | 4xx |
| 6 | `fmu/io.kicad_sch` | USB-C + 2 × 5.1 k + USBLC6-2SC6 + PMEG3020 (VBUS → 5 V), J_ESC1/J_ESC2 SM08B (J_ESC2 DNP, VBAT 0 Ω DNP), M5–M8 pedleri, RX SH4 (UART2), DJI SH6 (UART1 + 9 V + SBUS), GPS SH6 (UART6 + I2C1 + 5 V), SBUS → 74LVC1G04 → 1 k → PA3, UART3/4/5 pedleri, VTX/kamera, LED şerit, S9 pedleri | 5xx |

Sayfalar arası sinyaller global etiket; raylar (GND, +3V3, +3V3_IMU, +5V, +9V, VIN, VBAT, VBUS) güç sembolü. Ağ adları pin haritasındaki işlevlerden (M1…M8, UART1_TX, SPI1_MISO, IMU_CS, ADC_VBAT …). Kullanılmayan MCU pini yok (51 G/Ç dolu); diğer IC'lerin boş pinleri NC.

**FMU↔ESC 8 pin dizilimi** tek tabloda: `ESC_PINOUT` (`tools/fmu_schematic.py`). Bugün esc55a J0 sırası (1 CUR, 2 TLM, 3 M4, 4 M3, 5 M2, 6 M1, 7 VBAT, 8 GND); İP-10 SpeedyBee F405 V4'e göre değiştirirse yalnız tablo değişir ve betik yeniden çalıştırılır.

## Parça özeti (141 sembol: 104 BOM, 37 ped/test noktası/köprü; DNP 2: J503, R503)

| İşlev | Parça (LCSC) | Sıcaklık sınıfı |
|---|---|---|
| MCU | STM32F405RGT6 (C15742), ALT RGT7 C1337199 | −40…85 °C (müşteri istisnası, KRR-008) |
| IMU | ICM-42688-P Tokmas (C54308212), ALT TDK C1850418 | −40…85 °C **istisna** |
| Baro | DPS368XTSA1 Infineon (C3232508), ALT Tokmas C55090144 | −40…85 °C **istisna** |
| Flash | W25Q128JVSIQ (C97521), ALT GD25Q128ESJGR C22404005 | −40…85 °C (BF + ArduPilot destekli) |
| OSD | AT7456E (C82351) | −40…85 °C **istisna** |
| Buck × 2 | SY8303AAIC (C2937216) | T_A −40…105 °C |
| LDO | AMS1117-3.3 (C6186), ALT UMW C347222 | −40…125 °C |
| Ters kutup / zener / TVS / sigorta | AO3401A (C15127) / MM3Z10V (C42370498) / SMBJ24CA (C78416) / CFS12V3T5R0 (C163128) | T_J 150 / 150 / 150 °C / −20…105 °C |
| Bobinler | SWPA6045S6R8MT (C57254), SWPA5040S100MT (C84608) | −40…125 °C |
| Kristaller | 8 MHz HCI XC32M4 (C5179501) / 27 MHz YXC (C9008) | 105 °C / 85 °C **istisna** |
| USB | TYPE-C-31-M-12 (C165948), USBLC6-2SC6 (C2827654), PMEG3020EH (C19268151) | −30…80 °C **istisna** / 125 / 150 °C |
| Konnektör | XY-SM08B ×2, XY-SM04B, XY-SM06B ×2 (ALT JST) | −40/−25…85 °C **istisna** |
| Diğer | 74LVC1G04 TI, AO3400A, 1N4148WT, KT-0603R LED, TS-1088 düğme | 125 / 150 / 150 / 85 **istisna** / 80 °C **istisna** |
| Pasifler | Seramikler tümü X7R/C0G; dirençler UNI-ROYAL 0402WGF, VBAT bölücü %0.5 | −55…125 / −55…155 °C |

Her sembolde Value, Footprint, Datasheet, Description, MPN, Manufacturer, LCSC, Temperature; gerekirse ALT MPN/ALT LCSC, `8S` (VIN parçalarında 8S BOM notu, KRR-007) ve `Variant` (J503). LCSC kodları, stok ve sıcaklık JLC/LCSC parça arayüzünden 2026-11-11.

## Kontroller (2026-11-11)

| Kontrol | Sonuç |
|---|---|
| `LC_ALL=C.UTF-8 kicad-cli sch erc --severity-all boards/fmu/fmu/fmu.kicad_sch` | **0 hata, 0 uyarı** |
| Netlist ↔ `docs/pin-haritasi.md` §1.1 (64 MCU pini: pin adı + ağ) | **64/64 aynı, fark 0** |
| §3 kuralları: M1–M4 → J_ESC1, M5–M8 → J_ESC2, CUR1 → PC1, CUR2 → PC5, TLM J_ESC1 → PD2, J_ESC2 TLM NC, J_ESC2 VBAT bağlı değil, J_ESC1.VBAT = BAT+ = F101 girişi | **hepsi sağlanıyor** |
| İdempotent (ikinci çalıştırma ve sıfırdan üretim) | md5 aynı |
| BEC geri besleme (SY8303 VFB 0.600 V ±%1.5, DS) | 5 V: 100 k/13.7 k → 4.98 V (4.82–5.14); 9 V: 100 k/7.15 k → 8.99 V (8.69–9.30); R_FS 200 k → 500 kHz (f = 1e5/R_FS[k]) |
| VBAT bölücü | 140 k/10 k → 15:1, tam ölçek 49.5 V (SYS-022 ≥ 45 V) |

Pin karşılaştırma betiği oturum dizininde tutuldu (`pinmap_check.py`: §1.1 tablosunu ayrıştırır, kicadsexpr netlistini karşılaştırır).

## Maliyet (100 set, JLC 2026-11-11) — `bom-revb.csv`

| | $/kart |
|---|---|
| Komponent (std SKU) | 25.09 |
| PCB (36 × 36, 4 kat, `docs/bom-maliyet.md` §3 tahmini) | 0.25 |
| Dizgi (§4 yöntemi, Economic tek yüz [varsayım], 33 extended tür, 382 lehim noktası) | 1.72 |
| **FMU toplam** | **27.06** |
| Dual SKU farkı (J503) | +0.07 |

MCU tek başına 13.03 $ (STM32F405RGT6, JLC stoğu **4**). RGT6 (85 °C, stok 24) ile 18.61 $; RGT6 + Tokmas baro + W25Q128 ile ≈ 16.35 $.

## Açık konular

1. **MCU tedariki:** STM32F405RGT6 JLC/LCSC stoğu 4 (< 200), 13.03 $; RGT6 de 24 adet. `bom-tedarik` dış tedarik/konsinye fiyatı; KRR-008 MCU satırı maliyetle birlikte yeniden değerlendirilmeli.
2. **ESC 8 pin dizilimi** (İP-10, KRR-004): `ESC_PINOUT` geçici.
3. **SH konnektör cihaz tarafı dizilimleri** (RX, DJI, GPS) doğrulanmadı; SYS-065 GPS'i 4 pin diyor, mimari §4.2 6 pin (UART6 + I2C1 + 5 V) — ikincisi uygulandı, dış I2C bu konnektörde.
4. **Flash:** GD25Q128 Betaflight `flash_m25p16` tablosunda (0xC84018) var, `USE_FLASH_M25P16` gerekir (pin-haritasi §1.4 W25Q128FV yazıyor); ArduPilot `AP_Logger_Flash_JEDEC` tablosunda yok → AP yaması veya ALT W25Q128JVSIQ (85 °C istisnası).
5. **Baro:** DPS368 DPS310 sürücüsüyle çalışır (BF `barometer_dps310`, AP `AP_Baro_DPS280`, ID 0x10). DPS310 ve SPL06-001 stokta yok; SPA06-003 Betaflight'ta yalnız deneme sondası (sürücü yok), SPL07-003 ArduPilot'ta SPA06 sanılır — ikisi de seçilmedi.
6. **Ayak izleri `pcb-muhendisi` doğrulayacak:** ICM-42688-P için KiCad `LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y` (DS: D 2.5, E 3, D1 1.5, E1 1.0 ile uyumlu), DPS368 için `Bosch_LGA-8_2x2.5mm` (saat yönü numaralama), AT7456E açık ped ölçüsü, HCI kristal pin 1/3 sinyal.
7. **Q101** 3S tam yükte 0.45 W (G16): JSM7409 DFN3.3 ayak izi farklı → BAT pedleri + kılavuz yük sınırıyla AO3401A kaldı.
8. **USB'de VIN:** USB 5 V, U101'in üst MOSFET gövde diyoduyla VIN'e ≈ 4 V sızar (9 V buck UVLO 4.35 V altında, ADC_VBAT ≈ 4 V okur); `guc-elektronigi` incelesin.
9. **9 V EN:** PB11 → 1 k → EN, 100 k → 3V3 (sıfırda açık); Betaflight `PINIO1_CONFIG 129` anlamı `gomulu-yazilim` ile teyit.
10. Listeden sapmalar (gerekçeli): IMU süzgeç kondansatörü 2.2 µF (DS Şekil 5; listede 1 µF); CUR1 → PC1 yolunda 10 k (SJ101 kapalıyken eşit ağırlıklı ortalama için); flash ~WP/~HOLD 10 k ile 3V3'e; DJI pin 6 SBUS, SBUS pedi ile aynı ağ.
11. 8S BOM varyantı: VIN parçalarında `8S` alanı; 60 V buck ayak izi farkı PCB yer payı işidir (`pcb-muhendisi`).

## Güncelleme 2026-11-11 — FMU sıcaklık sınıfı 85 °C (müşteri)

Müşteri: “İşlemciyi bu sıcaklık durumundan muaf tut. FMU kartı hiçbir zaman ESC kadar yüksek bir sıcaklığa ulaşmayacak.” → SYS-087 / KRR-008 güncellendi.

| | Önce | Sonra |
|---|---|---|
| U201 | STM32F405RGT7 (C1337199, 13.03 $, stok 4) | **STM32F405RGT6 (C15742, 4.58 $, stok 24 → 100 set için dış tedarik)** |
| U303 | GD25Q128ESJGR (ArduPilot JEDEC tablosunda yok) | **W25Q128JVSIQ (C97521, BF + AP destekli)** |
| FMU kart (100 set) | 27.06 $ | **17.72 $** (komponent 15.78, PCB 0.25, dizgi 1.69) |
| Stack (+ ESC 17.20 $) | 44.26 $ | **34.92 $** (hedef ≤ 32 $) |

ERC 0, pin haritası farkı 0, betik idempotent. BOM: `python3 tools/fmu_bom.py` (fiyatlar `tools/jlc.py`, önbellek git dışı).

## Hedef BOM uygulaması (2026-11-13)

5. adım (`sematik-muhendisi`): şematik `boards/fmu/bom-hedef.csv` + `docs/muadil.md` §2/§6 + `docs/rapor/guc-tasarruf.md` §3–4, §7 + `docs/rapor/mcu-secimi.md` §3, §4.3 + KRR-011/012/013'e getirildi. Hepsi `tools/fmu_schematic.py` içinde (elle düzenleme yok); yukarıdaki parça özeti tablosu ve maliyet bölümü **bu bölümle geçersizdir**.

| Blok | Önce | Sonra |
|---|---|---|
| U201 MCU | STM32F405RGT6 C15742, sembol `STM32F405RGTx` | **AT32F435RGT7 C3029577**, sembol `AT32F435RGTx` (KiCad STM32F405RGTx kopyası, pin 31 **VCAP_1/PH3**, 47 **VCAP_2/PH2**); `Variant` = STACKF435 AT32F435RGT7 / STACKF405 STM32F405RGT6 C15742 / STACKF405A APM32F405RGT6 C5290473; ALT aynı aile AT32F435RMT7 C5178940; `Exception` MCU istisnası, `Procurement` 200 peşin |
| VCAP / saat / VDDA | — | C208/C209 2.2 µF her varyantta takılı (AT32'de PH3/PH2 G/Ç, zararsız); VCAP1/VCAP2 ağlarında yalnız U201 + kondansatör (betikle denetleniyor); Y201 8 MHz "sabit, değiştirme" notu; FB201 "VDDA = VDD şart" |
| §10 A | C205 4.7 µF, C206 1 µF, D202 1N4148WT SOD-523 | **C205 10 µF 0805 C380347, C206 2.2 µF 0603 C5360821, D202 1N4148WS SOD-323 C2128** |
| U301 IMU | ICM-42688-P (Tokmas) | **LSM6DSV16XTR C5267406**, sembol `LSM6DSV16X` (DS13510 Rev 4 Tablo 2'den çizildi), ayak izi `LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y` (KiCad standardı, ST LGA-14L 2.5 × 3). SPI1 mod 1: 12 CS ← PA4 (IMU_CS), 13 SCL ← SPI1_SCK, 14 SDA ← SPI1_MOSI, 1 SDO → SPI1_MISO, 4 INT1 → PC4 (IMU_INT1; pin adı aynı, pin haritası değişmedi); 2 SDx, 3 SCx → GND; 9 INT2, 10 OCS_Aux, 11 SDO_Aux NC (DS: "elektriksel bağlantısız, lehimli"); Vdd C301, Vdd_IO C115 100 nF (DS §7.1 C1/C2). **C302 (10 nF) kaldırıldı** (LSM6DSV16X DS'de yok). ALT **LSM6DSK320XTR C53025794** koşullu (`ALT Note`: yalnız STACKF435, BF ≥ 2026.6); pin 1–14 iki veri sayfasında birebir (DS13510 §3 Şekil 5 / DB5732 Rev 1 Tablo 1) |
| U302 baro | DPS368 Infineon | **SPA06-003 C30589048**, sembol `SPA06-003` (Goertek DS Ver2.0 Tablo 11); ALT Tokmas DPS368 C55090144, ALT2 Infineon C3232508 |
| U303 flash | ALT GD25Q128 | ALT **W25Q128JVSIM C401671**, ALT2 Micron MT25QL128ABA1ESE C41359590 |
| 3.3 V | U103 AMS1117-3.3 SOT-223 | **U103 TLV62569DBVR C141836** (ALT SY8089A1AAC C479074), **L103 2.2 µH WPN201610H2R2MT C97005** (ALT Murata C79317, ayak izi KiCad `L_Murata_DFE201610P`), C112 C_IN 10 µF, C113 C_OUT 22 µF, **R119 100 k / R120 22 k** → 3.327 V, **C119 C_FF 22 pF DNP**, EN → +5V |
| 5 V | R104/R105 100 k / 13.7 k, L101 → +5V | **R104 15 k C25756 / R105 2 k C4109** → 5.10 V; U101 çıkışı yeni yerel ağ **+5V_BUCK** (L101, C107, C108, FB) |
| USB yük anahtarı | yok | **Q102 AO3401A** (D = +5V_BUCK, S = +5V, G = LSW_G), **R117 100 k** (G–S, CSV'de R_a), **Q103 MMBT3904 C20526** (C = LSW_G, E = GND, B = LSW_B), **R118 100 k** VIN → baz (CSV'de R_b) — guc-tasarruf §3.2 |
| D501 / R111 | PMEG3020EH SOD-123F, 10 Ω | **B5819W SL C8598 SOD-123** (ALT MDD C64885, ALT2 PMEG3020EH C19268151 ortak ped), **R111 22 Ω C25092** (IMU süzgeci 3.3 kHz) |
| Alanlar | MPN/LCSC/ALT MPN/ALT LCSC | Her BOM parçasında ESC ile aynı adlar ve sıra: `MPN`, `Manufacturer`, `LCSC`, `ALT MPN`, `ALT Manufacturer`, `ALT LCSC`, `ALT2 MPN/Manufacturer/LCSC`, `ALT Note`, `Temperature`, `Critical` (evet/hayır), `Exception`, `Procurement` (+ `8S`, `Variant`); değerler `bom-hedef.csv`'den |

Referans eşlemesi (CSV yer tutucuları → şematik): R_a → **R117**, R_b → **R118**, R_FB3V3H → **R119**, R_FB3V3L → **R120**; C_FF → **C119** (DNP). Referanslar 1xx…5xx kuralında, betik her referansı `(U|C|R|L|D|Q|J|F|Y|FB|SW|SJ|TP)[1-5]dd` ve tekillik için denetler (ESC'deki C1/C01 tarzı çakışma yok).

Kütüphane: `lib/stack.kicad_sym`'ye yalnız ekleme (`AT32F435RGTx`, `LSM6DSV16X`, `SPA06-003`, `TLV62569DBV`, `MMBT3904`; mevcut semboller değişmedi, eski ICM-42688-P/DPS368/AMS1117/STM32F405RGTx kullanılmıyor ama silinmedi). `lib/stack.pretty/`'ye KiCad standart kopyası `D_SOD-123`, `L_Murata_DFE201610P`. Referans tasarımlardan dosya alınmadı (KRR-006).

### Kontroller (2026-11-13)

| Kontrol | Sonuç |
|---|---|
| `LC_ALL=C.UTF-8 kicad-cli sch erc --severity-all boards/fmu/fmu/fmu.kicad_sch` | **0 hata, 0 uyarı** (proje ERC ayarları değişmedi) |
| `python3 tools/pinmap_check.py . <netlist>` | **64/64 pin, fark 0**; §3 ESC kuralları OK; yeni: VCAP1/VCAP2 yalnız U201 + kondansatör OK. Betik uyarlaması: `PIN_ALIAS` "VCAP_1/PH3" → "VCAP_1", "VCAP_2/PH2" → "VCAP_2" (pin haritası STM32 adlarını tutuyor; AT32 adı aynı ped) |
| İdempotent | ikinci çalıştırmada ve `.kicad_sch` silinip yeniden üretildiğinde md5 aynı |
| `python3 tools/fmu_bom.py` ↔ `bom-hedef.csv` (ref bazında LCSC, MPN, ALT LCSC, kritik, DNP) | 111 / 111 ref; **fark 2, ikisi de bilinçli**: C302 (hedef CSV'de 10 nF, görev gereği kaldırıldı) ve C119 (C_FF DNP pedi, CSV'de yok). Hedef CSV düzeltilmedi |

### Maliyet (100 set, `tools/fmu_bom.py`)

| | $/kart |
|---|---|
| Komponent (std SKU) | **12.43** (hedef CSV 12.43) |
| PCB | 0.25 |
| Dizgi (betik formülü, 28 extended tür, 397 lehim noktası) | 1.59 (hedef CSV §4 "Standard tek yüz" yöntemiyle 1.42) |
| **FMU toplam** | **14.27** (hedef CSV 14.10); stack + ESC 15.71 = 29.98 $ ≤ 32 $ |

### Açık konular (bu adım)

1. `pcb-muhendisi`: LGA-14L ayak izi ST önerisiyle (KiCad'in LSM6DS3TR-C tabanlı deseni), L103 Sunlord WPN201610H ↔ Murata DFE201612P ped kesişimi, D501 SOD-123 ↔ PMEG3020EH SOD-123F ortak ped, SPA06-003 LGA-8 saat yönü numaralama, Q102 2 A yolu bakırı, U103 SW düğümü kısa / FB SW'den uzak.
2. SPA06-003 DS iki ayrı 100 nF (VDD, VDDIO) öneriyor; hedef BOM'da tek C303 var — `guc-elektronigi`/`bom-tedarik` kararı (eklenirse +1 basic 0402).
3. C_FF (C119) değeri DNP: TI 6.8 pF, SY 22 pF; prototipte gerekirse dizilir (DOG-042).
4. `sistem-mimari`: `docs/pin-haritasi.md` §1 başlığı ve güç satırına AT32 pin 31/47 (PH3/PH2) notu + §1.3 AT32 `dmaopt` sütunu (bu adımda dosyaya dokunulmadı).
5. `guc-elektronigi`: AT32 288 MHz akımıyla 3.3 V bütçesi (TLV62569 2 A, pay geniş), DOG-042 IMU pini dalgalanması.
