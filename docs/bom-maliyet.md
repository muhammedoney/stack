# BOM maliyeti ve tedarik durumu — 5" stack (fmu + esc55a)

> **Tarih:** 2026-11-06. Sahibi `bom-tedarik`. **Fiyat ve stok kaynağı:** JLCPCB parça arama arayüzü (`jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`, JLC dizgi fiyatı, basic/extended bilgisi). Parametreler LCSC ürün arayüzünden (`wmsc.lcsc.com/ftps/wm/product/detail`). İkisi de 2026-11-06'da okundu. Fiyatlar USD, KDV/kargo/gümrük hariç. Dizgi ücretleri [JLCPCB PCBA fiyat sayfası](https://jlcpcb.com/help/article/pcb-assembly-price) ve [PCBA SSS](https://jlcpcb.com/help/article/pcb-assembly-faqs) sayfalarından (2026-11-06). **PCB fiyatları tahmindir**: JLC fiyat hesaplayıcısına erişilemedi (§3).
> **Parça listesi:** `tools/altium_sch_dump.py` ile `boards/esc55a/altium/{main,mcu,mcu2}.SchDoc` ve `boards/fmu/altium/fmu.SchDoc` dosyalarından çıkarıldı. Pedler (`X PADS/PADR/PAD.ESC/PAD.PWR`) ve `LOGO` BOM dışı. Ham tablolar: [`boards/esc55a/bom-maliyet.csv`](../boards/esc55a/bom-maliyet.csv), [`boards/fmu/bom-maliyet.csv`](../boards/fmu/bom-maliyet.csv). CSV'de taban kod ve S1b önerisi yan yana.
> **Hedef (PRJ-004 / SYS-002):** 100 set kademesinde stack başına toplam ≤ 15 $ (komponent + PCB + dizgi). **2026-11-06 DT-001 ile ≤ 28 $** (tüm özellikler kalır).
> **2026-11-10 güncellemesi:** esc55a **Rev B** (İP-03 güç önerileri işlenmiş) maliyeti **§9**'da, BOM [`boards/esc55a/bom-revb.csv`](../boards/esc55a/bom-revb.csv). §1–§8 S0/S1/S1b değerleri (2026-11-06) değiştirilmedi.
> **Kademe kuralı:** "100 set" = 100 × karttaki adet. Birim fiyat bu toplam adetin JLC kademesinden alınır; örneğin 24 MOSFET için 2400 adet. CSV'de ayrıca 100 adet kademesi birim fiyatı da var. JLC'nin fire için eklediği fazla parça hesaba katılmadı (pasiflerde küçük).

## 1. Özet

| Senaryo (stack = fmu + esc55a) | 5 set $/stack | 100 set $/stack | 1000 set $/stack | 15 $'a göre (100 set) |
|---|---|---|---|---|
| **S0** Şematik olduğu gibi | 108.89 | 57.03 (**üretilemez**: ME7170 stoğu yetmez) | 52.40 | +42.0 |
| **S1** Stoklu muadiller, gereksinim değişmez, risk düşük | 80.20 | **31.93** | 27.39 | **+16.9** |
| **S1b** S1 + ekip kararıyla tasarım değişiklikleri (§5-A) | 73.61 | **27.38** | 22.97 | **+12.4** |
| **S2a** S1b + APM32F405 + BMI270 (**müşteri kararı**, özellikler kalır) | 70.73 | 24.84 | 19.77 | +9.8 |
| **S2** S2a + OSD, baro, flash, akım ölçümü çıkar + bulk 8 adet (**müşteri kararı**) | 60.64 | 19.53 | 15.17 | +4.5 |

**PRJ-004 durumu: karşılanmıyor.** JLC'de 100 sette en iyi gerçekçi değer S1b ile **~27 $**, bütün özellikler kesilse bile **~19.5 $**. 15 $'a ancak 1000 set kademesinde ve S2 kesintileriyle yaklaşılıyor (15.2 $). RSK-004 doğrulandı. Öneri ve müşteri soruları §6'da.

### 1.1 Kart başına kırılım ($/kart)

| | Komponent | PCB (tahmin) | Dizgi | **Toplam** |
|---|---|---|---|---|
| **S1, 100 set** — esc55a | 13.54 | 0.80 | 2.13 | **16.47** |
| **S1, 100 set** — fmu | 13.88 | 0.25 | 1.33 | **15.46** |
| **S1, 100 set — stack** | **27.42** | **1.05** | **3.46** | **31.93** |
| **S1b, 100 set** — esc55a | 10.13 | 0.80 | 2.08 | **13.01** |
| **S1b, 100 set** — fmu | 12.77 | 0.25 | 1.35 | **14.37** |
| **S1b, 100 set — stack** | **22.90** | **1.05** | **3.43** | **27.38** |
| **S1, 5 set** — esc55a | 18.82 | 6.00 | 19.70 | 44.52 |
| **S1, 5 set** — fmu | 20.45 | 0.40 | 14.82 | 35.67 |
| **S1, 5 set — stack** | **39.27** | **6.40** | **34.52** | **80.20** |
| **S1b, 5 set — stack** | 32.43 | 6.40 | 34.79 | **73.61** |

5 sette dizgi, kurulum ücretleri yüzünden (ESC çift yüz 51 $ + 16 $ şablon) en büyük kalemdir. Prototip bütçesi (S1, 5 set, kargo hariç): yaklaşık **400 $**.

### 1.2 En büyük kalemler (S1, 100 set, stack başına)

| # | Kart | LCSC | Parça | Adet | Birim $ | $/stack |
|---|---|---|---|---|---|---|
| 1 | fmu | C15742 | STM32F405RGT6 (ST) | 1 | 4.957 | 4.96 |
| 2 | esc | C6119969 | 22 µF 35 V X5R 1206 (HRE) | 29 | 0.135 | 3.91 |
| 3 | esc | C404363 | AON6354 MOSFET (AOS), ME7170 yerine | 24 | 0.149 | 3.58 |
| 4 | esc | C80713 | EFM8BB21F16G-C-QFN20R | 4 | 0.794 | 3.18 |
| 5 | fmu | C54308212 | ICM-42688-P (Tokmas); TDK orijinali C1850418 **18.99 $** | 1 | 2.118 | 2.12 |
| 6 | fmu | C82351 | AT7456E | 1 | 1.899 | 1.90 |
| 7 | fmu | C97521 | W25Q128JVSIQ (basic) | 1 | 1.588 | 1.59 |
| 8 | esc | C19077370 | JSM6288Q (FD6288Q muadili) | 4 | 0.273 | 1.09 |
| 9 | fmu | C54582187 | BMP388 (Tokmas); Bosch C779278 4.91 $ | 1 | 0.968 | 0.97 |
| 10 | esc | C2155860 | INA199C1DCKR | 1 | 0.532 | 0.53 |

İlk dört kalem S1 komponentinin %57'si. Dizgi 3.46 $/stack, PCB ~1.05 $/stack (tahmin).

## 2. BOM ve kodlar

### 2.1 Kurulan tek BOM (varsayımlar)

| Konu | Varsayım |
|---|---|
| fmu U0 ×2 | Aynı STM32F405 sembolünün iki parçası (çok parçalı sembol). **1 adet** |
| fmu J1 ×2 | USB-C ve SM08B ayrı parçalar. İkisi de var (SM08B'ye `J1b` dendi) |
| fmu U6 BMP388 / BMP280 | Yalnız BMP388 takılı, BMP280 DNP. Bosch BMP280 stokta yok (C83291, 0 adet) |
| fmu U2 MAX7456 | AT7456E (C82351) ile. MAX7456 stokta yok (C5346361, 0 adet). Pin uyumu §2.3 |
| fmu C60 ×2, C61 ×2 | 4 ayrı 100 nF varsayıldı (tutucu). Kopya çıkarsa 2 adet eksilir (−0.02 $) |
| fmu C? ×3 (10 µF 0805), R? ×2 (5.1 k 0805) | Ayrı parçalar sayıldı, numaralanacak |
| fmu 3.3 V regülatörü | **Şematikte yok** (SYS-042). Varsayım olarak U8 ME6211C33M5G-N (C82942, 500 mA, 5 V'tan) + 2 × 1 µF eklendi: +0.06 $ |
| esc R? ×8 (3 k / 1 k, E6) | Takılı sayıldı (+0.01 $) |
| Sayım | esc55a: **200 parça / 26 satır / 750 lehim noktası**. fmu: **98 parça (tekilleştirilmiş şematikten 95 + varsayım 3) / 44 satır / 389 lehim noktası** (pin sayısından) |

### 2.2 esc55a — taban kodlar (100 set birim fiyatı, 100 set için gereken adetin kademesinde)

| Ref | Adet | Parça | LCSC | JLC | Stok | 100 ad. $ | 100 set birim $ | Not |
|---|---|---|---|---|---|---|---|---|
| M1aH…M4cL | 24 | ME7170 30 V 110 A 2.6 mΩ (MATSUKI) | C2841360 | ext | **168** | 0.299 | 0.220 | **100 sete yetmez** (2400 lazım). 5 sete yeter (120) |
| U11…U41 | 4 | EFM8BB21F16G-C-QFN20R | C80713 | ext | 59 440 | 0.794 | 0.794 | Tüpteki QFN20 C1339974 stokta yok |
| U12…U42 | 4 | FD6288Q → **JSM6288Q** | C19077370 | ext | 10 630 | 0.273 | 0.273 | FD6288Q'nun bütün kodları stokta yok (C328453, C97677, C7466367) |
| U1 | 1 | JW5026SOTB#TRPBF | C185109 | ext | 7 208 | 0.267 | 0.267 | |
| U2 | 1 | INA199C1DCKR | C2155860 | ext | 3 003 | 0.532 | 0.532 | |
| U0 | 1 | AMS1117-3.3S SOT-89 (UMW) | C347256 | ext | 418 674 | 0.037 | 0.037 | Basic AMS1117 yalnız SOT-223 |
| D00 | 1 | SMDJ28CA (Brightking) | C310121 | ext | 1 660 | 0.239 | 0.239 | Littelfuse C224072: 191 stok |
| J0 | 1 | SM08B-SRSS-TB (JST) | C160407 | ext | 181 481 | 0.259 | 0.259 | |
| D13…D45 | 12 | 1N4148WT SOD-523 | C27748 | ext | 67 879 | 0.016 | 0.013 | |
| L00 | 1 | 6.8 µH 1210 NLCV32T-6R8M-EF | C250230 | ext | 11 606 | 0.049 | 0.049 | Akım değeri `guc-elektronigi` |
| R00, R000 | 2 | 1 mΩ 2512 RLM25FEER001 | C316227 | ext | 4 854 | 0.053 | 0.053 | E2: güç sınırı |
| C1…C60 | 29 | 22 µF 35 V X5R 1206 | C6119969 | ext | 14 347 | 0.197 | 0.135 | E4 |
| C00, C01 | 2 | 100 nF 50 V 0402 | C307331 | basic | | 0.009 | 0.009 | |
| C02 | 1 | 4.7 µF 35 V 0603 | C307467 | ext | | 0.033 | 0.033 | |
| C03 | 1 | 10 µF 10 V 0402 | C315248 | ext | | 0.030 | 0.030 | |
| C04, C11… | 9 | 100 nF 16 V 0402 | C1525 | basic | | 0.003 | 0.003 | |
| C05 | 1 | 1 nF 50 V 0402 | C1523 | basic | | 0.004 | 0.004 | |
| C13…C45 | 12 | 1 µF 0402 (25 V) | C52923 | basic | | 0.004 | 0.004 | |
| R0, R02 | 2 | 90.9 k 0402 | C26989 | ext | | 0.001 | 0.001 | |
| 10 k / 22 Ω / 220 Ω / 3.3 k / 1 k | 29 / 26 / 4 / 12 / 16 | 0402 | C25744 / C25092 / C25091 / C25890 / C11702 | basic | | ≤ 0.003 | | |
| R? (3 k) | 4 | 3 k 0402 | C25784 | ext | | 0.001 | | E6 |

Toplam: 26 satır, 25 farklı kod, **16 extended**.

### 2.3 fmu — taban kodlar

| Ref | Adet | Parça | LCSC | JLC | Stok | 100 ad. $ | Not |
|---|---|---|---|---|---|---|---|
| U0 | 1 | STM32F405RGT6 (ST) | C15742 | ext | **526** | 4.957 | 100 sete yeter, 1000 sete yetmez |
| U7 | 1 | ICM-42688-P (TDK) | C1850418 | ext | 766 | **18.99** | Kıtlık fiyatı. §4 |
| U6 | 1 | BMP388 (Bosch) | C779278 | ext | 15 531 | 4.911 | |
| U2 | 1 | AT7456E HTSSOP-28-EP | C82351 | ext | 22 439 | 1.899 | MAX7456 ile pin uyumlu (`lib/datasheet/MAX7456_AT7456E.pdf`). Şematikte TSSOP28: alt ped (EP) ayak izine eklenmeli |
| U5 | 1 | W25Q128JVSIQ | C97521 | **basic** | 69 118 | 1.588 | |
| U3, U4 | 2 | TPS54202DDCR | C191884 | ext | 23 466 | 0.113 | Şematikte "TPS54202H" yazıyor; JLC'de yalnız TPS54202DDCR var, ikisi farklı parça mı, `guc-elektronigi` |
| U8 | 1 | ME6211C33M5G-N [varsayım] | C82942 | ext | 356 218 | 0.051 | Şematikte yok |
| U1 | 1 | NUF2042XV6T1G | C90707 | ext | 4 784 | 0.246 | |
| J1 | 1 | USB-C GCT USB4110-GF-A | C5143397 | ext | 2 791 | 0.825 | |
| J0, J1b | 2 | SM08B-SRSS-TB (JST) | C160407 | ext | 181 481 | 0.227 | |
| J2, J4, J5 | 3 | SM04B-SRSS-TB (JST) | C160404 | ext | 57 943 | 0.154 | |
| J3 | 1 | SM06B-SRSS-TB (JST) | C160405 | ext | 19 571 | 0.585 | |
| J | 1 | SM03B-SRSS-TB → **ZX-SH1.0-3PWT** (Megastar) | C7430445 | ext | 94 490 | 0.048 | JST SM03B (C160403) stokta yok. SH 1.0 yatay, ayak izi aynı sınıf, kontrol `pcb-muhendisi` |
| Y0 | 1 | 24 MHz XRCGB24M000F3A00R0 (Murata) | C194420 | ext | 11 757 | 0.347 | |
| Y2 | 1 | 27 MHz X322527MSB4SI (YXC) | C9008 | ext | 101 312 | 0.088 | |
| U9 / Q10 | 1 / 1 | AO3401A / AO3400A | C15127 / C20917 | basic | | 0.066 / 0.072 | |
| D9 | 1 | MM3Z10VT1G (onsemi) | C39057 | ext | 1 068 | 0.039 | |
| F9 | 1 | CFS12V3T5R0 PTC 1206 | C163128 | ext | 24 264 | 0.032 | |
| SW80 | 1 | TS-1010-S26 (JXTCONN) | C42420270 | ext | 31 696 | 0.025 | Şematikteki kod. MPN alanı TL3330AF260QG yazıyor, kod başka üreticinin parçası: MPN düzeltilmeli |
| L32, L42 | 2 | 10 µH SWPA4030S100MT 4×4 | C38117 | ext | 48 027 | 0.049 | 5 V 2 A için doyma akımı yetmeyebilir, `guc-elektronigi` (fark < 0.1 $) |
| LED×4 | 4 | KT-0603R | C2286 | basic | | 0.008 | |
| Pasifler | 68 | 0402/0603/0805/1206 | CSV | 22 satır: 16 basic, 6 ext | | | 47 µF 0805 C16780 6.3 V: hangi rayda olduğu kontrol edilmeli |

Toplam: 44 satır, **24 extended**.

## 3. PCB (JLCPCB, **tahmin**)

JLC fiyat hesaplayıcısı (sipariş arayüzü) bu oturumda yanıt vermedi. Değerler yayımlanmış verilere dayanan **tahmindir**: JLC 4 katman 50 × 50 mm 5 adet kampanyası 2 $, yalnız 1 oz ([JLC blog](https://jlcpcb.com/blog/free-assembly-for-1-6-layer-pcbs-and-discounts-on-8-20-layer-pcba)). JLC örneği 100 × 100 mm, 100 adet, 4 katman 1 oz için 70.6 $ verir (2024). Bir forum teklifinde 4 katman 2 oz ≈ 1 oz × 2 ([PicBasic forum](https://www.picbasic.co.uk/forum/showthread.php/26823-Voltage-regulation-circuit-12V-to-5V-in-5A-range?p=156711)). Atlas PCB 2 oz için +%15–25 diyor ([Atlas PCB](https://atlaspcb.com/blog/multilayer-pcb-cost-2026-pricing-analysis)). 2 oz dış katman 4 katmanda belirli dizilimlerle sunuluyor ([JLC bakır kalınlığı](https://jlcpcb.com/help/article/jlcpcb-copper-weight)).

| Kart | Özellik | 5 adet (sipariş) | 100 adet (sipariş) | $/kart 5 / 100 | Aralık (100) |
|---|---|---|---|---|---|
| esc55a | 41.25 × 47.75 mm, 4 katman, dış 2 oz / iç 0.5 oz, 1.6 mm, HASL kurşunsuz, yeşil | ~30 $ | ~80 $ | 6.00 / **0.80** | 0.60–1.10 |
| fmu | 36 × 36 mm [varsayım], 4 katman 1 oz, 1.6 mm, HASL | 2 $ (kampanya) | ~25 $ | 0.40 / **0.25** | 0.20–0.40 |

Notlar:
- esc55a'da via deliği 0.2 mm (E9). JLC'de 0.3 mm altı via ek ücretlidir (tahmin): taşımada **0.3 mm** önerilir (`pcb-muhendisi`).
- fmu'da LGA IMU/baro için ENIG düşünülürse +~0.1–0.2 $/kart (tahmin).
- 1000 set için tahmin: esc 0.45 $/kart, fmu 0.12 $/kart.
- Panelleme JLC'de PCB fiyatını alan üzerinden belirgin düşürmez (cezeri notu: "maliyet avantajı olmadı"). fmu'nun 100 sette Economic dizgiye girebilmesi için gerekir (§4).

## 4. Dizgi (JLCPCB PCBA, 2026-11-06)

| Ücret | Economic | Standard |
|---|---|---|
| Kurulum | 8.18 $ | 25.56 $ tek yüz / **51.12 $ çift yüz** |
| Şablon (stencil) | 1.53 $ | 8.21 $ / 16.42 $ |
| Extended parça yükleme | 3.07 $/tür (preferred muaf) | 1.53 $/tür |
| Lehim noktası (SMT) | 0.0016 $ | 0.0016 $ (≤ 50 000), 0.0013 $ (50–100 k) |
| Paketleme | ücretsiz | ~0.50 $ |
| Sınır | tek yüz; 2–50 adet; 30 adet üstünde fare ısırığı paneli zorunlu | sınırsız, çift yüz |

Kaynak: [JLC PCBA fiyat](https://jlcpcb.com/help/article/pcb-assembly-price), [PCBA SSS](https://jlcpcb.com/help/article/pcb-assembly-faqs). Economic'in 2 oz bakırı kabul edip etmediği yazmıyor; esc55a için Standard varsayıldı. Standard'da basic parça yükleme ücreti olup olmadığı sayfada açık değil; yalnız extended türler için hesaplandı. Sayfadaki "single board assembly surcharge 0.48 $/kart" kalemi hesaba **katılmadı**: hangi siparişte uygulandığı belirsiz, panelle kalkıyor olabilir. Dahil olursa +0.48 $/kart.

| Kart | Taraf | Tür | 5 set (sipariş → $/kart) | 100 set (sipariş → $/kart) |
|---|---|---|---|---|
| esc55a | **Çift yüz zorunlu**: PCB'de 162 parça üstte, 62 parça altta (12 yüksek taraf MOSFET, 29 bulk C, buck, LDO, shunt, TVS) | Standard | 51.12 + 16.42 + 16 × 1.53 + 750 × 5 × 0.0016 + 0.5 = **98.5 $ → 19.70** | **212.5 $ → 2.13** (lehim noktası 1.20 $/kart) |
| fmu | Tek yüz [varsayım: PCB yok] | 5: Economic; 100: Economic, 2'li panel × 50 | 8.18 + 1.53 + 24 × 3.07 + 389 × 5 × 0.0016 = **74.1 $ → 14.82** | **133.2 $ → 1.33** |

Dizgi notları:
- Delikli (THT) parça yok. Motor/pil pedleri ve kablolar kullanıcıya bırakılır, el lehimi ücreti yok.
- ESC'yi tek yüze toplamak 25.56 + 8.21 = 33.8 $/sipariş kazandırır: 100 sette 0.34 $/set, 5 sette 6.8 $/set. Ama 62 parça 41 × 48 mm'de üst yüze sığmaz (tahmin; `pcb-muhendisi`). 100 set için değmez.
- fmu çift yüz çıkarsa (Mamba F405 MK2 çift yüzlü): Standard, 100 sette ~+0.6 $/set, 5 sette ~+11 $/set (tahmin).

## 5. Maliyet azaltma seçenekleri (100 set, S1'e göre $/stack, etkiye göre)

### A. Ekip kararı: gereksinim değişmez (S1b'ye dahil olanlar ✓)

| # | Seçenek | Tasarruf 100 set (5 set) | Risk / kim inceler |
|---|---|---|---|
| A1 ✓ | ESC bulk 22 µF 1206: 29 → 15 adet | **−1.83** (−2.80) | Bulk/dalgalanma, SYS-014 geçici sınırı. **guc-elektronigi incelemeli** |
| A2 ✓ | MOSFET AON6354 (AOS) → **AON6354-HXY** C22367225 (30 V, 2.6 mΩ, 120 A, Qg 24 nC@15 V; ME7170 ile aynı 2.6 mΩ) | **−0.84** (−1.32) | DFN5×6 standart pin dizilimi (S-S-S-G / D). Klon marka. Stok 4 455 / 2 400 lazım (1.9×). **guc-elektronigi incelemeli** |
| A3 ✓ | EFM8BB21 → **EFM8BB51F16G-C-QFN20R** C6547511 (0.598 $) | **−0.79** (−0.99) | QFN20 pin dizilimi BB21 ile aynı değil: yerleşim ve Bluejay hedefi değişir. `gomulu-yazilim` (Bluejay BB51 desteği doğrulanmalı) + `sematik-muhendisi` |
| A4 ✓ | W25Q128JVSIQ → GD25Q128ESIGR C2928891 | −0.61 (−0.63) | Basic → extended. Betaflight JEDEC ID desteği `gomulu-yazilim` doğrulasın |
| A5 ✓ | Baro Tokmas BMP388 → Goertek **SPA06-003** C30589048 (0.485 $, 67 740 stok) | −0.48 (−0.84) | Ayak izi LGA-8 2 × 2.5 (BMP388 LGA-10 değil). Betaflight sürücüsü (SPL06 ailesi) `gomulu-yazilim` doğrulasın; doğrulanmazsa Tokmas BMP388 kalır |
| A6 | 9 V BEC'i (U3 + bobin + R/C) çıkar, 9 V'u 5 V BEC'ten değil doğrudan VBAT pedinden ver | −0.37 | **SYS-041 değişir → müşteri kararı** (B grubuna bakın) |
| A7 | FMU 4 → 2 katman | ~−0.15 (tahmin) | LQFP64 + IMU + 2 buck + USB 36 mm'de; IMU gürültüsü/EMI riski yüksek, kazanç küçük. **Önerilmez** |
| A8 | ESC dizgisini tek yüze topla | −0.34 | Sığmaz (tahmin), ısı yayılımı kötüleşir. **Önerilmez** |
| A9 | Pasifleri basic'e çek (kalan ext pasifler: 90.9 k, 3 k, 7.15 k, 13.7 k, 75 Ω, 4 pF, 4.7 µF 35 V, 10 µF 10 V, 2.2 µF 25 V) | ~−0.10 (yükleme ücreti, 100 sette); 5 sette ~−2 $ | Değer yakın basic'e kaydırma (ör. 90.9 k → 91 k basic yoksa E24); FB dirençlerinde çıkış gerilimi değişir, `guc-elektronigi` |
| A10 | Panelleme (ESC 2'li) | ~0 | JLC PCB alana göre fiyatlıyor; yalnız 0.48 $/kart "tek kart" ücreti uygulanırsa onu kaldırır |

S1'in kendisi de ekip kararıdır (A0): ME7170 → AON6354 AOS (stok), JST → XYECONN SH 1.0 klonları (C54582896 / C51940130 / C56123098), USB-C → TYPE-C-31-M-12 C165948 (ayak izi değişir), 24 MHz Murata → YXC X201624MKB4SI C2682776, NUF2042 → USBLC6-2SC6 C2827654 (SOT-23-6, ayak izi değişir; NUF2042'deki EMI filtresi kalkar), ICM-42688-P TDK → Tokmas, BMP388 Bosch → Tokmas. S0 → S1: −25.1 $/stack. Bunun 16.9 $'ı IMU.

### B. **Müşteri kararı gerekir** (gereksinim değişir)

| # | Seçenek | Tasarruf 100 set (5 set) | Etkilenen gereksinim / risk |
|---|---|---|---|
| B1 | Bulk 29 → 8 adet + kutuda düşük ESR pil kondansatörü (SOR-011 seçenek 1) | −2.84 (−3.72) (A1 yerine, ondan −1.0 fazla) | SOR-011 yanıtı, SYS-014. **guc-elektronigi incelemeli** |
| B2 | **Analog OSD'yi çıkar** (AT7456E + 27 MHz + 2 × 75 Ω) | **−2.10** (−4.82) | SYS-034, **SOR-012 açık**. Analog kullanıcıları kaybedilir |
| B3 | **STM32F405 → APM32F405RGT6** (Geehy) C5290473 | **−1.76** (−2.53) | SYS-030 "resmî STM32F405". Pin uyumlu klon; Betaflight'ta APM32F405 hedefi var (≥ 4.5), USB/DFU ve hedef `gomulu-yazilim` doğrulamalı. Stok 1 779 |
| B4 | Blackbox flash'ı çıkar | −1.60 (−2.33) | SYS-033 (Ö) |
| B5 | Baro'yu çıkar | −1.00 (−1.90); A5 sonrası −0.48 | SYS-032 (Ö) |
| B6 | ICM-42688-P (Tokmas) → **BMI270** (Bosch orijinal) C2836813 1.33 $ | −0.79 (−0.35) | SYS-031: Betaflight'ta BMI270 3.2 kHz, 8 kHz yok. Pin dizilimi farklı. Avantajı orijinal marka (Tokmas riski kalkar) |
| B7 | Akım ölçümünü çıkar (INA199 + 2 shunt) | −0.68 (−1.58) | Akım/mAh okuması kalkar. Pazarda fark yaratma maddesi (pazar §6), E1/E2 de zaten yeniden tasarım ister |
| B8 | 9 V BEC'i çıkar (A6) | −0.37 | SYS-041 (dijital VTX beslemesi) |
| B9 | TVS'yi çıkar | −0.26 | SYS-014 geçici koruma. **Önerilmez** |
| B10 | **Hedefi yeniden tanımla:** PRJ-004'ü S1b ile **≤ 28 $** (özellikler tam) ya da S2a ile **≤ 25 $** (APM32 + BMI270) yap, 15 $ hedefini 1000 set kademesine taşı | — | PRJ-004, MUS-007. 70 $ satışta S1b ile maliyet/fiyat ≈ %39 |

Hepsi birden (S2: A1–A5 + B1–B7): **19.53 $/stack** (100 set). 15 $ yine tutmuyor. Farkın yapısı: ESC'de kanal başına MCU + sürücü + 6 MOSFET (4 × ~1.6 $ ≈ 6.4 $), FMU'da MCU (≥ 2.8 $), dizgi (~3.2 $), PCB (~1 $). Bunlar özellik kesilerek düşmez.

## 6. Tedarik riskleri

| Parça | Durum | Risk | Öneri |
|---|---|---|---|
| **ME7170** C2841360 / C709757 | Stok 168 / 10; 100 set için 2 400 lazım | **Yüksek**: 100 set üretilemez | AON6354 (AOS, 8 899) ya da AON6354-HXY (4 455). **guc-elektronigi incelemeli**: 30 V V_DS, 6S LiHV 26.1 V ve geçici tepe 35 V (sistem.md varsayımı) için **yetersiz pay**. 40 V seçenek: JSMSEMI **SHYG015N04LS1C2** C49206918 (40 V, 1.1 mΩ@10 V, Qg 87 nC, 0.286 $@500, stok 4 697) ya da HUAYI HYG015N04LS1C2 C2874970 (0.317 $, 11 288). Maliyet etkisi HXY'ye göre **+4.1 $/stack**. Ucuz 40 V KNY3404D C7465103 (0.088 $) 5.2 mΩ ile kayıp ×2 |
| **FD6288Q** | Bütün kodlar stok 0 | Yüksek (orijinal) | **JSM6288Q** C19077370 (veri sayfası repoda; pin uyumu `guc-elektronigi` + `sematik-muhendisi` teyit). Alternatif JSM6288Q1 C52196409 (11 783) |
| **ICM-42688-P** TDK C1850418 | 18.99 $, stok 766 | **Fiyat**: tek başına hedefi aşıyor | Tokmas klonu C54308212 (2.12 $, 2 255): kalite/kimlik riski. 5 set prototipte TDK ile karşılaştırma testi. Ya da BMI270 (B6). JLC global sourcing ile dağıtımcıdan TDK orijinal fiyatı sorulmalı (doğrulanmadı) |
| STM32F405RGT6 C15742 | Stok 526, 4.96 $ | Orta: 100 sete yeter, 1000'e yetmez | APM32F405 (B3); GD32F405 C99031 Betaflight'ta desteklenmez |
| BMP280 (Bosch) | Stok 0 | Yedek parça kullanılamaz | U6 BMP280 alternatifi şematikten kaldırılsın ya da SPA06-003 olsun |
| MAX7456 | Stok 0 | | AT7456E (pin uyumlu, EP'li kılıf) |
| JST SM03B-SRSS-TB | Stok 0 | | ZX-SH1.0-3PWT C7430445 |
| SMDJ28CA | Brightking 1 660 / Littelfuse 191 | Düşük–orta | Yeter (100 lazım). Gerilim seçimi E4, `guc-elektronigi` |
| INA199C1DCKR | 3 003, tek kaynak (TI) | Orta | Yeter (100). E1 yeniden boyutlandırmada INA199A1 vb. ayrıca fiyatlanır |
| XY-SM08B-SRSS-TB C54582896 | 2 000 | Düşük (300 lazım) | Alternatif JST C160407 (181 481) |
| MM3Z10VT1G (onsemi) C39057 | 1 068 | Düşük | TECH PUBLIC C42370498 (5 861) |
| Tokmas / HXY / XYECONN / Megastar | Yerli muadil markalar | Kalite tutarlılığı | Prototipte gelen kart kontrolü; seri üretimde tek parti alım |

Kullanımdan kalkma (EOL) bilgisi JLC/LCSC arayüzünde yok. Hiçbir parçada "discontinued" işareti görülmedi.

## 7. Şematiğe işlenecek LCSC alanları (`sematik-muhendisi`, KiCad'e taşımada)

Önerilen (S1 + S1b) kodları CSV'nin `lcsc_oneri` sütunundadır. Özet:

| Kart | Ref | Değişiklik |
|---|---|---|
| esc | M1aH…M4cL | LCSC **C22367225** (AON6354-HXY) ya da **C404363** (AON6354). 40 V kararı çıkarsa **C49206918**. `guc-elektronigi` kararı beklenir |
| esc | U12…U42 | MPN JSM6288Q, LCSC **C19077370** |
| esc | U11…U41 | LCSC **C80713** (BB21) ya da A3 kabul edilirse **C6547511** (BB51, yeni sembol/ayak izi) |
| esc | U1 / U2 / U0 / D00 / J0 / L00 | C185109 / C2155860 / C347256 / C310121 / C54582896 (ya da C160407) / C250230 |
| esc | R00, R000 | C316227 |
| esc | C1…C60 | C6119969 (adet A1/B1 kararına göre) |
| esc | pasifler | CSV'deki kodlar (basic: C1525, C307331, C52923, C1523, C25744, C25092, C25091, C25890, C11702) |
| esc | R? ×8 | Numaralanacak (E6); 3 k C25784, 1 k C11702 |
| fmu | U0 | Tek parça; C15742 (ya da B3 ile C5290473) |
| fmu | U7 | C54308212 (Tokmas) ya da C1850418 (TDK); B6 ile C2836813 |
| fmu | U6 | Tek parça: C30589048 (SPA06-003, yeni ayak izi) ya da C54582187; BMP280 kaldır |
| fmu | U2 | MPN AT7456E, LCSC **C82351**, HTSSOP-28-EP ayak izi |
| fmu | U5 | C97521 (ya da C2928891) |
| fmu | U8 (yeni) | **3.3 V regülatörü eklenmeli** (SYS-042), öneri ME6211C33M5G-N C82942 |
| fmu | J1 (USB-C) | C165948 TYPE-C-31-M-12 (ayak izi değişir) ya da C5143397 |
| fmu | J1 (SM08B) | Yeni ref (ör. J6); C54582896 |
| fmu | J2/J4/J5, J3, J | C51940130, C56123098, C7430445 |
| fmu | Y0 / Y2 | C2682776 (ya da C194420) / C9008 |
| fmu | U1 | C2827654 (USBLC6-2SC6, SOT-23-6) ya da C90707 |
| fmu | SW80 | MPN alanı TS-1010-S26 olarak düzeltilsin (LCSC C42420270) |
| fmu | C60/C61 ×2, C? ×3, R? ×2 | Numaralanacak |
| fmu | Bütün Digi-Key kodları (F6) | LCSC koduyla değiştirilsin (CSV) |

## 8. Açık noktalar

1. **PCB fiyatı tahmin.** JLC hesaplayıcısından gerçek teklif alınmalı: esc 2 oz 4 katman (5 ve 100 adet), fmu 1 oz.
2. JLC Economic dizginin 2 oz ve 4 katmanı kabul edip etmediği; Standard'da basic yükleme ücreti; 0.48 $/kart "tek kart" ücreti.
3. MOSFET gerilim sınıfı (30 V ↔ 40 V): `guc-elektronigi`. +4 $/stack etkisi olabilir.
4. Tokmas ICM-42688-P / BMP388 kimlik ve Betaflight uyumu: prototipte test (`test-muhendisi`).
5. fmu PCB'si yok: tek/çift yüz ve ölçü (36 × 36 mm) varsayım; dizgi ±0.6 $/set oynayabilir.
6. Müşteri soruları (yönetici üzerinden): PRJ-004 hedefinin yeniden tanımı (B10), SOR-012 (OSD), SOR-011 (kutuda kondansatör), SYS-030 (APM32), SYS-031 (BMI270).

## 9. Rev B (ESC)

> **Tarih:** 2026-11-10. **Kaynak:** fiyat, stok, basic/extended JLCPCB parça arayüzü (`selectSmtComponentList`), 2026-11-10'da okundu. Veri sayfası bağlantıları LCSC ürün arayüzünden (`wmsc.lcsc.com/ftps/wm/product/detail`), aynı gün. Dizgi ve PCB kuralları §3–§4 ile aynı: Standard, çift yüz, lehim noktası düz 0.0016 $. Bu tutucu bir varsayım; JLC'nin 50 k nokta üstü kademesi (0.0013 $) 1000 sette ESC'yi ~0.2 $/kart düşürür. PCB değerleri tahmin.
> **Girdi:** `docs/rapor/guc-ip03.md` §0, §10, §11 (G1–G14, G20). Şematik henüz işlenmedi (`sematik-muhendisi` paralel çalışıyor). Bu yüzden BOM, önerilen parça listesine göre kuruldu. Satır satır döküm: [`boards/esc55a/bom-revb.csv`](../boards/esc55a/bom-revb.csv). S1b ile karşılaştırma için S1b ESC listesi aynı gün yeniden fiyatlandı: 12.95 $/kart (2026-11-06'da 13.01 $).
> **MCU varsayımı:** Rev B'de **EFM8BB21 (C80713)** kullanıldı. Bu, şematikte olan ve SYS-051'in istediği parça. S1b'deki A3 (BB51) `gomulu-yazilim` tarafından doğrulanmadı. BB51 ayrı satırda gösterildi. `guc-ip03` §10'daki 31.2 $ hesabı BB51 varsayıyor.

### 9.1 Rev B ESC BOM özeti (S1b'ye göre değişenler)

| Ref | Adet | Rev B parça | LCSC | JLC | Stok (11-10) | 100 set birim $ | S1b'den | Kart Δ $ (100 set) |
|---|---|---|---|---|---|---|---|---|
| M1aH…M4cL | 24 | BLP016N04LC-Q (Belling) 40 V | C49328363 | ext | **3 953** | 0.1823 (2400 ad.) | AON6354-HXY | **+1.64** |
| U11…U41 | 4 | EFM8BB21F16G-C-QFN20R | C80713 | ext | 60 000 | 0.7658 | BB51 (A3 onaysız) | +0.67 |
| U12…U42 | 4 | **JSM6288Q1** | C52196409 | ext | 11 948 | 0.3486 | JSM6288Q | +0.30 |
| U2 | 1 | **INA240A3DR** (SOIC-8) | C2060584 | ext | 1 511 | 1.7901 | INA199C1 | +1.21 |
| R00 | 1 | 0.1 mΩ 3920 10 W HoLRS3920 (Milliohm) | C55113241 | ext | 3 845 | 0.2947 | 2 × 1 mΩ 2512 (R00, R000) | +0.19 |
| D00 | 1 | SMDJ24CA (DOWO) | C284061 | ext | 2 444 | 0.2018 | SMDJ28CA | −0.04 |
| C1…C60 | 15 | 10 µF 50 V X7R 1206 CL31B106KBHNNNE | C89632 | ext | 551 138 | 0.1205 | 15 × 22 µF 35 V | −0.27 |
| C02 | 1 | 4.7 µF 50 V 0805 | C98192 | ext | 176 733 | 0.0360 | 4.7 µF 35 V 0603 | +0.00 |
| C03 + C_LDO (yeni) | 2 | 10 µF 16 V 0603 (FH) | C70225 | ext | 131 539 | 0.0570 | C03 10 µF 10 V 0402 | +0.08 |
| L00 | 1 | 10 µH SWPA3015S100MT (Sunlord) | C45403 | ext | 16 256 | 0.0385 | NLCV32T-6R8M | −0.01 |
| sürücü VCC (yeni) | +4 | 1 µF 25 V 0402 | C52923 | **basic** | 11 M | 0.0044 | (12 → 16 adet) | +0.02 |
| R_G | 24 | 10 Ω 0402 | C25077 | **basic** | 3.2 M | 0.0008 | 22 Ω (C25092) | −0.01 |
| R99…R106 | 8 | DNP (E6, G20) | — | — | — | — | 3 k / 1 k | −0.01 |
| Değişmeyen | | JW5026, AMS1117 SOT-89, J0 XY-SM08B, 1N4148WT ×12, 100 nF / 1 nF / 90.9 k / 10 k / 220 Ω / 22 Ω ×2 / 3.3 k / 1 k | | | | | | 0 |
| **Komponent** | **182 parça / 25 kod** | | | **15 ext** | | | S1b 186 parça, 16 ext | **+3.79 → 13.86 $** |

### 9.2 ESC kart maliyeti ($/kart)

| ESC Rev B | Komponent | PCB (tahmin) | Dizgi | **Toplam** | S1b'ye göre (aynı gün fiyatı) |
|---|---|---|---|---|---|
| **5 set** | 19.02 | 6.00 | 19.34 | **44.36** | +5.04 (S1b 39.32) |
| **100 set** | 13.86 | 0.80 | 2.06 | **16.72** | **+3.77** (S1b 12.95; belgedeki 13.01'e göre +3.71) |
| **1000 set** | 12.09 | 0.45 | 1.24 | **13.77** | +3.31 (S1b 10.46). **BLP016 stoğu 1000 sete yetmez**, NTMFS ile **15.34** |
| 100 set, MOSFET yedek NTMFS5C430NLT1G (C194661) | 14.83 | 0.80 | 2.06 | 17.68 | +4.73 |
| 100 set, MCU BB51 (A3) | 13.19 | 0.80 | 2.06 | 16.04 | +3.09 |

**Dizgi (Standard, çift yüz):** Extended tür sayısı **16 → 15**. Türlerin çoğu yer değiştiriyor; 3 k (C25784) DNP olduğu için tür olarak düşüyor. 10 Ω basic. Lehim noktası 722 → 716: shunt −2, INA240 +2, 4 × 1 µF +8, LDO kondansatörü +2, DNP −16. Sipariş başına −1.53 $ (100 sette −0.015 $/kart, 5 sette −0.31 $/kart). **Kart çift yüzlü kalıyor.** 12 yüksek taraf MOSFET ve 15 bulk alt yüzde. Yeni 3920 shunt (10 × 5 mm) ile SOIC-8 INA240'ın yerleşimi `pcb-muhendisi`'nde. Tek yüze toplama yine önerilmez (§4). SYS-091'in "extended ≤ 10/kart" önerisi karşılanmıyor (15). §9.7'deki seçeneklerle 11'e iner.

### 9.3 Stack toplamı (fmu S1b + esc55a Rev B)

| $/stack | 5 set | **100 set** | 1000 set |
|---|---|---|---|
| esc55a Rev B (BLP016, BB21) | 44.36 | **16.72** | 13.77 (stok yetmez; NTMFS ile 15.34) |
| fmu S1b (§1; 5 ve 1000 set türetilmiş*) | ~34.24 | 14.37 | ~12.51 |
| **Stack, FMU S1b ile** | **~78.6** | **31.09** | ~26.3 (NTMFS ile ~27.9) |
| FMU İP-03 değişiklikleri G7–G10 (2 × SY8303A, bobinler, 3.3 V LDO): `guc-ip03` §10 tahmini, **ayrı satır** | ~+0.6 | **+0.6** | ~+0.6 |
| **Stack, FMU İP-03 dahil** | **~79.2** | **31.69** | ~26.9 (NTMFS ile ~28.5) |
| Değişken: MCU BB51 (A3) | | 31.01 | |
| Değişken: MOSFET NTMFS (yedek) | | 32.65 | |

\* fmu 5 set ≈ 73.61 − S1b ESC (5 set, A1–A3 çıkarılarak) ≈ 34.24. fmu 1000 set ≈ 22.97 − S1b ESC 1000 (bu gün hesaplanan 10.46). İkisi de ±0.5 $. fmu 1000 sette STM32F405 stoğu (526) zaten yetmez (§6).

### 9.4 Hedeflere göre durum (100 set)

| Hedef | Rev B (BLP016, BB21) + FMU İP-03 = **31.69 $** | Durum |
|---|---|---|
| **PRJ-004 / DT-001 ≤ 28 $** | **+3.69 $** | **Karşılanmıyor.** Gereksinim değişikliği olmadan ulaşılamaz. ESC tarafındaki güvenli tasarruflar (§9.7) en çok ~−0.9 $ getirir (BB51 ile ~−1.5 $). 28 $ ancak müşteri kararlarıyla tutar: B3 APM32F405 −1.76, B6 BMI270 −0.79, INA186A3 −1.22. Hepsiyle ≈ 26.4 $ |
| **≤ 32 $ alternatifi** | **−0.31 $ pay** | **Karşılanıyor, pay çok dar.** MOSFET'ler NTMFS'e geçerse 32.65 $ ile aşılır. PCB iç katmanı 1 oz'a çıkarsa (G19, tahmin +0.1–0.2 $/kart) ya da JLC "tek kart" ücreti uygulanırsa (+0.48 $/kart) da aşılır. §9.7'deki güvenli seçeneklerle ≈ 30.8 $ |
| RSK-004 | | Güncellenmeli: SYS-014 uyumlu tasarım ≤ 28 $'ı tutmuyor (`guc-ip03` §0 ile tutarlı) |

### 9.5 Stok ve tedarik riskleri (SYS-091: stok ≥ 2 × 100 set ihtiyacı)

| Parça | 100 set ihtiyaç / 2× | Stok 2026-11-10 | SYS-091 | Not |
|---|---|---|---|---|
| **BLP016N04LC-Q** C49328363 | 2 400 / 4 800 | **3 953** (ön satış 3 876) | **✗** | 100 sete yeter, 2× kuralı ve 1000 set tutmaz. Tek kaynak (Belling). Öneri: 5 set prototipte **hem BLP016 hem NTMFS5C430NL** ile kart yapıp ikisini nitelendirmek (ör. 3 + 2 set). 100 set kararı verilince BLP016'dan **2 500 adet** JLC parça stoğuna önceden alınır: stoğu ayırır ve 2 500 kademesi (0.1666 $) 2 400 × 0.1823'ten ucuzdur, kart başına −0.21 $ ve 100 yedek. Aksi halde NTMFS (stok 173 493): +0.97 $/kart |
| NTMFS5C430NLT1G C194661 | 2 400 / 4 800 | 173 493 | ✓ | Yedek. 100 sette 0.2226 $ (1500+ kademesi; daha alt kademe yok) |
| INA240A3DR C2060584 | 100 / 200 | 1 511 | ✓ | 1000 sette 2× kuralı tutmaz. Tek kaynak (TI) |
| INA199C1DCKR C2155860 | — | **424** (11-06'da 3 003) | (çıkarılıyor) | Hızlı tükeniyor. Rev B'de kullanılmıyor, bütçe seçeneği INA186A3 (C2058245, stok 4 051) |
| HoLRS3920 shunt C55113241 | 100 / 200 | 3 845 | ✓ | Tek kaynak (Milliohm). Veri sayfası repoda |
| SMDJ24CA C284061 | 100 / 200 | 2 444 | ✓ | DOWO. Yedek 5.0SMDJ24CA C284111 (4 253, 0.32 $) |
| JSM6288Q1 C52196409 | 400 / 800 | 11 948 | ✓ | |
| XY-SM08B C54582896 | 100 / 200 | 2 000 | ✓ | JST C160407 yedek |
| JW5026 C185109 | 100 / 200 | 4 308 | ✓ | 11-06'da 7 208: düşüyor, izlenmeli |
| Diğerleri | | ≥ 60 000 | ✓ | |

**Veri sayfası notu (`guc-elektronigi`'ne):** Sunlord SWPA serisi veri sayfasında (LCSC kopyası, 2014 sürümü) SWPA3015S100MT için **I_sat 0.72 A, I_rms 0.77 A, DCR 0.25 Ω** yazıyor. `guc-ip03` G11'de I_sat 0.92 A kullanılmış (dağıtımcı verisi). 0.47 A tepe akımla yine %65'te, sorun yok ama belgede düzeltilmeli.

### 9.6 İndirilen veri sayfaları (`lib/datasheet/`, hepsi `file` ile PDF olarak doğrulandı)

| Dosya | Kaynak | Sayfa |
|---|---|---|
| `Belling-BLP016N04LC-Q_C49328363.pdf` | datasheet.lcsc.com/…/60e9b7bb6d64f081d184b353ffc14825.pdf | 11 |
| `onsemi-NTMFS5C430NLT1G_C194661.pdf` | datasheet.lcsc.com/…/2a2a6d89c0f0698c54cd937bf00b2745.pdf | 7 |
| `JSMSEMI-JSM6288Q1_C52196409.pdf` | datasheet.lcsc.com/…/8e66a7cf2679ad9374949075990da53d.pdf (görüntü PDF) | 15 |
| `TI-INA240A3DR_C2060584.pdf` | ti.com/lit/ds/symlink/ina240.pdf (SBOS662C). LCSC'deki PDF yalnız seçim kılavuzu, alınmadı | 39 |
| `DOWO-SMDJ24CA_C284061.pdf` | datasheet.lcsc.com/…/f3a866763da2bf38848a6c16e1beeff3.pdf | 4 |
| `Milliohm-HoLRS3920-10W-0.1mR_C55113241.pdf` | datasheet.lcsc.com/…/f0d59f0eaa1bba956e553f01ceae8df7.pdf (Çince) | 7 |
| `Sunlord-SWPA-series_SWPA3015S100MT_C45403.pdf` | atta.szlcsc.com/upload/public/pdf/source/20140723/1457707156433.pdf (LCSC'nin Çin sitesi; C45403 için LCSC ürün arayüzü PDF vermedi) | 20 |

`guc-ip03` §1'deki diğer PDF'ler (ME7170, JW5026, INA199, AMS1117, SY8303A …) bu görevde indirilmedi. RSK-002 için ayrıca eklenmeli.

### 9.7 ESC'de ek maliyet azaltma (Rev B'ye göre, 100 set $/kart; 5 set parantezde)

| # | Seçenek | Tasarruf | Güvenlik / kim inceler |
|---|---|---|---|
| R1 | C03 + LDO çıkışı: C70225 (10 µF **16 V**, ext) → **CL10A106MA8NRNC 10 µF 25 V X5R 0603 C96446 (basic)** | **−0.08** (−0.38) | Aynı kılıf ve dielektrik, gerilim sınıfı daha yüksek (8 V'ta DC öngerilim kaybı daha az). Güvenliği bozmaz, yalnız `sematik-muhendisi` kodu girer |
| R2 | BLP016'yı 2 500 adet olarak önceden al (2 500 kademesi) | **−0.21** | Parça aynı. Stok ayırma da sağlar (§9.5) |
| R3 | Bulk 15 × X7R C89632 → 15 × **X5R 10 µF 50 V 1206 C13585 (basic)** | **−0.49** (−0.87) | X5R +85 °C; kart 95 °C'ye çıkabilir. `guc-ip03` §6.3: yalnız ölçümde kart ≤ 85 °C çıkarsa. **guc-elektronigi incelemeli** (prototip ısıl ölçümüne bağlı) |
| R4 | Bulk 15 → 12 adet | −0.36 | Dalgalanma akımı adet başına ~1 → 1.25 A_rms, set kondansatörüne bağlılık artar. **guc-elektronigi incelemeli**. Önceliği düşük |
| R5 | Bootstrap 1N4148WT SOD-523 (ext) → **1N4148WS SOD-323 C2128 (basic)** | −0.06 (−0.33) | Aynı diyot sınıfı (100 V, t_rr 4 ns), ayak izi büyür (12 adet). **guc-elektronigi incelemeli** + `pcb-muhendisi` yer |
| R6 | R0/R02 90.9 k (ext): R0 (EN çekme) → 100 k C25741 basic, R02/R01 (FB) basic çifte | −0.02 (−0.31) | FB oranı PVDD'yi değiştirir (100 k/10 k → 8.8 V). **guc-elektronigi incelemeli** |
| R7 | Pasif birleştirme (100 nF 50 V C307331 ile 100 nF 16 V C1525 tek kod vb.) | ≈ 0 | İkisi de basic, yükleme ücreti yok, fiyat farkı < 0.01 $. Değmez |
| R8 | MCU EFM8BB51 (A3) | −0.67 (−0.87) | Güvenlik etkisi yok. SYS-051 değişir (DT). `gomulu-yazilim` Bluejay BB51 doğrulaması + yeni sembol/ayak izi |
| R9 | INA240A3 → INA186A3IDCKR C2058245 | −1.22 | **Müşteri kararı**: SYS-021 doğruluğu gevşer (`guc-ip03` §5.2) |
| — | AMS1117 SOT-89 (ext) → SOT-223 C6186 (basic) | +0.10 | Basic parça daha pahalı. Önerilmez |

- **Güvenli ve hemen uygulanabilir (R1 + R2):** −0.29 $ → stack **31.40 $**.
- **guc-elektronigi onayıyla (R3 + R5 + R6 eklenince):** toplam −0.86 $ → **30.83 $**. Extended tür 15 → 12 (R1, R3, R5, R6 ile 11).
- R8 de eklenirse **30.16 $**, R9 de eklenirse **28.94 $**. Hâlâ 28 $'ın üstünde. Kalan fark FMU tarafında: B3 APM32F405 ile 27.2 $, B6 BMI270 ile de 26.4 $ (müşteri kararları).

### 9.8 Şematiğe işlenecek LCSC alanları (Rev B ESC, `sematik-muhendisi`)

M1aH…M4cL **C49328363**, U12…U42 **C52196409**, U2 **C2060584**, R00 **C55113241** (R000 sil), D00 **C284061**, C1…C60 15 adet **C89632**, C02 **C98192**, C03 ve yeni LDO çıkış kondansatörü **C70225** (R1 kabul edilirse **C96446**), L00 **C45403**, 4 yeni sürücü VCC kondansatörü **C52923**, 24 kapı direnci **C25077** (10 Ω), R99–R106 DNP, U11…U41 **C80713**. Değişmeyen kodlar §7'deki gibi.

### 9.9 Açık noktalar (Rev B)

1. BLP016 stoğu 2× kuralını karşılamıyor. 100 set öncesi MOSFET kararı ve önceden alım gerekiyor (§9.5).
2. PCB iç katman 1 oz (G19) için JLC teklifi alınmadı. Maliyet etkisi tahmini +0.1–0.2 $/kart, tabloya katılmadı.
3. JLC "tek kart" ücreti (+0.48 $/kart) belirsizliği sürüyor. Uygulanırsa 32 $ payı kalmaz.
4. A3 (BB51) ve INA186A3 kararları açık. 28 $ hedefi için müşteri kararları (B3, B6, R9) gerekiyor.

### 9.10 Yüksek sıcaklık güncellemesi (2026-11-11)

> **Girdi:** müşteri 2026-11-11 "kart yüksek derecelere çıkar". Kural [öneri, `gereksinim-muhendisi` yazıyor]: ESC'deki her parça ≥ 125 °C hedef, en az 105 °C; seramik en az X7R (X5R yok); elektrolitik yok. Isıl girdi `guc-ip03` §2.5: kart ≈ 95 °C, MOSFET kılıfı ≤ 110 °C. **Kaynak:** fiyat/stok JLCPCB parça arayüzü, sıcaklık LCSC parametresi ve `lib/datasheet/` veri sayfaları, 2026-11-11. Satır satır: [`bom-revb.csv`](../boards/esc55a/bom-revb.csv) `sicaklik_C`, `revb2_*` sütunları. Şematik: `tools/esc55a_revb.py` (alan `Temperature`).

**Sınıfı yetmeyen ve değişen parçalar (100 set kademesi):**

| Ref | Adet | Önce (LCSC, sınıf) | Sonra (LCSC) | Sınıf | Stok 11-11 / 2× ihtiyaç | Birim $ önce → sonra | Kart Δ $ |
|---|---|---|---|---|---|---|---|
| U11…U41 | 4 | EFM8BB21F16G-C-QFN20R C80713, T_A −40…85 °C | **EFM8BB21F16I-C-QFN20R C2053222** | T_A −40…125 °C (T_J 130) | 22 629 / 800 ✓ | 0.7658 → 0.8958 | **+0.520** |
| C13…C45, C120…C420 | 16 | 1 µF 25 V X5R 0402 C52923 (basic) | **1 µF 16 V X7R 0402 CCTC TCC0402X7R105K160AT C49210445** (ext) | X7R | 65 773 / 3 200 ✓ | 0.0044 → 0.0053 | +0.014 |
| C03, C07 | 2 | 10 µF 16 V X5R 0603 C70225 | **10 µF 16 V X7R 0805 CCTC TCC0805X7R106K160FT C380347** (0603 → 0805) | X7R | 535 301 / 400 ✓ | 0.0570 → 0.0246 | −0.065 |
| C02 | 1 | 4.7 µF 50 V X5R 0805 C98192 | **4.7 µF 50 V X7R 0805 HRE CGA0805X7R475K500MT C6119944** | X7R | 40 546 / 200 ✓ | 0.0360 → 0.0311 | −0.005 |
| Dizgi | | 15 extended tür | 16 (1 µF X7R extended; 0402 X7R 1 µF basic yok) | | | 1.53 $/sipariş | +0.015 |
| **Toplam** | | | | | | | **+0.48 $/kart** |

Yedekler (şematikte ALT alanları): C49210445 ↔ **1 µF 25 V X7R C53426846** (0.0228 $ @1600; kullanılırsa kart +0.29 $ daha, toplam +0.77 $); C380347 ↔ Samsung CL21B106KOQNNNE C95841 (0.0663 $); C6119944 ↔ CCTC TCC0805X7R475K500FT C20416422 (0.0708 $). 0603 kılıfta ≥ 16 V 10 µF X7R yok (10 V Murata GRM188Z71A106KA73D C2959727 var, C03'ün 8 V'u için yetersiz pay) — C03 ve C07 tek kod kalsın diye ikisi de 0805.

**Maliyet (100 set):**

| | ESC $/kart | Stack $/set (FMU S1b) | Stack $/set (FMU İP-03 dahil) |
|---|---|---|---|
| Rev B (9.2–9.3; C06 eklenerek 16.72) | 16.72 | 31.09 | 31.69 |
| **Rev B + yüksek sıcaklık** | **17.20** | **31.57** | **32.17** |
| Fark | **+0.48** | **+0.48** | **+0.48** |

- C06 (U2 VS 100 nF C1525) BOM'a eklendi: +0.003 $ parça, +2 lehim noktası (718); kartı yuvarlamada değiştirmiyor.
- **≤ 32 $ alternatifi aşılıyor (+0.17 $).** Kurtarma: §9.7 R2 (BLP016 2 500 adet önceden alım, −0.21) → **31.96 $**; R5 1N4148WS SOD-323 C2128 basic (−0.06; LCSC T_J değeri boş, veri sayfasından doğrulanmalı) ve R6 (−0.02) `guc-elektronigi` onayıyla → ≈ 31.9 $.
- **§9.7'de geçersiz kalanlar:** R1 (C96446 X5R) ve R3 (bulk X5R C13585) X5R yasağıyla çelişir, düşüldü. "Güvenli" tasarruf yalnız R2.
- MCU'da daha ucuz 125 °C seçenek yok: EFM8BB51F16I-C-QFN20R C3232998 stok **18** (A3 seçeneği yüksek sıcaklıkta fiilen kapandı); QSOP24 I sürümleri stoksuz.
- 5 sette MCU farkı daha büyük: 4 × (1.2129 − 1.0184) = +0.78 $/kart; extended tür +0.31 $/kart.

**Sıcaklık sınıfı (tüm ESC parçaları):**

| Parça | LCSC | Sınıf | Kaynak | Durum |
|---|---|---|---|---|
| BLP016N04LC-Q (ALT NTMFS5C430NL) | C49328363 (C194661) | T_J −55…175 °C | DS | ✓ |
| JSM6288Q1 | C52196409 | −40…125 °C | LCSC (DS görüntü PDF) | ✓ |
| EFM8BB21F16**I** | C2053222 | T_A −40…125 °C | DS Tablo 4.1 | ✓ (önce G: 85 °C ✗) |
| INA240A3DR | C2060584 | T_A −40…125 °C, T_J 150 | SBOS662 | ✓ |
| JW5026 | C185109 | T_J −40…125 °C | LCSC | ✓ sınırda (T_J); `guc-elektronigi` |
| AMS1117-3.3 (UMW) | C347256 | −40…125 °C | LCSC | ✓; ısıl pay `guc-elektronigi` (≈ 4.8 V × I_3V3) |
| SMDJ24CA | C284061 | T_J −55…150 °C | DS | ✓ (P_PP sıcaklıkla azalır) |
| 1N4148WT | C27748 | T_J −65…150 °C | LCSC | ✓ |
| SWPA3015S100MT | C45403 | −40…125 °C (öz ısınma dahil) | DS s.1 | ✓ |
| HoLRS3920 0.1 mΩ | C55113241 | −55…170 °C | DS s.3 | ✓ (güç azaltma eğrisi DS s.4) |
| J0 XY-SM08B-SRSS-TB (ALT JST) | C54582896 (C160407) | −40…85 °C (JST −25…85) | LCSC | **✗ < 105 °C — değişmedi** |
| Seramikler (tümü X7R) | C89632, C307331, C1525, C1523 + yeni 3 kod | −55…125 °C | EIA X7R | ✓ |
| Dirençler UNI-ROYAL 0402WGF | 7 kod | −55…155 °C | LCSC | ✓ |

**J0 (açık):** LCSC/JLC'de SH 1.0 mm 8 pin yatay 15 klon tarandı (XYECONN, Bossie, XUNPU, Megastar, LXW, SANHI, JXT, BX, HMT, CHUANGYUE …): hepsi −25/−40…85 °C. 105 °C sınıflı 1.0 mm seçenek **Molex Pico-Clasp 501568-0807** (C587867, −40…105 °C, 0.45 $ @100, stok 1 251; dikey 501331-0807 C505340, 0.30 $). SH ile geçmeli değil: FMU konnektörü ve kablo da değişir (`sistem-mimari`, FMU↔ESC arayüzü). Öneri: Rev B'de SH kalır; J0'ı kartın serin kenarına (MOSFET'lerden uzak) koymak (`pcb-muhendisi`) ve prototip ısıl ölçümünde J0 sıcaklığını ölçmek; > 85 °C çıkarsa Pico-Clasp'e geçiş kararı.

## 10. Tasarruf taraması (2026-11-11)

> **Kaynak:** fiyat, stok, basic/extended JLCPCB parça arayüzü (`tools/jlc.py`), 2026-11-11. Sürücü desteği GitHub kaynaklarından aynı gün: Betaflight `src/main/drivers/barometer/barometer_dps310.c`, `barometer_bmp5xx.c`, `drivers/flash_m25p16.c` (etiketler 4.5.2, 4.5.5, 2025.12.5, 2026.6.2); ArduPilot `libraries/AP_Baro/AP_Baro_SPL06.cpp`, `AP_Baro_BMP581.cpp`, `AP_Logger/AP_Logger_Flash_JEDEC.cpp` (Copter-4.5.7, 4.6.3, 4.7.x, master). Veri sayfaları: SPA06-003 (LCSC C30589048, Ver2.0), DPS368 (C3232508). STM32 dış fiyatı web araması (findchips/DigiKey/Future, tarihsiz önbellek), 2026-11-11.
> **Taban:** ESC Rev B + yüksek sıcaklık 17.20 $ + FMU (`boards/fmu/bom-revb.csv`) 17.72 $ = **34.92 $/stack**. Hedef PRJ-004 ≤ 32 $ → gereken ≥ 2.92 $.
> **Yöntem:** 100 set = 100 × karttaki adet kademesi. Dizgi §4: FMU extended tür başına Economic 3.07 $, Standard 1.53 $; ESC Standard 1.53 $; sipariş 100 set. Ham tablo: [`boards/tasarruf-2026-11-11.csv`](../boards/tasarruf-2026-11-11.csv). Şematik ve gereksinimler değiştirilmedi.
> **Sınıflar:** A güvenli (gereksinim değişmez, güç/yazılım incelemesi yok; yalnız `sematik-muhendisi` kod girer). B inceleme gerekir. C müşteri kararı (SYS değişir). KRR-008 (ESC ≥ 125 °C, X5R yok; FMU ≥ 85 °C, X7R) ve SYS-034 analog OSD korunur.

### 10.1 A — güvenli

| # | Kart / ref | Değişiklik | $/stack | Stok / 2× ihtiyaç |
|---|---|---|---|---|
| A1 | ESC M1aH…M4cL | BLP016 C49328363 2 500 adet peşin (2 500 kademesi 0.1664 $) — §9.7 R2 | **−0.21** | 3 903 / 4 800 ✗ (peşin alım stoğu ayırır) |
| A2 | FMU U103 | AMS1117-3.3 C6186 (basic, 0.1485) → UMW **C347222** (0.0385, ext, aynı SOT-223, −40…125 °C; şematikte zaten ALT) | −0.10 | 924 269 ✓ |
| A3 | FMU C302 | 10 nF C1524 (ext) → **C15195** CL05B103KB5NNNC (basic) | −0.02 | ✓ |
| A4 | FMU C206 | VDDA 1 µF C49210445 → 2.2 µF X7R 0603 **C5360821** (C114/C208/C209 ile tek kod) | −0.01 | ✓ |
| A5 | FMU C205 | VDD toplu 4.7 µF C107365 → 10 µF X7R 0805 **C380347** (C112/C404 ile tek kod) | −0.01 | ✓ |
| A6 | FMU D202 | 1N4148WT C27748 (ext) → 1N4148WS SOD-323 **C2128** (basic) | −0.02 | ✓ |
| A7 | FMU dizgi | Economic → **Standard tek yüz**: A2–A6 sonrası 29 extended türde Standard (25.56 + 8.21 + 0.50 + 29 × 1.53 = 78.6 $) Economic'ten (8.18 + 1.53 + 29 × 3.07 = 98.7 $) ucuz; başabaş 16 tür. §4'teki tür ücretleri JLC teklifiyle doğrulanmalı (§8.2) | −0.25 | — |
| | **A toplamı** | FMU extended tür 32 → 29 | **−0.61 → 34.31 $** | |

### 10.2 B — inceleme gerekir

| # | Kart / ref | Değişiklik | $/stack | Stok | Kim inceler, ne kontrol edilir |
|---|---|---|---|---|---|
| **B1** | FMU U302 | Baro DPS368XTSA1 C3232508 (2.78 $) → **Goertek SPA06-003 C30589048** (0.48 $) | **−2.30** | 39 085 ✓ | **gomulu-yazilim:** SPA06-003 PROD_ID 0x11, katsayılar 0x10–0x24 (DS §7.11). BF `barometer_dps310.c` 0x11'i "SPL07_003" olarak tanır ve aynı katsayı düzenini okur (4.5.2'den beri); AP `AP_Baro_SPL06` 0x11'i SPA06 olarak tanır (Copter ≥ 4.6.3; 4.5.7'de yok). Hedef: BF `baro_hardware DPS310`, AP hwdef `BARO SPL06 I2C:0:0x76`. Prototipte iki yazılımda tanınma ve irtifa testi. **pcb-muhendisi:** pin dizilimi DPS368 ile aynı (1 GND, 2 CSB, 3 SDA, 4 SCK, 5 SDO, 6 VDDIO, 7 GND, 8 VDD; LGA-8 2.0 × 2.5, 0.65 mm), ped ölçüsünü Goertek önerisiyle karşılaştır. SDO → GND = 0x76 aynı. *Düzeltme:* §9 sonrası FMU README'deki "SPA06-003 BF'de sürücü yok" bilgisi kaynak koduna göre geçersiz. Yedekler: Tokmas DPS368 C55090144 1.41 $ (aynı ayak izi ve sürücü, −1.37 $, klon riski); Bosch BMP581 C5362283 1.44 $ (−1.34 $, LGA-10 2 × 2, BF yalnız 2026.6+ `bmp5xx`, AP ≥ 4.5) |
| **B2** | ESC U2 | INA240A3DR C2060584 (1.79 $, SOIC-8, ×100) → **INA281B2IDBVR C1517409** (1.27 $, SOT-23-5, ×50, V_CM −4…110 V, −40…125 °C) | **−0.52** | 5 400 ✓ | **guc-elektronigi:** SYS-021 (10–200 A ±%5, < 10 A ±1 A) için B sınıfı ofset/kazanç hatası; CUR 5 mV/A → 280 A = 1.40 V (SYS-020 ✓, çözünürlük yarıya iner); PWM ortak kip geçici bastırımı (INA240'ın üstünlüğü). **gomulu-yazilim:** `ibata_scale` 100 → 200. **pcb-muhendisi:** SOT-23-5 + Kelvin yolları. Reddedilirse INA240A3 kalır |
| B3 | FMU D501 | PMEG3020EH C19268151 → B5819W SL **C8598** (basic, 40 V 1 A) | −0.05 | ✓ | guc-elektronigi: USB'de V_F (≈ 0.45 V @ 0.3 A), 5 V rayı ≈ 4.5 V; AT7456E 4.75 V alt sınırı yalnız USB'de |
| B4 | FMU 5 V FB | 100 k / 13.7 k (ext) → 15 k C25756 / 2 k C4109 (basic) → 5.10 V (4.97–5.23) | −0.02 | ✓ | guc-elektronigi (SYS-040; FB empedansı, R_FS değişmez). 9 V FB'de basic çift yok (47 k / 3.3 k üst sınırda), değişmez |
| B5 | ESC D13…D45 | 1N4148WT ×12 → 1N4148WS **C2128** (basic) — §9.7 R5 | −0.07 | ✓ | guc-elektronigi (T_J 150 °C veri sayfasından), pcb-muhendisi (SOD-523 → SOD-323, 12 yer) |
| B6 | ESC R0/R02 | 90.9 k (ext) → basic (100 k + FB çifti) — §9.7 R6 | −0.02 | ✓ | guc-elektronigi: PVDD değeri |
| B7 | ESC C1…C60 | Bulk 15 → 12 × C89632 — §9.7 R4 | −0.36 | ✓ | guc-elektronigi: dalgalanma 1 → 1.25 A_rms/adet, set kondansatörüne bağımlılık. **Pakete alınmadı** (yedek) |
| B8 | Üretim | FMU + ESC tek panel / tek Standard sipariş | ≈ −0.10 (net) | — | pcb-muhendisi. Kurulum + şablon + ortak extended türler ≈ −0.38 $, ama FMU ESC katman yapısına (dış 2 oz) geçer: PCB ≈ +0.28 $ ve 0.5 mm aralıklı LQFP64/LGA'da 2 oz riski. **Önerilmez** |
| B9 | ESC | Dizgiyi tek yüze topla | −0.34 | — | pcb-muhendisi: 62 alt yüz parçası sığmaz (tahmin), ısıl yayılım. **Önerilmez** (§4) |

**A + B paketi (B1–B6): −3.57 $ → 31.35 $/stack, ≤ 32 $ karşılanıyor (pay 0.65 $).** B7 eklenirse 30.99 $.
Duyarlılık: B1 Tokmas DPS368 yedeğine düşerse 32.27 $ (aşar); B2 reddedilirse 31.87 $ (pay 0.13 $).

### 10.3 C — müşteri kararı

| # | Değişiklik | $/stack | Stok | Gereksinim / etki |
|---|---|---|---|---|
| **C1** | STM32F405RGT6 C15742 → **APM32F405RGT6** C5290473 (3.20 $ @100; 2.79 $ @160) | **−1.38** (JLC fiyatına göre); dış tedarik STM32 fiyatına göre −2.9…−5.1 | 1 728 ✓ | SYS-030 "resmî STM32F405". Pin uyumlu; BF APM32F405 hedefi var; AP desteği ve USB/DFU `gomulu-yazilim` doğrulamalı. **STM32 tedarik riskini de kapatır** |
| C2 | INA240A3 → INA186A3IDCKR C2058245 (B2 yerine) | −1.22 | 4 046 ✓ | SYS-021 gevşer; V_CM ≤ 40 V, SYS-014 ile sınırda |
| C3 | ICM-42688-P (Tokmas) → BMI270 C2836813 (1.23 $) | −0.89 | 9 232 ✓ | SYS-031: BF'de 3.2 kHz (8 kHz yok); pin dizilimi farklı |
| C4 | W25Q128JVSIQ → PUYA PY25Q128HA-SUH-IT C7419750 (0.81 $) | −0.71 | 3 357 ✓ | BF ≥ 4.5 destekli (JEDEC 0x852018); ArduPilot tablosunda yok (master dahil) → SYS-056 için AP yaması. ZB25VQ128 (BF + AP 4.7) JLC'de yok; GD25Q128 / BY25Q128 / FM25Q128 / XT25F128F yalnız BF 2026.6 |
| C5 | Baro çıkar (B1 sonrası) | −0.50 | — | SYS-032 (Ö) |
| C6 | Flash çıkar | −1.53 | — | SYS-033 (Ö), SYS-056 |
| — | Analog OSD (AT7456E) | 0 | — | SYS-034 zorunlu: dokunulmadı. Stoklu muadil yok (AT7456 C82523 ve MAX7456 stok 0; AT7456ELAH 1.85 $ daha pahalı) |

### 10.4 Değişmeyenler ve neden

| Parça | Bulgu |
|---|---|
| IMU Tokmas ICM-42688-P 2.12 $ | TDK orijinali C1850418 20.60 $ @30, stok 39: alternatif yok (SYS-031). HXY klonu C46550687 2.48 $ daha pahalı |
| AT7456E 1.73 $ | 500 kademesi 1.61 $ ama 500 adet almak 100 set için toplamda pahalı |
| W25Q128JVSIQ 1.53 $ (basic) | BF 4.5 + AP stabil destekli ucuz 16 MB SOIC-8 JLC'de yok. W25Q64 (8 MB) daha pahalı (1.81 $). → C4 |
| EFM8BB21F16I ×4, JSM6288Q1 ×4 | 500 kademesine çıkmak toplamda pahalı; 125 °C muadil yok (§9.10) |
| 8 MHz kristal 0.17 $ | Ucuz 3225'ler (0.13 $) ESR 250 Ω: HSE kazanç payı < 5 (gm_crit ≈ 0.57 mA/V). Basic 8 MHz yalnız 5032/HC-49 |
| SY8303 ×2, bobinler, 22 µF'ler, SH konnektörler, USB-C, sigorta, TVS, 74LVC1G04, USBLC6 | Basic muadil yok ya da fark < 0.02 $; 22 µF birleştirme parça farkıyla tür tasarrufunu yiyor |

### 10.5 Yeni tedarik riskleri (2026-11-11)

| Parça | Durum | Etki |
|---|---|---|
| **STM32F405RGT6** C15742 | JLC stoğu **24** (100 lazım, 2× 200). Dış referans @100: Future ≈ 6.13 $, DigiKey RGT6TR ≈ 6.93 $ (+7 $ makara), Mouser ≈ 8.34 $ (findchips önbelleği, tarihsiz) | Taban 4.58 $ yerine ~6.1–8.3 $: **+1.5…+3.8 $/stack**. JLC "global sourcing" fiyatı da bu bantta beklenir (doğrulanmadı). A+B ile 31.35 $ → **~32.9–35.1 $** |
| **JW5026** C185109 (ESC buck) | Stok **132** (11-10'da 4 308) | SYS-091 ✗ (200). `guc-elektronigi` 40 V muadil seçmeli, maliyet bilinmiyor |
| BLP016N04LC-Q | 3 903 / 4 800 | A1 peşin alımıyla ayrılmalı (§9.5) |

### 10.6 Öneri

1. **A + B (B1–B6): 31.35 $/stack**, hedefin 0.65 $ altında — **yalnız STM32F405RGT6 JLC fiyatıyla (4.58 $) bulunabilirse**. Kritik kalemler B1 (−2.30, `gomulu-yazilim` + `pcb-muhendisi`) ve B2 (−0.52, `guc-elektronigi`).
2. **Gerçekçi MCU fiyatıyla (dış tedarik ~6.9 $) A + B ≈ 33.7 $ → 32 $ aşılır.** En az zararlı C seçimi: **C1 APM32F405RGT6** — hiçbir özellik kaybolmaz, stok sorununu kapatır; A + B + C1 = **29.97 $** (STM32 dış fiyatına göre pay daha da büyük). C1 kabul edilmezse C4 (−0.71) + C3 (−0.89) bile ~32.1 $'da kalır, yani STM32'yle 32 $ ancak MCU JLC fiyatına yakın bir kaynaktan alınırsa tutar.
3. Müşteriye soru (yönetici üzerinden): SYS-030 "resmî STM32F405" → "STM32F405 ya da Betaflight'ın resmî desteklediği pin uyumlu APM32F405" olarak gevşetilsin mi?

### 10.7 Şematiğe işlenecek parça değişiklikleri (`sematik-muhendisi`, onaylar gelince)

| Kart | Ref | Önce → sonra (LCSC) | Koşul |
|---|---|---|---|
| FMU | U103 | C6186 → **C347222** (MPN AMS1117-3.3, UMW; ALT C6186) | A |
| FMU | C302 | C1524 → **C15195** | A |
| FMU | C206 | 1 µF 0402 C49210445 → **2.2 µF 16 V X7R 0603 C5360821** | A |
| FMU | C205 | 4.7 µF C107365 → **10 µF 16 V X7R 0805 C380347** | A |
| FMU | D202 | 1N4148WT C27748 → **1N4148WS C2128**, SOD-323 | A |
| ESC | M1aH…M4cL | kod aynı; sipariş notu: 2 500 adet peşin | A |
| FMU | U302 | DPS368 C3232508 → **SPA06-003 C30589048** (ayak izi aynı; ALT C55090144 Tokmas DPS368); `Temperature` −40…85 °C | B1 onayı |
| ESC | U2 | INA240A3DR → **INA281B2IDBVR C1517409**, SOT-23-5 sembol/ayak izi; ALT INA240A3DR | B2 onayı |
| FMU | D501 | PMEG3020EH → **B5819W SL C8598**, SOD-123 | B3 onayı |
| FMU | 5 V FB | 100 k / 13.7 k → **15 k C25756 / 2 k C4109** | B4 onayı |
| ESC | D13…D45 | C27748 → **C2128** SOD-323 | B5 onayı |
| ESC | R0/R02 | C26989 → guc-elektronigi'nin basic değerleri | B6 onayı |
| FMU | U201 | C15742 → **C5290473** APM32F405RGT6 (ALT C15742) | C1 müşteri kararı |

## 11. Hedef BOM (2026-11-13)

> **Kapsam:** iki kartın onaylı tüm kararlar uygulanmış hâli (4. adım; şematik 5. adımda): §10 A1, A3–A7 (A2 geçersiz), B1, B3–B6 ve `docs/rapor/guc-tasarruf.md` (B2 yerine RSA240CXK + ALT INA240A3DR; U1 SCT2400 + R0/R02/R01 100 k/20 k/2.2 k + C03b; FMU 3.3 V TLV62569 buck + L103 + bölücü; USB yük anahtarı Q102/Q103 + 2 × 100 k; D501 B5819W; 5 V FB 15 k/2 k; R111 22 Ω), KRR-012 (U201 AT32F435RGT7), KRR-013 (U301 LSM6DSV16X). B7 ve §10 C2–C6 dahil değil.
> **Kaynak:** JLCPCB parça arayüzü (`tools/jlc.py` scratchpad kopyası; proje önbelleği değişmedi), 2026-11-13. Yöntem §4/§10 ile aynı: 100 set birim = 100 × karttaki adet kademesi; ESC Standard çift yüz, FMU Standard tek yüz (A7); PCB §3 tahmini. A1: BLP016 2 500 adet peşin (2 500 × 0.1664 $ / 100 set = 4.16 $/kart).
> **Satır satır:** [`boards/esc55a/bom-hedef.csv`](../boards/esc55a/bom-hedef.csv), [`boards/fmu/bom-hedef.csv`](../boards/fmu/bom-hedef.csv). Muadiller, istisnalar, peşin alım: [`docs/muadil.md`](muadil.md).

### 11.1 Kart ve stack maliyeti (STACKF435, standart SKU)

| | ESC 100 set | FMU 100 set | Stack 100 set | ESC 5 set | FMU 5 set | Stack 5 set |
|---|---|---|---|---|---|---|
| Komponent | 12.85 | 12.43 | 25.28 | 17.73 | 18.16 | 35.89 |
| PCB (tahmin) | 0.80 | 0.25 | 1.05 | 6.00 | 0.40 | 6.40 |
| Dizgi | 2.05 | 1.42 | 3.48 | 19.05 | 16.37 | 35.42 |
| **Toplam $/kart** | **15.71** | **14.10** | **29.81** | **42.78** | **34.93** | **77.71** |
| Extended tür / lehim noktası | 14 / 724 | 29 / 399 | | | | |

- **PRJ-004 (≤ 32 $, 100 set, STACKF435): 29.81 $ → karşılanıyor, pay 2.19 $.** KRR-013'teki ≈ 31.3 $ tahmininden düşük: LSM6DSV16X 100'lük kademede 2.41 $ (3.35 $ tekil fiyattı), RSA240C (−1.19), A1 (−0.21).
- Önceki tabana göre (ESC 17.20 + FMU 17.72 = 34.92 $): ESC −1.49 (RSA240C −1.19, A1 −0.21, B5/B6 −0.09, SCT2400 −0.01, C03b +0.03); FMU −3.62 (baro B1 −2.30, MCU STM32 → AT32 −1.31, IMU Tokmas → LSM6DSV16X +0.29, dizgi A7 −0.25, 3.3 V buck −0.06, A3–A6/B3/B4 −0.10, yük anahtarı +0.06, fiyat oynaması ≈ +0.05).
- SYS-091 "extended tür ≤ 10/kart [öneri]" karşılanmıyor (ESC 14, FMU 29) — Standard dizgide maliyet 1.53 $/tür/sipariş, ≈ 0.015 $/set/tür; değişmedi.
- Stok (≥ 2 × ihtiyaç): yalnız BLP016 (3 903 < 4 800) → A1 peşin alım; diğer tüm ana parçalar ✓.
- Belirsizlik: PCB ve dizgi tahmin (§3, §4; tek kart ek ücreti 0.48 $/kart katılmadı → olursa +0.96 $/stack, yine ≤ 32 $); C03b isteğe bağlı (takılmazsa −0.03).

### 11.2 Varyant farkları (yalnız U201, PCB ve diğer BOM aynı)

| SKU | MCU (LCSC) | 100 set $/stack | 5 set $/stack | Not |
|---|---|---|---|---|
| **STACKF435** | AT32F435RGT7 C3029577 (3.27 $ @100; 200 adet 2.85 $) | **29.81** | 77.71 | ≤ 32 ✓ |
| STACKF405 (JLC fiyatı) | STM32F405RGT6 C15742 (4.58 $) | 31.12 (+1.31) | 79.48 | JLC stok 74 < 100 → fiilen dış tedarik |
| STACKF405 (dış tedarik 6.1–8.3 $) | aynı | 32.64–34.84 (+2.8…+5.0) | — | SKU fiyatına yansır (PRJ-009); hedef yalnız STACKF435 için |
| STACKF405A | APM32F405RGT6 C5290473 (3.20 $) | 29.74 (−0.07) | 77.61 | Yalnız tedarik krizinde |
| (yedek, ayrı DT) | AT32F435RMT7 C5178940 (4.15 $) | 30.69 (+0.88) | — | stok 128 |

### 11.3 ALT'larla dizilen parti (SYS-095)

ALT'lar yalnız dizildiği partide maliyete girer. Tüm kritik ALT'lar birlikte (en kötü): **ESC +1.92 $/kart** (INA240A3 +1.19, NTMFS +0.81 (A1 peşin fiyatına göre), HL6288Q −0.37, shunt +0.14, JST SH +0.13), **FMU +5.20 $/kart** (LSM6DSK320X +1.25, Tokmas DPS368 +0.92, RMT7 +0.88, W25Q128JVSIM +0.69, JST SH ×4 +1.32 …). Tek tek kalemler CSV `alt_100set_birim_$` sütununda.

### 11.4 Peşin alım (100 set) — ayrıntı `muadil.md` §4

AT32F435RGT7 × 200 (571 $), BLP016 × 2 500 (416 $), EFM8BB21F16I × 500 (410 $), AT7456E × 110 (190 $) = **1 587 $** zorunlu; isteğe bağlı SY8303AAIC × 220, LSM6DSV16X × 110, HoLRS3920 × 110 (ALT teyitsizse).

### 11.5 Hedefe dahil edilmeyen ek tasarruf (muadil taramasından)

HL6288Q'yu ana sürücü yapmak −0.37, USB-C Shou Han ana −0.08 (ayrıca 85 °C ✓), Y401 KYX −0.04, cjiang bobinler −0.03 → ≈ −0.5 $/stack (`muadil.md` §5; HL6288Q için `guc-elektronigi` onayı).
