# fmu — F405 uçuş kontrol kartı (M1)

KiCad şematiği **sıfırdan** çizildi (İP-05, 2026-11-11): `tools/fmu_schematic.py`. Altium şeması (`altium/fmu.SchDoc`, Mamba F405 MK2 tersine mühendisliği, 143 parça) yalnız karşılaştırma girdisidir; hiçbir sembol, ayak izi veya sayfa referans tasarımlardan alınmadı (KRR-006). PCB **yok**.

- Kaynaklar: pin/zamanlayıcı/DMA [`docs/pin-haritasi.md`](../../docs/pin-haritasi.md) §1 (tek kaynak), mimari [`docs/mimari-fmu.md`](../../docs/mimari-fmu.md) §4, güç [`docs/rapor/guc-ip03.md`](../../docs/rapor/guc-ip03.md) §8 (G7–G10, G15–G18), KRR-005…008.
- Semboller: KiCad 10 standart kütüphanesinden `lib/stack.kicad_sym`'ye kopya; SY8303A, AT7456E, ICM-42688-P, DPS368 veri sayfasından çizildi. Ayak izleri: KiCad 10 standart kopyaları `lib/stack.pretty/` (35 yeni dosya). `lib/RLC|IC|MOS|CONN` değişmedi.
- Üretme: `python3 tools/fmu_schematic.py` — tekrar çalıştırılabilir; UUID'ler sabit (uuid5), ikinci çalıştırmada ve dosyalar silinip yeniden üretildiğinde md5 aynı.

## Şematik yapısı

| Sayfa | Dosya | Bloklar | Ref. |
|---|---|---|---|
| 1 | `fmu/fmu.kicad_sch` | Kök: blok akışı, sayfa sembolleri | — |
| 2 | `fmu/power.kicad_sch` | BAT+/− pedleri (F101/Q101 öncesi, J_ESC1.VBAT ile aynı düğüm), F101 5 A, Q101 AO3401A (D pil, S VIN) + 10 V zener + 100 k, D102 SMBJ24CA, 2 × 10 µF 50 V + 3 × 100 nF; U101 SY8303 5 V/2 A (L 6.8 µH SWPA6045), U102 SY8303 9 V/1.5 A (L 10 µH SWPA5040, EN ← PB11), U103 AMS1117-3.3 (22 µF), IMU süzgeci 10 Ω + 2.2 µF + 100 nF, VBAT 140 k/10 k %0.5 + 100 nF → PC0, CUR1 10 k + 100 nF → PC1, CUR2 1 k + 100 nF → PC5, SJ101 + 10 k (ortalama), test noktaları | 1xx |
| 3 | `fmu/mcu.kicad_sch` | STM32F405RGT7, VDD 4 × 100 nF + 4.7 µF, VDDA ferrit + 1 µF + 100 nF, VCAP 2 × 2.2 µF, NRST 100 nF, BOOT0 düğmesi + 10 k, BOOT1 10 k, HSE 8 MHz + 2 × 18 pF, LED0 (PC13), buzzer AO3400A (PC15) + pedler, SWD pedleri | 2xx |
| 4 | `fmu/sensors.kicad_sch` | ICM-42688-P SPI1 (CS PA4, INT1 PC4), DPS368 I2C1 0x76 + 2 × 2.2 k, GD25Q128 SPI3 (CS PC14) | 3xx |
| 5 | `fmu/osd.kicad_sch` | AT7456E SPI2 (CS PB12), 27 MHz, 5 V, CVBS giriş 0.1 µF + 75 Ω, çıkış 75 Ω | 4xx |
| 6 | `fmu/io.kicad_sch` | USB-C + 2 × 5.1 k + USBLC6-2SC6 + PMEG3020 (VBUS → 5 V), J_ESC1/J_ESC2 SM08B (J_ESC2 DNP, VBAT 0 Ω DNP), M5–M8 pedleri, RX SH4 (UART2), DJI SH6 (UART1 + 9 V + SBUS), GPS SH6 (UART6 + I2C1 + 5 V), SBUS → 74LVC1G04 → 1 k → PA3, UART3/4/5 pedleri, VTX/kamera, LED şerit, S9 pedleri | 5xx |

Sayfalar arası sinyaller global etiket; raylar (GND, +3V3, +3V3_IMU, +5V, +9V, VIN, VBAT, VBUS) güç sembolü. Ağ adları pin haritasındaki işlevlerden (M1…M8, UART1_TX, SPI1_MISO, IMU_CS, ADC_VBAT …). Kullanılmayan MCU pini yok (51 G/Ç dolu); diğer IC'lerin boş pinleri NC.

**FMU↔ESC 8 pin dizilimi** tek tabloda: `ESC_PINOUT` (`tools/fmu_schematic.py`). Bugün esc55a J0 sırası (1 CUR, 2 TLM, 3 M4, 4 M3, 5 M2, 6 M1, 7 VBAT, 8 GND); İP-10 SpeedyBee F405 V4'e göre değiştirirse yalnız tablo değişir ve betik yeniden çalıştırılır.

## Parça özeti (141 sembol: 104 BOM, 37 ped/test noktası/köprü; DNP 2: J503, R503)

| İşlev | Parça (LCSC) | Sıcaklık sınıfı |
|---|---|---|
| MCU | STM32F405RGT7 (C1337199) | −40…105 °C |
| IMU | ICM-42688-P Tokmas (C54308212), ALT TDK C1850418 | −40…85 °C **istisna** |
| Baro | DPS368XTSA1 Infineon (C3232508), ALT Tokmas C55090144 | −40…85 °C **istisna** |
| Flash | GD25Q128ESJGR (C22404005), ALT W25Q128JVSIQ C97521 | −40…105 °C (sipariş kodu J) |
| OSD | AT7456E (C82351) | −40…85 °C **istisna** |
| Buck × 2 | SY8303AAIC (C2937216) | T_A −40…105 °C |
| LDO | AMS1117-3.3 (C6186), ALT UMW C347222 | −40…125 °C |
| Ters kutup / zener / TVS / sigorta | AO3401A (C15127) / MM3Z10V (C42370498) / SMBJ24CA (C78416) / CFS12V3T5R0 (C163128) | T_J 150 / 150 / 150 °C / −20…105 °C |
| Bobinler | SWPA6045S6R8MT (C57254), SWPA5040S100MT (C84608) | −40…125 °C |
| Kristaller | 8 MHz HCI XC32M4 (C5179501) / 27 MHz YXC (C9008) | 105 °C / 85 °C **istisna** |
| USB | TYPE-C-31-M-12 (C165948), USBLC6-2SC6 (C2827654), PMEG3020EH (C19268151) | −30…80 °C **istisna** / 125 / 150 °C |
| Konnektör | XY-SM08B ×2, XY-SM04B, XY-SM06B ×2 (ALT JST) | −40/−25…85 °C **istisna** |
| Diğer | 74LVC1G04 TI, AO3400A, 1N4148WT, KT-0603R LED, TS-1088 düğme | 125 / 150 / 150 / 85 **istisna** / 80 °C **istisna** |
| Pasifler | Seramikler tümü X7R/C0G; dirençler UNI-ROYAL 0402WGF, VBAT bölücü %0.5 | −55…125 / −55…155 °C |

Her sembolde Value, Footprint, Datasheet, Description, MPN, Manufacturer, LCSC, Temperature; gerekirse ALT MPN/ALT LCSC, `8S` (VIN parçalarında 8S BOM notu, KRR-007) ve `Variant` (J503). LCSC kodları, stok ve sıcaklık JLC/LCSC parça arayüzünden 2026-11-11.

## Kontroller (2026-11-11)

| Kontrol | Sonuç |
|---|---|
| `LC_ALL=C.UTF-8 kicad-cli sch erc --severity-all boards/fmu/fmu/fmu.kicad_sch` | **0 hata, 0 uyarı** |
| Netlist ↔ `docs/pin-haritasi.md` §1.1 (64 MCU pini: pin adı + ağ) | **64/64 aynı, fark 0** |
| §3 kuralları: M1–M4 → J_ESC1, M5–M8 → J_ESC2, CUR1 → PC1, CUR2 → PC5, TLM J_ESC1 → PD2, J_ESC2 TLM NC, J_ESC2 VBAT bağlı değil, J_ESC1.VBAT = BAT+ = F101 girişi | **hepsi sağlanıyor** |
| İdempotent (ikinci çalıştırma ve sıfırdan üretim) | md5 aynı |
| BEC geri besleme (SY8303 VFB 0.600 V ±%1.5, DS) | 5 V: 100 k/13.7 k → 4.98 V (4.82–5.14); 9 V: 100 k/7.15 k → 8.99 V (8.69–9.30); R_FS 200 k → 500 kHz (f = 1e5/R_FS[k]) |
| VBAT bölücü | 140 k/10 k → 15:1, tam ölçek 49.5 V (SYS-022 ≥ 45 V) |

Pin karşılaştırma betiği oturum dizininde tutuldu (`pinmap_check.py`: §1.1 tablosunu ayrıştırır, kicadsexpr netlistini karşılaştırır).

## Maliyet (100 set, JLC 2026-11-11) — `bom-revb.csv`

| | $/kart |
|---|---|
| Komponent (std SKU) | 25.09 |
| PCB (36 × 36, 4 kat, `docs/bom-maliyet.md` §3 tahmini) | 0.25 |
| Dizgi (§4 yöntemi, Economic tek yüz [varsayım], 33 extended tür, 382 lehim noktası) | 1.72 |
| **FMU toplam** | **27.06** |
| Dual SKU farkı (J503) | +0.07 |

MCU tek başına 13.03 $ (STM32F405RGT7, JLC stoğu **4**). RGT6 (85 °C, stok 24) ile 18.61 $; RGT6 + Tokmas baro + W25Q128 ile ≈ 16.35 $.

## Açık konular

1. **MCU tedariki:** STM32F405RGT7 JLC/LCSC stoğu 4 (< 200), 13.03 $; RGT6 de 24 adet. `bom-tedarik` dış tedarik/konsinye fiyatı; KRR-008 MCU satırı maliyetle birlikte yeniden değerlendirilmeli.
2. **ESC 8 pin dizilimi** (İP-10, KRR-004): `ESC_PINOUT` geçici.
3. **SH konnektör cihaz tarafı dizilimleri** (RX, DJI, GPS) doğrulanmadı; SYS-065 GPS'i 4 pin diyor, mimari §4.2 6 pin (UART6 + I2C1 + 5 V) — ikincisi uygulandı, dış I2C bu konnektörde.
4. **Flash:** GD25Q128 Betaflight `flash_m25p16` tablosunda (0xC84018) var, `USE_FLASH_M25P16` gerekir (pin-haritasi §1.4 W25Q128FV yazıyor); ArduPilot `AP_Logger_Flash_JEDEC` tablosunda yok → AP yaması veya ALT W25Q128JVSIQ (85 °C istisnası).
5. **Baro:** DPS368 DPS310 sürücüsüyle çalışır (BF `barometer_dps310`, AP `AP_Baro_DPS280`, ID 0x10). DPS310 ve SPL06-001 stokta yok; SPA06-003 Betaflight'ta yalnız deneme sondası (sürücü yok), SPL07-003 ArduPilot'ta SPA06 sanılır — ikisi de seçilmedi.
6. **Ayak izleri `pcb-muhendisi` doğrulayacak:** ICM-42688-P için KiCad `LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y` (DS: D 2.5, E 3, D1 1.5, E1 1.0 ile uyumlu), DPS368 için `Bosch_LGA-8_2x2.5mm` (saat yönü numaralama), AT7456E açık ped ölçüsü, HCI kristal pin 1/3 sinyal.
7. **Q101** 3S tam yükte 0.45 W (G16): JSM7409 DFN3.3 ayak izi farklı → BAT pedleri + kılavuz yük sınırıyla AO3401A kaldı.
8. **USB'de VIN:** USB 5 V, U101'in üst MOSFET gövde diyoduyla VIN'e ≈ 4 V sızar (9 V buck UVLO 4.35 V altında, ADC_VBAT ≈ 4 V okur); `guc-elektronigi` incelesin.
9. **9 V EN:** PB11 → 1 k → EN, 100 k → 3V3 (sıfırda açık); Betaflight `PINIO1_CONFIG 129` anlamı `gomulu-yazilim` ile teyit.
10. Listeden sapmalar (gerekçeli): IMU süzgeç kondansatörü 2.2 µF (DS Şekil 5; listede 1 µF); CUR1 → PC1 yolunda 10 k (SJ101 kapalıyken eşit ağırlıklı ortalama için); flash ~WP/~HOLD 10 k ile 3V3'e; DJI pin 6 SBUS, SBUS pedi ile aynı ağ.
11. 8S BOM varyantı: VIN parçalarında `8S` alanı; 60 V buck ayak izi farkı PCB yer payı işidir (`pcb-muhendisi`).
