# FMU seri üretim MCU seçimi — AT32F435 ↔ APM32F405 ↔ STM32F405 (sistem-mimari + gomulu-yazilim + bom-tedarik bakışı)

> **Tarih:** 2026-11-12. **Hazırlayan:** `sistem-mimari` (kapsam: `gomulu-yazilim` yazılım desteği, `bom-tedarik` fiyat/stok). Yalnız bu rapor yazıldı; şematik, gereksinim, firmware, pin haritası değişmedi. Commit yok.
> **Girdi:** müşteri cevapları 2026-11-12 (`sorular.md`: “AT32’yi de değerlendir…”, “2–3 farklı derleme bile yaparız, farklı varyantlar olarak satarız”, IMU LSM6DSV16X), `docs/pin-haritasi.md` v0.1 §1, `docs/mimari-fmu.md`, `docs/rapor/yazilim-inceleme.md`, `firmware/README.md`, `firmware/fmu/STACKF405/config.h`, `boards/fmu/README.md`, `boards/fmu/bom-revb.csv`, SYS-030/031/037/050/056/095, KRR-005/008/010/011.
> **Yöntem:** kaynak kodları ve veri sayfaları oturum dizinine indirildi (repoya konmadı); fiyat/stok `tools/jlc.py`’nin **kopyasıyla** (önbellek bozulmadı). Derleyici ve kart yok → yazılım sonuçları “kaynak koddan; derleyicide/kartta doğrulanacak”.

## 0. Özet (yönetici için)

| # | Sonuç |
|---|---|
| 1 | **Önerilen seri MCU: Artery AT32F435RGT7** (C3029577, 3.27 $ @100, JLC stok 865). Betaflight’ta **4.5.0’dan beri** resmî platform (betaflight/config’te 37 AT32 kart; 2026.6.2’de `AT32F435G.hex` yayımlı), **INAV’da 6.1’den beri** (9.1.0’da 12 AT32 hedefi). APM32F405’e göre +0.07 $/stack, karşılığında INAV + olgun ekosistem + 288 MHz / 384 KB RAM + DMAMUX (14 serbest DMA kanalı) |
| 2 | **Muadiller (ayrı derleme, aynı PCB):** STM32F405RGT6 (BF + INAV + **ArduPilot**), APM32F405RGT6 (yalnız BF ≥ 2025.12; tedarik yedeği). Aynı aile ALT: AT32F435RMT7 (4 MB, `AT32F435M` derlemesi, stok 128 — yetersiz). GD32F405/F450 ve AT32F437 önerilmez (§1) |
| 3 | **ArduPilot AT32’yi ve APM32’yi desteklemiyor** (master `aea9a1b`: MCU tanımları yalnız STM32 + CKS32; AT32 için PR/issue 0). ArduPilot isteyen → **STM32F405RGT6 varyantı** (SYS-056 yalnız bu varyantta) |
| 4 | **Pin uyumu:** AT32F435 LQFP64, STM32F405RG LQFP64 ile **62/64 pin aynı**; fark yalnız **pin 31 (VCAP_1 → PH3)** ve **pin 47 (VCAP_2 → PH2)**. AT32’nin LDO’su dahili, harici kondansatör istemez; PH3/PH2 sıradan G/Ç. **Tek PCB üç MCU’yu taşır**: 2 × 2.2 µF VCAP kondansatörü her varyantta takılı kalır (AT32’de boş G/Ç’ye bağlı, zararsız — §3.2). Ayrı 0 Ω / DNP gerekmez. Emsal: Betaflight `REVO_AT` (“REVO with STM32F405 swapped for an AT32F435”) |
| 5 | **Pin haritası §1 AT32’de aynen karşılanır:** 12 zamanlayıcı pininin AT32 seçenek sırası STM32 ile birebir aynı (`TIMER_PIN_MAP` sıra numaraları değişmez); tüm UART/SPI/I2C/ADC pinleri AT32 tablolarında var. Yalnız `dmaopt` değerleri AT32’ye özgü (kanal indeksi, 0…13) yazılır. DMAMUX sayesinde 8 motor + LED + ADC + SPI1 + **SPI2 (OSD) de DMA’lı** (F405’te SPI2/SPI3 DMA’sız) |
| 6 | **Dikkat:** Betaflight ve INAV AT32’yi **288 MHz / LDO 1.3 V** ile sürer → veri sayfasına göre bu kipte **T_A −40…85 °C, VDD ≥ 3.0 V** (105 °C yalnız ≤ 240 MHz). FMU kuralı ≥ 85 °C (KRR-008 güncel) → **karşılar**, STM32F405RGT6 ile aynı sınıf. MCU akımı artar (DS tip. 231.6 mA “tüm çevre birimleri açık” @288 MHz; STM32 87 mA @168 MHz) → 3.3 V bütçesi `guc-elektronigi` yeniden bakmalı |
| 7 | **Betaflight HSE 8 MHz’e sabit** (AT32 saat kodu `pll_ns 72, pll_ms 1` → yalnız 8 MHz kristalle 288 MHz). Bizim 8 MHz kristal uygun; değiştirilmemeli |
| 8 | **Maliyet (100 set):** AT32 seri ≈ **30.04 $/stack** (KRR-010 APM32 tabanı 29.97 $ + 0.07). STM32 varyantı +1.38 $ (JLC 4.58 $, ama stok 74 < 200 → dış tedarik ≈ 6.1–8.3 $ ile +2.9…+5.1 $). PRJ-004 ≤ 32 $ sağlanır (STM32 varyantı dış tedarikte sınırda) |
| 9 | **Müşteriye 1 soru** (§6): ana MCU AT32F435 + ArduPilot için STM32F405 varyantı onayı (KRR-010’u değiştirir) |

## 1. Karşılaştırma tablosu

Fiyat/stok: JLCPCB parça arayüzü + LCSC ürün sayfası (`tools/jlc.py` kopyası), 2026-11-12. “100 set” = 100 adet (FMU’da 1 MCU) → kırılım 30–159 aralığı; 200 adet (2 × 100 set) kırılımı ayrıca. Stok ölçütü ≥ 200 (2 × 100 set).

| Aday | LCSC | Çekirdek / saat | Flash / RAM | Sıcaklık sınıfı | Paket | JLC stok (LCSC) | ≥ 200? | $ @100 (kırılım) | $ @200 | BF | INAV | ArduPilot | İkinci kaynak durumu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **AT32F435RGT7** (Artery) | **C3029577** | M4F, 288 MHz | 1 MB / 384 KB (512 KB’a ayarlanabilir) | −40…105 °C @ ≤ 240 MHz; **−40…85 °C @ 288 MHz** (LDO 1.3 V, DS Tablo 16) | LQFP64 10×10 | **865** (772) | ✓ | **3.27** (30+) | 2.85 (160+) | ✓ ≥ 4.5.0 (`AT32F435G`) | ✓ ≥ 6.1 | ✗ | Tek üretici (Artery). Aynı aile ALT RMT7; farklı üretici ALT = STM32/APM32 (ayrı derleme) |
| AT32F435RMT7 | C5178940 | M4F, 288 MHz | 4032 KB / 384 KB | aynı | LQFP64 | 128 (128) | ✗ | 4.15 | 3.62 | ✓ (`AT32F435M`) | ✓ (`xMT7`) | ✗ | Aynı kalıp ailesi, pin birebir; ayrı BF derlemesi (`AT32F435M`) |
| AT32F437RGT7 | C5178942 | M4F, 288 MHz (+EMAC) | 1 MB / 384 KB | aynı | LQFP64 | 30 | ✗ | 4.17 | 3.64 | ✗ (hedef yok) | ✗ | ✗ | Önerilmez: EMAC işimize yaramaz, BF hedefi yok, pahalı |
| AT32F437RMT7 | C3029581 | M4F, 288 MHz (+EMAC) | 4032 KB / 384 KB | aynı | LQFP64 | 162 | ✗ | 4.29 | 4.29 | ✗ | ✗ | ✗ | Önerilmez |
| **APM32F405RGT6** (Geehy) | **C5290473** | M4F, 168 MHz | 1 MB / 192 KB | −40…85 °C (T6; DS, `yazilim-inceleme`) | LQFP64 | **1 728** (—) | ✓ | **3.20** (30+) | 2.79 (160+) | ✓ ≥ 2025.12 (`APM32F405`) | ✗ | ✗ | Tek üretici; BF’de bu MCU’lu kayıtlı kart **yok** (ilk biz olurduk) |
| **STM32F405RGT6** (ST) | **C15742** | M4, 168 MHz | 1 MB / 192 KB | −40…85 °C | LQFP64 | **74** (74) | ✗ | 4.58 (100+) | 4.58 | ✓ tüm sürümler | ✓ | ✓ (`STM32F405xx.py`, kısıtlı) | Dış tedarik gerekir (≈ 6.1–8.3 $, KRR-010 bağlamı) |
| STM32F405RGT7 | C1337199 | M4, 168 MHz | 1 MB / 192 KB | −40…105 °C | LQFP64 | 4 | ✗ | 13.03 | 13.03 | ✓ | ✓ | ✓ | Pahalı, stok yok (KRR-008 güncellemesinde bırakıldı) |
| GD32F405RGT6 (bilgi) | C99031 | M4, 168 MHz | 1 MB / 192 KB | −40…85 °C | LQFP64 | 222 | ✓ | 3.46 | 3.07 | ✗ (BF’de GD32 platformu yok; Configurator yalnız USB kimliğini tanır) | ✗ | ✗ | Önerilmez: hiçbir uçuş yazılımında resmî değil; VDD 2.6–3.6 V |
| GD32F450 (bilgi) | — | M4, 200 MHz | — | — | LQFP64 sürümü JLC’de yok (V/Z/I kılıflar: C174269 vb.) | — | — | — | — | ✗ | ✗ | ✗ | Uygulanamaz (kılıf) |

Notlar:
- **AT32 sıcaklık:** “T7” 105 °C sınıfı yalnız LDO ≤ 1.2 V (≤ 240 MHz) için geçerli. Betaflight `startup/at32f435_437_clock.c` ve INAV `drivers/system_at32f43x.c` 288 MHz + `PWC_LDO_OUTPUT_1V3` kullanıyor → pratikte 85 °C parça. FMU için müşteri kuralı ≥ 85 °C (KRR-008 güncellemesi) → uygun. 105 °C gerekirse kendi derlememizde 240 MHz’e indirmek kaynak değişikliği ister (SYS-050 “kaynak değiştirilmez” ile çelişir) → önerilmez.
- **Güç kaybı:** AT32 LQFP64 θJA 64.4 °C/W, P_D (T_A 105 °C) 310 mW. 288 MHz’te DS akımı tip. 231.6 mA / maks. 260 mA (85 °C) “tüm çevre birimleri açık” koşulunda (≈ 0.86 W → ≈ +55 °C, JEDEC kartı). Betaflight yalnız kullandığı birimlerin saatini açar (DS “tüm çevre birimleri kapalı” tip. 59.9 mA); gerçek değer tahmini 100–150 mA — **kartta ölçülecek** (DOG-041 bağlamı). STM32F405 karşılığı tip. 87 / maks. 102 mA (DS Tablo 20).

## 2. Yazılım desteği (kaynak koddan)

### 2.1 Betaflight

Kaynak: betaflight **2026.6.2** (`e0b7bb01b17b`), betaflight/config `cacb3a0` (2026-11-09), configurator master `9c8b310a3f40`.

| Konu | AT32F435 | APM32F405 | STM32F405 | Kaynak |
|---|---|---|---|---|
| Platform, ilk sürüm | `src/platform/AT32/target/AT32F435G` (1 MB, `-DAT32F435RGT7`) ve `AT32F435M` (4 MB). **4.5.0’da var** (`src/main/target/AT32F435G`), 4.4.3’te yok | 2025.12’den beri | her sürüm | GitHub API `contents?ref=` |
| Yayımlanan hex (2026.6.2) | `betaflight_2026.6.2_AT32F435G.hex`, `…_AT32F435M.hex` | `…_APM32F405.hex` | `…_STM32F405.hex` | sürüm ekleri |
| Kayıtlı kart (betaflight/config) | **37** (25 × F435G, 12 × F435M) | **0** | 180 | `FC_TARGET_MCU` taraması |
| Saat | 8 MHz HEXT sabit → 288 MHz, APB 144 MHz, LDO 1.3 V | HSE 8 → 168 MHz | HSE 8 → 168 MHz | `AT32/startup/at32f435_437_clock.c` (`crm_pll_config(…, 72, 1, FR_2)`), `at32f435_437_conf.h` `HEXT_VALUE 8000000` |
| DShot | ✓ zamanlayıcı DMA (`pwm_output_dshot.c`) | ✓ | ✓ | `AT32/pwm_output_dshot.c` |
| Çift yönlü DShot | ✓ `USE_DSHOT_TELEMETRY` (common_pre.h; AT32 `pwm_output_dshot.c` 17 yerde) | ✓ | ✓ | `main/target/common_pre.h` 85–91 |
| Bit-bang DShot | ✓ (`dshot_bitbang.c`; ORBITF435, SPEEDYBEEF435AIOELRS, IFLIGHT_BLITZ_F435 varsayılanı ON) | ✓ | ✓ | |
| DShot burst (DMAR) | ✗ (`#undef USE_DSHOT_DMAR`) — biz zaten `DSHOT_DMAR_OFF` | ✓ | ✓ | `AT32/target/AT32F435G/target.h` |
| DMA | **DMAMUX**: DMA1 CH1–7 + DMA2 CH1–7 = 14 kanal, her istek her kanala; `dmaopt` = kanal indeksi 0…13 | STM32 F4 tablosu (sabit akış/kanal) | sabit akış/kanal | `AT32/dma_reqmap_mcu.c` (`dmaChannelSpec[]`, `dmaSetupRequest`) |
| SPI DMA ayırma | `USE_SPI_DMA_ENABLE_LATE`: motor/LED/ADC’den **sonra**, boş ilk kanal | EARLY | EARLY | `platform/common/stm32/bus_spi_hw.c` `spiInitBusDMA` |
| F4 DMA2 hata kaydı (bit-bang + SPI) | yok (kural yalnız `STM32F4 || APM32F4`) | var | var | aynı dosya |
| PPM / PWM alıcı | ✗ (`#undef USE_RX_PPM`, `USE_RX_PWM`) — SYS’te PPM yok | ✓ | ✓ | target.h |
| UART | 8 (UART7/8 dahil); PH2/PH3 UART4 alternatifi | 6 | 6 | `serial_uart_at32f43x.c` |
| USB VCP | 2E3C:5740 “AT32 VCP” | 314B:5740 | 0483:5740 | configurator `src/js/protocols/devices.ts` 98–100 |
| ROM DFU | **2E3C:DF11** “AT32F435 DFU Bootloader” (Configurator listesinde) | 314B:0106 | 0483:DF11 | `devices.ts` 155–157 |
| ROM önyükleyici yolları | OTGFS1 (PA11/PA12), USART1 (PA9/10), USART3 (RxT7: PC10/11) | — | — | AT32F435/437 DS v2.01 §2.5 Tablo 5 |
| BF’den ROM’a atlama | ✓ `systemResetToBootloader(BOOTLOADER_REQUEST_ROM)` | ✓ | ✓ | `AT32/system_at32f43x.c` 104–130 |
| Yükleme yolu | BOOT düğmesi + USB → ROM DFU → Configurator “Load firmware” → `STACKF435`; veya CLI `dfu`. Windows’ta Artery DFU için WinUSB sürücüsü gerekebilir (ImpulseRC Driver Fixer/Zadig). Configurator MCU türünü denetlemez (`yazilim-inceleme` §1.3) — ama USB kimliği farklı olduğundan yanlış varyant ekranda görünür | aynı | aynı | — |

### 2.2 INAV

Kaynak: INAV **9.1.0** (`e519b69`).

| Konu | Bulgu |
|---|---|
| AT32 desteği | `src/main/drivers/*_at32f43x.c` (adc, i2c, spi, uart, usb vcp/msc, timer, dma, system); CMake `target_at32f43x_xGT7()/xMT7()` |
| İlk sürüm | **6.1** (NEUTRONRCF435MINI/SE/WING; 6.0.0’da yok) |
| 9.1.0 AT32 hedefleri | BETAFPVF435, BLUEBERRYF435WING, DAKEFPVF435, IFLIGHT_BLITZ_ATF435, JHEMCUF435, JHEMCUF435AIO, NEUTRONRCF435MINI/SE/WING, **ORBITF435** (+ ORBITF435_SD), SAGEATF4, TBS_LUCID_FC |
| STM32F405 | ✓ (`target_stm32f405xg(SPEEDYBEEF405V4)` dahil 88 hedef) |
| APM32 | ✗ |
| Hedef biçimi | INAV unified config kullanmaz: **kendi `src/main/target/STACKF435/` (target.h/.c, CMakeLists) yazılıp INAV’a PR** gerekir; STM32 varyantı için `target_stm32f405xg(STACKF405)` aynı klasörde ikinci satır |
| LSM6DSV16X | ✓ 9.1.0 `drivers/accgyro/accgyro_lsm6dxx.c` (`LSM6DSV16X_CHIP_ID 0x70`); **9.0.0 ve 8.0.0’da yok** → INAV ≥ 9.1 |

### 2.3 ArduPilot

master `aea9a1b5d4d8` (2026-11-11): `libraries/AP_HAL_ChibiOS/hwdef/scripts/` MCU tanımları STM32F1/F3/F4/F7/G4/H7/L4 + `CKS32F407xx.py`; **AT32 ve APM32 yok**. GitHub aramada AT32F435 için kod 0, issue/PR 0; ArduPilot/ChibiOS’ta AT32 HAL yok. → **ArduPilot yalnız STM32F405RGT6 varyantında** (SYS-056; `speedybeef4v4` türevi hwdef, `yazilim-inceleme` Y6).

### 2.4 Sürücülerde MCU’ya bağlı fark

Betaflight 2026.6.2 `src/main/drivers/` altında “AT32/APM32” geçen **hiçbir dosya yok** → IMU, baro, flash, OSD sürücüleri MCU’dan bağımsız; fark yalnız platform katmanında (SPI/I2C/UART/DMA).

| Sürücü | BF | INAV | AP (STM32 varyantı) | MCU farkı |
|---|---|---|---|---|
| IMU LSM6DSV16X | ✓ `accgyro_spi_lsm6dsv16x.c` (4.5.0’dan beri); AT32 kartta kullanılıyor: `AIRBOTSUPERF4`, `AIRBOTSUPERF4V2` (AT32F435M) | ✓ ≥ 9.1 | ✓ (`LSM6DSV`, `yazilim-inceleme` §3) | yok |
| Baro DPS310/SPA06 | ✓ `barometer_dps310.c` | — (`gomulu-yazilim` ayrıca bakar) | ✓ (iki BARO satırı) | yok |
| SPI flash W25Q128 | ✓ `flash_m25p16.c` | ✓ | ✓ JEDEC | yok; AT32’de SPI3 DMA’sız kalır (F405’le aynı) |
| OSD AT7456E | ✓ `max7456.c` | ✓ | ✓ | AT32’de SPI2 **DMA’lı** olabilir (§3.4) |
| Bluetooth | Tasarımda BT yok; olursa UART üstü modül (MSP) → MCU bağımsız | | | yok |

## 3. Pin uyumu ve ortak ayak izi

### 3.1 LQFP64 pin karşılaştırması

Kaynak: AT32F435/437 DS v2.01 (LCSC C3029577 PDF) Şekil 4 + pin tablosu; STM32F405 `lib/datasheet/STM32F405RGT6.pdf` Tablo 7; APM32 `yazilim-inceleme` §11 (VCAP_2 47, BOOT0 60 STM32 ile aynı).

| LQFP64 pin | STM32F405RG | APM32F405RG | AT32F435RG | Bizdeki ağ | Ortak ayak izinde |
|---|---|---|---|---|---|
| 1 | VBAT | VBAT | VBAT | 3V3 | aynı |
| 5 / 6 | PH0 / PH1 (HSE) | aynı | PH0 / PH1 (HEXT 4–25 MHz) | 8 MHz kristal | aynı (BF AT32 8 MHz’e sabit) |
| 7 | NRST | NRST | NRST | 100 nF | aynı |
| 12 / 13 | VSSA / VDDA | aynı | VSSA/VREF− / VDDA/VREF+ (**VDDA = VDD şart**, DS Tablo 15) | ferrit + 1 µF + 100 nF | aynı (ferrit DC düşümü ihmal edilebilir) |
| 18 / 63 | VSS | VSS | VSS | GND | aynı |
| 19 / 32 / 48 / 64 | VDD | VDD | VDD (2.6–3.6 V; 288 MHz’te ≥ 3.0 V) | 3V3 | aynı |
| 28 | PB2 / BOOT1 | aynı | PB2 / BOOT1 | 10 k → GND | aynı (BOOT0 = 1, BOOT1 = 0 → ROM) |
| 30 | PB11 | PB11 | PB11 | PINIO1 (9 V EN) | aynı (not: F401/F411 LQFP64’te pin 30 VCAP’tır; F405’te değil) |
| **31** | **VCAP_1** | **VCAP_1** | **PH3** (G/Ç: UART4_TX, I2C2_SDA alt.) | 2.2 µF → GND | **fark** |
| **47** | **VCAP_2** | **VCAP_2** | **PH2** (G/Ç: UART4_RX, I2C2_SCL alt.) | 2.2 µF → GND | **fark** |
| 60 | BOOT0 | BOOT0 | BOOT0 (dahili zayıf aşağı çekme) | 10 k → GND + düğme → 3V3 | aynı |
| diğer 49 G/Ç | — | — | aynı adlar | pin haritası §1.1 | aynı |

AT32F435’in LDO’su dahili, çıkış kondansatörü istemez (DS §2.4.3); ayrıca BYPASS_REG/PDR_ON pini LQFP64’te üç MCU’da da yok.

### 3.2 VCAP kondansatörleri AT32’de

- AT32 açılışta PH2/PH3’ü giriş olarak bırakır; Betaflight `unusedPinsInit()` (`platform/common/stm32/system.c` 320–330) sahipsiz pinleri **girişe + iç çekme direncine** (IPU) alır (`TARGET_IO_PORTH 0xffff`). 2.2 µF bu durumda ~40 kΩ üstünden 3.3 V’a dolar (τ ≈ 90 ms), sürekli akım yok → **zararsız**. Pin hiçbir derlemede çıkış olarak atanmadığı sürece (config’imizde PH2/PH3 yok) güvenli.
- Bu yüzden **önerilen ortak ayak izi:** C_VCAP1/C_VCAP2 (2.2 µF X7R) **her üç varyantta takılı**, tek BOM; 0 Ω/DNP ek parça gerekmez. KRR-011 kural 4 (“pasif değer iki parçayı da karşılar”) sağlanır.
- Alternatif (önerilmez): AT32 varyantında kondansatörler DNP + PH2/PH3’ü 7. UART/I2C2 olarak pede çıkarmak. Bu, VCAP ağına başka iz bağlamak demek → STM32/APM32’de çekirdek beslemesine gürültü/kaçak riski. SYS-035 (≥ 6 UART) zaten karşılanıyor.
- Gerçek emsal: Betaflight `configs/OPEN/REVO_AT/config.h` (“REVO with STM32F405 swapped for an AT32F435”) — F405 PCB’sine AT32 dizilmiş; `ORBT/ORBITF435`, `TEBS/TBS_LUCID_FC` PH3/PH2’yi UART4 olarak, `SPBE/SPEEDYBEEF435AIOELRS`, `IFRC/IFLIGHT_BLITZ_F435` I2C2 olarak kullanıyor (AT32’ye özel PCB’ler). Artery’nin STM32F405→AT32F435 geçiş notu aramada bulunamadı (yalnız MG0018 AT32F403A→F435); pin farkı DS’den.

### 3.3 Gerçek AT32F435 kartlarının pin atamaları (betaflight/config `cacb3a0`)

| Kart | MCU hedefi | Motor pinleri | LED | DMA yaklaşımı | Bize benzerlik |
|---|---|---|---|---|---|
| **ORBT/ORBITF435** (Orbit) | F435G, HSE 8 | PB0, PB1, PB10, PB11, PA15, PB6, PB7, PA1 (8) | PA0 | bit-bang ON | SPI1 PA5/6/7 IMU (CS PA4, EXTI PC4), SPI2 PB13/PC2/PC3 OSD (CS PB12), SPI3 PB3/4/5 flash/SD, I2C1 PB8/9, UART5 PC12/PD2, UART6 PC6/7, ADC PC0/PC1/PC5, beeper PC15, LED0 PC13, `PINIO1_CONFIG 129` + `PINIO1_BOX 40` — **bizim SPEEDYBEEF405V4 türevi haritaya çok yakın** |
| IFRC/IFLIGHT_BLITZ_F435 | F435G | PB0, PB1, PC8, PC9, PB6, PB7, PB11, PB10 | PA8 | zamanlayıcı DMA, `dmaopt` 1…8 tekil, LED 0, ADC 11 | Motor + LED pinlerinin 7’si bizimle aynı → **aynı pinlerle 8 motor + LED zamanlayıcı DMA’sıyla çalışan kayıtlı kart** |
| AIRB/AIRBOTSUPERF4V2 | F435M | PC9, PC8, PB7, PB6, PB0, PB1, PC7, PC6 | PA15 | `dmaopt` 0…8 tekil, ADC 9 | LSM6DSV16X + 8 motor |
| TEBS/TBS_LUCID_FC | F435M | PC6, PB5, PC8, PC9, PA0–PA3 | PA8 | M1–M4 DMA 9–12, M5–M8 DMA’sız, `SPI3_TX_DMA_OPT 5` | UART4 = PH3/PH2 |
| SPBE/SPEEDYBEEF435AIOELRS | F435G, HSE 8 | PB6, PB7, PB0, PB1 | PB12 | bit-bang ON, ADC 11 | SpeedyBee’nin AT32’ye geçişi |
| NERC/NEUTRONRCF435 | F435G | PC9, PC8, PC7, PC6 | PA1 | `dmaopt` 0…3, LED 4, ADC 8 | INAV’da da hedef |

Diğer AT32F435 config’leri: AIRBOTSUPERF4, BAYCK_DOLPHIN(_MINI), BETAFPVF435, BROTHERHOBBYF435, CCRCF435AIO, ACCIF435(ELITE), DARWINF435, DAKEFPVF435(HD), FLYCOLORF435, GREATMOUNTAINF435, HUMMINGBIRD_200RS/AIO255, HGLRCF435AIO, IFLIGHT_BORG_F435S, JHEF435(PRO), NEUTRONRCF435MINI/SE, OXBOTF43512AAIO, OXBOT_FLOW_AIO45, SKYSTARSF435(PRO), TBS_LUCID_AIO/MOD_FC/PRO_FC, TUNERCF435, ATSTARTF435, REVO_AT.

### 3.4 Bizim pin haritası §1 AT32F435’te

**Zamanlayıcı** (`AT32/timer_at32f43x.c` ↔ `STM32/timer_stm32f4xx.c`, dosya sırası karşılaştırması):

| Pin | İşlev | AT32 seçenekleri (sıra) | STM32 seçenekleri (sıra) | `TIMER_PIN_MAP` sırası |
|---|---|---|---|---|
| PB6 / PB7 | M1 / M2 | TMR4_CH1 / TMR4_CH2 | TIM4 aynı | 1 / 1 (aynı) |
| PB0 / PB1 | M3 / M4 | TMR1_CH2N/3N, **TMR3_CH3/4**, TMR8_CH2N/3N | aynı sıra | 2 / 2 (aynı) |
| PC8 / PC9 | M5 / M6 | TMR3_CH3/4, **TMR8_CH3/4** | aynı | 2 / 2 (aynı) |
| PB10 / PA15 | M7 / M8 | TMR2_CH3 / TMR2_CH1 | aynı | 1 / 1 (aynı) |
| PA8 | LED | TMR1_CH1 | aynı | 1 |
| PB14 / PB15 | CC / servo | TMR1_CH2N/3N, TMR8_CH2N/3N, **TMR12_CH1/2** | aynı | 3 / 3 |
| PA3 | PPM | TMR2_CH4, TMR5_CH4, TMR9_CH2 | aynı | (AT32’de PPM derlenmez → satır etkisiz) |

Zamanlayıcı grupları (TIM4, TIM3, TIM8, TIM2 çiftleri) aynı → DShot hız kısıtı aynı.

**Pin işlevleri:** UART1–6 (PA9/10, PA2/3, PC10/11, PA0/1, PC12/PD2, PC6/7) `serial_uart_at32f43x.c`’de ✓; SPI1 PA5/6/7, SPI2 PB13/PC2/PC3, SPI3 PB3/4/5 `bus_spi_pinconfig.c` `#ifdef AT32F4` ✓; I2C1 PB8/PB9 `bus_i2c_atbsp_init.c` ✓; ADC PC0 (IN10), PC1 (IN11), PC5 (IN15) `adc_at32f43x.c` ✓; USB PA11/12 OTGFS1 ✓. → **§1.1 tablosu AT32’de değişmeden geçerli.**

**DMA (önerilen AT32 ataması, `dmaopt` = kanal indeksi):**

| dmaopt | Kanal | Kullanıcı |
|---|---|---|
| 0–6 | DMA1 CH1–CH7 | M1…M7 |
| 7 | DMA2 CH1 | M8 |
| 8 | DMA2 CH2 | LED şerit (TMR1_CH1) |
| 9 | DMA2 CH3 | ADC1 (`ADC1_DMA_OPT 9`) |
| 10–11 | DMA2 CH4–5 | SPI1 TX/RX (gyro) — LATE ayırmada otomatik |
| 12–13 | DMA2 CH6–7 | SPI2 TX/RX (OSD) — otomatik |
| — | — | SPI3 (flash) DMA’sız (F405’le aynı) |

**DMAMUX avantajı:** F405’te SPI1’in DMA’sını kurtarmak için `ADC1_DMA_OPT 1` ve “TIM8_CH3 dmaopt 1 kullanma” gibi akış satrancı gerekiyordu (pin-haritasi §1.3) ve SPI2/SPI3 DMA’sız kalıyordu. AT32’de her istek her kanala gider: çakışma denetimi “14 kanal ≥ kullanıcı sayısı” sayımına iner; OSD de DMA’lı; ileride bit-bang DShot’a geçilirse (3 port → ~3 kanal) SPI3 da DMA alır; F4 DMA2 hata kaydı (bit-bang + SPI) AT32’de yok. 8 motor + çift yönlü DShot + LED + gyro DMA = SYS-037 AT32’de **payla** karşılanır (kartta `dma show`, DOG-034/035).

## 4. Öneri

### 4.1 MCU kararı (KRR-010’un yerine KRR önerisi — `gereksinim-muhendisi`)

| Rol | MCU | Gerekçe |
|---|---|---|
| **Seri (ana)** | **AT32F435RGT7** (C3029577) | BF ≥ 4.5 + INAV ≥ 6.1 resmî, 37 BF / 12 INAV kart emsali (8 motorlu dahil), stok 865, 3.27 $; 288 MHz/384 KB, DMAMUX; APM32’ye göre +0.07 $/stack |
| Muadil 1 (farklı üretici, ArduPilot) | **STM32F405RGT6** (C15742) | Tek ArduPilot uyumlu aday; BF + INAV; tedarik dış kaynak |
| Muadil 2 (farklı üretici, tedarik yedeği) | APM32F405RGT6 (C5290473) | En ucuz, stok 1 728; yalnız BF ≥ 2025.12, INAV/AP yok, BF’de kayıtlı kartı yok |
| Aynı aile yedek | AT32F435RMT7 (C5178940) | Pin birebir; BF `AT32F435M` derlemesi; bugün stok 128 |
| Önerilmeyen | AT32F437x, GD32F405/F450, STM32F405RGT7 | yazılım desteği yok / kılıf yok / fiyat-stok |

### 4.2 Varyant / derleme planı

| SKU (öneri adı) | MCU | Betaflight config (betaflight/config) | INAV hedefi | ArduPilot | Not |
|---|---|---|---|---|---|
| **STACKF435** (standart, seri) | AT32F435RGT7 | `STACKF435` — `FC_TARGET_MCU AT32F435G`, BF ≥ 4.5.0 (öneri 2026.6.2) | `STACKF435` — `target_at32f43x_xGT7(STACKF435)`, INAV ≥ 9.1 (LSM6DSV16X için) | ✗ | Dual-ESC (J503) BOM varyantı aynen |
| **STACKF405** (ArduPilot / “Pro”) | STM32F405RGT6 | `STACKF405_STM` — `STM32F405` | `target_stm32f405xg(STACKF405)` (aynı INAV klasörü) | ✓ kendi hwdef (`speedybeef4v4` türevi, SYS-056) | ArduPilot isteyen müşteri bu SKU |
| STACKF405A (yalnız tedarik krizi) | APM32F405RGT6 | `STACKF405` — `APM32F405`, BF ≥ 2025.12 | ✗ | ✗ | Satış adı STACKF435 yerine; INAV yok uyarısı |
| (yedek) | AT32F435RMT7 | `STACKF435M` — `AT32F435M` | `target_at32f43x_xMT7` | ✗ | Yalnız RGT7 bulunamazsa |

Config içeriği üç MCU’da **pin satırları aynı**; AT32 config farkları: `FC_TARGET_MCU`, `TIMER_PIN_MAPPING` 4. sütun (dmaopt 0…8, §3.4), `ADC1_DMA_OPT 9`, `RX_PPM_PIN` etkisiz. `gomulu-yazilim`: `firmware/fmu/STACKF435/config.h` (yeni) + mevcut APM32/STM32 dosyaları; INAV hedefi. MCU türü ipek baskıda (üç kutu: F435 / F405 / A405 — dizgide işaretlenir) ve kutu etiketinde.

### 4.3 Ortak ayak izi — **gerekli değil (zaten ortak)**; şematik değişikliği listesi (`sematik-muhendisi`)

Mevcut `boards/fmu/fmu/mcu.kicad_sch` STM32F405 düzeni AT32’yi taşır. Değişiklikler yalnız alan/not düzeyinde:

| # | Ref / ağ | Değişiklik |
|---|---|---|
| 1 | U201 | MPN/LCSC ana: **AT32F435RGT7 / C3029577**; `ALT MPN`: STM32F405RGT6 (C15742), APM32F405RGT6 (C5290473), AT32F435RMT7 (C5178940); `Variant` alanı: F435 / F405 / A405; Temperature: “−40…85 °C @288 MHz (DS Tablo 16)”; not: “her MCU ayrı yazılım derlemesi (SYS-095 d istisnası)” |
| 2 | U201 pin 31, 47 | Sembolde pin adı “VCAP_1/PH3”, “VCAP_2/PH2” (veya not); ağ adları VCAP1/VCAP2 **başka hiçbir şeye bağlanmaz** |
| 3 | C_VCAP × 2 (2.2 µF X7R) | Değer/takılı durum değişmez, tüm varyantlarda takılı; açıklama “AT32’de PH3/PH2 G/Ç, kondansatör zararsız (mcu-secimi §3.2)”. APM32 VCAP değeri Geehy DS’den teyit (yazilim-inceleme’de DS metni kısmen bozuk) |
| 4 | Y201 8 MHz | Değişmez; açıklamaya “BF AT32 8 MHz’e sabit — değiştirme” |
| 5 | BOOT0 (10 k + SW201), BOOT1/PB2 (10 k → GND) | Değişmez (AT32 ROM DFU: BOOT0 = 1, BOOT1 = 0) |
| 6 | VDDA ferrit | Değişmez; not “AT32: VDDA = VDD şart” |
| 7 | İpek baskı | MCU türü işaret kutusu (F435 / F405 / A405) — `pcb-muhendisi` |
| 8 | 3.3 V regülatör (U103, SYS-042 küçük kılıf işi) | **`guc-elektronigi`**: MCU payı 102 mA → AT32 288 MHz için en kötü 260 mA (DS), gerçekçi tahmin 100–150 mA; 3V3 toplamı ve regülatör ısıl payı yeniden hesaplanır, prototipte ölçülür |

Pin haritası (`docs/pin-haritasi.md`, sahibi sistem-mimari) için sonraki iş: §1.3’e AT32 `dmaopt` sütunu (§3.4 tablosu), §1 başlığına AT32 pin 31/47 notu (bu görevde dosya değiştirilmedi).

### 4.4 Maliyet etkisi (100 set, JLC 2026-11-12)

| Varyant | MCU $ | Δ $/stack (APM32 KRR-010 tabanına göre) | Stack (KRR-010 A+B+APM32 ≈ 29.97 $ tabanı) |
|---|---|---|---|
| STACKF435 (AT32F435RGT7) | 3.27 (200 adet: 2.85) | **+0.07** | **≈ 30.04 $** ≤ 32 ✓ |
| STACKF405A (APM32) | 3.20 (2.79) | 0 | ≈ 29.97 $ |
| STACKF405 (STM32, JLC fiyatı) | 4.58 | +1.38 | ≈ 31.35 $ ✓ — ama stok 74 |
| STACKF405 (STM32, dış tedarik 6.1–8.3 $) | 6.1–8.3 | +2.9…+5.1 | ≈ 32.9–35.1 $ ✗ (ArduPilot SKU’su fiyatına yansıtılır) |
| AT32F435RMT7 (yedek) | 4.15 | +0.95 | ≈ 30.9 $ |

PCB, dizgi ve diğer BOM değişmez (aynı ayak izi, aynı pasifler). AT32 için 3.3 V regülatör sınıfı büyürse (madde 8) etkisi `guc-elektronigi`/`bom-tedarik` hesabıyla eklenir (tahmin < 0.1 $).

### 4.5 Riskler

| # | Risk | Etki | Önlem |
|---|---|---|---|
| R1 | ArduPilot AT32/APM32’yi desteklemiyor | SYS-056 yalnız STM32 SKU’sunda | STACKF405 varyantı; SYS-056 metni DT ile “STM32F405 varyantında” (gereksinim-muhendisi) |
| R2 | AT32 tek üretici (Artery) | Tedarik kesintisi | Aynı PCB’de STM32/APM32 muadil (ayrı derleme); 2 × 100 set için peşin alım (stok 865) |
| R3 | 288 MHz kipte 85 °C sınırı ve yüksek akım | FMU yığında 85 °C’ye yaklaşırsa | KRR-008 FMU ölçümü (DOG-104…108), MCU kılıf ölçümü; 3V3 bütçesi (§4.3-8) |
| R4 | BF AT32 farkları: PPM yok, DMAR yok, SPI DMA LATE | PPM SYS’te yok; DMAR kullanmıyoruz | Bilgi; kartta `dma show` / `timer show` (DOG-034/035) |
| R5 | 8 kanal zamanlayıcı tabanlı çift yönlü DShot AT32’de tezgâhta denenmedi (emsal kartların çoğu bit-bang) | SYS-037 | DOG-034; gerekirse `DSHOT_BITBANG_ON` (LED TMR1 ile çakışma AT32’de bit-bang zamanlayıcı seçimine göre kontrol) |
| R6 | INAV unified config yok | INAV’a hedef PR’ı + bakım | `gomulu-yazilim` iş paketi; INAV ≥ 9.1 |
| R7 | Yanlış varyant hex’i | Kart açılmaz | ROM DFU ile kurtarılır; USB kimlikleri farklı (2E3C / 0483 / 314B); ipek baskı işareti |
| R8 | Windows’ta Artery DFU sürücüsü | Kullanıcı yükleyemez | Kılavuzda ImpulseRC Driver Fixer/Zadig adımı; DOG-112’ye AT32 eklenir |
| R9 | STM32 stoğu 74 | ArduPilot SKU üretimi | Dış tedarik veya ArduPilot SKU sipariş üzerine |

### 4.6 Etkilenen işler

- `gereksinim-muhendisi`: KRR-010 → yeni KRR (AT32 seri); SYS-030 (AT32F435RG eklenir, “her MCU ayrı derleme” istisnası, ArduPilot yalnız STM32), SYS-050 (“AT32 ≥ 4.5.0, APM32 ≥ 2025.12”; INAV ≥ 9.1 eklenecekse yeni madde), SYS-056 (STM32 varyantına daralt), SYS-087 (AT32 85 °C @288 MHz notu), SYS-095 (d) MCU istisnası; DT numarası.
- `sematik-muhendisi`: §4.3 maddeleri 1–6.
- `guc-elektronigi`: §4.3-8 (3.3 V bütçesi).
- `gomulu-yazilim`: `STACKF435` BF config + INAV hedefi; DOG-112’ye AT32 DFU.
- `bom-tedarik`: U201 satırı ve ALT alanları, peşin alım.
- `pcb-muhendisi`: ipek baskı MCU işareti.

## 5. Doğrulama planı

| # | Kontrol | DOG |
|---|---|---|
| 1 | `make CONFIG=STACKF435` (AT32F435G) uyarısız; INAV `STACKF435` derlemesi | DOG-049/050 |
| 2 | AT32 kartta BOOT + USB → 2E3C:DF11 → Configurator yüklemesi; VCP 2E3C:5740; `status` 288 MHz | DOG-112 |
| 3 | `timer show`, `dma show`, `resource show` → §3.4 | DOG-034/035 |
| 4 | 8 × DShot600 çift yönlü + LED + OSD + blackbox + 8 kHz gyro (LSM6DSV16X) eşzamanlı, CPU yükü | DOG-034, 094–096 |
| 5 | Aynı PCB’de STM32F405 ve APM32F405 dizilmiş birer kart (VCAP takılı) açılış/USB | DOG-111 |
| 6 | 3V3 akımı ve MCU kılıf sıcaklığı (AT32 vs STM32) yığında | DOG-041, DOG-104…108 |

## 6. Müşteriye sorulacak (1)

**“Seri üretim MCU’su AT32F435 olsun mu? Betaflight ve INAV’ı destekliyor, maliyet APM32 ile aynı (+0.07 $). ArduPilot ise AT32’yi (ve APM32’yi) desteklemiyor; ArduPilot isteyenlere aynı kartın STM32F405’li varyantını (ayrı yazılım, MCU dış tedarikle +1.4…+5 $) sunarız. Onaylıyor musunuz?”**
Öneri: evet (KRR-010’un yerine geçer).

## 7. Kaynaklar

| Kaynak | Sürüm / tarih | Dosyalar |
|---|---|---|
| [betaflight/betaflight](https://github.com/betaflight/betaflight/tree/2026.6.2) | 2026.6.2 `e0b7bb01b17b`; 4.4.3 / 4.5.0 / 4.5.2 API | `src/platform/AT32/{target/AT32F435G/target.{h,mk},target/AT32F435M/target.mk,startup/at32f435_437_clock.c,startup/at32f435_437_conf.h,dma_reqmap_mcu.c,dma_at32f43x.c,timer_at32f43x.c,pwm_output_dshot.c,dshot_bitbang.c,serial_uart_at32f43x.c,bus_i2c_atbsp_init.c,adc_at32f43x.c,system_at32f43x.c}`, `src/platform/common/stm32/{bus_spi_hw.c,bus_spi_pinconfig.c,system.c}`, `src/platform/STM32/timer_stm32f4xx.c`, `src/main/target/common_pre.h`, `src/main/fc/init.c`, `src/main/drivers/accgyro/accgyro_spi_lsm6dsv16x.c`; sürüm ekleri |
| [betaflight/config](https://github.com/betaflight/config) | `cacb3a0` (2026-11-09) | `configs/{ORBT/ORBITF435,OPEN/REVO_AT,OPEN/REVO,IFRC/IFLIGHT_BLITZ_F435,AIRB/AIRBOTSUPERF4V2,TEBS/TBS_LUCID_FC,SPBE/SPEEDYBEEF435AIOELRS,NERC/NEUTRONRCF435}/config.h`, `FC_TARGET_MCU` taraması |
| [betaflight-configurator](https://github.com/betaflight/betaflight-configurator) | master `9c8b310a3f40` | `src/js/protocols/{devices.ts,usbdfu.ts}` |
| [iNavFlight/inav](https://github.com/iNavFlight/inav/tree/9.1.0) | 9.1.0 `e519b69`; 6.0.0/6.1.1/8.0.0/9.0.0 API | `src/main/target/*/CMakeLists.txt`, `src/main/drivers/*_at32f43x.c`, `src/main/drivers/accgyro/accgyro_lsm6dxx.c` |
| [ArduPilot/ardupilot](https://github.com/ArduPilot/ardupilot) | master `aea9a1b5d4d8` | `libraries/AP_HAL_ChibiOS/hwdef/scripts/`; GitHub kod/issue araması “AT32F435” (0) |
| AT32F435/437 veri sayfası (Çince) v2.01, 2022-01-13 | LCSC C3029577 PDF | §2.4.3 LDO, §2.5 önyükleme (Tablo 5), Şekil 4 / pin tablosu (LQFP64), Tablo 15–16 (LDO–f–T_A), Tablo 21/23 (akım), θJA |
| STM32F405xx/407xx DS | `lib/datasheet/STM32F405RGT6.pdf` | Tablo 7 (LQFP64), Tablo 20 (akım), VCAP |
| Geehy APM32F405 | `docs/rapor/yazilim-inceleme.md` §11 | LQFP64 VCAP_2 47, BOOT0 60 |
| Fiyat/stok | JLCPCB parça API + LCSC, 2026-11-12 (`tools/jlc.py` kopyası, oturum dizini) | C3029577, C5178940, C5178942, C3029581, C5290473, C15742, C1337199, C99031, C174269 |
| Web araması | Artery STM32F405→AT32F435 geçiş notu: bulunamadı; en yakın [MG0018 (AT32F403A→F435)](https://www.arterytek.com/download/MG/MG0018_Migrating_from_AT32F403A_407_to_AT32F435_437_EN_V2.0.3.pdf), [AT32F435 ürün sayfası](https://arterychip.com/en/product/AT32F435.jsp) | — |
