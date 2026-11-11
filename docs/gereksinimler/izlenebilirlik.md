# İzlenebilirlik

MUS → SYS → DOG → tasarım öğesi.

> 2026-11-06: Kapı 1 için ilk türetme; kapı 1’de `Onaylı`. Tasarım öğeleri: ESC `boards/esc55a/altium/`, FMU `boards/fmu/altium/` (KiCad’e taşınmadı); bulgu numaraları `docs/inceleme.md`. SYS → iş paketi önerisi `proje.md` → İş paketleri.
>
> 2026-11-10 (DT-002; müşteri onayı 2026-11-11): MUS-010…013, SYS-004/023/046/056/057 (Taslak), SYS-002/003/022/035/037/042/044/050/055/062 (Değişti), DOG-091…103 eklendi. FMU tasarım öğesi artık `docs/mimari-fmu.md` + `docs/pin-haritasi.md` (Altium fmu yalnız karşılaştırma).
>
> 2026-11-11: DT-002 onaylı (MUS-010…013, SYS-004/023/046/056/057 `Onaylı`; değişenler `Onaylı (DT-002)`, SOR-017 ile SYS-061/063 dahil). DT-003 (yüksek sıcaklık): MUS-014, SYS-083 `Değişti`, SYS-085…087 `Taslak`, DOG-104…108. SOR-017: MUS-015, DOG-109. DT-004: PRJ-004 ≤ 32 $.

| MUS | SYS | DOG | Tasarım öğesi | Durum |
|---|---|---|---|---|
| MUS-001 | SYS-001, SYS-015, SYS-030 | DOG-001, DOG-013, DOG-014, DOG-023 | esc55a (4 kanal EFM8BB21 + FD6288Q), fmu U0 STM32F405 | Bekliyor |
| MUS-002 | `Altium` kaynaklı: SYS-016, SYS-022, SYS-030…038, SYS-040, SYS-041, SYS-042, SYS-064, SYS-065, SYS-074 | DOG-015, DOG-016, DOG-021…036, DOG-037…042, DOG-065, DOG-066, DOG-074, DOG-075 | `boards/*/altium/`, `docs/inceleme.md` §2.1, §4.1 | Bekliyor; SYS-042 karşılamıyor (3.3 V regülatörü yok) |
| MUS-003 | SYS-045, SYS-070…075, SYS-083 | DOG-047, DOG-048, DOG-067…077, DOG-082, DOG-083 | ESC kapı aşağı çekmeleri, fmu U9 AO3401A, U1 NUF2042; Bluejay/Betaflight failsafe | Bekliyor; SYS-074 ESC kısmı SOR-010 |
| MUS-004 | SYS-003 | DOG-003 | esc65a (drawio), KRR-002 | Bekliyor |
| MUS-005 | SYS-001, SYS-010…016, SYS-020, SYS-021, SYS-022, SYS-044, SYS-063, SYS-064, SYS-081, SYS-082, SYS-084 (KRR-002 üzerinden) | DOG-001, DOG-004…022, DOG-045, DOG-046, DOG-064, DOG-065, DOG-079, DOG-080, DOG-081, DOG-084, DOG-085 | esc55a güç katı (ME7170 × 24), R00‖R000 + U2 INA199C1, D00 SMDJ28CA, fmu R95/R92 | Bekliyor; SYS-012, SYS-014, SYS-020, SYS-044 karşılamıyor (E1–E4, F4) |
| MUS-006 | SYS-035, SYS-060, SYS-061, SYS-065, SYS-080 | DOG-030, DOG-031, DOG-059, DOG-060, DOG-061, DOG-066, DOG-078 | esc55a J0, fmu J0/J1 SM08B, J2–J5, KRR-004, `docs/pin-haritasi.md` (yazılacak) | Bekliyor; dizilim doğrulanmadı (E8) |
| MUS-007 | SYS-002, SYS-090, SYS-091, SYS-092 (+ PRJ-003, PRJ-004 ≤ 32 $ DT-004) | DOG-002, DOG-086, DOG-087, DOG-088 | BOM, `docs/bom-maliyet.md` §9.4 (31.69 $) | Bekliyor; SYS-002 sınırda (pay 0.31 $), SYS-091 karşılamıyor (F6), RSK-004 |
| MUS-008 | SYS-030, SYS-031, SYS-036, SYS-037, SYS-050…053, SYS-055 (+ PRJ-006, KRR-003) | DOG-023, DOG-024, DOG-025, DOG-032…035, DOG-049…054, DOG-057, DOG-058 | `firmware/` (Betaflight config, Bluejay düzeni), fmu USB-C, SW80 | Bekliyor; F3, F5, §2.4 açık |
| MUS-009 | SYS-054, SYS-091, SYS-093, SYS-094 (+ PRJ-005, PRJ-007) | DOG-055, DOG-056, DOG-087, DOG-089, DOG-090 | C2/test pedleri (PCB), `test/` üretim testi | Bekliyor |
| Türetilmiş | SYS-012 (SYS-010/011), SYS-043 (SYS-040/041), SYS-062 (SYS-037/040/041/060), SYS-023 (SYS-020/037), SYS-057 (SYS-056), SYS-085 (SYS-010/083), SYS-086 (SYS-085), SYS-087 (SYS-083/043) | DOG-005, DOG-008, DOG-043, DOG-044, DOG-062, DOG-063, DOG-092, DOG-093, DOG-102, DOG-103 | Pil yolu bakırı, BEC ısısı, J0 VBAT pini | Bekliyor; SYS-012, SYS-062 karşılamıyor (tahmin) |
| MUS-010 | SYS-003, SYS-004, SYS-035, SYS-056 | DOG-003, DOG-091, DOG-030, DOG-031, DOG-100, DOG-101 | `docs/mimari-fmu.md`, fmu mekanik çizim (PCB), `docs/pazar/urun-portfoyu-yol-haritasi.md` | Bekliyor |
| MUS-011 | SYS-003, SYS-023, SYS-037, SYS-062 | DOG-003, DOG-034, DOG-035, DOG-062, DOG-063, DOG-092…096 | fmu J_ESC1/J_ESC2, PC5 CUR2 + SJ1, `docs/pin-haritasi.md` §1.3 | Bekliyor; CPU yükü RSK-014 |
| MUS-012 | SYS-003, SYS-022, SYS-044, SYS-046 | DOG-003, DOG-021, DOG-022, DOG-045, DOG-097, DOG-098 | fmu VIN ağı, VBAT 15:1, 8S BOM varyantı (`docs/mimari-fmu.md` §4.4) | Bekliyor; KRR-007 (SOR-013 seçenek 1) |
| MUS-013 | SYS-056, SYS-057 | DOG-100…103 | ArduPilot hwdef (`firmware/`), SWD pedleri | Bekliyor |
| MUS-014 | SYS-083, SYS-085, SYS-086, SYS-087 | DOG-082, DOG-083, DOG-104…108 | ESC/FMU BOM sıcaklık sınıfı (KRR-008), ESC güç katı ısıl modeli (guc-ip03 §2.5), FMU yerleşimi | Bekliyor (DT-003); SYS-083/086/087 karşılamıyor (EFM8BB21F16G, C_boot X5R, STM32F405RGT6) |
| MUS-015 | SYS-061, SYS-063 (+ SYS-014) | DOG-061, DOG-064, DOG-109 (+ DOG-012) | Set kondansatörü (kutu), ESC ipek baskı uyarısı, kullanıcı kılavuzu (PRJ-008) | Bekliyor |

## SYS → DOG

| SYS | DOG | SYS | DOG | SYS | DOG | SYS | DOG |
|---|---|---|---|---|---|---|---|
| SYS-001 | 001 | SYS-030 | 023 | SYS-050 | 049, 050, 099 | SYS-072 | 070, 071 |
| SYS-002 | 002 | SYS-031 | 024, 025 | SYS-051 | 051, 052 | SYS-073 | 072, 073 |
| SYS-003 | 003 | SYS-032 | 026, 025 | SYS-052 | 053 | SYS-074 | 074, 075 |
| SYS-004 | 091 | | | | | | |
| SYS-010 | 004, 005 | SYS-033 | 027, 025 | SYS-053 | 054 | SYS-075 | 076, 077 |
| SYS-011 | 006, 007 | SYS-034 | 028, 029 | SYS-054 | 055, 056 | SYS-080 | 078 |
| SYS-012 | 008, 005 | SYS-035 | 030, 031 | SYS-055 | 057, 058 | SYS-081 | 079 |
| SYS-013 | 009, 010 | SYS-036 | 032, 033 | SYS-060 | 059, 060 | SYS-082 | 080, 081 |
| SYS-014 | 011, 012 | SYS-037 | 034, 035, 094, 095, 096 | SYS-061 | 061 | SYS-083 | 082, 083 |
| SYS-015 | 013, 014 | SYS-038 | 036 | SYS-062 | 062, 063 | SYS-084 | 084, 085 |
| SYS-016 | 015, 016 | SYS-040 | 037, 038 | SYS-063 | 064, 109 | SYS-090 | 086 |
| SYS-020 | 017, 018 | SYS-041 | 039, 040 | SYS-064 | 065 | SYS-091 | 087 |
| SYS-021 | 019, 020 | SYS-042 | 041, 042 | SYS-065 | 066 | SYS-092 | 088 |
| SYS-022 | 021, 022 | SYS-043 | 043, 044 | SYS-070 | 067, 068 | SYS-093 | 089 |
| | | SYS-044 | 045, 046, 012, 097 | SYS-071 | 069 | SYS-094 | 090 |
| SYS-023 | 092, 093 | SYS-045 | 047, 048 | SYS-056 | 100, 101 | | |
| | | SYS-046 | 097, 098 | SYS-057 | 102, 103 | SYS-085 | 104, 105 |
| | | | | | | SYS-086 | 105, 106 |
| | | | | | | SYS-087 | 107, 108 |

## Kapsam özeti (2026-11-11)

| | Sayı |
|---|---|
| MUS | 15 (MUS-001…015), hepsi Onaylı (MUS-014/015 yeni, 2026-11-11) |
| SYS | 64: Onaylı 48, Onaylı (DT-002) 12 (SYS-002 ayrıca DT-004), Değişti (DT-003) 1 (SYS-083), Taslak (DT-003) 3 (SYS-085…087); Z 45, Ö 17, İ 2 |
| SYS alt sistem (birden çok olabilir) | SİS 9, ESC 20, FMU 20, GÜÇ 11, YAZ 11, ARA 8, MEK 7 |
| PRJ | 8 (PRJ-001…008; PRJ-004 DT-004 ile ≤ 32 $, PRJ-008 yeni) |
| KRR | KRR-001…009; KRR-005…007, 009 Onaylı (2026-11-11); KRR-008 kural onaylı, değerler [öneri] |
| DT | DT-001…004 (DT-003 değerler doğrulanıyor) |
| DOG (Ü-öncesi / Kart) | 63 / 46 (toplam 109; DOG-098 M3 kartında), hepsi Bekliyor |
| SYS’e bağlanmamış MUS | 0 |
| DOG’u olmayan SYS | 0 |
| Müşteri sorusuna bağlı | SYS-010/011/012/083/085 (SOR-015 açık, pazar analizi bekleniyor) |
| Mevcut tasarımın karşılamadığı SYS | SYS-010/011 (4 × 55 A, guc-ip03 G2), SYS-012, SYS-014, SYS-020, SYS-022 (29 V < 45 V, G15), SYS-023 (J1.1 bağlı değil), SYS-042, SYS-044, SYS-062, SYS-083/086/087 (sıcaklık sınıfı), SYS-091; SYS-002 sınırda (31.69 $ ≤ 32 $, DT-003 farkı eklenmedi) |
| Doğrulanamayan (veri sayfası/tasarım eksik) | SYS-013, SYS-016 (E5); SYS-037 (DMA yalnız analiz; DOG-094/095 kartta); SYS-051 (§2.4); SYS-054 (C2 pedi); SYS-060 (E8); SYS-086 (EFM8BB21 I sınıfı, sürücü/buck/LDO/konnektör sınıfları); FMU PCB’ye bağlı tüm MEK maddeleri (F1) |
| Sistem-mimari değerlendirmeli | SYS-003 (ESC 8S), SYS-010, SYS-012, SYS-037 (CPU yükü), SYS-046 (8S ayak izi), SYS-085 (ısıl zarf), SYS-087 (yığında FMU sıcaklığı) |
