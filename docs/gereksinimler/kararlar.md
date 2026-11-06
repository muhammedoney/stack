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
