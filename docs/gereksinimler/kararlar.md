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
**Durum:** **Değişti — yerini KRR-012 aldı (müşteri, 2026-11-13, DT-006).** APM32F405RGT6 artık seri MCU değil, yalnız tedarik krizinde dizilen STACKF405A varyantı; STM32F405RGT6 ArduPilot varyantı (STACKF405). Önceki durum: Onaylı (müşteri, 2026-11-12: “C’deki APM de uygun, gereksinimi gevşet. APM32F405 kullan.”; DT-005).
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
| 6 | Yazılım: ALT aynı Betaflight / ArduPilot / Bluejay imajında otomatik tanınır (WHO_AM_I/PROD_ID/JEDEC ID ile) veya yazılım ayarı değişmez. Ölçek değişiyorsa (ör. akım yükselteci kazancı) ALT aynı kazançta olmalı. MCU için özel durum: varyant başına ayrı resmî derleme (SOR-018 cevabı, KRR-012, DT-006; RSK-020 kapandı) |
| 7 | Muadili bulunmayan kritik parça → istisna listesi: parça, neden (tek üretici, yazılım, sıcaklık sınıfı), önlem (peşin alım, stok izleme, PCB revizyon planı), risk; müşteriye bildirilir |
| 8 | Prototipte en az bir FMU ve bir ESC ALT’larla dizilir (DOG-111); 100 set öncesi ALT’ı denenmemiş parçalar listelenir |

**Gerekçe:** Müşteri isteği; seri üretimde stok kesintisi (STM32, JW5026) PCB revizyonu olmadan aşılır; ortak ayak izi alan maliyeti olmadan sağlanır (seçenek 2 alan ister).
**Etki:** SYS-095 (yeni), SYS-091 (ilişkili); DOG-110, DOG-111; RSK-019, RSK-021; tüm BOM’lar (İP-02), şematik alanları (İP-05), ayak izleri (`lib/`, İP-06), firmware config (baro/IMU/flash çoklu sürücü, İP-07). §10.7’deki “ALT” kodlarından farklı kılıflı olanlar (INA281B2 ↔ INA240A3) bu kurala göre drop-in değildir.

## KRR-012 — Seri FMU MCU’su AT32F435RGT7; STM32F405 ve APM32F405 aynı PCB’de varyant (2026-11-13)
**Durum:** Onaylı (müşteri, 2026-11-13: seri MCU AT32F435RGT7 — “Evet”; varyant planı; 2026-11-12 SOR-018: “Betaflight, INAV her ne için olursa olsun 2–3 farklı derleme bile yaparız; farklı varyantlar olarak satarız. Yeter ki üretebilelim.”). KRR-010’un yerini alır. DT-006.
**Bağlam:** Müşteri “AT32’yi hem INAV hem Betaflight destekliyor… değerlendir” dedi. `docs/rapor/mcu-secimi.md` (2026-11-12): AT32F435RGT7 (C3029577) 3.27 $ @100, JLC stok 865; Betaflight ≥ 4.5.0 (37 kayıtlı kart), INAV ≥ 6.1 (9.1.0’da 12 hedef); 288 MHz / 384 KB RAM / DMAMUX 14 kanal. LQFP64’te STM32F405RG ile 62/64 pin aynı; fark pin 31/47 (VCAP_1/VCAP_2 ↔ PH3/PH2), 2.2 µF VCAP kondansatörleri AT32’de zararsız → tek PCB üç MCU’yu taşır (emsal BF `REVO_AT`). ArduPilot AT32 ve APM32’yi desteklemiyor (master `aea9a1b`); APM32F405 INAV’da yok, BF’de ≥ 2025.12 ve kayıtlı kartı yok (`docs/rapor/yazilim-inceleme.md` §1).
**Seçenekler:** 1) AT32F435RGT7 seri; STM32F405RGT6 ArduPilot varyantı; APM32F405RGT6 tedarik yedeği — aynı PCB, MCU başına ayrı derleme 2) APM32F405RGT6 seri kalır (KRR-010; INAV yok, BF’de ilk kart biz) 3) STM32F405RGT6 tek MCU (stok 74, dış tedarik +1.4…+5 $/stack).
**Karar:** 1. Varyant planı:

| SKU | MCU (LCSC) | Betaflight | INAV | ArduPilot | Kullanım |
|---|---|---|---|---|---|
| **STACKF435** | AT32F435RGT7 (C3029577) | ≥ 4.5.0, `AT32F435G` derlemesi + `STACKF435` config | ≥ 9.1 (LSM6DSV16X), kendi hedef `target_at32f43x_xGT7` | ✗ | Seri, standart |
| **STACKF405** | STM32F405RGT6 (C15742) | ≥ 4.5, `STM32F405` derlemesi + config | ≥ 9.1, aynı hedef klasörü `target_stm32f405xg` | ✓ kendi hwdef (`speedybeef4v4` türevi) | ArduPilot isteyene |
| **STACKF405A** | APM32F405RGT6 (C5290473) | ≥ 2025.12, `APM32F405` derlemesi + config | ✗ | ✗ | Yalnız tedarik krizinde |

Kurallar: (1) PCB, şematik ve pasifler üç varyantta aynı; fark U201 satırı (BOM varyantı) ve yazılım derlemesi. (2) VCAP_1/VCAP_2 2.2 µF X7R her varyantta takılı; VCAP ağları başka hiçbir yere bağlanmaz; PH2/PH3 hiçbir derlemede çıkış atanmaz. (3) HSE 8 MHz değişmez (BF AT32 saati 8 MHz’e sabit). (4) Pin ataması üç varyantta aynı (KRR-005, `SPEEDYBEEF405V4` tabanlı); AT32 config’inde yalnız `FC_TARGET_MCU`, `dmaopt` (0…8) ve `ADC1_DMA_OPT 9` farklı (`mcu-secimi` §3.4, §4.2). (5) MCU türü ipek baskı işaret kutusunda (F435 / F405 / A405) ve kutu etiketinde. (6) SYS-095 (d) için MCU istisnası: varyant başına ayrı resmî derleme. (7) Aynı aile yedeği AT32F435RMT7 (C5178940, `AT32F435M` derlemesi, stok 128) yalnız RGT7 bulunamazsa, ayrı DT ile.
**Gerekçe:** Betaflight + INAV resmî desteği ve geniş emsal (8 motorlu AT32 kartları dahil); stok 865 ≥ 2 × 100; APM32’ye göre yalnız +0.07 $/stack; daha fazla işlemci ve DMA payı (RSK-014 azalır); STM32 ArduPilot için, APM32 kriz yedeği olarak aynı PCB’de kalır → müşterinin “yeter ki üretebilelim” önceliği (MUS-017) PCB revizyonu olmadan karşılanır.
**Bilinen kısıtlar:** AT32 Betaflight/INAV’da 288 MHz / LDO 1.3 V ile koşar → bu kipte −40…85 °C ve VDD ≥ 3.0 V (DS Tablo 16); MCU akımı STM32’den yüksek (DS tip. 231.6 mA tüm çevre açık, azami 260 mA; gerçek tahmin 100–150 mA) → 3.3 V bütçesi (`guc-elektronigi`, DOG-041/115). BF AT32’de PPM ve DShot DMAR yok (SYS’te gerek yok). 8 kanal zamanlayıcı tabanlı çift yönlü DShot AT32’de tezgâhta denenmedi (RSK-024). Windows’ta Artery DFU için sürücü adımı gerekebilir (kılavuz). Configurator MCU türünü denetlemez → yanlış varyant dosyası (RSK-026).
**Maliyet:** STACKF435 ≈ 30.04 $/stack (KRR-010 tabanı 29.97 $ + 0.07; `mcu-secimi` §4.4) ≤ 32 $ (PRJ-004) — tahmin, IMU farkı (KRR-013) hariç; 4. adım muadil taramasında `bom-tedarik` yeniden hesaplar. STACKF405: JLC fiyatıyla +1.38 $, dış tedarikle +2.9…+5.1 $ (SKU fiyatına yansır, PRJ-009). STACKF405A: −0.07 $.
**Etki:** SYS-030, 037, 050, 056, 058 (yeni), 087, 095 (d); PRJ-006, PRJ-009 (yeni); DOG-023, -034, -041, -049, -050, -095, -099, -100, -101, -107, -112 (değişti), DOG-113…117 (yeni); RSK-014, -017, -020 (kapandı), RSK-022…026 (yeni); `sematik-muhendisi` U201 alanları ve pin 31/47 notu; `guc-elektronigi` 3.3 V bütçesi; `gomulu-yazilim` `STACKF435` BF config + INAV hedefi; `pcb-muhendisi` ipek baskı işareti; `bom-tedarik` U201 satırı, varyant BOM’ları, peşin alım; `sistem-mimari` `docs/pin-haritasi.md` §1.3 AT32 `dmaopt` sütunu.

## KRR-013 — IMU ana parçası LSM6DSV16X (2026-11-13)
**Durum:** Onaylı (müşteri, 2026-11-12: “LSM6DSV16X gayet iyi.”). DT-006.
**Bağlam:** FMU BOM’undaki “ICM-42688-P (Tokmas)” C54308212 veri sayfasına göre farklı bir yonga (kimlik 0x1F = 0xA1, WHO_AM_I 0x47 yok, gyro ODR 7.04/14.08 kHz) → Betaflight ve ArduPilot tanımaz; HXY klonu da farklı (`yazilim-inceleme` §3). TDK orijinali C1850418 ≈ 19–21.6 $, stok ≈ 33 → maliyet ve tedarik dışı. LSM6DSV16X (ST, C5267406) 3.35 $, stok 9 300; BF ✓ (`accgyro_spi_lsm6dsv16x.c`, 4.5.0’dan beri; AT32 kartlarda kullanılıyor), INAV ≥ 9.1 (`accgyro_lsm6dxx.c`, kimlik 0x70; 9.0 ve 8.0’da yok), ArduPilot ✓ (`LSM6DSV`).
**Seçenekler:** 1) LSM6DSV16X ana 2) TDK ICM-42688-P (pahalı, stok yok) 3) ICM-42605 / IIM-42652 (TDK ailesi, 11–12 $) 4) BMI270 (BF’de 3.2 kHz; müşteri C3’ü reddetti).
**Karar:** 1. SYS-031 IMU’dan bağımsız yazıldı: “LSM6DSV16X ya da BF + INAV (+ STM32 varyantında AP) destekli eşdeğeri”; örnekleme ölçütü LSM6DSV16X veri sayfasının azami gyro ODR’sine göre **≥ 7.68 kHz** (eski 8 kHz). SYS-037 gyro/PID hızı buna göre.
**Gerekçe:** Üç uçuş yazılımında da resmî sürücü; stoklu ve ucuz; Tokmas kimlik riski kalkar.
**Kısıtlar:** ICM-42688-P ile pin dizilimi farklı (LGA-14L 2.5 × 3 mm) → şematik sembol/bağlantı ve ayak izi değişir (`sematik-muhendisi`, `pcb-muhendisi`). INAV ≥ 9.1 zorunlu (RSK-023). Sıcaklık sınıfı −40…85 °C [`bom-tedarik` veri sayfasıyla teyit] → SYS-087 ≥ 85 °C ✓, yığında ≤ 70 °C ölçütü. Drop-in muadil (SYS-095) bugün tanımsız: aynı ayak izli, aynı yazılımla tanınan eşdeğer 4. adım muadil taramasında aranır; bulunmazsa istisna listesi (RSK-021). IMU besleme süzgeci (SYS-042) LSM6DSV16X veri sayfası önerisine göre yeniden bakılır (`guc-elektronigi`).
**Maliyet:** Tokmas 2.12 $ → LSM6DSV16X 3.35 $ (fiyat kademesi doğrulanmadı) ≈ **+1.2 $/stack** (tahmin) → AT32 + LSM6DSV16X ≈ 31.3 $ ≤ 32 $, pay ≈ 0.7 $ (RSK-004); `bom-tedarik` 4. adımda 100 set fiyatıyla yeniden hesaplar.
**Etki:** SYS-031, 037, 056, 058, 087; DOG-024, -025, -095, -099, -100, -101, -113, -114; RSK-004, -021, -023; FMU şematiği U301 + ayak izi, BOM, `firmware/` (BF config gyro sürücüsü, INAV hedefi, AP hwdef IMU satırı).

