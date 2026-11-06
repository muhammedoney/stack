# Proje gereksinimleri, riskler, iş paketleri

## Proje gereksinimleri (PRJ)

| ID | Gereksinim | Kaynak | Öncelik | Durum |
|---|---|---|---|---|
| PRJ-001 | Tasarım KiCad 10’da; tüm belgeler Türkçe ve repoda; dosya düzeni fiber/gofret projeleriyle aynı | Müşteri, 2026-11-06 | Z | Taslak |
| PRJ-002 | Hobi ürünü: sertifika (CE/FCC vb.) hedeflenmez | MUS-003 | Z | Taslak |
| PRJ-003 | Hedef satış fiyatı ≤ 70 $/stack (pazar: bütçe markalar 70–100 $, AliExpress 45–57 $) | SOR-005, `docs/pazar-analizi.md` §6 | Ö | Taslak (müşteri uygun buldu, 2026-11-06) |
| PRJ-004 | Stack (FMU + 55 A ESC) toplam maliyeti ≤ 15 $, 100 set kademesinde; kapsam TBD (SOR-009, varsayım: komponent + PCB + dizgi). Her parça seçiminde maliyet etkisi yazılır | SOR-005 | Z | Taslak |
| PRJ-005 | İlk üretim: en kısa sürede 100 set | SOR-008 | Z | Taslak |
| PRJ-006 | Yazılım: FMU’da hazır Betaflight, ESC’de Bluejay; yalnız hedef/düzen tanımı ve yükleme yolu bizden | SOR-006, KRR-003 | Z | Taslak |

## Riskler (RSK)

| ID | Risk | Olasılık | Etki | Önlem | Durum |
|---|---|---|---|---|---|
| RSK-001 | esc55a akım ölçümü ≈ 32 A’da doyuyor, shunt 100 A’da ≈ 5 W (inceleme E1, E2) | Yüksek | Akım okuması ve shunt ısısı | Akım sınıfı netleşince yeniden boyutlandırma | Açık |
| RSK-002 | Güç parçalarının (ME7170, JW5026) veri sayfası yok; 55 A sınıfı doğrulanamıyor (E5) | Orta | Yeniden parça seçimi | `bom-tedarik` veri sayfalarını bulur | Açık |
| RSK-003 | esc65a için yalnız fotoğraf var | Yüksek | Takvim | esc55a tabanlı varyant değerlendirmesi (SOR-003) | Açık |
| RSK-004 | 15 $/stack maliyet hedefi agresif: ESC’de 24 MOSFET + 4 MCU + 4 sürücü, FMU’da F405 + IMU + OSD; AliExpress perakende 45–57 $ (tahmin, BOM fiyatlanmadı) | Yüksek | Kâr / parça kalitesi | `bom-tedarik` 100 set BOM fiyatı; gereksiz parça ayıklama; PCB+dizgi kapsamı SOR-009 | Açık |
| RSK-005 | 100 set ilk parti tasarım doğrulanmadan üretilirse toplu hata riski | Orta | 100 set hurda | Ü-öncesi DOG’lar kapanmadan üretim yok; önerilen ara adım: 5–10 set ön seri | Açık |

## Değişiklik talepleri (DT)

| ID | Talep | Etkilenen | Durum |
|---|---|---|---|

## İş paketleri (İP)

| ID | Paket | Sahip | SYS | Durum |
|---|---|---|---|---|
