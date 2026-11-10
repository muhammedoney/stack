# Pin haritası — tek kaynak

Sahibi `sistem-mimari`. Şematik (`sematik-muhendisi`) ve yazılım (`gomulu-yazilim`, `firmware/`) bu belgeye uyar; sapma `dogrulama-kalite` bulgusudur. Gerekçe ve mimari: `docs/mimari-fmu.md`.

| Sürüm | Tarih | Değişiklik |
|---|---|---|
| 0.1 | 2026-11-10 | İlk sürüm: FMU STM32F405 önerilen pin/zamanlayıcı/DMA ataması (SPEEDYBEEF405V4 tabanlı), esc55a J0 mevcut dizilimi, FMU↔ESC 8 pin doğrulanmamış |

Durum işaretleri: **Ö** = öneri (şematik öncesi, kilitlenmeye aday), **D** = doğrulanmış, **?** = doğrulanacak.

## 1. FMU — STM32F405RGT6 (LQFP64), HSE 8 MHz — Ö

Taban: Betaflight `SPEEDYBEEF405V4` (`configs/SPBE/SPEEDYBEEF405V4/config.h`) ve ArduPilot `speedybeef4v4/hwdef.dat`. Farklar §1.4’te. Pin numaraları `lib/datasheet/STM32F405RGT6.pdf` Tablo 7 (LQFP64). Zamanlayıcı seçenekleri Betaflight `timer_stm32f4xx.c`, DMA akışları RM0090 §10.3.3 DMA1/DMA2 istek eşleme tabloları (Betaflight `dma_reqmap_mcu.c` aynı tabloyu kodlar).

### 1.1 Sinyal pinleri

| LQFP64 | Pin | İşlev | Betaflight kaynağı | Zamanlayıcı / AF | DMA (akış, kanal) | SpeedyBee V4 ile | Not |
|---|---|---|---|---|---|---|---|
| 2 | PC13 | LED0 (durum) | `LED0_PIN` | — | — | aynı | PC13–15 en çok 3 mA batırır; LED ≤ 2 mA |
| 3 | PC14 | **Flash CS** (W25Q128) | `FLASH_CS_PIN` | — | — | farklı (SD CS) | 2 MHz hız sınıfı; CS için yeterli |
| 4 | PC15 | Buzzer (AO3400A kapısı) | `BEEPER_PIN`, `BEEPER_INVERTED` | — | — | aynı | |
| 5/6 | PH0/PH1 | HSE 8 MHz kristal | `SYSTEM_HSE_MHZ 8` | — | — | aynı | Altium 24 MHz → 8 MHz |
| 8 | PC0 | VBAT ölçümü | `ADC_VBAT_PIN` | ADC123_IN10 | ADC1 → DMA2 S4 ch0 | aynı pin | Bölücü 140 k / 10 k (15:1) |
| 9 | PC1 | Akım 1 (J_ESC1.CUR) | `ADC_CURR_PIN` | ADC123_IN11 | (ADC1) | aynı | |
| 10 | PC2 | SPI2 MISO (OSD) | `SPI2_SDI_PIN` | AF5 | — (DMA’sız) | aynı | |
| 11 | PC3 | SPI2 MOSI (OSD) | `SPI2_SDO_PIN` | AF5 | — | aynı | |
| 14 | PA0 | UART4 TX (analog VTX SmartAudio/Tramp) | `UART4_TX_PIN` | AF8 | (DMA1 S4 ch4 boş) | aynı | |
| 15 | PA1 | UART4 RX | `UART4_RX_PIN` | AF8 | — | aynı | |
| 16 | PA2 | UART2 TX (alıcı) | `UART2_TX_PIN` | AF7 | (DMA1 S6 ch4 boş) | aynı | |
| 17 | PA3 | UART2 RX (alıcı CRSF; SBUS ters çeviriciden) / PPM | `UART2_RX_PIN`, `RX_PPM_PIN` | AF7; PPM: TIM9_CH2 (seç. 3) | — | aynı | SBUS: ayrı ped → ters çevirici → 1 k → PA3 |
| 20 | PA4 | IMU CS | `GYRO_1_CS_PIN` | — | — | aynı | |
| 21 | PA5 | SPI1 SCK (IMU) | `SPI1_SCK_PIN` | AF5 | — | aynı | |
| 22 | PA6 | SPI1 MISO | `SPI1_SDI_PIN` | AF5 | **DMA2 S0 ch3** | aynı pin, DMA farklı | |
| 23 | PA7 | SPI1 MOSI | `SPI1_SDO_PIN` | AF5 | **DMA2 S3 ch3** | aynı | |
| 24 | PC4 | IMU INT1 | `GYRO_1_EXTI_PIN` | EXTI4 | — | aynı | |
| 25 | PC5 | **Akım 2 (J_ESC2.CUR)** / RSSI | `ADC_RSSI_PIN` (BF), AP `BATT2_CURR_PIN 15` | ADC12_IN15 | (ADC1) | aynı pin, işlev farklı | Lehim köprüsü SJ1 (açık): CUR2 → 10 k → PC1 ortalaması |
| 26 | PB0 | **M3** | `MOTOR3_PIN` | TIM3_CH3 (seç. 2), AF2 | **DMA1 S7 ch5** | aynı | |
| 27 | PB1 | **M4** | `MOTOR4_PIN` | TIM3_CH4 (seç. 2), AF2 | **DMA1 S2 ch5** | aynı | |
| 28 | PB2 | BOOT1 | — | — | — | — | 10 k → GND |
| 29 | PB10 | **M7** | `MOTOR7_PIN` | TIM2_CH3 (seç. 1), AF1 | **DMA1 S1 ch3** | aynı | |
| 30 | PB11 | PINIO1: 9 V BEC EN | `PINIO1_PIN`, `PINIO1_CONFIG 129` | GPIO | — | aynı | SY8303 EN (U3), varsayılan açık |
| 33 | PB12 | OSD CS | `MAX7456_SPI_CS_PIN` | — | — | aynı | |
| 34 | PB13 | SPI2 SCK | `SPI2_SCK_PIN` | AF5 | — | aynı | |
| 35 | PB14 | Kamera kontrol (CC) | `CAMERA_CONTROL_PIN` | TIM12_CH1 (seç. 3), DMA yok | — | aynı | |
| 36 | PB15 | Servo 1 / S9 pedi | `SERVO1_PIN` | TIM12_CH2 (seç. 3), DMA yok | — | aynı | |
| 37 | PC6 | UART6 TX (GPS) | `UART6_TX_PIN` | AF8 | — | aynı | |
| 38 | PC7 | UART6 RX (GPS) | `UART6_RX_PIN` | AF8 | (DMA2 S1 ch5 boş) | aynı | |
| 39 | PC8 | **M5** | `MOTOR5_PIN` | TIM8_CH3 (seç. 2), AF3 | **DMA2 S2 ch0** (dmaopt 0) | aynı | |
| 40 | PC9 | **M6** | `MOTOR6_PIN` | TIM8_CH4 (seç. 2), AF3 | **DMA2 S7 ch7** | aynı | |
| 41 | PA8 | LED şerit | `LED_STRIP_PIN` | TIM1_CH1 (seç. 1), AF1 | **DMA2 S6 ch0** (dmaopt 0) | aynı | |
| 42 | PA9 | UART1 TX (DJI / MSP) | `UART1_TX_PIN` | AF7 | — | aynı | VBUS algılama kullanılmaz |
| 43 | PA10 | UART1 RX | `UART1_RX_PIN` | AF7 | (DMA2 S5 ch4 boş) | aynı | |
| 44 | PA11 | USB D− | — | OTG_FS AF10 | — | aynı | |
| 45 | PA12 | USB D+ | — | OTG_FS AF10 | — | aynı | |
| 46 | PA13 | SWDIO | — | — | — | — | SWD pedi (SYS-055) |
| 49 | PA14 | SWCLK | — | — | — | — | SWD pedi |
| 50 | PA15 | **M8** | `MOTOR8_PIN` | TIM2_CH1 (seç. 1), AF1 | **DMA1 S5 ch3** | aynı | |
| 51 | PC10 | UART3 TX (yedek) | `UART3_TX_PIN` | AF7 | — | aynı | |
| 52 | PC11 | UART3 RX | `UART3_RX_PIN` | AF7 | — | aynı | |
| 53 | PC12 | **UART5 TX** (yedek) | `UART5_TX_PIN` | AF8 | — | **farklı (V4’te yok)** | 6. tam UART |
| 54 | PD2 | UART5 RX (ESC telemetri / yedek) | `UART5_RX_PIN` | AF8 | — | aynı | J_ESC1 TLM pini (varsa) |
| 55 | PB3 | SPI3 SCK (flash) | `SPI3_SCK_PIN` | AF6 | — (DMA’sız) | aynı | |
| 56 | PB4 | SPI3 MISO | `SPI3_SDI_PIN` | AF6 | — | aynı | |
| 57 | PB5 | SPI3 MOSI | `SPI3_SDO_PIN` | AF6 | — | aynı | |
| 58 | PB6 | **M1** | `MOTOR1_PIN` | TIM4_CH1, AF2 | **DMA1 S0 ch2** | aynı | |
| 59 | PB7 | **M2** | `MOTOR2_PIN` | TIM4_CH2, AF2 | **DMA1 S3 ch2** | aynı | |
| 60 | BOOT0 | BOOT düğmesi | — | — | — | — | 10 k → GND, düğme → 3V3 |
| 61 | PB8 | I2C1 SCL (baro + dış) | `I2C1_SCL_PIN` | AF4 | — | aynı | 2.2 k → 3V3 |
| 62 | PB9 | I2C1 SDA | `I2C1_SDA_PIN` | AF4 | — | aynı | 2.2 k → 3V3 |

Güç pinleri: 1 VBAT (→ 3V3), 7 NRST (100 nF), 12 VSSA, 13 VDDA (ferrit + 1 µF + 100 nF), 18/63 VSS, 19/32/48/64 VDD (her biri 100 nF + toplam 4.7 µF), 31 VCAP_1 ve 47 VCAP_2 (her biri 2.2 µF düşük ESR, veri sayfası).

**Boş GPIO yok** (LQFP64’ün 51 G/Ç’sinin tamamı kullanılıyor). İkinci durum LED’i gerekirse PB15 (servo) veya PC5 (RSSI/CUR2) feda edilir.

### 1.2 Zamanlayıcı grupları

| Zamanlayıcı | Kanallar | DShot hızı | Not |
|---|---|---|---|
| TIM4 | M1, M2 | ortak | J_ESC1 |
| TIM3 | M3, M4 | ortak | J_ESC1 |
| TIM8 | M5, M6 | ortak | J_ESC2 |
| TIM2 | M7, M8 | ortak | J_ESC2 |
| TIM1 | LED şerit | — | |
| TIM9 | PPM (PA3) | — | DMA yok |
| TIM12 | CC (PB14), servo (PB15) | — | DMA yok |
| TIM5 | boş | — | ArduPilot sistem zamanlayıcısı (`STM32_ST_USE_TIMER 5`) |

### 1.3 DMA akış haritası (Betaflight, çakışma denetimi)

| Akış | DMA1 | DMA2 |
|---|---|---|
| S0 | M1 TIM4_CH1 (ch2) | **SPI1 RX** (ch3) |
| S1 | M7 TIM2_CH3 (ch3) | boş (UART6 RX ch5 seçilebilir) |
| S2 | M4 TIM3_CH4 (ch5) | M5 TIM8_CH3 (ch0) |
| S3 | M2 TIM4_CH2 (ch2) | **SPI1 TX** (ch3) |
| S4 | boş (UART4 TX ch4 seçilebilir) | **ADC1** (ch0, `ADC1_DMA_OPT 1`) |
| S5 | M8 TIM2_CH1 (ch3) | boş (UART1 RX ch4 seçilebilir) |
| S6 | boş (UART2 TX ch4 seçilebilir) | LED şerit TIM1_CH1 (ch0) |
| S7 | M3 TIM3_CH3 (ch5) | M6 TIM8_CH4 (ch7) |

Denetim:
- Her akışta tek kullanıcı → **çakışma yok**.
- SPI2 (OSD): RX yalnız DMA1 S3 (M2’de) → DMA’sız. SPI3 (flash): RX S0/S2, TX S5/S7 (hepsi motorlarda) → DMA’sız. SpeedyBee V4 ve diğer 8 motorlu F405 hedefleriyle aynı; OSD ve blackbox yoklamalı çalışır.
- SpeedyBee V4 `ADC1_DMA_OPT 0` (DMA2 S0) kullanıyor → SPI1 RX’in iki seçeneği (S0 ADC, S2 M5) dolu, gyro SPI1 DMA’sız kalıyor (analiz). Biz `ADC1_DMA_OPT 1` (S4) ile SPI1’e S0/S3 bırakıyoruz. Bu seçimde TIM8_CH3 `dmaopt 1` (S4) **kullanılmamalı**.
- `DEFAULT_DSHOT_BURST DSHOT_DMAR_OFF`, `DEFAULT_DSHOT_BITBANG DSHOT_BITBANG_OFF` (bit-bang TIM1/TIM8’i ister, LED şeridiyle çakışır).
- **?** Derleyicide/kartta `timer show`, `dma show`, `resource show` ile doğrulanacak (`gomulu-yazilim`, DOG-034/035).

ArduPilot: DShot için TIMx_UP akışlarını (TIM4_UP DMA1 S6, TIM3_UP DMA1 S2, TIM8_UP DMA2 S1, TIM2_UP DMA1 S1/S7) ve `dma_resolver` ile paylaşımı kullanır; `speedybeef4v4` aynı pinlerle derleniyor → ataması geçerli. AP’de çift yönlü DShot M1–M4 (hwdef `BIDIR` PB7, PB1).

### 1.4 SPEEDYBEEF405V4’ten farklar (kendi config’imiz)

| # | Konu | SPEEDYBEEF405V4 | Bizim | Hazır V4 yazılımıyla sonuç |
|---|---|---|---|---|
| 1 | Kayıt | `USE_SDCARD`, SD SPI3 CS PC14 | `USE_FLASH`, `USE_FLASH_W25Q128FV`, `FLASH_CS_PIN PC14`, `FLASH_SPI_INSTANCE SPI3`, `BLACKBOX_DEVICE_FLASH` | Uçar, blackbox yok |
| 2 | UART5 TX | yok | `UART5_TX_PIN PC12` | UART5 yalnız RX |
| 3 | ADC DMA | `ADC1_DMA_OPT 0` | `ADC1_DMA_OPT 1` | Çalışır (gyro DMA’sız) |
| 4 | PC5 | RSSI | RSSI / CUR2 (ArduPilot BATT2) | RSSI olarak okunur |
| 5 | Baro | `USE_BARO_DPS310` | `bom-tedarik` seçimi: DPS310 / SPL06 / BMP280, I2C1 0x76 | DPS310 seçilirse aynı |
| 6 | VBAT ölçeği | `vbat_scale` 110 (varsayılan) | `vbat_scale 150` (15:1) | CLI ile ayarlanır |
| — | Akım ölçeği | `DEFAULT_CURRENT_METER_SCALE 400` | ESC’ye göre (KRR-C INA240A3 10 mV/A → 100) | CLI |
| — | `GYRO_1_ALIGN` | CW90 | yerleşime göre (`pcb-muhendisi`) | CLI `align_board_*` |
| — | `MANUFACTURER_ID` | SPBE | kendi kimliğimiz (Betaflight’a kayıt) | — |

ArduPilot hwdef farkı: `SPIDEV dataflash SPI3 DEVID1 FLASH_CS MODE3 32*MHZ 32*MHZ`, `define HAL_LOGGING_DATAFLASH_ENABLED 1`, `PC12 UART5_TX UART5 NODMA`, `BARO <seçilen> I2C:0:0x76`, `HAL_BATT_VOLT_SCALE 15.0`, BATT2 akım PC5. **?** derleyicide doğrulanacak.

## 2. ESC — esc55a (EFM8BB21 × 4)

### 2.1 J0 (SM08B-SRSS-TB) — mevcut dizilim (Altium, `docs/inceleme.md` §2.1) — D (şemadan), ürün uyumu ?

| Pin | Sinyal | Not |
|---|---|---|
| 1 | CUR | INA199 çıkışı (KRR-C ile INA240A3’e değişecek) |
| 2 | NC | ESC telemetri yok (E7) |
| 3 | M4 | 220 Ω → ch4_in |
| 4 | M3 | 220 Ω → ch3_in |
| 5 | M2 | 220 Ω → ch2_in |
| 6 | M1 | 220 Ω → ch1_in |
| 7 | VBAT | pil (FMU beslemesi; yük sınırı SYS-062) |
| 8 | GND | |

### 2.2 EFM8BB21 port ataması — ?

`docs/inceleme.md` §2.4: pin 1 sinyal girişi, 7/11/13–16 köprü sürme, 17–19 BEMF mux, 20 nötr. Hangi Bluejay düzenine karşılık geldiği doğrulanmadı (SYS-051, RSK-009; `gomulu-yazilim`). Doğrulanınca bu bölüm port/pin tablosuyla doldurulur.

## 3. FMU↔ESC 8 pin konnektör (SM08B-SRSS-TB) — ? **İP-10 doğrulayacak, KRR-004 SpeedyBee**

| Pin | FMU J_ESC1 (M1–M4) | FMU J_ESC2 (M5–M8) | esc55a J0 (bugün) | SpeedyBee F405 V4 |
|---|---|---|---|---|
| 1–8 | **İP-10 doğrulayacak** (KRR-004: SpeedyBee F405 V4 dizilimi, öncelikli) | J_ESC1 ile aynı sıra; motor pinleri M5–M8; VBAT pini FMU’da **bağlı değil** (0 Ω DNP); CUR → PC5; TLM → NC | §2.1 | Üretici kılavuzundan alınacak (İP-10) |

Kurallar (dizilim ne olursa olsun):
- FMU tarafında M1–M4 → PB6, PB7, PB0, PB1; M5–M8 → PC8, PC9, PB10, PA15 (§1.1).
- J_ESC1 CUR → PC1, J_ESC2 CUR → PC5; TLM (varsa) J_ESC1 → PD2 (UART5 RX), J_ESC2 → NC.
- Kablo düz (1:1), SYS-060/061. esc55a J0 dizilimi SpeedyBee’den farklı çıkarsa ESC tarafı değişir (KRR-004 etkisi, `sematik-muhendisi`).
