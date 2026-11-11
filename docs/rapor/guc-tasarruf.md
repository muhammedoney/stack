# §10 tasarruf (B2–B6), FMU 3.3 V, JW5026 muadili ve güç parçası ALT incelemesi (guc-elektronigi)

> **Tarih:** 2026-11-12. **Hazırlayan:** `guc-elektronigi` (yalnız inceleme; bu dosya dışında proje dosyası değiştirilmedi, commit yok).
> **Girdi:** `docs/bom-maliyet.md` §10, `boards/tasarruf-2026-11-11.csv`, `docs/rapor/guc-ip03.md`, `boards/{esc55a,fmu}/README.md`, `boards/{esc55a,fmu}/bom-revb.csv`, `docs/gereksinimler/sistem.md` (SYS-014, 020, 021, 036, 040…046, 086, 087, 091, 095), `docs/gereksinimler/kararlar.md` (KRR-008, KRR-011), `lib/datasheet/`. ESC bağlantıları Rev B şematiğinden (`kicad-cli sch export netlist`, geçici dizine); FMU bağlantıları `tools/fmu_schematic.py`.
> **Fiyat / stok:** JLC parça arayüzü (`tools/jlc.py`, önbellek kopyası scratchpad'de), 2026-11-12. 100 set birim fiyatı = 100 × karttaki adet kademesi.
> **Müşteri girdisi (2026-11-12, DT-005):** §10 A ve B uygun (bu inceleme şartıyla); 3.3 V regülatörü küçük kılıf (SOT-223 değil, SYS-042 notu); kritik parçalarda pin + ayak izi uyumlu (drop-in) muadil (SYS-095, KRR-011).
> **Hesap kuralı:** tolerans en kötü durum (doğrusal toplam), yanında RSS. "T" = tahmin (ölçülmeli).

## 0. Özet (yönetici için)

| # | Konu | Karar | Bir cümle |
|---|---|---|---|
| 1 | B2 INA240A3 → INA281B2 | **RET** | INA281B2 kazancı ×50 (×20 olan B1); ofset en kötü ±300 µV = ±3 A → SYS-021 (< 10 A’da ±1 A, 10 A’da ±0.5 A) karşılanmaz; başka üreticiden SOT-23-5 B dizilimli ×50 drop-in yok. **Yerine:** SOIC-8 ayak izi kalır, ana **RSA240CXK (Runic, ×100, INA240 ile aynı pinler)**, ALT **INA240A3DR** → −1.19 $/stack (B2’nin −0.52’si yerine), `ibata_scale` 100 değişmez |
| 2 | B3 PMEG3020EH → B5819W | **Koşullu onay** | V_F +0.1 V, T_J 125 °C (SYS-087 ≥ 85 ✓); USB’de 5 V ≈ 4.3–4.6 V. Açık sorun (USB’de VIN’e ≈ 4 V sızıntı) için 5 V çıkışına **P-MOS yük anahtarı** (AO3401A + MMBT3904 + 2 × 100 k) |
| 3 | B4 5 V FB 100 k/13.7 k → 15 k/2 k | **Koşullu onay** | 5.10 V; en kötü 4.94–5.27 V (üst sınır 0.02 V aşıyor, RSS 4.98–5.22 ✓); kararlılık değişmez (iç kompanzasyon, C_FF yok). Yük anahtarı düşümüyle (2 A’da 0.12 V) pencere ortalanır. Ref düzeltme: **R104/R105** (R101 değil) |
| 4 | B5 1N4148WT → 1N4148WS ×12 | **Onay** | T_J 150 °C, V_R 100 V, t_rr 4 ns, V_F aynı; R_θJA 625 < 833 K/W; T_J ≈ 96 °C (kart 95 °C) |
| 5 | B6 JW5026 FB/EN 90.9 k → basic | **Koşullu onay** | R0 (EN) 100 k, R02 (FB üst) **20 k**, R01 (FB alt) 10 k → **2.2 k** → PVDD 8.07 V (7.73–8.43) **değişmez**; UVLO payı aynı (VCC +2.7 V, V_BS +1.7 V) |
| 6 | FMU 3.3 V küçük kılıf | **Buck öner** | SOT-89 LDO 0.46 W × 165 K/W = +76 K ✗; **TLV62569DBVR (TI) + ALT SY8089A1AAC (Silergy)**, SOT-23-5 aynı pinler, V_FB 0.6 V; 2.2 µH + 22 µF; kayıp 0.43 W → ≈ 0.1 W; IMU dalı 10 Ω → 22 Ω |
| 7 | JW5026 muadili (stok) | **Yeni ana SCT2400TVBR (SCT) + ALT JW5026 / JW5018 (JoulWatt)** | Hepsi SOT-23-6, BST-GND-FB-EN-VIN-SW aynı; V_IN mutlak 42/44 V, T_J 125 °C; aynı FB (20 k/2.2 k) ve L00 10 µH ile çalışır |
| 8 | Güç parçaları ALT | Tablo §8 | BLP016↔NTMFS ✓; JSM6288Q1 ↔ FD6288Q elektriksel ✓ ama **FD6288Q stok 0** → ALT **HL6288Q**; TVS’ler ✓; **SY8303 tek üretici (istisna, ALT SY8303AIC)**; AO3401A ✓; shunt ALT koşullu (EB3921, TCR ±300 ppm); bobinler ✓ |

**Paket güç açısından:** B2 hariç uygulanabilir; B2 yerine RSA240C önerisi ve madde 2/6/7 değişiklikleri şematiğe işlendikten sonra kapanabilir (koşullar §10).

## 1. Bulgular tablosu (istenen biçim)

| # | Konu | Karar | Gerekçe + hesap (özet; ayrıntı §2–§8) | Ana parça + LCSC | Drop-in ALT + LCSC | Sahibi |
|---|---|---|---|---|---|---|
| 1 | ESC U2 akım yükselteci (B2) | **Ret (INA281B2)**; karşı öneri | INA281B2 G = 50 (DS SBOSA29A Tablo 5.5); 280 A → 1.40 V ✓; V_CM −4…110 V ✓; ama V_OS ±300 µV maks → 3.0 A; toplam ofset 4.7 A (doğrusal) / 3.2 A (RSS) > 1 A ✗; ±%5 ancak ≥ 165 A’da. AC CMRR 65 dB @50 kHz (PWM bastırması yok). Drop-in ikinci üretici yok | **RSA240CXK, Runic, C54300729** (SOIC-8, ×100, 0.597 $) | **INA240A3DR, TI, C2060584** (aynı pin 1 IN− 2 GND 3 REF2 4 NC 5 OUT 6 VS 7 REF1 8 IN+) | sematik-muhendisi, bom-tedarik, test-muhendisi |
| 2a | FMU D501 (B3) | Koşullu onay | B5819W: 40 V / 1 A, V_F ≈ 0.45 V @0.4 A (DS eğrisi; 0.6 V maks @1 A), T_J 125 °C; PMEG3020EH 0.41 V @1 A tip. Kayıp 0.25 A × 0.42 V = 0.1 W → +20 K | **B5819W SL, CJ, C8598** (basic, SOD-123) | **B5819W, MCC / diğer SOD-123** — gerek yok: tek basic yeterli; ALT olarak eski **PMEG3020EH C19268151** (SOD-123F, ayak izi kesişimi pcb) | sematik-muhendisi, pcb-muhendisi |
| 2b | FMU USB’de VIN sızıntısı | **Önemli**, çözüm | +5V → L101 → U101 LX → üst FET gövde diyodu → VIN ≈ 4.3 V; Q101 (V_GS −4 V) açılır → BAT pedleri ve J_ESC1.VBAT 4 V olur (ESC beslenir), U102 UVLO (4.35 V) sınırında salınır, ADC_VBAT 4 V okur | **Q102 AO3401A C15127** (basic) + **Q103 MMBT3904 C20526** (basic) + R 100 k ×2 C25741 | Q102 ALT **AO3401A UMW C347476**; Q103 ALT **MMBT3904LT1G onsemi C81464** | sematik-muhendisi, pcb-muhendisi |
| 3 | FMU 5 V FB (B4) | Koşullu onay | V_REF 0.591–0.609 V (DS, 25 °C); 0.6 × (1 + 15/2) = 5.10 V; en kötü 4.94–5.27 V, RSS 4.98–5.22 V; C_FF yok → döngü değişmez | R104 **15 k C25756**, R105 **2 k C4109** (basic) | genel (direnç) | sematik-muhendisi |
| 4 | ESC D13…D45 (B5) | Onay | 1N4148WS CJ: V_RRM 100 V, I_F 300 mA, T_J 150 °C, t_rr 4 ns, R_θJA 625 K/W; ortalama 1.4 mA → 1 mW | **1N4148WS C2128** (basic, SOD-323) | **1N4148WS başka üretici** (ör. onsemi/Diodes) bom-tedarik; diyot kritik değil | sematik-muhendisi, pcb-muhendisi |
| 5 | ESC JW5026 R0/R02/R01 (B6) | Koşullu onay | 0.8 × (1 + 20/2.2) = 8.07 V; en kötü 7.73–8.43 V (JW5026), 7.83–8.53 V (SCT2400); EN 100 k: eşik 1.3 V, EN mutlak 44/42 V | R0 **100 k C25741**, R02 **20 k C25765**, R01 **2.2 k C25879** (basic) | genel | sematik-muhendisi |
| 6 | FMU U103 3.3 V | Buck öner (LDO SOT-89/DFN ret/yedek) | LDO: (5.10 − 3.3) × 0.24 + 5.1 × 0.005 = 0.46 W; SOT-89 165 K/W → +76 K (70 °C kartta 146 °C ✗); buck η ≈ %88 → 0.11 W | **TLV62569DBVR, TI, C141836** + L **WPN201610H2R2MT C97005** + 100 k/22 k | **SY8089A1AAC, Silergy, C479074**; L ALT **Murata DFE201612P-2R2M=P2 C79317** | sematik-muhendisi, pcb-muhendisi |
| 7 | ESC U1 buck | Yeni ana + ALT | SCT2400: V_IN mutlak 42 V ≥ 40 ✓, T_J 125 ✓, 600 mA (yük 75 mA), V_FB 0.81 V ±%2.5 (−40…125 °C), 2 MHz, stok 8 410 | **SCT2400TVBR, SCT, C2693819** | **JW5026SOTB#TRPBF, JoulWatt, C185109**; ALT2 **JW5018SOTB#TRPBF C3040676** | sematik-muhendisi, bom-tedarik |
| 8 | Güç parçaları | §8 tablosu | — | — | — | bom-tedarik, sematik-muhendisi, pcb-muhendisi |

## 2. Madde 1 — B2: INA240A3DR → INA281B2IDBVR (ESC U2)

### 2.1 Kazanç (×50 / ×20 çelişkisi)
TI INA281 veri sayfası SBOSA29A (Kasım 2023), s.1 ve Tablo 5.5 (s.4): **INA281A1/B1 = 20 V/V, A2/B2 = 50 V/V**, A3/B3 = 100, A4/B4 = 200, A5/B5 = 500. **INA281B2 = ×50.** "×20" yanlış (B1’e ait). A ve B harfi kazanç değil **pin dizilimi**dir (s.3 Şekil 4-1/4-2):

| Pin | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| INA281**A** | OUT | GND | IN+ | IN− | VS |
| INA281**B** | OUT | GND | VS | IN+ | IN− |

→ CUR = 0.1 mΩ × 50 = **5 mV/A**; 280 A → **1.40 V** (SYS-020 ≤ 3.3 V ✓); tam ölçek (3.3 − 0.15 V)/5 mV = 630 A, V_SENSE sınırı V_S/G = 66 mV → 660 A ✓. Çözünürlük 0.16 A/LSB (INA240A3’te 0.08).
**Betaflight ölçeği:** birim 0.1 mV/A → **`ibata_scale = 50`** (§10.2’deki "100 → 200" ters yönde ve yanlış; 200 = 20 mV/A). Bu öneri reddedildiği için uygulanmaz; bilgi `gomulu-yazilim`’e.

### 2.2 Doğruluk (SYS-021: kart başına kalibrasyon yok, 10–200 A ±%5, < 10 A ±1 A, −10…+50 °C)
Model: ofset terimleri (V_OS, sürüklenme ×35 K, CMRR × |V_CM − test V_CM| ≤ 35 V, PSRR × (5 − 3.3 V), ADC ±5 LSB = 4.03 mV) + kazanç (yükselteç + shunt %1 + shunt TCR × 60 K öz ısınma). Veri: INA281 DS Tablo 5.5; INA240 SBOS662; RSA240 Runic DS §7.3.

| Yükselteç | mV/A | V_OS maks | Ofset toplam doğrusal / RSS (A) | Kazanç hatası | Hata @5 A / 10 A / 30 A / 200 A (doğrusal) | Sınır | Sonuç |
|---|---|---|---|---|---|---|---|
| **INA281B2** | 5 | ±300 µV (×2; drift ±1 µV/°C, CMRR ≥ 120 dB) | **4.68 / 3.15** | %2.2 | 4.8 / 4.9 / 5.3 / 9.0 A | 1 / 0.5 / 1.5 / 10 A | **✗** (±%5 ancak ≥ 165 A’da) |
| INA281B2 tipik | 5 | 55 µV | 1.45 / 0.98 | %1.7 | 1.5 / 1.6 / 2.0 / 4.8 | | ✗ (tipikte bile 10 A ✗) |
| INA240A3 (mevcut) | 10 | ±25 µV (drift 0.25 µV/°C, CMRR ≥ 132 dB) | 1.00 / 0.52 | %1.8 | 1.1 / 1.2 / 1.5 / 4.6 | | RSS’de ✓ (guc-ip03 §5.2 ile uyumlu; 10 A’da 0.55 A, "±%5 veya ±1 A" yorumuyla ✓) |
| **RSA240C** 25 °C | 10 | ±30 µV | 0.97 / 0.55 | %1.7 | 1.1 / 1.1 / 1.5 / 4.4 | | INA240A3 ile eşdeğer ✓ |
| RSA240C sıcaklık üst sınırı | 10 | ±200 µV (−40…125 °C, SQC) | 2.67 / 2.05 | %2.1 | 2.8 / 2.9 / 3.3 / 6.9 | | ✗ olabilir → **ölçümle doğrula** |

**PWM / dalgalanma:** INA281 AC CMRR 65 dB @50 kHz. Set kondansatörüyle BAT dalgalanması ≈ 1.5 Vpp (guc-ip03 §6.3, T) → 24 kHz’de ≈ 70 dB (T) → giriş eşdeğeri 0.47 mVpp → çıkışta 24 mVpp; 0 A civarında çıkış GND’ye kırpılır (swing ≤ 20 mV) → doğrultma kayması ≈ 12 mV/π ≈ 3.8 mV ≈ **0.8 A** (T). INA240 ve RSA240 "PWM bastırmalı" (INA240 93 dB @50 kHz).
**Diğer:** V_CM 35 V tepe ✓ (çalışma 110 V, dayanım 120 V); I_B 20 µA/giriş (giriş süzgeci yok, ✓); bant 1.3 MHz; C_load ≤ 500 pF (R03/R04 22 Ω seri yalıtım ✓); V_S 2.7–20 V ✓; −40…125 °C ✓ (SYS-086 d).

### 2.3 Drop-in muadil (SOT-23-5, B dizilimi, ×50, ≥ 40 V V_CM, başka üretici)
- TI içinde: INA293B2 (aynı B dizilimi, ×50; stok 20) — **aynı üretici**, stok yetersiz.
- AnalogySemi **CSA220NA** (C5359394, SOT-23-5, ×50, 0–76 V, V_OS 5 µV, sıfır sürüklenme): pinler **1 GND 2 OUT 3 VDD 4 RS− 5 RS+** (DS s.4) → **drop-in değil**; bant 50 kHz.
- 3PEAK/SGM/Runic/Novosense SOT-23-5 110 V sınıfı INA281 eşleniği LCSC’de bulunamadı (tarama: "INA281", "-4V~110V", "SOT-23-5 50V/V", "CS281", "TP281", "NSCSA281").
→ INA281B2 için drop-in ALT **yok** (istisna olurdu) **ve** SYS-021’i karşılamıyor → **ret**.

### 2.4 Karşı öneri (SOIC-8 ayak izi değişmez, Rev B şematiği ve Kelvin düzeni aynen)
- **Ana: Runic RSA240CXK, C54300729** (SOP-8, ×100, V_CM −5…100 V çalışma / −10…105 V mutlak, −40…125 °C, T_J 150 °C, V_OS ±30 µV @25 °C, kazanç hatası ±%0.1 @25 °C / ±%0.5 tüm sıcaklık, PWM bastırmalı, 500 kHz; stok 3 822; **0.597 $ @100**). Pinler (DS s.5): 1 IN−, 2 GND, 3 REF2, 4 NC, 5 OUT, 6 VS, 7 REF1, 8 IN+ = **INA240 SOIC-8 ile birebir**; REF1 = REF2 = GND tek yönlü kullanım DS §8.4.2’de var.
- **ALT: TI INA240A3DR, C2060584** (1.79 $, stok 1 511). Aynı kazanç → **`ibata_scale = 100` her iki parçada aynı** (KRR-011 kural 6 ✓).
- Maliyet: 1.788 → 0.597 $ = **−1.19 $/stack** (B2’nin −0.52’sinden 0.67 $ fazla). Dizgi tür sayısı aynı.
- **Koşul (DOG-019’a ek):** RSA240’ın sıcaklıktaki ofseti yalnız ±200 µV üst sınırla verilmiş. Prototipte ≥ 5 kartta 0 A ve 10 A’da −10 / 25 / +50 °C ölçüm; |V_OS| ≤ 50 µV (0.5 A) değilse seri üretimde ALT INA240A3 takılır (PCB değişmez, +1.19 $).

## 3. Madde 2 — B3: PMEG3020EH → B5819W (FMU D501) ve USB’de VIN sızıntısı

### 3.1 B5819W (CJ, C8598) — veri sayfası (CJ "B5817W-5819W", D, Mar 2015)
| | PMEG3020EH (TECH PUBLIC, C19268151) | B5819W (CJ, C8598) |
|---|---|---|
| V_RRM / I_O | 40 V / 2 A | 40 V / 1 A |
| V_F | 0.41 V tip @1 A, 0.5 V maks @2 A (25 °C) | 0.6 V maks @1 A; eğriden ≈ 0.40 V @0.25 A, ≈ 0.45 V @0.4 A |
| T_J | −55…150 °C | **125 °C**; R_θJA 200 K/W |
| Kılıf | SOD-123FL | SOD-123 |

- USB yükü (yalnız USB): 3.3 V hattı 240 mA + OSD + pedler. LDO’yla 5 V’tan ≈ 0.3–0.4 A; madde 6’daki buck’la 0.24 × 3.3/(5 × 0.88) ≈ 0.18 A + OSD ≈ 0.25 A.
- 5 V rayı USB’de: V_BUS 4.75–5.25 V − V_F 0.40–0.45 V = **4.30–4.85 V** (PMEG ile 4.40–4.90 V). AMS1117 düşümü 1.1–1.3 V → 3.3 V için ≥ 4.5 V gerekir: **LDO ile V_BUS < 4.95 V’ta 3.3 V regülasyon dışı** (PMEG’de de < 4.85 V’ta) → madde 6 buck’ı (%100 görev, düşüm 0.24 A × 0.16 Ω ≈ 0.04 V) bu sorunu kaldırır. AT7456E 4.75 V alt sınırı yalnız USB’de karşılanmaz (her iki diyotta) — bilgi; OSD uçuşta 5.10 V’tan beslenir.
- Isı: 0.25 A × 0.42 V = 0.10 W → +20 K; USB masa koşulu (kart ≈ 30 °C) → T_J ≈ 50 °C. Uçuşta diyot ters kutuplu, kayıp ≈ 0.
- Sıcaklık sınıfı: SYS-087 (≥ 85 °C) ✓. **Not:** KRR-008 tablosunda FMU sütunu "diyot T_j ≥ 150 °C" satırı müşteri güncellemesinden sonra düzeltilmemiş; SYS-087 metni (≥ 85 °C) esas alındı → `gereksinim-muhendisi` tabloyu netleştirsin.
- Ters sızıntı (5 V → V_BUS, kablo takılı değilken): B5819W 25 °C’de µA, 100 °C’de ≈ 1 mA mertebesi (DS eğrisi); PMEG de aynı sınıf → SYS-036 açısından fark yok.
- **Karar: koşullu onay** (koşul: madde 6 buck’ı veya V_BUS ≥ 4.95 V varsayımı; ayak izi SOD-123, PMEG’in SOD-123F’i ile ortak ped `pcb-muhendisi`).

### 3.2 Açık sorun: yalnız USB takılıyken VIN ≈ 4 V
**Yol:** V_BUS → D501 → +5V → L101 → U101.LX → SY8303 üst FET gövde diyodu (LX → IN) → **VIN ≈ 5 − 0.45 − 0.7 ≈ 3.9–4.3 V**. Her senkron/asenkron monolitik buck’ta bu diyot vardır; diyot seçimiyle çözülmez.
**Etkileri (netlist, `tools/fmu_schematic.py`):**
1. Q101 AO3401A (S = VIN, G → 100 k → GND): V_GS ≈ −4 V > |V_th| ≈ 0.9 V → **açılır**; BAT+ pedleri ve **J_ESC1.VBAT ≈ 4 V** → ESC’nin JW5026’sı UVLO (4.0–4.6 V) sınırında, ESC MCU’ları belirsiz besleme alabilir, USB akımı ESC’ye akar.
2. U102 (9 V, EN 100 k ile açık): VIN UVLO 4.35 V sınırında → aç/kapa salınımı (T).
3. ADC_VBAT ≈ 4 V → Betaflight 1S pil görür (uyarı/bip).

**Önerilen çözüm (F5, 5 V çıkışında yük anahtarı):**
```
U101 → L101 → C107/C108 (+ R104/R105 FB burada, döngü değişmez) = "+5V_BUCK"
+5V_BUCK ─ D ┐ Q102 AO3401A (P) ┌ S ─ +5V (yükler, D501 katodu, U103 girişi)
             G ── R_a 100 k ── +5V   (kapalı tutar)
             G ── Q103 MMBT3904 C ; E → GND ; B ── R_b 100 k ── VIN
```
- Gövde diyodu D → S (buck → ray) yönünde: buck’tan yüke iletir, **raydan buck’a bloke eder** → USB’de VIN = 0 V, Q101 kapalı, ESC beslenmez, U102 kapalı, ADC_VBAT 0 V.
- Pil varken: VIN ≥ 1.5 V’ta Q103 doyar (I_B = (9 − 0.7)/100 k = 83 µA @3S, 0.34 mA @35 V; kollektör yükü 50 µA) → Q102 V_GS ≈ −5 V → R_DS(on) ≤ 60 mΩ (AOS DS, −4.5 V) → 2 A’da **0.12 V düşüm, 0.24 W** (SOT-23 ≈ 125 K/W → +30 K ✓).
- Q103 V_CEO 40 V; kollektör ≤ 5.3 V ✓. 8S varyantında (40 V) I_B 0.4 mA ✓; değişiklik gerekmez.
- Pil + USB birlikte: Q102 açık, ray 5.10 − 0.12 V; V_BUS − V_F ≤ 4.85 V < ray → D501 kapalı ✓.
- Maliyet ≈ +0.06 $/stack (hepsi basic, yeni tür yok). Alan: 2 × SOT-23 + 2 × 0402.
- Reddedilen seçenekler: U101 girişine seri Schottky (3S tam yükte 1.2 A × 0.45 V = 0.55 W, VIN UVLO payı düşer); yükü VBUS’tan ayrı bir ‘USB rayı’na bölmek (SYS-036 "USB’de 5 V hattı çalışır" ✗); geri beslemeyi anahtardan sonra almak (döngüye kutup ekler).

## 4. Madde 3 — B4: FMU 5 V geri besleme (U101 SY8303A)

- **Ref düzeltmesi:** FB üst = **R104** (100 k), alt = **R105** (13.7 k) (`tools/fmu_schematic.py` satır 539–540, 938). CSV/§10’daki "R101/R105" yanlış: **R101 Q101 kapı direncidir, değişmemeli.**
- Basic 0402 değerleri (JLC taraması: 1 k, 1.5 k, 2 k, 2.2 k, 3.3 k, 4.7 k, 5.1 k, 10 k, 12 k, 15 k, 20 k, 22 k, 33 k, 47 k, 51 k, 100 k, 200 k) içinde 4.8–5.3 V veren tek çift **15 k / 2 k** (33 k/4.7 k → 4.81 V düşük).
- V_OUT = 0.6 × (1 + 15/2) = **5.100 V**. SY8303A DS s.4: V_REF 0.591–0.609 V (yalnız 25 °C verilmiş), I_FB ±50 nA (15 k’da 0.75 mV, ihmal).
  - En kötü (%1 direnç + V_REF): 0.591 × (1 + 14.85/2.02) = **4.936 V** … 0.609 × (1 + 15.15/1.98) = **5.269 V** → üst sınır SYS-040 (5.25 V) **+0.019 V** aşıyor (yüksüz, yük anahtarından önce).
  - RSS: ±%2.3 → **4.98–5.22 V** ✓.
  - Madde 2 yük anahtarıyla rayda: 2 A’da −0.12 V → **4.82–5.15 V** ✓; 100 k/13.7 k ile bu 4.70 V’a düşerdi ✗ → 5.10 V ayarı anahtarla birlikte daha iyi.
- Kararlılık: SY8303A iç kompanzasyonlu tepe akım modu; şematikte C_FF (C1 opt.) yok → döngü kazancı yalnız oran (0.6/5.1) ile belirlenir, oran ≈ aynı (4.98 → 5.10 V, %2) → **değişmez**. Düşük empedans (17 k) gürültü bağışıklığını artırır; bölücü akımı 0.3 mA (1.5 mW).
- **Karar: koşullu onay** — koşul: (a) madde 2 yük anahtarı uygulanır ya da (b) `sistem-mimari` SYS-040 için RSS toleransını kabul eder; ikisi de yoksa 13.7 k (ext) kalsın (fark yalnız −0.015 $/stack).
- 9 V FB (R109/R110 100 k/7.15 k): basic çift yok (20 k/1.5 k 8.60 V, 22 k/1.5 k 9.40 V; ikisi de pencerede değil) → değişmez (§10.2 ile uyumlu).

## 5. Madde 4 — B5: 1N4148WT → 1N4148WS (ESC D13…D45, 12 bootstrap diyotu)

| | 1N4148WT (ST/Semtech C27748) | 1N4148WS (CJ C2128, DS A May 2011) |
|---|---|---|
| V_RRM / V_R | 100 / 75 V | 100 / 100 V |
| I_F / I_O | 250 / 125 mA | 300 / 150 mA |
| V_F @1/10/50 mA | 0.715 / 0.855 / 1.0 V | 0.715 / 0.855 / 1.0 V (aynı) |
| t_rr | 4 ns | 4 ns |
| T_J | −65…150 °C | 150 °C |
| R_θJA | 833 K/W (SOD-523) | 625 K/W (SOD-323) |

- Gerilme: 35 V geçici + 7 V − 8 V = 34 V (guc-ip03 §3.2) < 100 V ✓ (SYS-014 ≥ 40 ✓).
- Akım: 57 nC × 24 kHz = 1.4 mA ortalama; tepe şarj darbeleri I_FSM 2 A @1 µs içinde ✓. Kayıp ≈ 1.4 mA × 0.7 V = 1 mW → +0.6 K → **T_J ≈ 96 °C** (kart 95 °C) → 150 °C’ye 54 K pay ✓ (SYS-086 c: ≥ 150 °C ✓, ≥ 15 K pay ✓).
- 125 °C’de sızıntı artar (DS eğrisi, 100 °C’de 30 V’ta ≈ 1–10 µA mertebesi, T) → I_QBS 150 µA’ya eklenir; %100 görevde tutma süresi 6.9 ms → ≥ 6 ms ✓.
- **Karar: onay.** `pcb-muhendisi`: 12 ayak izi SOD-523 → SOD-323 (ESC PCB Rev B zaten yeniden çiziliyor).

## 6. Madde 5 — B6: ESC JW5026 R0 / R02 (/ R01)

Rev B netlistinden: **R0** PWR → U1.4 (EN), **R02** PVDD → FB (üst), **R01** FB → GND (alt, 10 k basic).
- R0 90.9 k → **100 k C25741**: EN eşiği 1.3 V (JW5026 DS s.4) / 1.21 V (SCT2400); EN mutlak 44 / 42 V; EN’e alt direnç yok → davranış aynı ✓.
- FB: basic 100 k üst + 10 k alt → 0.8 × 11 = 8.80 V olurdu (PVDD +0.7 V: AMS1117 kaybı 0.25 → 0.27 W, 1 µF 16 V X7R’ler %55 anma). Bunun yerine **R02 = 20 k (C25765), R01 = 2.2 k (C25879)**, ikisi basic: 0.8 × (1 + 20/2.2) = **8.073 V** (mevcutla aynı).
  - JW5026 (V_FB 0.78–0.82): 0.78 × (1 + 19.8/2.222) = 7.73 V … 0.82 × (1 + 20.2/2.178) = 8.43 V.
  - SCT2400 (madde 7, V_FB 0.79–0.83): 7.83–8.53 V. ≤ 12 V (U0 girişi) ✓.
  - Bölücü akımı 0.36 mA (75 mA yükün %0.5’i) ✓.
- **UVLO payı (JSM6288Q1 4.5 V tip; HL6288Q / FD6288Q 5.0–5.1 V maks):** VCC ≥ 7.73 − 5.1 = **+2.6 V**; V_BS ≥ 7.73 − 1.0 − 5.1 = **+1.6 V** ✓ (DOG-015 ≥ 1 V). 3S düşüm (8.4 V giriş): JW5026 ile PVDD ≈ 7.05 V → V_BS payı 6.05 − 5.1 = +0.95 V (sınırda, guc-ip03 ile aynı); SCT2400 ile ≈ 8.17 V (regülasyonda) → +2.2 V.
- **Karar: koşullu onay** (koşul: R01’in de 2.2 k’ya değişmesi; yalnız R02’yi basic 91 k/100 k yapmak önerilmez — 91 k C4147 extended).

## 7. Madde 6 — FMU 3.3 V regülatörü (U103), küçük kılıf

Yük 240 mA (MCU 102 + flash 25 + sensörler + dış ped 100; README), SYS-042 boyutlandırma 300 mA, %80 akım/ısıl sınıf kuralı. Kart sıcaklığı tasarım değeri 70 °C (SYS-087 ölçümü, 85 °C parçalar ≤ 70 °C).

### 7.1 LDO seçenekleri (θ_JA hesabı)
P = (5.10 − 3.3) × I + 5.1 × I_q.

| Seçenek | θ_JA (DS) | P @240 mA / 300 mA | T_J @70 °C kart | %80 ısıl kuralı (P_maks = (125 − 70)/θ) | Sonuç |
|---|---|---|---|---|---|
| SOT-223 AMS1117 (mevcut) | ≈ 60 K/W (guc-ip03 G9) | 0.46 / 0.57 W | 98 / 104 °C | 0.92 W → %50 / %62 ✓ | Kılıf müşteriye büyük |
| **SOT-89** AMS1117-3.3 (UMW C347256) | 165 K/W (UMW DS s.3, JEDEC) | 0.46 / 0.57 W | **146 / 164 °C ✗** | 0.33 W → %139 ✗ | ✗; bakır döküm + via ile ≈ 80 K/W (T) olursa 107 °C ama doğrulanmamış |
| DFN 2×2 (ör. TLV75733PDRV) | ≈ 70–90 K/W (T, DS) | 0.43 / 0.54 W | 101–111 °C | 0.61–0.79 W → %57–75 | Isıl olarak sınırda ✓; LCSC’de aynı DRV pinli ikinci üretici doğrulanamadı (TECH PUBLIC TPTLV75733PDRVR C55114419 kılıf bilgisi tutarsız) |
| SOT-23-5 LDO (ME6211 vb.) | ≈ 250 K/W | 0.43 W | > 170 °C | ✗ | G9’da zaten ret |

### 7.2 Senkron buck (önerilen)
- **Ana: TI TLV62569DBVR, C141836** (2 A, 1.5 MHz, V_IN 2.5–5.5 V, mutlak 6 V, T_J −40…125 °C, V_FB 0.588–0.612 V; stok 263 537; 0.054 $ @50). Pinler (DS SLVSDG1C §5): **1 EN, 2 GND, 3 SW, 4 VIN, 5 FB**.
- **ALT: Silergy SY8089A1AAC, C479074** (2 A, 1.5 MHz, V_IN 2.5–5.5 V, LX mutlak 6 V, T_J 125 °C / T_A 85 °C, V_FB 0.591–0.609 V; stok 91 268; 0.064 $). Pinler (DS s.1): **1 EN, 2 GND, 3 LX, 4 IN, 5 FB** → birebir.
- Ortak pasifler (KRR-011 kural 4 — ikisinin tablolarının kesişimi): **L 2.2 µH** (TI tablosu 2.2 µH + 10/22 µF; SY tablosu 2.2 µH + 22 µF), **C_OUT 22 µF X7R** (mevcut C113 kodu C5252682, 1206 16 V; 3.3 V’ta ≈ 15 µF etkin, T), **C_IN 10 µF X7R 0805** (mevcut C112 kodu C380347), **FB R_üst 100 k (C25741) / R_alt 22 k (C25768)** → 0.6 × (1 + 100/22) = **3.327 V** (SY önerisi 100 k/22.1 k); en kötü 0.588 × (1 + 99/22.22) = 3.21 V … 0.612 × (1 + 101/21.78) = 3.45 V (STM32/ICM/SPA06/W25Q ≤ 3.6 V ✓). C_FF: TI 6.8 pF, SY 22 pF önerir, ikisi de "isteğe bağlı" → **ped bırak, DNP**. EN → +5V (doğrudan veya 100 k; EN mutlak V_IN + 0.3/0.6 V ✓). V_IN maks 5.27 V (madde 3 en kötü) < 5.5 V ✓.
- Bobin: **Sunlord WPN201610H2R2MT, C97005** (2016, 2.2 µH, I_sat 2.15 A, I_r 1.45 A, 170 mΩ; 0.034 $) / ALT **Murata DFE201612P-2R2M=P2, C79317** (2016, I_sat 2.1 A, 144 mΩ; yükseklik 1.2 mm). Tepe 0.30 + 0.35/2 = 0.48 A (%23) ✓; kayıp 0.3² × 0.17 = 15 mW.
- Kayıp: P_out 0.80 W (240 mA), η ≈ %88 (T, DS eğrisi 5 V → 3.3 V) → **≈ 0.11 W** (LDO 0.46 W yerine) → FMU kart kaybı −0.35 W (SYS-043/087 payına katkı). IC payı ≈ 0.06 W × 188 K/W (en kötü DBV) = +11 K ✓. Akım sınıfı 0.3/2 A = %15 ✓.
- Alan: SOT-23-5 + 2016 bobin + 0805 + 1206 + 2 × 0402 ≈ SOT-223 + 0805 + 1206 kadar; SOT-223’ten küçük (pcb doğrular).

### 7.3 IMU gürültüsü (SYS-042: IMU pininde ≤ 10 mVpp)
- CCM dalgalanma: ΔI = (5.1 − 3.3) × 3.3/(5.1 × 2.2 µH × 1.5 MHz) = 0.35 App; ΔV ≈ ΔI/(8 f C) = 0.35/(8 × 1.5 M × 15 µ) = **2.0 mVpp** + ESL sivrilikleri (≈ 10–20 mV, T).
- IMU dalı R111 10 Ω + 2.2 µF (f_c 7.2 kHz): 1.5 MHz’de 1/207 → 0.01 mVpp ✓.
- **Hafif yük (PSM/PFM):** CCM sınırı ΔI/2 ≈ 0.18 A. Dış 3.3 V pedi boşken yük ≈ 130–150 mA (T) → PSM; patlama frekansı 10–100 kHz (T), dalgalanma 10–20 mVpp (T) → 20 kHz’de RC 1/2.9 → ≈ 7 mVpp (sınırda). **Öneri: R111 10 Ω → 22 Ω (C25092, basic)** → f_c 3.3 kHz, 20 kHz’de 1/6 → ≈ 3 mVpp ✓; ICM-42688 ≈ 1 mA → 22 mV düşüm (VDD 1.71–3.6 V ✓).
- MCU VDDA ferrit + kondansatör mevcut ✓; analog OSD 5 V’tan ✓.
- **Koşul (DOG-042):** prototipte IMU VDD pininde dalgalanma (20 MHz bant) ve motor kapalı jiroskop gürültü tabanı LDO’lu kartla karşılaştırılır.
- Maliyet: AMS1117 C6186 (basic, 0.149 $) → IC 0.054 + L 0.034 + 2 direnç 0.002 = −0.06 $; dizgi +2 extended tür (+0.031 $) → **≈ −0.03 $/stack** (bugünkü BOM’a göre; §10 A2 varsayımına göre +0.07 $).

## 8. Madde 7 — ESC JW5026 muadili (U1, stok riski RSK-019)

Ölçütler: V_IN mutlak ≥ 40 V (SYS-014: 35 V + 5 V), T_J çalışma ≥ 125 °C (SYS-086 d), stok ≥ 200, SOT-23-6 **1 BST, 2 GND, 3 FB, 4 EN, 5 VIN, 6 SW** (JW5026 DS s.2), V_FB ≈ 0.8 V (aynı bölücü), L00 10 µH ile uyum.

| Aday | Üretici | Pin | V_IN mutlak / çalışma | T_J | I_O | f_SW | V_FB | Stok | 100’de $ | Sonuç |
|---|---|---|---|---|---|---|---|---|---|---|
| JW5026SOTB (mevcut) C185109 | JoulWatt | ✓ | 44 / 40 V | 125 | 1 A | 1.1 MHz (0.75–1.25) | 0.80 ±%2.5 | **332** | 0.267 | ALT |
| **SCT2400TVBR C2693819** | **SCT** | **✓** (DS s.1) | **42 / 40 V** | **−40…125** (mutlak 150) | 0.6 A | 2 MHz (1.6–2.4) | **0.81 ±%2.5 (tüm T_J)** | **8 410** | **0.245** | **ANA** |
| JW5018SOTB C3040676 | JoulWatt | ✓ | 44 / 40 V | 125 | 0.6 A | 2 MHz | 0.80 ±%3 | 2 193 | 0.223 | ALT2 |
| SGM61410XN6G(TOKMAS) C7525409 | Tokmas | ✓ | 42 V | 125 | 0.6 A | 2 MHz | 0.81 | 2 879 | 0.294 | DS SCT2400 kopyası; SGMICRO orijinali (C699689) 0.8 V, 0.85–1.5 MHz, 1.57 $ → klon, önerilmez |
| LMR51410YFDBVR C32347484 | TI | ✓ (CB-GND-FB-EN-VIN-SW) | 45 / 42 V | 150 | 1 A | 1.1 MHz | 0.80 ±%1.5 | 998 | 0.85 | Teknik en iyi, **+0.58 $** → yedek |
| ME3121AM6G / ICW3126AM6G | Microne / ICW | ✓ | 40 V | T_A 85 / 150 | 1 A | 1 MHz | **0.60** | 20 230 / 2 959 | 0.23 / 0.32 | ✗ V_FB farklı (bölücü değişir), ME3121 T_A 85 °C |
| TP6841, LMR14010A klonları (MSKSEMI) | — | ✓ | 40 V | 125 | 0.8 A | 0.8 MHz | 0.75 | — | — | ✗ asenkron (dış Schottky gerekir) |
| TPS560430, LMR54410 | TI | ✓ | 36–38 V | 125 | | | | | | ✗ < 40 V |

**SCT2400 ↔ JW5026 aynı ayak izi ve pasiflerle (KRR-011 kural 4):**
- FB 20 k / 2.2 k → 8.07 V (JW) / 8.17 V (SCT) (madde 5). SCT DS alt direnç için 20 k önerir (verim); 2.2 k ile bölücü akımı 0.36 mA, sorun değil.
- L00 **10 µH SWPA3015S100MT** (I_sat 0.92 A): SCT2400 @2 MHz, 35 V: ΔI = 8.17 × (35 − 8.17)/(35 × 10 µ × 2 M) = 0.31 App → tepe 0.075 + 0.16 = **0.23 A** (I_sat %25, HS akım sınırı 0.7 A min) ✓; min. açık süre 8.17/35/2 MHz = 117 ns ≥ 80 ns ✓. DS 5 V için 15 µH önerir (dalgalanma %20–30 × 0.6 A); 75 mA yükte 10 µH yeterli. JW5026 1.1 MHz ile 10 µH guc-ip03 §7’de onaylı.
- Çıkış: C03 10 µF 16 V X7R 0805 (8 V’ta ≈ 4–5 µF, T) + 4 × 1 µF + 100 nF. SCT örnekleri 22 µF kullanıyor → **öneri: C03’e paralel ikinci 10 µF (C380347)** (iki parça için de kararlılık payı; +0.025 $/stack).
- EN: R0 100 k → PWR; SCT EN V_IN’e bağlanabilir (DS), iç UVLO 4.3 V (JW5026 4.0–4.6 V).
- Düşüm (3S, 8.4 V): SCT2400 BST tazelemeli yüksek görev (DS "Bootstrap Voltage Regulator") → PVDD ≈ min(8.17, 8.4 − 0.075 × 0.82 Ω) = 8.17 V ✓ (JW5026’da 7.05 V).
- Isı: P_out 0.6 W, η ≈ %83 (25 V → 8 V, 2 MHz, T) → 0.12 W × 89 K/W (DS) = +11 K → 95 °C kartta **T_J ≈ 106 °C** (125’e 19 K pay ✓; guc-ip03 JW5026 tahmini 101 °C).
- Maliyet: 0.267 → 0.245 $ = −0.02 $/stack (+0.025 $ ikinci 10 µF önerilirse).
- **Koşul (DOG-111):** prototipte bir ESC SCT2400, bir ESC JW5026 ile dizilir; PVDD dalgalanma ve 0 → 100 mA yük basamağı her ikisinde.

## 9. Madde 8 — Güç parçalarının muadil (ALT) uygunluğu (SYS-095, KRR-011)

| Kart / ref | Ana (LCSC) | Drop-in ALT (LCSC) | Kanıt / hesap | Karar |
|---|---|---|---|---|
| ESC M1aH…M4cL (24) | BLP016N04LC-Q, Belling, C49328363 (stok 3 903 < 4 800 → A1 peşin alım) | **NTMFS5C430NLT1G, onsemi, C194661** (stok 173 463) | İkisi DFN5×6, 1–3 S / 4 G / 5–8 D; 40 V; T_J 175 °C; R_DS(on) 1.25 / 1.4 mΩ @10 V; NTMFS Q_g 82 nC @10 V (≈ 51 nC @7.2 V) — guc-ip03 bootstrap (ΔV 0.095 V) ve kayıp hesapları zaten NTMFS ile yapıldı ✓. Ayak izi: SO-8FL ↔ PDFN5×6 ped kesişimi `pcb-muhendisi` | **✓ drop-in** |
| ESC U12…U42 (4) | JSM6288Q1, JSMSEMI, C52196409 (UVLO 4.5/4.3 V tip) | **HL6288Q, HL (iseachip), C50331902** (stok 6 867, 0.286 $) | QFN24 pinleri FD6288Q ile aynı (DS §5: LIN 1–3, VCC 4, COM 6, LO1–3 = 11/10/9, VS 18/15/12, HO 19/16/13, VB 20/17/14, HIN 22–24); VCC/VBS UVLO+ **4.2/4.7/5.1 V** (min/tip/maks), ölü zaman 100/200/300 ns, aynı fazlı + kilitleme (DS §8.3), T_A −40…125 °C. PVDD 7.73 V’ta VCC payı +2.6 V, V_BS +1.6 V ✓ | **✓ drop-in** (kılıf ölçüsü/EP `pcb-muhendisi`) |
| — | — | FD6288Q, Fortior, C328453 | UVLO 4.6 (4.2–5.0) V → 8 V PVDD’de **sorun yok** (+2.7 V / +1.7 V). Ama **LCSC/JLC stok 0** → ALT olarak tedarik edilemez | Elektriksel ✓, tedarik ✗ → ALT2 |
| — | — | NSG6288Q, WXNSIC, C54570588 (stok 4 022) | UVLO 4.5 tip / 5.0 maks, 200 ns, aynı pinler (DS Tablo 7-1), dahili bootstrap diyotu (dıştaki 1N4148WS ile paralel, sakıncasız) | ALT3 |
| **UYARI** | — | **JSM6288Q C19077370** ve **JSMSEMI "FD6288Q" C7466367** (V_CC 8–20 V) | UVLO ≈ 7 V (guc-ip03 §3.1) → yüksek taraf sürülemez | **ALT olarak yazılmamalı** |
| ESC D00 | SMDJ24CA, DOWO, C284061 (stok 2 444) | **SMDJ24CA-AT/TR13, Brightking, C523477** (stok 2 981) | SMC, 3 kW, V_RWM 24 V, V_BR ≥ 26.7 V, V_C 38.9 V @77.1 A, −55…150 °C; guc-ip03 R_d hesabı Brightking DS’den ✓. Diğer: BORN C511913, Liown C2990247 | **✓** |
| FMU D102 | SMBJ24CA, Brightking, C78416 | **SMBJ24CA, Littelfuse, C83268** (stok 25 179) | SMB, 600 W, V_C 38.9 V @15.5 A < 40 V (SYS-044) ✓, −65…150 °C. Not: Leiditech C384906 T_J 125 °C → yazılmasın | **✓** |
| FMU U101, U102 | SY8303AAIC, Silergy, C2937216 | **SY8303AIC, Silergy, C97054** (stok 114 428, 0.365 $) | Aynı pin (FB, FS, GND, GND, IN, LX, BS, EN), V_REF 0.591–0.609, F_SW = 105/R_FS, 40 V mutlak, θ_JA 60 K/W (DS AN_SY8303 s.1–3). BS kondansatörü AIC 10 nF, AAIC 100 nF önerir → 100 nF ikisinde de çalışır (T) | **İstisna: tek üretici** (TSOT-23-8 FS pinli 40 V 3 A başka üretici yok); önlem: ALT farklı sipariş kodu, stok izleme. 40 V mutlak = SYS-044 sınırı (pay 0) |
| FMU Q101 (+ yeni Q102) | AO3401A, AOS, C15127 (basic) | **AO3401A, UMW, C347476** (stok 814 822) | SOT-23 1 G / 2 S / 3 D, −30 V, 50 mΩ @10 V, −55…150 °C | **✓** |
| ESC R00 shunt | HoLRS3920-10W-0.1mR-1%, Milliohm, C55113241 (±100 ppm/K, ped 2.7 × 6.2 mm, c = 11 mm) | **EB390M10PFFWT, MHCH, C55591762** (EB3921, 0.1 mΩ, 15 W @70 °C, stok 1 992, 0.43 $) | 10.0 × 5.2 mm; **"mikro elektrot" sürümü** ped 11 / 2.7 / 6.2 mm = HoLRS önerisiyle aynı (DS s.3); TCR **±300 ppm/K** (MnSn) → 60 K öz ısınmada %1.8 (HoLRS %0.6) → 200 A’da hata 4.6 → ≈ 7 A < 10 A ✓, düşük akımda etkisiz | **Koşullu ALT**: sipariş kodunun mikro elektrot (A = 2.0 mm) olduğu üreticiden teyit; aksi hâlde istisna. HoLRS3920-6W-0.1mR C55113240 (aynı üretici, 6 W) **✗**: 220 A’da 4.8 W = %80 > %70 |
| ESC L00 | SWPA3015S100MT, Sunlord, C45403 | **FNR3015S100MT, cjiang, C167757** (stok 62 224) | 3 × 3 mm, 10 µH, 325 mΩ, I_sat 0.92 A, −40…125 °C öz ısınma dahil (DS s.1) ✓ | **✓** |
| FMU L101 | SWPA6045S6R8MT, Sunlord, C57254 | **FNR6045S6R8MT, cjiang, C168072** (stok 3 103) | 6 × 6, 6.8 µH, I_sat 4.3 A, I_r 3.3 A, 40 mΩ; tepe 2.6 A (%60) ✓ | **✓** |
| FMU L102 | SWPA5040S100MT, Sunlord, C84608 | **FNR5040S100MT, cjiang, C167967** (stok 50 888) | 5 × 5, 10 µH, 83 mΩ, 2.35 / 2.7 A; tepe 2.09 A = %77 (I_sat 2.7 A kabulüyle; 2.35 A ise %89 ✗) → DS’den I_sat teyit | **Koşullu ✓** |
| FMU L103 (yeni, 3.3 V buck) | WPN201610H2R2MT, Sunlord, C97005 | **DFE201612P-2R2M=P2, Murata, C79317** | §7.2 | **✓** |
| FMU U103 (yeni) | TLV62569DBVR, TI, C141836 | **SY8089A1AAC, Silergy, C479074** | §7.2 | **✓** |
| ESC U1 | SCT2400TVBR, SCT, C2693819 | **JW5026SOTB#TRPBF C185109**; ALT2 JW5018SOTB C3040676 | §8 | **✓** |
| ESC U2 | RSA240CXK, Runic, C54300729 | **INA240A3DR, TI, C2060584** | §2.4 | **✓** (koşul DOG-019) |
| ESC U0 (kapsam dışı, bilgi) | AMS1117-3.3S UMW C347256 (SOT-89) | aday: TECH PUBLIC AMS1117-3.3S C46473005 (−40…125 °C T_J, V_IN maks 12 V ≥ PVDD 8.53 ✓) | SOT-89 pin sırası iki DS’den doğrulanmalı | bom-tedarik |

## 10. `sematik-muhendisi`’ne uygulanacak parça listesi (ref → LCSC, ALT LCSC)

| Kart | Ref | Değişiklik (ana → LCSC) | ALT LCSC | Koşul / not |
|---|---|---|---|---|
| ESC | U2 | INA240A3DR → **RSA240CXK C54300729** (SOIC-8, ayak izi ve pinler aynı) | **C2060584** (INA240A3DR) | B2 (INA281B2) **uygulanmaz**; `ibata_scale 100` aynı |
| ESC | U1 | JW5026 → **SCT2400TVBR C2693819** | **C185109** (JW5026), ALT2 **C3040676** (JW5018) | — |
| ESC | R0 | 90.9 k → **100 k C25741** | genel | B6 |
| ESC | R02 | 90.9 k → **20 k C25765** | genel | B6 |
| ESC | R01 | 10 k → **2.2 k C25879** | genel | B6 (R02 ile birlikte) |
| ESC | C03b (yeni, öneri) | **10 µF 16 V X7R 0805 C380347**, PVDD–GND, U1 çıkışına yakın | genel | SCT2400 kararlılık payı |
| ESC | D13…D45 (12) | C27748 → **1N4148WS C2128** (SOD-323) | başka üretici (bom-tedarik) | B5 |
| ESC | U12…U42 | JSM6288Q1 C52196409 (aynı) | **C50331902** (HL6288Q); ALT2 C328453 (FD6288Q, stok 0) | **C19077370 / C7466367 ALT olarak yazılmaz** |
| ESC | M1aH…M4cL | C49328363 (aynı) | **C194661** (NTMFS5C430NLT1G) | mevcut |
| ESC | D00 | C284061 (aynı) | **C523477** (Brightking SMDJ24CA-AT) | — |
| ESC | R00 | C55113241 (aynı) | **C55591762** (MHCH EB3921 0.1 mΩ) | mikro elektrot teyidi; olmazsa istisna |
| ESC | L00 | C45403 (aynı) | **C167757** (FNR3015S100MT) | — |
| FMU | D501 | C19268151 → **B5819W SL C8598** (SOD-123) | C19268151 (PMEG3020EH, SOD-123F) | B3; ortak ped |
| FMU | Q102 (yeni) | **AO3401A C15127**: D = +5V_BUCK (U101 çıkışı, C107/C108 tarafı), S = +5V rayı, G → R_a | **C347476** (UMW) | USB sızıntı çözümü (§3.2) |
| FMU | Q103 (yeni) | **MMBT3904 C20526**: C = Q102.G, E = GND, B → R_b | **C81464** (onsemi MMBT3904LT1G) | §3.2 |
| FMU | R_a, R_b (yeni) | **100 k C25741** ×2: R_a Q102 G–S, R_b VIN → Q103 B | genel | §3.2 |
| FMU | R104 | 100 k → **15 k C25756** | genel | B4 (ref R101 değil) |
| FMU | R105 | 13.7 k → **2 k C4109** | genel | B4 |
| FMU | U103 | AMS1117-3.3 SOT-223 → **TLV62569DBVR C141836** (SOT-23-5) | **C479074** (SY8089A1AAC) | madde 6; EN → +5V |
| FMU | L103 (yeni) | **2.2 µH WPN201610H2R2MT C97005** (2016) | **C79317** (Murata DFE201612P) | — |
| FMU | R_FB3V3 üst/alt (yeni) | **100 k C25741 / 22 k C25768** | genel | 3.327 V; C_FF pedi DNP |
| FMU | C112, C113 | aynı kodlar (10 µF 0805 giriş, 22 µF 1206 çıkış) | — | buck C_IN / C_OUT |
| FMU | R111 | 10 Ω → **22 Ω C25092** | genel | IMU süzgeci (madde 6.3) |
| FMU | U101, U102 | C2937216 (aynı) | **C97054** (SY8303AIC) | istisna listesine: tek üretici |
| FMU | Q101 | C15127 (aynı) | **C347476** | — |
| FMU | D102 | C78416 (aynı) | **C83268** (Littelfuse) | — |
| FMU | L101 | C57254 (aynı) | **C168072** (FNR6045S6R8MT) | — |
| FMU | L102 | C84608 (aynı) | **C167967** (FNR5040S100MT) | I_sat teyidi |

`pcb-muhendisi`: ESC D13…D45 SOD-323; ESC U2 SOIC-8 aynı (Kelvin düzeni aynen); R00 ayak izi EB3921 mikro elektrot ile kesişim; HL6288Q ↔ JSM6288Q1 QFN24 EP; FMU D501 SOD-123/123F ortak ped; FMU U103 SOT-23-5 + 2016 bobin (SW düğümü kısa, FB yolu SW’den uzak — SY DS düzen notu); Q102 5 V yolunda 2 A için bakır.

## 11. SYS-095 istisna listesi (bu inceleme kapsamı)

| Parça | Neden | Önlem | Risk |
|---|---|---|---|
| SY8303A (FMU U101/U102) | TSOT-23-8 FS pinli 40 V / 3 A başka üretici yok; ALT aynı üreticinin SY8303AIC kodu | Stok izleme (12 313 + 114 428), 8S varyantı için ayrı ayak izi yeri (SYS-046) | Orta (tek üretici); 40 V mutlak = SYS-044 sınırı |
| HoLRS3920 0.1 mΩ (ESC R00) | Aynı ped ve 10 W sınıfında tek ikinci üretici (MHCH EB3921) TCR ±300 ppm ve elektrot sürümü teyitsiz | Üretici teyidi; olmazsa 2 500 adet peşin (stok 3 830) | Düşük–orta |
| (B2 uygulanırsa) INA281B2 | SOT-23-5 B dizilimli ×50 ikinci üretici yok | — | Ret gerekçesi |

## 12. Belgelerde düzeltilmesi gerekenler (bilgi; dosyalara dokunulmadı)

1. `docs/bom-maliyet.md` §10.2 B2 ve CSV: "×50 … `ibata_scale` 100 → 200" → INA281B2 ile **50** olurdu (200 = 20 mV/A). B2 reddedildiği için RSA240C/INA240A3 ile **100** kalır.
2. CSV B4 ve §10.7: "R101/R105" → **R104/R105**.
3. §10.5 JW5026 stok 132 → 2026-11-12’de **332** (yine RSK-019; madde 7 ile kapanır).
4. CSV B3 notu "T_J 125 (tipik)" → B5819W DS’de T_J **125 °C maks** (tipik değil); KRR-008 FMU tablosu diyot satırı (≥ 150 °C) SYS-087 ile çelişiyor.
5. `boards/fmu/README.md` "PMEG3020 … yalnız USB’de MCU, sensörler, OSD ve 5 V çalışır" → OSD (AT7456E ≥ 4.75 V) USB’de garanti değil; LDO’yla V_BUS < 4.95 V’ta 3.3 V düşer (madde 6 buck’ı giderir).
6. `lib/datasheet/`’te INA281, RSA240, JW5026, SCT2400, SY8303A, TLV62569, SY8089A1, B5819W, 1N4148WS, HL6288Q, EB3921, FNR yok → `bom-tedarik` eklesin (kaynaklar §13).

## 13. Veri sayfası kaynakları (yalnız scratchpad’e indirildi)

TI: `ti.com/lit/ds/symlink/ina281.pdf` (SBOSA29A), `tlv62569.pdf` (SLVSDG1C), `lmr51410.pdf`. LCSC `https://datasheet.lcsc.com/datasheet/pdf/<ad>.pdf`: RSA240 `cfd23beb0bf5a5e792cccc39733921bb`, CSA220 `e1ebad0617d2867122b84ee204fbf1ca`, B5819W `4ac2c059be7c462694ab0715ce987a85`, PMEG3020EH (TECH PUBLIC, görüntü PDF) `e756687f14dbf46d5677223c86053278`, 1N4148WS `460cf88f750c4519b4ed435068ee729e`, 1N4148WT `d78fb31904624a51a63f8a5d98d2dc04`, SY8303A(A) `65ea9869e3fbc8e85f9b73c0af83e582`, SY8303AIC `e1a61b84c1934bfd84df3c719ade0020`, SY8089A1 `0ca32da5d5c125881791fee9f2de17c1`, JW5026 `f83872ed2237628ee0705043f9e45a8d`, JW5018 `3fe447198e6a66ca55c2bc13e6469ce2`, SCT2400 `6d2d30a1729d799dffa8acd75e20e625`, SGM61410 (Tokmas) `dab83bc08b520fa945f71e6f6b4e83c2`, ME3121 `f7205801dddb5cd33ddcb77e5edbe32f`, ICW3126 `9fbad1209882756abe0790fa60743e70`, HL6288Q `e3876969d06524bf8e37e97ec233f633`, EG6288 `98e96e3fe2038dd1844893cf12db37df`, NSG6288Q `8060c9801d4561951f337f70b53ea0b4`, MHCH EB3921 (görüntü PDF) `8dfb4d5661ef020a1de8fafba3129e51`, FNR serisi `a0b12ba9dfe6b9e66b6bb852b7c71c03`. `lib/datasheet/`: HoLRS3920, BLP016, NTMFS5C430NL, FD6288Q, JSM6288Q1, SMDJ24CA, SWPA, INA240A3.

## 14. Maliyet etkisi (100 set, $/stack, §10 A + B planına göre; `bom-tedarik` yeniden hesaplamalı)

| Kalem | Δ |
|---|---|
| B2 yerine RSA240C (−1.19 yerine §10’da −0.52 sayılmıştı) | **−0.67** |
| B3, B4, B5, B6 (§10 değerleri) | değişmez (toplam −0.145) |
| Madde 6 buck (A2 −0.095 geçersiz; bugünkü BOM’a göre −0.03) | +0.065 |
| Madde 2 yük anahtarı | +0.06 |
| Madde 7 SCT2400 (+ ikinci 10 µF) | −0.02 (+0.025) |
| **Toplam** | **≈ −0.54** → §10 A + B 31.35 $ → **≈ 30.8 $** (STM32 JLC fiyatıyla); DT-005 APM32 ile ≈ 29.4 $ |

## 15. Güç açısından kapanabilir mi

**Evet, koşullu:** B3, B4, B5, B6 ve madde 6–8 değişiklikleri §10 tablosuna göre şematiğe işlenirse; B2 **INA281B2 olarak uygulanmaz**, yerine RSA240CXK + ALT INA240A3DR. Açık koşullar: (1) DOG-019 — RSA240 ofseti −10/25/+50 °C’de ≤ 50 µV; (2) DOG-042 — buck’lı 3.3 V’ta IMU pini ≤ 10 mVpp; (3) DOG-111 — SCT2400 ve JW5026 ile birer ESC; (4) B4 için SYS-040 RSS kabulü veya yük anahtarı; (5) shunt ALT elektrot sürümü ve FNR5040 I_sat teyidi; (6) SY8303 istisnasının müşteriye bildirilmesi (KRR-011 kural 7).
