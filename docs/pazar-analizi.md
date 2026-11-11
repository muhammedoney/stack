# Pazar analizi — FPV stack (FMU + 4’ü 1 arada ESC)

Sahibi `pazar-analisti`. Tarih: 2026-11-06 (§6a: 2026-11-10, müşteri km taşı sırası). Ham veri: [`pazar/rakipler.csv`](pazar/rakipler.csv). Fiyatlar USD, KDV/kargo hariç, satıcı sayfasında görülen değerler (stok ve kampanya sık değişiyor). Akım değerleri **üretici iddiası**; bağımsız test yok.

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

## 6a. Portföy ve yol haritası (2026-11-10, müşteri sırası)

Ayrıntı, muadiller ve kaynaklar: [`pazar/urun-portfoyu-yol-haritasi.md`](pazar/urun-portfoyu-yol-haritasi.md); ham veri [`pazar/portfoy-fiyatlar.csv`](pazar/portfoy-fiyatlar.csv). “F100” yazım hatasıydı, doğrusu **F405**. Hedef fiyatlar **öneri**dir.

| KT | Ürün | Ana muadil ($) | Hedef fiyat (öneri, $) |
|---|---|---|---|
| M1 | 5" stack: F405 FMU + 55 A (mevcut) + ayrı FMU/ESC SKU + aksesuar | SpeedyBee F405 V4 55A 65.99 | stack 59–65; FC 35–39; ESC 28–33 |
| M2 | 5"/7" ESC **65 A / 80 A, 3–6S** (esc65a, 40 V BOM) | SpeedyBee BLS 60A 46.99 (V4 60A stack kalktı), GEPRC H60 46.79 | ESC 39–45; stack 72–78 |
| M3 | 7"/10" **8S**: ESC 65 A + 80 A, 8S FMU, GPS M10 | GEPRC H65 8S 46.99, H80 69.99; GEP-F405-8S 47.99; HGLRC M100-5883 16–22 | ESC 45–49 / 62–68; FMU 40–45; GPS 15–18 |
| M4 | F7 FMU (F722; Betaflight + INAV) | SpeedyBee F7 V3 FC 45.99 (stack kalktı), Foxeer F722 V4 64.90 | FC 42–48 |
| M4a | **Dual-ESC FMU** (2× 4in1 → 8 motor), ayrı SKU | SpeedyBee 8 motor pedi; fark = çift ESC konnektörü | FC Dual 48–55 |
| M5 | 2. versiyon: BF + INAV + **ArduPilot** → **H743** önerisi | GEPRC Taker H743 FC 87, TBS Lucid H7 59.95 | FC 55–65; stack 105–115 |
| M6 | Kanat FC (INAV) + ESC aynı PCB (kırılabilir) | TBS Lucid Wing AIO (H7 + 50 A) 69.95–82.99; RU НИМБУС F4 stack 7 700 ₽ | F405 + 45 A 55–65 |
| M7 | AM32 32 bit ESC (60 A 3–6S, 80 A 8S) | JHEMCU AM32A60 44.99, TBS Lucid 60A 8S 84.99 | 45–50 / 70–80 |
| M8 | ELRS alıcı (2.4 G → LR1121) | Happymodel EP2 13.49–16.99, RP1 V2 18.99 | 13–16 / 22–25 |
| M9 | Analog VTX seviye 1 (≤ 600 mW, 20×20) | Flywoo HM600 19.99, Unify Pro32 Nano 22.99–31.10 | 22–27 |
| M10 | Analog VTX seviye 2 (1.6–2.5 W, 7–36 V) | RUSH Max Solo 49.99–51.99 | 45–52 |
| M11 | Fiber → stack uyumu (`../fiber` mevcut; sıfırdan değil) | Transwan 35×30 mm; bizim fiberair Rev B | fiber deposunda |

**Marka:** ürün ailesi **Crow** (müşteri kararı K12, 2026-11-11); konumlandırma, isim şeması, SKU, kanal ve tescil riski: [`pazar/crow-marka-pazarlama.md`](pazar/crow-marka-pazarlama.md).

Ertelenen: AIO (en arkaya), dijital VTX (durdu), mekanik (en son). Önerilen takvim 2026 Q4→2029 Q3 ve poster: [`pazar/urun-portfoyu-yol-haritasi.md`](pazar/urun-portfoyu-yol-haritasi.md) §B, [`pazar/stack-yol-haritasi-poster.jpg`](pazar/stack-yol-haritasi-poster.jpg).

**Önemli bulgular / güncellemeler (§2, §3, §6’ya göre):**
- SpeedyBee F405 V4 55A stack resmi **65.99 $**; **V4 60A ve F7 V3 stack’leri üretimden kalktı** (SpeedyBee, 2026-11-10). §6 “≤ 70 $” lider ürünün üstünde.
- **STM32F722’de ArduPilot çalışmaz** (512 KB; ArduPilot ≥ 1 MB ister). F405 ve F745 kısıtlı firmware, F765/H743 tam. F765 Betaflight ürün hedefi yok ve Matek’te EOL → üç yazılım için gerçekçi seçenek **H743**.
- 10" sınıfı 80–100 A 8S’e kaydı (GEPRC H80 69.99 $, H100 79.99 $).
- GEPRC H65 8S: FPVtopia (üretici verisi) BLHeli_S, hedef B_X_30 → önceki çelişki büyük ölçüde çözüldü.
- UAVMODEL blog özellik bilgisinde hatalı; yalnız eğilim için kullanılmalı.

## 7. Belirsizlikler

- Fiyatların çoğu tek tarih anlık görüntüsü; stok dışı ürünler var. AliExpress fiyatları kampanyalı.
- Akım sınıfları üretici iddiası (sürekli değer genelde anlığın %60–70’i, kaynak: satıcı blogu). **Düzeltme 2026-11-11 (§8):** 24 üründe sürekli değer anlığın %65–93’ü (ModalAI %40), 55 A sınıfında %79–85; “sürekli”nin süresi ve koşulu çoğunda yazılmamış.
- 8 pin dizilimleri doğrulanmadı.
- Satış adedi / pazar payı verisi bulunamadı; “en çok satan” yorumu inceleme siteleri ve satıcı listelerine dayanıyor.

## 8. Akım etiketleri: 55 A ne demek

Tarih 2026-11-11. Müşteri sorusu: *“Diğer ürünlerde nasıl oluyor, ona göre isimlendirelim. 55A yazıldığında sürekli 55A mı kastediliyor?”* (SOR-015). Ham tablo: [`pazar/esc-akim-etiketleri.csv`](pazar/esc-akim-etiketleri.csv): 24 FPV 4’ü 1 arada ESC, karşılaştırma için 2 HobbyWing endüstriyel ESC ve bizim hesap. Kaynak türü her satırda yazılı: **üretici** (12 ürün: üretici sayfası, kılavuz ya da veri sayfası) veya **satıcı** (12 ürün; üretici sayfası açılmadığında satıcının kopyaladığı üretici tablosu). Tüm sayılar **üretici iddiası**.

### 8.1 Üreticiler nasıl yazıyor (24 ürün)

| Bilgi | Kaç üründe var | Not |
|---|---|---|
| Ürün adındaki sayı = “continuous” değeri | adında sayı olan 22 ürünün 21’inde | İstisna **HobbyWing XRotor G2 “65A”**: tabloda 60 A × 4 sürekli, 80 A × 4 tepe. Ad ne sürekli ne anlık değeri |
| “Continuous” değeri | 24 / 24 | JHEMCU BL32 60A yalnız “Current: 60A” yazıyor (sürekli/anlık ayrımı yok) |
| **Sürekli değer için süre** | **3 / 24** | TBS Lucid 6S: **60 A × 4, 300 s**; TBS Lucid 8S: **60 A × 4, 60 s**; FlyingRC 75A: **75 A, 45 s (4S’te test)**. Diğer 21 üründe “continuous”un süresi yok |
| Anlık (burst/peak) değeri | 23 / 24 | 55 A sınıfında 65–70 A; tüm ürünlerde anlık/sürekli oranı 1.08 (GEPRC H60) – 1.54 (Foxeer 65/100 A) |
| Anlık değer için süre | 14 / 24 | 5 s (GEPRC, T-Motor V70A), **10 s (çoğu)**, 60 s (TBS 6S), < 1 s (ModalAI). Aynı ürüne farklı satıcılar 5 s / 10 s yazabiliyor (SpeedyBee 55A) |
| Kanal başına olduğu açık (“× 4”, “per channel/motor”) | 16 / 24 | Kalan 8’de yazılmamış ama piyasa okuması kanal başına (Oscar Liang, ZeniRace) |
| **4 kanalın aynı anda sürekli taşıdığı akım** | **0 / 24** | Hiçbir üretici “4 kanal birlikte” ile “tek kanal” arasında ayrım yapmıyor |
| **Sayısal test koşulu** (hava akışı m/s, ortam °C, soğutucu, PWM frekansı) | **0 / 24** | Yalnız FlyingRC gerilimi yazıyor (“4S’te test”) |
| Nitel koşul / uyarı | 5 / 24 | Holybro Tekko32 65A: yüksek akımda hava akışı “çok önemli”; TBS: 7" üstünde “iyi hava akışı gerekli”; FlyingRC: sıcak ortam, nem, düşük basınç, hava akışı yokken sürekli akım değerin altına düşer; ModalAI: 40 A/motor “yeterli hava akışıyla, uygulamaya bağlı”. Pilotix yalnız çalışma sıcaklığı (−20…40 °C) |
| MOSFET sayısı / kanal | 0 / 24 | Yalnız parça adı: T-Motor F55A Pro III TPHR8504, FlyingRC Infineon IRF7480 (0.95 mΩ). SpeedyBee 55A/60A: “3 oz bakır, alüminyum soğutucu” |

**Endüstriyel karşılaştırma (HobbyWing XRotor Pro, tek ESC):** adındaki sayı **tepe akımına** yakın, sürekli değer çok daha düşük ve koşula bağlı: H100A → sürekli **40 A “(Good heat dissipation)”**, tepe 120 A **3 s**; H130A → sürekli 60 A, tepe 150 A 3 s. Aynı üretici FPV ürününde (G2 65A) farklı bir kural kullanıyor. Yani **sektörde tek bir ad kuralı yok**.

### 8.2 Bağımsız ölçüm ve topluluk görüşü

**Ölçüm (yayımlanmış, sayısal):** 5" sınıfı bir 4’ü 1 arada ESC’nin etiket akımını kaç saniye/dakika, hangi sıcaklıkta taşıdığını gösteren **bağımsız bir test bulunamadı** (Oscar Liang incelemeleri, IntoFPV, RCGroups, tezgâh/termal test aramaları). Oscar Liang’in Tekko32 incelemesinde de akım/sıcaklık ölçümü yok. Bulunan sayısal veriler üreticiye ait:
- ModalAI (üretici personeli, forum 2023-08-02): mini 4’ü 1 arada ESC 16 V’ta kanal başına 15 A (toplam 60 A), **1 dk** sürekli test edilmiş; ESC sıcaklığı için öneri 90–100 °C altı. (Ayrı ürün olan VOXL FPV ESC’nin değeri 40 A/motor “yeterli hava akışıyla”.)
- FlyingRC 75A: “sürekli” = **45 s, 4S**.
- TBS: “sürekli” = **60 s (8S) / 300 s (6S)**.

Bu üç örnek, üreticinin “continuous” dediği değerin **ısıl denge (saatlerce) değil, 45–300 s’lik bir yük** olduğunu gösteriyor. Süreyi yazmayan 21 üründe tanım belirsiz.

**Anekdot / görüş (ölçüm değil):**
- Oscar Liang (ESC rehberi): değer **kanal (motor) başına**. 60 A 4’ü 1 arada = toplam ~240 A. Anlık genelde < 10 s. 55 A’lık ESC birkaç saniye 70–80 A görebilir.
- ZeniRace (üretici blogu): 55 A = her kanal 55 A’ya kadar. Kart ortak bakır ve ısı sınırı paylaştığı için **toplamı (4 × 55 A) sürekli taşımayabilir**. Değer üreticinin test koşuluna bağlı. Açık tezgâhta test edilen ESC gövde içinde çok daha sıcak çalışır.
- IntoFPV, “35A AIO” başlığı (2021): katılımcılara göre AIO/4’ü 1 arada akım değerleri “abartılı” ve yüksek değerler hava akışı altında kısa süreleri gösteriyor. Normal uçuşta motor başına ~10 A, tepe anlarını kondansatör karşılıyor. Sorun çıkaran durumlar: punch-out, takılan pervane, turtle modu.
- esk8.news (elektrikli kaykay ESC’leri, 2019): ESC akımı için **standart test yöntemi yok**, değerler “güvene dayalı”. Trampa’nın aktardığına göre 200 A etiketli bir klon ~120 A’da kalmış. Önerilen yöntem: 20 ± 3 °C ortamda 5 dk sürekli yük, adım adım artırma, MOSFET ve soğutucu sıcaklığı ölçümü (topluluk önerisi, standart değil).
- Gerçek ihtiyaç (§2): 5" 6S 2207 motor tepe 38–45 A; uçuş ortalaması motor başına 10–25 A (SOR-015); punch’ta ~30 A (anekdot).

### 8.3 Standart / norm

- Hobi RC / FPV ESC’leri için **“continuous current” tanımlayan bir standart bulunamadı** (IEC, hobi birlikleri, üretici birliği yok). Her üretici kendi tanımını kullanıyor, çoğu tanımı yazmıyor.
- Benzerlik için kullanılabilecek normlar (ESC’ye doğrudan uygulanmaz): IEC 60034-1 motor görev tipleri (**S1 sürekli** / **S2 kısa süreli**, ör. S2 10 dk), IEC 61800-2 ayarlı hız sürücülerinde belirtilen ortam ve soğutmada **anma çıkış akımı** ile süreli aşırı yük, IEC 60512-5-2 / EIA-364-70 akım–sıcaklık artışı (3 ardışık 5 dk ölçümü ≤ 2 °C fark = ısıl denge). MOSFET veri sayfası I_D değeri de T_C = 25 °C idealinde verilir. Hiçbiri hobi ESC etiketine bağlayıcı değil.
- Üretici “tanımları”: HobbyWing endüstriyel = “Good heat dissipation” notlu sürekli + **3 s** tepe; T-Motor / SpeedyBee / Diatone / Aikon / HGLRC = sürekli + **10 s** anlık; GEPRC = sürekli + **5 s** anlık; TBS = **süreli sürekli (60/300 s)** + süreli anlık. Bunlar üretici kuralı, norm değil.

### 8.4 Cevap: “55A yazıldığında sürekli 55A mı kastediliyor?”

**Kısmen evet.** FPV pazarında ürün adındaki “55A” (21/22 üründe) üreticinin **kanal başına “continuous”** değeri. Yanında genelde 65–70 A anlık değer (çoğunlukla 10 s) yazılıyor. Ama:
1. “Sürekli”nin **süresi 24 üründen yalnız 3’ünde** yazılı ve orada da 45–300 s. Isıl dengede (dakikalarca, saatlerce) 55 A anlamına gelmiyor.
2. **Test koşulu hiçbirinde sayısal değil.** Hava akışı, ortam sıcaklığı ve PWM frekansı bilinmiyor.
3. **Dört kanalın aynı anda 55 A taşıyacağı hiçbir üründe söylenmiyor.** ZeniRace bunun garanti olmadığını açıkça yazıyor.
4. Isıl hesabımız (`rapor/guc-ip03.md` §2.5) 41 × 48 mm kartın 5 m/s havada ≈ 35 W atabildiğini gösteriyor. En iyi 40 V FET ile 4 × 55 A ≈ 61 W kayıp demek. Aynı kart boyundaki rakiplerin de 4 × 55 A’yı ısıl dengede taşıyamayacağı fizik olarak beklenir (**tahmin**: rakiplerin FET’i, bakırı ve soğutucusu bilinmiyor, ölçülmedi). Rakip etiketi büyük olasılıkla “tek kanal ya da kısa süre, hava akışında” anlamına geliyor.

Sonuç: pazarın “55A”sı **sınıf adı**. Pratikte “kanal başına, kısa-orta süre, hava akışında 55 A” demek, dört kanalda ısıl dengede sürekli 55 A demek değil. Bizim hesaplanan değerlerimiz (**tahmin ± %50**, DOG-005 ile ölçülecek; 25 °C, 5 m/s, 24 kHz, 6S): **tek kanal ~62 A sürekli; 4 × 34–41 A sürekli; 4 × 55 A 10 s**; 50 °C’de 4 × 27.5–34 A. Bu değerler pazardaki 55 A sınıfıyla aynı yerde. Fark, bizim rakamlarımızın tanımlı ve koşullu olması.

### 8.5 İsimlendirme seçenekleri

| # | Ürün adı / veri sayfası | Artı | Eksi | Rakiplere göre algı | Yasal / iade riski |
|---|---|---|---|---|---|
| A | **“Crow 55A”** + veri sayfasında koşullu akım tablosu: *55 A kanal başına sürekli (tek kanal yüklü) · 4 × 35 A sürekli (4 kanal birlikte) · 4 × 55 A 10 s · 4 × 70 A 2 s · koşul: 25 °C, ≥ 5 m/s hava, 24 kHz, 6S · 50 °C azaltma eğrisi* | Pazarın ad kuralına (kanal başına sürekli) uyuyor, rafta 55 A sınıfında görünür. Her satır doğru ve test edilebilir. 4 kanal satırı pazarda yok, “açık belge” farkını destekler | Tablo okuyan kullanıcı “4 × 35 A”yı rakibin “55 A × 4” yazısıyla karşılaştırıp bizi zayıf sanabilir | Adda eşit. Tablo dikkatli okuyanda başta zayıf, ama dürüst ve teknik kullanıcıda güven verici. Yanına “pazar eşdeğeri: 55 A sınıfı (kanal başına)” notu ve test yöntemi bağlantısı konursa bu algı azalır | Düşük: her iddianın koşulu yazılı. “Tek kanal 55 A sürekli” DOG-005’te ölçülmeli (hesap 62 A, ± %50 belirsizlik) |
| B | **“Crow 40A”** ya da “40A sürekli / 55A burst” | En muhafazakâr, iade riski en düşük | 55 A sınıfı rakiplerle aynı donanımda bir sınıf aşağıda görünür. 5" 6S alıcısı 55–60 A arıyor (§2). Satış ve fiyat (≤ 70 $) zayıflar | Açıkça zayıf (HAKRC/HGLRC 60 A, SpeedyBee 55 A) | En düşük |
| C | **“Crow 55A”**, veri sayfasında yalnız “55 A × 4 continuous / 70 A burst” (pazar gibi) | Rakiplerle birebir aynı görünüm, en kolayı | 4 × 55 A sürekli kendi hesabımızla tutmuyor. Bilerek koşulsuz yazmak SOR-015 seçenek 3’e denk | Eşit | **Yüksek.** Kendi analizimiz 4 × 55 A sürekliyi çürütüyor. Türkiye’de 6502 sayılı TKHK md. 8’e göre etiket, tanıtım ve kılavuzdaki özelliği taşımayan mal ayıplıdır (iade, değişim, bedel indirimi). Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği yanıltıcı teknik iddiayı da kapsar. AB’ye satışta 2019/771 (tanıma uygunluk) ve 2005/29/AT geçerli. Hukuki görüş alınmalı |
| D | **“Crow 55A”** + TBS tarzı süreli tanım: “55 A × 4, X s” | Pazarda en dürüst örnekle (TBS) aynı dil | τ ≈ 24 s olduğu için 60 s, ısıl dengenin ~%92’si demek. 4 × 55 A 60 s **tutmuyor** (tahmin). Yalnız 10 s yazılabilir, o da rakibin “anlık”ına denk düşer | “55 A × 4, 10 s” rakibin 70 A 10 s’iyle karşılaştırılınca zayıf | Düşük, ama ad ile tablo arasında açıklama gerekir |
| E | **“Crow 55A”** + yalnız “55 A per channel @ airflow” | Kısa | Hava akışı ve süre sayısal değil, belirsizlik kalıyor. Pazarın sorunu tekrarlanır | Eşit | Orta: “airflow” tanımlanmadığı için iade itirazında savunması zayıf |

### 8.6 Öneri

**Seçenek A** (SOR-015 seçenek 1 ile uyumlu):
1. **Ad “Crow 55A” kalsın.** Pazarda 22 üründen 21’inde ad, kanal başına sürekli değerdir. Bizim tek kanal sürekli değerimiz (~62 A, tahmin) bu kuralı karşılıyor.
2. **Veri sayfası ve kutu üstünde akım tablosu** (pazarda yok, fark yaratan nokta): kanal başına sürekli (tek kanal) · 4 kanal birlikte sürekli · 4 × 10 s · 4 × 2 s, yanında test koşulu (ortam °C, hava m/s, PWM kHz, gerilim) ve 50 °C azaltması. Kutu yüzünde tek satır yeter: *“55 A / kanal · 4 × 55 A 10 s · koşullar veri sayfasında”*.
3. **Rakamlar ölçümden sonra yazılsın:** DOG-005 (ve DOG-004/006/083) testinde 25 °C, 5 m/s hava ve 24 kHz’de tek kanal ve 4 kanal sürekli, 10 s ve 2 s değerleri ölçülür. Satışta tahmin değil, ölçülen değer kullanılır. Hesap ± %50 belirsiz. Ölçülen 4 kanal sürekli değer 30 A’nın altında çıkarsa ad yeniden değerlendirilir (ör. “Crow 50A”).
4. **Test yöntemi yayımlansın** (kısa PDF veya kılavuz bölümü). Bu, “açık belge” konumlandırmasını destekler. TBS ve FlyingRC örneği gösteriyor ki süre ve koşul yazmak pazarda kabul görüyor.
5. **Pazarlama dili:** “gerçek, ölçülmüş akım” vurgusu, rakibe isim vermeden. Rakip ürün hakkında doğrulanmamış “sahte 55 A” iması yapılmasın (karşılaştırmalı reklam riski).
6. C seçeneği (koşulsuz “55 A × 4 continuous”) **önerilmez**: kendi analizimiz bu iddiayı çürütüyor, ayıplı mal / yanıltıcı reklam riski var.

**Belirsizlikler:** 12 ürünün verisi satıcı sayfasından (üretici sayfası 404 ya da açılmadı). Satıcılar arasında 5 s / 10 s ve anlık 65 / 70 A çelişkileri var (CSV `not`). Rakiplerin gerçek 4 kanal sürekli değeri ölçülmedi. Bir rakip ESC’nin (ör. SpeedyBee BLS 55A) DOG-005 düzeneğinde bizimkiyle yan yana ölçülmesi, A seçeneğindeki “pazar eşdeğeri” iddiasını kanıtlamanın en ucuz yolu (öneri, `test-muhendisi`). Yasal değerlendirme hukukçu görüşü değildir.

**Kaynaklar (erişim 2026-11-11):** üretici: [SpeedyBee BLS 55A (F405 V4 stack)](https://www.speedybee.com/speedybee-f405-v4-bls-55a-30x30-fc-esc-stack/), [SpeedyBee BLS 60A](https://www.speedybee.com/speedybee-bls-60a-30x30-4-in-1-esc/), [GEPRC Taker H60](https://geprc.com/product/geprc-taker-h60_bls-60a-4in1-esc/), [GEPRC Taker H65 8S](https://geprc.com/product/geprc-taker-h65_8s_bls-65a-4in1-esc/), [iFlight BLITZ E55](https://shop.iflight.com/BLITZ-E55-4-IN-1-2-6S-ESC-Pro1694), [HobbyWing XRotor G2 65A](https://www.hobbywing.com/en/products/xrotor-fpv-g2-65a-4in1-esc268), [HobbyWing H100A](http://www.hobbywing.com/en/products/xrotor-h100a-14s-foc-v1123), [HobbyWing H130A](https://www.hobbywing.com/en/products/xrotorh130a14sfoc), [Holybro Tekko32 F4 Metal 65A](https://holybro.com/products/tekko32-f4-metal-4in1-65a-esc-65a), [Holybro Tekko32 F4 50A spec PDF](https://cdn.shopify.com/s/files/1/0604/5905/7341/files/Holybro_Tekko32_F4_4in1_50A_ESC_spec_7f900ab6-7c29-483f-86a9-260c69b669fd.pdf), [FlyingRC 4v1 75A kılavuzu](https://www.rotorama.com/assets/docs/153b380199c70910607d3b864880c4e9/40357-1/manual-flyingrc-4v1-esc-75a-en.pdf), [Pilotix 75A datasheet](https://public.hobbydrone.cz/Pilotix/6208/Datasheet/Pilotix%204in1%2075A%20AM32%20%28SKU%206208%29%20datasheet%20EN.pdf), [ModalAI VOXL FPV ESC](https://docs.modalai.com/voxl-fpv-esc-datasheet), [ARK 4IN1](https://docs.arkelectron.com/electronic-speed-controller/ark-4in1-esc); satıcı: [GetFPV SpeedyBee F405 V5](https://www.getfpv.com/speedybee-f405-v5-stack-f405-fc-55a-3-6s-ox32-esc-30x30-standard.html), [myfpvstore E55S](https://www.myfpvstore.com/8zvk), [KiwiQuads Mamba F55](https://www.kiwiquads.co.nz/product/diatone-mamba-f55-128k-bl32-4in1-esc-55a-6s/), [KiwiQuads F55A Pro III](https://www.kiwiquads.co.nz/product/t-motor-f55a-pro-iii-55a-3-8s-bl32-4-in-1-esc), [fpv24 Velox V70A](https://www.fpv24.com/en/t-motor/t-motor-velox-f7-se-v70a-8s-fc-flight-controller-esc-stack), [FlyingTech Foxeer Reaper 65A](https://www.flyingtech.co.uk/product/foxeer-reaper-f4-128k-3-8s-bl32-4-in-1-30x30-esc-65a), [RMRC TBS Lucid 6S](https://www.readymaderc.com/products/details/86684-tbs-lucid-4in1-6s-60a-esc), [RMRC TBS Lucid 8S](https://www.readymaderc.com/products/details/86468-tbs-lucid-4in1-8s-60a-esc), [RotorGeeks Aikon AK32](https://rotorgeeks.com/aikon-ak32-4-in-1-55a-v3-6s-esc), [GetFPV HGLRC Specter 60A](https://www.getfpv.com/drone-brands/hglrc/hglrc-specter-60a-blheli-32-3-6s-4-in-1-esc.html), [WREKD HAKRC 3B60A](https://wrekd.com/products/hakrc-3b60a-4-in-1-blheli-esc), [WREKD JHEMCU BL32 60A](https://wrekd.com/products/jhemcu-bl32-32bit-60a-3-6s-30x30-4in1-esc), [Unmanned Tech GEPRC H60](https://www.unmannedtechshop.co.uk/products/geprc-taker-h60_bls-60a-4in1-esc), [openelab Holybro Tekko32 50A FAQ](https://openelab.io/products/holybro-tekko32-f4-50a); görüş: [Oscar Liang — ESC rehberi](https://oscarliang.com/esc), [Oscar Liang — Tekko32 incelemesi](https://oscarliang.com/holybro-tekko32-4in1-esc/), [ZeniRace — ESC akım değerleri](https://zenirace.com/blogs/news/understanding-esc-current-ratings-in-fpv), [IntoFPV — 35A AIO](https://intofpv.com/archive/index.php/thread-19196.html), [esk8.news — Verifying ESC Performance](https://forum.esk8.news/t/verifying-esc-performance-sro/12727), [ModalAI forum — 15 A 1 dk testi](https://forum.modalai.com/post/11585), [ModalAI forum — sıcaklık](https://forum.modalai.com/post/24464).

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
