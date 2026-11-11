# Gereksinimler

Müşteri ihtiyacından doğrulamaya kadar izlenebilir gereksinim kaydı. Sahibi `gereksinim-muhendisi`; süreç kökteki `CLAUDE.md`’de.

## Dosyalar

| Dosya | Önek | İçerik |
|---|---|---|
| [musteri.md](musteri.md) | `MUS-` | Müşteri ihtiyaçları: müşterinin dilinde, ne ve neden |
| [sistem.md](sistem.md) | `SYS-` | Sistem gereksinimleri: ölçülebilir, alt sisteme atanmış |
| [proje.md](proje.md) | `PRJ-`, `RSK-`, `DT-`, `IP-` | Proje gereksinimleri (maliyet, takvim, adet, üretim, sertifika), riskler, değişiklik talepleri ve etki analizi, iş paketleri |
| [dogrulama.md](dogrulama.md) | `DOG-` | Her SYS için doğrulama yöntemi, ölçüt, aşama, sonuç |
| [izlenebilirlik.md](izlenebilirlik.md) | — | MUS → SYS → DOG → tasarım öğesi matrisi |
| [kararlar.md](kararlar.md) | `KRR-` | Tasarım kararları: seçenekler, gerekçe, etki |
| [sorular.md](sorular.md) | `SOR-` | Müşteriye sorulacak / sorulmuş açık noktalar |

## Kurallar

- Numara bir kez verilir, silinmez; iptal edilen madde `İptal` durumuna alınır.
- Durum: `Taslak` → `Onaylı` → (`Değişti` → `Onaylı`) / `İptal`; sonraki sürüme bırakılan madde `Ertelendi`.
- Her SYS iyi yazılmış olmalı: tek şey, ölçülebilir (değer + birim + koşul), doğrulanabilir, uygulanabilir, çözümden bağımsız (gerekmedikçe).
- Her SYS en az bir MUS’a (veya `Türetilmiş: KRR-/SYS-` gerekçesine) ve en az bir DOG’a bağlı olmalı.
- Doğrulama yöntemi: **A** analiz/hesap, **S** simülasyon, **M** muayene (şematik/PCB/BOM inceleme), **G** gösterim, **T** test (ölçüm).
- Doğrulama aşaması: **Ü-öncesi** (kart üretilmeden yapılabilir) veya **Kart** (donanım gerekir).
- Öncelik: **Z** zorunlu, **Ö** önemli, **İ** iyi olur.
- Değeri henüz belli olmayan yer `TBD (SOR-xxx)` yazılır; ekibin önerdiği ama müşterinin onaylamadığı değer `[öneri]` diye işaretlenir.
- Kaynak `Altium` = cezeri’den gelen mevcut tasarımdan geri çıkarıldı; müşteri onayına kadar `Taslak`.
- Onaylı maddede kalan `[öneri]` değer kapı 1’de ekip hedefi olarak kabul edilmiştir; değiştirmek değişiklik talebi (DT) ister.

## Durum (2026-11-06)

Kapı 1’e hazır taslak (5" stack: fmu + esc55a). Hepsi `Taslak`, müşteri onayı bekliyor.

| | Durum |
|---|---|
| MUS | MUS-001…009 (9) |
| SYS | SYS-001…094 (56; Z 40, Ö 15, İ 1) — `sistem.md` |
| DOG | DOG-001…090 (90; Ü-öncesi 53, Kart 37) — `dogrulama.md` |
| PRJ / KRR | PRJ-001…007; KRR-001…004 |
| RSK | RSK-001…013 (RSK-006…013 yeni) |
| İP | İP-01…11 (Öneri) — `proje.md` |
| Açık soru | SOR-010 (ESC ters kutup), SOR-011 (kutu içeriği), SOR-012 (analog OSD) |
| Mevcut tasarımın karşılamadığı | SYS-012, SYS-014, SYS-020 (kritik, E1), SYS-042, SYS-044, SYS-062, SYS-091 — `izlenebilirlik.md` kapsam özeti |

**Kapı 1 (2026-11-06):** müşteri onayladı. SYS-001…094 ve MUS/PRJ `Onaylı`; DT-001 maliyet hedefi ≤ 28 $/stack; SOR-010…012 cevaplandı. İş paketleri İP-01…11 açık.

## Durum (2026-11-10) — DT-002 (2026-11-11’de onaylandı)

FMU (M1 F405) gereksinimleri yol haritasındaki hedef ürünlere göre güncellendi (müşteri: “F405 için gereksinimleri hedef ürünü göz önüne alarak yap”). Etki analizi `proje.md` → DT-002.

| | Durum |
|---|---|
| MUS | MUS-001…013 (13; Onaylı 9, Taslak 4: MUS-010…013) |
| SYS | 61 (Onaylı 46, **Değişti 10**: SYS-002, 003, 022, 035, 037, 042, 044, 050, 055, 062; **Taslak 5**: SYS-004, 023, 046, 056, 057); Z 41, Ö 18, İ 2 |
| DOG | DOG-001…103 (Ü-öncesi 59, Kart 44); değişen 13, yeni DOG-091…103 |
| KRR | KRR-001…004; **öneri** KRR-005 (pin haritası SPEEDYBEEF405V4), KRR-006 (referans kullanım kuralı), KRR-007 (8S stratejisi) |
| RSK | RSK-001…016 (RSK-014…016 yeni) |
| Açık soru (şimdi sorulacak, sırayla) | SOR-013 8S stratejisi, SOR-015 “55 A” tanımı, SOR-016 maliyet ≤ 32 $, SOR-017 pil kondansatörü zorunlu, SOR-014 açık kaynak |

## Durum (2026-11-11) — DT-002 onaylı; DT-003 yüksek sıcaklık; DT-004 ≤ 32 $

Müşteri SOR-013, 014, 016, 017’yi cevapladı, DT-002’ye itiraz yok → DT-002 onaylı. Yeni talep: “Kart yüksek derecelere çıkar. Ona göre komponentleri güncelle.” (DT-003). Etki analizleri `proje.md`.

| | Durum |
|---|---|
| MUS | MUS-001…015 (15), hepsi Onaylı; yeni MUS-014 (yüksek sıcaklık), MUS-015 (kutuda silindirik kondansatör zorunlu) |
| SYS | 64: Onaylı 48, Onaylı (DT-002) 12, **Değişti (DT-003)** SYS-083, **Taslak (DT-003)** SYS-085 (ESC ısıl zarfı), SYS-086 (ESC parça ≥ 125 °C), SYS-087 (FMU parça ≥ 105 °C, STM32F405RGT7); Z 45, Ö 17, İ 2 |
| DOG | DOG-001…109 (Ü-öncesi 63, Kart 46); değişen DOG-002, -061, -064, -082; yeni DOG-104…109 |
| PRJ | PRJ-001…008; PRJ-004 ≤ 32 $ (DT-004), PRJ-008 açık belge / kapalı tasarım |
| KRR | KRR-005, 006, 007 Onaylı; yeni KRR-008 (sıcaklık sınıfı kuralı, değerler [öneri]), KRR-009 (tasarım kapalı, açık belge) Onaylı |
| RSK | RSK-001…018 (RSK-004 güncellendi: pay 0.31 $; RSK-017 parça bulunabilirliği, RSK-018 FMU 85 °C sensörler) |
| DT | DT-001 (DT-004 ile güncellendi), DT-002 Onaylı, DT-003 (ihtiyaç onaylı, değerler doğrulanıyor), DT-004 Onaylı |
| Açık soru | SOR-015 “55 A” tanımı — `pazar-analisti` rakip etiketlerini analiz ediyor; SYS-010/011 değişmez, cevapla yeni DT |
| Doğrulama bekleyen (ekip) | EFM8BB21 125 °C (I) sınıfı ve LCSC stoğu; STM32F405RGT7 fiyat/stok; ESC sürücü/buck/LDO/SH konnektör sınıfları; FMU 85 °C istisna listesi; DT-003 fark maliyeti (≤ 32 $ içinde mi) |

## Durum (2026-11-12) — DT-005 seri üretim tedarik ve maliyet kararları (Onaylı)

Müşteri `docs/bom-maliyet.md` §10 tasarruf taramasına karar verdi ve muadil talebi getirdi. Etki analizi `proje.md` → DT-005.

| | Durum |
|---|---|
| MUS | 16; yeni **MUS-016** (kritik parçalarda tasarım değişmeden takılabilen muadil), Onaylı |
| SYS | 65: Onaylı 49, Onaylı (DT-002) 12, Onaylı (DT-005) 1, Değişti (DT-003) 1, Taslak (DT-003) 2; Z 46, Ö 17, İ 2. **Değişti → Onaylı (DT-005):** SYS-030 (APM32F405RGT6 seri, STM32F405RGT6 drop-in muadil). **Yeni:** SYS-095 (drop-in muadil kuralı, Z). **Not:** SYS-042 (3.3 V regülatörü küçük kılıf, SOT-223 değil [öneri]) |
| DOG | DOG-001…112 (Ü-öncesi 64, Kart 48); değişen DOG-023, -041, -100, -101; yeni DOG-110 (muadil BOM muayenesi), DOG-111 (muadil takılı prototip), DOG-112 (APM32 kartında BF + AP + DFU) |
| PRJ | PRJ-004 ≤ 32 $: A + B (B1–B6) + APM32 ≈ 29.97 $/stack → karşılanıyor (tahmin) |
| KRR | yeni KRR-010 (APM32F405 seri MCU; maliyet ve tedarik), KRR-011 (muadil uygulama kuralı) Onaylı |
| RSK | RSK-004 Azaltıldı; RSK-017 güncellendi; yeni RSK-019 (JW5026 stok 132 < 2 × 400), RSK-020 (APM32: ArduPilot desteği / ayrı yazılım derlemesi), RSK-021 (muadili olmayan kritik parçalar) |
| §10 kararları | A1–A7, B1–B6 kabul, gereksinim değişmez (B1 SPA06-003 → `gomulu-yazilim` + `pcb-muhendisi`; B2 INA281B2 → `guc-elektronigi` + `gomulu-yazilim`; B3–B6 → `guc-elektronigi`); A2 (SOT-223 AMS1117) küçük kılıf notuyla geçersiz; C1 kabul (DT-005); **C2–C6 reddedildi** (SYS-021, 031, 032, 033, 056 değişmez) |
| Açık soru | SOR-015 (“55 A” tanımı, pazar analizi); SOR-018 koşullu (APM32/STM32 tek yazılım imajı ve ArduPilot desteği — `gomulu-yazilim` DOG-023 sonucu olumsuzsa sorulur) |
| Doğrulama bekleyen (ekip) | `gomulu-yazilim`: BF/AP APM32F405 desteği, baro iki sürücü (SPA06/DPS368), `ibata_scale`; `guc-elektronigi`: B2–B6, küçük kılıf LDO + ALT, JW5026 muadil çifti; `bom-tedarik`: ALT MPN/LCSC sütunları ve istisna listesi (DOG-110); `sematik-muhendisi`: APM32/STM32 pin tablosu farkları |
