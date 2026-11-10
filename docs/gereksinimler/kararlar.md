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
**Durum:** Öneri / müşteri onayı bekliyor (DT-002; SYS-050 Onaylı maddeyi değiştirir).
**Bağlam:** KRR-004 SpeedyBee F405 V4 ailesiyle uyumu seçti; F405 LQFP64’te 8 DShot + LED + 6 UART + 3 SPI ancak DMA’sı dikkatle dağıtılırsa sığar (FeroFly V1.0 “motor 3 DMA” revizyonu). Cezeri Altium şeması (Mamba F405 MK2 tersine mühendisliği) müşterinin kendi şeması sayılmıyor (`docs/mimari-fmu.md`).
**Seçenekler:** 1) `SPEEDYBEEF405V4` (BF) + `speedybeef4v4` (AP) pinleri, belgelenmiş farklarla 2) Altium (Mamba) pinleri 3) Sıfırdan kendi ataması 4) GEPRC F405 pinleri.
**Karar:** 1. Farklar yalnız `docs/pin-haritasi.md` §1.4: SPI3’te flash (CS PC14), UART5 TX PC12, `ADC1_DMA_OPT 1`, PC5 = CUR2, baro parçası, VBAT 15:1. HSE 8 MHz.
**Gerekçe:** BF ve AP’de resmî, uçan hedef → hazır yazılımla çalışır (DOG-099), ArduPilot hwdef türevi kolay (SYS-056); 8 motor DMA çakışmasız (analiz, DOG-034); pazar lideriyle aynı pinler uyumluluk iddiasını güçlendirir. GEPRC MCU pinleri farklı, ikisi birlikte tutulamaz (8 pin ESC dizilimi KRR-004 ayrı konu).
**Etki:** SYS-035, 037, 050, 056; DOG-034, -049, -094, -099, -100; fmu şematiği (İP-05), `firmware/` config ve hwdef (İP-07). Boş GPIO kalmıyor (RSK-015).

## KRR-006 — Referans tasarım kullanım kuralı (2026-11-10)
**Durum:** Öneri (ekip kuralı) / müşteri onayı bekliyor; SOR-014 cevabı “açık kaynak” olursa yeniden değerlendirilir.
**Bağlam:** `docs/mimari-fmu.md` §1: açık F405 referansları farklı lisanslarda — CERN-OHL-P (FeroFly), -W (Mini-Air), -S (KURC), CC-BY-SA (Pixhawk), CC-BY-NC-SA (Revolution, Sparky2, Acci); ticari kartlar yalnız GPL-3 config/hwdef. Hukuki görüş değildir.
**Seçenekler:** 1) Hiçbir referanstan dosya kopyalanmaz; yalnız fikir ve yayımlanmış pin atamaları (işlevsel bilgi) kullanılır 2) İzin verici (P/W) kaynaklardan dosya alınır, bildirim korunur 3) Serbest kullanım.
**Karar:** 1. Tasarım veri sayfaları + `guc-ip03` hesapları + kendi `lib/` kütüphanemizle sıfırdan çizilir. Sembol, ayak izi, şema sayfası, yerleşim **kopyalanmaz**. NC lisanslı kaynaklar (CC-BY-NC-SA) **yalnız okunur**; -S ve CC-BY-SA kaynaklardan da dosya alınmaz. İleride P/W kaynaklı bir dosya gerçekten alınırsa önce bu KRR değişir, kaynak + lisans belgeye ve `CHANGELOG.md`’ye yazılır.
**Gerekçe:** Hiçbir lisans yükümlülüğü ürüne geçmez; kapalı/açık yayımlama kararı (SOR-014) serbest kalır; kopyalamanın kazancı küçük (parça seti zaten veri sayfasından). Kendi BF config ve AP hwdef’imiz o depolara girdiği için GPL-3’tür (SYS-050/056), bu ayrı.
**Etki:** Tüm tasarım ajanları (sematik, pcb, gomulu); `dogrulama-kalite` incelemesinde kaynak sorusu. SYS etkisi yok (kural, gereksinim değil).

## KRR-007 — FMU 8S stratejisi (2026-11-10)
**Durum:** Öneri / müşteri onayı bekliyor (SOR-013).
**Bağlam:** M3 8S FMU ister (MUS-012). 8S LiHV dolu 34.8 V; SYS-014 kuralıyla (geçici + 5 V) VIN parçaları mutlak ≥ 45 V. M1 BOM’undaki SY8303 (40 V), AO3401A (−30 V), sigorta (32 V DC), SMBJ24CA 8S’e uymaz (`docs/mimari-fmu.md` §4.4). Onaylı SYS-003 “FMU iki ESC sınıfında değişmeden” diyordu.
**Seçenekler:** 1) M1 BOM 3–6S; PCB 8S BOM varyantına yer bırakır; M3’te yalnız BOM (gerekirse küçük revizyon) 2) M1 baştan 8S dayanıklı, tek BOM (tahmini +1–2 $/kart, `bom-tedarik` doğrulayacak) 3) M3’te ayrı FMU PCB’si.
**Karar (öneri):** 1. **Gerekçe:** M1 maliyeti zaten hedefin üstünde (SOR-016); 5" kullanıcısı 8S dayanımına para ödemez; 8S’in ayak izi riski (60 V buck kılıfı) yerleşim payıyla küçülür, M3 takvimi (2027 Q3) öncesi doğrulanır.
**Etki:** SYS-003, 022, 044, 046; DOG-003, -045, -097, -098; FMU şematik/PCB (İP-05/06), `bom-tedarik` 8S BOM listesi. Seçenek 2 seçilirse SYS-046 İptal, SYS-044’te M1 için ≥ 45 V, SYS-002’ye +1–2 $.
