# Boards

Her alt klasör bir fiziksel kart. İçinde Altium orijinali (`altium/`, değiştirilmez), taşımadan sonra KiCad projesi (`<ad>/`) ve `README.md` (durum, kontrol sonuçları, açık işler).

| Klasör | Kart | Durum (2026-11-06) |
|---|---|---|
| [`esc55a`](esc55a/README.md) | 4’ü 1 arada 55 A ESC: 4 × EFM8BB21 + FD6288Q, 24 MOSFET, JW5026 buck, INA199 akım ölçümü | Altium şematik + yollu PCB; KiCad’e taşınmadı |
| [`fmu`](fmu/README.md) | F405 uçuş kontrol: STM32F405, ICM-42688-P, BMP388, AT7456E OSD, W25Q128, 2 × TPS54202 BEC | Altium şematik; PCB yok |

esc65a için kart klasörü yok: yalnız `docs/esc65a.drawio` (fotoğraflar). Gereksinimden sonra açılacak.

KiCad projeleri `lib/` altındaki ortak kütüphaneleri `${KIPRJMOD}/../../../lib/` yoluyla kullanacak.
