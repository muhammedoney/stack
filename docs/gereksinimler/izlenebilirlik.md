# İzlenebilirlik

MUS → SYS → DOG → tasarım öğesi.

> 2026-11-06: Kapı 1 için ilk türetme; hepsi `Taslak`. Tasarım öğeleri: ESC `boards/esc55a/altium/`, FMU `boards/fmu/altium/` (KiCad’e taşınmadı); bulgu numaraları `docs/inceleme.md`. SYS → iş paketi önerisi `proje.md` → İş paketleri.

| MUS | SYS | DOG | Tasarım öğesi | Durum |
|---|---|---|---|---|
| MUS-001 | SYS-001, SYS-015, SYS-030 | DOG-001, DOG-013, DOG-014, DOG-023 | esc55a (4 kanal EFM8BB21 + FD6288Q), fmu U0 STM32F405 | Bekliyor |
| MUS-002 | `Altium` kaynaklı: SYS-016, SYS-022, SYS-030…038, SYS-040, SYS-041, SYS-042, SYS-064, SYS-065, SYS-074 | DOG-015, DOG-016, DOG-021…036, DOG-037…042, DOG-065, DOG-066, DOG-074, DOG-075 | `boards/*/altium/`, `docs/inceleme.md` §2.1, §4.1 | Bekliyor; SYS-042 karşılamıyor (3.3 V regülatörü yok) |
| MUS-003 | SYS-045, SYS-070…075, SYS-083 | DOG-047, DOG-048, DOG-067…077, DOG-082, DOG-083 | ESC kapı aşağı çekmeleri, fmu U9 AO3401A, U1 NUF2042; Bluejay/Betaflight failsafe | Bekliyor; SYS-074 ESC kısmı SOR-010 |
| MUS-004 | SYS-003 | DOG-003 | esc65a (drawio), KRR-002 | Bekliyor |
| MUS-005 | SYS-001, SYS-010…016, SYS-020, SYS-021, SYS-022, SYS-044, SYS-063, SYS-064, SYS-081, SYS-082, SYS-084 (KRR-002 üzerinden) | DOG-001, DOG-004…022, DOG-045, DOG-046, DOG-064, DOG-065, DOG-079, DOG-080, DOG-081, DOG-084, DOG-085 | esc55a güç katı (ME7170 × 24), R00‖R000 + U2 INA199C1, D00 SMDJ28CA, fmu R95/R92 | Bekliyor; SYS-012, SYS-014, SYS-020, SYS-044 karşılamıyor (E1–E4, F4) |
| MUS-006 | SYS-035, SYS-060, SYS-061, SYS-065, SYS-080 | DOG-030, DOG-031, DOG-059, DOG-060, DOG-061, DOG-066, DOG-078 | esc55a J0, fmu J0/J1 SM08B, J2–J5, KRR-004, `docs/pin-haritasi.md` (yazılacak) | Bekliyor; dizilim doğrulanmadı (E8) |
| MUS-007 | SYS-002, SYS-090, SYS-091, SYS-092 (+ PRJ-003, PRJ-004) | DOG-002, DOG-086, DOG-087, DOG-088 | BOM (LCSC kodsuz), `docs/bom-maliyet.md` (yazılacak) | Bekliyor; SYS-091 karşılamıyor (F6), RSK-004 |
| MUS-008 | SYS-030, SYS-031, SYS-036, SYS-037, SYS-050…053, SYS-055 (+ PRJ-006, KRR-003) | DOG-023, DOG-024, DOG-025, DOG-032…035, DOG-049…054, DOG-057, DOG-058 | `firmware/` (Betaflight config, Bluejay düzeni), fmu USB-C, SW80 | Bekliyor; F3, F5, §2.4 açık |
| MUS-009 | SYS-054, SYS-091, SYS-093, SYS-094 (+ PRJ-005, PRJ-007) | DOG-055, DOG-056, DOG-087, DOG-089, DOG-090 | C2/test pedleri (PCB), `test/` üretim testi | Bekliyor |
| Türetilmiş | SYS-012 (SYS-010/011), SYS-043 (SYS-040/041), SYS-062 (SYS-040/041/060) | DOG-005, DOG-008, DOG-043, DOG-044, DOG-062, DOG-063 | Pil yolu bakırı, BEC ısısı, J0 VBAT pini | Bekliyor; SYS-012, SYS-062 karşılamıyor (tahmin) |

## SYS → DOG

| SYS | DOG | SYS | DOG | SYS | DOG | SYS | DOG |
|---|---|---|---|---|---|---|---|
| SYS-001 | 001 | SYS-030 | 023 | SYS-050 | 049, 050 | SYS-072 | 070, 071 |
| SYS-002 | 002 | SYS-031 | 024, 025 | SYS-051 | 051, 052 | SYS-073 | 072, 073 |
| SYS-003 | 003 | SYS-032 | 026, 025 | SYS-052 | 053 | SYS-074 | 074, 075 |
| SYS-010 | 004, 005 | SYS-033 | 027, 025 | SYS-053 | 054 | SYS-075 | 076, 077 |
| SYS-011 | 006, 007 | SYS-034 | 028, 029 | SYS-054 | 055, 056 | SYS-080 | 078 |
| SYS-012 | 008, 005 | SYS-035 | 030, 031 | SYS-055 | 057, 058 | SYS-081 | 079 |
| SYS-013 | 009, 010 | SYS-036 | 032, 033 | SYS-060 | 059, 060 | SYS-082 | 080, 081 |
| SYS-014 | 011, 012 | SYS-037 | 034, 035 | SYS-061 | 061 | SYS-083 | 082, 083 |
| SYS-015 | 013, 014 | SYS-038 | 036 | SYS-062 | 062, 063 | SYS-084 | 084, 085 |
| SYS-016 | 015, 016 | SYS-040 | 037, 038 | SYS-063 | 064 | SYS-090 | 086 |
| SYS-020 | 017, 018 | SYS-041 | 039, 040 | SYS-064 | 065 | SYS-091 | 087 |
| SYS-021 | 019, 020 | SYS-042 | 041, 042 | SYS-065 | 066 | SYS-092 | 088 |
| SYS-022 | 021, 022 | SYS-043 | 043, 044 | SYS-070 | 067, 068 | SYS-093 | 089 |
| | | SYS-044 | 045, 046, 012 | SYS-071 | 069 | SYS-094 | 090 |
| | | SYS-045 | 047, 048 | | | | |

## Kapsam özeti

| | Sayı |
|---|---|
| MUS (taslak / onaylı) | 9 / 0 |
| SYS (taslak / onaylı) | 56 / 0 — Z 40, Ö 15, İ 1 |
| SYS alt sistem (birden çok olabilir) | SİS 8, ESC 18, FMU 15, GÜÇ 10, YAZ 9, ARA 8, MEK 5 |
| PRJ | 7 (PRJ-001…007) |
| DOG (Ü-öncesi / Kart) | 53 / 37 (toplam 90), hepsi Bekliyor |
| SYS’e bağlanmamış MUS | 0 |
| DOG’u olmayan SYS | 0 |
| TBD (müşteri sorusu) | SYS-034 (SOR-012), SYS-061 (SOR-011), SYS-074 ESC kısmı (SOR-010) |
| Mevcut tasarımın karşılamadığı SYS | SYS-012 (pil yolu/shunt, E2), SYS-014 (geçici payı, E3/E4), **SYS-020 (akım ölçümü 32 A’da doyuyor, E1)**, SYS-042 (FMU 3.3 V regülatörü yok), SYS-044 (FMU girişi 28 V, F4), SYS-062 (VBAT pini akımı, tahmin), SYS-091 (LCSC kodu yok) |
| Doğrulanamayan (veri sayfası/tasarım eksik) | SYS-010, SYS-011, SYS-013, SYS-016 (E5); SYS-037 (F5); SYS-051 (§2.4); SYS-054 (C2 pedi); SYS-060 (E8); FMU PCB’ye bağlı tüm MEK maddeleri (F1) |
| Sistem-mimari değerlendirmeli | SYS-003, SYS-010, SYS-012, SYS-062 |
