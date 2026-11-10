# FMU (STM32F405) — açık kaynak referans taraması ve önerilen mimari

Sahibi `sistem-mimari`. Tarih: 2026-11-10. Kapsam: M1 F405 FMU (5" stack), M4a iki ESC konnektörlü 8 motor varyantı, M3 8S hazırlığı, ArduPilot (kısıtlı firmware) fırsatı. Girdi: `docs/inceleme.md` §4, `docs/rapor/guc-ip03.md` §8 (G7–G10, G15–G18), `docs/gereksinimler/sistem.md`, `docs/pazar/urun-portfoyu-yol-haritasi.md`. Pin/zamanlayıcı/DMA ataması: `docs/pin-haritasi.md` §1.

> **Not:** `boards/fmu/altium/fmu.SchDoc` cezeri’den gelmiştir (Diatone Mamba F405 MK2 tersine mühendisliği); müşteri bunu kendi F405 şeması saymıyor. Bu belge FMU’yu referans tasarımlar + veri sayfaları + güç analizinden (`guc-ip03`) yeniden tanımlar; Altium şeması yalnız karşılaştırma girdisidir.

Yöntem: GitHub API ile depo/lisans doğrulama, Betaflight `betaflight/config` ve ArduPilot `hwdef` dosyalarının indirilmesi (scratchpad, repoya konmadı), WebSearch. İndirilen dosyalar: `fmuref/bf/*.h` (SPEEDYBEEF405V4/V5, GEPRCF405, MAMBAF405US, MATEKF405STD/TE, REVO, REVOLT), `fmuref/ap/*.dat` (speedybeef4v4, MatekF405-TE/-Wing, MambaF405v2, MicoAir405v2, omnibusf4pro), `fmuref/src/dma_reqmap.c`, `timer_f4.c` (Betaflight F4 DMA/zamanlayıcı tablosu), Revolution ve Sparky2 şema PDF’leri.

## 1. Referans tablosu

“Açık” = şema/PCB kaynak dosyası yayımlanmış. “Yalnız config” = donanım kapalı, yalnız yazılım tarafı pin ataması açık (GPL-3).

| # | Ad | Kaynak | Lisans | Format | MCU | IMU | Baro | OSD | Flash/kayıt | BEC / güç (giriş V maks, parça) | USB koruması | UART / motor | Konnektör | Durum | Bizim için ne alınır |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **SpeedyBee F405 V4** (BF `SPEEDYBEEF405V4`, AP `speedybeef4v4`) | [BF config](https://github.com/betaflight/config/blob/master/configs/SPBE/SPEEDYBEEF405V4/config.h), [AP hwdef](https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef/speedybeef4v4) | Donanım kapalı; config GPL-3 | Yalnız config | F405RG, HSE 8 MHz | ICM-42688-P (SPI1) | DPS310 (BF) / SPL06 (AP), I2C1 | AT7456E (SPI2) | microSD (SPI3) | Şema yok | Şema yok | 6 UART (UART5 yalnız RX) / **8 motor** + LED + servo | 8 pin ESC (dizilim İP-10) | Satışta; ürün V5’e geçiyor (V5 yalnız 4 motor) | **Pin/zamanlayıcı/DMA ataması** (KRR-004 ailesi), BF + AP hedefi aynı pinlerle hazır, PINIO1 = VTX güç anahtarı |
| 2 | **Mini-Air FC** (darshg321) | [GitHub](https://github.com/darshg321/Mini-Air) | **CERN-OHL-W-2.0** (GitHub API); OSHWA CA000079 (arama sonucu, sertifika sayfası açılmadı) | KiCad + PDF + JLC BOM (LCSC kodlu) | F405RGT6, 8 MHz | **ICM-42688-P** | BMP280 | **AT7456E** | **W25Q128JV** | TPSM84209 modül (VIN ≤ 28 V) → 5 V; **2 × LP5912-3.3** (ayrı gyro LDO’su); FCM1608 ferrit | USB-C, 1N5819 VBUS diyotu; ESD görülmedi | — / 4 | 8 pin ESC (GND/VBAT/M1–M4/CUR/NC), SH | Kişisel proje, 2026-08; uçuş durumu belgesiz | **Parça seti bizimkinin aynısı** (BOM karşılaştırma), ayrı IMU LDO’su fikri, LCSC kodları |
| 3 | **FeroFlyF405** (Ozonised) | [GitHub](https://github.com/Ozonised/FeroFlyF405), [haber](https://circuitdigest.com/news/feroflyf405-an-open-source-drone-flight-controller-designed-from-scratch-on-the-stm32f405-with-inav-ported) | **CERN-OHL-P-2.0** (izin verici) | KiCad (8 sayfa: Power, MCU, IMUs, IO…), iBOM | F405 | LSM6DSL | DPS368 | Yok | — | AP63300 (32 V) + AP63200 → 5 V / 4.5 V, TLV757P LDO × 2, SK34 / PMEG3020 diyotlar | — | 3 UART / 12 çıkış, CAN | JST-GH, **Pixhawk konnektör standardı** | Bakımlı (2026-11-03); V1.1 “motor 3 DMA sorunu” düzeltmesi | Çok sayfalı KiCad düzeni, güç sayfası (buck + iki LDO), DMA dersinin kanıtı (§3) |
| 4 | **KURC F405** (ganymede451) | [GitHub](https://github.com/ganymede451/kurc-f405) | **CERN-OHL-S-2.0** (güçlü karşılıklı) | KiCad 10 + PDF | F405RGT6 | BMI270 | — | — | microSD | **TPS54360 (60 V)** → 5 V, AP2112K-3.3 | USB-C | — / 4 (SPEEDYBEEF405V3 pinleri) | 8 pin SH ESC | Üretilmedi, uçmadı (README) | 60 V buck’ın F405 FC’de kullanımı (8S fikri); SpeedyBee pin uyumluluğu yaklaşımının aynısı |
| 5 | **OpenPilot Revolution** (LibrePilot) | [LibrePilot hardware](https://github.com/librepilot/LibrePilot/tree/next/hardware/Production/OpenPilot%20Revolution), [ArduPilot arşivi](https://github.com/ArduPilot/Schematics/tree/master/OpenPilot-Revolution) | **CC-BY-NC-SA** (License.txt: “klon/türev satılamaz”; şema “Not for commercial use”) | Altium + PDF | F405RGT6 | MPU-6000 | MS5611 | Yok | 16 Mbit flash | Şemada LDO tabanlı | Micro-USB | 4 UART / 6 (+ servo) | Eski DF13 | Arşiv (≈2015) | **Yalnız inceleme.** F405 RG temel devresi (VCAP, BOOT, HSE), sensör filtreleme; ticari türev yasak |
| 6 | **TauLabs Sparky2** | [TauLabs hw](https://github.com/TauLabs/TauLabs/tree/next/flight/targets/sparky2/hw), [ArduPilot arşivi](https://github.com/ArduPilot/Schematics/tree/master/TauLabs-Sparky) | **CC-BY-NC-SA 4.0** | KiCad + PDF + BOM | F405RGT6 | MPU-9250 | MS5611 | Yok | — | LP2992 LDO | — | — / 10, CAN | — | Arşiv (2017) | Yalnız inceleme (NC) |
| 7 | **Pixhawk FMUv2/v3** (F427) | [pixhawk/Hardware](https://github.com/pixhawk/Hardware) | **CC-BY-SA 3.0** (README: doğrudan türev açık kaynak olmalı) | Altium/PDF | F427 | MPU-6000/9250, L3GD20 | MS5611 | — | microSD | Güç modülü + yedekli besleme, ideal diyot | ESD + PTC | 5 UART / 8 + 6 | DF13 / Pixhawk standardı | Arşiv (2022) | **Mimari referans:** güç yolu seçici (BAT/USB), IMU ayrı ve filtreli besleme, ESD/seri dirençli dış pedler |
| 8 | Chickadee F4FC | [GitHub](https://github.com/chickadee-tech/f4fc) | CC-BY-4.0 | KiCad (kütüphane ayrı depoda) | F405**VG** (LQFP100) | MPU-6000 | — | — | — | Polystack modülü | — | — | Polystack | Terk edilmiş (2016) | Önemsiz (LQFP100, eski) |
| 9 | Acci FC (jesuslg123) | [EasyEDA](https://easyeda.com/jesuslg123/f4-v1) | CC BY-NC-SA 3.0 | EasyEDA | F4 | ICM-42688-P varyantı | — | — | — | — | — | — | — | “RC 1.1 test ediliyor”, 42688 varyantı “test edilmedi” | Yalnız inceleme (NC) |
| 10 | Diatone Mamba F405 MK2 / US | [BF `MAMBAF405US`](https://github.com/betaflight/config/blob/master/configs/DIAT/MAMBAF405US/config.h), AP `MambaF405v2` | Donanım kapalı; config GPL-3 | Yalnız config (+ bizim drawio) | F405 | MPU-6000 / 42688 | BMP280 | MAX7456 | W25Q128 (SPI3) | — | — | 6 UART / 4 (+LED) | 8 pin ESC | Satışta | Cezeri Altium şemasının kaynağı; AP’de **dataflash günlüğü** F405’te çalışıyor kanıtı |
| 11 | GEPRC F405 / Taker | [BF `GEPRCF405`](https://github.com/betaflight/config/blob/master/configs/GEPR/GEPRCF405/config.h) | Kapalı; GPL-3 config | Yalnız config | F405 | MPU-6000/42688 (SPI3) | BMP280/DPS310 (I2C2) | AT7456E (SPI1) | W25Q128 (SPI2) | — | — | 6 UART / 7 | 8 pin ESC | Satışta | KRR-004 ikinci ailesi; SpeedyBee’den farklı pinler (uyumlu tutulamaz) |
| 12 | Matek F405-TE / STD | [BF `MATEKF405TE`](https://github.com/betaflight/config/blob/master/configs/MTKS/MATEKF405TE/config.h), AP `MatekF405-TE` | Kapalı; GPL-3 config | Yalnız config + üretici pin şeması | F405 | ICM-42688-P | DPS310/SPL06 | AT7456E | flash + SD | — | — | 6 UART / 8 + servo | Ped | Satışta | 8 motorlu ikinci DMA çözümü (karşılaştırma); şema yok |
| 13 | MicoAir405v2 | AP `MicoAir405v2` | Kapalı; GPL-3 hwdef | Yalnız hwdef | F405 | **BMI088** | SPL06 (SPI) | AT7456E | microSD | — | — | — / 10 | — | Satışta | ArduPilot odaklı F405 örneği (BMI088 seçeneği) |
| 14 | Raceflight / FlightOne Revolt | [BF `REVOLT`](https://github.com/betaflight/config/tree/master/configs/FLON/REVOLT) | Firmware açık; **donanım şeması bulunamadı** | — | F405 | ICM-20602 | — | — | — | — | — | — | — | Üretimden kalktı | Yok |
| 15 | BrainFPV, Holybro Kakute F4 | — | Kapalı (şema bulunamadı) | — | — | — | — | — | — | — | — | — | — | — | Yok |
| 16 | oshwhub.com (“F405 飞控”) | oshwhub.com arama | — | — | — | — | — | — | — | — | — | — | — | Site araması 0 proje döndü (2026-11-10); arama motoru dizinlemiyor | **Bulunamadı**; elle tarama gerekirse oturumla (`pazar-analisti`/yönetici) |

### 1.1 En iyi 5 referans ve gerekçe

| Sıra | Referans | Neden |
|---|---|---|
| 1 | **SpeedyBee F405 V4 config + hwdef** | KRR-004 ailesi; 8 motor + LED + 6 UART + SPI1 IMU + SPI2 OSD + SPI3 kayıt aynı LQFP64’e sığdırılmış, **BF ve ArduPilot’ta resmi hedef**. Aynı pinler = hazır yazılım + uyumluluk iddiası |
| 2 | **Mini-Air** (CERN-OHL-W) | Parça seti bizimle birebir (F405RGT6, ICM-42688-P, AT7456E, W25Q128JV, AO3401A, USB-C), KiCad + LCSC kodlu JLC BOM; ayrı gyro LDO’su |
| 3 | **FeroFlyF405** (CERN-OHL-P) | En serbest lisans; çok sayfalı, okunaklı KiCad yapısı; 32 V buck + çift LDO güç sayfası; DMA hatasının ve düzeltmesinin belgelenmiş olması |
| 4 | **Pixhawk FMUv2/v3** (CC-BY-SA) | Güç yolu (BAT/USB seçimi, ters kutup), sensör besleme filtrelemesi, ESD ve konnektör standardında olgun mimari referansı |
| 5 | **KURC F405** (CERN-OHL-S) | 60 V buck (TPS54360) ile F405: 8S hazırlığı için ölçek; SpeedyBee pin uyumluluğu yaklaşımı (CLI remap) |

### 1.2 Lisans notları (hukuki görüş değildir)

| Lisans | Bulunduğu referans | Bizim kullanımımızın etkisi |
|---|---|---|
| GPL-3 | Betaflight config, ArduPilot hwdef | Pin ataması işlevsel bilgidir; aynı pinleri kullanmak lisans yükü getirmez. **Kendi `config.h` / `hwdef.dat` dosyamız** BF/AP deposuna gireceği için zaten GPL-3 olur (SYS-050) |
| CERN-OHL-P-2.0 | FeroFlyF405 | İzin verici: dosya alınırsa telif/lisans bildirimi korunur; ürün kapalı kalabilir |
| CERN-OHL-W-2.0 | Mini-Air | Zayıf karşılıklı: **alınan/değiştirilen tasarım parçaları** (ör. bir şema sayfası, kütüphane) dağıtılırsa açık kalır; bizim yeni parçalarımız kapalı kalabilir |
| CERN-OHL-S-2.0 | KURC F405 | Güçlü karşılıklı: türetilmiş **tüm** tasarım ürünle birlikte açık kaynak verilmeli |
| CC-BY-SA 3.0 | Pixhawk | Türev tasarım CC-BY-SA ile açık olmalı, atıf zorunlu (README “doğrudan türev açık kaynak olmalı”) |
| CC-BY-NC-SA (3.0/4.0) | Revolution, Sparky2, Acci FC | **Ticari türev yasak.** Yalnız okunur; hiçbir dosya, sembol, ayak izi, yerleşim alınmaz |

**Uygulama kuralı (öneri, KRR):** Tasarım veri sayfaları + `guc-ip03` hesapları + kendi KiCad kütüphanemizle (`lib/`) sıfırdan çizilir. Referanslardan **dosya kopyalanmaz** (sembol, ayak izi, şema sayfası, yerleşim); yalnız mimari fikir ve yayımlanmış pin ataması (işlevsel bilgi) kullanılır. Bu durumda yukarıdaki lisansların hiçbiri ürüne geçmez. CERN-OHL-P/W kaynaklı bir dosya ileride gerçekten alınırsa belgeye ve `CHANGELOG.md`’ye kaynak + lisans yazılır; -S, CC-BY-SA, NC kaynaklardan dosya alınmaz. Tasarımı açık yayımlama (pazar §D “açık belge”) ayrı bir müşteri kararıdır (§6 S2).

## 2. Referanslardan çıkan dersler

| # | Ders | Kaynak | Bizim tasarıma etkisi |
|---|---|---|---|
| D1 | F405’te 8 DShot + LED şeridi ancak SPI2/SPI3 DMA’sız sığar; bütün 8 motorlu F405 hedefleri böyle (SpeedyBee V4: `DSHOT_DMAR_OFF`, `DSHOT_BITBANG_OFF`) | BF config, `dma_reqmap.c` | OSD ve flash DMA’sız (yoklamalı) çalışır; gyro SPI1 DMA’lı kalır (`pin-haritasi.md` §1.3) |
| D2 | SpeedyBee V4’te `ADC1_DMA_OPT 0` (DMA2 S0) SPI1 RX’in iki seçeneğinden birini (S0) alıyor, diğeri (S2) M5’te → gyro SPI1 DMA’sız kalıyor (analiz; derleyicide `dma show` ile doğrulanacak) | `dma_reqmap.c` | Biz `ADC1_DMA_OPT 1` (DMA2 S4): SPI1 RX S0 + TX S3 serbest. Matek F405-TE ve SpeedyBee V5 de `ADC1_DMA_OPT 1` kullanıyor |
| D3 | FeroFly V1.0 “motor 3 DMA sorunu” ile revizyon gerektirdi | FeroFly README/haber | DMA tablosu şematik öncesi kilitlenir (bu belge + `pin-haritasi.md`), `gomulu-yazilim` derleyicide `timer show`/`dma show` ile teyit eder |
| D4 | Bütün açık tasarımlarda IMU ayrı LDO veya ferrit + LDO ile besleniyor (Mini-Air 2 × LP5912, FeroFly 2 × TLV757, Pixhawk ayrı sensör rayı) | Şema/BOM | G9 önerisi (AMS1117 + IMU’ya 10 Ω + 1 µF) korunur; ikinci seçenek: IMU için ayrı küçük LDO (§4.3) |
| D5 | Açık F405 tasarımlarının buck’ları 28–32 V sınıfı (TPSM84209 28 V, AP63300 32 V); yalnız KURC 60 V | BOM | 3–6S için SY8303 (40 V, G7) yeterli; 8S için 60 V sınıfı buck gerekir (§4.4) |
| D6 | ArduPilot F405’te dataflash günlüğünü destekliyor (`MambaF405v2`: `HAL_LOGGING_DATAFLASH_ENABLED`) ve 48 KB önyükleyici + 8 MHz HSE bekliyor | AP hwdef | 16 MB W25Q128 ArduPilot için de kayıt aygıtı olur; HSE 8 MHz (Altium 24 MHz yerine) |
| D7 | ArduPilot SpeedyBee hwdef’inde çift yönlü DShot (BIDIR) yalnız M1–M4 gruplarında (TIM4, TIM3) | AP hwdef | ArduPilot’ta M5–M8 RPM telemetrisi yok (bilgi); Betaflight’ta 8 kanal zamanlayıcı tabanlı çift yönlü DShot tezgâhta doğrulanacak (DOG-034/035) |

## 3. Pin ataması özeti

Ayrıntılı tablo, DMA akış haritası ve Betaflight/ArduPilot farkları: **`docs/pin-haritasi.md` §1**. Özet:

- **Temel:** Betaflight `SPEEDYBEEF405V4` ve ArduPilot `speedybeef4v4` ile **aynı** motor, LED, UART, SPI, I2C, ADC, PINIO pinleri. Hazır SpeedyBee F405 V4 yazılımı bizim kartta motorlar, IMU, OSD, UART’lar ve VBAT/akımla çalışır.
- **Farklar (6):** (1) SPI3’te microSD yerine W25Q128 flash, CS PC14; (2) UART5 TX PC12 eklenir (6 tam UART); (3) `ADC1_DMA_OPT 1`; (4) ESC2 akımı PC5 (RSSI pini, ArduPilot BATT2); (5) baro parçası (DPS310 / SPL06 / BMP280 — `bom-tedarik` seçer, I2C1 0x76); (6) VBAT bölücü 15:1 (`vbat_scale 150`) 8S için.
- **DMA:** 8 motor + LED + ADC + SPI1 çakışmasız; SPI2 (OSD) ve SPI3 (flash) DMA’sız (SpeedyBee V4 ile aynı), DMA1 S4/S6 ve DMA2 S1/S5 UART DMA’sı için boş.

## 4. Önerilen mimari

### 4.1 Blok diyagram

```
                 ┌──────────────────────────── FMU 36 × 36 mm, 30.5 × 30.5 M3, 4 katman ───────────────────────────┐
 BAT+/BAT− pedleri ─┐  (U9 öncesi, 22–24 AWG; SYS-062, G16/G17)
 J_ESC1.VBAT ───────┴─ BAT düğümü ─ F9 sigorta 5 A ─ U9 P-MOS (D pil, S yük; G8) ─ VIN ─┬─ TVS (6S: SMBJ24CA)
 J_ESC2.VBAT ── NC (0 Ω DNP)                     zener 10 V G–S, 100 k              ├─ 2 × 10 µF 50 V + 100 nF
                                                                                    ├─ VBAT bölücü 140 k / 10 k (0.5 %) → PC0
                                                                                    ├─ U3 SY8303 → 9 V 1.5 A ── EN ← PB11 (PINIO1)
                                                                                    │      └→ 9 V pedleri (VTX, kamera), DJI 6 pin SH
                                                                                    └─ U4 SY8303 → 5 V 2 A ──┬→ AT7456E (5 V), LED şerit, buzzer (AO3400A ← PC15)
                                                                USB-C VBUS ─ PTC/ESD ─ Schottky ─────────────┤   RX / GPS 5 V pedleri
                                                                                                             └→ U5 AMS1117-3.3 (SOT-223, 22 µF) → 3V3
                                                                                                                   ├→ MCU VDD (×4 100 nF + 4.7 µF), VDDA (ferrit + 1 µF)
                                                                                                                   ├→ W25Q128JV, baro (I2C1), 3V3 dış pedi ≤ 100 mA
                                                                                                                   └→ 10 Ω + 1 µF (+ 100 nF) → ICM-42688-P VDD/VDDIO
 STM32F405RGT6 LQFP64, HSE 8 MHz
   SPI1 ── ICM-42688-P (CS PA4, INT1 PC4)          SPI2 ── AT7456E (CS PB12, 27 MHz kristal, CVBS in/out 75 Ω)
   SPI3 ── W25Q128JV 16 MB (CS PC14)               I2C1 ── baro (0x76) + dış I2C (GPS/pusula konnektörü)
   TIM4/3 ── M1–M4 ─ J_ESC1 (SM08B)                TIM8/2 ── M5–M8 ─ J_ESC2 (SM08B, Dual SKU’da takılı)
   ADC1 ── PC0 VBAT, PC1 CUR1 (J_ESC1), PC5 CUR2 (J_ESC2) / RSSI
   UART1 DJI/MSP · UART2 alıcı (+ SBUS ters çevirici) · UART3 yedek · UART4 analog VTX · UART5 ESC TLM / yedek · UART6 GPS
   USB-C (PA11/12, CC 5.1 k × 2, USBLC6-2 veya NUF2042) · BOOT düğmesi · SWD pedleri (PA13/14) · LED0 PC13 · LED şerit PA8 · CC PB14
```

### 4.2 Blok bazında seçim

| Blok | Seçim | Gerekçe / kaynak | Sahibi |
|---|---|---|---|
| MCU | STM32F405RGT6 LQFP64, **HSE 8 MHz** | SYS-030; 8 MHz → SPEEDYBEEF405V4 ve AP önyükleyicisi değişmeden (F3 kapanır) | sematik |
| IMU | ICM-42688-P, SPI1, INT1 → PC4; INT2/CLKIN boş | SYS-031; SpeedyBee V4 ile aynı | sematik |
| IMU beslemesi | AMS1117 3V3 → 10 Ω + 1 µF + 100 nF (G9). Seçenek: ayrı 3.3 V LDO (Mini-Air/FeroFly gibi) | SYS-042 ≤ 10 mVpp; G9 hesabı ≈ 0.5 mV | guc, sematik |
| Baro | I2C1 (PB8/PB9) 0x76, **tek parça** (DPS310, SPL06-001 veya BMP280) | SYS-032; F2 çift referans kapanır. SpeedyBee BF=DPS310, AP=SPL06 | bom-tedarik |
| OSD | AT7456E, SPI2, CS PB12, 27 MHz, 5 V besleme | SYS-034 | sematik |
| Flash | W25Q128JV 16 MB, SPI3, CS PC14 | SYS-033; BF + AP dataflash | sematik |
| Buck 5 V / 9 V | **SY8303AAIC × 2** (40 V), R_FS 200 k, L: SWPA6045S6R8MT (5 V) / SWPA5040S100MT (9 V), 9 V EN ← PB11 | G7, G10, KRR-F | sematik, guc |
| 3.3 V | AMS1117-3.3 SOT-223, 22 µF | G9 | sematik |
| Ters kutup | AO3401A **D pil tarafında, S VIN’de**, zener G–S | G8, SYS-074 (6S) | sematik |
| Besleme yolu | Ayrı BAT+/− pedleri U9/F9 **öncesi**; J_ESC1.VBAT aynı düğüm; J_ESC2.VBAT bağlanmaz (0 Ω DNP) | SYS-062, G16, G17, KRR-I | sematik, pcb |
| VBAT ölçümü | 140 k / 10 k %0.5 → 15:1, tam ölçek 49.5 V, `vbat_scale 150`; PC0’da 100 nF | SYS-022 (≥ 30 V), 8S için ≥ 45 V; G15 | sematik, test |
| Akım | CUR1 (J_ESC1.CUR) → PC1; CUR2 (J_ESC2.CUR) → PC5; SJ (açık) ile CUR2 → 10 k/10 k ortalama PC1 (BF 8 motor seçeneği) | SYS-020; inceleme §8.1 (J1 akımı bağlı değildi) | sematik, gomulu |
| USB | USB-C, CC 5.1 k × 2, ESD (USBLC6-2SC6 veya NUF2042), VBUS → Schottky → 5 V (geri besleme yok) | SYS-036, SYS-075 | sematik |
| SBUS | Ayrı SBUS pedi → tek transistör / 74LVC1G04 ters çevirici → 1 k → UART2 RX (CRSF pedi doğrudan RX2) | SYS-035 (F405 USART ters çeviremez) | sematik |
| Programlama | BOOT0 düğmesi, SWD pedleri (SWDIO, SWCLK, GND, 3V3) | SYS-055 | sematik, pcb |
| ESC konnektörü | J_ESC1 SM08B (M1–M4), J_ESC2 SM08B (M5–M8). **Tek PCB**, J_ESC2 yalnız Dual SKU’da takılı (M4a) | SYS-037, SYS-060, K10 | sematik, pcb |
| Çevre konnektörleri | Alıcı 4 pin SH (UART2), GPS 6 pin SH (UART6 + I2C1 + 5 V), DJI 6 pin SH (UART1 + 9 V), analog VTX/kamera pedleri (UART4, 9 V/5 V, CVBS) | SYS-065 | sematik |
| Mekanik | 36 × 36 mm, 30.5 × 30.5 M3 (SYS-080/081), 4 katman (iç GND + güç), BEC’ler kenarda MCU/IMU’dan uzak | G18, SYS-081 | pcb |

### 4.3 Güç bütçesi (guc-ip03 §8’den)

| Ray | Yük | Kaynak | Pay |
|---|---|---|---|
| 9 V | 1.5 A | SY8303, η ≈ %96, 0.6 W | L: tepe %72 I_sat |
| 5 V | 2 A (OSD, LED, alıcı, GPS, 3V3 LDO girişi dahil) | SY8303, η ≈ %93, 0.75 W | L: tepe %60 I_sat |
| 3.3 V | 240 mA (MCU 102 + flash 25 + sensör + dış 100) | AMS1117, 0.43 W | %24 sınıf |
| Giriş | 23.5 W → 3S 3.0 A, 6S 1.1 A | BAT pedleri (SH pini değil) | SYS-062 |
| Kart ısı | ≈ 2.5 W → 60–90 °C (T, masa) | G18 | DOG-044 belirleyici |

### 4.4 8S hazırlığı (SYS-003, M3)

8S LiHV dolu = 8 × 4.35 = **34.8 V**; SYS-014 kuralıyla (geçici + 5 V) VIN’deki parçaların mutlak sınırı ≥ 45 V olmalı (geçici 40 V varsayımı, SYS-003 “≥ 40 V geçici”).

| Parça | 3–6S (M1) | Durum 8S’te | 8S varyantı (M3, aday — `bom-tedarik` + `guc-elektronigi` doğrulayacak) |
|---|---|---|---|
| Buck × 2 | SY8303 40 V | ✗ (40 < 45) | 60–65 V sınıfı buck (ör. TPS54360B — KURC’ta kullanılmış; LMR16030; MP9486A). Kılıf farklı → ya ortak ayak izi bulunur ya ikinci PCB revizyonu |
| U9 P-MOS | AO3401A −30 V | ✗ | −40…−60 V P-MOS (aday sınıfı; seçilecek) |
| F9 sigorta | 32 V DC | ✗ | ≥ 50 V DC sınıflı sigorta |
| TVS | SMBJ24CA | ✗ (V_RWM 24 < 34.8) | SMBJ36CA sınıfı (V_C ≈ 58 V < 60 V buck: sınırda, hesapla doğrulanmalı) |
| VIN kondansatörü | 50 V | ✓ (sınırda) | 63–100 V |
| VBAT bölücü | 15:1 → 49.5 V | ✓ | aynı |
| ESC konnektör VBAT | SH pini | ✓ (gerilim) | aynı |

**Öneri (KRR adayı):** M1 PCB’si 8S **yerleşim payı** ile çizilir (buck çevresinde 60 V parçaya yetecek alan, VIN ağında yol aralığı ≥ 0.2 mm, 63 V kondansatör ayak izi 0805/1206); M1 BOM’u 3–6S (KRR-F). M3’te yalnız BOM + gerekirse buck ayak izi değişir. Bu, SYS-003’ün “FMU iki ESC sınıfında değişmeden kullanılır” metniyle çelişir → müşteri sorusu §6 S1.

### 4.5 M4a — 8 motor, iki ESC konnektörü

- Tek PCB: J_ESC1 (M1–M4, TIM4/TIM3) + J_ESC2 (M5–M8, TIM8/TIM2). Standart SKU’da J_ESC2 takılmaz, M5–M8 pedleri açık kalır (SpeedyBee V4 gibi); Dual SKU’da J_ESC2 takılı + 2. kablo.
- 8 DShot çıkışın tamamı ayrı DMA akışında (`pin-haritasi.md` §1.3): DShot300/600 + Betaflight’ta zamanlayıcı tabanlı çift yönlü DShot mümkün (DMA açısından). CPU yükü 8 kanal çift yönlü DShot’ta F405’te tezgâhta ölçülmeli (DShot300 + 4 kHz PID önerilir, tahmin).
- ESC2 VBAT pini FMU’da bağlanmaz (iki ESC’nin pil hatlarını FMU üstünden paralellememek için).
- ESC2 akımı PC5’e; Betaflight tek akım girişi okur → SJ ile ortalama seçeneği; ArduPilot BATT2 olarak okur.
- ESC telemetri (UART5 RX PD2) yalnız J_ESC1’de; bizim ESC’de TLM pini NC (E7) — Bluejay RPM’i çift yönlü DShot ile verir.

### 4.6 ArduPilot fırsatı

`speedybeef4v4` hwdef pinleri bizimkiyle aynı → kendi hwdef’imiz farkla yazılır: `SPIDEV dataflash SPI3 … PC14`, `HAL_LOGGING_DATAFLASH_ENABLED 1`, UART5 TX, baro satırı, `HAL_BATT_VOLT_SCALE 15.0`, BATT2 PC5. F405 = 1 MB → `minimize_fpv_osd.inc` kısıtlı firmware (Copter, kısıtlı özellik). Resmi kart için ArduPilot board ID başvurusu gerekir. Derleyici yok → “derleyicide doğrulanacak” (`gomulu-yazilim`).

### 4.7 Cezeri Altium şemasıyla farklar (bilgi)

| Konu | Altium (cezeri) | Öneri |
|---|---|---|
| HSE | 24 MHz | 8 MHz |
| Flash | SPI2 (OSD ile ortak) | SPI3 ayrı |
| VBAT ADC | PC3, 8.80:1 (29 V) | PC0, 15:1 (49.5 V) |
| ESC2 akımı | J1.1 bağlı değil | PC5 |
| ESC2 VBAT | bağlı değil | bağlı değil (0 Ω DNP) — aynı |
| Buck | TPS54202 (28 V) | SY8303 (G7) |
| 3.3 V | regülatör yok | AMS1117-3.3 (G9) |
| U9 | ters yönde | düzeltilmiş (G8) |
| BAT3 pedi | VIN’de | U9 öncesi (G17) |

## 5. Gereksinim mühendisine girdiler (öneri)

| Öneri | Tür | Metin (öneri) |
|---|---|---|
| SYS-037 değişiklik | Değişen | 8 motor çıkışı: M1–M4 J_ESC1, M5–M8 J_ESC2 (iki SM08B). Tek PCB; J_ESC2 Dual SKU’da takılı (M4a). 8 çıkışın tamamı ayrı DMA akışında, DShot300/600 + çift yönlü DShot (BF) |
| SYS-03x yeni | Yeni | ESC2 akım hattı MCU ADC’sine bağlı (PC5); Betaflight için ortalama seçeneği (lehim köprüsü); ESC2 VBAT pini FMU’da bağlı değil |
| SYS-050 ek | Değişen | Pin ataması Betaflight `SPEEDYBEEF405V4` ile uyumlu (motor, UART, SPI1/2, I2C, ADC, PINIO); HSE 8 MHz; kendi hedefimiz bu hedefin türevi |
| SYS-056 yeni | Yeni (Ö) | FMU donanımı ArduPilot F405 (kısıtlı) hedefini destekler: 8 MHz HSE, I2C baro + dış pusula, 16 MB dataflash, `speedybeef4v4` hwdef türevi; resmi hedef sonraki iş |
| SYS-003 / SYS-044 | Değişen | M3 8S FMU: VIN’deki parçalar mutlak ≥ 45 V (8S LiHV 34.8 V + geçici 40 V + 5 V pay); M1 PCB’si 8S BOM varyantına yerleşim payı bırakır (S1 cevabına göre) |
| SYS-022 | Değişen | VBAT ölçüm aralığı ≥ 45 V (8S), 15:1 bölücü |
| SYS-035 | Değişen | 6 tam UART (UART5 TX PC12 dahil) + SBUS ters çevirici pedi (UART2) |
| SYS-062 | Netleşen | KRR-I: BAT+/− pedleri U9/F9 öncesi; konnektör VBAT yalnız düşük güç |
| KRR (öneri) — Pin haritası tabanı | Karar | SPEEDYBEEF405V4 tabanı + 6 fark (`pin-haritasi.md` §1.4) |
| KRR (öneri) — Referans kullanım kuralı | Karar | Referanslardan dosya kopyalanmaz; NC, -S ve SA kaynaklar yalnız okunur (§1.2) |
| KRR (öneri) — 8S stratejisi | Karar (müşteri, S1) | §4.4 |

## 6. Müşteriye sorular (en fazla 2)

| # | Soru | Seçenekler | Neden |
|---|---|---|---|
| S1 | 8S hazırlığı: tek FMU mu, iki varyant mı? | 1) **[öneri]** M1 FMU 3–6S BOM, PCB 8S’e yer bırakır; M3’te 8S BOM varyantı (gerekirse küçük revizyon) 2) M1 FMU baştan 8S’e dayanıklı (tek FMU, SYS-003’ün dediği gibi; tahmini +1–2 $/kart, `bom-tedarik` doğrulayacak) | 8S için buck, P-MOS, sigorta, TVS 60 V sınıfına çıkmalı; maliyet M1 bütçesine (KRR-H) dokunuyor |
| S2 | Tasarımı açık kaynak yayımlayacak mıyız? | 1) **[öneri]** Hayır (şimdilik): referanslardan dosya almadan kendi tasarım; sonradan karar verilebilir 2) Evet, CERN-OHL-W/P ile (pazarda “açık belge” farkı) | Açık yayımlarsak CERN-OHL/CC-BY-SA kaynaklardan parça almak serbestleşir ve pazarlama farkı olur; kapalı kalırsak yalnız fikir/pin bilgisi kullanılır |

## 7. Kaynaklar (erişim 2026-11-10)

- Betaflight config: <https://github.com/betaflight/config> (`configs/SPBE/SPEEDYBEEF405V4`, `SPEEDYBEEF405V5`, `GEPR/GEPRCF405`, `DIAT/MAMBAF405US`, `MTKS/MATEKF405TE`, `MTKS/MATEKF405STD`, `OPEN/REVO`, `FLON/REVOLT`)
- Betaflight F4 DMA/zamanlayıcı eşlemesi: <https://github.com/betaflight/betaflight/blob/master/src/platform/STM32/dma_reqmap_mcu.c>, `timer_stm32f4xx.c`
- ArduPilot hwdef: <https://github.com/ArduPilot/ardupilot/tree/master/libraries/AP_HAL_ChibiOS/hwdef> (`speedybeef4v4`, `MatekF405-TE`, `MambaF405v2`, `MicoAir405v2`)
- STMicroelectronics RM0090 (STM32F405/407 başvuru kılavuzu) §10.3.3 DMA1/DMA2 istek eşleme tabloları; `lib/datasheet/STM32F405RGT6.pdf` Tablo 7 (LQFP64 pinleri)
- Açık donanım: <https://github.com/darshg321/Mini-Air>, <https://github.com/Ozonised/FeroFlyF405>, <https://github.com/ganymede451/kurc-f405>, <https://github.com/pixhawk/Hardware>, <https://github.com/ArduPilot/Schematics>, <https://github.com/librepilot/LibrePilot>, <https://github.com/TauLabs/TauLabs>, <https://github.com/chickadee-tech/f4fc>, <https://easyeda.com/jesuslg123/f4-v1>
- Haber: <https://circuitdigest.com/news/feroflyf405-an-open-source-drone-flight-controller-designed-from-scratch-on-the-stm32f405-with-inav-ported>
