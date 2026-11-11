# Proje gereksinimleri, riskler, iş paketleri

## Proje gereksinimleri (PRJ)

| ID | Gereksinim | Kaynak | Öncelik | Durum |
|---|---|---|---|---|
| PRJ-001 | Tasarım KiCad 10’da; tüm belgeler Türkçe ve repoda; dosya düzeni fiber/gofret projeleriyle aynı | Müşteri, 2026-11-06 | Z | Onaylı |
| PRJ-002 | Hobi ürünü: sertifika (CE/FCC vb.) hedeflenmez | MUS-003 | Z | Onaylı |
| PRJ-003 | Hedef satış fiyatı ≤ 70 $/stack (pazar: bütçe markalar 70–100 $, AliExpress 45–57 $) | SOR-005, `docs/pazar-analizi.md` §6 | Ö | Onaylı |
| PRJ-004 | Stack (FMU + 55 A ESC) toplam maliyeti ≤ 32 $ (DT-004; önceki hedefler: 15 $ → 28 $ DT-001 → 32 $), 100 set kademesinde, tüm özellikler kalır (`docs/bom-maliyet.md` §9.4 Rev B 31.69 $; 2026-11-11 güncel: ESC 17.20 $ + FMU 17.72 $ = 34.92 $ → hedefi 2.9 $ aşıyordu; **2026-11-12, DT-005: §10 A + B (B1–B6) + APM32F405 ≈ 29.97 $ → karşılanıyor**, pay ≈ 2.0 $, RSK-004): komponent + PCB + dizgi dahil, gümrük ve kargo hariç (SOR-009). Her parça seçiminde maliyet etkisi yazılır | SOR-005, SOR-016 | Z | Onaylı (DT-004) |
| PRJ-005 | İlk prototip: en kısa sürede 5 set | SOR-008, 2026-11-06 | Z | Onaylı |
| PRJ-007 | Prototip doğrulandıktan sonra 100 set üretim | SOR-008 | Z | Onaylı |
| PRJ-006 | Yazılım: FMU’da hazır Betaflight, ESC’de Bluejay; yalnız hedef/düzen tanımı ve yükleme yolu bizden | SOR-006, KRR-003 | Z | Onaylı |
| PRJ-008 | Tasarım (şematik, PCB kaynak dosyaları, BOM) şimdilik kapalı; açık yayımlanan belgeler: kullanıcı pin/ped haritası, Betaflight config ve ArduPilot hwdef (GPL-3), kullanıcı kılavuzu (set kondansatörü zorunluluğu ve garanti şartı dahil, SYS-063). 100 set sonrası yeniden değerlendirilir | SOR-014, KRR-009 | Ö | Onaylı |

## Riskler (RSK)

| ID | Risk | Olasılık | Etki | Önlem | Durum |
|---|---|---|---|---|---|
| RSK-001 | esc55a akım ölçümü ≈ 32 A’da doyuyor, shunt 100 A’da ≈ 5 W (inceleme E1, E2) | Yüksek | Akım okuması ve shunt ısısı | Akım sınıfı netleşince yeniden boyutlandırma | Açık |
| RSK-002 | Güç parçalarının (ME7170, JW5026) veri sayfası yok; 55 A sınıfı doğrulanamıyor (E5) | Orta | Yeniden parça seçimi | `bom-tedarik` veri sayfalarını bulur | Açık |
| RSK-003 | esc65a için yalnız fotoğraf var | Yüksek | Takvim | esc55a tabanlı varyant değerlendirmesi (SOR-003) | Açık |
| RSK-004 | ≤ 32 $/stack hedefinde (DT-004) pay çok az: Rev B 31.69 $ (`docs/bom-maliyet.md` §9.4) → pay 0.31 $; DT-003 sıcaklık sınıfı değişiklikleri (STM32F405RGT7, 4 × EFM8BB21 I sınıfı, 125 °C IC muadilleri) fiyatı bilinmeyen artış getirir; bom-maliyet R3 (bulk X5R, −0.49 $) tasarrufu KRR-008 ile kapandı; PCB fiyatı tahmin, Economic dizgi ek ücreti +0.48 $/kart belirsiz (§7)  **2026-11-11:** yeni FMU şematiğiyle stack 34.92 $ (ESC 17.20 + FMU 17.72) > 32 $; FMU’daki eklemeler (40 V BEC’ler, LDO, J_ESC2, X7R) ve ESC 40 V/125 °C yükseltmeleri. **2026-11-12 (DT-005):** müşteri §10 A + B (B1–B6) ve C1 APM32F405RGT6’yı onayladı → ≈ 29.97 $/stack (`docs/bom-maliyet.md` §10.6), pay ≈ 2.0 $. Kalan belirsizlik: A2 geçersiz (küçük kılıf LDO, SYS-042, fark ±0.1 $), B1/B2 incelemeden geçmezse sırayla +2.30 / +0.52 $ (B1 yedeği Tokmas DPS368 ile ≈ 31.3 $), JW5026 muadili (RSK-019), SYS-095 ALT parçaları pahalıysa ALT’la dizilen partide fark, PCB/dizgi gerçek teklif. | Orta (2026-11-12) | Kâr | `bom-tedarik` DT-003 fark maliyeti; güvenli tasarruflar (≈ 30.8 $, SOR-016 notu); JLC gerçek teklifi; aşılırsa yeni DT ile müşteriye (özellik/sınıf ödünleri ayrı satırlarda) | Azaltıldı (2026-11-12) |
| RSK-005 | 100 set ilk parti tasarım doğrulanmadan üretilirse toplu hata riski | Orta | 100 set hurda | Önce 5 set prototip (PRJ-005); Ü-öncesi DOG’lar ve prototip testleri kapanmadan 100 set yok (PRJ-007) | Azaltıldı |
| RSK-006 | FMU tüm beslemesini 8 pin SH konnektörün tek VBAT pininden alıyor: BEC tam yükte 3S’te ≈ 3.1 A (tahmin), SH pin sınıfı ≈ 1 A (tahmin) → pin/kablo ısınması, gerilim düşümü (SYS-062) | Yüksek | Kart/kablo hasarı, FMU sıfırlanması | `sistem-mimari`: pin sayısı, ayrı besleme pedi veya BEC akım hedefinin düşürülmesi; konnektör veri sayfası (`bom-tedarik`) | Açık (2026-11-06) |
| RSK-007 | 4 × 55 A eşzamanlı sürekli + 220 A pil yolu, 41 × 48 mm, iç katman 0.5 oz kartta ısıl olarak tutmayabilir; hava akışı varsayımı (5 m/s) kullanıcı kurulumuna bağlı (SYS-010, SYS-012) | Orta | 55 A iddiası düşer, MOSFET/shunt yanması | DOG-004/008 erken analiz; gerekirse iç katman kalınlığı, MOSFET veya “55 A” tanımının (eşzamanlı kanal sayısı) DT ile güncellenmesi | Açık (2026-11-06) |
| RSK-008 | 6S geçici payı yok: SMDJ28CA ≈ 45 V kıstırma > 35 V bulk; INA199 26 V; FMU TPS54202 28 V; ME7170 V_DS bilinmiyor (E3, E4, E5, F4; SYS-014, SYS-044) | Yüksek | Sahada parça delinmesi | `guc-elektronigi` DOG-009/011/045; TVS ve kondansatör yeniden seçimi; set kondansatörü (SOR-011) | Açık (2026-11-06) |
| RSK-009 | esc55a EFM8BB21 pin ataması hiçbir Bluejay düzenine uymazsa kaynak değişikliği + derleme gerekir; yerelde derleyici yok, PRJ-006 (“yalnız düzen”) aşılır (SYS-051) | Orta | Takvim, yazılım bakımı | `gomulu-yazilim` DOG-051 erken; uymazsa şematikte pin değişimi tercih | Açık (2026-11-06) |
| RSK-010 | SpeedyBee F405 V4 / GEPRC Taker 8 pin dizilimi belgelenemezse veya iki aile farklıysa uyumluluk iddiası tutmaz; yanlış takma kartı bozar (SYS-060) | Orta | Uyumluluk (MUS-006), iade | `sistem-mimari` kılavuz/şema toplama (DOG-059); gerekirse referans kart satın alma (DOG-060) | Açık (2026-11-06) |
| RSK-011 | Kart DOG’ları için tezgâh yok: 4 × 70 A yük, ≥ 100 A akım referansı, ısıl kamera, ESD tabancası (DOG-005, -007, -018, -020, -077) | Orta | Kart doğrulaması eksik kalır | `test-muhendisi` teçhizat listesi ve alternatif (motor + pervane tezgâhı, pil, pens ampermetre); erişilemeyen ölçütler “Kısmen” | Açık (2026-11-06) |
| RSK-012 | FMU şematiğinde 3.3 V regülatörü yok (SYS-042); taşımada eksik besleme fark edilmezse kart çalışmaz | Orta | Prototip hurdası | İP-05’te eklenir, DOG-041 | Açık (2026-11-06) |
| RSK-013 | 100 sette 400 EFM8BB21 C2 ile tek tek yüklenecek; ped/fikstür yoksa süre ve hata (SYS-054) | Düşük | Üretim süresi | C2 pedleri + yaylı pim fikstürü (DOG-055/056) | Açık (2026-11-06) |
| RSK-014 | F405’te 8 kanal çift yönlü DShot + 8 kHz gyro CPU’yu doyurabilir; DMA tablosu yalnız analiz (SYS-037) | Orta | Dual SKU’da RPM filtresi kısıtlı ya da DShot300/PID 4 kHz zorunlu | DOG-094/095 ilk prototipte; sınır ayar kılavuza; gerekirse M5–M8 çift yönlü kapalı (ArduPilot zaten M1–M4) | Açık (2026-11-10) |
| RSK-015 | SpeedyBee V4 uyumlu pin haritası LQFP64’ün 51 G/Ç’sinin tamamını kullanıyor; sonradan özellik (2. LED, ek UART) eklenemez (KRR-005) | Orta | M1 revizyonunda özellik kısıtı | Yeni özellik M4/M5 (LQFP100) ailesinde; gerekirse PB15 (servo) veya PC5 (CUR2) feda edilir, DT ile | Açık (2026-11-10) |
| RSK-016 | (SOR-013 seçenek 1 onaylı, KRR-007) 8S BOM varyantının (60–65 V buck, P-MOS, sigorta) M1 ayak izlerine sığmaması; M1 SY8303 40 V tam 35 + 5 V sınırında (SYS-044, 046) | Orta | M3’te FMU PCB revizyonu, takvim | DOG-097 M1 PCB öncesi; ortak ayak izli aday aranır (`bom-tedarik`, `guc-elektronigi`); SOR-013 | Açık (2026-11-10) |
| RSK-017 | 125 °C (ESC) / 105 °C (FMU) sınıflı parçalar LCSC’de stoksuz, extended veya pahalı olabilir; EFM8BB21 I sınıfı (−40…125 °C) LCSC’de bulunmayabilir; 8 pin JST SH konnektörün katalog sınıfı +85 °C (doğrulanacak) ESC tasarım sıcaklığının (95 °C) altında (SYS-086, SYS-091)  **2026-11-11:** STM32F405RGT6 JLC stoğu da 24 (100 set için dış tedarik gerekir). **2026-11-12:** seri MCU APM32F405RGT6 (stok 1 728 ✓, KRR-010); STM32 ALT olarak kalır.| Orta | Parça değişimi, maliyet (RSK-004), Bluejay hedefi (BB21 → başka MCU olursa SYS-051) | `bom-tedarik` DOG-106/107 erken; I sınıfı yoksa: `sistem-mimari` MCU’yu kartın soğuk bölgesine, ölçülen sıcaklığı sınırın ≥ 15 °C altında tutan yerleşim ya da muadil; konnektör için 105 °C sınıflı SH uyumlu muadil veya kenar yerleşimi + yerel ölçüm | Açık (2026-11-11) |
| RSK-018 | FMU yığında sıcak ESC’nin (≈ 95 °C) üstünde; IMU, baro, OSD çipi gibi 105 °C muadili olmayan 85 °C parçalar ≤ 70 °C ölçütünü aşabilir; IMU sıcaklık kayması gyro gürültüsünü artırır (SYS-087) | Orta | FMU parça ömrü, uçuş kalitesi | `pcb-muhendisi`: 85 °C parçaları BEC/LDO’dan uzak, ESC sıcak bölgesinin üstüne gelmeyecek konumda; DOG-108 yığın ölçümü; kılavuzda yığın aralığı (tampon yüksekliği) önerisi | Açık (2026-11-11) |
| RSK-019 | ESC buck JW5026 (C185109) JLC stoğu 132 (2026-11-11; 11-10’da 4 308): 100 set için 400 adet gerekir, SYS-091 “stok ≥ 2 × ihtiyaç” (800) tutmuyor; ikinci kaynak yok (SYS-095) | Yüksek | ESC 100 set takvimi, yeniden parça seçimi ve maliyet (RSK-004) | `guc-elektronigi`: SYS-013/014/016/086’yı karşılayan (≥ 40 V, ≥ 125 °C) aynı ayak izli muadil çifti seçer (ana + ALT); `bom-tedarik` stok ve fiyat; seçilemezse peşin alım + istisna listesi (SYS-095 e) | Açık (2026-11-12) |
| RSK-020 | APM32F405 seri MCU (KRR-010): (a) ArduPilot’un APM32F405’i resmî desteklediği doğrulanmadı → SYS-056 (ArduPilot hazırlığı) APM32’li kartta karşılanmayabilir; (b) Betaflight’ta APM32F405 ayrı MCU derlemesi olabilir → STM32 ALT ile “aynı yazılım imajı” ölçütü (SYS-095 d) tutmayabilir, kullanıcı yükleme sırasında doğru derlemeyi seçmeli; (c) VCAP/BOOT/USB/HSE farkları | Orta | SYS-056 “Kısmen”, kullanıcı yanlış yazılım yükler, destek yükü | DOG-023 (kaynak kodu araştırması, Ü-öncesi), DOG-112 (kart); `gomulu-yazilim`: BF config’in iki MCU’yu nasıl kapsadığı, AP hwdef/ChibiOS durumu; AP desteği yoksa seçenekler: ArduPilot SKU’sunda STM32F405RGT6 dizilir (aynı PCB, BOM varyantı) veya SYS-056 için DT; sonuç müşteriye (SOR-018) | Açık (2026-11-12) |
| RSK-021 | Muadil kuralı (SYS-095): bazı kritik parçaların pin/ayak izi uyumlu ve aynı yazılımla tanınan muadili yok (EFM8BB21F16I 125 °C — Bluejay yalnız EFM8BB21/BB51; AT7456E — MAX7456/AT7456 stok 0; W25Q128JV — ucuz muadiller ArduPilot’ta yok; INA281B2 SOT-23-5 — INA240 ALT’ı farklı kılıf); muadil eklemek ayak izini büyütebilir veya pahalı ALT getirir | Orta | İstisna listesi uzar, seri üretimde tek kaynak riski kalır; ayak izi büyürse FMU alanı | `bom-tedarik` + `sematik-muhendisi` erken tarama (DOG-110, şematik Rev B öncesi); istisnalar müşteriye gerekçeyle bildirilir; peşin alım önlemi | Açık (2026-11-12) |

## Değişiklik talepleri (DT)

| ID | Talep | Etkilenen | Durum |
|---|---|---|---|
| DT-001 | Maliyet hedefi 15 $ → ≤ 28 $/stack (100 set), tüm özellikler kalır. Gerekçe: bom-maliyet S1 31.9 $, S1b 27.4 $; özellikler kesilse bile 19.5 $ | PRJ-004, RSK-004, İP-02, İP-05 (S1b sadeleştirmeleri `guc-elektronigi`/`gomulu-yazilim` incelemesiyle) | Onaylı (müşteri, 2026-11-06); hedef DT-004 ile ≤ 32 $’a güncellendi (2026-11-11) |
| DT-002 | FMU (M1 F405) gereksinimlerinin hedef ürün ailesine (M3 8S FMU, M4a Dual-ESC, M4/M5 F7/H7, ArduPilot) göre güncellenmesi. Müşteri: “F405 için gereksinimleri hedef ürünü göz önüne alarak yap” (2026-11-10) | SYS-002, 003, 022, 035, 037, 042, 044, 050, 055, 062 (Değişti); SYS-004, 023, 046, 056, 057 (yeni); MUS-010…013; KRR-005…007; DOG-002, -003, -021, -022, -030, -031, -034, -041, -045, -049, -057, -062, -063 (değişti), DOG-091…103 (yeni); RSK-014…016; SOR-013…017; SOR-017 cevabıyla SYS-061, 063 ve DOG-061, -064 değişti, DOG-109 yeni (2026-11-11). Etki analizi aşağıda | Onaylı (müşteri, 2026-11-11; SOR-013, 014, 016, 017 cevaplandı, itiraz yok; SOR-015 açık) |
| DT-003 | Yüksek sıcaklık: kart yüksek sıcaklığa çıkar, bileşenler buna göre seçilir. Müşteri: “Kart yüksek derecelere çıkar. Ona göre komponentleri güncelle.” (2026-11-11) | MUS-014; SYS-083 (Değişti); SYS-085, 086, 087 (yeni, Taslak); KRR-008; DOG-082 (değişti), DOG-104…108 (yeni); RSK-004, 017, 018; BOM (ESC, FMU). Etki analizi aşağıda | İhtiyaç onaylı (müşteri talebi, 2026-11-11); [öneri] değerler `bom-tedarik`/`sistem-mimari` doğrulaması sonrası müşteriye bildirilir |
| DT-004 | Maliyet hedefi ≤ 28 $ → ≤ 32 $/stack (100 set), tüm özellikler kalır; DT-001’i günceller. Gerekçe: SYS-014 uyumlu Rev B ESC + FMU düzeltmeleri 31.69 $ (`docs/bom-maliyet.md` §9.4) | PRJ-004, SYS-002, DOG-002, RSK-004 | Onaylı (müşteri, 2026-11-11, SOR-016) |
| DT-005 | Seri üretim tedarik ve maliyet kararları (müşteri, 2026-11-12): (1) SYS-030 → “STM32F405RG veya pin ve yazılım uyumlu APM32F405RG; seri varsayılan APM32F405RGT6, STM32F405RGT6 drop-in muadil” (KRR-010); (2) yeni MUS-016 / SYS-095 kritik parçalarda drop-in muadil (KRR-011); (3) SYS-042 küçük kılıf notu; (4) `docs/bom-maliyet.md` §10 A1–A7, B1–B6 gereksinim değişmeden kabul, C2–C6 reddedildi | SYS-030 (Değişti), SYS-095 (yeni), SYS-042 (not), SYS-091 (ilişki); MUS-016; KRR-010, KRR-011; DOG-023, -041, -100, -101 (değişti), DOG-110…112 (yeni); RSK-004, 017 (güncellendi), RSK-019…021 (yeni); SOR-018; PRJ-004 durumu. Etki analizi aşağıda | Onaylı (müşteri, 2026-11-12) |

### DT-002 etki analizi (2026-11-10, müşteri onayı 2026-11-11; `gereksinim-muhendisi`; girdi `sistem-mimari` `docs/mimari-fmu.md`, `docs/pin-haritasi.md`)

**Değişen onaylı SYS (10):**

| SYS | Değişiklik (özet) | Neden (km taşı) |
|---|---|---|
| SYS-002 | Maliyet ölçütü PRJ-004’e bağlandı (15 $ metni DT-001 artığıydı); SKU varyant farkları ayrı | Tutarlılık, M4a/M3 varyantları |
| SYS-003 | FMU M1/M3/M4a’da aynı PCB, farklar BOM varyantı | M3, M4a |
| SYS-022 | VBAT aralığı ≥ 45 V | M3 8S |
| SYS-035 | ≥ 6 tam UART + SBUS donanım çevirici | M3 (GPS + pusula), KRR-005 |
| SYS-037 | 8 motor zorunlu, 2. konnektör Dual SKU’da takılı, her çıkış ayrı DMA, CPU yükü ölçütü | M4a (K10) |
| SYS-042 | 3.3 V regülatör açık, IMU ayrı süzgeçli dal | guc-ip03 G9, referans dersleri D4 |
| SYS-044 | VIN parçaları ≥ 40 V (M1), 8S varyantta ≥ 45 V | M3 |
| SYS-050 | `SPEEDYBEEF405V4` uyumlu pin ataması, HSE 8 MHz | KRR-004/005, ArduPilot |
| SYS-055 | SWD SYS-057’ye ayrıldı | ArduPilot önyükleyicisi |
| SYS-062 | Ayrı BAT pedleri zorunlu, J_ESC2 VBAT bağlı değil | guc-ip03 G16/G17, M4a |

**Yeni SYS (5, Taslak):** SYS-004 (M4/M5 dış ölçü/konnektör sürekliliği, İ), SYS-023 (ESC2 akım ölçümü PC5, Ö), SYS-046 (8S BOM varyantı hazırlığı, Ö, SOR-013), SYS-056 (ArduPilot F405 kısıtlı donanım hazırlığı, Ö), SYS-057 (SWD pedleri, Ö). Referans kullanım kuralı SYS değil, KRR-006.

**Değişmeyen ama ilgili:** SYS-001 (M1 stack tanımı; Dual-ESC stack M4a gereksinimlerinde yazılacak), SYS-031/032/033 (ICM-42688-P, tek baro, 16 MB flash ArduPilot’ta da destekli), SYS-060 (8 pin dizilimi İP-10’da), SYS-074 (8S ters kutup −34.8 V SYS-046’da), PRJ-006 (resmî BF/AP kaydı kapsam dışı; hwdef `gomulu-yazilim` ek işi).

**Etkilenen DOG:** değişen 13 (DOG-002, -003, -021, -022, -030, -031, -034, -041, -045, -049, -057, -062, -063), yeni 13 (DOG-091…103; Ü-öncesi 6, Kart 7). Toplam 103.

**Tasarım öğeleri:**

| Öğe | Etki | Sahip / İP |
|---|---|---|
| `boards/fmu/` şematik | Altium’dan taşıma yerine `docs/mimari-fmu.md` §4 mimarisiyle: HSE 8 MHz, flash SPI3, VBAT 15:1 PC0, CUR2 PC5 + SJ1, J_ESC2 (VBAT NC), SBUS çevirici, UART5 TX, SWD pedleri, BAT pedleri U9 öncesi, AMS1117 + IMU süzgeci, SY8303 × 2, U9 yönü (G8) | sematik-muhendisi / İP-05 |
| `boards/fmu/` PCB | 36 × 36 mm, 8S yerleşim payı (VIN ağı), J_ESC2 ve M5–M8 pedleri, SWD/test pedleri, BEC’ler MCU/IMU’dan uzak; konnektör konumları M4/M5 için belgelenir | pcb-muhendisi / İP-06 |
| `firmware/` | BF config (`SPEEDYBEEF405V4` türevi, §1.4 farkları), ArduPilot hwdef (`speedybeef4v4` türevi); derleyicide doğrulanacak | gomulu-yazilim / İP-07 |
| BOM | Standart / Dual SKU / 8S varyant BOM’ları; 8 MHz kristal; 8S aday parçalar | bom-tedarik / İP-02 |
| `test/` | DOG-093, -095, -098, -099, -101, -103 prosedürleri; 8 motor (iki ESC) pervanesiz tezgâh | test-muhendisi / İP-08, İP-11 |

**Maliyet etkisi (100 set, $/kart, S1b FMU’ya göre, tahmin — `bom-tedarik` doğrulayacak; guc-ip03 G7–G10 +0.6 $ DT-002’ye dahil değil):**

| Kalem | Standart SKU | Dual SKU | Not |
|---|---|---|---|
| 24 MHz kristal (0.347 $) → 8 MHz | ≈ −0.25 | ≈ −0.25 | tahmin |
| 2. SM08B (J_ESC2) DNP | ≈ −0.24 | 0 | S1b’de 2 adet vardı |
| 2. ESC kablosu (kutu) | 0 | ≈ +0.2–0.3 | tahmin |
| SBUS çevirici, CUR2 süzgeci + SJ, VBAT %0.5 dirençler | ≈ +0.05 | ≈ +0.05 | |
| SWD, BAT pedleri, 8S yerleşim payı | 0 | 0 | PCB alanı 36 × 36 içinde |
| **Toplam M1** | **≈ −0.45** | **≈ −0.2 + kablo** | |
| SOR-013 seçenek 2 (baştan 8S) | +1–2 | +1–2 | ≤ 32 $ hedefini aşar |

**İP etkisi:** onaylanırsa İP-05/06/07’ye SYS-023, 046, 056, 057 eklenir; İP-01 (pin haritası) KRR-005 ile kapanmaya aday; İP-10 8 pin dizilimi değişmeden açık.

**Karar (2026-11-11):** DT-002 müşteri onaylı. SOR-013 → seçenek 1 (KRR-007 Onaylı, SYS-046 Onaylı); SOR-014 → kapalı tasarım + açık belge (KRR-009, PRJ-008; KRR-006 Onaylı); SOR-016 → ≤ 32 $ (DT-004); SOR-017 → set kondansatörü zorunlu (SYS-061, SYS-063 `Onaylı (DT-002)`, DOG-061/064 değişti, DOG-109 yeni); KRR-005 Onaylı. **Açık:** SOR-015 (pazar analizi; SYS-010/011 değişmez, cevapla yeni DT).

### DT-003 etki analizi (2026-11-11, `gereksinim-muhendisi`; girdi `docs/rapor/guc-ip03.md` §2.5, §6.3, §8.3, G6, G18; `docs/mimari-fmu.md`)

**Gerekçe:** guc-ip03: ESC sınır akımda kart ortalaması ≈ 95–99 °C, MOSFET kılıfı ≈ 110 °C; X5R +85 °C aşılır. FMU kart ≈ 60–90 °C (masa, tahmin), yığında ESC ısısı eklenir; STM32F405RGT6 (85 °C) sınırda. Onaylı SYS-083 (“≥ −20…+85 °C”) kart ısınmasını hesaba katmıyordu.

**Değişen / yeni SYS:**

| SYS | Değişiklik | Durum |
|---|---|---|
| SYS-083 | “Tüm parçalar ≥ 85 °C” → üst sınıf kart ısınmasına göre (ESC SYS-086, FMU SYS-087); alt sınır ≤ −20 °C | Değişti (DT-003) |
| SYS-085 | ESC ısıl zarfı: sıcak nokta (MOSFET kılıfı) ≤ 110 °C, kart ortalaması ≤ 95 °C [öneri], anma akımında ve 50 °C azaltılmış akımda | Taslak (yeni) |
| SYS-086 | ESC parça sınıfı ≥ 125 °C [öneri]; X7R+, kartta elektrolitik/polimer yok, IC ≥ 105 °C (tercih 125), MCU EFM8BB21 I sınıfı | Taslak (yeni) |
| SYS-087 | FMU parça sınıfı ≥ 105 °C [öneri]; X7R+, MCU STM32F405RGT7; 85 °C istisnaları (IMU, baro, OSD…) ≤ 70 °C ölçülür | Taslak (yeni) |

**Değişmeyen ama ilgili:** SYS-010/011 (MOSFET ≤ 110 °C zaten var; anma tanımı SOR-015 açık), SYS-012, SYS-043 (FMU BEC ısısı masa), SYS-030 (RGT7 de Betaflight destekli F405 — aynı kalıp), SYS-050/056 (pin ataması ve yazılım etkilenmez), SYS-051 (EFM8BB21 I sınıfı aynı kalıp; MCU değişirse etkilenir), SYS-063 (set kondansatörü 105 °C sınıfı bu kurala bağlandı), SYS-091 (LCSC stoğu, extended sayısı).

**Etkilenen DOG:** DOG-082 (değişti), DOG-104…108 (yeni; Ü-öncesi 3, Kart 2). DOG-005, -044, -083 ölçümleri DOG-105/108 ile aynı düzenekte yapılır.

**Tasarım öğeleri:**

| Öğe | Etki | Sahip / İP |
|---|---|---|
| ESC BOM / şematik | EFM8BB21F16G → 125 °C sınıfı (I) sipariş kodu; C_boot 1 µF X5R (C52923) → X7R; JSM6288Q1, JW5026, ESC LDO, L00, SH konnektör sınıfı taranır; bulk C89632 X7R kalır (bom-maliyet R3 X5R tasarrufu reddedilir) | bom-tedarik, sematik-muhendisi / İP-02, İP-05 |
| FMU BOM / şematik | STM32F405RGT6 → RGT7; tüm seramikler X7R; SY8303, AMS1117, kristaller (8 MHz, 27 MHz), USB-C, SH konnektörler, LED’ler, flash taranır; 85 °C istisna listesi | bom-tedarik, sematik-muhendisi / İP-02, İP-05 |
| FMU PCB | 85 °C istisna parçaları (IMU, baro, OSD) BEC/LDO’dan ve ESC sıcak bölgesinin üstünden uzak (RSK-018) | pcb-muhendisi / İP-06 |
| ESC PCB | 125 °C bulunamayan parçalar (SH konnektör, gerekirse MCU) kartın soğuk bölgesinde (RSK-017) | pcb-muhendisi / İP-06 |
| `firmware/` | Etki yok (RGT7 ve BB21 I sınıfı aynı kalıp) — `gomulu-yazilim` teyit eder | gomulu-yazilim / İP-07 |
| `test/` | DOG-105 ve DOG-108 prosedürü: ısıl kamera + ısıl çift; ısıl kabin yoksa 25 °C ölçüm + 25 K kaydırma (RSK-011) | test-muhendisi / İP-08, İP-11 |

**Maliyet etkisi:** henüz hesaplanmadı (TBD, `bom-tedarik`): STM32F405RGT7 − RGT6 farkı, 4 × EFM8BB21 I − G farkı, 125 °C IC muadilleri, X7R C_boot (≈ 0). Bütçe ≤ 32 $ (DT-004) içinde pay 0.31 $ → RSK-004. Aşılırsa yeni DT ile müşteriye seçenek sunulur.

**İP etkisi:** İP-02’ye DOG-106/107/109 (BOM sıcaklık sınıfı, set kondansatörü); İP-03’e DOG-104; İP-05/06’ya SYS-086/087 parça ve yerleşim kuralları; İP-08/11’e DOG-105/108.

### DT-005 etki analizi (2026-11-12, `gereksinim-muhendisi`; girdi `docs/bom-maliyet.md` §10)

**Müşteri kararları (özet):** muadil kuralı (“Tasarımda değişiklik yapmadan yerine muadil komponent takabilmek isterim.”); “A ve B uygun.”; AMS1117 SOT-223 karta sığmayabilir; “C’deki APM de uygun, gereksinimi gevşet. APM32F405 kullan.”; “C’deki riskli durumları boşver, güvenli yerde kalalım.”

**Değişen / yeni SYS:**

| SYS | Değişiklik | Durum |
|---|---|---|
| SYS-030 | “Resmî STM32F405” → STM32F405RG veya pin/yazılım uyumlu APM32F405RG; seri APM32F405RGT6, ALT STM32F405RGT6 | Onaylı (DT-005) |
| SYS-095 | Yeni: kritik parçalarda drop-in muadil, ALT MPN/LCSC, ortak ayak izi, aynı yazılım imajı, gerekçeli istisna listesi | Onaylı (yeni) |
| SYS-042 | Not: 3.3 V regülatörü küçük kılıf (SOT-223 değil) [öneri]; ölçütler aynı | Onaylı (DT-002; not DT-005) |

**Gereksinim değişmeden kabul edilen §10 maddeleri (uygulama şartlı):**

| Madde | Şart (inceleme) | İlgili SYS / DOG |
|---|---|---|
| A1, A3–A7 | Yok; `sematik-muhendisi` kodları girer. A7 (Standard dizgi) JLC teklifiyle doğrulanır | SYS-002, 091; DOG-002 |
| A2 (AMS1117 UMW SOT-223) | **Geçersiz:** SYS-042 küçük kılıf notu; `guc-elektronigi` küçük kılıflı LDO + pin uyumlu ALT seçer | SYS-042, 095; DOG-041 |
| B1 SPA06-003 baro | `gomulu-yazilim`: BF `dps310` sürücüsü PROD_ID 0x11, AP `SPL06` (Copter ≥ 4.6.3); ALT Tokmas/Infineon DPS368 aynı imajda tanınmalı (AP hwdef’te iki BARO satırı); `pcb-muhendisi`: LGA-8 ped ölçüsü | SYS-032, 056, 087, 095; DOG-025, -026, -100 |
| B2 INA281B2 | `guc-elektronigi`: SYS-021 tolerans bütçesi (DOG-019), PWM ortak kip; `gomulu-yazilim`: `ibata_scale` 200; SYS-095 için SOT-23-5 pin uyumlu ALT bulunmalı (INA240A3 SOIC-8 drop-in değil) | SYS-020, 021, 086, 095; DOG-017, -019, -106 |
| B3–B6 | `guc-elektronigi`: B3 USB’de 5 V rayı ≈ 4.5 V (AT7456E alt sınır), B4 5 V FB (SYS-040), B5 T_J, B6 PVDD; `pcb-muhendisi` B5 SOD-323 | SYS-034, 036, 040, 016, 086 |

**Reddedilen (C2–C6):** INA186A3 (SYS-021), BMI270 (SYS-031, 8 kHz yok), PUYA flash (SYS-056, AP’de yok), baro çıkar (SYS-032), flash çıkar (SYS-033, 056). İlgili SYS değişmez. Ayrıca C3/C4 parçaları SYS-095 muadili olarak da kullanılmaz (aynı gerekçe).

**Değişmeyen ama ilgili:** SYS-050 (pin ataması aynı; BF config APM32 için ayrı MCU tanımı gerekebilir, RSK-020), SYS-055 (USB DFU, APM32’de DOG-112), SYS-056 (AP; RSK-020), SYS-087 (APM32F405RGT6 −40…85 °C, FMU kuralı ≥ 85 °C ✓ — veri sayfasıyla doğrulanır), SYS-091 (ALT stoğu bilgi amaçlı), SYS-086 (ESC ALT’ları da ≥ 125 °C).

**Tasarım öğeleri:**

| Öğe | Etki | Sahip / İP |
|---|---|---|
| FMU şematik | U201 APM32F405RGT6 ana, STM32F405RGT6 ALT; VCAP/BOOT/HSE farkı varsa iki parçayı karşılayan devre; U103 küçük kılıflı LDO; tüm kritik parçalarda ALT MPN/ALT LCSC alanları; §10.7 A/B değişiklikleri | sematik-muhendisi / İP-05 |
| ESC şematik | U2 INA281B2 + SOT-23-5 ALT; JW5026 yerine/yanına muadil çifti (RSK-019); sürücü, MOSFET, LDO, TVS ALT alanları | sematik-muhendisi, guc-elektronigi / İP-05 |
| PCB | Ortak ayak izleri (iki veri sayfası ped önerisini kapsayan) | pcb-muhendisi / İP-06 |
| BOM | ALT MPN/ALT LCSC sütunları, istisna listesi, ALT stok/fiyat | bom-tedarik / İP-02 |
| `firmware/` | BF config APM32F405 + STM32F405; AP hwdef APM32 durumu; baro iki sürücü; `ibata_scale` | gomulu-yazilim / İP-07 |
| `test/` | DOG-111 (ALT takılı kart), DOG-112 (APM32 BF/AP/DFU) prosedürü; 5 set dizgisinde ALT’lı kart sayısı | test-muhendisi / İP-08, İP-11 |

**Maliyet etkisi:** A + B (B1–B6) + APM32 ≈ 29.97 $/stack (§10.6) ≤ 32 $ (PRJ-004) ✓; A2’nin yerini alan küçük kılıflı LDO farkı ±0.1 $ (TBD, `bom-tedarik`); ALT parçalar yalnız dizilen partide maliyete girer. RSK-004 “Azaltıldı”.

**İP etkisi:** İP-02’ye DOG-110 ve istisna listesi; İP-05’e ALT alanları ve MCU/LDO; İP-07’ye DOG-023 yazılım kısmı, DOG-100; İP-11’e DOG-111, DOG-112.

## İş paketleri (İP)

> 2026-11-06: Kapı 1 onaylandı; paketler açıldı. Parantezde pakette kapanacak DOG. Kart DOG’ları prototip gelince ayrı paket (İP-11).

| ID | Paket | Sahip | SYS | Durum |
|---|---|---|---|---|
| İP-01 | Mimari: `docs/pin-haritasi.md` (8 pin dizilimi KRR-004, FMU MCU pin/zamanlayıcı/DMA, UART), güç/ısı bütçesi (220 A pil yolu, 4 × 55 A, BEC, VBAT pini), geçici gerilim stratejisi, 65 A varyant uyumu | sistem-mimari | SYS-003, 010, 012, 014, 035, 037, 044, 060, 062 (DOG-003, -030, -034, -059, -062) | Açık |
| İP-02 | Tedarik: eksik veri sayfaları (ME7170, JW5026, INA199, AMS1117, SMDJ28CA, SH konnektör — RSK-002), LCSC kodlama, 100 set BOM ve maliyet | bom-tedarik | SYS-002, 083, 091 (DOG-002, -082, -087); veri girdisi SYS-010…016, 062 | Açık |
| İP-03 | Ü-öncesi güç analizleri: kayıp/ısı, akım ölçümü yeniden boyutlandırma, TVS/kondansatör, BEC, BEMF, failsafe donanımı | guc-elektronigi | SYS-010, 011, 013…016, 020, 021, 040…045, 070, 073, 074, 083 (DOG-004, -006, -009, -011, -013, -015, -017, -019, -037, -039, -041, -043, -045, -047, -067, -072, -074, -083) | Açık (İP-02 veri sayfalarına bağlı) |
| İP-04 | KiCad taşıma: esc55a şematik + PCB, fmu şematik; ortak `lib/`, çift referanslar (E6, F2), Altium kuralları (E9, E10) | sematik-muhendisi, pcb-muhendisi | SYS-001, 030, 032, 090 (DOG-001, -023, -026) | Açık |
| İP-05 | Şematik Rev B: akım ölçümü (E1, E2), TVS/kondansatör (E3, E4), FMU 3.3 V regülatörü ve giriş koruması (F4), 8 pin dizilimi, C2/SWD/test pedleri, ESC giriş çekmesi, ters kutup | sematik-muhendisi | SYS-014, 020, 036, 042, 044, 054, 055, 060, 070, 073, 074, 075, 093 | Açık (İP-01, İP-03’e bağlı) |
| İP-06 | PCB: esc55a Rev B yerleşim/yol (pil yolu bakırı), fmu PCB sıfırdan (F1), test noktaları, ipek baskı, JLC kuralları | pcb-muhendisi | SYS-012, 063, 064, 065, 080, 081, 082, 084, 090, 092, 093 (DOG-008, -079, -080, -084, -086, -088) | Açık (İP-05’e bağlı) |
| İP-07 | Yazılım: Betaflight config (HSE 24 MHz, F3), Bluejay düzen eşlemesi (§2.4), failsafe varsayılanları; derleme gereken yer “derleyicide doğrulanacak” | gomulu-yazilim | SYS-031, 050, 051, 052, 053, 055, 071, 072 (DOG-024, -049, -051, -070) | Açık (İP-01’e bağlı) |
| İP-08 | Doğrulama planı: Ü-öncesi hesap betikleri (DOG-021), tezgâh ve pervaneli test prosedürleri, teçhizat listesi (RSK-011), üretim sonu test prosedürü | test-muhendisi | SYS-022, 094 ve tüm Kart DOG’larının prosedürü | Açık |
| İP-09 | Kalite kapısı: her paket sonunda `guc-elektronigi` + `dogrulama-kalite` incelemesi; dogrulama-kalite Ü-öncesi M DOG’ları (DOG-001, -023, -026, -027, -028, -032, -036, -055, -057, -061, -064, -065, -066, -076, -078, -089) | dogrulama-kalite, guc-elektronigi | SYS-001, 030, 032…034, 036, 038, 054, 055, 061, 063…065, 075, 080, 093 | Açık |
| İP-10 | Pazar girdisi: rakip kütle/ölçü/set içeriği, SpeedyBee/GEPRC 8 pin ve DJI dizilim kılavuzlarının toplanması | pazar-analisti | SYS-060, 061, 065, 081, 082 | Açık |
| İP-11 | Prototip (5 set) Kart DOG’ları: 37 madde (DOG-005, -007, -010, …, -090) | test-muhendisi | Tüm SYS (Kart DOG’u olanlar) | Açık (prototip gelince) |
