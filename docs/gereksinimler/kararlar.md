# Tasarım kararları (KRR)

Her karar: bağlam, seçenekler, seçilen ve gerekçe, etkilediği SYS/dosyalar.

## KRR-001 — Altium orijinalleri korunur, KiCad’e taşınır (2026-11-06)
**Bağlam:** esc55a ve fmu Altium’da; fiber/gofret KiCad 10 kullanıyor.
**Seçenekler:** 1) Altium dosyaları `boards/*/altium/` altında değişmeden kalır, KiCad projesi yanında kurulur. 2) Yalnız KiCad’e taşınmış hali tutulur.
**Karar:** 1 (ekip önerisi, müşteri onayı bekliyor). **Gerekçe:** taşıma hataları orijinalle karşılaştırılabilir; fiber’de de kaynak notlanmıştı.
**Etki:** PRJ-001; `boards/*/`, `CLAUDE.md`.

## KRR-002 — İlk ESC: 5", 55 A sürekli / 70 A anlık, 3–6S (2026-11-06)
**Bağlam:** Müşteri önce 5" ve akımın pazara göre seçilmesini istedi, kararı ekibe bıraktı (SOR-002, SOR-003).
**Seçenekler:** 1) 45 A 2) 55 A / 70 A anlık 3) 60–65 A.
**Karar:** 2. **Gerekçe:** 5" stack’lerin çoğu 55–60 A (SpeedyBee, iFlight, Diatone 55 A; GEPRC 60 A); 2207 motor tepe 38–45 A → %20–40 pay; esc55a zaten bu sınıfta (`docs/pazar-analizi.md` §2, §6). 7"/10" için esc65a sonra, 65 A ve 3–8S (gerilim sınıfı farkı; tek kart mı ayrı kart mı `sistem-mimari` değerlendirir).
**Etki:** esc55a gereksinimleri (SYS türetilecek); RSK-001 (akım ölçümü 55 × 4 A’ya göre yeniden boyutlanacak); RSK-003.

## KRR-003 — ESC yazılımı Bluejay, telemetri çift yönlü DShot ile (2026-11-06)
**Bağlam:** esc55a EFM8BB21 kullanıyor; J0.2 NC (inceleme E7). Müşteri kararı ekibe bıraktı.
**Seçenekler:** 1) Bluejay (açık kaynak, çift yönlü DShot RPM) 2) BLHeli_S (geliştirme durdu) 3) Kendi yazılımımız.
**Karar:** 1. **Gerekçe:** ücretsiz, bakımlı, Betaflight RPM filtresi; ek telemetri hattı gerekmez. 32 bit ESC’ye geçilirse AM32 (pazar eğilimi).
**Etki:** SOR-006 kısmen (ESC tarafı); `firmware/esc/`; esc55a port ataması bir Bluejay düzenine uymalı (`gomulu-yazilim`).

## KRR-004 — Uyumluluk hedefi: SpeedyBee F405 V4 / GEPRC Taker dizilimi, 30.5 mm (2026-11-06)
**Bağlam:** 8 pin dizilimi markaya göre değişiyor; müşteri “bazılarıyla uyumlu yeter” dedi (SOR-004).
**Seçenekler:** 1) En çok satan bütçe ailesinin dizilimi (SpeedyBee F405 V4, GEPRC Taker) 2) Kendi dizilimimiz + çevirici kablo 3) Mamba (fmu referansı) dizilimi.
**Karar:** 1, dizilimler üretici kılavuzlarından doğrulandıktan sonra (iki aile farklıysa SpeedyBee önce). Montaj 30.5 × 30.5 mm M3. **Gerekçe:** en büyük kullanıcı tabanı; GEPRC F405 HD V3 elimizde çizim olarak var.
**Etki:** `docs/pin-haritasi.md` (sistem-mimari), esc55a J0 ve fmu J0/J1 dizilimi değişebilir (inceleme E8).

## KRR-005 — FMU MCU pin ataması Betaflight `SPEEDYBEEF405V4` tabanlı (2026-11-10)
**Durum:** Onaylı (müşteri, 2026-11-11, DT-002 onayıyla; SYS-050 `Onaylı (DT-002)`).
**Bağlam:** KRR-004 SpeedyBee F405 V4 ailesiyle uyumu seçti; F405 LQFP64’te 8 DShot + LED + 6 UART + 3 SPI ancak DMA’sı dikkatle dağıtılırsa sığar (FeroFly V1.0 “motor 3 DMA” revizyonu). Cezeri Altium şeması (Mamba F405 MK2 tersine mühendisliği) müşterinin kendi şeması sayılmıyor (`docs/mimari-fmu.md`).
**Seçenekler:** 1) `SPEEDYBEEF405V4` (BF) + `speedybeef4v4` (AP) pinleri, belgelenmiş farklarla 2) Altium (Mamba) pinleri 3) Sıfırdan kendi ataması 4) GEPRC F405 pinleri.
**Karar:** 1. Farklar yalnız `docs/pin-haritasi.md` §1.4: SPI3’te flash (CS PC14), UART5 TX PC12, `ADC1_DMA_OPT 1`, PC5 = CUR2, baro parçası, VBAT 15:1. HSE 8 MHz.
**Gerekçe:** BF ve AP’de resmî, uçan hedef → hazır yazılımla çalışır (DOG-099), ArduPilot hwdef türevi kolay (SYS-056); 8 motor DMA çakışmasız (analiz, DOG-034); pazar lideriyle aynı pinler uyumluluk iddiasını güçlendirir. GEPRC MCU pinleri farklı, ikisi birlikte tutulamaz (8 pin ESC dizilimi KRR-004 ayrı konu).
**Etki:** SYS-035, 037, 050, 056; DOG-034, -049, -094, -099, -100; fmu şematiği (İP-05), `firmware/` config ve hwdef (İP-07). Boş GPIO kalmıyor (RSK-015).

## KRR-006 — Referans tasarım kullanım kuralı (2026-11-10)
**Durum:** Onaylı (müşteri, 2026-11-11, DT-002 onayıyla). SOR-014 cevabı “şimdilik kapalı” (KRR-009) → kural aynen geçerli; tasarım açık kaynağa çevrilirse yeniden değerlendirilir.
**Bağlam:** `docs/mimari-fmu.md` §1: açık F405 referansları farklı lisanslarda — CERN-OHL-P (FeroFly), -W (Mini-Air), -S (KURC), CC-BY-SA (Pixhawk), CC-BY-NC-SA (Revolution, Sparky2, Acci); ticari kartlar yalnız GPL-3 config/hwdef. Hukuki görüş değildir.
**Seçenekler:** 1) Hiçbir referanstan dosya kopyalanmaz; yalnız fikir ve yayımlanmış pin atamaları (işlevsel bilgi) kullanılır 2) İzin verici (P/W) kaynaklardan dosya alınır, bildirim korunur 3) Serbest kullanım.
**Karar:** 1. Tasarım veri sayfaları + `guc-ip03` hesapları + kendi `lib/` kütüphanemizle sıfırdan çizilir. Sembol, ayak izi, şema sayfası, yerleşim **kopyalanmaz**. NC lisanslı kaynaklar (CC-BY-NC-SA) **yalnız okunur**; -S ve CC-BY-SA kaynaklardan da dosya alınmaz. İleride P/W kaynaklı bir dosya gerçekten alınırsa önce bu KRR değişir, kaynak + lisans belgeye ve `CHANGELOG.md`’ye yazılır.
**Gerekçe:** Hiçbir lisans yükümlülüğü ürüne geçmez; kapalı/açık yayımlama kararı (SOR-014) serbest kalır; kopyalamanın kazancı küçük (parça seti zaten veri sayfasından). Kendi BF config ve AP hwdef’imiz o depolara girdiği için GPL-3’tür (SYS-050/056), bu ayrı.
**Etki:** Tüm tasarım ajanları (sematik, pcb, gomulu); `dogrulama-kalite` incelemesinde kaynak sorusu. SYS etkisi yok (kural, gereksinim değil).

## KRR-007 — FMU 8S stratejisi (2026-11-10)
**Durum:** Onaylı (müşteri, 2026-11-11, SOR-013: “önerini uygula” → seçenek 1).
**Bağlam:** M3 8S FMU ister (MUS-012). 8S LiHV dolu 34.8 V; SYS-014 kuralıyla (geçici + 5 V) VIN parçaları mutlak ≥ 45 V. M1 BOM’undaki SY8303 (40 V), AO3401A (−30 V), sigorta (32 V DC), SMBJ24CA 8S’e uymaz (`docs/mimari-fmu.md` §4.4). Onaylı SYS-003 “FMU iki ESC sınıfında değişmeden” diyordu.
**Seçenekler:** 1) M1 BOM 3–6S; PCB 8S BOM varyantına yer bırakır; M3’te yalnız BOM (gerekirse küçük revizyon) 2) M1 baştan 8S dayanıklı, tek BOM (tahmini +1–2 $/kart, `bom-tedarik` doğrulayacak) 3) M3’te ayrı FMU PCB’si.
**Karar:** 1. **Gerekçe:** M1 maliyeti zaten hedefin üstünde (SOR-016); 5" kullanıcısı 8S dayanımına para ödemez; 8S’in ayak izi riski (60 V buck kılıfı) yerleşim payıyla küçülür, M3 takvimi (2027 Q3) öncesi doğrulanır.
**Etki:** SYS-003, 022, 044, 046; DOG-003, -045, -097, -098; FMU şematik/PCB (İP-05/06), `bom-tedarik` 8S BOM listesi. Seçenek 2 seçilirse SYS-046 İptal, SYS-044’te M1 için ≥ 45 V, SYS-002’ye +1–2 $.

## KRR-008 — Yüksek sıcaklık bileşen sınıfı kuralı (2026-11-11)
**Durum:** Kural onaylı (müşteri talebi MUS-014, DT-003); sayısal sınırlar [öneri] — `bom-tedarik` (bulunabilirlik, LCSC stoğu, fiyat) ve `sistem-mimari` (EFM8BB21 I sınıfı, STM32F405RGT7) doğrulamasından sonra SYS-085…087 `Onaylı`.
**Bağlam:** Müşteri: “Kart yüksek derecelere çıkar. Ona göre komponentleri güncelle.” guc-ip03 §2.5: ESC sınır akımda kart ortalaması ≈ 95–99 °C, MOSFET kılıfı ≈ 110 °C; X5R (+85 °C) aşılır (G6). FMU kart kaybı ≈ 2.5 W → 60–90 °C (masa, tahmin), STM32F405RGT6 (−40…85 °C) sınırda (G18); FMU yığında ESC’nin üstünde. Onaylı SYS-083 yalnız “≥ −20…+85 °C” istiyordu (ortam −10…+50 °C’ye göre yazılmıştı, kart ısınmasını hesaba katmıyordu).
**Seçenekler:** 1) Sınıf kartın tasarım sıcaklığına göre: ESC ≥ 125 °C, FMU ≥ 105 °C, istisnalar ölçümle gerekçeli 2) Her iki kartta ≥ 125 °C (FMU’da IMU/baro/OSD için muadil yok → uygulanamaz) 3) ≥ 85 °C kalır, ısı yalnız yerleşim/akım sınırıyla yönetilir (müşteri talebine aykırı).
**Karar:** 1. Kural tablosu:

| Parça türü | ESC (SYS-086) | FMU (SYS-087) |
|---|---|---|
| Seramik kondansatör | X7R veya üstü (X7S, X8R, C0G); X5R/X6S/Y5V yok | X7R veya üstü |
| Elektrolitik / polimer / tantal | Kartta yok | Kullanılırsa ≥ 105 °C |
| Set (kutu) kondansatörü | Silindirik Al elektrolitik, 105 °C (SYS-063) | — |
| Direnç, shunt, ferrit, bobin | ≥ 125 °C (öz ısınma dahil) | ≥ 105 °C (çoğu 125–155 °C, ek maliyet yok) |
| MOSFET, diyot, TVS | T_j,maks ≥ 150 °C | T_j,maks ≥ 150 °C |
| IC (sürücü, akım yükselteci, buck, LDO) | ≥ 125 °C tercih; 105 °C yalnız muadil yoksa ve ölçülen kılıf ≤ 90 °C | ≥ 105 °C |
| MCU | EFM8BB21 I sınıfı (−40…125 °C) [doğrulanacak] | STM32F405RGT7 (−40…105 °C) |
| IMU, baro, OSD, flash | — | ≥ 105 °C; muadil yoksa 85 °C, kılıf ≤ 70 °C ölçülür |
| Kristal / osilatör | (kullanılırsa) ≥ 125 °C | ≥ 105 °C; yoksa 85 °C istisnası |
| Konnektör (SH, USB-C), LED, buzzer | ≥ 125 °C; yoksa istisna listesi + yerel ölçüm | ≥ 105 °C; yoksa 85 °C, yerel ≤ 70 °C |
| Genel ölçüt | SYS-085 koşulunda her parça sınırının ≥ 15 °C altında | Yığın ölçümünde sınırın ≥ 15 °C altında |

**Gerekçe:** ESC tasarım sıcaklığı (kart 95 °C, sıcak nokta 110 °C) 15 °C payla 125 °C sınıfı ister; 105 °C IC yalnız soğuk bölgede kabul. FMU kendi kaybı + yığında ESC’den gelen ısıyla 85 °C sınırını aşabilir; 105 °C ekonomik orta yol, IMU/baro/OSD gibi 105 °C muadili olmayan işlevler yerleşim ve ölçümle korunur. STM32F405RGT7 aynı kalıp ve pin dizilimi → Betaflight/ArduPilot ve pin haritası (KRR-005) etkilenmez. Pasiflerin çoğu (X7R, kalın film direnç) zaten bu sınıfta; maliyet farkı MCU’larda ve bazı IC’lerde yoğunlaşır.
**Etki:** SYS-083 (Değişti), SYS-085…087 (yeni); DOG-082, DOG-104…108; `bom-tedarik` BOM taraması ve fark maliyeti (SYS-002, PRJ-004 ≤ 32 $, RSK-004, RSK-017); `sematik-muhendisi` parça numaraları (EFM8BB21F16I?, STM32F405RGT7, C_boot X7R); `bom-maliyet.md` R3 (bulk X5R tasarrufu) reddedilir; `pcb-muhendisi` 85 °C istisna parçalarını ısı kaynaklarından uzak yerleştirir (RSK-018).

**Güncelleme (müşteri, 2026-11-11):** FMU sütunu gevşetildi: “İşlemciyi bu sıcaklık durumundan muaf tut. FMU kartı hiçbir zaman ESC kadar yüksek bir sıcaklığa ulaşmayacak. ESC önemli olan!” → FMU parçaları ≥ 85 °C, MCU STM32F405RGT6; ESC kuralı (≥ 125 °C, X5R yok) değişmedi. Etki: FMU 27.06 → 17.72 $/kart (RGT6 + W25Q128JV), `boards/fmu/bom-revb.csv`.

## KRR-009 — Tasarım şimdilik kapalı, açık belge yayımlanır (2026-11-11)
**Durum:** Onaylı (müşteri, 2026-11-11, SOR-014: “tamam”).
**Bağlam:** SOR-014: şema/PCB açık kaynak mı? Açık referansların lisansları (KRR-006) ve kopyalanma riski.
**Seçenekler:** 1) Şimdilik kapalı; açık belge = pin haritası, BF/AP hedefleri, kılavuz; 100 set sonrası yeniden açılabilir 2) CERN-OHL-W 3) CERN-OHL-P.
**Karar:** 1. Yayımlanacak: `docs/pin-haritasi.md` türevi kullanıcı pin/ped haritası, Betaflight config ve ArduPilot hwdef (zaten GPL-3), kullanıcı kılavuzu (set kondansatörü zorunluluğu dahil). Şematik/PCB kaynak dosyaları ve BOM yayımlanmaz; şema PDF’i isteğe bağlı, ayrı karar. 100 set sonrası yeniden değerlendirilir.
**Gerekçe:** Kopyalanma riski düşer, karar geri alınabilir (kapalıdan açığa geçmek kolay, tersi değil); KRR-006 kuralıyla lisans yükümlülüğü yok.
**Etki:** PRJ-008; KRR-006 geçerli; SYS etkisi yok.

## KRR-010 — Seri üretim FMU MCU’su APM32F405RGT6, STM32F405RGT6 drop-in muadil (2026-11-12)
**Durum:** Onaylı (müşteri, 2026-11-12: “C’deki APM de uygun, gereksinimi gevşet. APM32F405 kullan.”; DT-005).
**Bağlam:** `docs/bom-maliyet.md` §10: stack 34.92 $ > 32 $ (PRJ-004). STM32F405RGT6 (C15742) JLC stoğu 24; dış tedarik ≈ 6.1–8.3 $/adet (+1.5…+3.8 $/stack). APM32F405RGT6 (Geehy, C5290473) 3.20 $ @100, stok 1 728, LQFP64 pin uyumlu, Betaflight’ta APM32F405 desteği var (§10.3 C1). SYS-030 “resmî STM32F405” diyordu.
**Seçenekler:** 1) APM32F405RGT6 seri, STM32F405RGT6 ALT (aynı ayak izi) 2) STM32F405RGT6 kalır, dış tedarikten alınır (≈ 32.9–35.1 $, hedef aşılır) 3) STM32 + C3/C4 tasarrufları (özellik kaybı; müşteri C2–C6’yı reddetti).
**Karar:** 1. **Gerekçe:** maliyet (−1.38 $/stack JLC fiyatına göre, dış STM32 fiyatına göre −2.9…−5.1 $) ve tedarik (stok sorunu kapanır; STM32 ikinci kaynak olarak kalır, SYS-095). Hiçbir özellik kaybolmaz; A + B + APM32 ≈ 29.97 $/stack.
**Koşullar / açık noktalar:** `gomulu-yazilim` Betaflight’ta APM32F405 config/derleme yolunu ve ArduPilot desteğini doğrular (DOG-023, DOG-112); ArduPilot desteklemiyorsa SYS-056 için RSK-020 seçenekleri (AP SKU’sunda STM32 dizimi veya DT). `sematik-muhendisi` iki veri sayfasının pin tablosunu karşılaştırır (VCAP, BOOT0, HSE, USB). Sıcaklık: APM32F405RGT6 sınıfı veri sayfasından SYS-087 (≥ 85 °C) için teyit edilir.
**Etki:** SYS-030 (Değişti), SYS-050/055/056/087 (doğrulama); DOG-023, -100, -101, -112; RSK-004, -017, -020; FMU BOM U201; `firmware/`.

## KRR-011 — Kritik parça muadil (ALT) kuralı (2026-11-12)
**Durum:** Onaylı (müşteri talebi MUS-016, 2026-11-12; SYS-095). Kritik parça listesinin tamamı ve istisnalar `bom-tedarik` BOM’unda; istisnalar müşteriye bildirilir.
**Bağlam:** Müşteri: “Tasarımda değişiklik yapmadan yerine muadil komponent takabilmek isterim.” Bugünkü bulgular: STM32 stok 24, JW5026 stok 132 (RSK-019); bazı ALT önerileri farklı kılıflı (INA281B2 ↔ INA240A3).
**Seçenekler:** 1) Her kritik parçaya pin + ayak izi uyumlu ALT, ortak ayak izi, aynı yazılım imajı; olmazsa gerekçeli istisna 2) Çift ayak izi (iki ayrı ped grubu, biri boş) — alan ister, 30.5 mm FMU’da uygulanamaz 3) Yalnız stok takibi, muadil gerekince PCB revizyonu (müşteri talebine aykırı).
**Karar:** 1. Uygulama kuralı:

| # | Kural |
|---|---|
| 1 | Kritik parça: MCU, MOSFET, kapı sürücü, akım yükselteci, buck/LDO, IMU, baro, OSD, flash, konnektörler (SH, USB-C), TVS, bobin, kristal, sigorta, ters kutup MOSFET’i, SBUS çevirici ve işlevi tek parçaya bağlı her IC. Direnç/seramik kondansatör kritik değildir (genel değer + kılıf yeterli; BOM’da “genel” işaretli) |
| 2 | BOM’da her kritik satır: MPN, LCSC, **ALT MPN, ALT LCSC**, ALT üretici, ALT stok, ALT fiyat, “drop-in kanıtı” (iki veri sayfası sayfa no) |
| 3 | ALT tercihen farklı üretici; aynı üreticinin farklı sipariş kodu yalnız farklı üretici yoksa (gerekçe yazılır) |
| 4 | Pin dizilimi ve kılıf ölçüsü aynı; ayak izi iki veri sayfasının ped önerisini kapsar (`pcb-muhendisi`). Şematikte iki parçanın farklı gerektirdiği pasif varsa (ör. VCAP, FB direnci) değer iki parçayı da karşılar; karşılamıyorsa drop-in sayılmaz |
| 5 | ALT, ana parçanın bağlı olduğu tüm SYS’leri karşılar: gerilim/akım sınıfı (SYS-014, 044), sıcaklık sınıfı (ESC ≥ 125 °C SYS-086, FMU ≥ 85 °C SYS-087), doğruluk (SYS-021, 022), işlev (SYS-031 8 kHz vb.) |
| 6 | Yazılım: ALT aynı Betaflight / ArduPilot / Bluejay imajında otomatik tanınır (WHO_AM_I/PROD_ID/JEDEC ID ile) veya yazılım ayarı değişmez. Ölçek değişiyorsa (ör. akım yükselteci kazancı) ALT aynı kazançta olmalı. MCU için özel durum: RSK-020, SOR-018 |
| 7 | Muadili bulunmayan kritik parça → istisna listesi: parça, neden (tek üretici, yazılım, sıcaklık sınıfı), önlem (peşin alım, stok izleme, PCB revizyon planı), risk; müşteriye bildirilir |
| 8 | Prototipte en az bir FMU ve bir ESC ALT’larla dizilir (DOG-111); 100 set öncesi ALT’ı denenmemiş parçalar listelenir |

**Gerekçe:** Müşteri isteği; seri üretimde stok kesintisi (STM32, JW5026) PCB revizyonu olmadan aşılır; ortak ayak izi alan maliyeti olmadan sağlanır (seçenek 2 alan ister).
**Etki:** SYS-095 (yeni), SYS-091 (ilişkili); DOG-110, DOG-111; RSK-019, RSK-021; tüm BOM’lar (İP-02), şematik alanları (İP-05), ayak izleri (`lib/`, İP-06), firmware config (baro/IMU/flash çoklu sürücü, İP-07). §10.7’deki “ALT” kodlarından farklı kılıflı olanlar (INA281B2 ↔ INA240A3) bu kurala göre drop-in değildir.
