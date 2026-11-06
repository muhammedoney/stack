# Changelog

## 2026-11-06 — Kapı 1 taslağı ve maliyet çalışması

- `docs/gereksinimler/`: 5" stack için SYS-001…094 (56 madde), DOG-001…090 (53 Ü-öncesi, 37 Kart), RSK-006…013, İP-01…11 (öneri), SOR-010…012; izlenebilirlikte yetim MUS ve DOG’suz SYS yok. Yeni bulgular: fmu’da 3.3 V regülatörü yok (SYS-042), FMU beslemesi tek SH pininden (SYS-062).
- `docs/bom-maliyet.md`, `boards/*/bom-maliyet.csv`: JLC/LCSC fiyatlarıyla (2026-11-06) stack 100 sette 31.9 $ (stoklu muadillerle), ekip sadeleştirmesiyle 27.4 $, her özellik kesilse 19.5 $; 5 set prototip 80.2 $/stack. PRJ-004 (≤ 15 $) karşılanmıyor (RSK-004). ME7170 ve FD6288Q stok sorunu → AON6354 / JSM6288Q muadilleri.

## 2026-11-06 — Pazar analizi ve ilk kararlar

- Yeni ajan `pazar-analisti` (`docs/pazar-analizi.md`, `docs/pazar/` sahibi); rakip/satış fiyatı işi `bom-tedarik`ten ayrıldı.
- `docs/pazar-analizi.md` + `docs/pazar/rakipler.csv`: 16 stack/ESC; 5" standart 55–60 A, 3–6S; 7"–10" 65–80 A, 3–8S; fiyat bantları 45–57 / 70–100 / 110–210 $; Bluejay/AM32 eğilimi; 8 pin dizilimi standart değil.
- Müşteri cevapları SOR-001…004 (hobi, sertifika yok; 5"/7"/10", önce 5"; bazı sistemlerle uyum) → MUS-003…006, PRJ-002, PRJ-003 [öneri].
- Müşteri cevapları SOR-005/006/008: satış ~70 $, toplam maliyet ≤ 15 $/stack (PRJ-004, RSK-004), hazır Betaflight (PRJ-006), ilk prototip 5 set, sonra 100 set (PRJ-005, PRJ-007, RSK-005). SOR-009: 15 $ komponent + PCB + dizgi, gümrük ve kargo hariç.
- Ekip kararları (müşteri yetkisiyle): KRR-002 ilk ESC 55 A / 70 A, 3–6S; KRR-003 Bluejay + çift yönlü DShot; KRR-004 SpeedyBee F405 V4 / GEPRC Taker dizilimi, 30.5 mm.

## 2026-11-06 — Proje kuruldu

- `../cezeri/us/` altından esc55a, esc65a ve fmu kopyalandı: Altium projeleri `boards/esc55a/altium/`, `boards/fmu/altium/`; drawio çizimleri `docs/`; veri sayfaları `lib/datasheet/`; FMU görselleri `docs/reference/fmu/`. Eşleme tablosu `docs/inceleme.md` §1.
- Fiber/gofret düzeni: `CLAUDE.md` (yönetici iş akışı, müşteri kapıları, dosya sahipliği), `.claude/agents/` altında 9 ajan (gereksinim, sistem mimarı, şematik, PCB, güç elektroniği, gömülü yazılım, doğrulama-kalite, BOM-tedarik, test). `.gitignore` yalnız `.claude/agents/`’ı izliyor.
- İlk inceleme `docs/inceleme.md`: esc55a (4 katman, 30.5 mm, yollu; akım ölçümü ≈ 32 A’da doyuyor, shunt gücü, TVS/kondansatör payı), esc65a (yalnız fotoğraf), fmu (şematik var, PCB yok; çift referanslar). İnceleme betikleri `tools/altium_sch_dump.py`, `tools/pcb_stat.py`, `tools/drawio_dump.py`.
- `docs/gereksinimler/` iskeleti ve ilk müşteri soruları (SOR-001…).
