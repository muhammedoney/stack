# İzlenebilirlik

MUS → SYS → DOG → tasarım öğesi.

> 2026-11-06: Kapı 1 için ilk türetme; kapı 1’de `Onaylı`. Tasarım öğeleri: ESC `boards/esc55a/altium/`, FMU `boards/fmu/altium/` (KiCad’e taşınmadı); bulgu numaraları `docs/inceleme.md`. SYS → iş paketi önerisi `proje.md` → İş paketleri.
>
> 2026-11-10 (DT-002; müşteri onayı 2026-11-11): MUS-010…013, SYS-004/023/046/056/057 (Taslak), SYS-002/003/022/035/037/042/044/050/055/062 (Değişti), DOG-091…103 eklendi. FMU tasarım öğesi artık `docs/mimari-fmu.md` + `docs/pin-haritasi.md` (Altium fmu yalnız karşılaştırma).
>
> 2026-11-11: DT-002 onaylı (MUS-010…013, SYS-004/023/046/056/057 `Onaylı`; değişenler `Onaylı (DT-002)`, SOR-017 ile SYS-061/063 dahil). DT-003 (yüksek sıcaklık): MUS-014, SYS-083 `Değişti`, SYS-085…087 `Taslak`, DOG-104…108. SOR-017: MUS-015, DOG-109. DT-004: PRJ-004 ≤ 32 $.
>
> 2026-11-12 (DT-005): MUS-016 (drop-in muadil) → SYS-095 → DOG-110, DOG-111 (KRR-011); SYS-030 `Onaylı (DT-005)` APM32F405RGT6 seri / STM32F405RGT6 ALT (KRR-010) → DOG-023 (değişti), DOG-112 (yeni); SYS-042 küçük kılıf notu (DOG-041). §10 A/B kabul, C2–C6 reddedildi (SYS değişmez).
>
> 2026-11-13 (DT-006): MUS-017 (üretilebilirlik, MCU başına ayrı derleme, varyant SKU) → SYS-030, 050, 056, 058 (yeni), 095 (d) → DOG-023, -049, -050, -100, -101, -112…114, -117; KRR-012 seri AT32F435RGT7 (KRR-010 Değişti), PRJ-009 varyant SKU’ları. KRR-013 IMU LSM6DSV16X → SYS-031 (gyro ≥ 7.68 kHz), SYS-037 → DOG-024, -025, -095, -116. SYS-087 AT32 288 MHz 85 °C → DOG-107 (düzeltildi), DOG-108; SYS-042 → DOG-041, DOG-115. SOR-018 cevaplandı.

| MUS | SYS | DOG | Tasarım öğesi | Durum |
|---|---|---|---|---|
| MUS-001 | SYS-001, SYS-015, SYS-030 | DOG-001, DOG-013, DOG-014, DOG-023, DOG-112 | esc55a (4 kanal EFM8BB21 + FD6288Q), fmu U201 AT32F435RGT7 (varyant STM32F405RGT6 / APM32F405RGT6, KRR-012) | Bekliyor |
| MUS-002 | `Altium` kaynaklı: SYS-016, SYS-022, SYS-030…038, SYS-040, SYS-041, SYS-042, SYS-064, SYS-065, SYS-074 | DOG-015, DOG-016, DOG-021…036, DOG-037…042, DOG-065, DOG-066, DOG-074, DOG-075 | `boards/*/altium/`, `docs/inceleme.md` §2.1, §4.1 | Bekliyor; SYS-042 karşılamıyor (3.3 V regülatörü yok) |
| MUS-003 | SYS-045, SYS-070…075, SYS-083 | DOG-047, DOG-048, DOG-067…077, DOG-082, DOG-083 | ESC kapı aşağı çekmeleri, fmu U9 AO3401A, U1 NUF2042; Bluejay/Betaflight failsafe | Bekliyor; SYS-074 ESC kısmı SOR-010 |
| MUS-004 | SYS-003 | DOG-003 | esc65a (drawio), KRR-002 | Bekliyor |
| MUS-005 | SYS-001, SYS-010…016, SYS-020, SYS-021, SYS-022, SYS-044, SYS-063, SYS-064, SYS-081, SYS-082, SYS-084 (KRR-002 üzerinden) | DOG-001, DOG-004…022, DOG-045, DOG-046, DOG-064, DOG-065, DOG-079, DOG-080, DOG-081, DOG-084, DOG-085 | esc55a güç katı (ME7170 × 24), R00‖R000 + U2 INA199C1, D00 SMDJ28CA, fmu R95/R92 | Bekliyor; SYS-012, SYS-014, SYS-020, SYS-044 karşılamıyor (E1–E4, F4) |
| MUS-006 | SYS-035, SYS-060, SYS-061, SYS-065, SYS-080 | DOG-030, DOG-031, DOG-059, DOG-060, DOG-061, DOG-066, DOG-078 | esc55a J0, fmu J0/J1 SM08B, J2–J5, KRR-004, `docs/pin-haritasi.md` (yazılacak) | Bekliyor; dizilim doğrulanmadı (E8) |
| MUS-007 | SYS-002, SYS-030, SYS-090, SYS-091, SYS-092 (+ PRJ-003, PRJ-004 ≤ 32 $ DT-004) | DOG-002, DOG-023, DOG-086, DOG-087, DOG-088 | BOM, `docs/bom-maliyet.md` §10, `docs/rapor/mcu-secimi.md` §4.4 (STACKF435 ≈ 30.04 $; + LSM6DSV16X ≈ 31.3 $, tahmin) | Bekliyor; SYS-002 karşılanıyor (tahmin, pay ≈ 0.7 $, DT-006; 4. adımda yeniden hesap), SYS-091 karşılamıyor (F6, JW5026 RSK-019), RSK-004 azaltıldı |
| MUS-008 | SYS-030, SYS-031, SYS-036, SYS-037, SYS-050…053, SYS-055 (+ PRJ-006, KRR-003, KRR-013) | DOG-023, DOG-024, DOG-025, DOG-032…035, DOG-049…054, DOG-057, DOG-058, DOG-112, DOG-116 | `firmware/` (Betaflight config’leri STACKF435/STACKF405, Bluejay düzeni), fmu USB-C, SW80, U301 LSM6DSV16X | Bekliyor; F3, F5, §2.4 açık |
| MUS-009 | SYS-054, SYS-091, SYS-093, SYS-094 (+ PRJ-005, PRJ-007) | DOG-055, DOG-056, DOG-087, DOG-089, DOG-090 | C2/test pedleri (PCB), `test/` üretim testi | Bekliyor |
| Türetilmiş | SYS-012 (SYS-010/011), SYS-043 (SYS-040/041), SYS-062 (SYS-037/040/041/060), SYS-023 (SYS-020/037), SYS-057 (SYS-056), SYS-085 (SYS-010/083), SYS-086 (SYS-085), SYS-087 (SYS-083/043) | DOG-005, DOG-008, DOG-043, DOG-044, DOG-062, DOG-063, DOG-092, DOG-093, DOG-102, DOG-103 | Pil yolu bakırı, BEC ısısı, J0 VBAT pini | Bekliyor; SYS-012, SYS-062 karşılamıyor (tahmin) |
| MUS-010 | SYS-003, SYS-004, SYS-035, SYS-056 | DOG-003, DOG-091, DOG-030, DOG-031, DOG-100, DOG-101 | `docs/mimari-fmu.md`, fmu mekanik çizim (PCB), `docs/pazar/urun-portfoyu-yol-haritasi.md` | Bekliyor |
| MUS-011 | SYS-003, SYS-023, SYS-037, SYS-062 | DOG-003, DOG-034, DOG-035, DOG-062, DOG-063, DOG-092…096 | fmu J_ESC1/J_ESC2, PC5 CUR2 + SJ1, `docs/pin-haritasi.md` §1.3 | Bekliyor; CPU yükü RSK-014 |
| MUS-012 | SYS-003, SYS-022, SYS-044, SYS-046 | DOG-003, DOG-021, DOG-022, DOG-045, DOG-097, DOG-098 | fmu VIN ağı, VBAT 15:1, 8S BOM varyantı (`docs/mimari-fmu.md` §4.4) | Bekliyor; KRR-007 (SOR-013 seçenek 1) |
| MUS-013 | SYS-056, SYS-057 | DOG-100…103 | ArduPilot hwdef (`firmware/`, yalnız STACKF405 STM32 varyantı, DT-006), SWD pedleri | Bekliyor |
| MUS-014 | SYS-083, SYS-085, SYS-086, SYS-087 | DOG-082, DOG-083, DOG-104…108, DOG-115 | ESC/FMU BOM sıcaklık sınıfı (KRR-008), ESC güç katı ısıl modeli (guc-ip03 §2.5), FMU yerleşimi | Bekliyor (DT-003); SYS-083/086/087 karşılamıyor (EFM8BB21F16G, C_boot X5R, STM32F405RGT6) |
| MUS-015 | SYS-061, SYS-063 (+ SYS-014) | DOG-061, DOG-064, DOG-109 (+ DOG-012) | Set kondansatörü (kutu), ESC ipek baskı uyarısı, kullanıcı kılavuzu (PRJ-008) | Bekliyor |
| MUS-016 | SYS-095 (+ SYS-030 MCU varyantları, SYS-091 ilişkili; KRR-011, KRR-012) | DOG-110, DOG-111 (+ DOG-023, DOG-112) | Tüm kritik BOM satırlarında ALT MPN/ALT LCSC, ortak ayak izleri (`lib/`), firmware çoklu sürücü (baro, IMU, flash), istisna listesi | Bekliyor; ALT alanları yok, INA281B2/JW5026/EFM8BB21F16I/AT7456E/W25Q128JV muadili tanımsız (RSK-019, RSK-021); IMU LSM6DSV16X muadili tanımsız |
| MUS-017 | SYS-030, SYS-050, SYS-056, SYS-058, SYS-095 (d) (+ PRJ-006, PRJ-009; KRR-012) | DOG-023, DOG-049, DOG-050, DOG-100, DOG-101, DOG-112, DOG-113, DOG-114, DOG-117 | fmu U201 varyant BOM’ları (AT32F435RGT7 / STM32F405RGT6 / APM32F405RGT6), ipek baskı MCU işareti, `firmware/` BF config’leri (STACKF435, STACKF405, STACKF405A), INAV hedefi, AP hwdef (STM32), kutu etiketi | Bekliyor (DT-006); şematikte U201 hâlâ STM32F405RGT6, STACKF435 config ve INAV hedefi yok |

## SYS → DOG

| SYS | DOG | SYS | DOG | SYS | DOG | SYS | DOG |
|---|---|---|---|---|---|---|---|
| SYS-001 | 001 | SYS-030 | 023, 112, 117 | SYS-050 | 049, 050, 099 | SYS-072 | 070, 071 |
| SYS-002 | 002 | SYS-031 | 024, 025 | SYS-051 | 051, 052 | SYS-073 | 072, 073 |
| SYS-003 | 003 | SYS-032 | 026, 025 | SYS-052 | 053 | SYS-074 | 074, 075 |
| SYS-004 | 091 | | | | | | |
| SYS-010 | 004, 005 | SYS-033 | 027, 025 | SYS-053 | 054 | SYS-075 | 076, 077 |
| SYS-011 | 006, 007 | SYS-034 | 028, 029 | SYS-054 | 055, 056 | SYS-080 | 078 |
| SYS-012 | 008, 005 | SYS-035 | 030, 031 | SYS-055 | 057, 058 | SYS-081 | 079 |
| SYS-013 | 009, 010 | SYS-036 | 032, 033 | SYS-060 | 059, 060 | SYS-082 | 080, 081 |
| SYS-014 | 011, 012 | SYS-037 | 034, 035, 094, 095, 096, 116 | SYS-061 | 061 | SYS-083 | 082, 083 |
| SYS-015 | 013, 014 | SYS-038 | 036 | SYS-062 | 062, 063 | SYS-084 | 084, 085 |
| SYS-016 | 015, 016 | SYS-040 | 037, 038 | SYS-063 | 064, 109 | SYS-090 | 086 |
| SYS-020 | 017, 018 | SYS-041 | 039, 040 | SYS-064 | 065 | SYS-091 | 087 |
| SYS-021 | 019, 020 | SYS-042 | 041, 042, 115 | SYS-065 | 066 | SYS-092 | 088 |
| SYS-022 | 021, 022 | SYS-043 | 043, 044 | SYS-070 | 067, 068 | SYS-093 | 089 |
| | | SYS-044 | 045, 046, 012, 097 | SYS-071 | 069 | SYS-094 | 090 |
| | | | | | | SYS-095 | 110, 111 |
| SYS-023 | 092, 093 | SYS-045 | 047, 048 | SYS-056 | 100, 101 | | |
| | | SYS-046 | 097, 098 | SYS-057 | 102, 103 | SYS-085 | 104, 105 |
| | | | | SYS-058 | 113, 114 | | |
| | | | | | | SYS-086 | 105, 106 |
| | | | | | | SYS-087 | 107, 108 |

## Kapsam özeti (2026-11-13)

| | Sayı |
|---|---|
| MUS | 17 (MUS-001…017), hepsi Onaylı (MUS-017 yeni, DT-006) |
| SYS | 66: Onaylı 46 (SYS-058 yeni dahil), Onaylı (DT-002) 10 (SYS-002 ayrıca DT-004; SYS-042 DT-005 notu), Onaylı (DT-006) 7 (SYS-030, 031, 037, 050, 056, 087, 095), Değişti (DT-003) 1 (SYS-083), Taslak (DT-003) 2 (SYS-085, 086); Z 47, Ö 17, İ 2 |
| SYS alt sistem (birden çok olabilir) | SİS 10, ESC 20, FMU 20, GÜÇ 11, YAZ 12, ARA 8, MEK 7 |
| PRJ | 9 (PRJ-001…009; PRJ-006 Onaylı (DT-006), PRJ-009 varyant SKU’ları yeni) |
| KRR | KRR-001…013; KRR-010 Değişti (yerini KRR-012 aldı); KRR-012 (AT32F435 seri + varyantlar), KRR-013 (IMU LSM6DSV16X) Onaylı (2026-11-13); KRR-008 kural onaylı, değerler [öneri] |
| DT | DT-001…006 (DT-003 değerler doğrulanıyor; DT-005, DT-006 Onaylı) |
| DOG (Ü-öncesi / Kart) | 66 / 51 (toplam 117; DOG-098 M3 kartında), hepsi Bekliyor |
| RSK | RSK-001…026 (RSK-020 kapandı; RSK-022…026 yeni) |
| SYS’e bağlanmamış MUS | 0 |
| DOG’u olmayan SYS | 0 |
| Müşteri sorusuna bağlı | SYS-010/011/012/083/085 (SOR-015 açık, pazar analizi bekleniyor) |
| Mevcut tasarımın karşılamadığı SYS | SYS-010/011 (4 × 55 A, guc-ip03 G2), SYS-012, SYS-014, SYS-020, SYS-022 (29 V < 45 V, G15), SYS-023 (J1.1 bağlı değil), SYS-031 (U301 Tokmas yonga tanınmıyor → LSM6DSV16X), SYS-042, SYS-044, SYS-058 (INAV hedefi yok), SYS-062, SYS-083/086 (sıcaklık sınıfı), SYS-091 (JW5026 stok), SYS-095 (ALT alanları yok); SYS-030 kısmen (U201 hâlâ STM32F405RGT6, AT32 işlenecek); SYS-002 tahminen karşılanıyor (≈ 31.3 $ AT32 + LSM6DSV16X, DT-006) |
| Doğrulanamayan (veri sayfası/tasarım eksik) | SYS-013, SYS-016 (E5); SYS-037 (DMA yalnız analiz; AT32 zamanlayıcı tabanlı çift yönlü DShot denenmedi, DOG-116); SYS-051 (§2.4); SYS-054 (C2 pedi); SYS-060 (E8); SYS-086 (EFM8BB21 I sınıfı, sürücü/buck/LDO/konnektör sınıfları); FMU PCB’ye bağlı tüm MEK maddeleri (F1) |
| Sistem-mimari değerlendirmeli | SYS-095 (ortak ayak izi uygulanabilirliği), SYS-003 (ESC 8S), SYS-010, SYS-012, SYS-037 (CPU yükü F405 varyantlarında, AT32 DShot), SYS-046 (8S ayak izi), SYS-085 (ısıl zarf), SYS-087 (yığında FMU/AT32 sıcaklığı); SYS-030 kapandı (`mcu-secimi`) |
