# Ürün portföyü ve yol haritası — FPV aviyonik (2025–2026 pazarı)

Sahibi `pazar-analisti`. Tarih: 2026-11-10 (rev 3, takvim + Dual-ESC + fiber). Ham veri: [`portfoy-fiyatlar.csv`](portfoy-fiyatlar.csv) ve [`rakipler.csv`](rakipler.csv) (stack’ler, 2026-11-06). Fiyatlar USD, KDV/kargo hariç, satıcı sayfasında görülen değerler; başka para birimi veya KDV dahil olanlar öyle yazıldı. Akım ve güç değerleri **üretici iddiası**dır, bağımsız test yok. “Birim maliyet” ve “hedef fiyat” sütunları **öneri/tahmin**dir. Maliyetin tek dayanağı bizim 100 setlik BOM’umuz (`docs/bom-maliyet.md` S1b: fmu 14.4 $, esc55a 13.0 $); M2+ için gerçek BOM’u `bom-tedarik` çıkaracak. Satış/hacim verisi bulunamadı. “Talep” sütunu yorumdur.

## Kararlar (müşteri, 2026-11-10 — zorunlu girdi)

| # | Karar | Bu belgedeki etki |
|---|---|---|
| K1 | “F100” yazım hatasıydı; doğrusu **F405** (STM32F405 bütçe sınıfı) | M1 FMU = mevcut fmu (F405). Önceki §E S1 kapandı |
| K2 | Km taşı sırası **M1…M11** (aşağıda §B); müşteri sırası | §B baştan yazıldı; önceki M2–M6 sırası geçersiz |
| K3 | **M2:** amper yükseltme önce **5" ve 7"**, **3–6S**; 8S/10" henüz değil | 8S ve 10" M3’e kaydı. M2 önerisi: 65 A 3–6S (§B) |
| K4 | **M3:** 7"/10" **8S** ESC + 8S FMU + **GPS M10** | Önceki “M2 uzun menzil seti” M3 oldu |
| K5 | **M4 (yeni):** **F7 FMU** (Betaflight + INAV), M3’ten sonra, kesin | F722 önerildi (§B, §F) |
| K6 | **M5 (yeni):** F7’nin 2. versiyonu, **Betaflight + INAV + ArduPilot** aynı donanımda ya da yakın varyantta | F722’de ArduPilot **çalışmaz**; gerçekçi silikon H743 (§F). Açık soru S1 |
| K7 | **M6:** kanat FC (INAV); ESC mümkünse **aynı PCB**’de (kırılabilir iki parça seçeneği); Rus ve Çin ürünlerine bakılacak | §G |
| K8 | **M7** AM32 32 bit ESC · **M8** ELRS alıcı · **M9** analog VTX seviye 1 · **M10** analog VTX seviye 2 · **M11** fiber modemin stack’e uyarlanması | RF ürünler portföyde (önceki S5 = “evet”). §H, §I |
| K9 | **Ertelenenler:** AIO (25.5 / 20×20 / whoop) **en arkaya**; **dijital VTX durur**; **mekanik en sonda** | §C |
| K10 | **Dual-ESC FMU:** bir FMU **2 × 4’ü 1 arada ESC** bağlar (8 motor); yüksek itki için **ayrı SKU** | §B M4a; SpeedyBee F405 V4/V5’te 8 motor pedi var, fark = **iki fiziksel ESC konnektörü** |
| K11 | Fiber modemler **zaten var** (`/home/user/calismalar/fiber`); M11 = sıfırdan ürün değil, **stack formuna uyum** (30.5, SH, CRSF) | §I |
| K12 | Ürün ailesinin markası **Crow** (2026-11-11); tüm ürünler Crow adıyla pazarlanır | §D; [`crow-marka-pazarlama.md`](crow-marka-pazarlama.md) |
| K13 | Crow FPV: **EN-first**; logo **gaga**; slogan **Fly to Joy**; ad Crow FPV; belge = **pin + kılavuz poster** (şema kapalı). Domain ve tescil **ertelendi** (müşteri 2026-11-11) | [`crow-marka-pazarlama.md`](crow-marka-pazarlama.md); logo [`crow-fpv-logo.jpg`](crow-fpv-logo.jpg) |

Not: Kararların `KRR-` numarası ve `MUS-` karşılıkları `gereksinim-muhendisi`nin işidir (`docs/gereksinimler/kararlar.md`); bu tablo yalnız pazar girdisidir.

## Özet

| | Bulgu (2026-11-10) |
|---|---|
| Portföy deseni | Büyük markalar **stack/FC/ESC çekirdeği**nden başlayıp **ELRS → GPS → analog VTX → kanat FC** yönünde genişlemiş (SpeedyBee, GEPRC, Matek). Bizim sıramız (M1–M11) bu desene uyuyor; tek fark AIO’nun en sona atılması |
| 5" lider | SpeedyBee F405 V4 55A stack resmi fiyatı **65.99 $**. **60A V4 stack’i ve F7 V3 stack’i üretimden kalktı** (SpeedyBee sayfası “Discontinued”); yerlerine F405 V5 OX32 55A (115–120 $) geldi → 60–65 A 3–6S 8 bit sınıfında **boşluk** (M2 fırsatı) |
| F7 gerçeği | “F7” adıyla satılan kartların çoğu **STM32F722** (512 KB flash) → **ArduPilot çalışmaz** (ArduPilot en az 1 MB ister). ArduPilot’lu “F7”ler ya **F745** (1 MB, kısıtlı firmware) ya **F765** (2 MB; Matek F765-WSE üretimden kalktı, yerine H743 geldi). Üç yazılımı tam çalıştıran pazar standardı **H743** (§F) |
| F405 + ArduPilot | F405 (1 MB) ArduPilot’u **kısıtlı firmware** ile çalıştırıyor (SpeedyBeeF405v4 hedefi, Copter 4.4.4’ten beri). M1 FMU’su da ileride ArduPilot hedefi alabilir (fırsat; `gomulu-yazilim` değerlendirir) |
| Kanat + ESC tek kart | Pazarda az: **TBS Lucid Wing AIO** (H743 + 50 A AM32, 70–83 $). Rusya’da **НИМБУС F4** stack’i (ООО ИРТ, F4 + 65 A 32 bit, 7 700 ₽). **Kırılabilir FC+ESC kanat kartı bulunamadı** (fark yaratma fırsatı, tahmin) |
| Analog VTX | Seviye 1 (≤ 600–800 mW, 20×20): **20–37 $**. Seviye 2 (1.6–2.5 W, fanlı/CNC, 7–36 V): **47–66 $**. 25 mW üstü çoğu ülkede lisans gerektirir (risk) |
| Fiber hava ünitesi rakipleri | 35×30 mm 16 g (Transwan), 50×29×13 mm (SkycraftUA), 33×53×14 mm (RUID); **hiçbiri 30.5 stack deliğiyle satılmıyor** (bulunamadı). Bizim hava kartı 51.5×24.5 mm (fiber Rev B) |
| ABD/Çin dışı talep | FCC/tarife baskısı devam ediyor (SpeedyBee ABD siparişlerinde %54 peşin gümrük alıyor). JLC’de Çin’de üretim bu avantajı siler (önceki §E S4 açık) |
| TR pazarı | SpeedyBee V4 stack TR’de 3 540–5 340 TL; Komponentci 92.90 $ + KDV (ABD resmi fiyatın ~1.4 katı). Yerli rakip: Orbit Teknoloji (AT32F435 + 50 A), Yuke Aero (prototip) |

---

## A) Portföy kategorileri

Fit: ●●● mevcut tasarımın türevi, ●● yeni kart ama aynı teknoloji, ● yeni uzmanlık (RF, optik, mekanik). “KT” sütunu müşteri kararına göre güncellendi.

| Kategori | Satış fiyat bandı ($) | Birim maliyet (tahmin, 100 adet) | Talep | Rekabet | Fit | KT |
|---|---|---|---|---|---|---|
| 5" stack F405 + 55 A, 3–6S | 66 (SpeedyBee resmi) – 100 (GEPRC) | 27 (S1b) | Yüksek | Çok yüksek | ●●● | **M1** |
| FC tek satış (30.5 F405) | 32–49 | 14.4 | Yüksek | Çok yüksek | ●●● | **M1** |
| 4’ü 1 ESC tek satış 55 A | 26–47 | 13.0 | Yüksek | Yüksek | ●●● | **M1** |
| Stack aksesuarı (8 pin kablo, kondansatör, damper, XT60, LED, buzzer) | 1–14 | < 1–3 | Orta | Yüksek | ●●● | **M1** |
| 5"/7" ESC 60–65 A, 3–6S | 40–47 (8 bit); 120 (HobbyWing 65A AM32) | 14–15 | Yüksek | Orta (SpeedyBee 60A çekildi) | ●●● (esc65a) | **M2** |
| 7"/10" ESC 65–100 A 8S + FMU 8S | ESC 47–80; FMU 8S 48–50 | ESC 15–17; FMU 15 | Orta (büyüyor) | Orta | ●●● | **M3** |
| GPS M10 (+ pusula) | 7–25; markalı 30–33 | 6–9 | Yüksek | Yüksek | ●● | **M3** |
| F7 FMU (F722, BF + INAV) | 46–65 (FC); 85–123 (stack) | 16–18 | Orta (azalıyor) | Orta | ●● | **M4** |
| H7 FMU (H743, BF + INAV + ArduPilot) | 46–87 (FC); 110–135 (stack) | 18–22 | Orta (artıyor) | Orta | ●● | **M5** |
| Kanat / VTOL FC (INAV) + entegre ESC | 57–75 (F405 kanat FC); 70–83 (H7 + 50 A AIO) | 18–22 | Orta | Orta (Matek, CoreWing/SpeedyBee, TBS) | ●● | **M6** |
| 32 bit ESC (AM32) | 45 (JHEMCU 60A) – 85 (TBS 8S) – 150 (Ewing) | 14–18 | Orta (artıyor) | Orta | ●● (yeni MCU) | **M7** |
| ELRS alıcı (2.4 GHz; LR1121 çift bant) | 13–25; çift bant 26–28 | 3–6; 7–10 | Yüksek | Çok yüksek | ● (RF) | **M8** |
| Analog VTX seviye 1 (≤ 600–800 mW) | 20–37 | 5–8 | Yüksek (azalan) | Çok yüksek | ● (RF) | **M9** |
| Analog VTX seviye 2 (1.6–2.5 W) | 47–66 | 8–12 | Orta (uzun menzil, kanat) | Yüksek | ● (RF PA, ısı) | **M10** |
| Fiber modem (hava ünitesi, stack uyumlu) | Çift 130–415 (perakende, fiber deposu) | fiber `docs/bom-maliyet.md` | Büyüyor | Orta (Çin) | ●● (tasarım var) | **M11** |
| FMU’ya entegre ELRS | +10–15 fark (tahmin) | +3–5 | Orta | Orta | ● | M8 sonrası |
| PDB / BEC / akım sensörü | BEC 8–27; PDB 27–39 | 1–7 | Düşük–orta | Düşük | ●●● | M6 (kanat PDB) içinde; ayrı ürün sonra |
| 20×20 mini stack / 25.5 AIO / 1–2S whoop AIO | 50–90 | 10–22 | Orta–yüksek | Yüksek | ●●–● | **Ertelendi (en son, K9)** |
| Dijital VTX ve besleme aksesuarı | 70–230; besleme 8–27 | — | Yüksek | Kapalı sistem | ✗ | **Durdu (K9)** |
| FPV kamera, gözlük, radyo TX, şarj | — | — | — | — | ● | Öncelik dışı |
| Mekanik (çerçeve, pervane, BNF) | — | — | — | — | ● | **En son (K9)** |

---

## B) Km taşı sırası (müşteri sırası, 2026-11-10)

Hedef değer ve hedef fiyat **öneri**dir (gereksinim girdisi), `gereksinim-muhendisi` MUS/SYS’e çevirir. Muadil fiyatları: kaynak ve tarih §J ve CSV’de; hepsi erişim 2026-11-10.

| KT | Ürün | Hedef değer (öneri) | Muadil (en iyi örnekler, $) | Hedef fiyat (öneri) | Yeniden kullanım / not |
|---|---|---|---|---|---|
| **M1** | 5" stack: **F405** FMU + 55 A ESC (mevcut) + **ayrı FMU ve ESC SKU** + aksesuar | 55 A sürekli / 70 A 10 s, 3–6S, 30.5 mm; F405 + ICM-42688-P + baro + 16 MB + AT7456E, 5 V + 9 V BEC; SpeedyBee 8 pin dizilimi (KRR-004) | **SpeedyBee F405 V4 55A** stack 65.99 (resmi); FC 45.99 (RDQ) / 44.39 € (Rotorama); ESC 26.39–39.99. GEPRC Taker F405 60A V2 80.99–100.32 | Stack **59–65**; FC 35–39; ESC 28–33; aksesuar seti 5–8 | Sıfır ek tasarım (SKU ayrımı). Lider 65.99 $ → “≤ 70 $” (PRJ-003) liderin üstünde kalıyor; fark yaratma yoksa ≤ 65 $ |
| **M2** | 5"/7" yüksek akım ESC, **3–6S** (stack: M1 FMU + bu ESC) | **65 A sürekli / 80 A 10 s**, 3–6S, Bluejay, akım sensörü, 30.5 mm, 8 pin aynı dizilim [öneri] | **SpeedyBee BLS 60A** (60/80 A) 46.99 tek ESC, V4 60A stack 75.99 (**üretimden kalktı**); GEPRC Taker H60 (60/65 A) 46.79; JHEMCU Ruibet 60/65A BLS 39.99+; HobbyWing XRotor G2 65A AM32 (65/80 A) 119.99 | ESC **39–45**; stack **72–78** | esc65a PCB’si 40 V MOSFET BOM’uyla (M3’te aynı PCB 8S BOM’u, SOR-003 “tek kart iki varyant”; fizibilite `sistem-mimari` + `guc-elektronigi`). Etiket: piyasadaki “60 A” sınıfının bir adım üstü, aynı fiyat |
| **M3** | 7"/10" **8S**: ESC 65 A 8S + 80 A 8S, **8S FMU**, **GPS M10 + pusula**; “Long Range set” | ESC 65 A / 70 A 5 s, 3–8S (7"); 80 A, 4–8S (10"); FMU girişi ≥ 40 V geçici dayanım; GPS u-blox M10 + QMC5883/IST8310, 10 Hz | ESC: **GEPRC Taker H65 8S** 46.99 (GEPRC, FPVtopia), **H80 8S** 69.99, H100 8S 79.99 (tek satıcı). FMU 8S: GEP-F405-8S 47.99, Taker F722 8S 49.99 (tek satıcı). GPS: HGLRC M100-5883 16.40–22.49, Matek M10Q-5883 24.99+ | ESC 65 A 8S **45–49**; 80 A 8S **62–68**; FMU 8S **40–45**; GPS **15–18**; LR set (stack + GPS) **95–105** | MUS-004. FMU 8S: SYS-003/SYS-044 (TPS54202 28 V sınırı, RSK-008) ile aynı iş. GPS en basit yeni kart (RF yok, hazır modül) |
| **M4** | **F7 FMU** (Betaflight + INAV) | **STM32F722** (LQFP100), ICM-42688-P, baro, ≥ 16 MB blackbox, AT7456E, 5 V + 10 V BEC, 8 motor çıkışı, 6+ UART, 3–6S (8S seçeneği M3 girişinden) | **SpeedyBee F7 V3** FC 45.99 (indirimli, resmi; stack 89.99 “Discontinued”, RMRC 102.66); **Foxeer F722 V4** 64.90; GEPRC Taker F722 8S 49.99; Matek F722-SE | FC **42–48**; stack (M2 ESC ile) **85–90** | F722 = 512 KB flash → **ArduPilot yok**. Pazar riski: H743 FC’ler 46–60 $’a indi (GEPRC H743 Mini 45.99, TBS Lucid H7 59.95), F7 primi eriyor ve SpeedyBee F7 V3’ü kaldırdı (S1) |
| **M4a** | **Dual-ESC FMU** (ayrı SKU): **2 × 4in1 ESC** → **8 motor** | M4 (veya M1 F405) ile aynı çekirdek; **iki adet 8 pin SH ESC konnektörü** (M1–M4 + M5–M8); DMA/zamanlayıcı çakışmasız 8 DShot; kutu: 2× ESC kablosu. Yüksek itki / X-class / 7–10" ağır | SpeedyBee F405 V4/V5 ve F7: 8 motor **pedi** var ama tipik tek ESC kablosu; çift 4in1 kurulumu kullanıcı lehim/kablo. Holybro/iFlight 8 çıkışlı FC’ler | FC Dual **48–55** (F7) / **40–45** (F405 varyant); “2× ESC stack” seti ESC×2 + Dual FMU **110–130** (tahmin) | M4 ile aynı PCB ailesi, konnektör + ipek farkı [öneri]. M1 F405’e de aynı Dual SKU taşınabilir (müşteri isterse erken). SYS-037 (≥ 8 motor) ile hizalı |
| **M5** | F7’nin 2. versiyonu: **BF + INAV + ArduPilot** | **Öneri: STM32H743VIT6** (2 MB flash, 480 MHz, LQFP100); M4 ile aynı dış ölçü, konnektör ve dizilim (“yakın varyant”: MCU ve güç katı farklı); çift IMU [öneri], microSD veya ≥ 128 MB flash (ArduPilot kaydı), CAN (DroneCAN) [öneri] | **GEPRC Taker H743 BT** FC 87 (Next FPV) / 65.89 € (Rotorama, kalktı); stack 65A 120.59–135 (diyfpv); **TBS Lucid H7** 59.95; GEPRC Taker H743 Mini 45.99; MicoAir743v2 (AIO) | FC **55–65**; stack **105–115** | Ayrıntı §F. Pazarda “F7 + ArduPilot” diye satılabilecek gerçek seçenek yalnız F745 (kısıtlı) ve kalkan F765. **Pazar adı “H7” olmalı**; “F7” adıyla H743 satmak yanıltıcı olur |
| **M6** | **Kanat FC (INAV, + ArduPilot)**, ESC **aynı PCB** (kırılabilir iki parça seçeneği) | F405 (M1 çekirdeği) veya H743 (M5 çekirdeği); PDB + 90–100 A akım sensörü; servo BEC 5–8 A (5 / 6 / 7.2 V); 5 V + 9/12 V BEC; ≥ 10 PWM; ESC **1 kanal 45–50 A, 2–6S** [öneri], fare ısırığıyla ayrılabilir | **TBS Lucid Wing AIO** (H743 + 50 A AM32) 69.95 (TBS) / 76.99 (RDQ) / 82.99 (GetFPV); ESC’siz: **CoreWing F405 Wing V2** (eski SpeedyBee F405 WING APP) 64.99–74.99, **Matek F405-WING V2**, Matek F405-WTE 56.39 £ (KDV dahil). RU: **НИМБУС F4** stack 7 700 ₽ | F405 + 45 A: **55–65**; H743 + 50 A: **72–78** | §G. VTOL (quadplane) için 4 kaldırma motoru → M1/M2 4’ü 1 ESC’leri doğrudan aksesuar |
| **M7** | **AM32 32 bit ESC** | 60 A 3–6S (5"/7") ve 80 A 8S (10"); çift yönlü DShot + ESC telemetrisi, akım sensörü; MCU AT32F421 veya STM32G071 (AM32 hedefi hazır) [öneri] | **JHEMCU AM32A60** 60A 3–6S 44.99 (SpeedyFPV, liste 54.99); **GEPRC H60 Mini AM32** 45.99; **TBS Lucid 60A 8S AM32** 84.99; HobbyWing XRotor G2 65A AM32 119.99; Ewing 80A AM32 149.99 (NDAA) | 60 A **45–50**; 80 A 8S **70–80** | GEPRC H65 8S 32 bit ESC’si AM32’yi `AM32_AT32DEV_F421` hedefiyle destekliyor → AT32F421 pazarda kanıtlı. Yeni MCU ailesi (`gomulu-yazilim`) |
| **M8** | **ELRS alıcı** (2.4 GHz → LR1121 çift bant) | 2.4 GHz SX1281 + ESP8285, seramik / T anten; ardından LR1121 (900 MHz + 2.4 GHz) | Happymodel EP2 13.49–16.99; RadioMaster RP1/RP2 V2 18.99, RP3 V2 19.99; GEPRC C3 Gemini 25.99–27.99 | 2.4G **13–16**; çift bant **22–25** | Açık kaynak ELRS hedefleri hazır. RF ölçüm altyapısı + telsiz uygunluğu (AB RED, ABD FCC) kararı şart |
| **M9** | **Analog VTX seviye 1** | 5.8 GHz, 25–400/600 mW, 7–26 V (2–6S), 20×20 (+ 30.5 adaptör), IRC Tramp + SmartAudio, MMCX, pit mod, 5 V kamera çıkışı | Flywoo GOKU HM600 19.99 (RDQ); HGLRC Zeus Nano 350 mW 22.99–25.99; TBS Unify Pro32 Nano 22.99–31.10; JHEMCU 600 mW 26.99; SpeedyBee TX800 29.99–36.77; RUSH Tank Solo 1 W 33.99 | **22–27** | §H |
| **M10** | **Analog VTX seviye 2** | 25 mW – 1.6/2.5 W, **7–36 V (8S’e hazır)**, aktif soğutma veya CNC kasa, SmartAudio + MSP-VTX, MMCX + SMA pigtail, 30.5 delik | RUSH Max Solo 2.5 W 49.99 (RUSH) / 51.99 (FPVSTORERC, CaptainRC); GEPRC MATEN 1.6/2.5 W 47.99–54.99; TBS Unify Pro32 HV 1 W 46.75–52.41; Foxeer Reaper Extreme 2.5 W 62.90 | **45–52** | §H. M3/M6 kitlesiyle paket (uzun menzil, kanat) |
| **M11** | **Fiber modem → stack uyumu** (mevcut `../fiber`) | Mevcut **fiberair / fiberground** tasarımı uyarlanır (sıfırdan ürün değil). Hava: 30.5 delikli ≤ 38×38 mm stack katmanı; ≤ 16 g; 6–40 V; **CRSF çift yönlü**; JST-SH UART. Yer: JR yuvası korunabilir | Transwan 35×30 mm 16 g; SkycraftUA; RUID. Bizim Rev B: hava 51.5×24.5 mm, yer 50×40 mm | Fiyat fiber deposunun işi | Kaynak: `/home/user/calismalar/fiber`. Stack deposunda yalnız arayüz/montaj gereksinimleri; PCB işi fiber ekibinde |

**Sonra (ertelenen, K9):** 25.5 AIO / 20×20 mini stack / 1–2S whoop AIO (en arkaya), dijital VTX ve besleme aksesuarı (durdu), FPV kamera, PDB/BEC ayrı ürün, mekanik (en son).

### Önerilen takvim (tahmin — müşteri onayıyla sabitlenir)

Başlangıç: 2026-11 (M1 KiCad taşıması yapılmış). Süreler seri değil tamamen; M4a M4 ile paralel. Pazarlama satırı ürünle aynı çeyrekte.

| Çeyrek | Ürün km taşı | Pazarlama |
|---|---|---|
| **2026 Q4** | **M1** prototip 5 set (şu an) | İnceleme birimi, açık belge |
| **2027 Q1** | M1 100 set + ayrı FC/ESC SKU | Betaflight hedefi, TR bayi |
| **2027 Q2** | **M2** 65 A 3–6S ESC | Isı/akım ölçüm raporu |
| **2027 Q3** | **M3** 8S ESC + 8S FMU + GPS | Long Range set videosu |
| **2027 Q4** | **M4** F7 FMU + **M4a** Dual-ESC (8 motor) | F7 lansmanı; “2× ESC / 8 motor” SKU |
| **2028 Q1** | **M5** H743 (BF+INAV+ArduPilot) | Üç yazılım hedefi duyurusu |
| **2028 Q2** | **M6** Kanat FC+ESC | MEB / üniversite takımları |
| **2028 Q3** | **M7** AM32 ESC | 32 bit ESC kuşağı |
| **2028 Q4** | **M8** ELRS alıcı | RF uygunluk kararı sonrası |
| **2029 Q1** | **M9** Analog VTX L1 | Katalog genişliği |
| **2029 Q2** | **M10** Analog VTX L2 | Uzun menzil / kanat paketi |
| **2029 Q3** | **M11** Fiber → stack formu | fiberair 30.5 katman; CRSF |

Poster: [`stack-yol-haritasi-poster.jpg`](stack-yol-haritasi-poster.jpg) (üretilmiş görsel) + Cursor canvas `fpv-yol-haritasi-poster`.

---

## C) Bilinçli erteleme listesi

| Ürün | Neden sonra |
|---|---|
| AIO (25.5 AIO 40 A, 20×20 mini stack, 1–2S whoop AIO) | **Müşteri kararı (K9): en arkaya.** Pazar notu: SpeedyBee F405 Mini 20×20 üretimden kalktı (boşluk sürüyor); whoop AIO’lar BNF dronların içinde satılıyor |
| Dijital VTX (DJI O4, Walksnail, HDZero) ve besleme aksesuarı | **Müşteri kararı (K9): durdu.** Kapalı sistem; FMU’daki 9–12 V BEC yeterli |
| Mekanik (çerçeve, pervane, BNF) | **Müşteri kararı (K9): en son** |
| FPV kamera, gözlük, radyo TX, şarj | Optik/mekanik/yazılım uzmanlığı; aviyonik çekirdeğin dışında |
| Ayrı PDB / BEC / LED ürünleri | M1 aksesuar setinde (LED, buzzer) ve M6 kanat PDB’sinde özellik olarak; ayrı SKU sonra |
| Ayrı ESC telemetri/akım sensörü kartı | Pazarda ayrı ürün olarak yok; ESC/PDB özelliği |

**Çelişki / güncelleme notları:**
1. SpeedyBee F405 V4 55A stack resmi **65.99 $**; 60A V4 stack ve F7 V3 stack resmi sayfada “Discontinued” (2026-11-10). 60 A tek ESC hâlâ 46.99 $.
2. GEPRC H65 8S yazılımı: FPVtopia (üretici verisi, 2026-10-22) **BLHeli_S, hedef B_X_30** diyor; diyfpv “BLHeli_32” diyor. Ürün adı “BLS” → BLHeli_S ağırlıklı; 32 bit sürümü ayrı ürün (Taker H65_8S_32Bit, Taker H743 stack’inde). Çelişki büyük ölçüde çözüldü.
3. UAVMODEL blog özellik bilgisinde hatalı (SpeedyBee V4 için BMI270/16 MB); yalnız eğilim için kullanıldı.
4. Önceki belgede SpeedyBee F405 WING APP olarak geçen ürün artık **CoreWing F405 Wing V2** adıyla satılıyor (RDQ).

---

## D) Pazarlama / tanıtım km taşları

Marka **Crow** (K12). Ürün adları (Crow F405, Crow ESC 55, Crow Stack 55, Crow LR, Crow Dual, Crow Wing, Crow Link …), SKU, kanal tablosu, bütçe bantları ve marka çakışması riski: [`crow-marka-pazarlama.md`](crow-marka-pazarlama.md). Aşağıdaki tablo özet olarak kalır.

| KT | Pazarlama adımı | Not |
|---|---|---|
| M1 prototip | TR FPV topluluğunda tanınmış pilotlara 2–3 **inceleme birimi**; açık belge (pin haritası, KiCad çıktıları, Betaflight hedefi) | Açık belge rakiplerde yok |
| M1 100 set | **Betaflight resmî hedef** kaydı; TR bayileri (Robotzade, F1depo, Migitec, Komponentci, İsotronic) + Trendyol/Hepsiburada/PttAVM | Betaflight üretici kaydı şartları doğrulanacak |
| M2 | “65 A 3–6S, 60 A fiyatına” + bağımsız ısı/akım ölçüm raporu | SpeedyBee 60A çekildi; ölçüm yayımı fark |
| M3 | “7" Long Range set” (stack + GPS), GPS Rescue gösterimi, 8S dayanım testi | |
| M4–M5 | “Aynı kart, üç yazılım” (M5): Betaflight / INAV / ArduPilot hedeflerinin üçü de resmî | ArduPilot hedefi için `hwdef` PR’ı ve board ID (ArduPilot porting belgesi) |
| M6 | Üniversite/lise takımları, MEB Robot ve Teknofest İHA; “kırılabilir FC + ESC” tek kart | MEB RC sabit kanat şartnamesinde yerlilik 0–5 puan; Teknofest doğrulanmadı |
| M7+ | Yurt dışı bayi (AB), ABD’de “Çin dışı” yalnız üretim Çin dışına alınırsa | ABD tarife yorumu kesin değil |

---

## E) Müşteriye açık sorular (en fazla 2)

| # | Soru | Seçenekler | Neden |
|---|---|---|---|
| S1 | M5’te MCU **H743** kabul mü? | 1) **[öneri]** H743, pazar adı “H7”; M4 (F722) ile aynı dış ölçü/konnektör, MCU ve güç katı farklı 2) F745, adı “F7” kalır; ArduPilot yalnız kısıtlı firmware (F405 ile aynı seviye) 3) M4’ü doğrudan H743 yapıp M4 + M5’i tek karta birleştirmek (bir kart az; F722 primi zaten eriyor) | F722’de ArduPilot imkânsız (512 KB). F765 Betaflight’ta ürün hedefi yok, Matek’te üretimden kalktı |
| S2 | M6 kanat kartında ESC kaç kanal? | 1) **[öneri]** 1 kanal 45–50 A, 2–6S (tek motorlu kanat/uçak; TBS Lucid Wing AIO gibi) 2) 2 kanal (çift motorlu kanat, diferansiyel itki) 3) ESC’siz kanat FC + VTOL için ayrı 4’ü 1 ESC (M1/M2) | PCB boyutu, ısı ve fiyat bandını belirler |

Kapanan eski sorular: S1 (“F100” = F405, K1), S2 (M2 sırası, K2–K3), S5 (RF ürünler portföyde, K8). Açık kalanlar: S3 satış kanalı önceliği, S4 “Çin dışı üretim” (gerekirse M1 100 set öncesi sorulur).

---

## F) M4/M5 — “F7” pazar adı ile gerçek silikon, ArduPilot uygunluğu

ArduPilot en az **1 MB** dahili flash ister; 1 MB kartlarda özellikleri kısılmış (“limited”) firmware üretilir, 2 MB’de tam firmware. Kaynak: ArduPilot porting belgesi, “Firmware Limitations” sayfası, ArduPilot forumu (F722 için “zero possibility”).

| MCU | Flash / RAM | Betaflight | INAV | ArduPilot | Pazardaki örnek | Fiyat ($) |
|---|---|---|---|---|---|---|
| STM32F405 | 1 MB / 192 KB | ✓ | ✓ | **Kısıtlı** (SpeedyBeeF405v4, MatekF405, SpeedyBeeF405WING) | SpeedyBee F405 V4, CoreWing F405 Wing V2 | FC 44–49 |
| **STM32F722** | **512 KB** / 256 KB | ✓ | ✓ | **✗ (yetersiz flash)** | SpeedyBee F7 V3, Diatone Mamba F722, Matek F722-SE, Foxeer F722 V4, GEPRC Taker F722 | FC 46–65 |
| STM32F745 | 1 MB / 320 KB | ✓ (KAKUTEF7, FLYWOOF745, FOXEERF745 AIO, GEPRCF745_BT_HD) | ✓ | **Kısıtlı** (KakuteF7, FlywooF745, BlitzF745) | Holybro Kakute F7, Flywoo GOKU F745 | — (bu taramada fiyat alınmadı) |
| STM32F765 | 2 MB / 512 KB | Ürün hedefi yok (Betaflight hedef listesinde F765 kartı bulunamadı) | ✓ (MATEKF765SE) | ✓ tam (MatekF765-SE / -Wing) | Matek F765-WSE — **EOL**, yerine H743-WLITE | 78.99–79.99 (stok yok) |
| **STM32H743** | **2 MB** / 1 MB | ✓ (GEPRC_TAKER_H743, TBS_LUCID_H7, MATEKH743, KAKUTEH7 …) | ✓ | ✓ tam | GEPRC Taker H743, TBS Lucid H7, Matek H743, Kakute H7, iFlight BLITZ Wing H743, MicoAir743 | FC 46–87 |

**Sonuç:** “Betaflight + INAV + ArduPilot aynı donanımda” isteğini tam karşılayan, bugün üretimde olan ve pazarda yaygın tek seçenek **H743**. F745 “F7” adını korur ama ArduPilot’ta F405’ten fazlasını vermez (kısıtlı firmware). F765 tam ArduPilot verir ama Betaflight ürün hedefi yok ve Matek bile H743’e geçti. Birçok “F7 ArduPilot” algısı aslında **H7** kartlardan geliyor (TBS Lucid H7, Taker H743). Parça fiyat farkı (F722 ↔ H743) `bom-tedarik`ten alınmalı; pin uyumu (LQFP100 F722VET6 ↔ H743VIT6: VCAP, güç alanları, bazı alternatif fonksiyonlar farklı) `sistem-mimari` tarafından doğrulanmalı. Burada “aynı PCB” değil, **“aynı dış ölçü ve konnektör, farklı MCU yerleşimi”** varsayıldı (tahmin).

---

## G) M6 — Kanat FC + ESC aynı PCB (Rus ve Çin ürünleri)

| Ürün | Menşe | MCU | ESC | Hücre | Yazılım | Biçim | Fiyat | Kaynak (2026-11-10) |
|---|---|---|---|---|---|---|---|---|
| **TBS Lucid Wing AIO** | TBS (CN üretim) | H743, çift ICM42688, DPS310 | **1 × 50 A AM32**, MR30 motor | 2–6S | INAV, ArduPilot | Plastik kasalı tek kart; servo BEC 5 A (5/6/7.2/8.4 V) | 69.95 $ (TBS), 76.99 $ (RDQ), 82.99 $ (GetFPV), 69.95 £ KDV dahil | team-blacksheep.com, RDQ, GetFPV, flyingtech |
| MicoAir743v2-AIO-35A | MicoAir (CN) | H743, BMI088 + BMI270 | 4 × 35 A Bluejay | 2–6S | ArduPilot, INAV, Betaflight, PX4 | Quad AIO; VTOL için örnek | fiyat alınmadı | micoair.com |
| CoreWing F405 Wing V2 (eski SpeedyBee F405 WING APP) | CN | F405 | **yok** (PDB + servo BEC 8 A) | 3–6S | INAV, ArduPilot | 3 katlı stack (FC + PDB + kablosuz kart) | 64.99–74.99 $ (önceki adıyla); RU 8 217 ₽ (rccopter.ru) | RDQ, Great Hobbies, rccopter.ru |
| Matek F405-WING V2 / F405-WTE / H743-WING V3 | Matek (CN) | F405 / H743 | **yok** (PDB 100–220 A sensör) | 3–6S | INAV, ArduPilot | Kanat FC + PDB | WTE 56.39 £, H743-WING V3 109.99 £ (KDV dahil); RU 12 200 ₽ (H743-WING) | Unmanned Tech, 3DXR, glory-avia.ru |
| iFlight BLITZ Wing H743 Combo | iFlight (CN) | H743 | ayrı BLITZ E80 tek ESC | 2–8S | BF, INAV, ArduPilot | FC + ayrı ESC (kombo) | fiyat alınmadı | shop.iflight.com |
| **НИМБУС F4** stack | ООО «ИРТ» (RU) | STM32 F4 | **4’ü 1, 65 A, 32 bit, kendi ESC yazılımı**, akım/gerilim sensörü | 4–6S | Betaflight (varsayılan), INAV, ArduPilot, EMUFlight, Ampl-fpv | 30.5 stack (36×36 FC + 58×45 ESC); “uçak tipi İHA” da hedef | **7 700 ₽** (налетай.рф) | налетай.рф, irtsolution.com |
| Баклан-1 | КБ «Око» (RU) | belirtilmemiş | **yok**; > 100 A motorlar için güç katı | — | — | Büyük kanat İHA FC’si, standart konnektörler | prototip (2024–25), satışta değil | aviastat.ru, techuav |
| «Стриж» | НИТУ МИСИС (RU) | yerli eleman tabanı | yok; dahili güç modülü + ampermetre | — | — | Kanat + çok rotorlu | prototip, “≥ 1000 adet/yıl talep” iddiası | misis.ru (2025-01-30) |

**Çıkarımlar:**
- Kanat FC’ye ESC’yi aynı kartta koyan ürün az: tek yaygın örnek TBS Lucid Wing AIO (H7, 70–83 $). **Kırılabilir (fare ısırıklı) FC + ESC kanat kartı bulunamadı** → fark yaratma fırsatı (tahmin; arama Türkçe/İngilizce/Rusça, sonuçlar sınırlı).
- Kanatta motor sayısı 1–2 → 4’ü 1 değil **1 kanallı ESC** yeterli; tek EFM8BB21 + Bluejay ile esc55a güç katı bilgisi taşınır (öneri, `guc-elektronigi` değerlendirir). VTOL’de 4 kaldırma motoru için M1/M2 4’ü 1 ESC kullanılır.
- Rusya’da “yerli üretim” en güçlü satış argümanı (НИМБУС, Стриж, Баклан); TR’de aynı argüman MEB/Teknofest yerlilik puanında (§D).
- Fiyat önerisi: F405 + 45 A kırılabilir kart **55–65 $** (CoreWing/Matek ESC’siz kanat FC’lerle aynı bant, ESC bedava gibi); H743 sürümü **72–78 $** (TBS’nin altında).

---

## H) Analog VTX — iki kademe

| | Seviye 1 (M9) | Seviye 2 (M10) |
|---|---|---|
| Hedef kitle | 3–5" freestyle, yarış, giriş | 7"/10" uzun menzil, kanat (M3, M6) |
| Güç | 25 / 100 / 200 / 400 (600) mW + pit | 25 mW … 1.6 / 2.5 W + pit |
| Giriş | 7–26 V (2–6S) | 7–36 V (8S’e hazır) |
| Biçim | 20×20 (+ 30.5 adaptör), ≤ 3–5 g | 30.5 delik veya 40×24 mm, fan veya CNC kasa, ~15 g |
| Kontrol | IRC Tramp + SmartAudio | SmartAudio + MSP-VTX |
| Anten | MMCX / U.FL | MMCX + SMA pigtail |
| Muadil ($, 2026-11-10) | Flywoo GOKU HM600 19.99 (RDQ); HGLRC Zeus Nano 22.99 (diyfpv) / 25.99 (Wrekd); TBS Unify Pro32 Nano 22.99 (Wrekd) / 31.10 (diyfpv); JHEMCU 600 mW 26.99; SpeedyBee TX800 29.99 (Wrekd) / 36.77 (diyfpv); RUSH Tank Solo 33.99 | RUSH Max Solo 2.5 W 49.99 (RUSH) / 51.99 (FPVSTORERC, CaptainRC); GEPRC MATEN 47.99–54.99; TBS Unify Pro32 HV 46.75–52.41; Foxeer Reaper Extreme 2.5 W 62.90 |
| Hedef fiyat (öneri) | **22–27 $** | **45–52 $** |
| Fark yaratma | Ölçülmüş çıkış gücü tablosu (pazarda “400 mW deyip 230 mW” şikâyeti yaygın, anekdot); ısıl düşme ölçümü | Kanal başına kalibre güç; 8S giriş; düşük gürültülü besleme; ölçüm raporu |

**Risk:** 5.8 GHz’te lisanssız sınır AB’de 25 mW EIRP (SRD); 1 W üstü amatör lisans gerektirir. TR (BTK) sınırı ve CE/RED uygunluğu **doğrulanacak**. Ölçüm için spektrum analizörü + güç ölçer yatırımı gerekir (M8 ile ortak).

---

## I) M11 — Fiber modemin stack uyumu (kısa)

| Konu | Bizim fiberair (Rev B, fiber deposu) | Rakip hava üniteleri | Öneri |
|---|---|---|---|
| Boyut | 51.5 × 24.5 mm (1262 mm²), 1x9 modül 1.2 mm yükseltilmiş, SC ağzı karttan taşıyor | 35×30 mm 16 g (Transwan); 50×29×13 mm (SkycraftUA); 33×53×14 mm 16 g (RUID) | **30.5 delikli ≤ 38×38 mm** “stack katmanı” seçeneği (fark; rakiplerde bulunamadı). 36×36 = 1296 mm² ≈ bugünkü alan → **CPLD TQFP144 → TQFP100** (fiber `docs/yerlesim.md` önerisi, ~42×24 mm) olmadan sığmaz (tahmin) |
| Montaj | Montaj deliği yok | “4 köşe deliği” (FPV.BASE), ölçü verilmemiş | 30.5 × 30.5 mm M3, stack’in en üstünde (fiber çıkışı arkaya) |
| FMU arayüzü | JST-GH 8 pin: UART (SBUS), besleme, CVBS | SH1.0 6P (SkycraftUA, RUID), GH1.25 (Transwan) | FMU tarafındaki UART konnektörüyle eşleşen **JST-SH 1.0** kablo veya pin; dizilim `docs/pin-haritasi.md`’ye (`sistem-mimari`) |
| Besleme | ~6–40 V (SY8291 buck) | 5–32 V, 5.5–26 V, 9–30 V | **Koru:** 6–40 V → 8S’e hazır tek ürün (M3 ile uyumlu, fark) |
| Tüketim | 3V3 yükü ~260–360 mA (fiber `devre-analizi.md`), ≈ 1–1.5 W (tahmin) | 0.4 W (SkycraftUA iddiası) | Ölçülmeli; FMU 5 V BEC’ten beslenecekse bütçeye girer |
| Kumanda | SBUS tek yön (yerden havaya) | Çoğunda **CRSF çift yönlü** + telemetri | CRSF telemetrisi stack satışı için **zorunlu** (Betaflight/INAV OSD) |

Not: Değişiklikler fiber deposunun sahiplerinin işidir; bu tablo yalnız pazar girdisidir. Hava ünitesi fiyatı ve maliyeti fiber `docs/pazar-analizi.md` ve `docs/bom-maliyet.md`’de.

---

## Rakip marka portföy haritası

●●● güçlü / amiral ürün, ●● var, ● sınırlı, — yok. Kaynak: üretici mağaza sayfaları ve satıcı listeleri (2026-11-10); BNF/çerçeve ve bazı hücreler genel bilgi, satır satır doğrulanmadı.

| Marka | Stack / FC | AIO | ESC (tek) | Kanat FC | GPS | Analog VTX | ELRS RX | Genişleme sırası (yorum) |
|---|---|---|---|---|---|---|---|---|
| SpeedyBee | ●●● (F405 V4/V5; F7 V3 kalktı) | ●● | ●● | ●● (CoreWing’e devredildi) | ● | ● (TX800) | ● | Bluetooth’lu stack → AIO → kanat → aksesuar/RX/GPS → BNF |
| GEPRC | ●●● (Taker F405/F722/H743) | ● | ●●● (H60…H100 8S, AM32) | — | ● | ●●● (MATEN) | ●●● (C3 Gemini) | BNF → stack/ESC → VTX/RX |
| Matek | ●●● (en geniş FC yelpazesi) | ● | ● | ●●● (F405/H743-WING, WTE) | ●●● | ● | ●● | FC → kanat FC → PDB/BEC/GPS (**bize en yakın model**) |
| TBS | ●● (Lucid H7) | — | ●● (Lucid 60A 8S AM32) | ●● (Lucid Wing AIO) | ● | ●●● | ● (Crossfire) | Link → VTX → radyo → FC/ESC → kanat AIO |
| Holybro | ●● (Kakute F7/H7) | — | ●● (Tekko32) | ●● (Kakute H7 Wing) | ●●● | — | — | Pixhawk → FPV FC → GPS |
| iFlight | ●● (BLITZ F7/H7) | ● | ●● (E55/E80) | ●● (BLITZ Wing H743) | ● | ●● | ● | Motor/BNF → stack → VTX |
| HobbyWing | ● (XRotor F7) | — | ●● (G2 65A AM32) | — | — | — | — | ESC → FC |
| RUSHFPV | ● (Blade F4/F7) | ● | — | — | — | ●●● (Tank, Max Solo) | — | VTX → FC |
| Orbit Teknoloji (TR) | ●● (F435 + 50 A) | — | ● | — | — | — | — | Yerli stack → savunma |
| ООО ИРТ (RU) | ●● (НИМБУС F4 + 65 A) | — | ● (kendi 32 bit) | ● (uçak tipi destek) | — | — | — | Yerli stack → İHA |

---

## Belirsizlikler

- Satış adedi/pazar payı verisi yok; “talep” yorumdur.
- Maliyet ve hedef fiyatlar **tahmin/öneri**; M2+ BOM’ları `bom-tedarik` çıkaracak.
- Tek satıcıdan gelen fiyatlar (GEPRC katalog, Flywoo HM600 RDQ, Foxeer F722 V4, НИМБУС) CSV’de işaretli.
- Ruble fiyatları USD’ye çevrilmedi (kur varsayımı yapılmadı).
- F722 ↔ H743 ve F722 ↔ F745 pin uyumu doğrulanmadı (`sistem-mimari`).
- Rus pazarı taraması arama motoru sonuçlarıyla sınırlı; savunma odaklı ürünlerin çoğu açık fiyat vermiyor.
- VTX güç sınırları (TR BTK, AB RED) doğrulanmadı.
- Betaflight’ın F765 platform desteği kod düzeyinde araştırılmadı; yalnız ürün hedef listesine bakıldı.

## J) Kaynaklar (erişim 2026-11-10)

- **SpeedyBee:** [F405 V4 60A stack (Discontinued, 75.99; BLS 60A ESC 46.99)](https://www.speedybee.com/speedybee-f405-v4-bls-60a-30x30-fc-esc-stack/), [ürün listesi s.6](https://www.speedybee.com/products/?page=6), [F7 V3 stack (Discontinued, 89.99)](https://www.speedybee.com/speedybee-f7-v3-bl32-50a-30x30-stack/), [RMRC F7 V3 102.66](https://www.readymaderc.com/products/details/85784-speedybee-f7-v3-stack-f722-fc-50a-128k-esc-30-30), [FPVSTORERC F405 V4 60A](https://fpvstorerc.com/products/speedybee-f405-v4-bls-60a-30x30-fc-esc-stack), [RaceDayQuads F405 V4 FC](https://www.racedayquads.com/products/speedybee-f405-v4-3-6s-30x30-flight-controller), [RotorBuilds Rotorama](https://rotorbuilds.com/part/71881)
- **ArduPilot / MCU:** [Porting (≥ 1 MB flash)](https://en.ardupilot.org/dev/docs/porting.html), [Firmware Limitations](https://ardupilot.org/plane/docs/common-limited-firmware.html), [Forum: SpeedyBee F7 V3 (F722) desteklenmiyor](https://discuss.ardupilot.org/t/speedybee-f7-v3-compatible-firwmare/141131), [Forum: Mamba F722](https://discuss.ardupilot.org/t/why-is-diatone-mamba-mk4-app-f722-2024-unsupported/115783), [GitHub #15531 Matek F722](https://github.com/ArduPilot/ardupilot/issues/15531), [FlywooF745 hwdef (1024 KB)](https://github.com/ArduPilot/ardupilot/blob/3e40de50/libraries/AP_HAL_ChibiOS/hwdef/FlywooF745/hwdef.dat), [KakuteF7 features.txt](https://firmware.ardupilot.org/Plane/latest/KakuteF7/features.txt), [Kart bazında kısıtlar](https://ardupilot.ardupilot.org/sub/docs/binary-features.html), [SpeedyBee F4 V3/V4 ArduPilot](https://ardupilot.ardupilot.org/copter/docs/common-speedybeef4-v3.html), [Copter 4.4 sürüm notları](https://github.com/ArduPilot/ardupilot/blob/Copter-4.4/ArduCopter/ReleaseNotes.txt), [Betaflight hedef listesi](https://support.betaflight.com/targets), [Matek F765-WSE (EOL)](https://www.mateksys.com/?portfolio=f765-wse), [hobbywireless F765-WSE](https://www.hobbywireless.com/flight-controller-f765wse-matek-p-4955.html), [defianceRC F765-WSE](https://www.defiancerc.com/products/matek-f765-wse-flight-controller)
- **H743:** [Next FPV Taker H743 BT FC](https://www.nextfpv.com/hr/products/geprc-taker-h743-30x30-bt-flight-controller), [GEPRC Taker H743 50A stack](https://geprc.com/product/taker-h743-bt-32bit-50a/), [diyfpv Taker H743 65A stack](https://www.diyfpv.com/product/geprc-taker-h743-bt-32bit-65a-stack), [Rotorama Taker H743](https://www.rotorama.com/product/geprc-taker-h743-bt), [TBS Lucid H7](https://www.team-blacksheep.com/products/prod:lucid_h7)
- **Kanat / AIO:** [TBS Lucid Wing AIO](https://www.team-blacksheep.com/products/prod:tbs_wing_aio6s), [GetFPV Lucid Wing AIO](https://www.getfpv.com/tbs-lucid-wing-aio-h7-fc-50a-2-6s-am32-esc.html), [RDQ Lucid Wing AIO](https://www.racedayquads.com/products/tbs-lucid-wing-aio-h7-fc-50a-2-6s-am32-esc), [flyingtech Lucid Wing AIO](https://www.flyingtech.co.uk/product/tbs-lucid-wing-aio-flight-controller-esc-2-6s-50a/), [MicoAir743v2-AIO-35A](https://micoair.com/flightcontroller_micoair743v2_aio_35a/), [iFlight BLITZ Wing H743](https://shop.iflight.com/BLITZ-Wing-H743-Combo-Set-Pro2244), [RDQ CoreWing F405 Wing V2](https://www.racedayquads.com/products/corewing-f405-wing-v2-flight-controller-stack), [Oscar Liang F405 WING APP](https://oscarliang.com/speedybee-f405-wing-app/), [flyingtech Matek F405-WING V2](https://www.flyingtech.co.uk/product/matek-f405-wing-v2-fixed-wing-inav-flight-controller-pdb/), [SoarSky F405 WING APP](https://soarskyrc.com/products/speedybee-f405-wing-app-fixed-wing-flight-controller), [Unmanned Tech Matek F405-WTE](https://www.unmannedtechshop.co.uk/product-category/flight-controllers-autopilots/page/21/?add-to-cart=607189), [3DXR H743-WING V3](https://www.3dxr.co.uk/products/matek-systems-flight-controller-h743-wing-v3)
- **Rusya:** [НИМБУС F4 stack — налетай.рф](https://xn--80aaorhk2b.xn--p1ai/product/stek-nimbus-kontroller-esc), [НИМБУС F4 — irtsolution.com](https://irtsolution.com/nimbus-f4), [Баклан-1 — AviaStat](https://www.aviastat.ru/news/274495-v-rossii-sozdali-poletnyy-kontroller-adaptirovannyy-pod-bpla-samoletnogo-tipa), [Баклан-1 — techuav](https://techuav.github.io/%D0%A2%D0%AD%D0%A7_%D0%91%D0%BF%D0%9B%D0%90_FPV/%D0%A7%D0%B0%D1%82/%D0%91%D0%B0%D0%BA%D0%BB%D0%B0%D0%BD-1.html), [Стриж — МИСИС](https://misis.ru/news/9574/), [rccopter.ru F405 WING APP](https://rccopter.ru/product/polyotnyy-kontroller-speedybee-f405-wing-app), [glory-avia.ru H743-WING](https://glory-avia.ru/h743-wing_v2_v3), [getfpv.ru GEPRC F722 AIO](https://getfpv.ru/shop/komponenty-dlya-sborki-drona/poletnye-kontrollery/poletnyy-kontroller-geprc-gep-45a-f722-aio/)
- **ESC 60–65 A / AM32 / 8S:** [FPVtopia GEPRC H65 8S](https://fpvtopia.com/gear/geprc-taker-h65-8s-bls-65a-4-in-1-esc/), [SpeedyFPV JHEMCU (Ruibet 60/65A, AM32A60)](https://speedyfpv.com/collections/escs), [Pyrodrone HobbyWing XRotor G2 65A AM32](https://pyrodrone.com/products/hobbywing-xrotor-65a-3-6s-blheli32-4in1-esc-for-fpv-racing-30-5x30-5mm), [Wrekd ESC listesi](https://wrekd.com/collections/escs?page=4), [rcsearch 65A 4in1](https://rcsearch.info/-c33100), [MyFPVStore H60/H65](https://www.myfpvstore.com/fpv-electronics/esc/geprc-taker-h60-65-4in1-choose-your-esc/), [GetFPV TBS](https://www.getfpv.com/drone-brands/tbs.html)
- **Analog VTX:** [RDQ Flywoo HM600](https://www.racedayquads.com/products/flywoo-goku-hm600-25-600mw-5-8ghz-20x20-25x25-30x30-vtx-u-fl), [diyfpv JHEMCU 600 mW](https://www.diyfpv.com/product/jhemcu-25-600mw-5-8ghz-mmcx-vtx-w-irc-tramp-20x20mm), [Wrekd analog VTX](https://wrekd.com/collections/analog-video-transmitters), [Rotor Riot Reaper Nano](https://rotorriot.com/products/reaper-nano-25-350mw-vtx-for-analog-video-system), [RUSH Max Solo](https://rushfpv.net/products/rushfpv-max-solo-vtx), [CaptainRC Max Solo](https://captainrc.com/products/rushfpv-max-solo-5-8g-vtx-2-5w), [diyfpv Max Solo](https://www.diyfpv.com/product/rushfpv-rush-max-solo-5-8ghz-2-5w-37ch-vtx-w-smart-audio), [Reddit analog VTX 2026 (anekdot)](https://www.reddit.com/r/fpv/comments/1q8jttf/analog_vtx_sub_250_2026/), [diyfpv Unify Pro32 HV](https://www.diyfpv.com/product/tbs-unify-pro32-hv-25-1000mw-5-8ghz-vtx-mmcx), [yohorc analog VTX](https://yohorc.com/fpv-electronics/video-transmitters/analog/)
- **Fiber:** [Transwan fiber modül](https://www.transwan.com.cn/products/fiber-optic-module-for-fpv-drone-supports-protocol-of-ttl-elrs-tbs-sbus-and-crsf-expresslrs), [Streamblick (aynı ürün)](https://streamblick.com/products/fiber-optic-module-for-fpv-drone-supports-dji-protocol-of-ttlelrstbssbus-and-crsfexpresslrs), [SkycraftUA](https://skycraftua.com/en/product/modul-z-optovoloknom-dlya-fpv/), [RUID veri sayfası](https://www.fiberwdm.com/uploadfile/attachment/ac354cf7ee592e0e698bc53cf8c2ba57.pdf), [FPV.BASE hava ünitesi](https://fpvbasestore.com/en/product/FIB-0002/); iç: `/home/user/calismalar/fiber` README, `docs/yerlesim.md`, `docs/devre-analizi.md`, `docs/pazar-analizi.md`
- **GPS, ELRS, TR pazarı, ABD düzenleme:** önceki sürümdeki kaynaklar geçerli — [HGLRC M100-5883](https://www.hglrc.com/products/m100-5883-gps), [diyfpv M10Q-5883](https://www.diyfpv.com/product/matek-m10q-5883-gps-module-gps-compass), [RadioMaster RP](https://radiomasterrc.com/collections/rp-series-receivers), [FlyFive33 EP2](https://flyfive33.com/products/happymodel-2-4g-expresslrs-ep2-rx-receiver-module), [GEPRC C3 Gemini](https://geprc.com/product/geprc-elrs-915m-2-4g-c3-gemini-xrossband-receiver/), [Migitec](https://migitec.com/speedybee-f405-v4-bls-55a-30x30-fc-esc-stack/), [Robotzade](https://www.robotzade.com/urun/speedybee-f405-v4-bls-55a-30x30-ucus-kontrol-karti-esc), [Komponentci](https://www.komponentci.net/speedybee-f405-v4-bls-55a-30x30-ucus-kontrol-karti-ve-esc-pmu13370), [Orbit STACK F435](https://orbitteknoloji.com.tr/portfolio/stack-f435-bls-50a/), [Yuke Aero](https://yukeaero.com/blog/yuke-aero-neden-acik-ekosistem), [MEB Robot 2026 RC sabit kanat](https://robot.meb.gov.tr/yukleme/Robot2026/11_rc_sabit_kanat_ucak_v1.pdf), [fpvdroneessentials tarife](https://fpvdroneessentials.com/columns/us-drone-parts-tariffs-fpv), [Capstone DC](https://capstonedc.com/insights/regulatory-changes-to-foster-us-drone-supply-chains/)
