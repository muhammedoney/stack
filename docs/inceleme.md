# İlk inceleme — esc55a, esc65a, fmu (2026-11-06)

Kaynak: `../cezeri/us/` (cezeri reposu, son ilgili commit 2026-02-27). Bu belge kopyalanan tasarımların ve tersine mühendislik çizimlerinin bugünkü durumunu, bulguları ve önerilen sıradaki işleri verir. Sahibi `sistem-mimari`. Sayılar Altium dosyalarından (`tools/altium_sch_dump.py`), KiCad’e geçici içe aktarılmış PCB’den (`kicad-cli pcb import`, `tools/pcb_stat.py`) ve `lib/datasheet/` veri sayfalarından; hesaplar yazılı, tahminler “tahmin” diye işaretli.

## 1. Kopyalanan dosyalar

| Kaynak (`cezeri/us/`) | Hedef | Ne |
|---|---|---|
| `esc55a/esc55a/*` | `boards/esc55a/altium/` | Altium projesi: `main`, `mcu`, `mcu2` SchDoc; `ESC_v0.PcbDoc` (yollu), `FPV_Template.PcbDoc` (eski taslak, projede yok), `escPan.PcbDoc` (boş 100 × 100 mm panel), `StandartJob.OutJob` |
| `esc55a/f55_bls.drawio` | `docs/esc55a.drawio` | 55 A BLHeli_S ESC tersine mühendislik: kart fotoğrafı üstünde 4. kanal (ch4) bağlantıları |
| `esc55a/*.pdf` | `lib/datasheet/` | EFM8BB21 (iki paket), FD6288Q (Çince + İngilizce), JSM6288Q (FD6288Q muadili), AP2210 LDO |
| `esc65a/f65_bls.drawio` | `docs/esc65a.drawio` | 65 A ESC: yalnızca 16 fotoğraf ve iki parça etiketi (FD6288Q, QN3109 MOSFET). Şematik yok |
| `fmu/diatone_f405mk2/fmu_f405/*` | `boards/fmu/altium/` | Altium projesi: tek sayfa `fmu.SchDoc`. **PCB yok** |
| `fmu/diatone_f405mk2/F405mk2.drawio` | `docs/fmu-diatone-f405mk2.drawio` | Diatone Mamba F405 MK2 tersine mühendislik (2 sayfa) |
| `fmu/diatone_f405mk2/*.webp` | `docs/reference/fmu/` | Mamba F405 MK2 ürün görselleri |
| `fmu/diatone_f405mk2/*.pdf` | `lib/datasheet/` | STM32F405RG, MAX7456 / AT7456E, MPU-6050 |
| `fmu/geprc_f405_hd_v3/f405_hd_v3.drawio` | `docs/fmu-geprc-f405-hd-v3.drawio` | GEPRC F405 HD v3 tersine mühendislik (“henüz tamamlanmadı”, 2026-02-27) |

Kopyalanmayanlar: `esc55a/.$f55_bls.drawio.bkp` (drawio yedeği). Altium projeleri ortak kütüphaneye (`../../../libraries/*.SchLib/PcbLib`, cezeri, 21 MB) bağlı; semboller ve ayak izleri SchDoc/PcbDoc içinde gömülü olduğu için KiCad’e taşımada gerekmez. KiCad kütüphanesi taşıma sırasında `lib/` altında kurulacak (fiber’deki `altium_libs.py` yöntemi).

Kaynak geçmişi (cezeri git): FMU şematiği 2025-04-04…04-10 (güç, sensörler, buzzer, ters kutup, konnektörler, “Mamba ile karşılaştırılacak”); ESC panel denemesi 2025-05-29 (“maliyet avantajı olmadı”); ESC bileşenleri 2025-07-24; GEPRC incelemesi 2026-02-27.

## 2. esc55a — 4’ü 1 arada 55 A ESC

### 2.1 Mimari

```
 BAT pedi ─ R00‖R000 (2 × 1 mΩ 2512, yüksek taraf shunt) ─ PWR ─┬─ 24 × ME7170 (4 kanal × 3 yarım köprü) ─ P1a…P4c motor pedleri
                         └ U2 INA199C1 → curr_sens → J0.1      ├─ D00 SMDJ28CA TVS, 22 µF 1206 bulk × 29
                                                                ├─ U1 JW5026 buck → L00 6.8 µH → PVDD 8.07 V ─┬─ 4 × FD6288Q VCC
                                                                │                                             └─ U0 AMS1117-3.3 → +3V3 → 4 × EFM8BB21, INA199
 J0 SM08B-SRSS-TB: 1 CUR · 2 NC · 3 M4 · 4 M3 · 5 M2 · 6 M1 (her biri 220 Ω → chN_in) · 7 PWR · 8 GND
```

Her kanal: EFM8BB21F16G (QFN20) → FD6288Q (QFN24) → 3 × (yüksek + alçak) ME7170, 22 Ω kapı dirençleri, 10 k alçak kapı aşağı çekme, 1N4148WT + 1 µF bootstrap, BEMF bölücüleri (faz → 10 k → muxN; muxN → 1 k → GND; muxN → 3.3 k → com_all). Klasik BLHeli_S düzeni; Bluejay ile uyumlu olması beklenir (pin ataması doğrulanacak, §2.4).

| | Değer |
|---|---|
| Parça | Şematikte 232 (main 100, mcu 66, mcu2 66); PCB’de 224 ayak izi |
| Kart | 41.25 × 47.75 mm dış hat; montaj 30.5 × 30.5 mm, 4 × M3 (Ø 4.57 mm bakırlı delik) |
| Katman | 4: dış 0.075 mm (≈ 2 oz), iç 0.0175 mm (0.5 oz); toplam 1.67 mm |
| Yol | 1730 parça yol (F.Cu 1127, In1 269, In2 258, B.Cu 76), 210 via (çoğu 0.45 / 0.2 mm), 34 bakır bölge; **bağlanmamış 0** |
| Çıktılar | Altium’da gerber/drill/pick-place/STEP üretilmiş (projede listeli, dosyalar kopyalanmadı — kaynakta yok) |

### 2.2 Doğrulanan değerler (hesap)

| Konu | Hesap | Sonuç |
|---|---|---|
| PVDD | JW5026 FB, R02 90.9 k / R01 10 k; V_FB 0.8 V varsayıldı (JW5026 veri sayfası yok) | 0.8 × (1 + 9.09) = **8.07 V** — FD6288Q VCC 5–20 V içinde ✓ |
| 3V3 | AMS1117 8.07 → 3.3 V, yük tahmini 4 × ~10 mA MCU + INA | (8.07 − 3.3) × 0.05 A ≈ 0.24 W ✓ |
| BEMF bölücü | faz → 10 k / (1 k ‖ 3.3 k sanal nötr) | 25.2 V fazda mux ≈ 25.2 × 0.77/10.77 ≈ 1.8 V < 3.3 V ✓ (nötr katkısı ihmal) |
| Akım ölçümü | shunt 1 mΩ ‖ 1 mΩ = 0.5 mΩ; INA199C1 kazanç 200 → 0.1 V/A | Tam ölçek (≈ 3.2 V) ≈ **32 A toplam** |

### 2.3 Bulgular

| # | Önem | Konu | Bulgu | Öneri / sahibi |
|---|---|---|---|---|
| E1 | Kritik | Akım ölçümü aralığı | 0.5 mΩ × 200 → ≈ 32 A’da doyuyor; 4 × 55 A = 220 A sınıfı kart için toplam akımın 1/7’si | Shunt/kazanç yeniden seçilmeli (ör. INA199A1 ×50 ile 0.25 mΩ → 256 A tam ölçek). `guc-elektronigi`, `sistem-mimari` |
| E2 | Kritik | Shunt gücü | Batarya akımı tümüyle iki 2512 dirençten geçiyor: 100 A’da 0.5 mΩ × 100² = **5 W**, 2512 tipik 1–2 W (×2 = 2–4 W) | Düşük direnç/daha çok paralel shunt veya farklı ölçüm (manganin şerit, faz tabanlı). `guc-elektronigi` |
| E3 | Önemli | INA199 ortak mod | INA199 V_CM en çok 26 V; 6S dolu 25.2 V ve TVS kıstırma (SMDJ28CA ≈ 45 V) üstünde kalıyor | Hücre sınırı netleşince (SOR) koruma/parça değişimi. `guc-elektronigi` |
| E4 | Önemli | TVS ↔ kondansatör | Bulk 22 µF **35 V** X5R; SMDJ28CA kıstırma ≈ 45 V; şematik notu “22 µF 50 V low ESR” ile çelişiyor. 25 V öngerilimde 1206 22 µF etkin kapasite tahminen 3–5 µF | 50 V sınıfı ve/veya elektrolitik bulk; TVS seçimi hücre sayısına göre. `guc-elektronigi` |
| E5 | Önemli | Veri sayfası eksik | ME7170 (MOSFET, 24 adet), JW5026 (buck), INA199, AMS1117, SMDJ28CA `lib/datasheet/`’te yok; 55 A iddiası (V_DS, R_DS(on), ısı) doğrulanamıyor | `bom-tedarik` bulsun, `guc-elektronigi` değerlendirsin |
| E6 | Önemli | Çift referans | mcu/mcu2 sayfalarında 4 × `R?` (3 k / 1 k “????”), “Bu dirençlere anlam veremedim” notu | BEMF/nötr ağının parçası olup olmadığı drawio ile karşılaştırılmalı; KiCad’de numaralanacak. `sematik-muhendisi` |
| E7 | Önemli | Telemetri yok | J0.2 NC; ESC telemetrisi yok. Bluejay’de çift yönlü DShot sinyal hattından RPM verir | Gereksinim sorusu (SOR). `sistem-mimari` |
| E8 | Önemli | Konnektör dizilimi | J0: 1 CUR, 2 NC, 3 M4, 4 M3, 5 M2, 6 M1, 7 VBAT, 8 GND. Piyasada 8 pinlik dizilim üreticiden üreticiye değişiyor; FMU J0/J1 ile aynı mı kontrol edilmeli | `docs/pin-haritasi.md`’de tek kaynak. `sistem-mimari` |
| E9 | Küçük | Kurallar | KiCad varsayılan kurallarıyla DRC: 499 açıklık, 199 via çapı (0.45 < 0.5), 199 delik (0.2 < 0.3) — Altium kuralları içe aktarılmadığı için | Taşımada Altium kurallarını `.kicad_pro`’ya yaz. `pcb-muhendisi` |
| E10 | Küçük | Dış hat | 4 adet çok kısa (2 nm – 0.86 µm) dış hat parçası, 114 bakır–kenar ihlali | Taşımada temizlenir. `pcb-muhendisi` |
| E11 | Küçük | Gerilim notu | `main.SchDoc` “max 15V” notu ne için belirsiz (JW5026? AP2210?) | Taşımada açıklığa kavuştur. `sematik-muhendisi` |
| E12 | Küçük | LDO | AP2210 veri sayfası var ama şematikte AMS1117; muadil planı mı belirsiz | `bom-tedarik` |

### 2.4 Açık mimari sorular
- EFM8BB21 port ataması (pin 1 sinyal, 7/11/13–16 köprü, 17–19 mux, 20 nötr) hangi Bluejay/BLHeli_S düzenine karşılık geliyor? Uyarsa yazılım yazılmaz, yalnız yüklenir (`gomulu-yazilim`).
- `FPV_Template.PcbDoc` (8DFN 5 × 6 MOSFET, tek shunt, buck bobini yok) eski taslak mı, ayrı varyant mı?

## 3. esc65a — 65 A ESC

Yalnızca tersine mühendislik başlangıcı: 16 fotoğraf, FD6288Q ve QN3109 (N-MOS, DFN) etiketleri. Şematik, PCB, parça listesi yok. Mimari esc55a ile aynı aile (FD6288Q sürücü, BLHeli_S). 65 A için esc55a’dan farkın (MOSFET, bakır, shunt) ne olacağı gereksinimle belirlenmeli; esc55a’nın 65 A varyantı mı, ayrı kart mı — müşteri sorusu.

## 4. fmu — STM32F405 uçuş kontrol kartı

### 4.1 Mimari (şematikten, tek sayfa, 143 parça)

| Blok | Parçalar | Not |
|---|---|---|
| MCU | U0 STM32F405 LQFP64, Y0 24 MHz | Betaflight/INAV F405 hedefleri |
| IMU | U7 ICM-42688-P (SPI1, INT1/INT2) | “Mamba’da INT2 boşta” |
| Baro | U6 BMP388 (+ yedek U6 BMP280, notta BMP581 seçeneği) | **İki parça aynı referans** |
| OSD | U2 MAX7456 / AT7456E, Y2 27 MHz, CVBS_IN/OUT, R20/R21 75 Ω | SPI2 |
| Flash | U5 W25Q128JV (blackbox) | SPI2 |
| Güç | U3 TPS54202 → 9 V (R32/R33 100 k / 7.15 k → 8.93 V ✓), U4 TPS54202 → 5 V (R42/R43 100 k / 13.7 k → 4.95 V ✓); 3V3 LDO şematikte ayrı görünmüyor | Notlar: “BEC 9 V 1.4 A (VIN 10–28 V)”, “BEC 5 V 2 A (VIN 8–28 V)” |
| Koruma | U9 AO3401A ters kutup (P-MOS), D9 10 V zener, F9 PTC, U1 NUF2042 USB ESD | |
| Kullanıcı | USB-C (R10/R11 5.1 k CC), SW80 boot, 4 LED, buzzer (Q10 AO3400A), LED şerit | |
| Konnektörler | J0/J1 SM08B (ESC 1 ve 2 → 8 motor: chN_in0/in1), J SM03B, J2/J4/J5 SM04B (ELRS, GPS…), J3 SM06B (DJI), VTX, kamera, SBUS pedleri | UART1…6, I2C, SPI1 pedleri |
| VBAT ölçümü | R95 100 k / R92 10 k → 11:1 | 3.3 V ADC’de 36 V tam ölçek ✓ (6S + pay) |

### 4.2 Bulgular

| # | Önem | Konu | Bulgu | Öneri / sahibi |
|---|---|---|---|---|
| F1 | Kritik | PCB yok | FMU yalnız şematik; yerleşim/yol hiç başlamamış | Gereksinim kapısından sonra iş paketi. `pcb-muhendisi` |
| F2 | Önemli | Çift referans | U0 ×2, J1 ×2 (USB-C ve SM08B), U6 ×2 (BMP388/BMP280), C60 ×2, C61 ×2, C? ×3, R? ×2 | KiCad taşımada yeniden numaralama; baro için tek parça + DNP varyantı. `sematik-muhendisi` |
| F3 | Önemli | Kristal | 24 MHz HSE; Betaflight F405 hedeflerinin çoğu 8 MHz. Desteklenir (`SYSTEM_HSE_MHZ`), ama USB ve hedef tanımı buna göre yazılmalı | `gomulu-yazilim` doğrulasın |
| F4 | Önemli | TPS54202 giriş sınırı | VIN en çok 28 V; 6S dolu 25.2 V + sıcak takma geçici. Girişte TVS/sınırlayıcı görünmüyor (D9 10 V zener başka bir hat) | `guc-elektronigi` |
| F5 | Önemli | Zamanlayıcı/DMA | 8 motor çıkışı (iki ESC konnektörü) DShot için zamanlayıcı/DMA çakışmasız atanmalı; şematikte ağ adları var, MCU pinleri doğrulanmadı | `sistem-mimari` + `gomulu-yazilim`, `docs/pin-haritasi.md` |
| F6 | Küçük | Tedarik kodu | Kodlar Digi-Key (ör. 1276-1099-1-ND), LCSC değil | `bom-tedarik` |
| F7 | Küçük | Referans çizimler | Mamba MK2 çizimindeki MPU6050 notu (“SPI desteklemiyor, MPU6000 olmalı”); GEPRC çizimi eksik | Referans olarak kalır |

## 5. Ortak gözlemler

- İki ESC ve FMU aynı Altium kütüphanesinden (RLC, IC, CONN, MOS) ve aynı adlandırmadan geliyor; KiCad’e tek seferde ortak `lib/` ile taşınabilir.
- Hiçbir parçada LCSC kodu yok (ESC’de hiç kod yok, FMU’da Digi-Key). JLC üretimi için BOM sıfırdan kodlanacak.
- Gereksinim yok: akım sınıfı (sürekli/anlık, süre), hücre sayısı, kart ölçüsü, yazılım, telemetri, maliyet ve adet tanımsız. Bulguların çoğu (E1–E4, E7, F4) bu sayılara bağlı.

## 6. Önerilen sıra

1. **Gereksinim kapısı 1:** müşteri ihtiyacı → MUS/SYS/DOG (`gereksinim-muhendisi`), ilk sorular `docs/gereksinimler/sorular.md`.
2. **KiCad’e taşıma:** esc55a şematik + PCB, fmu şematik (`sematik-muhendisi`, `pcb-muhendisi`); Altium kuralları, ortak `lib/`, çift referanslar.
3. **Ü-öncesi analiz:** güç katı kayıp/ısı, shunt aralığı, TVS/kondansatör payları (`guc-elektronigi`, `test-muhendisi`).
4. **Pin haritası:** FMU↔ESC konnektörü ve MCU pinleri tek kaynak `docs/pin-haritasi.md`; Bluejay düzeni ve Betaflight hedefi (`sistem-mimari`, `gomulu-yazilim`).
5. Revizyon tasarımı (esc55a Rev B, esc65a, fmu PCB) ve BOM/maliyet (`bom-tedarik`).
