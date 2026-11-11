# Firmware

Sahibi `gomulu-yazilim`. Pin ve zamanlayıcı atamalarının tek kaynağı `docs/pin-haritasi.md`. Ayrıntılı inceleme ve kaynaklar: [`docs/rapor/yazilim-inceleme.md`](../docs/rapor/yazilim-inceleme.md) (2026-11-12).

| Klasör / dosya | İçerik | Durum |
|---|---|---|
| [`fmu/STACKF405/config.h`](fmu/STACKF405/config.h) | Betaflight kart tanımı (betaflight/config biçimi), `FC_TARGET_MCU APM32F405`, SPEEDYBEEF405V4 tabanlı, pin haritası §1 ile birebir | Taslak — **derleyicide doğrulanacak** |
| [`esc/README.md`](esc/README.md) | esc55a → Bluejay düzen `C` eşlemesi, ölü zaman, yükleme yolu, güvenlik davranışı | Kaynak koduna göre doğrulandı; kartta DOG-051/052 |

Not: İstenen `STACKF405.config` (CLI/unified-target biçimi, Betaflight ≤ 4.4) yerine `config.h` yazıldı: Betaflight ≥ 4.5 yalnız `configs/<ad>/config.h`’den derler (`mk/config.mk`), MCU seçimi de bu dosyadaki `FC_TARGET_MCU`’dan gelir; CLI ayar adları 2026.6’da değişti (ör. `gyro_1_bustype` yok), eski biçim doğrulanamaz.

## Bulgular (2026-11-12)

| # | Konu | Sonuç | Yazılım ayarı / not |
|---|---|---|---|
| 1 | APM32F405RGT6 — Betaflight | **İki imaj** (aynı config içeriği, iki `FC_TARGET_MCU`) | APM32 platformu **≥ 2025.12** (4.5.x’te yok). DMA ve zamanlayıcı tabloları STM32 ile birebir → pin-haritasi §1.3 aynen geçerli. HSE 8 MHz → 168 MHz. VCP 314B:5740, ROM DFU 314B:0106 Configurator’da tanımlı. STM32 varyantı: `STACKF405_STM` (yalnız MCU satırı farklı) |
| 1 | APM32F405 — INAV 9.1 | Desteklenmiyor | gereksinim değil |
| 1 | APM32F405 — ArduPilot | **Desteklenmiyor** | MCU tanımı/hwdef yok; STM32 imajının APM32’de çalıştığı kanıtsız. SYS-056 APM32’li kartta ✗ → **SOR-018 sorulmalı** |
| 2 | Baro SPA06-003 ↔ DPS368 | **Tek imaj** | BF `barometer_dps310.c` 0x10 + 0x11 (tüm sürümler). AP: `BARO DPS310 I2C:0:0x76` **önce**, `BARO SPL06 I2C:0:0x76` sonra; SPA06 Copter ≥ 4.6. Tokmas “DPS368” C55090144 aslında 0x11 (SPA06 eşleniği) |
| 3 | IMU Tokmas ↔ TDK ICM-42688-P | **Tokmas desteklenmiyor (kritik)** | Tokmas C54308212: kimlik 0x1F = 0xA1, WHO_AM_I 0x47 yok → BF/AP tanımaz. Yalnız TDK (0x47). ALT: ICM-42605 / IIM-42652 (TDK). Numunede 0x75 okunarak teyit |
| 4 | Flash W25Q128JV ALT | **Tek imaj** (uygun ALT ile) | BF + AP kararlı ortak: 0xEF4018, 0xEF7018, 0x20BA18, 0x016018, 0x5E4018 (AP ≥ 4.7). Öneri ALT: **W25Q128JVSIM** (C401671); GD25Q128/BY25Q128/PY25Q128 yalnız BF |
| 5 | OSD AT7456E ↔ MAX7456 | **Tek imaj** | Aynı sürücü, BF tipi CMAL[6] ile algılar; MAX7456 tedarik yok |
| 6 | ESC akım (RSA240C / INA240A3, ×100) | Aynı ölçek | `ibata_scale 100`, `ibata_offset 0` (birim mV/10A). SJ101 kapalı (iki ESC ortalaması) → 50. AP `BATT_AMP_PERVLT 100` |
| 7 | ESC Bluejay | **Düzen `C` birebir**; EFM8BB21F16I ✓ (`MCU=H`) | Ölü zaman derleme sabiti 20.4 ns/adım → **10 (204 ns)**; 24 kHz → **`C_H_10_24_v0.21.0.hex`** |
| 8 | 9 V PINIO (PB11) | `PINIO1_CONFIG 129` = çıkış + ters → açılışta **açık** | **`PINIO1_BOX 40`** (USER1 aktif = 9 V kapalı). SpeedyBee’nin `0` (= ARM) değeri bizde silahlanınca 9 V’u keser — kopyalanmaz |

## Kararlar (gomulu-yazilim, bu iş paketi)

| # | Karar | Gerekçe |
|---|---|---|
| Y1 | Betaflight hedefi betaflight/config `config.h` biçiminde; seri MCU APM32F405, STM32 ALT için ikinci klasör | Betaflight bir config’e tek MCU bağlar; AT32 varyantlarındaki emsal (`REVO` / `REVO_AT`) |
| Y2 | Sensör/flash muadilleri için sürücüler config’te açık (ICM42688P/42605/IIM42652/42686P, DPS310 + SPA06, M25P16) | SYS-095 (d): ALT aynı imajda tanınır |
| Y3 | `PINIO1_CONFIG 129`, `PINIO1_BOX 40` | Donanımda EN yüksek = açık; 9 V asla ARM’a bağlanmaz |
| Y4 | `vbat_scale 150`, `ibata_scale 100`, `ibata_offset 0` | 15:1 bölücü; ×100, 0.1 mΩ |
| Y5 | ESC: Bluejay v0.21.0 `C_H_10_24` | Düzen `C` birebir; ≥ 200 ns ek ölü zaman; 24 kHz |
| Y6 | ArduPilot hwdef (sonraki iş): `BARO DPS310` + `BARO SPL06` (bu sırayla), dataflash, `PB11 PINIO1 OUTPUT HIGH`; yalnız STM32F405 dizili kart | AP’de APM32 yok |

## Pin / zamanlayıcı / DMA (config ↔ pin-haritasi §1)

Motor M1–M8: PB6, PB7, PB0, PB1, PC8, PC9, PB10, PA15 (TIM4, TIM4, TIM3, TIM3, TIM8, TIM8, TIM2, TIM2) — DMA1 S0, S3, S7, S2; DMA2 S2, S7; DMA1 S1, S5. LED PA8 TIM1 DMA2 S6. ADC1 DMA2 S4 (`ADC1_DMA_OPT 1`). SPI1 (gyro) DMA2 S0/S3. SPI2 (OSD), SPI3 (flash) DMA’sız. `DSHOT_DMAR_OFF`, `DSHOT_BITBANG_OFF`. APM32 tablolarıyla aynı olduğu kaynaktan kontrol edildi; kartta `timer show` / `dma show` (DOG-034/035).

## Yükleme yolu

| Kart | Yol |
|---|---|
| FMU (APM32F405) | BOOT düğmesi + USB → ROM DFU (314B:0106) → Betaflight Configurator, kart adı `STACKF405`. Betaflight ≥ 2025.12. Windows’ta DFU sürücüsü (WinUSB) gerekebilir |
| FMU (STM32F405 ALT) | ROM DFU (0483:DF11) → `STACKF405_STM` derlemesi |
| ESC | İlk: C2 (pin 5/6 pedleri) ile `C_H_10_24_v0.21.0.hex`; sonra Betaflight passthrough + esc-configurator |

Uyarı: Configurator DFU MCU türünü denetlemez (yalnız flash boyutu) → yanlış derleme yüklenebilir; BOOT ile kurtarılır. MCU türü kart etiketinde/ipek baskıda belirtilmeli.

## Kaynaklar

Betaflight [2026.6.2](https://github.com/betaflight/betaflight/tree/2026.6.2) (`e0b7bb0`), [betaflight/config](https://github.com/betaflight/config) (`cacb3a0`), [betaflight-configurator](https://github.com/betaflight/betaflight-configurator) (`9c8b310`), [ArduPilot master](https://github.com/ArduPilot/ardupilot) (`aea9a1b`) + Copter-4.5.7/4.6.3/4.7.2, [INAV 9.1.0](https://github.com/iNavFlight/inav/tree/9.1.0), [Bluejay v0.21.0](https://github.com/bird-sanctuary/bluejay/tree/v0.21.0) (`93bf3e1`). Dosya yolları ve veri sayfaları: rapor §11. Lisans: Betaflight, Bluejay GPL-3.0; `config.h` SPEEDYBEEF405V4 (GPL-3.0) türevi, başlıkta belirtildi.

## Açık konular

1. **SOR-018** müşteriye (yönetici): APM32 için iki BF derlemesi + ArduPilot’ta APM32 yok.
2. **IMU ana parçası** (Tokmas C54308212) yazılımca uyumsuz → `sematik-muhendisi` / `bom-tedarik` yeniden seçim; numunede teyit.
3. `MANUFACTURER_ID` (geçici `STCK`) ve kart adı Betaflight’a kayıt; `GYRO_1_ALIGN` yerleşim sonrası.
4. Bluejay sıcaklık koruması eşiği (varsayılan kapalı).
5. ArduPilot hwdef (SYS-056, STM32 SKU) — sonraki iş.
