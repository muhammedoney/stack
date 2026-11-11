# Doğrulama (DOG)

Yöntem: A analiz, S simülasyon, M muayene, G gösterim, T test. Aşama: Ü-öncesi / Kart.
Sonuç: `Bekliyor`, `Geçti`, `Kaldı`, `Kısmen`; kanıt `test/` altındaki rapora bağlanır.

> 2026-11-06: Kapı 1 için ilk plan (`gereksinim-muhendisi`), hepsi `Taslak`. Ü-öncesi 53, Kart 37 (toplam 90). Kart DOG’ları ilk 5 set prototipte (PRJ-005); 100 set (PRJ-007) Ü-öncesi DOG’lar ve Z öncelikli Kart DOG’ları kapanmadan başlamaz (RSK-005). Pervaneli/motorlu testler yalnız `test-muhendisi` prosedürüyle (CLAUDE.md). “derleyicide doğrulanacak” = derleme gerektirir, yerelde derleyici yok.

> **DT-002 (2026-11-10; müşteri onayı 2026-11-11):** `[DT-002]` işaretli maddeler değişti veya yeni. Değişen: DOG-002, -003, -021, -022, -030, -031, -034, -041, -045, -049, -057, -062, -063. Yeni: DOG-091…103 (Ü-öncesi 6, Kart 7). Toplam 103: Ü-öncesi 59, Kart 44. DOG-098 M3 8S kartında yapılır.

> **2026-11-11 (DT-002 onayı, DT-003, DT-004):** `[DT-003]` işaretli maddeler değişti veya yeni. Değişen: DOG-002 (≤ 32 $, DT-004), DOG-061 ve DOG-064 (SOR-017 set kondansatörü), DOG-082 (sıcaklık sınıfı). Yeni: DOG-104…109 (Ü-öncesi 4, Kart 2). Toplam 109: Ü-öncesi 63, Kart 46.

| ID | Doğrulanan SYS | Yöntem | Prosedür / ölçüt | Aşama | Sorumlu | Sonuç | Kanıt |
|---|---|---|---|---|---|---|---|
| DOG-001 | SYS-001 | M | Şematik/PCB: bir FMU + bir 4 kanallı ESC, ikisinde 30.5 × 30.5 mm desen, 3–6S giriş | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-002 | SYS-002 | A | **[DT-002]** 100 set BOM (LCSC fiyatı) + JLC PCB (4 katman, 2 oz dış) + dizgi (kurulum, extended ücreti, set başına) ≤ PRJ-004 hedefi (32.00 $, DT-004); DT-003 sıcaklık sınıfı parça farkları ayrı satırda; her satırda SYS/KRR bağı; Dual-ESC ve 8S BOM varyant farkları ayrı satırda | Ü-öncesi | bom-tedarik | Bekliyor | |
| DOG-003 | SYS-003 | A | **[DT-002]** M2 (65 A 3–6S) ve M3 (8S) ESC varyantları için değişen parça listesi; montaj, konnektör, dizilim değişmiyor; FMU’nun M1/M3/M4a’da aynı PCB olduğu (fark yalnız BOM; kaçınılmaz ayak izi farkı listelenir) | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-004 | SYS-010 | A | Kanal başına kayıp (iletim I²R_DS(on) @ T_j, anahtarlama, ölü zaman) + ölçüm elemanı + bakır; ısıl direnç modeli 5 m/s hava akışıyla; 4 × 55 A kararlı hâlde MOSFET kılıfı ≤ 110 °C, her parça sınırın ≥ 15 °C altında | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-005 | SYS-010, SYS-012 | T | Tezgâh: 6S kaynak, 4 kanal × 55 A (motor + yük veya elektronik yük), fanla 5 m/s, 25 ± 3 °C; 10 dk sonra ısıl kamera: MOSFET ≤ 110 °C, pil pedi/ölçüm elemanı/bakır sınır içinde; hasar yok | Kart | test-muhendisi | Bekliyor | |
| DOG-006 | SYS-011 | A | Isıl geçici (Zth) hesabı: 25 °C’den 4 × 70 A 10 s, ardından 55 A; T_j tepe sınırın ≥ 15 °C altında | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-007 | SYS-011 | T | DOG-005 düzeneğinde 4 × 70 A 10 s, 60 s arayla 3 tekrar; MOSFET ≤ 110 °C, hasar/desenkron yok | Kart | test-muhendisi | Bekliyor | |
| DOG-008 | SYS-012 | A | Pil yolu: ped, bakır kesiti (katman başına kalınlık), via sayısı, ölçüm elemanı gücü 220 A sürekli / 280 A 10 s; her elemanın gücü sınıfının ≤ %70’i, bakır sıcaklık artışı ≤ 40 °C (IPC-2152) | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-009 | SYS-013 | M + A | BAT hattındaki her parçanın (MOSFET V_DS, sürücü, buck, akım yükselteci V_CM, kondansatör) çalışma sınırı ≥ 26.1 V; 8.4 V’ta buck/LDO çıkışı ve MCU besleme | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-010 | SYS-013 | T | Ayarlı kaynakla 8.4, 9.0, 16.8, 25.2, 26.1 V’ta 4 motor %0–100 gaz taraması; sıfırlanma ve desenkron yok | Kart | test-muhendisi | Bekliyor | |
| DOG-011 | SYS-014 | A + S | Fren/gaz kesme geçicisi (motor endüktansı, kablo 15 cm, set kondansatörü ESR) hesabı veya devre simülasyonu; TVS kıstırması ≤ 35 V; tüm BAT parçalarının mutlak sınırı ≥ tepe + 5 V | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-012 | SYS-014, SYS-044 | T | 6S pil, set kondansatörü takılı, 4 motor tam gazdan ani sıfıra (pervanesiz ve prosedürlü pervaneli); BAT tepe ≤ 35 V (osiloskop, ≥ 100 MHz, kısa toprak) | Kart | test-muhendisi | Bekliyor | |
| DOG-013 | SYS-015 | A | BEMF bölücü ve nötr ağı 8.4–26.1 V aralığında mux girişi ≤ 3.3 V ve sıfır geçiş algılama payı; E6 dirençlerinin anlamı çözülmüş | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-014 | SYS-015 | T | 2207 1750–1960 KV motor 6S’te, 2207 ≥ 2400 KV 4S’te; %0–100 gaz basamakları ve hızlı geçişler (100 ms), desenkron/titreme yok | Kart | test-muhendisi | Bekliyor | |
| DOG-015 | SYS-016 | A | PVDD (buck geri besleme, veri sayfası V_FB) ve 3.3 V hesabı 8.4–26.1 V’ta; FD6288Q VCC UVLO payı ≥ 1 V; LDO kaybı | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-016 | SYS-016 | T | 8.4 V ve 26.1 V’ta tam gazda PVDD ve 3.3 V test noktalarından ölçüm, sınır içinde | Kart | test-muhendisi | Bekliyor | |
| DOG-017 | SYS-020 | A | Ölçüm elemanı × kazanç → tam ölçek ≥ 280 A; yükseltecin V_CM ve çıkış sınırı; CUR ≤ 3.3 V her koşulda (kazanç toleransı + ofset) | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-018 | SYS-020 | T | Elektronik yük/akım kaynağıyla 0–≥ 100 A (tezgâh sınırı) basamaklar + 4 × 70 A darbede doyma kontrolü; CUR ≤ 3.3 V | Kart | test-muhendisi | Bekliyor | |
| DOG-019 | SYS-021 | A | Tolerans bütçesi (eleman toleransı, sıcaklık katsayısı −10…+50 °C, yükselteç ofseti, ADC çözünürlüğü): 10–200 A’da ±%5, < 10 A’da ±1 A | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-020 | SYS-021 | T | 5 kartta tip ölçekle 5, 10, 30, 60, 100 A noktaları; referans şönt/pens ampermetre ile ±%5 / ±1 A; Betaflight mAh ile pil şarj cihazı mAh farkı ≤ %10 | Kart | test-muhendisi | Bekliyor | |
| DOG-021 | SYS-022 | A | **[DT-002]** Gerçek bölücü oranı, direnç toleransı (%0.5), ADC referansı (VREFINT telafili): tam ölçek ≥ 45 V; 9–26.1 V’ta (8S varyantta 9–34.8 V) ±%1 ±0.1 V; 40 V geçicide ADC pini ≤ VDDA + 0.3 V | Ü-öncesi | test-muhendisi | Bekliyor | |
| DOG-022 | SYS-022 | T | **[DT-002]** Ayarlı kaynak 9.0, 16.8, 25.2 V (8S BOM’lu kartta ayrıca 33.6 V); Betaflight okuması ±%1 ±0.1 V | Kart | test-muhendisi | Bekliyor | |
| DOG-023 | SYS-030 | M | MCU parça numarası Betaflight destekli F405 (STM32F405RGT6) | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-024 | SYS-031 | M | IMU SPI ve INT bağlantısı, Betaflight sürücüsü var, SPI hızı ve 8 kHz için pin/DMA uygun | Ü-öncesi | gomulu-yazilim | Bekliyor | |
| DOG-025 | SYS-031, SYS-032, SYS-033 | G | Betaflight Configurator: gyro 8 kHz, ivmeölçer, baro, flash (boyut ≥ 8 MB) algılanır; blackbox 60 s kayıt okunur | Kart | test-muhendisi | Bekliyor | |
| DOG-026 | SYS-032 | M | Tek baro parçası, Betaflight sürücüsü var, I2C/SPI adresi config ile uyumlu | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-027 | SYS-033 | M | Flash ≥ 8 MB, Betaflight destekli, SPI bağlantısı | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-028 | SYS-034 | M | OSD çipi, 27 MHz, CVBS 75 Ω giriş/çıkış, SPI bağlantısı | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-029 | SYS-034 | T | NTSC ve PAL kamerayla OSD yazısı monitörde görünür, görüntü genliği 75 Ω’da 1 Vpp ±%10 | Kart | test-muhendisi | Bekliyor | |
| DOG-030 | SYS-035 | M | **[DT-002]** Pin haritasında ≥ 6 tam UART (TX + RX) ve 1 I2C pede/konnektöre çıkıyor, USB ve motor zamanlayıcılarıyla çakışmıyor; SBUS pedi → donanım ters çevirici → UART RX yolu şematikte | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-031 | SYS-035 | G | **[DT-002]** 6 UART’ın her birinde Betaflight’ta seri RX (CRSF) veya MSP ile çift yönlü haberleşme; SBUS pedine SBUS alıcıyla kanal verisi gelir | Kart | test-muhendisi | Bekliyor | |
| DOG-032 | SYS-036 | M | USB-C CC 5.1 kΩ × 2, D± ESD, VBUS → 5 V hattı tek yönlü (geri besleme yok), 9 V USB’den beslenmiyor | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-033 | SYS-036 | T | C–C ve A–C kabloyla: pil yokken Configurator bağlanır, DFU’ya girer; pil takılıyken VBUS’a geri akım ≤ 1 mA | Kart | test-muhendisi | Bekliyor | |
| DOG-034 | SYS-037 | A | **[DT-002]** Zamanlayıcı/DMA tablosu (`docs/pin-haritasi.md` §1.2–1.3): M1–M8 her biri ayrı DMA akışında, DShot600 + çift yönlü DShot (giriş yakalama); SPI1 (gyro), ADC1, LED şerit DMA’larıyla çakışma yok; DMA’sız kalan birimler (SPI2 OSD, SPI3 flash) listelenmiş | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-035 | SYS-037 | T | Osiloskop: 8 çıkışta DShot600 bit süresi 1.67 µs ±%5; çift yönlü DShot’ta ESC yanıtı yakalanır | Kart | test-muhendisi | Bekliyor | |
| DOG-036 | SYS-038 | M | LED şerit çıkışı (zamanlayıcılı pin), buzzer sürücüsü, durum LED’i şematikte ve config’te | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-037 | SYS-040 | A | 5 V BEC: geri besleme toleransı ±%5 içinde, 2 A’da bobin doyması, kayıp, 8.4–26.1 V giriş | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-038 | SYS-040 | T | 0, 1, 2 A yükte 9.0 ve 25.2 V girişte 4.75–5.25 V, dalgalanma ölçülür | Kart | test-muhendisi | Bekliyor | |
| DOG-039 | SYS-041 | A | 9 V BEC: ±%5, 1.5 A’da kayıp ve bobin; 3S’te düşme ≤ 1.5 V | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-040 | SYS-041 | T | 0, 0.75, 1.5 A yükte 14.8 ve 25.2 V girişte 8.55–9.45 V; 9.0 V girişte (3S) ≥ 7.5 V (VIN − 1.5 V) | Kart | test-muhendisi | Bekliyor | |
| DOG-041 | SYS-042 | M + A | **[DT-002]** 3.3 V regülatörü kart üstünde; yük toplamı (veri sayfası tepe) + 100 mA ≤ regülatör akım sınıfının %80’i, kayıp ısıl sınırın %80’i; IMU besleme dalı ayrı süzgeçli ve hesapla ≤ 10 mVpp; VDDA süzgeci var | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-042 | SYS-042 | T | Tam yükte 3.3 V ±%3; IMU besleme pininde dalgalanma ≤ 10 mVpp (motorlar dönerken) | Kart | test-muhendisi | Bekliyor | |
| DOG-043 | SYS-043 | A | BEC kayıpları + ısıl direnç (bakır alanı), 25 °C hava akışsız, T_j sınırın ≥ 15 °C altında | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-044 | SYS-043 | T | 6S, 5 V 2 A + 9 V 1.5 A, 10 dk, ısıl kamera; parçalar sınırın ≥ 15 °C altında | Kart | test-muhendisi | Bekliyor | |
| DOG-045 | SYS-044 | M + A | **[DT-002]** M1 BOM: FMU VIN’e bağlı her parçanın mutlak sınırı ≥ 40 V (35 V + 5 V); giriş TVS’i 35 V’ta kıstırır. 8S varyantı DOG-097 | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-046 | SYS-044 | T | FMU girişine 26.1 V sürekli ve 35 V darbe (ESC üzerinden, DOG-012 düzeneği); hasar ve sıfırlanma yok | Kart | test-muhendisi | Bekliyor | |
| DOG-047 | SYS-045 | M | BEC çipi veri sayfası: akım sınırı ve hiccup/otomatik dönüş var | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-048 | SYS-045 | T | 5 V ve 9 V çıkışı 10 s kısa devre; kalkınca çıkış döner, hasar yok | Kart | test-muhendisi | Bekliyor | |
| DOG-049 | SYS-050 | M | **[DT-002]** Üçlü muayene: `docs/pin-haritasi.md` ↔ şematik netlist ↔ Betaflight config (ve ArduPilot hwdef, DOG-100): her MCU pininin işlevi, zamanlayıcısı, DMA seçeneği, HSE 8 MHz, ADC ölçekleri aynı; `SPEEDYBEEF405V4`’ten farklar yalnız §1.4 listesi; derleme derleyicide doğrulanacak | Ü-öncesi | dogrulama-kalite (+ gomulu-yazilim) | Bekliyor | |
| DOG-050 | SYS-050 | G | Resmî Betaflight F405 yazılımı + config yüklenir; tüm donanım (gyro, baro, flash, OSD, UART, motor) Configurator’da görünür | Kart | test-muhendisi | Bekliyor | |
| DOG-051 | SYS-051 | M | EFM8BB21 pin ataması (sinyal, köprü, mux, nötr) Bluejay düzen tablosundaki bir düzenle birebir aynı; düzen kodu yazılır | Ü-öncesi | gomulu-yazilim | Bekliyor | |
| DOG-052 | SYS-051 | G | Resmî Bluejay (o düzen) 4 MCU’ya yüklenir; 4 motor doğru yönde döner, açılış sesi gelir | Kart | test-muhendisi | Bekliyor | |
| DOG-053 | SYS-052 | T | Betaflight motorlar sekmesi: 4 kanal RPM okunur; %0–100 taramada DShot telemetri hata oranı ≤ %1; RPM filtresi etkin | Kart | test-muhendisi | Bekliyor | |
| DOG-054 | SYS-053 | G | FMU USB’den ESC Configurator passthrough: 4 ESC okunur, ayar yazılır, Bluejay güncellenir | Kart | test-muhendisi | Bekliyor | |
| DOG-055 | SYS-054 | M | PCB: 4 × (C2CK, C2D) + 3.3 V + GND pedleri Ø ≥ 1.0 mm, aralık ≥ 2.54 mm, tek yüzden erişilebilir | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-056 | SYS-054 | G | Fikstürle 4 MCU’ya Bluejay önyükleyicisi + yazılım yükleme, kart başına süre ölçülür (hedef ≤ 2 dk [öneri]) | Kart | test-muhendisi | Bekliyor | |
| DOG-057 | SYS-055 | M | **[DT-002]** BOOT0 düğmesi, USB D± doğru pinlerde (PA11/PA12). SWD → DOG-102 | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-058 | SYS-055 | G | BOOT basılı açılışta DFU görünür, Betaflight yüklenir | Kart | test-muhendisi | Bekliyor | |
| DOG-059 | SYS-060 | M | SpeedyBee F405 V4 ve GEPRC Taker kılavuz/şemalarından 8 pin dizilimi; bizim ESC J0 ve FMU konnektörüyle pin pin aynı; `docs/pin-haritasi.md` | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-060 | SYS-060 | T | Düz kabloyla: bizim FMU + SpeedyBee F405 V4 ESC ve SpeedyBee F405 V4 FC + bizim ESC; 4 motor, akım ve VBAT okuması doğru (referans kartlar satın alınırsa [öneri]) | Kart | test-muhendisi | Bekliyor | |
| DOG-061 | SYS-061 | M | **[DT-003]** Set kablo çizimi 1:1, uzunluk ≈ 35 mm, konnektör SH 1.0 mm; set (kutu) içerik listesinde her sette 1 silindirik pil kondansatörü (SYS-063 parça numarası), 8 pin kablo, M3 tampon/vida seti; ambalaj/sevk talimatında “kondansatörsüz sevk yok” | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-062 | SYS-062 | A + M | **[DT-002]** BAT+/− pedleri ters kutup elemanı ve sigortadan önce, ped ölçüsü ≥ 22 AWG, tam yük akımı (çıkış gücü / verim, 8.4 V) bu yolda; konnektör VBAT’tan izinli yük = 0.8 × pin akım sınıfı (veri sayfası) × V_giriş, kılavuz metniyle aynı; J_ESC2 VBAT bağlantısız | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-063 | SYS-062 | T | **[DT-002]** (a) BAT pedlerinden 8.4 V, BEC tam yük, 10 dk: ped, kablo ve ters kutup elemanında sıcaklık artışı ≤ 30 °C; (b) yalnız konnektörden, kılavuzdaki izinli yükte 10 dk: pin sıcaklık artışı ≤ 30 °C | Kart | test-muhendisi | Bekliyor | |
| DOG-064 | SYS-063 | M | **[DT-003]** Pil pedi ölçüsü 12 AWG için yeterli, + / − ipek baskı, kondansatör bacakları için ped/yer; ESC ipek baskısında “kondansatörsüz kullanmayın” uyarısı okunaklı (yükseklik ≥ 0.8 mm [öneri]) | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-065 | SYS-064 | M | Kanal başına 3 ped 18 AWG için yeterli; M1–M4 ipek baskı ve Betaflight motor sırasıyla eşleşme | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-066 | SYS-065 | M | Alıcı, GPS, DJI 6 pin konnektör dizilimleri ilgili cihaz belgeleriyle aynı; 9 V yalnız DJI/VTX pininde | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-067 | SYS-070 | M | Şematik: her köprü kapısının MCU sıfırlama/boşta hâlinde kapalı kaldığı (aşağı çekme, sürücü giriş varsayılanı) | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-068 | SYS-070 | T | Pervanesiz, 20 kez pil takma: arm yokken faz akımı yok (akım pensi), motor dönmez; C2 yükleme sırasında faz akımı yok | Kart | test-muhendisi | Bekliyor | |
| DOG-069 | SYS-071 | T | Pervanesiz %30 gazda FMU↔ESC sinyali kesilir; faz akımı ≤ 500 ms içinde sıfır; sinyal dönünce sıfır gaz + arm olmadan dönmez | Kart | test-muhendisi | Bekliyor | |
| DOG-070 | SYS-072 | M | Config dosyasında failsafe: RX kaybı ≥ 1 s → aşama 2 “drop” (motor durur) | Ü-öncesi | gomulu-yazilim | Bekliyor | |
| DOG-071 | SYS-072 | G | Pervanesiz arm’lı, %30 gaz; kumanda kapatılır, ≤ 1.5 s’de motorlar durur | Kart | test-muhendisi | Bekliyor | |
| DOG-072 | SYS-073 | M | ESC sinyal girişinde tanımlı seviye (çekme direnci veya MCU iç çekmesi + Bluejay giriş ayarı) | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-073 | SYS-073 | T | Kablo çıkarılmış ESC 6S’e takılı, 10 dk, 30 cm yakında çalışan motor/VTX gürültüsü; motor dönmez | Kart | test-muhendisi | Bekliyor | |
| DOG-074 | SYS-074 | M | FMU ters kutup elemanı V_DS/V_GS sınıfı ≥ 26.1 V + pay; ESC: koruma yok, + / − ipek baskı ve kutu uyarısı var mı (SOR-010) | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-075 | SYS-074 | T | FMU VBAT’a −26.1 V, 10 s (akım sınırlı kaynak); sonra normal çalışma | Kart | test-muhendisi | Bekliyor | |
| DOG-076 | SYS-075 | M | USB ve dış pedlerde ESD elemanı / seri direnç; ESD akım yolu kısa | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-077 | SYS-075 | T | ESD tabancasıyla (erişilebilirse) USB ±4 kV temas / ±8 kV hava, diğer pedler ±2 kV temas, 10 darbe; işlev bozulmaz | Kart | test-muhendisi | Bekliyor | |
| DOG-078 | SYS-080 | M | PCB: delik merkezleri 30.5 × 30.5 mm ±0.1 mm; delik çapı M3 tampon ölçüsüyle uyumlu; delik çevresinde parça/yol açıklığı | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-079 | SYS-081 | M | PCB ve 3B model: dış ölçü ve parça yüksekliği sınırlar içinde | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-080 | SYS-082 | A | PCB alan × kalınlık + BOM parça kütleleri: FMU ≤ 8 g, ESC ≤ 14 g (tahmin) | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-081 | SYS-082 | T | 5 set tartılır (0.1 g terazi) | Kart | test-muhendisi | Bekliyor | |
| DOG-082 | SYS-083 | M | **[DT-003]** BOM: her parçanın çalışma sıcaklığı alt sınırı ≤ −20 °C; üst sınır ESC’de DOG-106, FMU’da DOG-107 ile; depolama −20…+70 °C her parçanın depolama sınıfı içinde | Ü-öncesi | bom-tedarik | Bekliyor | |
| DOG-083 | SYS-083 | A | DOG-004 modeliyle 50 °C ortamda izin verilen sürekli akım (azaltma değeri) hesaplanır ve belgelenir | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-084 | SYS-084 | M | ≥ 1 g parçalar (bobin, konnektör) yerleşimi ve sabitleme; konnektörlerde mekanik tutma pedi | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-085 | SYS-084 | T | Titreşim tezgâhı yoksa: 5" çerçevede 10 uçuş × 4 dk (prosedürlü), sonra lehim/konnektör muayenesi ve gyro gürültüsü blackbox’ta | Kart | test-muhendisi | Bekliyor | |
| DOG-086 | SYS-090 | M | DRC JLC 4 katman standart kural dosyasıyla 0 hata; katman yığını ve bakır kalınlığı JLC seçeneklerinde | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-087 | SYS-091 | M | BOM: her satırda LCSC kodu, stok ≥ 2 × 100 set ihtiyacı, extended çeşidi kart başına ≤ 10, el lehimi parça yok | Ü-öncesi | bom-tedarik | Bekliyor | |
| DOG-088 | SYS-092 | M | Yerleşim: dizgi yüz sayısı; çift yüzse maliyet farkı DOG-002’de | Ü-öncesi | pcb-muhendisi | Bekliyor | |
| DOG-089 | SYS-093 | M | PCB: test noktası listesi tam, Ø ≥ 1.0 mm, tek yüzden erişilebilir, adları ipek baskıda | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-090 | SYS-094 | G | 5 sette üretim sonu test prosedürü uygulanır; kart başına süre ≤ 5 dk, hata yakalama listesi | Kart | test-muhendisi | Bekliyor | |
| DOG-091 | SYS-004 | M | **[DT-002]** M1 FMU mekanik çizimi (dış ölçü, delikler, ESC ve çevre konnektörlerinin konumu, yönü, dizilimi) belgelenmiş ve M4/M5 mimari girdisine bağlanmış; sürekliliği bozan öğe yok | Ü-öncesi | sistem-mimari | Bekliyor | |
| DOG-092 | SYS-023 | M | **[DT-002]** J_ESC2.CUR → seri direnç + kondansatör süzgeci → ayrı ADC kanalı (PC5); 3.3 V üstüne karşı koruma (enjeksiyon ≤ 1 mA); toplam/ortalama lehim köprüsü varsayılan açık, ölçek notu config’te | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-093 | SYS-023 | T | **[DT-002]** CUR2 pinine 0.3, 1.5, 3.0 V: ArduPilot BATT2 ve Betaflight ADC okuması ±%2 [öneri]; köprü kapalıyken PC1 = (CUR1 + CUR2)/2 ±%2; Dual SKU’da iki ESC’yle (pervanesiz) iki akım okunur | Kart | test-muhendisi | Bekliyor | |
| DOG-094 | SYS-037 | G | **[DT-002]** Betaflight (kendi config) kartta: `timer show`, `dma show`, `resource show` çıktısında M1–M8, LED şerit, SPI1, ADC1 için çakışma veya “DMA yok” uyarısı yok; çıktı DOG-034 tablosuyla aynı | Kart | gomulu-yazilim | Bekliyor | |
| DOG-095 | SYS-037 | T | **[DT-002]** 8 motor (iki ESC, pervanesiz), çift yönlü DShot300 ve DShot600, gyro 8 kHz, PID 4 ve 8 kHz: Betaflight `tasks`/`status` CPU yükü ≤ %75 [öneri], döngü süresi sapması yok, 8 kanalda RPM okunur, telemetri hata ≤ %1; çalışan en yüksek ayar kılavuza yazılır | Kart | test-muhendisi | Bekliyor | |
| DOG-096 | SYS-037 | M | **[DT-002]** BOM/şematik varyantları: standart SKU’da J_ESC2 DNP, M5–M8 ve CUR2 pedleri erişilebilir ve ipek baskıda; Dual SKU BOM’unda J_ESC2 takılı + kutuda 2. kablo; iki konnektör aynı dizilim (SYS-060) | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-097 | SYS-046, SYS-044 | M + A | **[DT-002]** 8S BOM varyant listesi: VIN’e bağlı her parçanın mutlak sınırı ≥ 45 V (buck, P-MOS V_DS/V_GS, sigorta DC sınıfı, kondansatör), TVS kıstırması ≤ buck mutlak sınırı; her 8S parçası M1 ayak izine/alanına uyar (uymayan listelenir); VIN ağı yol aralığı ≥ 0.2 mm; 34.8 V girişte BEC ısısı; fark maliyeti | Ü-öncesi | guc-elektronigi (+ bom-tedarik) | Bekliyor | |
| DOG-098 | SYS-046 | T | **[DT-002]** 8S BOM’lu kartta (M3): 34.8 V sürekli, 40 V darbe, −34.8 V ters 10 s; BEC çıkışları SYS-040/041 sınırında; hasar ve sıfırlanma yok | Kart (M3) | test-muhendisi | Bekliyor | |
| DOG-099 | SYS-050 | G | **[DT-002]** Değiştirilmemiş resmî Betaflight `SPEEDYBEEF405V4` yazılımı kartta: M1–M4, IMU, OSD, UART’lar, VBAT ve akım çalışır (blackbox ve UART5 TX hariç, `docs/pin-haritasi.md` §1.4) — uyumluluk kanıtı | Kart | test-muhendisi | Bekliyor | |
| DOG-100 | SYS-056 | M | **[DT-002]** Kendi ArduPilot hwdef’i (`speedybeef4v4` türevi) ↔ pin haritası ↔ şematik: HSE 8 MHz, dataflash SPI3 CS PC14, baro I2C1, dış I2C, UART’lar, BATT/BATT2, DShot grupları, 1 MB kısıtlı yapı; derleme derleyicide doğrulanacak | Ü-öncesi | gomulu-yazilim | Bekliyor | |
| DOG-101 | SYS-056 | G | **[DT-002]** ArduPilot Copter (kendi hwdef’le) SWD/DFU ile yüklenir; yer istasyonunda IMU, baro, dataflash günlüğü (60 s kayıt indirilir), GPS + pusula (I2C), 4 motor DShot testi (pervanesiz), VBAT/akım okunur | Kart | test-muhendisi | Bekliyor | |
| DOG-102 | SYS-057 | M | **[DT-002]** PCB: SWDIO (PA13), SWCLK (PA14), NRST, GND, 3.3 V pedleri Ø ≥ 1.0 mm, tek yüzden erişilebilir, ipek baskıda adlı | Ü-öncesi | dogrulama-kalite | Bekliyor | |
| DOG-103 | SYS-057 | G | **[DT-002]** SWD programlayıcıyla (ST-LINK) bağlanılır; flash silinir, yazılır, okunur; BOOT düğmesine dokunmadan önyükleyici yüklenir | Kart | test-muhendisi | Bekliyor | |
| DOG-104 | SYS-085 | A | **[DT-003]** guc-ip03 §2.5 ısıl modeliyle (R_kart-hava 2.0 K/W esas, 4.9 K/W kötü durum ayrıca): anma akımında (SOR-015 tanımı) 25 °C + 5 m/s ve 50 °C ortamda azaltılmış akımda MOSFET kılıfı ≤ 110 °C, kart ortalaması ≤ 95 °C; 50 °C azaltma değeri DOG-083 ile aynı | Ü-öncesi | guc-elektronigi | Bekliyor | |
| DOG-105 | SYS-085, SYS-086 | T | **[DT-003]** DOG-005 düzeneği (6S, anma akımı, fanla 5 m/s, 25 ± 3 °C), 10 dk ısıl kararlı hâl sonrası ısıl kamera (ε ayarlı, kalibre nokta için ısıl çift): en sıcak nokta ≤ 110 °C, kart ortalaması ≤ 95 °C; DOG-106 listesindeki her parçanın (MCU, sürücü, akım yükselteci, buck, LDO, konnektör, kondansatörler) ölçülen kılıf sıcaklığı kendi sınırının ≥ 15 °C altında, 105 °C sınıflı IC’ler ≤ 90 °C; 50 °C değerleri ölçüm + 25 K kaydırma ile (ısıl kabin varsa ölçümle) | Kart | test-muhendisi | Bekliyor | |
| DOG-106 | SYS-086 | M | **[DT-003]** ESC BOM sıcaklık sınıfı muayenesi (her satır, veri sayfası sayfa numarasıyla): üst sınır ≥ 125 °C; seramikler X7R veya üstü (X5R/X6S/Y5V yok); kartta elektrolitik/polimer/tantal yok; MOSFET/diyot/TVS T_j,maks ≥ 150 °C; IC’ler 125 °C (105 °C ise gerekçe + DOG-105 ölçütü); EFM8BB21 sipariş kodu 125 °C sınıfı (I); istisna listesi (ör. SH konnektör) gerekçeli | Ü-öncesi | bom-tedarik (+ dogrulama-kalite) | Bekliyor | |
| DOG-107 | SYS-087 | M | **[DT-003]** FMU BOM sıcaklık sınıfı muayenesi: üst sınır ≥ 105 °C; seramikler X7R veya üstü; MCU STM32F405RGT7; 85 °C istisnaları (IMU, baro, OSD, flash, konnektör, kristal vb.) için “105 °C muadili yok” kanıtı (LCSC/üretici araması) ve yerleşimde ısı kaynaklarına uzaklık (PCB muayenesi, `pcb-muhendisi`) | Ü-öncesi | bom-tedarik (+ dogrulama-kalite) | Bekliyor | |
| DOG-108 | SYS-087 | T | **[DT-003]** Yığın (FMU, ESC’nin üstünde, standart tampon/aralıkla) ESC DOG-105 koşulunda + FMU 5 V 2 A ve 9 V 1.5 A yük, 25 ± 3 °C, 10 dk; ısıl kamera (üst yüz) + ısıl çift (IMU, MCU): 85 °C istisna parçaları ≤ 70 °C, diğer parçalar sınırının ≥ 15 °C altında; ayrıca hava akışsız masa durumu (DOG-044) | Kart | test-muhendisi | Bekliyor | |
| DOG-109 | SYS-063 | M | **[DT-003]** Set kondansatörü veri sayfası: silindirik alüminyum elektrolitik, ≥ 470 µF, ≥ 35 V (8S varyantında ≥ 50 V), 105 °C sınıfı, ESR ≤ 50 mΩ (100 kHz, 20 °C), dalgacık akımı sınıfı yazılı; kullanıcı kılavuzu taslağında zorunluluk + garanti şartı metni ve ipek baskı metniyle tutarlı | Ü-öncesi | bom-tedarik (+ dogrulama-kalite) | Bekliyor | |
