# Yazılım incelemesi — APM32F405 seri MCU ve kritik parça muadillerinin yazılım uyumu (gomulu-yazilim)

> **Tarih:** 2026-11-12. **Hazırlayan:** `gomulu-yazilim`. Yalnız inceleme; değişen dosyalar `firmware/README.md`, `firmware/fmu/STACKF405/config.h`, `firmware/esc/README.md` ve bu rapor. Commit yok.
> **Girdi:** `docs/pin-haritasi.md` v0.1, `docs/mimari-fmu.md`, `boards/fmu/README.md`, `docs/bom-maliyet.md` §10, `docs/rapor/guc-tasarruf.md`, `docs/gereksinimler/sistem.md` (SYS-030…034, 050, 051, 056, 095, DT-005), `kararlar.md` (KRR-005, 010, 011), `proje.md` (RSK-020), `sorular.md` (SOR-018). ESC port ataması Rev B şematik netlistinden (`kicad-cli sch export netlist`, geçici dizinde).
> **Müşteri isteği:** seri üretimde APM32F405, STM32F405 drop-in muadil; kritik parçaların muadilleri tasarım değişmeden takılabilmeli ve mümkünse aynı yazılım imajında tanınmalı (SYS-095 d, KRR-011 kural 6).
> **Yöntem:** kaynak kodları yalnız okumak için oturum dizinine indirildi (repoya konmadı). Derleyici yok → derleme sonuçları “derleyicide doğrulanacak”. Veri sayfaları LCSC/üretici bağlantılarından (§11).

## 0. Özet (yönetici için)

| # | Konu | Sonuç | Bir cümle |
|---|---|---|---|
| 1a | APM32F405 — Betaflight | **İki imaj** | APM32F405 ayrı platform (`src/platform/APM32`), **2025.12’den beri** (4.5.x’te yok). Bir config tek `FC_TARGET_MCU` taşır → APM32 ve STM32 için iki config/iki .hex; pin, zamanlayıcı, DMA tabloları birebir aynı, config içeriği aynı. USB VCP 314B:5740, ROM DFU 314B:0106 Configurator’da tanımlı |
| 1b | APM32F405 — INAV | **Desteklenmiyor** | INAV 9.1.0’da APM32 kodu yok (yalnız STM32F4/F7/H7, AT32F43x). Gereksinim değil, bilgi |
| 1c | APM32F405 — ArduPilot | **Desteklenmiyor** | master’da APM32 MCU tanımı/hwdef yok; STM32 imajının APM32’de çalıştığına dair kayıt bulunamadı. Klon MCU emsali var (`CKS32F407xx.py`) → port mümkün ama iş ve test ister. RSK-020 (a) gerçekleşti |
| 1d | SOR-018 | **Sorulmalı** | Hem “iki ayrı derleme” hem “ArduPilot desteklemiyor” koşulu sağlandı. Öneri: SOR-018 seçenek 1 |
| 2 | Baro SPA06-003 ↔ DPS368 | **Tek imaj** (BF her sürüm; AP ≥ 4.6 ve iki BARO satırı) | BF `barometer_dps310.c` 0x10 ve 0x11’i tanır. AP: 0x10 → `DPS310`, 0x11 → `SPL06` (SPA06). **Yeni bulgu:** Tokmas “DPS368” (C55090144) veri sayfasında ID **0x11** ve katsayılar 0x10–0x24 → Infineon DPS368 değil, SPA06 eşleniği |
| 3 | IMU ICM-42688-P Tokmas ↔ TDK | **Tokmas desteklenmiyor (kritik)** | Tokmas C54308212 veri sayfası **farklı bir yonga**: kimlik 0x1F = 0xA1 (“K01”), I2C 0x36, jiroskop ODR 7.04/14.08 kHz; WHO_AM_I 0x75 = 0x47 yok → BF ve AP tanımaz. HXY C46550687 de farklı (WHO_AM_I 0x01 = 0x6A). Yalnız TDK orijinali (0x47) çalışır |
| 4 | Flash W25Q128JV ALT | **Tek imaj** (seçilen ALT ile) | BF ≥ 2025.12 **ve** AP Copter-4.7.2’de ortak 128 Mbit: Winbond 0xEF4018/0xEF7018, Micron 0x20BA18, Cypress 0x016018, Zbit 0x5E4018. GD25Q128 / BY25Q128 / PY25Q128 / MX25L128 yalnız BF; XM25QH128 ikisinde de yok |
| 5 | OSD AT7456E ↔ MAX7456 | **Tek imaj** | Aynı sürücü (BF `max7456.c`, AP `AP_OSD_MAX7456`); BF tipi CMAL[6] ile otomatik algılar. MAX7456 yazılımca uygun, tedarik yok (stok 0) |
| 6 | ESC akım ölçeği | `ibata_scale 100`, `ibata_offset 0` | RSA240C ve INA240A3 ikisi ×100 → 10 mV/A; BF birimi mV/10A. İki ESC SJ101 ile ortalanırsa 50. AP `BATT_AMP_PERVLT 100` |
| 7 | ESC Bluejay | **Uyuyor: düzen `C`**; BB21F16I ✓ | Port ataması `C.inc` ile birebir. Ölü zaman derleme sabiti (20.4 ns/adım): ≥ 200 ns → `DEADTIME 10` (204 ns); dosya `C_H_10_24_v0.21.0.hex` |
| 8 | 9 V PINIO | `PINIO1_CONFIG 129` = çıkış + ters → **varsayılan AÇIK** | SpeedyBee’nin `PINIO1_BOX 0` (= ARM) değeri bizde silahlanınca 9 V’u keser → **`PINIO1_BOX 40` (USER1)** |

**Ek bulgular:** (i) RSK-020’deki “yanlış dosya yüklenemez (DFU reddeder)” varsayımı yanlış: Configurator DFU yalnız flash boyutunu denetler (§1.3). (ii) SYS-050 “Betaflight ≥ 4.5” APM32’li kartta **≥ 2025.12** olmalı. (iii) Akım ölçeği SJ101 kapalıyken yarıya iner (§6).

## 1. APM32F405RGT6

### 1.1 Betaflight

| Soru | Bulgu | Kaynak |
|---|---|---|
| Ne zamandan beri? | `src/platform/APM32/target/APM32F405` **2025.12.0-RC1**’de var; 4.4.3, 4.5.0, 4.5.2, 4.5.5’te yok (`src/main/target` listelerinde APM32 yok). Yayımlanan `betaflight_<sürüm>_APM32F405.hex` ilk kez 2026.6.0-rc1 eklerinde (2025.12.x eklerinde hex yok, bulut derleme) | GitHub API `contents?ref=` ve sürüm ekleri |
| Ayrı MCU hedefi mi? | **Evet.** `TARGET_MCU := APM32F405xx`, `TARGET_MCU_FAMILY := APM32F4`, ayrı HAL (Geehy DAL), ayrı USB kütüphanesi (`APM32_USB_Library`), ayrı başlangıç/ld (`apm32_flash_f405.ld`), `TARGET_BOARD_IDENTIFIER "A405"` (STM32: `"F405"`) | `src/platform/APM32/target/APM32F405/target.{mk,h}`, `mk/APM32F4.mk` |
| Unified/config | `mk/config.mk`: `TARGET := FC_TARGET_MCU` (config.h’den). **Bir config tek MCU** → APM32 ve STM32 için iki config klasörü, iki .hex. Emsal: AT32 varyantları ayrı ad taşır (ör. `REVO` / `REVO_AT`). betaflight/config’te bugün APM32F405 kullanan **hiç config yok** (175 STM32F405, 37 AT32) → ilk APM32 kartı biz oluruz | `mk/config.mk` satır 86; `betaflight/config` taraması |
| STM32 imajı APM32’de çalışır mı? | Kodda MCU kimlik denetimi yok (`IDCODE` aranmıyor; MCU adı derleme sabiti). Ama Betaflight ekibi APM32’yi ayrı platform yaptı (farklı USB çekirdeği, flash/RCC sürücüleri). Çalıştığını gösteren kaynak bulunamadı → **desteklenmiyor varsayılır**; DOG-112’de deneme olarak bakılabilir (resmî yol sayılmaz) | kaynak + web araması (sonuçsuz) |
| Clock / HSE 8 MHz | `SYSTEM_HSE_MHZ 8` → `pll_m = hse/2 = 4`, PLL girişi 2 MHz, 168 MHz; STM32 yolu ile aynı mantık | `APM32/startup/system_apm32f4xx.c` `DAL_SysClkConfig()` |
| DMA tablosu (pin-haritasi §1.3) | `APM32/dma_reqmap_mcu.c` F405 satırları STM32 F4 satırlarıyla **birebir aynı** (SPI1 SDO {D2S3, D2S5}, SDI {D2S0, D2S2}; ADC1 {D2S0, D2S4}; TIM1…TIM8 kanal tabloları) → §1.3 aynen geçerli | `diff` STM32 ↔ APM32 `dma_reqmap_mcu.c` |
| Zamanlayıcı seçenekleri | Kullandığımız 12 pin için (`PB6 PB7 PB0 PB1 PC8 PC9 PB10 PA15 PA8 PB14 PB15 PA3`) `timer_apm32f4xx.c` ve `timer_stm32f4xx.c` girişleri ve sıraları aynı → `TIMER_PIN_MAP` sıra numaraları iki MCU’da aynı | betik karşılaştırması |
| USB VCP | Geehy VID 0x314B, PID 0x5740 (`usbd_cdc_descriptor.c`); Configurator listesinde “APM32 VCP” | `APM32/usb/vcp/`, configurator `src/js/protocols/devices.ts` |
| USB DFU / ROM önyükleyici | Configurator DFU filtresi: `{ vendorId: 12619 (0x314B), productId: 262 (0x0106) } // APM32 DFU Bootloader`. Betaflight `systemResetToBootloader(ROM)` APM32’de sistem belleğine atlar | configurator `devices.ts`; BF `APM32/system_apm32f4xx.c` |
| Yükleme | Configurator → “Load firmware” → kart adı `STACKF405` (APM32) seçilir → BOOT düğmesi + USB (ROM DFU) veya CLI `dfu`. Windows’ta APM32 DFU için WinUSB sürücüsü (Zadig/ImpulseRC) gerekebilir | **kartta doğrulanacak (DOG-112)** |

### 1.2 INAV ve ArduPilot

| Yazılım | Bulgu | Kaynak |
|---|---|---|
| INAV 9.1.0 / master | `lib/main`: AT32F43x, STM32F4/F7/H7; `src/main/drivers`: yalnız `*_at32f43x.c` → **APM32 yok**. `SPEEDYBEEF405V4` hedefi var (STM32) | GitHub API |
| ArduPilot master (aea9a1b) | `libraries/AP_HAL_ChibiOS/hwdef/scripts/` MCU tanımları: STM32 ailesi + **`CKS32F407xx.py`** (STM32F407 tablolarını devralan klon); APM32 yok; hwdef’lerde ve kaynakta “APM32/Geehy” geçmiyor. Uygulama tarafında MCU kimlik kapısı yok (önyükleyici `get_mcu_id()` yalnız raporlar) | dosya taraması, `Tools/AP_Bootloader/support.cpp` |
| STM32 imajı APM32’de (AP) | Kayıt/forum sonucu bulunamadı. ChibiOS STM32 OTG/flash sürücüsü APM32’de denenmemiş → **desteklenmiyor**. Port yolu: `APM32F405xx.py` (CKS32 emsali) + USB/flash denemesi; kabul ArduPilot ekibine bağlı | web araması (sonuçsuz) |

### 1.3 Yanlış imaj riski

Configurator DFU akışı (`usbdfu.ts` `selectFlashLayout`) yalnız hex boyutunu ve flash düzenini denetler; MCU türünü denetlemez. Firmware sekmesindeki MCU yalnız gösterim (`state.targetMCUText`). → STM32 imajı APM32’ye (veya tersi) **yüklenebilir**; sonuç belirsiz, kart ROM DFU (BOOT düğmesi) ile kurtarılır. RSK-020’deki “DFU reddeder” ifadesi düzeltilmeli (`gereksinim-muhendisi`).

### 1.4 Sonuç ve öneri

- **Betaflight: iki imaj, tek config içeriği.** `firmware/fmu/STACKF405/config.h` (`FC_TARGET_MCU APM32F405`); STM32 ALT dizilirse aynı dosya `STACKF405_STM` adıyla, yalnız MCU satırı farklı. Kart üstünde MCU türü ipek baskı/etikette, Configurator’da kart adı ve “A405/F405” tanıtıcısında görünür.
- **ArduPilot: APM32’de yok.** SYS-056 APM32’li kartta karşılanmaz → SOR-018 seçenek 1 (ArduPilot SKU’sunda STM32F405RGT6) veya 3.
- **SOR-018 sorulmalı** (koşul gerçekleşti). Önerilen cevap: seçenek 1.
- SYS-050 notu: APM32’li kartta Betaflight **≥ 2025.12** (öneri: 2026.6.2).

## 2. Baro — SPA06-003 (Goertek) ↔ DPS368

### 2.1 Kimlikler (veri sayfaları)

| Parça | LCSC | ID (0x0D) | Katsayı | Sonuç |
|---|---|---|---|---|
| Infineon DPS368XTSA1 | C3232508 | 0x10 | 0x10–0x21 (18 B) | DPS310 eşdeğeri |
| **Goertek SPA06-003** | C30589048 | **0x11** | 0x10–0x24 (c31, c40 ek) | SPL07/SPA06 ailesi |
| **Tokmas “DPS368XTSA1”** | C55090144 | **0x11** (DS reg tablosu, “ID 11h”) | 0x10–0x24, Pcomp’ta c40·P⁴ ve c31 | **Infineon DPS368 değil**, SPA06-003 eşleniği |

### 2.2 Betaflight

`src/main/drivers/barometer/barometer_dps310.c` (2026.6.2): `DPS310_ID_REV_AND_PROD_ID 0x10`, `SPL07_003_CHIP_ID 0x11`; `deviceDetect` ikisini de kabul eder, 0x11’de 22 katsayı okur ve c31/c40’lı formülü kullanır. 4.5.0, 4.5.2, 4.5.5, 2025.12.1’de de aynı kod var. 2026.6’dan itibaren `USE_BARO_SPA06_003` ile 0x11 “SPA06_003” diye raporlanır (`sensors/barometer.c`); eski sürümde “DPS310” görünür, ölçüm aynı. Adres varsayılanı 0x76. → **Üç parça da tek imajda ✓.**

### 2.3 ArduPilot

| Sürücü | Kabul ettiği ID | Not |
|---|---|---|
| `AP_Baro_DPS280.cpp` (`AP_Baro_DPS310::probe`) | yalnız 0x10 | Infineon DPS310/DPS368 |
| `AP_Baro_SPL06.cpp` | 0x10 → SPL06, 0x11 → SPA06 | **SPA06 desteği Copter-4.6.0’dan beri** (4.5.7’de yok) |

Aynı adreste ikinci kez kayıt `_i2c_sensor_is_registered()` ile engellenir; hwdef sırası = prob sırası (`hwdef.py write_BARO_config`). SPL06 sürücüsü 0x10’u da “SPL06” sanacağı için **DPS310 satırı önce**:

```
define AP_BARO_BACKEND_DEFAULT_ENABLED 0
define AP_BARO_DPS280_ENABLED 1
define AP_BARO_SPL06_ENABLED 1
BARO DPS310 I2C:0:0x76
BARO SPL06 I2C:0:0x76
```

Emsal: `MatekH743/hwdef.dat` aynı 0x76 adresinde `BARO DPS310` + `BARO BMP280`. → **Tek imaj ✓** (Copter ≥ 4.6). **Derleyicide doğrulanacak.**

### 2.4 Parça seçimi sonucu

SPA06-003 (ana) ve Tokmas DPS368 (ALT) yazılım açısından aynı sınıf (0x11). Infineon DPS368 de (0x10) tanınır. Üçü aynı LGA-8 2.0 × 2.5 dizilimi (`bom-maliyet` §10.2 B1) — ayak izi `pcb-muhendisi`.

## 3. IMU — ICM-42688-P

| Parça | LCSC | Kimlik | BF | AP | Sonuç |
|---|---|---|---|---|---|
| TDK ICM-42688-P | C1850418 (21.6 $, stok 33) | WHO_AM_I (0x75) = **0x47** | ✓ `ICM42688P_WHO_AM_I_CONST 0x47` (`accgyro_spi_icm426xx.c`) | ✓ `INV3_ID_ICM42688_P 0x47` (`AP_InertialSensor_Invensensev3.cpp`) | çalışır |
| **Tokmas “ICM-42688-P(TOKMAS)”** | C54308212 (2.94 $, stok 7 006) | DS: CHIP ID reg **0x1F = 0xA1 (“K01”)**; ivme verisi 0x00–0x05; I2C 0x36/0x37; jiro ODR 110…14 080 Hz (8 kHz yok) | ✗ (0x75’te 0x47 yok, sürücü yok) | ✗ | **farklı yonga; SYS-031/050/056 karşılanmaz** |
| HXY ICM-42688P | C46550687 | DS: WHO_AM_I **0x01 = 0x6A** | ✗ | ✗ | farklı yonga |
| Tokmas ICM-42688-PC | C48586483 (stok 0) | DS incelenmedi | ? | ? | — |

Pin dizilimi Tokmas’ta TDK’ya benzer (1 SDO, 4 INT1, 5 VDDIO, 8 VDD, 12 CS, 13 SCK, 14 SDA) ama yazılım uyumu yok. **Uyarı:** sonuç LCSC’de yayımlanan Tokmas veri sayfasına dayanır; prototipten önce bir numunede SPI ile 0x75 okunarak doğrulanmalı (0x47 dönerse veri sayfası yanlış eklenmiştir).

Aynı ayak izinde (LGA-14 2.5 × 3, TDK dizilimi) BF + AP tanıyan, stoklu seçenekler — hepsi TDK (farklı üretici yok → KRR-011 kural 3 gerekçesi):

| Parça | LCSC, fiyat, stok (JLC 2026-11-12) | BF | AP | 8 kHz | Not |
|---|---|---|---|---|---|
| ICM-42688-P (TDK) | C1850418, 21.6 $, 33 | ✓ | ✓ | ✓ | ana aday |
| ICM-42605 | C2655099, 12.3 $, 1 130 | ✓ | ✓ (0x42) | ✓ | ALT adayı |
| IIM-42652 | C2988404, 11.1 $, 8 | ✓ | ✓ (0x6F) | ✓ | stok az |
| ICM-42686-P | C19191783, 9.5 $, 3 | ✓ | ✗ | ✓ | AP’de yok |
| ICM-45686 | C22459454, 10.2 $, 2 584 | ✓ | ✓ (0xE9) | ✓ | **pin dizilimi 42688 ile aynı mı → `sematik-muhendisi` DS’den** |
| LSM6DSV16X (ST) | C5267406, 3.35 $, 9 300 | ✓ | ✓ (`LSM6DSV`) | 7.68 kHz | farklı pin dizilimi → drop-in değil, ancak ana parça olarak düşünülebilir (SYS-031 “veya eşdeğer”) |

Config’te ALT’lar için sürücüler açık (`USE_GYRO_SPI_ICM42605`, `USE_ACCGYRO_IIM42652`, `USE_ACCGYRO_ICM42686P`) → aynı imaj ✓. Maliyet etkisi büyük (Tokmas 2.94 $ → TDK ≥ 10 $); karar `bom-tedarik` + `sistem-mimari` + müşteri.

## 4. Flash — W25Q128JV ve 128 Mbit ALT’lar

Betaflight `src/main/drivers/flash/flash_m25p16.c` (2026.6.2; 4.5.5 ve 2025.12.x’te `drivers/flash_m25p16.c` / aynı tablo) ve ArduPilot `libraries/AP_Logger/AP_Logger_Flash_JEDEC.cpp` (Copter-4.6.3, 4.7.2, master; 4.5.7’de `AP_Logger_DataFlash.cpp`).

| JEDEC | Parça | BF 4.5.5 | BF 2025.12.5 | BF 2026.6.2 | AP 4.6.3 | AP 4.7.2 | AP master | Her ikisinde (kararlı) |
|---|---|---|---|---|---|---|---|---|
| 0xEF4018 | Winbond W25Q128JV-IQ (ana) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 0xEF7018 | Winbond W25Q128JV-IM | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 0x20BA18 | Micron N25Q128 / MT25QL128 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 0x016018 | Cypress/Infineon S25FL128L | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 0x5E4018 | Zbit ZB25VQ128 | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ | **✓ (AP ≥ 4.7)** |
| 0xA14018 | FMSH FM25Q128A | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | yalnız BF 2026.6 + AP master |
| 0x0B4018 | XTX XT25F128F | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | yalnız BF 2026.6 + AP master |
| 0x1C7118 | Giantec GT25Q128EZ | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | yalnız BF 2026.6 + AP master |
| 0xC84018 | GigaDevice GD25Q128E/C | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | yalnız BF |
| 0x684018 | Boya BY25Q128ES | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | yalnız BF |
| 0x852018 | PUYA PY25Q128HA | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ | yalnız BF |
| 0xC22018 | Macronix MX25L12845G | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | yalnız BF |
| — | XMC XM25QH128 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | hiçbiri |

Tedarik (JLC 2026-11-12, SOIC-8 208 mil = W25Q128JVSIQ kılıfı):

| ALT | LCSC, fiyat, stok | Yazılım | Değerlendirme |
|---|---|---|---|
| **W25Q128JVSIM** (Winbond) | C401671, 3.33 $, 1 022 | BF + AP ✓ (0xEF7018) | Aynı üretici, farklı sipariş kodu (KRR-011 kural 3 gerekçesiyle) — **öneri** |
| MT25QL128ABA1ESE-0SIT (Micron) | C41359590, 12.94 $, 2 050 | BF + AP ✓ (0x20BA18) | Farklı üretici, pahalı — ikinci seçenek |
| ZB25VQ128ASIG (Zbit) | C609616 / C3098138, stok 0 | BF + AP 4.7 ✓ | tedarik yok |
| FM25Q128AI3 (Fudan) | C2928936 / C908405, stok 0 | AP kararlı ✗ | — |
| XT25F128FSSIGU-W (XTX) | C5187911, 1.47 $, 55 | AP kararlı ✗ | AP sonraki kararlı sürümü bekler |
| S25FL128L (Infineon) | SOIC-8 kodları 1 adet stok | ✓ | tedarik yok |

BF config: `USE_FLASH_M25P16` (JEDEC tablosu). `pin-haritasi` §1.4’teki `USE_FLASH_W25Q128FV` SPI’da `USE_FLASH_M25P16`’yı açar (`common_post.h` 487) → doğru çalışır; config’te ikisi de var.

## 5. OSD — AT7456E ↔ MAX7456

- BF `src/main/drivers/max7456.c`: tek sürücü; algılama OSDM yazıp okuyarak, tip ayrımı CMAL[6] (CA[8]) yazma/okuma ile (`MAX7456_DEVICE_TYPE_AT` / `_MAX`). SPI: algılama 5 MHz, çalışma 10 MHz (`max7456_clock` NOMINAL; F405 overclock’ta HALF/DOUBLE seçenekleri). Fark yalnız “AB7456’da NTSC bazen algılanmıyor” yorumu ve saat seçenekleri.
- AP `AP_OSD_MAX7456.cpp`: aynı yazmaç seti, tip ayrımı yok, hwdef `SPIDEV osd SPI2 … 10*MHZ`.
- Sonuç: **tek imaj ✓**. MAX7456 (Analog/Maxim) yazılımca drop-in, ancak JLC/LCSC stoğu 0 (`bom-maliyet` §10.3) → tedarik açısından ALT yok (istisna, RSK-021).

## 6. ESC akım ölçeği

BF `src/main/sensors/current.c`: `centiAmps = (mV × 10000 / scale + offset) / 10`, yorum “m is scale in (mV/10A) and b is offset in (mA)”.

| Yükselteç | Kazanç | Shunt | Çıkış | `ibata_scale` | `ibata_offset` |
|---|---|---|---|---|---|
| RSA240CXK (ana, guc-tasarruf §2.4) | ×100 | 0.1 mΩ | 10 mV/A = 100 mV/10A | **100** | **0** (REF1 = REF2 = GND, tek yönlü) |
| INA240A3DR (ALT) | ×100 | 0.1 mΩ | 10 mV/A | **100** | 0 |
| (INA281B2, reddedildi) | ×50 | 0.1 mΩ | 5 mV/A | 50 | 0 |

- **Aynı ölçek → ALT yazılım ayarı değiştirmez ✓** (KRR-011 kural 6).
- 8 motor (J_ESC2 dolu) ve **SJ101 kapalı**: PC1 iki CUR’un eşit ağırlıklı ortalamasını görür → toplam akım için `ibata_scale 50`. SJ101 açıkken PC1 yalnız ESC1. (Kullanıcı kılavuzu notu.)
- Ofset doğruluğu (RSA240 sıcaklıkta ±200 µV) donanım konusu, DOG-019; yazılımda `ibata_offset` ile ortalama ofset düzeltilebilir ama kart başı kalibrasyon SYS-021’de yok.
- ArduPilot: `BATT_AMP_PERVLT 100`, `BATT_AMP_OFFSET 0` (hwdef `HAL_BATT_CURR_SCALE 100`).

## 7. ESC — Bluejay

Ayrıntılı tablo: [`firmware/esc/README.md`](../../firmware/esc/README.md).

- **Düzen:** esc55a Rev B port ataması (P0.0 RX, P0.2 Vn, P0.3/4/5 A/B/C mux, P0.6 Ap, P0.7 Ac, P1.0 Bp, P1.1 Bc, P1.2 Cp, P1.3 Cc) = Bluejay `src/Layouts/C.inc` (“RX __ Vn Am Bm Cm Ap Ac | Bp Bc Cp Cc”, PWM/COM ters değil). **SYS-051 ✓** (kaynak koduna göre), RSK-009 kapanabilir (kartta DOG-051/052).
- **EFM8BB21F16I:** Bluejay `MCU=H` (BB21). Önyükleyici imzası derleme sabiti E8 B2; F16I ve F16G aynı → aynı hex ✓.
- **Ölü zaman:** derleme sabiti, hex adının 3. alanı, 20.4 ns/adım (`Bluejay.asm` satır 130). ≥ 200 ns ek → **10 (204 ns)**. PWM 24 kHz (guc-ip03 §2.4). Dosya **`C_H_10_24_v0.21.0.hex`** (v0.21.0 sürüm eklerinde var).
- **Düzeltme:** `docs/inceleme.md` §2.4 “pin 1 sinyal, 7/11/13–16 köprü” → sinyal **pin 2 (P0.0)**, köprü **10, 11, 13–16**.
- Sıcaklık koruması Bluejay’de varsayılan kapalı (`DEFAULT_PGM_ENABLE_TEMP_PROT 0`) → eşik kararı açık konu.

## 8. 9 V PINIO (PB11 → SY8303 EN)

BF `src/main/drivers/pinio.h`: `PINIO_CONFIG_MODE_OUT_PP 0x01`, `PINIO_CONFIG_OUT_INVERTED 0x80`.

| Değer | Anlam | Açılışta PB11 | Kutu aktif |
|---|---|---|---|
| **129 = 0x81** | push-pull çıkış + ters | **HIGH** (`pinioInit`: ters ise `IOHi`, state = true) | `pinioSet(on)` → fiziksel `on XOR ters` → LOW |
| 1 | push-pull, düz | LOW | HIGH |

Donanım: PB11 → 1 k → EN, 100 k → 3V3; EN yüksek = açık. → **129: 9 V açılışta açık ✓**; MCU sıfırlanırken/DFU’da pin giriş, 100 k çekme ile yine açık ✓.

`PINIO1_BOX`: SpeedyBee V4 `0` kullanıyor; `0` = `BOXARM` kalıcı kimliği ve `getBoxIdState(BOXARM) = ARMING_FLAG(ARMED)` (`msp_box.c` 399). ARM için mod tanımlıysa (her zaman) görev çalışır → **silahlanınca PB11 LOW → 9 V kapanır** (bizim donanımda DJI/VTX uçuşta söner). → **`PINIO1_BOX 40` (USER1)**: USER1 tanımlı değilse 9 V hep açık; USER1 aktifken kapalı. betaflight/config’te 129 ile en yaygın ikili (≈ 250 kart 40, ≈ 50 kart 0).

ArduPilot `speedybeef4v4` hwdef’inde PB11 tanımsız (giriş) → bizim kartta 100 k ile açık kalır. Kendi hwdef’imizde öneri: `PB11 PINIO1 OUTPUT GPIO(81) HIGH` + `define RELAY2_PIN_DEFAULT 81` (derleyicide doğrulanacak).

## 9. DMA notu (Betaflight, kaynak kodundan)

`USE_SPI_DMA_ENABLE_EARLY` (F405 ve APM32F405 target.h) → `spiInitBusDMA()` motor (`motorDevInit`, init.c 562), ADC (710) ve LED (816) ayırmalarından sonra, `motorPostInit`’ten önce (1048) çalışır; SPI DMA seçeneği verilmezse ilk boş akışı alır. Beklenen: SPI1 TX DMA2 S3, RX DMA2 S0 ✓ (pin-haritasi §1.3). SPI2 TX DMA1 S4’ü ayırabilir ama RX yok → `useDMA = false` (yoklamalı); DMA1 S4 UART4 TX DMA’ya kapanabilir. Kartta `dma show` ile bakılacak (DOG-034/035).

## 10. Parça seçimi kısıtları (sematik-muhendisi / bom-tedarik)

| Parça | Yazılımca uygun ALT | Uygun değil | Not |
|---|---|---|---|
| MCU | STM32F405RGT6 (ayrı BF derlemesi; AP yalnız STM32) | — | MCU satırına “BF: iki derleme; AP: yalnız STM32” notu |
| IMU | TDK ICM-42688-P, ICM-42605, IIM-42652, (ICM-45686: pin dizilimi teyidi) | **Tokmas C54308212, HXY C46550687** | Mevcut ana parça (Tokmas) değişmeli — kritik |
| Baro | Goertek SPA06-003, Tokmas DPS368 C55090144, Infineon DPS368 C3232508 | BMP280/BMP581 (farklı ayak izi), SPL06-001 tek başına AP’de DPS310 ile karışır (0x10) | AP hwdef iki satır, Copter ≥ 4.6 |
| Flash | W25Q128JVSIM (C401671), MT25QL128ABA1ESE (C41359590); ileride ZB25VQ128 | GD25Q128, BY25Q128, PY25Q128, MX25L128, XM25QH128 (AP’de yok); FM25Q128, XT25F128F, GT25Q128 (AP kararlıda yok) | SOIC-8 208 mil |
| OSD | MAX7456 (yazılımca ✓) | — | tedarik yok → istisna |
| ESC akım yükselteci | INA240A3 ↔ RSA240C (aynı ×100) | farklı kazançlı her parça | ölçek aynı kalmalı |
| ESC MCU | — (EFM8BB21F16I tek) | EFM8BB51 (pin farklı), diğer 8051’ler | istisna |

## 11. Kaynaklar

Kaynak kodu (oturum dizinine indirildi, repoya konmadı):

| Depo | Sürüm / commit | Okunan dosyalar |
|---|---|---|
| [betaflight/betaflight](https://github.com/betaflight/betaflight) | **2026.6.2** (`e0b7bb01b17b`, 2026-09-17); ayrıca 4.5.0/4.5.2/4.5.5/2025.12.x API/raw | `src/platform/APM32/{target/APM32F405/target.{h,mk},mk/APM32F4.mk,dma_reqmap_mcu.c,timer_apm32f4xx.c,system_apm32f4xx.c,startup/system_apm32f4xx.c,usb/vcp/usbd_cdc_descriptor.c}`, `src/platform/STM32/{dma_reqmap_mcu.c,timer_stm32f4xx.c,target/STM32F405/target.h}`, `mk/config.mk`, `Makefile`, `src/main/drivers/barometer/barometer_dps310.c`, `src/main/sensors/{barometer.c,current.c}`, `src/main/drivers/accgyro/{accgyro_mpu.h,accgyro_spi_icm426xx.c}`, `src/main/drivers/flash/{flash_m25p16.c,flash.c}`, `src/main/drivers/max7456.c`, `src/main/drivers/pinio.{c,h}`, `src/main/io/piniobox.c`, `src/main/pg/{piniobox.c,max7456.c}`, `src/main/msp/msp_box.c`, `src/main/target/{common_pre.h,common_post.h}`, `src/main/fc/init.c`, `src/platform/common/stm32/bus_spi_hw.c` |
| [betaflight/config](https://github.com/betaflight/config) | master `cacb3a06d7d9` (2026-11-09) | `configs/SPBE/SPEEDYBEEF405V4/config.h`, `configs/DIAT/MAMBAF405US/config.h`, tüm `FC_TARGET_MCU` / `PINIO1_BOX` taraması, `Manufacturers.md` |
| [betaflight/betaflight-configurator](https://github.com/betaflight/betaflight-configurator) | master `9c8b310a3f40` (2026-11-09) | `src/js/protocols/{devices.ts,usbdfu.ts}`, `src/components/tabs/FirmwareFlasherTab.vue` |
| [ArduPilot/ardupilot](https://github.com/ArduPilot/ardupilot) | master `aea9a1b5d4d8` (2026-11-11); Copter-4.5.7 / 4.6.0 / 4.6.3 / 4.7.2 raw | `libraries/AP_HAL_ChibiOS/hwdef/{scripts/,speedybeef4v4,MambaF405v2,MicoAir405v2,MatekH743}`, `libraries/AP_HAL/hwdef/scripts/hwdef.py`, `libraries/AP_Baro/{AP_Baro.cpp,AP_Baro_SPL06.cpp,AP_Baro_DPS280.cpp}`, `libraries/AP_InertialSensor/AP_InertialSensor_Invensensev3.cpp`, `libraries/AP_Logger/AP_Logger_Flash_JEDEC.cpp`, `libraries/AP_OSD/AP_OSD_MAX7456.cpp`, `Tools/AP_Bootloader/support.cpp` |
| [iNavFlight/inav](https://github.com/iNavFlight/inav) | 9.1.0 ve master (API) | `lib/main`, `src/main/drivers`, `src/main/target` listeleri |
| [bird-sanctuary/bluejay](https://github.com/bird-sanctuary/bluejay) | **v0.21.0** (`93bf3e1a081e`, 2024-07-19) | `src/Layouts/{A…Z,Base}.inc`, `src/Bluejay.asm`, `src/Modules/{Common,Settings}.asm`, `Makefile`, sürüm ekleri |

Veri sayfaları (LCSC, oturum dizinine): Tokmas ICM-42688-P C54308212 (`datasheet.lcsc.com/…/7a03aa93fd81d2bed1a22512fe4360f9.pdf`), Goertek SPA06-003 C30589048 (`…/f11af3d36680da63e45f00c5b1db2c97.pdf`), Tokmas DPS368 C55090144 (`…/83b240d40893b7d17f66987926ee5aa9.pdf`), HXY ICM-42688P C46550687 (`…/3ba6b2a6034ab09d5caaba833c27f1ae.pdf`), TDK ICM-42688-P C1850418 (`…/d5f9e170444ac167b391a8574fc574ca.pdf`); Geehy APM32F405xG/407xExG DS V1.1 (`elsin.ru/pdf/APM32F405XG_407XEXG.pdf`, metin kısmen bozuk; LQFP64 VCAP_2 47, BOOT0 60 STM32 ile aynı). Fiyat/stok: JLC parça arayüzü (`tools/jlc.py` kopyası, oturum dizininde), 2026-11-12.

## 12. Doğrulama planı (kartta / derleyicide)

| # | Kontrol | DOG |
|---|---|---|
| 1 | `make CONFIG=STACKF405` (APM32) ve `STACKF405_STM` derlemesi; uyarısız | DOG-049/050 |
| 2 | APM32 kartta ROM DFU (314B:0106) ile Configurator yüklemesi, VCP bağlantısı, `status` 168 MHz | DOG-112 |
| 3 | `timer show`, `dma show`, `resource show` → pin-haritasi §1.1/§1.3 ile aynı | DOG-034/035 |
| 4 | 8 motor DShot600 + çift yönlü, LED şerit, OSD, blackbox aynı anda | DOG-034 |
| 5 | Baro: SPA06-003, Tokmas DPS368 ve (varsa) Infineon DPS368 numuneleriyle BF ve AP’de tanınma + irtifa | DOG-026, DOG-111 |
| 6 | IMU numunesinde SPI 0x75 okuması (Tokmas sonucu teyidi) | DOG-024 |
| 7 | Flash ALT (W25Q128JVSIM) ile `flash_info`, AP `LOG_BACKEND_TYPE` | DOG-027, DOG-111 |
| 8 | PINIO: açılışta 9 V var, USER1 ile kapanıyor, silahlanınca değişmiyor | — |
| 9 | (Deneme) STM32F405 imajı APM32’de: açılış, USB, DShot | DOG-112 (bilgi) |
