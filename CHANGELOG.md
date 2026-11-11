# Changelog

## 2026-11-13 — Crow PCB ipek logosu

- `tools/crow_logo_pcb.py` yeniden yazıldı: piksel izleme yerine temiz vektör gaga işareti; gaga içine oyulmuş CROW kaldırıldı (6–8 mm’de basılmıyordu). KiCad ayak izleri `lib/stack.pretty/Crow_Logo_{6,8}mm`, `Crow_Logo_Text_{6,8}mm` (yazı ayrı stroke metin, JLC sınırları içinde); önizleme KiCad’in kendi çıktısından.

## 2026-11-13 — Seri MCU AT32F435, muadil kuralı, hedef BOM şematiklerde

- Müşteri: tasarım değişmeden takılabilen muadil (SYS-095, KRR-011); seri MCU AT32F435RGT7, STM32F405/APM32F405 aynı PCB’de varyant (DT-006, KRR-012, PRJ-009 SKU’lar); IMU LSM6DSV16X (KRR-013); MCU başına ayrı derleme kabul.
- İncelemeler: `docs/rapor/guc-tasarruf.md` (RSA240C, SCT2400, TLV62569 3.3 V buck, USB yük anahtarı), `docs/rapor/yazilim-inceleme.md` (Bluejay düzen C, Tokmas IMU uyumsuz), `docs/rapor/mcu-secimi.md`.
- `docs/muadil.md`: 32 kritik parça, 25 koşulsuz drop-in ALT, 4 istisna (EFM8BB21F16I, AT32F435, AT7456E, SY8303), peşin alım ≈ 1587 $. Hedef BOM `boards/*/bom-hedef.csv`, `docs/bom-maliyet.md` §11.
- Şematikler hedef BOM’da: ESC (`tools/esc55a_revb.py`) ERC 0 hata, BOM ↔ CSV farkı 0; FMU (`tools/fmu_schematic.py`) ERC 0, pin haritası 64/64. Stack STACKF435 ≈ 29.8–30.0 $ (100 set).
- Açık: ESC’de Altium’dan kalan C1/C01, R0/R00 referans çakışması (PCB güncellemesinden önce düzeltilmeli).

## 2026-11-11 — Tasarruf taraması

- `docs/bom-maliyet.md` §10, `boards/tasarruf-2026-11-11.csv`: A (güvenli) −0.61 $, B (inceleme gerekir; SPA06-003 baro −2.30 $, INA281B2 −0.52 $ …) → A + B = 31.35 $/stack (MCU JLC fiyatıyla). Dış tedarik STM32F405 fiyatıyla ~33.7 $; C1 APM32F405 ile 29.97 $. Yeni risk: ESC JW5026 stoğu 132.

## 2026-11-11 — FMU sıcaklık istisnası, QN3109 analizi

- Müşteri: FMU 105 °C kuralından çıkarıldı (SYS-087, KRR-008); ESC kuralı aynı. FMU: STM32F405RGT6, W25Q128JVSIQ (ArduPilot flash sorunu kapandı); FMU 17.72 $, stack 34.92 $ (≤ 32 $’ı 2.9 $ aşıyor, RSK-004). `tools/fmu_bom.py`, `tools/jlc.py` repoya alındı.
- `docs/rapor/qn3109-analiz.md`: Mamba F55 / GEPRC’deki QN3109 (UBIQ, 30 V, 1.35 mΩ) 4 kanal sürekli 55 A veremez (≈ 35–39 A @ 5 m/s; 4 × 55 A ≈ 10 s); bizim BLP016 ile aynı ısıl sınıf. Veri sayfası `lib/datasheet/UBIQ-QN3109M6N.pdf`.

## 2026-11-11 — F405 FMU şematiği (İP-05)

- `tools/fmu_schematic.py`: M1 F405 FMU şematiği sıfırdan, 5 alt sayfa (power, mcu, sensors, osd, io); STM32F405RGT7, ICM-42688-P, DPS368, GD25Q128, AT7456E, SY8303 × 2 (5 V/2 A, 9 V/1.5 A), AMS1117-3.3, AO3401A ters kutup (doğru yön), J_ESC1 + J_ESC2 (Dual SKU, DNP), SBUS evirici, USB-C + USBLC6. Referanslardan dosya kopyalanmadı (KRR-006); yeni semboller `lib/stack.kicad_sym`, ayak izleri `lib/stack.pretty/` (KiCad standart kopyaları).
- ERC 0 ihlal; MCU pinleri `docs/pin-haritasi.md` §1 ile 64/64 aynı (`tools/pinmap_check.py`); betik idempotent.
- BOM `boards/fmu/bom-revb.csv`: FMU 27.06 $/kart (RGT7 13.03 $, stok 4) → stack 44.26 $; RGT6 ile 35.81 $. ≤ 32 $ hedefi tutmuyor, müşteri kararı bekliyor.

## 2026-11-11 — Müşteri kararları, yüksek sıcaklık, 55 A etiketi

- Müşteri: DT-002 onaylı; DT-004 maliyet hedefi ≤ 32 $/stack; kutuda silindirik düşük ESR kondansatör kesin (SYS-061/063); tasarım kapalı, açık belge (KRR-009, PRJ-008); 8S: M1 3–6S, PCB 8S varyantına yer (KRR-007).
- DT-003 yüksek sıcaklık (SYS-085…087, KRR-008): ESC parçaları ≥ 125 °C, FMU ≥ 105 °C, X5R yasak.
- esc55a: EFM8BB21F16I (125 °C), X5R → X7R (C02, C03, C07, 16 × 1 µF), C06 BOM’a; ERC 0 hata, netlist aynı (`tools/esc55a_revb.py`). ESC 17.20 $, stack ~32.17 $ (≤ 32 $’ı 0.17 $ aşıyor; MOSFET peşin alımıyla 31.96 $). J0 SH konnektörü 85 °C, açık.
- Pazar: “55 A” etiketi analizi (`docs/pazar-analizi.md` §8, `docs/pazar/esc-akim-etiketleri.csv`): ad = kanal başına süresi belirtilmemiş sürekli değer; 4 kanal birlikte değeri hiçbir rakip vermiyor. SOR-015 açık.

## 2026-11-10 — ESC şematik Rev B, F405 referansları, DT-002

- İP-03 güç analizi (`docs/rapor/guc-ip03.md`): 40 V MOSFET, JSM6288Q1 (UVLO), 0.1 mΩ + INA240 akım ölçümü, SMDJ24CA + 15 × 10 µF 50 V, FMU SY8303 × 2 + AMS1117; 4 × 55 A sürekli ısıl olarak tutmuyor. `docs/inceleme.md` düzeltmesi: INA199C1 kazancı 50 (tam ölçek ~124 A), FMU VBAT bölücüsü 29 V.
- esc55a şematik Rev B (`tools/esc55a_revb.py`, `tools/sch_edit.py`): G1, G3–G6, G11–G14, E6 uygulandı; tüm parçalarda LCSC/MPN; ERC 0 hata, 2 uyarı. PCB güncellenmedi (senkron notu `boards/esc55a/README.md`). Yeni semboller/ayak izleri `lib/`, `lib/stack.pretty/`.
- ESC Rev B maliyeti (`docs/bom-maliyet.md` §9, `boards/esc55a/bom-revb.csv`): ESC 16.72 $, stack ~31.7 $ (100 set); veri sayfaları `lib/datasheet/`.
- F405 referans taraması ve önerilen mimari `docs/mimari-fmu.md`; pin haritası `docs/pin-haritasi.md` (SPEEDYBEEF405V4 uyumlu, 8 motor, HSE 8 MHz).
- DT-002 (müşteri onayı bekliyor): FMU gereksinimleri hedef ürün ailesine göre (M3 8S, M4a 8 motor, ArduPilot); SYS 61, DOG 103; KRR-005…007 öneri; SOR-013…017.

## 2026-11-06 — Kapı 1 onayı

- Müşteri gereksinimleri onayladı: SYS-001…094, MUS, PRJ `Onaylı`. DT-001: maliyet hedefi 15 $ → ≤ 28 $/stack (100 set, tüm özellikler). SOR-010: ESC’de ters kutup koruması yok, + / − ipek baskı ve uyarı. SOR-011: kutuda 8 pin kablo, düşük ESR kondansatör, M3 tampon/vida. SOR-012: analog OSD kesin (SYS-034 zorunlu).
- İş paketleri İP-01…11 açıldı.

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
