# fmu — F405 uçuş kontrol kartı

Diatone Mamba F405 MK2 referans alınarak çizilmiş uçuş kontrol kartı. STM32F405 (LQFP64, 24 MHz HSE), ICM-42688-P IMU (SPI1), BMP388 baro (+ BMP280 yedek), MAX7456/AT7456E OSD (SPI2, 27 MHz), W25Q128 flash, TPS54202 × 2 (9 V ve 5 V BEC), AO3401A ters kutup, USB-C + NUF2042, iki ESC konnektörü (8 motor), DJI, ELRS, GPS, VTX, kamera bağlantıları.

- Kaynak: Altium [`altium/fmu_f405.PrjPcb`](altium/fmu_f405.PrjPcb) — tek sayfa `fmu.SchDoc`, 143 parça.
- PCB: **yok**.
- KiCad: taşınmadı.

## Kontrol (2026-11-06)

| | Sonuç |
|---|---|
| Çift referans | U0 ×2, J1 ×2, U6 ×2 (BMP388/BMP280), C60 ×2, C61 ×2, C? ×3, R? ×2 |
| BEC geri besleme | 9 V: 0.596 × (1 + 100/7.15) = 8.93 V; 5 V: 0.596 × (1 + 100/13.7) = 4.95 V |
| VBAT bölücü | 100 k / 10 k → 36 V tam ölçek |

Bulgular F1–F7: [`docs/inceleme.md`](../../docs/inceleme.md) §4.2.
