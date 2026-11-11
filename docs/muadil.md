# Kritik parça muadilleri (SYS-095, KRR-011) — hedef BOM, ESC + FMU

> **Tarih:** 2026-11-13 (4. adım). **Hazırlayan:** `bom-tedarik`. Şematiklere dokunulmadı; uygulama 5. adımda `sematik-muhendisi` (liste §6).
> **Kapsam:** iki kartın **hedef BOM'u** = Rev B + onaylı kararlar: §10 A1, A3–A7 (A2 geçersiz), B1, B3–B6; `guc-tasarruf` (RSA240C, SCT2400, R0/R02/R01, C03b, TLV62569 buck, USB yük anahtarı, R111 22 Ω, güç ALT'ları); KRR-012 (AT32F435RGT7 + varyantlar), KRR-013 (LSM6DSV16X).
> **Satır satır veri:** [`boards/esc55a/bom-hedef.csv`](../boards/esc55a/bom-hedef.csv), [`boards/fmu/bom-hedef.csv`](../boards/fmu/bom-hedef.csv) (ana + ALT LCSC/MPN/üretici/stok/fiyat, drop-in kanıtı, kritik, istisna). Maliyet: [`bom-maliyet.md`](bom-maliyet.md) §11.
> **Kaynak:** fiyat/stok JLCPCB parça arayüzü (`tools/jlc.py`'nin scratchpad kopyası, proje önbelleği değişmedi), 2026-11-13. Veri sayfaları LCSC (`datasheet.lcsc.com`; st.com bu oturumda erişilemedi). Yazılım: kaynak kodu GitHub raw (Betaflight 4.5.0…2026.6.2, INAV 8.0.0…9.1.0, ArduPilot Copter-4.6.3…4.7.2 ve master), 2026-11-13.
> **Drop-in ölçütü (KRR-011):** aynı pin dizilimi + aynı ayak izi (ped kesişimi) + aynı/üstün elektriksel ve sıcaklık sınıfı (ESC ≥ 125 °C SYS-086, FMU ≥ 85 °C SYS-087) + aynı yazılım imajında tanınma (`yazilim-inceleme`). Tercihen farklı üretici.

## 0. Özet

| | ESC | FMU | Toplam |
|---|---|---|---|
| Kritik parça (satır) | 10 | 22 | **32** |
| Drop-in ALT bulundu (koşulsuz) | 8 | 17 | **25** |
| ALT koşullu (teyit/sürüm şartı) | 1 (R00 shunt) | 2 (U301 IMU, L102) | **3** |
| ALT yok → istisna | 1 (EFM8BB21F16I) | 3 (AT32F435RGT7 MCU istisnası, AT7456E, SY8303A tek üretici) | **4** |

- **LSM6DSV16X:** drop-in ALT **LSM6DSK320X (ST, C53025794)** — aynı LGA-14L pin dizilimi; Betaflight ≥ 2026.6.0 ve INAV 9.1.0'da aynı sürücüde tanınır, ArduPilot yalnız master'da → **koşullu ALT** (STACKF435'te; STACKF405 ArduPilot SKU'sunda dizilmez). Farklı üreticiden muadil yok.
- Stok kuralı (≥ 2 × 100 set): yalnız **BLP016** (3 903 < 4 800 → A1 peşin alım) ve ALT AT32F435RMT7 (128) tutmuyor.
- Hedef BOM maliyeti (100 set): **STACKF435 29.81 $/stack ≤ 32 $ ✓** (ESC 15.71 + FMU 14.10); ALT'larla dizilen partide ESC +1.92, FMU +5.20 $/kart (en kötü, tüm ALT'lar birlikte).

## 1. ESC (esc55a) — ana / ALT

| Ref | İşlev | Ana (LCSC, üretici, stok) | ALT (LCSC, üretici, stok, 100 set $) | Drop-in kanıtı | Durum |
|---|---|---|---|---|---|
| M1aH…M4cL ×24 | MOSFET 40 V | BLP016N04LC-Q C49328363, Belling, 3 903 | **NTMFS5C430NLT1G C194661**, onsemi, 173 443, 0.216 | DFN5×6 1–3 S / 4 G / 5–8 D, 40 V, T_J 175 °C (BLP016 DS s.1–2; NTMFS DS s.1, s.6); kayıp/bootstrap hesabı NTMFS ile (guc-ip03) | ✓ |
| U11…U41 ×4 | MCU (Bluejay) | EFM8BB21F16I-C-QFN20R C2053222, Silicon Labs, 22 629 | — | — | **İstisna** (§3) |
| U12…U42 ×4 | 3 faz sürücü | JSM6288Q1 C52196409, JSMSEMI, 11 932 | **HL6288Q C50331902**, HL, 6 867, 0.255; ALT2 NSG6288Q C54570588 (WXNSIC, 4 018) | QFN24 FD6288Q dizilimi (HL6288Q DS §5; JSM6288Q1 DS s.2), UVLO+ ≤ 5.1 V → PVDD 7.73 V'ta +2.6 V pay, −40…125 °C (guc-tasarruf §9). **JSM6288Q C19077370 ve JSMSEMI "FD6288Q" C7466367 ALT OLAMAZ** (UVLO ≈ 7 V) | ✓ |
| U1 | Buck 40 V (PVDD) | SCT2400TVBR C2693819, SCT, 8 410 | **JW5026SOTB C185109**, JoulWatt, 12 320, 0.255; ALT2 JW5018 C3040676 | SOT-23-6 BST-GND-FB-EN-VIN-SW (SCT2400 DS s.1; JW5026 DS s.2); aynı FB 20 k / 2.2 k, L00 10 µH; T_J 125 °C | ✓ |
| U2 | Akım yükselteci ×100 | RSA240CXK C54300729, Runic, 3 822 | **INA240A3DR C2060584**, TI, 1 511, 1.788 | SOIC-8 1 IN− 2 GND 3 REF2 4 NC 5 OUT 6 VS 7 REF1 8 IN+ (RSA240 DS s.5; SBOS662 §6); aynı kazanç → `ibata_scale 100` | ✓ (koşul DOG-019, ofset) |
| U0 | LDO 3.3 V | AMS1117-3.3S C347256, UMW, 372 206 | **AMS1117-3.3S C46473005**, TECH PUBLIC, 7 144, 0.037 | SOT-89 1 GND/ADJ, 2 VOUT (sekme), 3 VIN (UMW DS §4; TECH PUBLIC DS s.1); V_IN ≤ 12 V ≥ PVDD 8.53 V; T_J −40…125 | ✓ |
| D00 | TVS 3 kW | SMDJ24CA C284061, DOWO, 2 444 | **SMDJ24CA-AT C523477**, Brightking, 2 981, 0.189 | SMC, V_C 38.9 V @77 A, −55…150 °C (iki DS s.1) | ✓ |
| J0 | SH 8 pin | XY-SM08B-SRSS-TB C54582896, XYECONN, 1 990 | **SM08B-SRSS-TB C160407**, JST (orijinal), 176 871, 0.201; ALT2 SHOU HAN 1.0-8P WT C5340778 | XY bir JST SM08B klonu: JST DS s.1 "PC board layout" (0.6 × 1.55, sekme 1.2 × 1.8, 5.55) ↔ XY DS s.1 (sekme 1.2 × 2.5, 5.50) → ortak ayak izi JST ölçüsü | ✓ (sıcaklık istisnası SYS-086 f) |
| L00 | 10 µH | SWPA3015S100MT C45403, Sunlord, 16 181 | **FNR3015S100MT C167757**, cjiang, 62 190, 0.035 | 3 × 3, 325 mΩ, I_sat 0.92 A, −40…125 °C (iki DS s.1) | ✓ |
| R00 | Shunt 0.1 mΩ 10 W | HoLRS3920 C55113241, Milliohm, 3 830 | **EB390M10PFFWT C55591762**, MHCH, 1 992, 0.433 | 3921 "mikro elektrot" ped 11 / 2.7 / 6.2 = HoLRS (MHCH DS s.3); TCR ±300 ppm → 200 A'da ≈ 7 A < 10 A | **Koşullu** (elektrot sürümü üretici teyidi) |

Genel (kritik değil): 1N4148WS ×12 C2128 (ALT Yangjie C389058), seramikler X7R, dirençler.

## 2. FMU — ana / ALT

| Ref | İşlev | Ana (LCSC, üretici, stok) | ALT (LCSC, üretici, stok, 100 set $) | Drop-in kanıtı | Durum |
|---|---|---|---|---|---|
| U201 | MCU | AT32F435RGT7 C3029577, Artery, 865 | Aynı aile **AT32F435RMT7 C5178940** (128); varyant: **STM32F405RGT6 C15742** (ST, 74), **APM32F405RGT6 C5290473** (Geehy, 1 728) | LQFP64; RMT7 pin birebir; STM32/APM32 62/64 pin aynı, 31/47 VCAP ↔ PH3/PH2 (mcu-secimi §3.1–3.2) | **MCU istisnası** (SYS-095 d, varyant başına derleme) |
| U301 | IMU | LSM6DSV16XTR C5267406, ST, 9 215 | **LSM6DSK320XTR C53025794**, ST, 3 776, 3.662 | §2.1 | **Koşullu** |
| U302 | Baro | SPA06-003 C30589048, Goertek, 39 058 | **DPS368XTSA1(TOKMAS) C55090144**, Tokmas, 10 037, 1.407; ALT2 Infineon DPS368 C3232508 (11 057) | LGA-8 2.0 × 2.5, 1 GND 2 CSB 3 SDA 4 SCK 5 SDO 6 VDDIO 7 GND 8 VDD; ID 0x11 → BF `barometer_dps310.c` her sürüm, AP `SPL06` ≥ 4.6 (yazilim-inceleme §2) | ✓ |
| U303 | Flash 128 Mbit | W25Q128JVSIQ C97521, Winbond, 75 616 | **W25Q128JVSIM C401671**, Winbond, 1 017, 2.225; ALT2 MT25QL128ABA1ESE C41359590 (Micron, 2 050, 10.03) | SOIC-8 208 mil aynı; JEDEC 0xEF7018 / 0x20BA18 BF + AP kararlı ✓ (yazilim-inceleme §4) | ✓ (ALT1 aynı üretici, KRR-011 k.3 gerekçesi: farklı üretici ALT2 10 $) |
| U401 | Analog OSD | AT7456E C82351, ZHONGKEWEI, 22 252 | — (MAX7456EUI C5346361 stok 0; AT7456 C82523 stok 0) | — | **İstisna** |
| U101, U102 | Buck 5 V / 9 V | SY8303AAIC C2937216, Silergy, 12 313 | **SY8303AIC C97054**, Silergy, 114 397, 0.365 | Aynı pin, V_REF, F_SW = 105/R_FS (iki DS s.1–4) | **İstisna** (tek üretici) |
| U103 | 3.3 V buck | TLV62569DBVR C141836, TI, 262 824 | **SY8089A1AAC C479074**, Silergy, 93 251, 0.055 | SOT-23-5 1 EN 2 GND 3 SW 4 VIN 5 FB, V_FB 0.6 V (SLVSDG1C §5; SY8089A1 DS s.1); ortak 2.2 µH + 22 µF + 100 k / 22 k | ✓ |
| L103 | 2.2 µH | WPN201610H2R2MT C97005, Sunlord, 26 550 | **DFE201612P-2R2M=P2 C79317**, Murata, 7 109, 0.087 | 2016, I_sat 2.15 / 2.1 A | ✓ |
| L101 | 6.8 µH | SWPA6045S6R8MT C57254, Sunlord, 8 162 | **FNR6045S6R8MT C168072**, cjiang, 3 103, 0.057 | 6 × 6, I_sat 4.3 A, 40 mΩ | ✓ |
| L102 | 10 µH | SWPA5040S100MT C84608, Sunlord, 45 620 | **FNR5040S100MT C167967**, cjiang, 42 846, 0.047 | 5 × 5, 83 mΩ; I_sat 2.35 / 2.7 A, tepe 2.09 A | **Koşullu** (I_sat teyidi) |
| Y201 | 8 MHz HSE | XC32M4-8.000-F12LGDWL C5179501, HCI, 2 841 | **3X008000BP C19723344**, huaxindianzi, 2 868, 0.118 | 3225-4P, 12 pF, ESR 60 Ω ≤ 100 Ω (AT32/STM32 HSE kazanç payı, bom-maliyet §10.4), −40…85 °C ≥ 85 ✓ | ✓ (pin 1-3 kristal / 2-4 GND pcb teyidi) |
| Y401 | 27 MHz OSD | X322527MSB4SI C9008, YXC, 96 981 | **K3A270002010 C368745**, KYX, 27 386, 0.053 | 3225-4P, 20 pF, ESR 30 Ω, −40…85 °C | ✓ |
| J501 | USB-C 16P | TYPE-C-31-M-12 C165948, HRO, 282 856 | **TYPE-C 16PIN 2MD(073) C2765186**, SHOU HAN, 1 075 715, 0.058 | 16 ped 0.5 aralık, 4 kabuk yuvası 0.6 genişlik, 8.64 / 5.78 (HRO "Recommend PCB layout" 8.65 / 5.78; Shou Han DS s.1); pim ø0.65 / ø0.60 → ortak ped pcb | ✓ (§5 öneri: ana/ALT yer değiştirme) |
| J502 (J503 Dual) | SH 8 | XY-SM08B C54582896 | **JST SM08B-SRSS-TB C160407** | ESC J0 ile aynı | ✓ |
| J504 | SH 4 | XY-SM04B C51940130, 20 981 | **JST SM04B-SRSS-TB C160404**, 75 514, 0.136 | JST orijinali | ✓ |
| J505, J506 | SH 6 | XY-SM06B C56123098, 6 179 | **JST SM06B-SRSS-TB C160405**, 18 817, 0.584 | JST orijinali | ✓ (pahalı: +1.06 $/kart) |
| F101 | Sigorta 5 A | CFS12V3T5R0 C163128, TA-I, 24 182 | **0466005.NRHF C57525**, Littelfuse, 29 557, 0.063 | 1206, 32 V, 50 A kesme, −55…90 °C | ✓ |
| Q101, Q102 | P-MOS (ters kutup, 5 V yük anahtarı) | AO3401A C15127, AOS, 1.6 M | **AO3401A C347476**, UMW, 809 744, 0.024 | SOT-23 1 G 2 S 3 D, −30 V, 50 mΩ | ✓ |
| D102 | TVS 600 W | SMBJ24CA C78416, Brightking, 56 881 | **SMBJ24CA C83268**, Littelfuse, 25 001, 0.112 | SMB, V_C 38.9 V < 40 V | ✓ |
| U501 | USB ESD | USBLC6-2SC6 C2827654, TECH PUBLIC, 219 999 | **USBLC6-2SC6 C7519**, ST, 24 694, 0.119 | ST orijinali, aynı pin | ✓ |
| U502 | SBUS evirici | SN74LVC1G04DBVR C7827, TI, 62 438 | **74LVC1G04GV,125 C12509**, Nexperia, 15 504, 0.125 | SOT-23-5 1 NC 2 A 3 GND 4 Y 5 VCC, −40…125 °C | ✓ |
| D501 | VBUS Schottky | B5819W SL C8598, CJ, 380 514 | **B5819W C64885**, MDD, 563 096, 0.016; ALT2 PMEG3020EH C19268151 (SOD-123F ortak ped) | SOD-123, 40 V 1 A, −55…125 °C | ✓ |

Genel: Q103 MMBT3904 (ALT onsemi C81464), D101 zener (ALT onsemi C39057), D202 1N4148WS, LED, ferrit, düğme, seramikler, dirençler.

### 2.1 LSM6DSV16X muadil taraması (aynı LGA-14L 2.5 × 3 ayak izi, BF + INAV)

| Aday | LCSC, $ @100, stok | WHO_AM_I | Betaflight | INAV | ArduPilot | Sonuç |
|---|---|---|---|---|---|---|
| **LSM6DSV16X** (ana) | C5267406, 2.41, 9 215 | 0x70 | ✓ ≥ 4.5.0 | ✓ 9.1.0 (8.0/9.0 ✗) | ✓ Copter ≥ 4.7.0 | ana |
| **LSM6DSK320X** | C53025794, 3.66, 3 776 | 0x75 | ✓ **≥ 2026.6.0** (2025.12.5 ve 4.5.x'te yok); `common_pre.h` varsayılanında açık, config'te `USE_ACCGYRO_LSM6DSK320X` gerekir | ✓ 9.1.0 (`lsm6dxxIsGenV`, 8 kHz, 2000 dps) | yalnız master (Copter-4.7.2 ✗) | **koşullu ALT** |
| LSM6DSV | C5267399, 7.17, **38** | 0x70 | ✓ (16X olarak) | ✓ | ✓ | yazılımca drop-in, **stok yok** |
| LSM6DSV32X | C22461202, 2.27, 89 | 0x70 | **✗**: sürücü FS_XL = 11 yazar → 32X'te ±32 g, `acc_1G` 16 g varsayılır → ivme yarı ölçek | **✗** (aynı) | ✓ (CTRL8 bit2 ile ayırır, master) | ret |
| LSM6DSV16B / 16BX, ISM330BX, LSM6DSV320X | 7.6 / 5.9 / 10.2 / 9.8 $, stok 0–313 | 0x70/0x75 değil [ST DS'den teyit edilmedi]; üç yazılımın sürücüsünde tanımlı değil | ✗ | ✗ | ✗ | ret |
| LSM6DSVQ / LSM6DSVD / LSM6DSVE | C17496470 1.60 $ (19 486) / C46570983 1.12 $ (312) / C41785564 3.19 $ (1 116) | veri sayfası yok / doğrulanamadı | ? | ? | ? | **araştırılmalı** (LSM6DSVQ ucuz ve stoklu; ST veri sayfası ve WHO_AM_I numuneyle okunmalı) |
| LSM6DSO / DSOX / DSR | 2.7–4.0 $ | 0x6C / 0x6C / 0x6B | DSO ✓ | DSO ✓ | ✗ | ret: gyro ODR 6.66 kHz < 7.68 kHz (SYS-031), AP yok |
| Farklı üretici (TDK, Bosch, klon) | — | — | — | — | — | LSM6DSV pin dizilimli farklı üretici yok |

**Kanıt:** pin tablosu LSM6DSV16X DS13510 Rev 4 §3 Şekil 5 (s.9) ↔ LSM6DSK320X DB5732 Rev 1 Şekil 1 + Tablo 1 (s.4–6) ↔ LSM6DSV DS13476 §3 (s.8): 1 SDO/SA0, 2 SDx, 3 SCx, 4 INT1, 5 VDDIO, 6–7 GND, 8 VDD, 9 INT2, 10 OCS_aux, 11 SDO_aux, 12 CS, 13 SCL/SPC, 14 SDA/SDI; kılıf LGA-14L 2.5 × 3.0 × 0.83 mm; −40…85 °C (SYS-087 ✓); VDD/VDDIO 100 nF. Kaynak: Betaflight `src/main/drivers/accgyro/accgyro_spi_lsm6dsv16x.c` (2026.6.2: `lsm6dsk320xSpiDetect` 0x75), `src/main/target/common_pre.h` satır 145–146; INAV `src/main/drivers/accgyro/accgyro_lsm6dxx.c` (9.1.0: `LSM6DSK320X_CHIP_ID 0x75`); ArduPilot `libraries/AP_InertialSensor/AP_InertialSensor_LSM6DSV.cpp` (master: 0x70 + CTRL8 bit2 = 32X, 0x75 = DSK320X; Copter-4.7.0…4.7.2 yalnız 0x70).
**Kural:** ALT yalnız STACKF435'te; dizilen partide yazılım ≥ BF 2026.6 / INAV 9.1 ve config'te iki sürücü (`gomulu-yazilim`). STACKF405 (ArduPilot) ALT'la dizilmez — ArduPilot kararlı sürümü DSK320X'i içerince kalkar. Aynı üretici (ST): KRR-011 kural 3 gerekçesi "farklı üretici yok". Prototipte bir FMU DSK320X ile (DOG-111).

## 3. İstisna listesi (SYS-095 e — müşteriye bildirilir)

| # | Parça | Neden | Risk azaltma | Risk |
|---|---|---|---|---|
| İ1 | **EFM8BB21F16I-C-QFN20R** (ESC U11…U41) | Bluejay yalnız EFM8BB21/BB51 (`yazilim-inceleme` §10); 125 °C sınıfında stoklu tek kod (QFN20 tray C5727559 stok 0, QSOP24 farklı kılıf, BB51 I sınıfı stok 18); G sınıfı (C80713) SYS-086 ✗ | **Peşin alım 500** (400 + 100 yedek, 500 kademesi 0.821 $ → 410 $); stok izleme (22 629). Tasarım varyantı: kriz hâlinde F16G (85 °C) ile ayrı DT + ESC ısıl ölçüm şartı; uzun vadede BB51 QFN20 (pin farklı → ESC Rev C) | Orta |
| İ2 | **AT32F435RGT7** (FMU U201) | MCU istisnası (SYS-095 d, KRR-012): farklı üretici muadiller ayrı derleme ve ayrı SKU; aynı aile RMT7 stok 128 < 200 | **Peşin alım 200** (2 × 100 set; 160 kademesi 2.854 $ → 571 $; stok 865); kriz: STACKF405A (APM32, 1 728) / STACKF405 (STM32, dış tedarik); varyant config'leri hazır (DOG-049/112) | Orta (RSK-022) |
| İ3 | **AT7456E** (FMU U401) | Stoklu pin uyumlu muadil yok (MAX7456 / AT7456 stok 0; AT7456ELAH LGA-16 farklı kılıf); tek üretici ZHONGKEWEI | **Peşin alım 110** (100 + 10, 1.731 $ → 190 $); MAX7456EUI stok izleme (yazılımca drop-in); tasarım varyantı: OSD'siz BOM (SYS-034 zorunlu → yalnız kriz, DT) | Orta |
| İ4 | **SY8303AAIC** (FMU U101/U102) | FS pinli TSOT-23-8 40 V 3 A başka üretici yok; ALT aynı üreticinin SY8303AIC kodu (C97054, stok 114 397) | Stok izleme (12 313 + 114 397); isteğe bağlı peşin alım 220; 8S varyantında ayrı ayak izi (SYS-046) | Düşük–orta (40 V mutlak = SYS-044 sınırı) |
| (k) | HoLRS3920 shunt (ESC R00) | ALT EB3921 elektrot sürümü teyitsiz | Teyit gelmezse istisna + **peşin 110** (stok 3 830) | Düşük |
| (k) | LSM6DSV16X (FMU U301) | ALT aynı üretici (ST) ve sürüm koşullu (BF ≥ 2026.6, AP master) | İsteğe bağlı **peşin 110** (2.41 $ → 265 $); LSM6DSVQ araştırması | Düşük (stok 9 215) |
| (k) | SH 1.0 konnektörler | Sıcaklık istisnası (≤ 85 °C; SYS-086 f / SYS-087): muadil var, sınıf yok | Serin kenar yerleşimi, DOG-105/108 ölçümü; > 85 °C → Molex Pico-Clasp DT (bom-maliyet §9.10) | Düşük |
| (k) | USB-C HRO (FMU J501) | −30…80 °C < 85 °C (SYS-087) | ALT Shou Han −25…85 °C ✓ → ana yapılması önerilir (§5) | Düşük |

(k) = koşullu / sıcaklık notu; ALT'ı olduğu için sayımda istisna değil.

## 4. Peşin alım listesi (100 set, JLC "parça ayırma" / global sipariş)

| Parça | LCSC | Adet | Birim $ (kademe) | Tutar $ | Neden |
|---|---|---|---|---|---|
| BLP016N04LC-Q | C49328363 | **2 500** | 0.1664 (2 500) | 416 | A1: stok 3 903 < 4 800 (2×); 100 yedek; −0.21 $/set |
| AT32F435RGT7 | C3029577 | **200** | 2.854 (160) | 571 | İ2, RSK-022 (ikinci 100 setin MCU'su dahil) |
| EFM8BB21F16I-C-QFN20R | C2053222 | **500** | 0.821 (500) | 410 | İ1 |
| AT7456E | C82351 | **110** | 1.731 (100) | 190 | İ3 |
| SY8303AAIC | C2937216 | 220 (isteğe bağlı) | 0.329 (100) | 72 | İ4 |
| LSM6DSV16XTR | C5267406 | 110 (isteğe bağlı) | 2.408 (100) | 265 | ST tek üretici |
| HoLRS3920 0.1 mΩ | C55113241 | 110 (yalnız ALT teyitsizse) | 0.294 (50) | 32 | (k) |
| **Zorunlu toplam** | | | | **1 587 $** | (isteğe bağlılar + 369 $) |

STM32F405RGT6 (STACKF405) JLC stoğu 74: ArduPilot SKU'su sipariş üzerine, dış tedarik (6.1–8.3 $).

## 5. Muadil taramasından çıkan ek tasarruf seçenekleri (hedef BOM'a **dahil değil**)

| # | Değişiklik | $/stack | Not |
|---|---|---|---|
| M1 | ESC sürücü ana HL6288Q C50331902 / ALT JSM6288Q1 (yer değiştirme) | −0.37 | UVLO+ maks 5.1 V (JSM 4.5 V tip.) → V_BS payı +1.6 V (DOG-015 ≥ 1 V ✓); `guc-elektronigi` onayı |
| M2 | FMU USB-C ana Shou Han C2765186 / ALT HRO | −0.08 | 85 °C sınıfı ✓ (HRO 80 °C) |
| M3 | Y401 ana KYX C368745 | −0.04 | |
| M4 | L101/L102 ana cjiang FNR | −0.03 | L102 I_sat teyidi |
| | **Toplam** | **≈ −0.5** | |

## 6. 5. adım — `sematik-muhendisi`'ne uygulanacak değişiklikler

Her kritik satıra alan ekle: `ALT MPN`, `ALT LCSC`, `ALT Manufacturer`, `Critical` (evet/hayır), `Exception` (not). Değerler hedef CSV'lerden aynen.

**ESC (esc55a Rev B şematiği):**
1. U2 INA240A3DR → **RSA240CXK C54300729** (SOIC-8 sembol/ayak izi aynı); ALT C2060584.
2. U1 JW5026 → **SCT2400TVBR C2693819**; ALT C185109, ALT2 C3040676.
3. R0 90.9 k → **100 k C25741**; R02 90.9 k → **20 k C25765**; R01 10 k → **2.2 k C25879**.
4. **C03b** (yeni, isteğe bağlı; hedef BOM'da takılı): 10 µF 16 V X7R 0805 **C380347**, PVDD–GND, U1 çıkışına yakın.
5. D13…D45 (12) 1N4148WT → **1N4148WS C2128**, ayak izi **SOD-323**; ALT C389058.
6. ALT alanları: M (C194661), U12…U42 (C50331902; ALT2 C54570588; not: "C19077370 / C7466367 ALT değildir"), D00 (C523477), L00 (C167757), U0 (C46473005), J0 (C160407), R00 (C55591762, koşullu).
7. U11…U41: `Exception` = "Bluejay tek MCU; peşin alım". M: sipariş notu "2 500 adet peşin".

**FMU:**
1. U201 → **AT32F435RGT7 C3029577**; `Variant` F435/F405/A405; ALT/varyant C15742, C5290473, aynı aile C5178940; pin 31/47 notu (mcu-secimi §4.3).
2. U301 ICM-42688-P (Tokmas) → **LSM6DSV16XTR C5267406**: yeni sembol + **LGA-14L 2.5 × 3** ayak izi; bağlantı SPI1: 13 SCL ← SCK, 14 SDA ← MOSI, 1 SDO → MISO, 12 CS ← PA4, 4 INT1 → PC4; 2 SDx ve 3 SCx → GND (Mode 1, DS pin tablosu "Connect to VDDIO or GND"); 10 OCS_aux, 11 SDO_aux boş (lehimli); 9 INT2 boş; 5 VDDIO ve 8 VDD'ye 100 nF (mevcut C301/C303/C304 ile). C302 10 nF (ICM'e özgü) **kaldırılabilir** — LSM6DSV16X DS'de yok (hedef BOM'da C15195 olarak bırakıldı, maliyet ihmal). ALT C53025794 (koşullu, §2.1).
3. U302 DPS368 → **SPA06-003 C30589048**; ALT C55090144, ALT2 C3232508.
4. U103 AMS1117 SOT-223 → **TLV62569DBVR C141836** (SOT-23-5), ALT C479074; **L103 2.2 µH C97005** (ALT C79317); FB **100 k C25741 / 22 k C25768**; C_FF pedi DNP; EN → +5V; C112 = C_IN, C113 = C_OUT.
5. USB sızıntı yük anahtarı: **Q102 AO3401A C15127** (ALT C347476), **Q103 MMBT3904 C20526** (ALT C81464), **R_a, R_b 100 k C25741** (guc-tasarruf §3.2 bağlantısı).
6. D501 → **B5819W SL C8598** SOD-123 (ALT C64885; ALT2 PMEG3020EH C19268151, ortak ped).
7. R104 → **15 k C25756**, R105 → **2 k C4109**; R111 → **22 Ω C25092**.
8. §10 A: C302 → C15195 (veya madde 2'ye göre kaldır), C206 → **2.2 µF 0603 C5360821**, C205 → **10 µF 0805 C380347**, D202 → **1N4148WS C2128** SOD-323.
9. ALT alanları: U303 (C401671; ALT2 C41359590), U101/U102 (C97054, `Exception` tek üretici), Y201 (C19723344), Y401 (C368745), J501 (C2765186), J502/J503 (C160407), J504 (C160404), J505/J506 (C160405), F101 (C57525), Q101 (C347476), D102 (C83268), U501 (C7519), U502 (C12509), L101 (C168072), L102 (C167967, koşullu), D101 (C39057). U401 `Exception` = "stoklu muadil yok; peşin alım".

**Diğer ajanlara bilgi:** `pcb-muhendisi` — ortak ayak izleri (USB-C HRO ↔ Shou Han, SH JST ↔ XY, R00 HoLRS ↔ EB3921, D501 SOD-123/123F, LGA-14L, 2016 bobin); `gomulu-yazilim` — STACKF435 BF config'e `USE_ACCGYRO_LSM6DSV16X` + `USE_ACCGYRO_LSM6DSK320X`, ALT'lı parti için BF ≥ 2026.6; `guc-elektronigi` — M1 (HL6288Q ana) ve L102 ALT I_sat; `test-muhendisi` — DOG-111: prototipte 1 ESC + 1 FMU tüm ALT'larla.
