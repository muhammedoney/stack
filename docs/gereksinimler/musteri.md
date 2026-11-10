# Müşteri ihtiyaçları (MUS)

| ID | İhtiyaç (müşterinin dilinde) | Neden | Kaynak | Öncelik | Durum |
|---|---|---|---|---|---|
| MUS-001 | FPV dronlar için uçuş kontrol kartı (FMU) ve ESC kartları yapılacak | Ürün ailesi | Müşteri, 2026-11-06 | Z | Onaylı |
| MUS-002 | Mevcut çalışmalar (esc55a, esc65a, fmu) başlangıç noktası olacak | Önceki emek korunur | Müşteri, 2026-11-06 | Ö | Onaylı |
| MUS-003 | Hobi FPV kullanıcısı için; sertifika gerekmez | Hedef kitle | SOR-001, 2026-11-06 | Z | Onaylı |
| MUS-004 | 5", 7" ve 10" dronlarda kullanılacak; daha büyükler ileride | Ürün ailesi | SOR-002, 2026-11-06 | Z | Onaylı |
| MUS-005 | Önce 5" için; akım sınıfı pazara göre belirlenecek | Öncelik | SOR-002, 2026-11-06 | Z | Onaylı |
| MUS-006 | Piyasadaki bazı FMU/ESC’lerle takılabilmeli (hepsiyle değil) | Kullanıcı mevcut parçasını kullanabilsin | SOR-004, 2026-11-06 | Ö | Onaylı |
| MUS-007 | Satış ~70 $/stack; toplam maliyet ≤ 15 $ olursa kâr edilir | Kârlılık; gümrük ve kargo hariç (SOR-009) | SOR-005, 2026-11-06 | Z | Onaylı |
| MUS-008 | Hazır Betaflight yeterli | Yazılım emeği yok | SOR-006, 2026-11-06 | Ö | Onaylı |
| MUS-009 | İlk prototip en kısa sürede 5 set, sonra 100 set | Pazara çıkış | SOR-008, 2026-11-06 | Z | Onaylı |
| MUS-010 | Ürünler müşterinin km taşı sırasıyla gelişecek (M1 F405 stack → M2 yüksek akım ESC → M3 8S set → M4 F7 FMU / M4a Dual-ESC FMU → M5 H7, BF + INAV + ArduPilot …); F405 gereksinimleri bu hedef ürünler göz önüne alınarak yazılsın | M1’de verilen kararlar sonraki ürünleri kilitlemesin; aynı PCB/konnektör yeniden kullanılsın | Müşteri, 2026-11-10 (yol haritası K2; “F405 için gereksinimleri hedef ürünü göz önüne alarak yap”) | Z | Taslak (DT-002) |
| MUS-011 | Bir FMU iki adet 4’ü 1 arada ESC bağlayıp 8 motor sürebilmeli; ayrı ürün (SKU) olarak satılacak | Yüksek itki, X-class, 7–10" ağır dronlar | Müşteri, 2026-11-10 (K10) | Ö | Taslak (DT-002) |
| MUS-012 | 7"/10" için 8S FMU olacak (M3, 8S ESC ve GPS ile “Long Range set”) | Uzun menzil / ağır sınıf | Müşteri, 2026-11-10 (K4) | Ö | Taslak (DT-002) |
| MUS-013 | ArduPilot ailede olacak (M5’te BF + INAV + ArduPilot kesin); F405’te kısıtlı ArduPilot fırsatı değerlendirilsin | Kullanıcı tabanı genişler, “aynı kart üç yazılım” pazarlaması | Müşteri, 2026-11-10 (K6); F405 kısmı ekip önerisi (`docs/pazar/urun-portfoyu-yol-haritasi.md` §F) | İ | Taslak (DT-002) |
