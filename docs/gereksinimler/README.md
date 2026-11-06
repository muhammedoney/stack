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
