# Crow — marka ve pazarlama planı

Sahibi `pazar-analisti`. Tarih: 2026-11-11 (rev 3). Girdi: marka **Crow** (K12); dil/logo/slogan/ad/açıklık **K13**. Km taşları M1…M11 + M4a. Fiyatlar USD; bütçe **tahmin**.

**Erteleme (müşteri, 2026-11-11):** domain satın alınmaz; tescil şimdi yapılmaz.

**Logo taslakları:**
| Dosya | Kullanım |
|---|---|
| [`crow-fpv-logo.jpg`](crow-fpv-logo.jpg) | Web, kutu, belge — 30.5 kare + gaga + Crow FPV + Fly to Joy |
| [`crow-fpv-logo-pcb.jpg`](crow-fpv-logo-pcb.jpg) | **PCB ipek** önizlemesi (KiCad çıktısı) — tek parça dolu gaga; kare yok. 2026-11-13: gaga içine oyulmuş CROW yazısı kaldırıldı (6–8 mm’de harf boşlukları JLC ipek sınırının altında, basılmıyordu). Yazı gerekiyorsa ayrı KiCad metni olarak gaganın sağında |
| [`crow-fpv-logo-pcb.svg`](crow-fpv-logo-pcb.svg) | PCB / CAD — vektör, 8 mm |
| `lib/stack.pretty/Crow_Logo_{6,8}mm`, `Crow_Logo_Text_{6,8}mm` | KiCad ayak izleri (F.SilkS): yalnız işaret / işaret + CROW (6 mm: 1.2 mm yazı, 8 mm: 1.6 mm). FMU (36 mm) için 6 mm, ESC için 8 mm önerilir |
| [`crow-fpv-logo-pcb.dxf`](crow-fpv-logo-pcb.dxf) | PCB — poliline (mm), 8 mm; hepsi `python3 tools/crow_logo_pcb.py` ile üretilir |

## Kararlar (müşteri, 2026-11-11 — K13)

| # | Karar | Etki |
|---|---|---|
| K13-1 | **Dil: EN-first** | Web, kutu birincil dil İngilizce; TR destek ve gerektiğinde TR alt satır (kutu/web). AliExpress/AB yolu erken açılır |
| K13-2 | **Logo: gaga** — 30.5 × 30.5 kare içinde soyut gaga/kafa | §3 brief kilitli (seçenek a) |
| K13-3 | **Slogan: Fly to Joy** (müşteri: “fly to joy gibi”) | Ana slogan EN; ölçüm mesajı slogan değil, raporda kalır |
| K13-4 | **Ad: Crow FPV** (tescil hedefi aynı); domain crowfpv.com | **2026-11-11 müşteri:** domain **şimdi alınmaz**; tescil **şimdi yapılmaz**. Ad/logo brief kilitli kalır |
| K13-5 | **Açık belge sınırı:** yalnız **pin haritası + kılavuz**, poster/tek sayfa formunda (rakipler gibi). **Şema PDF açık değil** | D2 daraltıldı |

## Özet

| Konu | Kilitli değer |
|---|---|
| Marka | **Crow FPV** (ürün ailesi); isimler Crow F405, Crow ESC 55, Crow Stack 55 … |
| Slogan | **Fly to Joy** |
| Dil | **EN-first**; TR destek ikincil |
| Logo | 30.5 kare + soyut **gaga** |
| Belge | Pin haritası + kılavuz (poster); şema kapalı |
| Konumlandırma | SpeedyBee fiyat bandında; ölçülmüş (rapor), pin/kılavuz net, tek dizilim; EN global |
| En büyük risk | “Crow” savunma/dron kalabalığı → bileşik **CROW FPV** + logo; kutu öncesi vekil |

---

## 1. Marka konumlandırma

**Crow FPV**, Türkiye’de tasarlanan, ölçümle satılan FPV aviyonik ailesidir. Slogan: **Fly to Joy**. Kendi dronunu toplayan 5"–10" FPV pilotlarına ve küçük entegratörlere; SpeedyBee fiyat bandında (stack 59–65 $ hedefi), **etikette yazanı ölçümle gösteren**, net **pin haritası + kılavuz** (şema kapalı; rakipler gibi) ve M1’den M11’e **tek 8 pin diziliminde** birbirine takılan ürünler vaat eder. Birincil dil **İngilizce** (global / AliExpress / AB); TR destek ve yerelde stok ikincil kanaldır. SpeedyBee/GEPRC/Matek Çin kaynaklıdır ve ölçüm raporu yayımlamaz. Crow’un farkı: **seri ürün + ölçüm raporu + pin/kılavuz netliği + tek dizilim**.

| # | Değer | Somut karşılık (kanıt) | Rakipte durum |
|---|---|---|---|
| D1 | **Ölçülmüş** | Her SKU için yayımlanmış rapor: sürekli/anlık akım, ısı, akım sensörü doğruluğu, BEC (DOG, `test/`) | SpeedyBee/GEPRC/Matek: yalnız üretici iddiası |
| D2 | **Net kurulum belgesi** | **Pin haritası + kılavuz** (poster / tek sayfa, EN birincil). Şema PDF **yayımlanmaz** (K13-5) | Matek/SpeedyBee: pin + manual; şema genelde kapalı |
| D3 | **Ulaşılabilir destek** | EN destek birincil; TR destek ve TR stok ikincil (≤ 48 saat yanıt hedefi) | Yabancı markalar bayi üzerinden |
| D4 | **Tek aile, tek dizilim** | Tüm Crow FC/ESC aynı 8 pin (KRR-004); 30.5; fiber dahil | Markalar arası dizilim değişiyor |
| D5 | **Doğru akım ölçümü** | Kalibre sensör, raporda hata payı (%) | Kalibrasyon şikâyeti yaygın (anekdot) |

**Yapılmayacak vaat:** “en hafif”, “en güçlü”, “askerî sınıf”. Ölçülmemiş hiçbir sayı reklamda kullanılmaz (D1 ile çelişir).

---

## 2. İsim sistemi

### Kural

`Crow <aile> <temel sayı>[-<hücre>][ <ek>] [V<n>]`

- **Aile:** FC adı MCU sınıfıdır (F405, F722, H743); ESC `ESC`; set adları `Stack`, `Dual`, `LR`; diğerleri `Wing`, `GPS`, `RX`, `VTX`, `Link`.
- **Temel sayı:** ESC’de sürekli akım (A), VTX’te üst güç (mW), RX’te bant.
- **Hücre eki** yalnız varsayılan (3–6S) dışındaysa: `-8S`.
- **32 bit ESC** eki: `AM32`. 8 bit (Bluejay) ek almaz (varsayılan).
- **Sürüm** `V2`, `V3` … yalnız uyumsuz değişiklikte; PCB revizyonu (Rev A/B) ürün adına girmez.
- **Yasak adlar:** `Crow Racer` (Craycle ürünü, TR), `Karga` / `Kargu` (Z-Sistem KARGA-40 ve STM KARGU mühimmatları); silah/saldırı çağrışımlı ekler (Strike, Hunter, Kamikaze).

### Ürün adları (M1…M11)

| KT | Ürün | Pazar adı (EN) | TR etiket alt satırı | EN etiket alt satırı |
|---|---|---|---|---|
| M1 | F405 FMU | **Crow F405** | Uçuş Kontrol Kartı · 3–6S · 30.5 | Flight Controller · 3–6S · 30.5 |
| M1 | 55 A ESC | **Crow ESC 55** | 4’ü 1 Arada ESC · 55 A · 3–6S | 4-in-1 ESC · 55 A · 3–6S |
| M1 | Stack | **Crow Stack 55** | Uçuş Kartı + ESC Seti | FC + ESC Stack |
| M2 | 65 A ESC | **Crow ESC 65** / **Crow Stack 65** | 4’ü 1 Arada ESC · 65 A · 3–6S | 4-in-1 ESC · 65 A · 3–6S |
| M3 | 8S ESC | **Crow ESC 65-8S**, **Crow ESC 80-8S** | 4’ü 1 Arada ESC · 3–8S | 4-in-1 ESC · 3–8S |
| M3 | 8S FMU | **Crow F405-8S** | Uçuş Kontrol Kartı · 3–8S | Flight Controller · 3–8S |
| M3 | GPS | **Crow GPS M10** | GPS + Pusula Modülü | GPS + Compass Module |
| M3 | Set | **Crow LR** (Long Range set) | Uzun Menzil Seti · 7"–10" · 8S | Long Range Set · 7"–10" · 8S |
| M4 | F7 FMU | **Crow F722** | Uçuş Kontrol Kartı · Betaflight / INAV | Flight Controller · Betaflight / INAV |
| M4a | Dual-ESC FMU | **Crow F722 Dual** (F405 varyantı: **Crow F405 Dual**) | 8 Motor · 2 ESC Girişi | 8 Motors · Dual ESC Port |
| M4a | Set | **Crow Dual Set** (2 × ESC + Dual FC) | Çift ESC Seti · 8 Motor | Dual ESC Set · 8 Motors |
| M5 | H743 FMU | **Crow H743** | Uçuş Kontrol Kartı · Betaflight / INAV / ArduPilot | Flight Controller · Betaflight / INAV / ArduPilot |
| M6 | Kanat FC + ESC | **Crow Wing F405-45** / **Crow Wing H743-50** | Kanat Uçuş Kartı + ESC · Ayrılabilir | Wing FC + ESC · Breakaway |
| M7 | AM32 ESC | **Crow ESC 60 AM32**, **Crow ESC 80-8S AM32** | 32 bit 4’ü 1 Arada ESC | 32-bit 4-in-1 ESC |
| M8 | ELRS alıcı | **Crow RX 2.4**, **Crow RX Dual** (LR1121) | ELRS Alıcı | ELRS Receiver |
| M9 | VTX L1 | **Crow VTX 600** | Analog Görüntü Vericisi | Analog Video Transmitter |
| M10 | VTX L2 | **Crow VTX 2500** | Analog Görüntü Vericisi · 7–36 V | Analog VTX · 7–36 V |
| M11 | Fiber | **Crow Link Air** / **Crow Link Ground** (set: **Crow Link**) | Fiber Optik Kumanda Bağlantısı | Fiber Optic Control Link |

**Not:** “F7” adıyla H743 satılmaz (yol haritası §F); M5 adı **Crow H743**. “Stack” TR’de de yerleşik terim; TR alt satırda açıklanır, ad çevrilmez.

---

## 3. Görsel kimlik notları (brief; uygulatma yok)

| Unsur | Brief |
|---|---|
| Metafor | Karga/kuzgun = zekâ, dikkat; saldırgan yırtıcı değil. Tek geometrik çizgi; kuş bütün çizilmez |
| Logo | **Kilitli:** 30.5 × 30.5 kare içinde soyut **gaga/kafa** + “CROW FPV” / “CROW” |
| Slogan | **Fly to Joy** — kutu önü, web hero, video outro |
| Dil | Kutu/web **EN birincil**; isteğe bağlı küçük TR alt satır; destek EN + TR |
| Renk | Mat siyah `#111214`, grafit `#3A3D42`, açık gri `#C9CCD1`, vurgu `#3F4FA0` (tahmin); uyarı/ölçüm kehribar `#F2A900` |
| Tipografi | Geometrik sans (OFL); teknik değerler mono |
| PCB | Siyah maske + beyaz ipek, logo küçük |
| Kutu | Siyah karton; ön: foto + **Fly to Joy** + değer satırı; arka: EN özellik + pin/kılavuz QR |
| Kurulum posteri | Rakipler gibi: **pin haritası + kısa kılavuz**; şema yok |
| Kaçınılacak | Nişangâh, kamuflaj, askerî font; Indra/Crow Group benzeri logo |

---

## 4. Kanal stratejisi (km taşına göre)

| Kanal | M1 prototip (2026 Q4) | M1 100 set (2027 Q1) | M2–M3 (2027 Q2–Q3) | M4–M5 (2027 Q4–2028 Q1) | M6–M7 (2028 Q2–Q3) | M8–M11 (2028 Q4–2029 Q3) |
|---|---|---|---|---|---|---|
| **Web** crowfpv.com (EN) | Açılış + pin/kılavuz poster + ön kayıt + *Fly to Joy* | EN mağaza (USD); TR alt sayfa isteğe bağlı | Ölçüm raporu her SKU | Yazılım hedef sayfaları | Eğitim sayfası | RF uygunluk |
| **TR bayi** | Görüşme, numune | **1–2 bayi** | 3–5 bayi | Aynı | Eğitim bayisi | Aynı |
| **Pazar yeri** | — | Trendyol (TR) + **AliExpress hazırlığı** (EN-first) | AliExpress açılış (CE varsa) + Hepsiburada | AB bayi | Aynı | Aynı |
| **Topluluk** | Kapalı Discord (EN) | Açık Discord EN; TR Telegram ikincil | Ölçüm paylaşımı | Firmware beta | Okul kanalı | — |
| **YouTube** | 1–2 EN + 1–2 TR inceleme birimi | EN inceleme öncelikli | Uluslararası blog/kanal | Dual 8 motor demo | Kanat | VTX ölçüm |
| **Yazılım hedefi** | BF config | **Betaflight** | **INAV** | **ArduPilot** (M5) | INAV wing, **AM32** | ELRS (M8) |
| **AliExpress / AB** | Domain/EN hazırlığı | CE yolu başlar | **Açılış hedefi** (EN-first ile öne çekildi) | AB bayi | Aynı | RF yalnız RED sonrası |
| **Kurumsal / MEB** | — | İsteğe bağlı | — | ArduPilot demo | MEB / Teknofest | Fiber kurumsal (ad ayrımı §7) |

---

## 5. Lansman takvimi ve pazarlama aksiyonları

Bütçe bandı **tahmin** (USD, ürün maliyeti hariç pazarlama harcaması; inceleme birimleri BOM maliyetiyle). RF sertifika test bedeli pazarlama dışıdır, ayrı satır.

| Dönem | KT | Aksiyon / içerik | Kime | Bütçe bandı ($, tahmin) |
|---|---|---|---|---|
| 2026 Q4 | **M1 prototip** (5 set) | Vekil + **CROW FPV** tescil; **crowfpv.com** (+ .com.tr); logo (gaga) + *Fly to Joy*; EN açılış; pin/kılavuz poster; 2–4 inceleme birimi (EN+TR); Discord | Global + TR inceleyiciler | 1 000–2 500 |
| 2027 Q1 | **M1 100 set** + FC/ESC SKU | EN kutu (*Fly to Joy*), foto/video, **ölçüm raporu v1**, crowfpv.com mağaza, AliExpress hazırlık / erken liste, Trendyol + 1–2 TR bayi, Betaflight hedefi, lansman kodu | Global FPV + TR | 1 500–3 500 |
| 2027 Q2 | **M2** Crow ESC 65 | “65 A, 60 A fiyatına” + ısı/akım karşılaştırma videosu (kendi ölçüm; rakip ESC aynı tezgâhta) | 5"/7" freestyle | 800–2 000 |
| 2027 Q3 | **M3** Crow LR (8S + GPS) | 7" uzun menzil uçuş videosu, GPS Rescue gösterimi, 8S dayanım testi raporu; INAV hedefi; AliExpress/AB kararı | Uzun menzil pilotları | 1 000–2 500 (7" test dronu dahil) |
| 2027 Q4 | **M4 + M4a** Crow F722, Crow Dual | X8/8 motor ağır yük demo, “tek FC, iki ESC, tak-çalıştır” kablo videosu | Ağır yük, X-class, entegratör | 1 000–2 500 (X8 demo gövdesi) |
| 2028 Q1 | **M5** Crow H743 | “Aynı kart, üç yazılım” duyurusu; ArduPilot geliştiricilerine 2–3 numune; ArduPilot forumu | ArduPilot kullanıcıları, kurumsal | 500–1 500 |
| 2028 Q2 | **M6** Crow Wing | Teknofest/MEB fuar masası, okul seti (FC+ESC+kılavuz TR), 5–10 takıma destek | Lise/üniversite takımları, kanat pilotları | 2 000–6 000 (stand bedeli doğrulanmadı) |
| 2028 Q3 | **M7** Crow ESC AM32 | 32 bit ESC ölçüm raporu; Bluejay ↔ AM32 karşılaştırma | Mevcut Crow kullanıcıları | 500–1 500 |
| 2028 Q4 | **M8** Crow RX | Menzil testi videosu; **yalnız RED/BTK uygunluğu sonrası** satış | Tüm FPV | 500–1 500 + sertifika 3 000–10 000 (tahmin, ayrı bütçe) |
| 2029 Q1 | **M9** Crow VTX 600 | “Ölçülmüş çıkış gücü” tablosu (kanal başına) | Freestyle/giriş | 500–1 500 + sertifika |
| 2029 Q2 | **M10** Crow VTX 2500 | Uzun menzil/kanat paketi; lisans uyarısı belirgin | Lisanslı uzun menzil | 500–1 500 + sertifika |
| 2029 Q3 | **M11** Crow Link | Stack katmanı tanıtımı, CRSF telemetri demosu; kurumsal demo | Kurumsal, uzun menzil | 1 000–3 000 |

**Toplam (2026 Q4–2029 Q3, sertifika hariç):** ~11 000–30 000 $ (tahmin).

---

## 6. SKU / paket yapısı

SKU kodu: `CRW-<tip>-<değer>[-<hücre>]-V<n>`.

| Paket | Pazar adı | İçerik | SKU | KT | Hedef fiyat ($, öneri; yol haritası §B) |
|---|---|---|---|---|---|
| Stack seti | **Crow Stack 55** | Crow F405 + Crow ESC 55 + 8 pin kablo + kondansatör + damper + vida | CRW-STK-55-V1 | M1 | 59–65 |
| Tek FC | **Crow F405** | FC + kablo seti + damper | CRW-FC-F405-V1 | M1 | 35–39 |
| Tek ESC | **Crow ESC 55** | ESC + kondansatör + XT60 kablo | CRW-ESC-55-V1 | M1 | 28–33 |
| Stack 65 | **Crow Stack 65** | Crow F405 + Crow ESC 65 | CRW-STK-65-V1 | M2 | 72–78 |
| Long Range seti | **Crow LR** | Crow F405-8S + Crow ESC 65-8S (veya 80-8S) + Crow GPS M10 + kablolar | CRW-LR-65-8S-V1 / CRW-LR-80-8S-V1 | M3 | 95–105 |
| Dual-ESC seti | **Crow Dual Set** | Crow F722 Dual (veya F405 Dual) + 2 × Crow ESC + 2 × 8 pin kablo | CRW-DUAL-F722-V1 | M4a | 110–130 (tahmin) |
| Tek Dual FC | **Crow F722 Dual** | FC + 2 × kablo | CRW-FC-F722D-V1 | M4a | 48–55 |
| H7 FC / stack | **Crow H743** / **Crow Stack H743** | FC (+ ESC 65) | CRW-FC-H743-V1 | M5 | 55–65 / 105–115 |
| Kanat | **Crow Wing F405-45** / **H743-50** | Kırılabilir FC + 1 kanal ESC, servo kabloları | CRW-WNG-F405-45-V1 | M6 | 55–65 / 72–78 |
| Eğitim seti | **Crow Wing Edu** | Crow Wing + TR kılavuz + örnek INAV ayarı (okul/MEB) | CRW-EDU-WNG-V1 | M6 | Kurumsal fiyat (müşteri) |
| 32 bit ESC | **Crow ESC 60 AM32** | ESC + kondansatör | CRW-ESC-60-AM32-V1 | M7 | 45–50 |
| Alıcı / VTX | **Crow RX 2.4**, **Crow VTX 600 / 2500** | Modül + anten | CRW-RX-24-V1, CRW-VTX-600-V1 | M8–M10 | 13–16; 22–27; 45–52 |
| Fiber | **Crow Link** (Air + Ground) | Hava + yer ünitesi; fiber bobin ayrı | CRW-LNK-AIR-V1 / -GND-V1 / -SET-V1 | M11 | fiber deposunda |
| Aksesuar | **Crow Parts** | 8 pin kablo seti (Crow + SpeedyBee/GEPRC dizilim çevirici), 1000 µF 35 V / 50 V kondansatör, damper, XT60 kablo, LED, buzzer | CRW-ACC-<parça> | M1 | 1–8; set 5–8 |

**Kural:** Her set, içindeki kartlar tek tek de satılır (yedek parça talebi). Dizilim çevirici kablo, “tek aile” vaadinin (D4) rakip kartlarla da çalışan kanıtıdır.

---

## 7. Riskler

### 7.1 “Crow” ad çakışması (web taraması, 2026-11-11)

| Kullanan | Ülke | Alan | Bize etkisi |
|---|---|---|---|
| **Indra — CROW** C-UAS (anti-dron) sistemi | ES | Savunma, radar/RF sensör, karşı önlem | **Yüksek** kurumsal/savunma kanalında karışıklık; büyük şirket, tescili muhtemel (sorgulanmadı) |
| **Crow Electronic Engineering (The Crow Group)** | IL (1977, TR’de İzmir distribütörü) | Kablosuz alarm, RF (868 MHz, ZigBee), uygulama | **Yüksek** tescil çakışması: sınıf 9 elektronik; TR’de satışta. İtiraz riski |
| **Craycle — Crow Racer** 750 mm FPV uçak | **TR** (Buca, İzmir) | RC/FPV uçak kiti, STL, “elektronik bileşen” | **Orta–yüksek** TR FPV topluluğunda aynı ad; M6 “Crow Wing” ile karışabilir. Alternatif: işbirliği (Crow Racer + Crow Wing kombosu) — müşteri kararı |
| **Smart Birds — “Crow”** FPV saldırı dronu | RU | Askerî, Ukrayna yaptırım listesinde (2025-08) | **İtibar** riski: “Crow FPV” aramasında çıkabilir; AB/UA pazarında yanlış ilişkilendirme |
| **Hydronalix — CROW** İHA | US | Askerî lojistik İHA | Orta (ABD/kurumsal) |
| **CROW** (Avusturya) — BVLOS dron operasyonu; **Project Crow** (PL) — ArduPilot’lu kanat İHA | AT, PL | Savunma/İHA hizmeti | Orta (AB kurumsal) |
| Realacc Crow, TCMMRC Crow150 | CN | FPV çerçeve model adı | Düşük (model adı, mekanik) |
| **KARGA-40** (Z-Sistem), **KARGU** (STM) | TR | Dolanan mühimmat | Türkçe karşılık “Karga” **kullanılmaz** |
| Kaynak: Indra, thecrowgroup.com, craycle.com + ETBİS kaydı, liga.net, hydronalix.com, militaeraktuell.at, projectcrow.pl, yeniasir.com.tr, z-sistem.com (§Kaynaklar) | | | |

**Sonuç:** “Crow” FPV aviyonik **ürün markası** olarak kullanılmıyor (bulunamadı), ama kelime dron/savunma ve RF elektronikte yoğun. Tek kelime “CROW” sınıf 9’da reddedilebilir veya itiraz alabilir (tahmin; benzer kelime işaretleri için Hindistan’da 2024 ret kararı örneği var). Öneri:

1. **Tescil:** TÜRKPATENT’te **bileşik ve şekil işaret** (“CROW FPV” veya “CROW AVIONICS” + logo), sınıflar **9** (FC, ESC, alıcı, VTX, fiber modem), **12** (dronlar ve parçaları — vekil doğrular), **28** (RC model ve parçaları), istenirse **35** (çevrim içi satış). Başvuru **M1 100 set kutusu basılmadan önce** (2026 Q4). AB (EUIPO) ve Madrid başvurusu AB satışı kararıyla (M3).
2. **Önce araştırma:** marka vekili ile TÜRKPATENT + EUIPO + WIPO benzerlik araştırması (sınıf 9/12/28). Ret riski yüksek çıkarsa yedek: “Crow” ürün adı korunur, tescil “CROW FPV” bileşik işaretle yapılır.
3. **Kurumsal/savunma kanalında** (M6+, M11) ürün adı yanında şirket adı kullanılır; Indra CROW ile aynı cümlede anılmayacak açık ayrım.

### 7.2 Domain (RDAP / DNS, 2026-11-11)

| Domain | Durum | Öneri |
|---|---|---|
| crow.com | Kayıtlı (1997) | — |
| **crow.com.tr** | Kayıtlı, bir **dijital pazarlama ajansı** kullanıyor | Satın alma teklifi isteğe bağlı (S4) |
| crowdrone.com | Kayıtlı (2013) | — |
| crowflight.com | Kayıtlı (2023) | — |
| **crowfpv.com**, **crowavionics.com**, crowaero.com, crow-fpv.com, crowfpv.net | RDAP’te kayıt yok (boş görünüyor) | **crowfpv.com + crowavionics.com hemen alınsın** |
| crowfpv.com.tr, crowavionics.com.tr, crowaero.com.tr | DNS kaydı yok (boş olabilir; .tr için RDAP sorgulanamadı) | .com.tr başvurusu marka başvuru belgesiyle (TRABİS belge şartı doğrulanacak) |

Sosyal hesap adları (`@crowfpv`, YouTube, Instagram, Discord sunucu adı) domainle aynı gün alınır; mevcut durumları kontrol edilmedi.

### 7.3 Sertifika ve iddia mesajları

| Ürün grubu | Mesaj (kutu/web) | Not |
|---|---|---|
| FC, ESC (RF yok) | “CE (EMC + RoHS)” yalnız test/beyan yapıldıktan sonra yazılır | Bileşen olarak satılan kartlarda CE kapsamı doğrulanacak (`gereksinim-muhendisi` + vekil) |
| GPS (yalnız alıcı) | RED kapsamındadır (alıcılar da) | Sertifika yoksa CE işareti konmaz |
| **ELRS RX, VTX** (M8–M10) | “Kutudan çıkış 25 mW; yüksek güç yalnız amatör telsiz lisansı olanlar ve izinli bölgeler için” | AB’de 5.8 GHz lisanssız 25 mW EIRP; TR (BTK) sınırı ve Radyo Ekipmanları Yönetmeliği doğrulanacak. “2.5 W” reklamda tek başına kullanılmaz |
| **Crow Link** (fiber) | “Kumanda hattı RF yaymaz” — yalnız EMC testinden sonra | Güçlü fark mesajı; abartmadan (kart yine EMC kapsamında) |
| Tüm ürünler | Askerî/saldırı çağrışımlı dil yok; “sivil, hobi, eğitim” | Çift kullanım ve ihracat algısı; Smart Birds/Indra çağrışımından uzak durma |
| AB satış (M3+) | GPSR (2024) gereği AB’de sorumlu kişi, WEEE/EPR kaydı | Doğrulanacak; AliExpress/AB kararının ön koşulu |

---

## 8. Müşteri soruları — kapanış (2026-11-11)

| # | Cevap | Kilit |
|---|---|---|
| S1 | **EN-first** | K13-1 |
| S2 | **Gaga** (30.5 kare) | K13-2 |
| S3 | **Fly to Joy** | K13-3 |
| S4 | **Crow FPV** + crowfpv.com | K13-4 |
| S5 | Açıklık = **pin + kılavuz poster**; şema kapalı. Craycle teması ayrıca (isteğe bağlı) | K13-5 |

Açık kalan (ürün, yol haritası): M5 H743 kabulü; M6 ESC kanal sayısı; Craycle ile temas isteğe bağlı.

---

## Belirsizlikler

- TÜRKPATENT, EUIPO, USPTO veritabanları **sorgulanmadı**; çakışma tablosu web aramasıdır. Hukuki değerlendirme marka vekilinindir.
- .com.tr boşluğu DNS’e dayanıyor (RDAP yok); kayıtlı ama yayında olmayan olabilir.
- Bütçe bantları teklif almadan yapılmış tahmindir; Trendyol komisyonu, Teknofest stand bedeli, RF test bedeli doğrulanmadı.
- Betaflight üretici kaydı ve resmî hedef şartları (numune, üretici kodu) doğrulanmadı.
- Renk kodları başlangıç önerisidir; tasarımcı ve baskı provası ile kesinleşir.

## Kaynaklar (erişim 2026-11-11)

- Çakışma: [Indra CROW C-UAS](https://defence.indragroup.com/en/systems-services/c-uas-system), [Indra CROW broşür](https://www.indragroup.com/cms-content/importacion/indra_crow_20062022_en_b.pdf), [The Crow Group](https://thecrowgroup.com/), [Crow ürünleri](https://thecrowgroup.com/products/), [Crow LinkedIn](https://linkedin.com/company/crow-electronic-engineering-ltd), [EAS Güvenlik — Crow alarm TR](https://www.easguvenlik.com.tr/crow-kablosuz-alarm-sistemleri), [Craycle Crow Racer V2](https://craycle.com/product/crow-racer-v2-750-mm-fpv-racer-plane-complete-kit/), [Craycle iletişim (Buca, İzmir)](https://craycle.com/contact/), [Craycle ETBİS kaydı](https://etbis.ticaret.gov.tr/tr/SiteSorgulamaSonuc?siteId=653193fd-533f-4834-92be-229ba60a6687), [LIGA.net — Smart Birds “Crow” yaptırımı](https://news.liga.net/en/politics/news/zelenskyy-imposes-sanctions-against-ai-drone-manufacturers-for-the-russian-army), [Hydronalix CROW](https://www.hydronalix.com/crow), [CROW (AT)](https://militaeraktuell.at/en/crow-operational-solutions-for-modern-armed-forces/), [Project Crow (PL)](https://www.projectcrow.pl/), [Realacc Crow çerçeve](https://www.fpvracer.lt/model/realacc-crow-140mm-wheelbase-4mm-arm-fpv-racing-frame-kit-58g-18160.html), [TCMMRC Crow150](https://www.amazon.com/TCMMRC-Drone-Carbon-Racing-Crow150/dp/B0BR7RMK4P), [Hindistan CROW başvurusu ret kararı (2024)](https://tmrsearch.ipindia.gov.in/eregister/ShowCorrespondence/ShowCorrespondence.aspx?CRS_NO=WFlaW1xdKC8uKi4pKCp1S0k9WFlaW1xd)
- “Karga”: [Z-Sistem KARGA-40](https://www.z-sistem.com/tr/karga40), [Yeni Asır — STM KARGU (2026-10-17)](https://www.yeniasir.com.tr/yasam/2026/10/17/20-adet-karga-iha-hedefleri-es-zamanli-vurdu)
- Domain: Verisign RDAP (`rdap.verisign.com`, .com/.net) ve DNS sorgusu, 2026-11-11; [crow.com.tr](http://crow.com.tr) (ajans sitesi)
- Pazar ve fiyat: [`urun-portfoyu-yol-haritasi.md`](urun-portfoyu-yol-haritasi.md) §J, [`../pazar-analizi.md`](../pazar-analizi.md) kaynakları
