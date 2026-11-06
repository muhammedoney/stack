# Pazar analizi — FPV stack (FMU + 4’ü 1 arada ESC)

Sahibi `pazar-analisti`. Tarih: 2026-11-06. Ham veri: [`pazar/rakipler.csv`](pazar/rakipler.csv). Fiyatlar USD, KDV/kargo hariç, satıcı sayfasında görülen değerler (stok ve kampanya sık değişiyor). Akım değerleri **üretici iddiası**; bağımsız test yok.

## 1. Özet

| | Bulgu |
|---|---|
| Ana segment | 5" freestyle, 3–6S, 30.5 × 30.5 mm stack. Standart ESC sınıfı **55–60 A sürekli / ~70 A anlık** |
| Fiyat bantları | AliExpress markaları **45–57 $**; bütçe markalar (SpeedyBee, GEPRC) **70–100 $**; orta/üst (iFlight, Diatone, T-Motor, HobbyWing, Holybro) **110–210 $** |
| En çok satan tip | F405 + ICM-42688-P + 8 bit BLHeli_S/Bluejay ESC (SpeedyBee F405 V4, GEPRC Taker F405 60A) |
| 7"–10" | 65–80 A, **3–8S**; F722 ağırlıklı; 85–130 $ |
| ESC yazılımı | 8 bit tarafta BLHeli_S → **Bluejay** (açık kaynak, çift yönlü DShot ile RPM). 32 bit tarafta BLHeli_32 geri çekildi → **AM32** yükseliyor |
| Konnektör | 8 pin SM08B yaygın ama **dizilim standart değil**; markalar arası kablo değişimi gerekiyor |
| Bizim esc55a | 55 A, 3–6S, 30.5 mm, EFM8BB21 + FD6288Q: segmentin tam ortasında. Eksik: akım ölçümü aralığı (inceleme E1) ve 6S geçici payı |

## 2. 5" segmenti

| Ürün | FC | ESC (sürekli / anlık) | Hücre | ESC yazılımı | Fiyat ($) | Not |
|---|---|---|---|---|---|---|
| SpeedyBee F405 V4 BLS 55A | F405, ICM-42688-P | 55 / 70 A (10 s) | 3–6S | BLHeli_S 8 bit | 70–86 | Bluetooth; 5 V + 9 V BEC toplam 3 A; ESC 23.5 g (soğutuculu) |
| SpeedyBee F405 V5 OX32 55A | F405, ICM-42688-P | 55 / 70 A | 3–6S | OX32 (32 bit) | 115–120 | 8 motor çıkışı; Deluxe 200 $ |
| GEPRC Taker F405 BLS 60A V2 | F405 (GEP-F405-HD V3), ICM-42688-P, BMP280 | 60 A | 3–6S | BLHeli_S | 72–99 | 16 MB blackbox; 14.9 g; DJI tak-çalıştır |
| HAKRC F405 V2 + 60/65A | F405 | 60–65 A | 3–6S | belirtilmemiş | 44–49 | Çift BEC; AliExpress |
| HGLRC Specter F460 60A | F405, ICM-42688-P | 60 A | 2–6S | BLHeli_S | 57 | AliExpress |
| Diatone Mamba MK2 F405 F50 | F405 | 50 A | 3–6S | BLHeli_S | 88 | fmu referansımız; eski ürün |
| iFlight BLITZ F7 E55 | F722 | 55 A | 2–6S | BLHeli_32 | 110–150 | |
| Diatone Mamba MK4 F722 / H743 F55 | F722 / H743 (çift IMU) | 55 A | 3–6S | BLHeli_32 128K | 110–119 | |
| Holybro Kakute H7 + Tekko32 65A | H743, MPU6000, BMP280 | 65 / 75 A | 4–6S | AM32 | 139–210 | Premium; ArduPilot/INAV |

**Akım ihtiyacı (5", 6S, 2207 motor):** üretici motor tepe akımları 38 A (1750 KV) – 45 A (1850 KV); 1960 KV için 40.3 A. Uçuş kaydı örneği: toplam ~120 A, motor başına ~30 A (anekdot). Pazar 5" için 55–60 A satıyor; 45 A yalnız hafif kurulumlar için öneriliyor.

## 3. 7" ve 10" segmenti

| Ürün | ESC (sürekli / anlık) | Hücre | Fiyat ($) | Not |
|---|---|---|---|---|
| GEPRC Taker F722 BLS 65A V2 | 65 / 70 A (5 s) | 3–8S | 85–123 | Üretici 7" uzun menzil için öneriyor; çift BEC |
| T-Motor Velox F7 SE + V70A SE | 70 A | 3–8S | 86–130 | 7"–10" için önerilmiş; ESC 44.4 × 41 mm |
| GEPRC Taker F722 BLS 80A V2 | 80 / 85 A (5 s) | 3–6S | 85–123 | |
| ZeniRace F722 80A | 80 / 100 A | 6–8S | 80 | 70 A 6S sürümü 65 $ |
| HobbyWing XRotor G2 65A + F7 | 65 / 80 A | 3–6S | 159 | |

7" için pazar **65–70 A, 8S’e kadar** veriyor; 10" için 80 A ve 8S konuşuluyor. Yani 7"/10" ürünü yalnız akım değil **gerilim sınıfı** (8S = 33.6 V dolu) farkıdır: MOSFET V_DS ≥ 40 V, kondansatör ≥ 50 V, TVS ve INA/BEC girişi buna göre.

## 4. Özellik eğilimleri

| Konu | Pazarda bugün | Not |
|---|---|---|
| FC MCU | 5" bütçede F405, ortada F722, üstte H743 | F405 5" için yeterli kabul ediliyor |
| IMU | ICM-42688-P baskın | MPU6000 yalnız eski/premium (Holybro) |
| Baro, flash, OSD | Baro (BMP280) ve 8–16 MB blackbox orta sınıfta standart; analog OSD (AT7456E) hâlâ var | |
| BEC | 5 V + 9 V (dijital VTX için 9 V); bütçede toplam ~3 A | |
| Kablosuz ayar | SpeedyBee Bluetooth (uygulama) — bütçede fark yaratan özellik | |
| ESC yazılımı | Bluejay (8 bit, açık) ve AM32 (32 bit, açık) yükseliyor; BLHeli_32 geri çekildi | Çift yönlü DShot RPM: Bluejay ≥ 0.16, AM32 ≥ 1.80 |
| Motor çıkışı | Bazı yeni FC’lerde 8 motor (SpeedyBee V5) | |
| ESC telemetrisi | 8 bit ESC’lerde genelde yok; RPM çift yönlü DShot’tan | |

## 5. Uyumluluk

- 8 pin SM08B ESC konnektörü neredeyse her stack’te var; **pin dizilimi markaya göre değişiyor** ve yanlış takmak kartı bozabiliyor. Bağımsız bir dizilim karşılaştırması bulunamadı.
- Pratik çözüm: dizilimi en çok satan aileye (SpeedyBee F405 V4 ve GEPRC Taker) uydurmak, diğerleri için ters/çapraz kablo vermek. Kesin dizilim üretici kılavuzlarından çıkarılacak (`sistem-mimari`, `docs/pin-haritasi.md`).
- Montaj: 30.5 × 30.5 mm M3 (bazılarında Ø 4 mm silikon tampon → M3).

## 6. Öneri — konumlandırma ve hedef değerler

| Konu | Öneri | Gerekçe |
|---|---|---|
| İlk ürün | **5" stack: F405 FMU + 55 A 4’ü 1 arada ESC, 3–6S, 30.5 mm** | Pazarın en büyük ve en standart bölümü; esc55a ve fmu tasarımları zaten bu sınıfta |
| ESC akımı | **55 A sürekli, 70 A anlık (10 s)** | SpeedyBee/iFlight/Diatone 55 A, GEPRC 60 A; 2207 motor tepe 38–45 A → %20–40 pay |
| ESC yazılımı | **Bluejay** (EFM8BB21) | Açık kaynak, ücretsiz, RPM filtresi için çift yönlü DShot; ek telemetri hattı gerekmez |
| FMU | F405 + ICM-42688-P + baro + 16 MB flash + AT7456E OSD + 5 V/9 V BEC (toplam ≥ 3 A) | GEPRC/SpeedyBee seviyesi; fmu şematiği bunu zaten içeriyor |
| Fiyat bandı | Satış **≤ 70 $/stack** [öneri, tahmin] | SpeedyBee V4 (70 $) ile aynı, AliExpress markalarının (45–57 $) üstünde; yerli destek + belgeli tasarım fark |
| 7"/10" (sonra) | esc65a: **65 A, 3–8S** varyantı | GEPRC H65 8S ve T-Motor V70A 8S ile aynı sınıf; 10" için 80 A ayrı değerlendirilir |
| Fark yaratma | Doğru akım ölçümü (pazarda kalibrasyon sorunlu), 6S geçici koruması, açık belgeler, yerli destek; ileride Bluetooth/kablosuz ayar | |

## 7. Belirsizlikler

- Fiyatların çoğu tek tarih anlık görüntüsü; stok dışı ürünler var. AliExpress fiyatları kampanyalı.
- Akım sınıfları üretici iddiası (sürekli değer genelde anlığın %60–70’i, kaynak: satıcı blogu).
- 8 pin dizilimleri doğrulanmadı.
- Satış adedi / pazar payı verisi bulunamadı; “en çok satan” yorumu inceleme siteleri ve satıcı listelerine dayanıyor.

## Kaynaklar (erişim 2026-11-06)

- 5" karşılaştırma ve fiyat: [Oscar Liang — cheapest 5" build](https://oscarliang.com/cheapest-fpv-drone-build/), [UAVMODEL stack guide 2026](https://blog.uavmodel.com/fpv-drone-stack-guide-2026-aio-vs-separate-escfc-which-architecture-wins/), [UAVMODEL F7 vs H7 vs F405](https://blog.uavmodel.com/fpv-flight-controller-comparison-2026-f7-vs-h7-vs-f405-processors/)
- SpeedyBee: [Pyrodrone F405 V4 55A](https://pyrodrone.com/products/speedybee-f405-v4-stack-w-55a-3-6s-bls-4in1-esc-30x30mm), [Wrekd F405 V4](https://wrekd.com/products/speedybee-f405-v4-bls-3-6s-30x30-stack-combo-f405-fc-8bit-55a-4in1-esc), [Oscar Liang F405 V4 review](https://oscarliang.com/speedybee-f405-v4/), [Betaflight SPEEDYBEEF405V4](https://betaflight.com/docs/wiki/boards/current/SPEEDYBEEF405V4), [NextFPV F405 V5](https://www.nextfpv.com/products/speedybee-f405-v5-ox32-55a-30x30-stack), [RaceDayQuads F405 V5](https://www.racedayquads.com/products/speedybee-f405-v5-stack-f405-fc-55a-3-6s-ox32-esc-30x30-standard), [GetFPV F405 V5 Deluxe](https://www.getfpv.com/electronics/stacks/speedybee-f405-v5-stack-f405-fc-55a-3-6s-ox32-esc-30x30-deluxe.html)
- GEPRC: [Defiance RC Taker F405 60A V2](https://defiancerc.com/products/geprc-taker-f405-blheli_s-60a-stack-v2-30x30), [rcdrone.top Taker F405 60A V2](https://rcdrone.top/products/geprc-taker-f405-bls-60a-v2-stack-stm32f405-flight-controller-60a-4in1-esc-for-3-6s-fpv-drones), [Unmanned Tech — Taker lineup](https://www.unmannedtechshop.co.uk/de/blogs/knowledge-base/geprc-taker-flight-controller-esc-lineup-buying-guide-f405-f722-h743), [Dronkart Taker F722 60/65/80A](https://dronkart.com/product/geprc-taker-f722-bls-60a-65a-80a-v2-stack-4in1-esc-flight-controller-data-analyze-record-flight-data-plug-play-racing-fpv-drone/)
- Diatone: [GetFPV Mamba MK2 F405 F50 BLS](https://www.getfpv.com/diatone-mamba-stack-dji-f405-mk2-fc-f50-50a-blheli-s-esc.html), [Pyrodrone MK4 H743 F55A](https://pyrodrone.com/products/diatone-mamba-mk4-h743-v2-flight-controller-and-f55a-128k-6s-esc-stack-30x30mm), [RaceDayQuads MK4 F722 F55](https://www.racedayquads.com/products/diatone-mamba-mk4-f722-app-f55_128k-3-6s-30x30-stack-combo-f722-fc-55a-128k-32bit-4in1-esc?aff=60)
- iFlight: [iFlight BLITZ F7 E55](https://shop.iflight.com/BLITZ-F7-Stack-E55-4-IN-1-ESC-Pro1695), [RobotShop BLITZ F7](https://www.robotshop.com/products/iflight-blitz-f7-stack-e55-4-in-1-esc)
- Holybro: [rcdrone.top Kakute H7 v1.5](https://rcdrone.top/products/holybro-kakute-h7-v1-5-flight-controller-stack), [Epic FPV Kakute H7 v1.3](https://epicfpv.ca/products/kakute-h7-v1-3-stack-tekko32-f4-metal-4in1-65a-esc)
- 7"/10": [T-Hobby Velox V70A SE 8S](https://www.t-hobby.com/products/4-in1-fpv-stack-v70a-f7-se-8), [fpvstorerc Velox F7 SE 8S](https://fpvstorerc.com/products/t-motor-velox-f7-se-8s-stack-f7-fc-70a-4in1-esc-combo-1), [HobbyWing XRotor G2 65A](https://www.hobbywing.com/en/products/xrotor-fpv-g2-65a-4in1-esc--xrotor-fc-f7-combo), [RMRC HobbyWing 65A](https://www.readymaderc.com/products/details/hobby-wing-fpv-stack-65a-esc-f7-fc), [ZeniRace 7" long range](https://zenirace.com/pages/7in-long-range-build), [makerme 10" build](https://makerme.blog/posts/10inch-long-range/), [KiwiQuads T-Motor F55A Pro III](https://www.kiwiquads.co.nz/product/t-motor-f55a-pro-iii-55a-3-8s-bl32-4-in-1-esc)
- AliExpress: [HAKRC F405 V2 dual BEC](https://www.aliexpress.us/item/3256808946065124.html?gatewayAdapt=glo2usa4itemAdapt), [HGLRC Specter F460 60A](https://www.aliexpress.us/item/3256809166899187.html?gatewayAdapt=glo2usa4itemAdapt)
- Akım ihtiyacı: [IntoFPV — 2207 amp draw](https://intofpv.com/t-amp-draw-on-2207-motors), [Unmanned Tech — 2207 6S](https://www.unmannedtechshop.co.uk/blogs/knowledge-base/2207-motor-1750kv-1850kv-1960kv-2050kv-6s), [UAVMODEL ESC guide 2026](https://blog.uavmodel.com/fpv-drone-esc-selection-guide-amps-protocols-and-firmware-in-2026/)
- ESC yazılımı: [Oscar Liang — identify ESC firmware](https://oscarliang.com/identify-esc-firmware/), [UAVMODEL AM32 vs BLHeli_32](https://blog.uavmodel.com/fpv-drone-esc-selection-guide-2026-protocols-amp-ratings-am32-vs-blheli_32/)
- Konnektör: [IntoFPV — ESC/FC connection](https://intofpv.com/printthread.php?tid=23857), [IntoFPV forum](https://intofpv.com/printthread.php?tid=19430)
