# İP-03 — Ü-öncesi güç analizleri (guc-elektronigi)

> **Tarih:** 2026-11-10. **Hazırlayan:** `guc-elektronigi` (yalnız inceleme; başka proje dosyası değiştirilmedi). **Kapsam:** SYS-010, 011, 013…016, 020, 021, 040…045, 070, 073, 074, 083; DOG-004, -006, -009, -011, -013, -015, -017, -019, -037, -039, -041, -043, -045, -047, -067, -072, -074, -083 (analiz kısımları).
> **Girdi:** `docs/inceleme.md` §2, §4; `docs/bom-maliyet.md` (S1/S1b); `docs/gereksinimler/{sistem,dogrulama,proje}.md`; `test/analiz/{bolucu,shunt}.py`; `test/sonuc/DOG-0{13,15,17,19,21,37}.md`; Altium şematikleri (`boards/*/altium/*.SchDoc`).
> **Bağlantı (netlist) çıkarımı:** `tools/altium_sch_dump.py` yalnız parça listesi verdiği için SchDoc kayıtlarından (pin uç noktası + tel + ağ etiketi) basit bir netlist çıkarıldı (geçici betik, scratchpad; repoya konmadı). Bulduğu bağlantılar aşağıda “netlist” diye işaretli; **şematik görselle `sematik-muhendisi` teyit etmeli**.
> **Hesaplar:** Python betikleri scratchpad’de (`mos.py` kayıp, `isil.py`/`isil2.py`/`ozet.py` ısıl model, `akim.py` akım ölçümü). İstenirse `test-muhendisi` `test/analiz/` altına alabilir.
> **Fiyatlar:** JLC parça arayüzü, 2026-11-10, 100 set için gereken adet kademesinde (ör. 24 MOSFET → 2400 adet), USD. S1b referansı `docs/bom-maliyet.md`: **27.38 $/stack**.

## 0. Özet (yönetici için)

| Konu | Karar / bulgu | Maliyet (100 set, $/stack, S1b’ye göre) |
|---|---|---|
| **MOSFET** | 30 V parçalar (ME7170, AON6354, **AON6354-HXY**) SYS-014’ü (mutlak sınır ≥ 35 + 5 = 40 V) karşılamaz. HXY ayrıca Crss 340 pF (yanlış iletime girme riski) ve Qrr 324 nC. **Öneri: 40 V BLP016N04LC-Q (Belling, C49328363, 1.6 mΩ maks)**, ikinci kaynak **NTMFS5C430NLT1G (onsemi, C194661, 1.4 mΩ maks, stok 173 k)**, ikisi de DFN5×6 standart pin dizilimi | +1.64 (BLP) / +2.96 (onsemi) |
| **SYS-010/011 (4 × 55 A sürekli / 4 × 70 A 10 s)** | **Hiçbir aday karşılamıyor.** 41 × 48 mm kart, 5 m/s hava ile ≈ 35 W ısı atabiliyor (tahmin, ±%50). 4 × 55 A’da en iyi 40 V FET ile kart kaybı ≈ 61 W (24 kHz). Ulaşılabilir: **4 × 34 A (anahtarlamalı) / 4 × 41 A (tam gaz) sürekli, tek kanal 62 A, 4 × 55 A 10 s**. Akım sınıfı tanımı değişmeli (KRR önerisi, müşteri kararı) | — |
| **Kapı sürücü** | Stoklu JSM6288Q (S1/S1b) **FD6288Q ile pin uyumlu ama elektriksel olarak uyumsuz**: UVLO 6.4–7.7 V, PVDD 8.07 V’ta yüksek taraf UVLO’ya girer. **JSM6288Q1 (C52196409, UVLO 4.5 V)** gerekli | +0.30 |
| **Akım ölçümü** | INA199**C1 kazancı 50** (200 değil): mevcut tam ölçek ≈ 124 A (inceleme E1’deki 32 A yanlış), 220 A’da shunt 24 W, V_CM 26 V < 26.1 V. **Öneri: 1 × 0.1 mΩ 3920 10 W (C55113241) + INA240A3DR (C2060584), yüksek taraf, 10 mV/A, Betaflight `ibata_scale` 100**; tam ölçek ≥ 297 A, kayıp 4.8 W | +1.45 (bütçe seçeneği INA186A3: +0.23, SYS-021 gevşer) |
| **TVS / bulk** | SMDJ28CA 35 V altında kıstıramaz (VBR maks 34.4 V). **SMDJ24CA (C284061)**; bulk **15 × 10 µF 50 V X7R 1206 (C89632)**; **set kondansatörü (≥ 470 µF, ESR ≤ 50 mΩ) zorunlu** — olmadan pil takmada tepe ≈ 42 V | −0.31 |
| **FMU buck** | TPS54202 VIN mutlak 30 V < 35 V (SYS-044). **SY8303AAIC (C2937216, 40 V, 3 A)** ×2; geri besleme dirençleri aynen kalır (V_REF 0.6 V) | +0.43 |
| Diğer zorunlu düzeltmeler | FMU 3.3 V LDO (AMS1117-3.3 SOT-223, basic), BEC bobinleri, ESC L00, kondansatörler, FMU giriş TVS | +0.29 |
| **Toplam** | Önerilen (BLP016 + INA240A3): **≈ 31.2 $/stack**; ekonomik (ND2R8TG + INA186A3 + X5R bulk): ≈ 29.3 $/stack. **DT-001 (≤ 28 $) SYS-014 uyumlu tasarımla tutmuyor** | +3.8 / +1.9 |

**Ayrıca kritik (netlist):** FMU ters kutup P-MOS’u (U9 AO3401A) ters bağlı görünüyor: kaynak pil tarafında, savak yük tarafında. Ters kutupta gövde diyodu iletir, koruma yok; düz kutupta açılışta V_GS ≈ −26 V (> ±12 V). **FMU VBAT bölücüsü gerçekte R92 10 k + R93 7.15 k / R94 2.2 k (8.80:1, tam ölçek 29.0 V)**; DOG-021 R95 100 k (aslında U9 kapı direnci) ile hesaplanmış.

**İP-03 güç açısından kapanabilir mi:** **Hayır.** Analizler tamamlandı ama 9 kritik bulgu açık, 4 karar müşteri onayı istiyor (§13–14).

---

## 1. Veri sayfaları (kaynak)

`lib/datasheet/`’te yalnız FD6288Q, JSM6288Q, EFM8BB21, STM32F405, AP2210 vardı. Diğerleri LCSC ürün arayüzündeki PDF bağlantılarından indirildi (yalnız scratchpad’e). Kaynak bağlantıları `https://datasheet.lcsc.com/datasheet/pdf/<ad>.pdf`:

| Parça | LCSC | Kaynak (pdf adı) | Kullanılan sayfa |
|---|---|---|---|
| ME7170 (Matsuki) | C2841360 | 662a8f3f3f046c76a793678d5e137be8 | s.1–2 |
| AON6354 (AOS) | C404363 | 27ab13d2c4ecf7483e03524c796e0587 | s.1–2 |
| AON6354-HXY | C22367225 | 67bcb2f62ad06e8f4e7dc3ad8f71d000 | s.1–2 |
| SHYG015N04LS1C2 (JSMSEMI) | C49206918 | 8c9bcf0ca09cce9592faa362a5ce66ac (görüntü PDF) | s.1–3 |
| HYG015N04LS1C2 (HUAYI) | C2874970 | 90199d1734bfa7d3e70d8ba70436f1ea | s.2–3 |
| NTMFS5C430NL (onsemi) | C194661 | 2a2a6d89c0f0698c54cd937bf00b2745 | s.1–2 |
| BLP016N04LC-Q (Belling) | C49328363 | 60e9b7bb6d64f081d184b353ffc14825 | s.2–3 |
| ND2R8TG (DOINGTER) | C54300813 | 56d7643d2cb4e5271710ba62bc6cda99 | s.2 |
| MGC021N04L (Megain) | C49242745 | ed6e2576d368308e2b278f9b55f6ffef | s.1–2 |
| KNY3404D (KIA) | C7465103 | 24aad627d56bb54014d1705d161d53ea | s.2–3 |
| JSM6288Q1 (JSMSEMI) | C52196409 | 8e66a7cf2679ad9374949075990da53d (görüntü PDF) | s.1, 3–8 |
| JW5026 (JoulWatt) | C185109 | f83872ed2237628ee0705043f9e45a8d | s.2, 4 |
| INA199 (TI) | C2155860 | bea3986d333415d765e3ddd617d4a962 | s.4, 5, 7 |
| INA186 (TI, Çince) | C2058245 | 41988dc4b496b8350137e0236fc4339f | s.4–5 |
| INA240 (TI SBOS662C) | C2060584 | ti.com/lit/ds/symlink/ina240.pdf (LCSC PDF yalnız seçim kılavuzu) | s.4–5 |
| AMS1117 (UMW) | C347256 | 40abec897f3661104e2a4d1ebd8e7463 | s.3, 5 |
| SMDJ (Brightking) | C310121 | 8f036c281617a08b931924e42f4520e4 | s.3 |
| TPS54202 (TI) | C191884 | d157217c6eb23490850aa6db6ab39179 | s.4, 5, 11 |
| SY8303A (Silergy) | C2937216 | 65ea9869e3fbc8e85f9b73c0af83e582 | s.3–4 |
| LMR51430 (TI) | C5185863 | 2abe6d28001db846b928dba24a5e98c2 | s.1, 4 |
| ME6211 (Microne) | C82942 | d15331d096a848ac81a26b001a32d4e3 | s.5, 8 |
| AO3401A (AOS) | C15127 | fee353dd1e9e0bc90b295f14f381aa4c | s.1 |
| 1N4148WT | C27748 | d78fb31904624a51a63f8a5d98d2dc04 | s.1 |
| NLCV32T-6R8M | C250230 | 309c3759b491b08564f62f5d5572e057 | (LCSC parametresi 530 mA) |
| CFS12V3T5R0 (F9) | C163128 | 74939aaca6654e47bc79adb0bc0bd0a1 | s.3 |
| RLM25FEER001 (shunt) | C316227 | 8c65958124b16053d25433479b831d3f | (LCSC: 2 W, ±275 ppm/K) |

**Öneri (`bom-tedarik`, İP-02):** yukarıdaki PDF’ler `lib/datasheet/`’e eklenmeli (RSK-002 kapanır).

## 2. MOSFET seçimi (SYS-010, 011, 013, 014; DOG-004, -006, -009, -083)

### 2.1 Gerilim payı
- Sürekli en yüksek: 6S LiHV 26.1 V. Geçici tepe (SYS-014): 35 V; kural: BAT hattındaki her parçanın mutlak sınırı ≥ 35 + 5 = **40 V**.
- 30 V parçalar: V_DS 30 V < 40 V → **SYS-014’ü karşılamaz**. AON6354’ün “V_SPIKE 36 V, 10 µs” değeri (DS s.1) yalnız 1 V pay verir. 26.1 V’ta pay 3.9 V (%13), olağan 6S tasarım payının (≥ %25) altında.
- 40 V parçalar: 40 ≥ 40 ✓ (pay tam sınırda; TVS kıstırması ≤ 35 V olmalı, §6).

### 2.2 Aday verileri (veri sayfası; “T” = tahmin)

| Aday | V_DS | R_DS(on) 10 V maks / tip (mΩ) | 4.5 V maks | Q_g 10 V / Q_gd (nC) | Crss / Ciss (pF) | Qrr (nC) | RθJC (K/W) | T_j maks | JLC $ @2400 | Stok |
|---|---|---|---|---|---|---|---|---|---|---|
| ME7170 (şematik) | 30 | 2.6 / 2.4 | 3.9 | 86 / 12 | 418 / 5406 | — | 2.2 | 150 | 0.220 | 165 ✗ |
| AON6354 (AOS) | 30 | 3.3 / 2.75 | 5.2 | 20 / 3.5 | 55 / 1330 | 17 | 3.5 | 150 | 0.149 | 8 879 |
| **AON6354-HXY (S1b)** | 30 | 3.3 / 2.6 | 5.0 | 24@4.5 V / 13 | **340** / 2218 | **324** | 1.3 | 150 | 0.114 | 4 425 |
| SHYG015N04LS1C2 | 40 | 1.4 / 1.1 | 2.6 | 87 / 15 | 65 / 5500 | 53 | 1.1 | 150 | 0.278 | 4 697 |
| HYG015N04LS1C2 | 40 | 1.7 / 1.4 | 2.4 | 59 / 8.5 | 33 / 4050 | 43 | 2.0 | 175 | 0.299 | 11 247 |
| **NTMFS5C430NL** | 40 | **1.4 / 1.2** | 2.2 | 70 / 9 | 72 / 4300 | 80 | 1.4 | 175 | 0.237 | **173 523** |
| **BLP016N04LC-Q** | 40 | **1.6 / 1.25** | 2.4 | 61 / 8.2 | 65 / — | 80 | 1.3 | 175 | **0.182** | 3 963 |
| ND2R8TG | 40 | 3.0 / 2.5 | — (4.0 T) | 36 / 5.6 | 46 / 1980 | 14 | 1.47 | 150 | 0.174 | 4 957 |
| MGC021N04L | 40 | 2.8 / 2.1 | 3.5 | 20 (tutarsız, Ciss 6150) / 11 | 372 / 6150 | — | 1.5 | 150 | 0.122 | 3 604 |
| KNY3404D | 40 | 5.5 / 5.2 | 10 | 58 / — | 225 / 2680 | — | 1.95 | 150 | 0.088 | 3 195 |

Notlar: HXY veri sayfasında Q_g 24 nC “V_GS = 4.5 V” (s.2), LCSC parametresinde “@15 V”; Ciss 2218 pF ile Q_gd 13 nC tutarsız değil ama Crss 340 pF ve Qrr 324 nC (trr 258 ns) AOS orijinalinin 6×/19× kötüsü → klon, orijinalle aynı parça değil. MGC021N04L’de Q_g 20 nC ↔ Ciss 6150 pF tutarsız (10 V’ta ≥ 60 nC beklenir) → güvenilmez veri sayfası.

### 2.3 Kapı sürme koşulları
- Alçak taraf V_GS = PVDD = 8.07 V; yüksek taraf V_GS ≈ PVDD − V_f(1N4148WT) ≈ 7.2 V.
- Sürücü (JSM6288Q1/FD6288Q): I_O+ 1.5 A / I_O− 1.8 A @15 V → eşdeğer çıkış direnci ≈ 10 Ω açma / 8.3 Ω kapama (T).
- Açma akımı I_on = (V_drv − V_pl)/(R_G + 10 + R_g,iç); kapama I_off = V_pl/(R_G + 8.3 + R_g,iç). Geçiş süresi t = (Q_gs/2 + Q_gd)/I.
- NTMFS, R_G = 22 Ω: I_on = (7.2 − 2.9)/33 = 0.13 A → t_on = (6 + 9) nC/0.13 A = 115 ns; I_off = 2.9/31.3 = 0.093 A → t_off = 162 ns; dV/dt ≈ 26.1 V/69 ns = 0.38 V/ns.
- Aynısı R_G = 10 Ω: t_on 73 ns, t_off 100 ns, dV/dt 0.59 V/ns.

### 2.4 Kayıp modeli (kanal başına, 6 adım komütasyon)
- İletim: her an bir yüksek + bir alçak taraf iletimde → P_c = I² × (R_LS + R_HS), R @ T_j = 100 °C (normalize çarpan: AOS 1.25 (DS s.2, 125 °C 4.4/3.3), SHYG 1.25 (Şekil 6), diğerleri 1.35–1.45 T).
- Anahtarlama (yalnız PWM’li faz; alçak taraf ZVS, yüksek taraf sert): E = ½·V·I·(t_on + t_off) + Qrr·V + Coss·V².
- Ölü zaman: P_dt = V_SD·I·2·t_dt·f, t_dt = 250 ns (T), V_SD = 0.8 V.
- Koşul: I = 55 A faz, V = 26.1 V, tipik R.

| Aday (R_G = 22 Ω) | R_LS / R_HS @100 °C (mΩ) | P_c (W) | 24 kHz: P_sw + P_dt → **P_kanal** | 48 kHz: P_sw + P_dt → **P_kanal** | 48 kHz maks R | Kart 4 × 55 A, 24 kHz |
|---|---|---|---|---|---|---|
| ME7170 | 3.44 / 3.59 | 21.3 | 6.9 + 0.5 → **28.7** | 13.8 + 1.1 → **36.2** | 37.9 | 115 W |
| AON6354 (AOS) | 3.69 / 3.87 | 22.9 | 1.7 + 0.5 → **25.1** | 3.4 + 1.1 → **27.3** | 31.9 | 100 W |
| AON6354-HXY | 3.74 / 3.90 | 23.1 | 5.0 + 0.5 → **28.7** | 10.1 + 1.1 → **34.3** | 40.5 | 115 W |
| SHYG015N04LS1C2 | 1.52 / 1.63 | 9.5 | 8.0 + 0.5 → **18.1** | 16.1 + 1.1 → **26.6** | 29.2 | 72 W |
| NTMFS5C430NL | 1.87 / 1.96 | 11.6 | 4.9 + 0.5 → **16.9** | 9.7 + 1.1 → **22.3** | 24.3 | 68 W |
| BLP016N04LC-Q | 1.91 / 1.98 | 11.8 | 4.8 + 0.5 → **17.1** | 9.5 + 1.1 → **22.3** | 25.6 | 68 W |
| ND2R8TG | 3.78 / 3.89 | 23.2 | 2.8 + 0.5 → **26.5** | 5.6 + 1.1 → **29.9** | 34.5 | 106 W |

R_G = 10 Ω ile (öneri, §3.4): NTMFS/BLP P_sw 24 kHz 3.1 W → P_kanal **15.1 W** (kart 61 W); 48 kHz 18.7 W (kart 75 W). Kapı sürme kaybı (2 × Q_g × V × f, çoğu R_G’de): NTMFS 48 kHz’de 2 × 56 nC × 8.07 V × 48 kHz = 43 mW/kanal — ihmal edilebilir.

### 2.5 Isıl model ve tutar mı (DOG-004, -006, -083)
**Model (tahmin, kart üstü ölçümle doğrulanacak):**
- Kart → hava: düz levha laminer, L = 45 mm, v = 5 m/s → Re ≈ 13 000, Nu ≈ 68, h ≈ 40 W/m²K; pervane türbülansı ve parçalarla 40–80 W/m²K. Alan 2 × 41.25 × 47.75 mm² × 1.3 (parça) = 5.1·10⁻³ m². Motor/pil kabloları kanatçık etkisi ≈ 0.2 W/K. **R_kart-hava: 4.9 (kötü) / 2.0 (orta, esas) / 1.6 (iyi) K/W.**
- Kılıf → kart ortalaması (DFN5×6, 2 oz dış + 0.5 oz iç, via’lı): 10 K/W (T). T_j = T_kılıf + P_FET × RθJC.
- Diğer kayıplar: shunt (0.1 mΩ önerisi), pil yolu bakırı 0.20 mΩ (T), faz yolları 0.24 mΩ/kanal (T), besleme/sürücü 1 W (T).
- Isıl kapasite (10 s darbe): FR4 6.6 + bakır 0.9 + parçalar ≈ 12 J/K (T); τ = 2.0 × 12 = 24 s.
- Ölçüt: kılıf ≤ 110 °C, T_j ≤ T_j,maks − 15 °C, kart ortalaması ≤ 95 °C (ESC’deki IC’ler ve X7R kondansatörler için).

**Sonuç (R_G = 10 Ω, 24 kHz, R_kart-hava 2.0 K/W, 25 °C):**

| Aday | 4 kanal sürekli: anahtarlamalı / tam gaz (A) | 50 °C’de (A) | Tek kanal sürekli (A) | 4 kanal 10 s darbe, T_j ölçütü: anahtarlamalı / tam gaz (A) | 10 s darbe, kılıf ≤ 110 °C (A) |
|---|---|---|---|---|---|
| AON6354-HXY (S1b) | 26.5 / 30.7 | 21.4 / 25.6 | 46.6 | 45 / 50 | 41 / 46 |
| AON6354 (AOS) | 29.2 / 30.8 | 24.1 / 25.8 | 49.9 | 47 / 49 | 45 / 47 |
| ND2R8TG | 28.1 / 30.5 | 23.1 / 25.5 | 48.5 | 47 / 50 | 43 / 46 |
| **BLP016N04LC-Q** | **34.1 / 40.4** | **27.5 / 33.8** | **62.1** | **64 / 71** | **54 / 62** |
| **NTMFS5C430NL** | **34.2 / 40.7** | **27.6 / 34.0** | **62.4** | **65 / 72** | **54 / 62** |
| SHYG015N04LS1C2 | 32.5 / 44.0 | 25.6 / 36.8 | 61.5 | 60 / 74 | 53 / 68 |

- Sınırda kartın toplam kaybı ≈ 35–37 W (T_kart 95–99 °C) → **sınırlayan, kartın ısı atma bütçesi**; FET seçimi bu bütçeye kaç amper sığdığını belirler.
- Duyarlılık (NTMFS, anahtarlamalı): R_kart-hava 1.6 / 2.0 / 4.9 K/W → 4 × 38 / 34 / 21 A. Belirsizlik büyük; DOG-005 testi kesin sonucu verir.
- **4 × 55 A sürekli (SYS-010):** en iyi 40 V FET ile kart kaybı 61 W (24 kHz, R_G 10 Ω); kart ancak ≈ 35 W atabiliyor → **karşılanmıyor**. S1b HXY ile 108 W.
- **4 × 70 A, 10 s (SYS-011):** NTMFS/BLP tam gazda T_j tepe ≈ 149 °C ≤ 160 °C (sınırda), kılıf ≈ 144 °C; anahtarlamalıda T_j > 160 °C. Ardından 55 A’ya dönüş SYS-010 yüzünden zaten tutmuyor → **karşılanmıyor (kısmen tam gazda)**. HXY 4 × 45–50 A’da kalır.
- **50 °C azaltma (DOG-083):** 4 kanal sürekli akım 25 °C değerinin ≈ %81’i (BLP/NTMFS 27.5 / 34 A).
- **48 kHz:** anahtarlama kaybı 2 katı; NTMFS 4 kanal sürekli ≈ 24 A (R_G 22 Ω) → **Bluejay varsayılanı 24 kHz önerilir.**

### 2.6 Yanlış iletime girme (Cdv/dt) ve paralel FET
- Alçak tarafa kuplajla gelen V_GS üst sınırı ≈ Crss/(Crss + Ciss) × 26.1 V: NTMFS 0.43 V, BLP ≈ 0.4 V, SHYG 0.31 V, ND2R8TG 0.6 V, AOS 1.04 V, **HXY 3.47 V**, MGC 1.57 V. 100 °C’de V_th(min) ≈ 0.8–1.0 V (−5.6 mV/K, onsemi DS s.2) → **HXY ve MGC’de alçak taraf kısa süre iletebilir (shoot-through), AOS sınırda**, 40 V düşük Crss’li adaylarda pay var.
- Paralel FET: kanal başına 12 FET 41 × 48 mm’e sığmaz; sınırlayan zaten kart ısı bütçesi. Önerilmez.

### 2.7 Net öneri (MOSFET)
1. **AON6354-HXY reddedilir** (30 V, Crss 340 pF, Qrr 324 nC, veri sayfası tutarsız). AON6354 (AOS) ve ME7170 de 30 V oldukları için SYS-014’ü karşılamaz.
2. **Seçim: BLP016N04LC-Q (C49328363, 0.182 $, +1.64 $/stack)**, 40 V, 1.6 mΩ maks, T_j 175 °C, Crss 65 pF. Stok 3 963: 100 sete (2 400) yeter, SYS-091 “≥ 2×” kuralına yetmez → sipariş öncesi stok ayırma (`bom-tedarik`).
3. **İkinci kaynak / prototip: NTMFS5C430NLT1G (C194661, 0.237 $, +2.96 $/stack)**, onsemi orijinal, stok 173 k. Aynı DFN5×6 (S-S-S-G / D) dizilimi; ayak izi her ikisine uygun çizilmeli (`pcb-muhendisi`).
4. Bütçe seçeneği: ND2R8TG (C54300813, +1.44 $/stack, 40 V) — ısıl olarak AOS 30 V ile aynı sınıf (4 × 28–30 A).
5. 40 V’a geçmek akım sınıfını da yükseltir: HXY 4 × 26.5 A → BLP 4 × 34 A (anahtarlamalı).

## 3. Kapı sürme (SYS-016, 070; DOG-015, -067)

### 3.1 JSM6288Q / JSM6288Q1 ↔ FD6288Q uyumu

| | FD6288Q (lib, s.7, 10–12) | JSM6288Q C19077370 (lib, s.2–6) | JSM6288Q1 C52196409 (s.1, 3–8) |
|---|---|---|---|
| QFN24 pin dizilimi | 1–3 LIN1–3, 4 VCC, 6 COM, 9–11 LO3–LO1, 12/15/18 VS3/2/1, 13/16/19 HO3/2/1, 14/17/20 VB3/2/1, 22–24 HIN1–3, 5/7/8/21 NC | **Aynı** | **Aynı** |
| Mantık | Çıkış girişle aynı fazda; HIN = LIN = H → iki çıkış L | Aynı (Tablo 7-1) | Aynı (Tablo 7-1) |
| VCC önerilen | 5–20 V | **8–20 V** | 5–20 V |
| VCC UVLO+ / UVLO− | 4.6 (4.2–5.0) / 4.3 (3.9–4.7) V | **7.0 (6.4–7.6) / 6.6 (6.0–7.2) V** | 4.5 / 4.3 V (tip; min/maks verilmemiş) |
| VBS UVLO+ / UVLO− | 4.6 (4.2–5.0) / 4.3 V | **7.1 (6.4–7.7) / 6.9 (6.2–7.5) V** | 4.5 / 4.3 V |
| VB önerilen | ≥ VS + 5 V | ≥ VS + 8 V | ≥ VS + 6 V |
| I_O+ / I_O− | 1.5 / 1.8 A | 1.5 / 1.8 A | 1.5 / 1.8 A |
| Ölü zaman | 100 / 200 / 300 ns | 100 / 200 / 300 ns | 100 / 200 / 300 ns |
| V_IH / V_IL | 2.7 / 0.8 V | 2.5 / 0.8 V | 2.5 / 0.8 V |
| Giriş direnci | 200 kΩ (140–260) aşağı | 800 kΩ aşağı | 800 kΩ (metin: HIN → VSS, LIN → **VCC**; blok şema: ikisi de aşağı — tutarsız) |
| En kısa giriş darbesi | — | **< 1 µs iletilmez** (s.3 not 2) | < 1 µs iletilmez (s.4 not 2) |

**PVDD ile UVLO payı:** JW5026 V_FB 0.78–0.82 V (DS s.4) ve R02/R01 90.9 k/10 k %1 → **PVDD 7.73–8.42 V** (nominal 8.07 V; DOG-015’teki ±%2 varsayımı ±%2.5 ile güncellendi). 8.4 V girişte JW5026 düşüm bölgesinde: D_maks = 1 − t_off,min·f = 1 − 120 ns × 1.25 MHz = 0.85 → PVDD ≈ 0.85 × 8.4 − 0.1 A × (0.6 + 0.33) Ω ≈ **7.05 V**. V_BS = PVDD − V_f (0.6–1.0 V).

| Koşul | VCC payı JSM6288Q (UVLO+ maks 7.6) | V_BS payı JSM6288Q (7.7) | VCC payı Q1 / FD (5.0 maks, T) | V_BS payı Q1 / FD |
|---|---|---|---|---|
| 6S, PVDD 7.73 V (en kötü) | +0.13 V ✗ | 6.73 − 7.7 = **−0.97 V ✗** | +2.73 V ✓ | +1.73 V ✓ |
| 3S düşüm, 8.4 V giriş | 7.05 − 7.2 (UVLO− maks) = **−0.15 V ✗** | **✗** | +2.05 V ✓ | 6.05 − 5.0 = **+1.05 V ✓** |

→ **JSM6288Q (S1/S1b) ile yüksek taraf sürülemez (Kritik).** JSM6288Q1 ile DOG-015 ölçütü (≥ 1 V) geçer. Fark +0.075 $ × 4 = **+0.30 $/stack**. Q1’in UVLO’su yalnız “tipik” verilmiş; prototipte 3S düşümünde test edilmeli (DOG-016).

### 3.2 Bootstrap (1 µF + 1N4148WT)
- C_boot: 1 µF 0402 X5R 25 V (C52923); 7 V öngerilimde etkin ≈ 0.6 µF (T).
- PWM periyodu başına çekilen yük: Q_g(7.2 V) NTMFS ≈ 32 + 38 × 2.7/5.5 = 51 nC + I_QBS 150 µA × 41.7 µs (24 kHz, D ≈ 1) = 6 nC → 57 nC → **ΔV = 0.095 V** ✓ (pay 1.7 V).
- %100 görevde tutma süresi: (V_BS − 5.0 V) × C / I_QBS = 1.73 × 0.6 µF / 150 µA = **6.9 ms** → yüksek taraf 120° el. açık kalabilir; 6.9 ms ≥ T_e/3 → T_e ≤ 21 ms → 48 Hz elektriksel üstünde sorun yok (≈ 410 rpm, 7 çift kutup). ✓
- **En düşük/en yüksek görev oranı:** yenileme için alçak taraf açık süresi ≥ ölü zaman + şarj ≈ 0.3 + 1.5 µs (T) → D_maks ≈ %95.7 (24 kHz), %91 (48 kHz). Ayrıca sürücü < 1 µs darbeyi iletmez → 24 kHz’de %2.4–97.6, 48 kHz’de %4.8–95.2 dışında darbe kaybolur (düşük gazda düzgünsüzlük riski; 24 kHz bir neden daha).
- 1N4148WT: V_R 100 V ✓ (gerilme ≈ 35 + 7 − 8 = 34 V), ortalama akım 57 nC × 24 kHz = 1.4 mA ≪ 125 mA ✓, trr 4 ns ✓, V_f 1 V@50 mA (DS s.1) V_BS’yi düşürür — Q1 ile sorun değil. Schottky gerekmez.

### 3.3 Sürücü VCC dekuplajı
- Şematikte her sürücü VCC’sinde yalnız 100 nF 16 V (C32/C42 vb., netlist); FD6288 DS s.4: “C1 10 µF, çipe yakın”.
- Alçak taraf açılışı Q_g ≈ 56 nC + bootstrap yenilemesi ≈ 57 nC → 100 nF’de ≈ 1.1 V çökme. **Öneri: her sürücüye ≥ 1 µF 25 V 0402 (C52923, basic)** ekle (çökme ≈ 0.19 V); PVDD çıkışında C03 10 µF 10 V 0402 (8 V’ta etkin ≈ 2 µF, T) → **10 µF 16 V 0603** (C70225).

### 3.4 Kapı direnci 22 Ω ve aşağı çekme 10 k
- 22 Ω ile NTMFS/BLP’de anahtarlama kaybı 24 kHz’de 4.8 W/kanal (§2.4). **10 Ω** → 3.1 W/kanal (−%35), dV/dt 0.38 → 0.59 V/ns.
- Çınlama: kapı döngüsü L ≈ 8 nH (T), Ciss 4.3 nF → Z₀ = √(L/C) ≈ 1.4 Ω; R_toplam ≈ 19 Ω ≫ 2Z₀ → aşırı sönümlü ✓.
- Cdv/dt: alçak taraf tutma yolu 10 + 8.3 + 1 = 19.3 Ω; NTMFS’te kuplaj üst sınırı 0.43 V < V_th(100 °C) ≈ 0.8 V ✓.
- 10 k alçak kapı aşağı çekme: sürücü beslemesizken alçak tarafı kapalı tutar ✓. Yüksek tarafta aşağı çekme yok; düşük Crss’li 40 V FET’lerde pil takarken kuplaj ≈ 0.4 V ✓. HXY gibi yüksek Crss’li FET’lerde yüksek tarafa da 47 k G–S gerekirdi.

### 3.5 Ölü zaman (200 ns dahili)
- Motor sürerken alçak taraf ters akımla (S→D) kapanır; Miller platosu yoktur, kapı V_th’a RC ile iner: τ = 19.3 Ω × ≈ 6 nF (V_DS ≈ 0’da Ciss) ≈ 116 ns → t = τ·ln(8.07/1.2) ≈ **220 ns** (R_G 10 Ω), ≈ **360 ns** (R_G 22 Ω).
- Yüksek tarafın V_th’a ulaşması: ölü zaman (100–300 ns) + Q_g(th) 7 nC / 0.25 A ≈ 30 ns = 130–330 ns.
- → Ölü zaman en alt sınırdayken (100 ns) **çapraz iletim penceresi var** (Önemli). **Öneri:** Bluejay düzenindeki ölü zaman ayarı sürücünün 200 ns’ine ek olarak ≥ 200 ns (R_G 10 Ω) sağlamalı; ayar biriminin (Bluejay hedef adındaki ölü zaman alanı) doğrulanması `gomulu-yazilim`. Ölü zaman kaybı 24 kHz, 55 A, 400 ns toplamda ≈ 0.85 W/kanal.

### 3.6 MCU sıfırlama / programlama sırasında kapılar (DOG-067)
- EFM8BB21 sıfırlamada port mandalları 1, açık savak ve **zayıf yukarı çekme açık** (DS s.9); I_PU −10…−30 µA (Tablo 4.13).
- JSM6288Q(1) giriş 800 kΩ: 10 µA × 800 kΩ ≫ V_IH → HIN = LIN = H → kilitleme (interlock) **iki çıkışı da L yapar** ✓. C2 programlamada MCU durdurulmuş, pinler sıfırlama hâlinde ✓.
- 3.3 V gelmeden (PVDD önce yükselir): MCU pinleri ≈ 0 V (ESD diyotu) → giriş L → çıkışlar L ✓. Yüksek taraf ilk açılışta V_BS = 0 → UVLO → HO L ✓.
- FD6288Q ile (200 kΩ, 140 kΩ min): 10 µA × 140 kΩ = 1.4 V → 0.8–2.7 V belirsiz bölge; FD’ye dönülürse LIN/HIN’e 10 k aşağı çekme gerekir. JSM6288Q1 ile gerekmez.
- **Sonuç: Geçti (analiz).** Q1’in “LIN → VCC 800 kΩ” metni ile blok şema çelişiyor; yukarı çekme olsa bile MCU sıfırlamada iki giriş H → çıkışlar L; MCU beslemesizken LIN ESD diyotuyla ≈ 0.6 V’ta kalır ✓.

## 4. BEMF bölücü (SYS-015; DOG-013)

- Ağ (netlist, mcu.SchDoc): faz → 10 k → muxN → 1 k → GND; muxN → 3.3 k → com_all (P0.2). EFM8 komparatör giriş aralığı −0.25…VDD + 0.25 V (DS Tablo 4.12, s.21); I/O mutlak sınır VDD + 2.5 V = 5.8 V (Tablo 4.15).
- `test/sonuc/DOG-013.md` hesabı doğrulandı: 26.1 V + 0.7 V diyot → mux en çok **2.44 V**; 35 V’ta **3.25 V** (≤ 3.55 V ✓). Önerilen SMDJ24CA ile kıstırma ≤ 35 V’u ≤ 45 A’e kadar tutar (§6); 38.9 V (77 A) uç durumda mux ≈ 3.6 V → karşılaştırıcı aralığı dışına çıkar, hasar yok (mutlak sınıra karşılık faz ≈ 81 V).
- Sıfır geçişte nötr dengeli; komparatör ofseti (±10 mV) faza ±210 mV yansır (DOG-013).
- **E6 çözüldü (netlist):** her MCU sayfasında `+VD` → R? 3 k → **P0.1** → R? 1 k → GND. `+VD` güç portu yalnız mcu/mcu2 sayfalarında var, main sayfasında hiçbir besleme `+VD` değil → **ağ boşta, bölücü işlevsiz.** Oran 4:1; `+VD` = VBAT olsaydı 26.1 V → 6.5 V, 35 V → 8.75 V → P0.1 mutlak sınırını (5.8 V) aşardı. 4:1 oran ≤ 3S (12.6 V → 3.15 V) pil ölçümü için tasarlanmış görünüyor (BLHeli eski düşük gerilim kesmesi). BEMF ağının parçası değil.
- **Öneri:** 8 direnç DNP / kaldır (−0.03 $/stack). Bluejay P0.1 kullanmıyorsa (doğrulama `gomulu-yazilim`) P0.1 boşta kalabilir. İleride pil ölçümü istenirse 10 k / 1 k (11:1, 35 V → 3.18 V).
- **Sonuç: Geçti (analiz), E6 kararıyla.** Algılama payı motorla DOG-014.

## 5. Akım ölçümü (SYS-020, 021, 013; DOG-017, -019)

### 5.1 Mevcut tasarım (netlist)
- BAT (VBAT) → R00 ‖ R000 (2 × 1 mΩ 2512, C316227, 2 W, **±275 ppm/K**) → PWR; U2 IN+ = VBAT, IN− = PWR, REF = GND, V+ = 3.3 V; OUT → R03 22 Ω → R04 22 Ω → curr_sens → J0.1. C05 1 nF shunt üstünde. FMU bu shunt’tan sonra (J0.7 = PWR) beslendiği için FMU akımı da ölçülür ✓.
- **INA199C1 kazancı 50 V/V** (INA199 DS s.7: x1 = 50, x2 = 100, x3 = 200; A/B/C sürüm harfi). inceleme §2.2/E1 ve DOG-017 ×200 almış.
- Ölçek 0.5 mΩ × 50 = 25 mV/A → tam ölçek (3.3 − 0.2 V salınım)/0.025 = **124 A nominal, 116 A en kötü** (< 280 A ✗).
- Kayıp: 220 A’da 0.5 mΩ × 220² = **24.2 W** (eleman başına 12.1 W, 2 W sınıf ✗), 280 A’da 39 W.
- V_CM: INA199 mutlak ve çalışma sınırı 26 V (DS s.4–5) < 26.1 V (LiHV) ve 35 V geçici ✗.
- Tedarik: INA199C1 stoku 3 003 → **424**’e düşmüş (2026-11-10).

### 5.2 Seçenekler (hesap: `akim.py`; ölçüt ≥ 280 A en kötü, eleman ≤ %70 sınıf, V_CM ≥ 40 V; doğruluk VREFINT telafili ADC, ET ±5 LSB, shunt öz ısınma 60 K)

| Seçenek | mV/A | Tam ölçek nom / en kötü (A) | P 220 A / 280 A (W) | V_CM mutlak | 10 A / 30 A / 200 A hata (A) | $/stack (S1b’ye göre) |
|---|---|---|---|---|---|---|
| Mevcut 0.5 mΩ + INA199C1 (×50) | 25 | 124 / 116 ✗ | 24.2 / 39.2 ✗ | 26 V ✗ | 0.92 / 1.85 / 9.7 | — |
| **0.1 mΩ 3920 10 W + INA240A3 (×100)** | 10 | **310 / 297 ✓** | **4.8 / 7.8 ✓ (%48)** | **90 V ✓** | **0.89 / 1.36 / 5.4** | **+1.45** |
| 0.1 mΩ 3920 + INA186A3 (×100) | 10 | 326 / 310 ✓ | 4.8 / 7.8 ✓ | 42 V ✓ | 1.22 ✗ / 1.85 ✗ / 7.2 | +0.23 |
| 0.2 mΩ 3920 5 W + INA186A2 (×50) | 10 | 326 / 312 ✓ | 9.7 ✗ (%194) | 42 V ✓ | 0.93 / 1.47 / 6.1 | — |
| 0.25 mΩ 2512 6 W + INA186A2 | 12.5 | 261 / 247 ✗ | 12.1 ✗ | 42 V ✓ | — | — |
| Alçak taraf (GND dönüşü) 0.1 mΩ + INA181/INA199 | 10 | ✓ | 4.8 | V_CM ≈ 0 ✓ | V_OS 150 µV → 1.5 A sabit ✗ | +0.0–0.2 |

- **Doğruluk (SYS-021):** INA240A3 ile 30–200 A ±%5 içinde; 10 A’da 0.89 A > 0.5 A (yazılı ölçüt) ama ≤ max(%5, 1 A) ✓ → DOG-019’daki “±%5 veya ±1 A, hangisi büyükse” önerisi benimsenirse geçer. Sabit hata: V_OS 25 µV/0.1 mΩ = 0.25 A + ADC 5 LSB 0.40 A. INA186 (V_OS ±50 µV, kazanç ±%1) ve INA199/INA181 (±150 µV) düşük akım ölçütünü karşılamaz.
- **Alçak taraf:** ortak mod sorununu çözer ama ucuz yükselteçlerin ofseti doğruluğu bozar; ayrıca ESC toprağı (MCU, sürücü COM) pil eksisinden shunt kadar ayrılır (280 A’da 28 mV + L·di/dt sıçramaları). Önerilmez.
- **Shunt:** HoLRS3920-10W-0.1mR-1% (Milliohm, **C55113241**, ±100 ppm/K, 10 × 5 mm, 0.295 $, stok 3 845). Tek eleman: paralel 2512’lerde akım paylaşımı ve Kelvin bağlantısı sorunlu. 95 °C kartta 10 W sınıfı ≈ %75’e düşer (T) → 4.8 W ≈ %65 ✓. **Kelvin (4 telli) bağlantı zorunlu** (`pcb-muhendisi`); 0.1 mΩ, 2 oz bakırın ≈ 0.4 karesine eşit.
- **Yükselteç:** INA240A3DR (**C2060584**, SOIC-8, 1.79 $, stok 1 511), V_S 3.3 V, REF1 = REF2 = GND (tek yönlü). Çıkış tavanı V_S − 0.2 V = 3.1 V → CUR ≤ 3.3 V her koşulda ✓. Giriş süzgeci önerilmez (I_B ≈ 90 µA, seri R kazanç hatası yapar); INA240’ın PWM bastırması yeterli. C05 (1 nF) kalabilir.
- **Betaflight ölçeği:** 10 mV/A → `ibata_scale = 100`, `ibata_offset = 0` (birim 0.1 mV/A; `gomulu-yazilim` doğrulasın). 280 A → CUR 2.8 V.
- FMU tarafı: ADC_CURR0’da doğrudan 10 µF 0805 (C?) var (netlist). 44 Ω seri dirençle kararlı ama yavaş; **1 kΩ + 100 nF** önerilir (enjeksiyon sınırı, DOG-017 not 4).
- **Net öneri:** **0.1 mΩ 3920 10 W + INA240A3DR, yüksek taraf**, +1.45 $/stack. Bütçe seçeneği INA186A3IDCKR (**C2058245**, INA199 ile **pin uyumlu SC70-6**, +0.23 $/stack): SYS-020 ✓, SYS-021 için “±%8 veya ±2 A” gevşetmesi gerekir (müşteri kararı).

## 6. Geçici gerilim, TVS, bulk (SYS-014, RSK-008; DOG-011, -009)

### 6.1 Kaynaklar ve hesap (pil kablosu 2 × 15 cm 12 AWG + XT60: L ≈ 0.25 µH (T), R_pil + kablo ≈ 20 mΩ (T))
**a) Pil takma (hot-plug), yalnız seramik:** C_etkin = 15 × 10 µF 50 V @26 V ≈ 15 × 4 µF = 60 µF (T). Z₀ = √(0.25 µH/60 µF) = 65 mΩ, ζ = 0.02/(2 × 0.065) = 0.15 → aşma e^(−πζ/√(1−ζ²)) = 0.62 → **tepe ≈ 26.1 × 1.62 = 42 V ✗**.
**b) Pil takma, set kondansatörü (≥ 470 µF, ESR 50 mΩ) pedlerde:** C = 530 µF, Z₀ = 22 mΩ, ζ ≈ (20 + 50)/(2 × 22) = 1.6 → aşırı sönümlü, **tepe ≈ 26.1 V ✓**.
**c) Gaz kesme / rejeneratif fren:** köprü akımı 4 × 55 A → −50 A (rejen.), ΔI = 270 A. Motor endüktansı (≈ 15 µH, T) eğimi ≈ 7 A/µs (4 motor) → ≈ 40 µs rampa. Yalnız seramik: ω₀ = 1/√(LC) = 258 krad/s, ω·T_r/2 = 5.2 → |sin x / x| ≈ 0.17 → aşma ≈ 270 × 0.065 × 0.17 ≈ 3 V + pil iç direnci 50 A × 25 mΩ = 1.3 V → **≈ 30.5 V ✓**. Ani kesme (desenkron/frenleme, en kötü): 270 A × 65 mΩ = 17.6 V → **≈ 44 V ✗**; set kondansatörüyle 270 A × (22 mΩ ‖ ESR) ≈ 6 V → **≈ 32 V ✓**.
→ **Set kondansatörü SYS-014’ün zorunlu parçası** (SYS-014 metni “takılıyken” diyor; SOR-011 kabul edildi). Kutudaki kondansatör: ≥ 470 µF, ≥ 35 V, ESR ≤ 50 mΩ @100 kHz, bacak ≤ 3 cm; kılavuzda “takılmadan uçma” uyarısı.

### 6.2 TVS
Dinamik direnç R_d ≈ (V_C − V_BR,maks)/I_PP (Brightking DS s.3):

| TVS (3 kW SMC) | V_RWM | V_BR (V) | V_C @ I_PP | R_d | ≤ 35 V’ta taşıyabildiği akım | 26.1 V’ta |
|---|---|---|---|---|---|---|
| SMDJ28CA (mevcut) | 28 | 31.1–34.4 | 45.4 V @66 A | 0.17 Ω | **3.6 A** ✗ | iletmez |
| SMDJ26CA | 26 | 28.9–31.9 | 42.1 V @71 A | 0.14 Ω | 22 A | iletmez (−10 °C’de V_BR ≈ 27.9 V) |
| **SMDJ24CA** | 24 | 26.7–29.5 | 38.9 V @77 A | 0.12 Ω | **45 A** | ≤ 1 mA sızıntı (T); −10 °C’de mA mertebesi |

**Öneri:** **SMDJ24CA (DOWO C284061, 0.202 $, stok 2 444)** ya da 5 kW 5.0SMDJ24CA (C284111, 0.322 $, stok 4 253). Pil takılıyken mA mertebesinde sızıntı kabul (≤ 26 mW, pil bağlıyken). Çift yönlü kalır (ters kutup koruması yok, SOR-010).

### 6.3 Bulk kondansatör
- **Sınıf:** SYS-014 kuralı (≥ 40 V) → 35 V kondansatörler karşılamaz → **50 V**.
- **Sıcaklık:** kart ortalaması sınırda 95 °C (§2.5) → X5R (+85 °C) aşılır → **X7R**.
- **Adet:** dalgalanma akımı (4 kanal, %50 görev, kanal başı 30 A, eşzamansız PWM): I_rms ≈ √4 × 0.5 × 30 = 30 A; set kondansatörü (ESR 30–50 mΩ) 24 kHz’de çoğunu taşır, seramik payı ≈ %50 → 15 adette ≈ 1 A_rms/adet (1206 ESR ≈ 5 mΩ → 5 mW) ✓. Gerilim dalgalanması seramik yalnızken 30 × 0.25/(24 kHz × 60 µF) ≈ 5 Vpp, set kondansatörüyle ≈ 1–1.5 Vpp (T).
- **Seramik DC öngerilim:** 22 µF 35 V 1206 X5R @26 V ≈ %25–30 kalır (≈ 6 µF); 10 µF 50 V 1206 X7R @26 V ≈ %35–45 kalır (≈ 4 µF) (T, üretici eğrisi ölçülmeli). 29 × 22 µF ≈ 174 µF → 15 × 10 µF ≈ 60 µF etkin; set kondansatörüyle yeterli.
- **Öneri:** **15 × CL31B106KBHNNNE (10 µF 50 V X7R 1206, C89632, 0.121 $)** → −0.27 $/stack (S1b’ye göre). Kart ölçümde ≤ 85 °C çıkarsa X5R basic C13585 (0.089 $, −0.75 $/stack).
- C02 (JW5026 girişi) 4.7 µF **35 V** 0603 → **4.7 µF 50 V 0805 (C98192)**. C00/C01/C05 50 V ✓.
- BAT hattındaki diğer parçalar 40 V kuralına göre (öneriler uygulanınca): JW5026 44 V ✓, JSM6288Q1 VB 275 V ✓, 1N4148WT 100 V ✓, INA240 90 V ✓, 0402 dirençler 50 V ✓, MOSFET 40 V ✓.

## 7. ESC beslemesi (SYS-016; DOG-015; E11, E12)

| Kalem | Hesap | Sonuç |
|---|---|---|
| JW5026 V_IN | Mutlak 44 V (SW 45 V/5 ns), önerilen 4.7–40 V (DS s.2) | 35 V tepeye 9 V pay ✓ |
| V_FB | 0.780 / 0.800 / 0.820 V (DS s.4) | PVDD **8.07 V** (7.73–8.42 V en kötü) ✓ |
| V_OUT ≤ V_IN − 3 V (DS s.2) | 8.07 V için V_IN ≥ 11.1 V | 3S’te (9–12.6 V) kısmen düşüm bölgesi; D_maks ≈ 0.85 → 8.4 V’ta PVDD ≈ 7.05 V; JSM6288Q1 ile yeterli (§3.1) |
| EN | R0 90.9 k PWR → EN, EN mutlak 44 V | ✓ (alt direnç yok; UVLO dahili 4.3 V) |
| PVDD yükü | 4 × [sürücü 0.35 mA + 2 × Q_g × f (NTMFS 48 kHz 5.4 mA) + bootstrap] + AMS1117 45 mA | ≈ 75 mA (1 A sınıfının %8’i) ✓ |
| L00 6.8 µH NLCV32T (530 mA, 270 mΩ) | ΔI = (26.1 − 8.07) × 8.07/(26.1 × 6.8 µH × 1.1 MHz) = 0.75 A pp; f_min 0.75 MHz ve 35 V’ta 1.2 A pp → tepe 0.47–0.71 A | **> 530 mA ✗** → **10 µH SWPA3015S100MT (C45403, 3 × 3 mm, I_sat 0.92 A)**: tepe ≤ 0.47 A (%51) ✓, −0.01 $/stack |
| JW5026 ısı | P_out 0.6 W, η ≈ %85 → 0.1 W; kart üstüne θ_JB ≈ 60 K/W (T) → +6 K | Kart 95 °C’de T_j ≈ 101 °C ≤ 110 ✓ |
| C03 (PVDD çıkışı) | 10 µF **10 V** 0402: 8.07 V’ta %81 anma, etkin ≈ 2 µF (T) | **10 µF 16 V 0603 (C70225)** |
| AMS1117-3.3 (UMW C347256) | Yük ≈ 4 × 10.1 mA (EFM8 49 MHz maks, DS Tablo 4.2) + INA 0.3 mA = 41 mA; I_q 5 mA. P = (8.42 − 3.3) × 0.041 + 8.42 × 0.005 = 0.25 W | SOT-89 θ_JA 165 K/W (DS s.3, JEDEC) → kart üstüne ≈ +10 K (T) ✓; giriş mutlak 18 V, önerilen ≤ 12 V ✓ |
| AMS1117 çıkış kondansatörü | +3V3’te yalnız 100 nF’ler var (C04 + 4 MCU, netlist); DS s.5: “kararlılık için çıkış kondansatörü gerekli, 22 µF tantal her durumu kapsar” | **Önemli:** ≥ 10 µF ekle (10 µF 16 V 0603, C70225); düşük ESR seramikle kararlılık prototipte ölçülmeli |
| AP2210 (E12) | AP2210: 300 mA, V_IN mutlak 15 V, önerilen 13.2 V, SOT-23 | Gerek yok; AMS1117 (SOT-89) ısıl olarak daha iyi. AP2210 veri sayfası referans kalır |
| “max 15V” notu (E11) | AP2210 V_IN mutlak 15 V (DS), AMS orijinal AMS1117 15 V | **3.3 V LDO giriş sınırı** = PVDD üst sınırı. PVDD ≤ 12 V (UMW AMS1117 önerilen) kalmalı; notu “PVDD ≤ 12 V (LDO)” olarak netleştir |

## 8. FMU beslemesi (SYS-040…045, 062, 074; DOG-037, -039, -041, -043, -045, -047, -074)

### 8.1 Netlist bulguları (fmu.SchDoc)
- **Giriş:** J0.7 (ESC konnektörü VBAT) → F9 → **U9 pin 2 (S)**; **U9 pin 3 (D)** → VIN (U3/U4 girişi, C30/C40 10 µF 50 V, C31/C41 100 nF 50 V). Kapı (pin 1) → R95 100 k → GND; D9 10 V zener katot VIN, anot kapı.
  - AO3401A SOT-23: pin 1 G, 2 S, 3 D (DS s.1). Doğru yüksek taraf P-MOS koruması **D pil tarafında, S yük tarafında** olmalı. Mevcut bağlantıda gövde diyodu (D → S) ters kutupta iletir → −25.4 V yüke ulaşır; düz kutupta açılışta V_GS ≈ −V_BAT = −26 V (> ±12 V) ta ki VIN yükselip zener kıstırana kadar. Zenerin VIN’e bağlanması tasarımcının S’yi VIN tarafında düşündüğünü gösteriyor → **sembol/yerleşim ters (Kritik, `sematik-muhendisi` görselle teyit)**.
  - Doğru yönde: V_DS −30 V vs −26.1 V → pay 3.9 V ✓ (SYS-074); V_GS: zener 9.4–10.6 V < ±12 V ✓; zener akımı (35 − 10)/100 k = 0.25 mA ✓; VBAT bölücüsü VIN’de (U9’dan sonra) ✓ (DOG-021 not 3).
- **BAT3 pedi VIN’de** (U9 ve F9’dan sonra): bu pedden beslenirse ters kutup ve sigorta koruması yok. Öneri: BAT pedi U9’dan önce (J0.7 ile aynı düğümde) olsun.
- **VBAT bölücüsü:** VIN → R92 10 k → R93 7.15 k → ADC_VBAT (PC3) → R94 2.2 k → GND; ADC_VBAT’ta 10 µF (C?). Oran (10 + 7.15 + 2.2)/2.2 = **8.80:1 → tam ölçek 29.0 V < 30 V (SYS-022 ✗)**; 35 V’ta pin 3.98 V (> VDDA + 0.3, enjeksiyon ≈ 20 µA, zararsız ama okuma doyar). inceleme §4.1 ve DOG-021 “R95 100 k / R92 10 k, 11:1” almış; R95 aslında U9 kapı direnci. **DOG-021 yeniden yapılmalı (`test-muhendisi`).**
- **İkinci ESC konnektörü (J1, SM08B):** pin 7 (VBAT) bağlantısız; J1.1 ADC_CURR1 MCU’ya bağlı değil (netlist). Bilgi; X8’de ikinci ESC akımı okunmaz.
- **F9 PTC değil sigorta:** CFS12V3T5R0 = 1206 hızlı sigorta 5 A, 32 V DC, kesme 50 A (LCSC; DS s.3). 32 V ≥ 26.1 V ✓. En büyük giriş akımı 3S’te 3.1 A (%62) ✓. Bir kez atar (BEC kısa devresinde atmaz, buck akım sınırı önce devreye girer).
- 3.3 V regülatörü yok (RSK-012) ✓ teyit.

### 8.2 Buck değişimi (SYS-044, DOG-045)
TPS54202: V_IN 4.5–28 V, mutlak **30 V** (DS s.4) < 35 V geçici ✗; “TPS54202H” yazımı: LCSC’de yalnız TPS54202DDCR var, veri sayfasında H sürümü yok → aynı ailenin farklı sipariş kodu; değişince önemsiz.
Ön koruma ile kurtarma mümkün değil: 26.1 V sürekliyi geçirip ≤ 28 V’ta kıstıran TVS yok (V_RWM ≥ 26.1 → V_C ≥ 40 V).

| Aday | V_IN çalışma / mutlak | Akım | V_REF | Kısa devre | Kılıf | JLC $ (200 ad.) | Stok |
|---|---|---|---|---|---|---|---|
| TPS54202 (mevcut) | 28 / 30 V ✗ | 2 A | 0.596 ±%2.5 | hiccup ✓ (DS s.11) | SOT-23-6 | 0.113 | 175 k |
| **SY8303AAIC (Silergy)** | **40 / 40 V** ✓ (sınırda) | 3 A | **0.600 ±%1.5** | SCP + ısıl kapanma, kendiliğinden dönüş (mod ayrıntısız) | TSOT-23-8 | **0.329** | 12 941 |
| LMR51430XDDCR (TI) | 36 / **38 V** | 3 A | 0.6 | hiccup ✓ | SOT-23-6, **TPS54202 ile pin uyumlu** | 0.473 | 9 537 |
| AP64200SP (Diodes) | 40 V | 2 A | — | — | SO-8EP | 0.462 | 19 860 |

**Öneri: SY8303AAIC × 2 (C2937216), +0.43 $/stack**, R_FS 200 k → 500 kHz. LMR51430 35 V’ta hasar görmez ama 40 V kuralını 2 V kaçırır (yedek seçenek; FMU PCB henüz yok, pin uyumunun faydası az). Ek: FMU VIN’e **SMBJ24CA (C78416, 0.045 $)** — kablo ve konnektörden gelen yerel çınlamaya karşı.

### 8.3 BEC değerleri (DOG-037, -039, -043, -047)
**Geri besleme (dirençler aynen kalır, %1):**

| Ray | Dirençler | TPS54202 (0.581–0.611 V) en kötü | SY8303A (0.591–0.609 V) en kötü | Pencere ±%5 |
|---|---|---|---|---|
| 5 V | R42 100 k / R43 13.7 k | 4.738–5.161 V ✗ (alt sınırı 12 mV aşıyor) | **4.820–5.144 V ✓** (nominal 4.98 V) | 4.75–5.25 |
| 9 V | R32 100 k / R33 7.15 k | 8.546–9.330 V ✗ (4 mV) | **8.693–9.299 V ✓** (nominal 8.99 V) | 8.55–9.45 |

(DOG-037’deki V_FB ±%2 varsayımı TPS54202 DS s.5’e göre ±%2.5; bu yüzden mevcut tasarım iki rayda da sınırı az farkla kaçırıyor.)

**Bobinler (L32/L42 = SWPA4030S100MT, 10 µH, I_sat 2.4 A, I_rms 1.5 A, 130 mΩ):**
- 5 V / 2 A: ΔI(26.1 V, 500 kHz, 10 µH) = 21.1 × 5/(26.1 × 10 µ × 500 k) = 0.81 A pp → tepe 2.41 A ≥ I_sat ✗; I_rms 2 A > 1.5 A ✗. **Öneri: SWPA6045S6R8MT (6.8 µH, I_sat 4.3 A, I_rms 3 A, 31 mΩ, 6 × 6 mm, C57254)**: ΔI 1.19 A pp → tepe 2.6 A (%60), I_rms %68 ✓.
- 9 V / 1.5 A: ΔI = 17.1 × 9/(26.1 × 10 µ × 500 k) = 1.18 A pp → tepe 2.09 A (%87 I_sat), I_rms %100 ✗. **Öneri: SWPA5040S100MT (10 µH, I_sat 2.9 A, I_rms 2.1 A, 83 mΩ, 5 × 5 mm, C84608)**: tepe %72, I_rms %71 ✓.

**Kayıp (SY8303A: R_on üst 110 / alt 70 mΩ, DS s.4; geçiş ≈ 20 ns T):**
- 5 V 2 A, 26.1 V giriş: iletim 2² × (0.11 × 0.19 + 0.07 × 0.81) = 0.31 W + anahtarlama ½ × 26.1 × 2 × 20 ns × 500 kHz = 0.26 W + bobin 0.13 W + 0.05 → **≈ 0.75 W, η ≈ %93**.
- 9 V 1.5 A: 0.19 + 0.20 + 0.19 → **≈ 0.6 W, η ≈ %96**.
- 3S’te 9 V (SYS-041 “≥ V_IN − 1.5 V”): D_maks = 1 − 120 ns × 500 kHz = 0.94 → 9.0 V girişte 9.0 × 0.94 − 1.5 × 0.19 = **8.17 V ≥ 7.5 V ✓**; 8.4 V’ta 7.6 V ≥ 6.9 V ✓. 9V_EN: EN eşiği ≤ 1.5 V, EN mutlak 40 V ✓.

**Isı (DOG-043, masa, hava akışsız, 25 °C, 10 dk; FMU PCB yok → tahmin):** FMU kart kaybı: 5 V BEC 0.75 + 9 V BEC 0.6 + 3.3 V LDO 0.43 + MCU/sensör 0.5 + OSD (5 V) 0.2 ≈ **2.5 W**. 36 × 36 mm iki yüz, doğal taşınım + ışınım h ≈ 12.5 W/m²K → R ≈ 26 K/W → kart **≈ 60–90 °C** (yığındaki ESC ve kablolarla iletim belirsiz). SY8303A T_j = kart + 0.75 W × θ_JC 11.2 ≈ +8 K ✓ (150 − 15 = 135). **STM32F405RGT6 (−40…85 °C sınıfı, T_j maks 105 °C → ölçüt ≤ 90 °C) sınırda.** → Kısmen; FMU yerleşiminde BEC’ler MCU’dan uzak, bakır alanı büyük (`pcb-muhendisi`); DOG-044 testi belirleyici.

**Kısa devre (DOG-047):** TPS54202 hiccup (512 çevrim bekle, 16 384 çevrim sonra yeniden başla, DS s.11) → kendiliğinden döner ✓. SY8303A: çevrim çevrim akım sınırı (4–6.8 A), “Short Circuit Protection”, ısıl kapanma ve kendiliğinden dönüş (DS s.1, 4); SCP modu (hiccup/frekans katlama) belirtilmemiş → DOG-048 testinde doğrulanmalı.

### 8.4 3.3 V hattı (SYS-042, DOG-041)
- Yük: STM32F405 168 MHz tüm çevre birimleri 102 mA (85 °C maks, DS Tablo 21) + W25Q128 ≈ 25 mA + IMU 1 mA + baro 1 mA + LED/diğer 10 mA ≈ **140 mA** + dış 3.3 V pedi 100 mA = **240 mA**. OSD (AT7456E) +5V’tan beslenir (netlist).
- **ME6211C33M5G (S1 varsayımı):** 500 mA (C33 tablosu, DS s.8) ama **SOT-23-5 P_D 300 mW** (DS s.5). P = (5.0 − 3.3) × 0.24 = 0.41 W > 0.30 W ✗ (dış yük olmadan 0.24 W, %80).
- **Öneri: AMS1117-3.3 SOT-223 (C6186, basic, 0.161 $)**: 0.24 A ≤ 0.8 × 1 A ✓; P = 0.41 + 5 V × 5 mA = 0.43 W; θ_JA 120 K/W (UMW DS s.3) → +52 K (JEDEC), kart üstüne ≈ +8 K (T) ✓; düşüm 0.24 A’da ≈ 1.0–1.15 V → 4.75 V − 1.15 = 3.6 V ≥ 3.3 V ✓. Çıkışa 22 µF (DS s.5). +0.11 $/stack (basic olduğu için extended yükleme ücreti düşer).
- IMU beslemesi ≤ 10 mVpp: buck dalgalanması (≈ 10–20 mVpp 500 kHz) × LDO PSRR (yüksek frekansta ≈ 30 dB, T) ≈ 0.5 mV; ayrıca IMU VDD’ye **10 Ω + 1 µF RC** önerilir.
- VDDA referansı DOG-021’in istediği ±%0.5’i AMS1117 (±%1–2) vermez → VREFINT telafisi (`gomulu-yazilim`) ya da ayrı ±%0.5 referans; ayrı karar.

### 8.5 VBAT tek SH pini (SYS-062, RSK-006) — elektriksel öneri
- FMU girişi (9 V 1.5 A + 5 V 2 A = 23.5 W, η ≈ %94): 3S 8.4 V’ta **3.0 A**, 4S 14.8 V’ta 1.7 A, 6S 22.2 V’ta 1.1 A. JST SH kontak sınıfı ≈ 1 A (T, konnektör DS ile doğrulanacak) → SYS-062’nin %80 ölçütü (0.8 A) hiçbir hücre sayısında tam yükte tutmuyor.
- Seçenekler: (1) **FMU’ya U9’dan önce ayrı BAT+/− lehim pedleri** (24–22 AWG, ESC pil pedinden), konnektör VBAT pini yalnız düşük güç için; kılavuzda “9 V yükü > 5 W ise ped kullan”. (2) Konnektör pin bütçesine göre BEC sınırı: 6S’te 0.8 A × 22.2 V × 0.94 ≈ 16.7 W, 4S’te 11 W. (3) İki pin VBAT (KRR-004 dizilimini bozar, önerilmez). **Öneri: (1) + (2) kılavuzda.** Karar `sistem-mimari` (İP-01).
- Ayrıca 3S tam yükte U9 kaybı: 3.0² × 50 mΩ (V_GS −8.4 V) = 0.45 W SOT-23’te (θ_JA 90–125 K/W, DS s.1) → +40–56 K ✗. Seçenek (1) ile akım düşerse AO3401A yeter; düşmezse **JSM7409 (30 V, 15 mΩ, DFN3.3, C2874717, +0.15 $)**.

## 9. S1b sadeleştirmelerinin güç onayı

| S1b maddesi | Karar | Gerekçe |
|---|---|---|
| A1 bulk 29 → 15 (22 µF 35 V) | **Koşullu onay**: adet 15 kalır, **parça 10 µF 50 V X7R 1206 (C89632)**, SMDJ24CA ve set kondansatörü zorunlu | 35 V sınıfı SYS-014’ü karşılamaz; set kondansatörüyle tepe ≤ 32 V (§6.1); ısıl olarak X7R |
| A2 AON6354-HXY | **Red** | 30 V (SYS-014), Crss 340 pF (yanlış iletim), Qrr 324 nC; yerine BLP016N04LC-Q / NTMFS5C430NL (§2.7) |
| B1 bulk 8 adet + set kondansatörü (müşteri) | Önerilmez | 8 × 4 µF = 32 µF; set kondansatörü bağlanmadan ilk takmada çınlama ≈ 45 V; seramik dalgalanma akımı adet başına ≈ 2 A |
| A9 FB dirençleri basic’e | JW5026 90.9 k → 91 k basic uygun (PVDD 8.08 V); FMU 13.7 k / 7.15 k aynen kalmalı (SY8303A ile pencere içinde) | §8.3 |
| B9 TVS’yi çıkar | **Önerilmez** | §6 |

## 10. Maliyet etkisi (100 set, $/stack, S1b = 27.38 $’a göre; JLC 2026-11-10)

| # | Değişiklik | Δ $/stack | Zorunlu? |
|---|---|---|---|
| 1 | MOSFET HXY → **BLP016N04LC-Q** (24 × +0.0685) / NTMFS5C430NL (+0.1235) / ND2R8TG (+0.0601) | **+1.64** / +2.96 / +1.44 | Evet (SYS-014) |
| 2 | JSM6288Q → JSM6288Q1 (4 × +0.075) | +0.30 | Evet (Kritik) |
| 3 | Shunt 2 × 1 mΩ → 1 × 0.1 mΩ 3920 | +0.19 | Evet |
| 4 | INA199C1 → **INA240A3DR** / INA186A3 | **+1.26** / +0.04 | Evet (biri) |
| 5 | SMDJ28CA → SMDJ24CA | −0.04 | Evet |
| 6 | Bulk 15 × 22 µF 35 V → 15 × 10 µF 50 V X7R (X5R basic) | −0.27 (−0.75) | Evet |
| 7 | C02 50 V, L00 10 µH 3×3, C03 16 V, AMS1117 çıkışı 10 µF, 4 × 1 µF sürücü VCC, E6 DNP | +0.08 | Evet |
| 8 | FMU 2 × SY8303AAIC | +0.43 | Evet |
| 9 | FMU bobinleri (6.8 µH 6045 + 10 µH 5040) | +0.03 | Evet |
| 10 | FMU 3.3 V LDO AMS1117-3.3 SOT-223 + 22 µF | +0.13 | Evet |
| 11 | FMU giriş SMBJ24CA | +0.05 | Önerilir |
| 12 | U9 → JSM7409 (3S tam yük gerekirse) | +0.15 | Koşullu |
| | **Önerilen paket (1 BLP + 4 INA240A3 + 2–11)** | **+3.80 → ≈ 31.2 $/stack** | |
| | Onsemi MOSFET ile | +5.12 → ≈ 32.5 $/stack | |
| | Ekonomik (ND2R8TG + INA186A3 + X5R basic; SYS-021 gevşer, 4 × 28 A sınıfı) | +1.90 → ≈ 29.3 $/stack | |

Extended çeşit değişimi: ESC +0 (çeşitler yer değiştiriyor), FMU +1 (SY8303A tek çeşit, LDO basic). **DT-001 (≤ 28 $) SYS-014 uyumlu tasarımla tutmuyor.** Dengeleme yolu müşteri kararları: B3 APM32F405 (−1.76), B6 BMI270 (−0.79) → önerilen paket ≈ 28.7 $/stack.

## 11. Bulgular

| # | Önem | Konum | Sorun (sayısal) | Öneri (değer, LCSC, fiyat etkisi) | Sahibi | SYS / DOG |
|---|---|---|---|---|---|---|
| G1 | Kritik | esc main, M1aH…M4cL | 30 V FET (ME7170/AON6354/HXY) < 40 V (35 V tepe + 5 V); HXY Crss 340 pF → alçak tarafta ≈ 1.5–3.5 V kuplaj, Qrr 324 nC | **BLP016N04LC-Q C49328363** (+1.64 $), yedek **NTMFS5C430NLT1G C194661** (+2.96 $); DFN5×6 ayak izi iki parçaya uygun | sematik-muhendisi, bom-tedarik, pcb-muhendisi | SYS-014, 010 / DOG-009, -011, -004 |
| G2 | Kritik | SYS-010/011 (ESC) | 4 × 55 A sürekli: en iyi FET’le kart 61 W, kart kapasitesi ≈ 35 W → **4 × 34 A (anahtarlamalı) / 41 A (tam gaz)**; 4 × 70 A 10 s yalnız tam gazda T_j sınırda (149 °C) | Akım sınıfını yeniden tanımla (KRR-B, müşteri kararı); 24 kHz varsayılan; iç katman ≥ 1 oz, pil yolu kısa; DOG-005 testiyle model kalibrasyonu | sistem-mimari, pcb-muhendisi (yönetici → müşteri) | SYS-010, 011, 012, 083 / DOG-004, -006, -083 |
| G3 | Kritik | esc mcu/mcu2, U12…U42 | JSM6288Q UVLO VCC 6.4–7.6 V, VBS 6.4–7.7 V; PVDD 7.73–8.42 V, V_BS 6.7–7.8 V → yüksek taraf UVLO (pay −0.97 V); 3S’te VCC da düşer | **JSM6288Q1 C52196409** (pin ve mantık aynı, UVLO 4.5 V), +0.30 $ | sematik-muhendisi, bom-tedarik | SYS-016, 013 / DOG-015, -009 |
| G4 | Kritik | esc main, U2 + R00/R000 | INA199**C1 = ×50** → tam ölçek 116–124 A (< 280 A); 220 A’da 24 W; V_CM 26 V < 26.1 V; stok 424 | **1 × 0.1 mΩ 3920 10 W (C55113241) + INA240A3DR (C2060584)**, Kelvin; `ibata_scale` 100; +1.45 $ (bütçe: INA186A3 C2058245, +0.23 $, SYS-021 gevşer) | sematik-muhendisi, pcb-muhendisi (Kelvin), bom-tedarik | SYS-020, 021, 013, 014 / DOG-017, -019 |
| G5 | Kritik | esc main, D00 | SMDJ28CA V_BR maks 34.4 V → 35 V’ta yalnız 3.6 A kıstırır | **SMDJ24CA C284061** (≤ 35 V’ta 45 A), −0.04 $ | sematik-muhendisi, bom-tedarik | SYS-014 / DOG-011 |
| G6 | Kritik | esc main, C1…C60; C02 | Bulk ve C02 35 V sınıfı (< 40 V); X5R +85 °C < kart 95 °C | **15 × 10 µF 50 V X7R 1206 C89632** (−0.27 $); C02 → 4.7 µF 50 V 0805 C98192; set kondansatörü (≥ 470 µF, ESR ≤ 50 mΩ) zorunlu, kılavuzda | sematik-muhendisi, bom-tedarik | SYS-014, 083 / DOG-011 |
| G7 | Kritik | fmu U3, U4 | TPS54202 V_IN mutlak 30 V < 35 V; V_FB ±%2.5 ile 5 V en kötü 4.738 V, 9 V 8.546 V (pencere dışı) | **SY8303AAIC C2937216 × 2** (40 V, V_REF ±%1.5; R32/R33/R42/R43 aynen), R_FS 200 k; +0.43 $; yedek LMR51430XDDCR C5185863 | sematik-muhendisi, bom-tedarik | SYS-044, 040, 041 / DOG-045, -037, -039 |
| G8 | Kritik | fmu U9, D9 (netlist) | AO3401A S pil tarafında, D yükte: ters kutupta gövde diyodu iletir; açılışta V_GS ≈ −26 V (> ±12 V) | U9’u çevir: D → F9/J0.7, S → VIN; zener G–S (VIN); görselle teyit | sematik-muhendisi | SYS-074, 044 / DOG-074 |
| G9 | Kritik | fmu 3.3 V | Regülatör yok; ME6211 SOT-23 P_D 0.3 W < 0.41 W (240 mA) | **AMS1117-3.3 SOT-223 C6186 (basic)** + 22 µF; IMU’ya 10 Ω + 1 µF; +0.13 $ | sematik-muhendisi | SYS-042 / DOG-041 |
| G10 | Önemli | fmu L32, L42 | SWPA4030S100MT: 5 V 2 A’da tepe 2.41 A ≥ I_sat 2.4 A, I_rms 2 > 1.5 A; 9 V I_rms %100 | 5 V: **SWPA6045S6R8MT C57254**; 9 V: **SWPA5040S100MT C84608**; +0.03 $ | sematik-muhendisi, pcb-muhendisi | SYS-040, 041 / DOG-037, -039 |
| G11 | Önemli | esc L00 | NLCV32T 530 mA; tepe 0.47–0.71 A | **SWPA3015S100MT C45403** (10 µH, 3 × 3, I_sat 0.92 A), −0.01 $ | sematik-muhendisi, pcb-muhendisi | SYS-016 / DOG-015 |
| G12 | Önemli | esc +3V3 (U0) | AMS1117 çıkışında yalnız 100 nF’ler; DS: kararlılık için çıkış kondansatörü gerekli (22 µF tantal) | 10 µF 16 V 0603 (C70225) AMS1117 çıkışına; +0.06 $ | sematik-muhendisi | SYS-016 / DOG-015 |
| G13 | Önemli | esc sürücü VCC (C32/C42…), C03 | Sürücü VCC’de yalnız 100 nF → LO açılışında ≈ 1.1 V çökme; C03 10 µF 10 V 0402 (8 V’ta ≈ 2 µF) | Her sürücüye 1 µF 25 V 0402 (C52923); C03 → 10 µF 16 V 0603 (C70225); +0.07 $ | sematik-muhendisi | SYS-016 / DOG-015 |
| G14 | Önemli | esc R_G (22 Ω × 24) | 24 kHz’de anahtarlama 4.8 W/kanal; LS kapanma (≈ 360 ns) > ölü zaman alt sınırı (100 ns + 30 ns) | R_G **10 Ω** (basic 0402); Bluejay ölü zaman ayarı ek ≥ 200 ns; PWM 24 kHz | sematik-muhendisi, gomulu-yazilim | SYS-010, 070 / DOG-004 |
| G15 | Önemli | fmu VBAT bölücü (netlist) | Gerçek bölücü R92 10 k + R93 7.15 k / R94 2.2 k = 8.80:1 → tam ölçek 29.0 V (< 30 V); DOG-021 yanlış dirençlerle (R95) hesaplanmış | DOG-021 yeniden; DOG-021 önerisi (20 k/2 k %0.1) yerine bölücü yeniden seçilsin; inceleme §4.1 düzeltilsin | test-muhendisi, sematik-muhendisi, sistem-mimari | SYS-022 / DOG-021 |
| G16 | Önemli | FMU besleme yolu | 23.5 W BEC → 3S 3.0 A, 6S 1.1 A tek SH pininde (≈ 1 A sınıf); U9 3S’te 0.45 W | FMU’ya U9 öncesi ayrı BAT pedleri + kılavuzda yük sınırı; gerekirse U9 → JSM7409 C2874717 (+0.15 $) | sistem-mimari, sematik-muhendisi | SYS-062, 043 / DOG-062, -043 |
| G17 | Önemli | fmu BAT3 pedi | BAT3 VIN’de: sigorta ve ters kutup korumasını atlar | Pedi U9/F9 öncesine taşı | sematik-muhendisi | SYS-074 / DOG-074 |
| G18 | Önemli | FMU ısıl (masa) | Kart kaybı ≈ 2.5 W → kart 60–90 °C (T); STM32F405RGT6 T_j ≤ 90 °C ölçütü sınırda | BEC’leri MCU’dan uzak, geniş bakır; DOG-044 ölçümü; gerekirse 9 V yükü masa testinde sınırlı | pcb-muhendisi, test-muhendisi | SYS-043 / DOG-043 |
| G19 | Önemli | Kart ısı bütçesi | Pil yolu bakırı 0.20 mΩ (T) → 220 A’da ≈ 10 W; iç katman 0.5 oz | İç katman ≥ 1 oz (`bom-tedarik` PCB fiyatı), pil pedi–köprü yolu kısa, çok via; DOG-008 | pcb-muhendisi | SYS-012, 010 / DOG-008 |
| G20 | Küçük | esc E6 (mcu/mcu2 R? × 8) | `+VD` boşta; 3 k / 1 k → P0.1; VBAT’a bağlanırsa 6S’te 6.5 V > 5.8 V | DNP / kaldır (−0.03 $); Bluejay P0.1 kullanımını doğrula | sematik-muhendisi, gomulu-yazilim | SYS-015 / DOG-013 |
| G21 | Küçük | esc ch_in (J0 → 220 Ω → P0.0) | Harici çekme yok; MCU sıfırlamada zayıf yukarı çekme | Bluejay DShot (CRC) ile sahte gaz olasılığı düşük; isteğe bağlı 100 k aşağı çekme; firmware giriş ayarı doğrulansın | gomulu-yazilim, sematik-muhendisi | SYS-073 / DOG-072 |
| G22 | Küçük | JSM6288Q(1) | < 1 µs giriş darbesi iletilmez (48 kHz’de %4.8 altı / %95.2 üstü) | 24 kHz; Bluejay en küçük görev oranı ayarı | gomulu-yazilim | SYS-015 / DOG-014 |
| G23 | Küçük | fmu ADC_CURR0 | CUR hattında doğrudan 10 µF 0805 | 1 kΩ seri + 100 nF | sematik-muhendisi | SYS-020 / DOG-017 |
| G24 | Küçük | fmu J1 (2. ESC) | Pin 7 VBAT bağlantısız, ADC_CURR1 MCU’ya gitmiyor (netlist) | Bilinçli mi, teyit; X8’de 2. akım okunmaz | sematik-muhendisi, sistem-mimari | SYS-020, 037 |
| G25 | Küçük | “max 15V” (E11), AP2210 (E12) | AP2210/AMS1117 V_IN mutlak 15 V; AP2210 kullanılmıyor | Notu “PVDD ≤ 12 V (3.3 V LDO)” yap; AP2210 gerekmez | sematik-muhendisi | SYS-016 |
| G26 | Küçük | Veri sayfaları | ME7170, JW5026, INA199, AMS1117, SMDJ, TPS54202, ME6211, AO3401A ve öneri parçaları repoda yok | §1’deki PDF’leri `lib/datasheet/`’e ekle | bom-tedarik | RSK-002 |

## 12. DOG bazında Ü-öncesi analiz sonucu

| DOG | SYS | Sonuç (mevcut tasarım) | Öneriler uygulanınca | Gerekçe |
|---|---|---|---|---|
| DOG-004 | 010 | **Kaldı** | Kaldı (sınıf yeniden tanımlanırsa Geçti) | 4 × 55 A’da kart kaybı ≥ 61 W, atabildiği ≈ 35 W; ulaşılabilir 4 × 34/41 A (BLP/NTMFS), S1b HXY 4 × 27/31 A (§2.5) |
| DOG-006 | 011 | **Kaldı** | Kısmen | 4 × 70 A 10 s: tam gazda T_j 149 °C ≤ 160 °C (sınırda), anahtarlamalıda > 160 °C; 55 A’ya dönüş SYS-010’a bağlı |
| DOG-009 | 013 | **Kaldı** | Geçti | INA199 V_CM 26 V < 26.1 V; JSM6288Q 8.4 V’ta UVLO. Q1 + INA240 ile tüm BAT parçaları ≥ 26.1 V, 8.4 V’ta PVDD 7.05 V, V_BS payı 1.05 V |
| DOG-011 | 014 | **Kaldı** | Kısmen | SMDJ28CA, 35 V kondansatörler, 30 V FET, INA199. Öneriyle: set kondansatörlü hesap ≤ 32 V, TVS ≤ 35 V’ta 45 A, tüm parçalar ≥ 40 V; simülasyon/ölçüm DOG-012’de |
| DOG-013 | 015 | Kısmen | Geçti | Mux ≤ 2.44 V (26.1 V), 3.25 V (35 V) ✓; E6 çözüldü (boşta bölücü, DNP) |
| DOG-015 | 016 | **Kaldı** | Geçti | PVDD 7.73–8.42 V (V_FB ±%2.5); JSM6288Q UVLO payı −0.97 V; Q1 ile VCC ≥ 2.7 V, V_BS ≥ 1.05 V (3S düşümünde); AMS1117 0.25 W ✓ (çıkış kondansatörü eklenmeli) |
| DOG-017 | 020 | **Kaldı** | Geçti | Mevcut 116–124 A (×50), 24 W, V_CM 26 V. Öneri 297–310 A, 4.8 W (%48), V_CM 90 V, CUR ≤ 3.1 V |
| DOG-019 | 021 | **Kaldı** | Kısmen (INA240A3) / Kaldı (INA186A3) | INA240A3: 30–200 A ±%5 ✓, 10 A’da 0.89 A (> 0.5 A yazılı; ≤ max(%5, 1 A) ✓) |
| DOG-037 | 040 | **Kaldı** | Geçti | TPS54202 en kötü 4.738 V; bobin I_rms 2 > 1.5 A; V_IN 28 V. SY8303A 4.82–5.14 V, 6.8 µH 6045, η ≈ %93 |
| DOG-039 | 041 | **Kaldı** | Geçti | TPS54202 en kötü 8.546 V; bobin I_rms %100. SY8303A 8.69–9.30 V, 10 µH 5040, 3S’te 8.17 V ≥ 7.5 V |
| DOG-041 | 042 | **Kaldı** | Geçti | Regülatör yok; ME6211 SOT-23 ısıl ✗. AMS1117-3.3 SOT-223: 240 mA ≤ 800 mA, 0.43 W |
| DOG-043 | 043 | Kısmen | Kısmen | FMU PCB yok; tahmini kart 60–90 °C, STM32 sınırda; DOG-044 ölçümü belirler |
| DOG-045 | 044 | **Kaldı** | Geçti | TPS54202 30 V. SY8303A 40 V (= 35 + 5), C30/C40 50 V, F9 32 V DC ≥ 26.1, U9 ters bağlantı düzelirse |
| DOG-047 | 045 | Geçti (TPS54202 hiccup) | Kısmen (SY8303A) | SY8303A’da SCP + ısıl dönüş var, mod belirsiz → DOG-048 testi |
| DOG-067 | 070 | Geçti | Geçti | EFM8 sıfırlamada zayıf yukarı çekme → HIN = LIN = H → kilitleme çıkışları L; beslemesizken 800 k aşağı; LS 10 k G–S |
| DOG-072 | 073 | Kısmen | Kısmen | Harici çekme yok; Bluejay giriş ayarı (yukarı çekme, DShot CRC) `gomulu-yazilim` doğrulamalı |
| DOG-074 | 074 | **Kaldı** | Geçti (ESC ipek baskı/kutu uyarısı PCB’de bakılacak) | U9 S/D ters (netlist); düzelince V_DS 30 V ≥ 26.1 + 3.9, V_GS zener 10 V < 12 V; BAT3 pedi korumayı atlıyor |
| DOG-083 | 083 | Kısmen | Kısmen | 50 °C’de 4 kanal sürekli ≈ %81 (BLP/NTMFS 27.5 / 34 A); X5R parçalar 85 °C sınırı → X7R; BOM sıcaklık sınıfı DOG-082 (`bom-tedarik`) |

## 13. Önerilen KRR’ler

| KRR (öneri) | Seçenekler | Önerilen ve gerekçe | Etki |
|---|---|---|---|
| **KRR-A — Güç MOSFET’i 40 V** | 1) AON6354-HXY 30 V (S1b) 2) AON6354 AOS 30 V 3) ND2R8TG 40 V 4) **BLP016N04LC-Q 40 V** 5) NTMFS5C430NL 40 V | **4, yedek 5.** SYS-014’ün 40 V kuralı; R_DS(on) yarıya iner, akım sınıfı 4 × 27 → 4 × 34 A (anahtarlamalı); düşük Crss | +1.64 $/stack (5 ile +2.96); bom-maliyet §2.2, §7; ayak izi DFN5×6 |
| **KRR-B — ESC akım sınıfı tanımı** (müşteri) | 1) 4 × 55 A sürekli korunur (kart/soğutucu büyür, form faktörü değişir) 2) **4 × 35 A sürekli + tek kanal 55 A sürekli + 4 × 55 A 10 s + 4 × 70 A 2 s (tam gaz)** 3) Pazar gibi doğrulamasız “55 A” etiketi | **2.** Ölçülebilir ve dürüst; 5" kullanımda ortalama motor akımı 10–25 A, tepe 40–45 A birkaç saniye (KRR-002 gerekçesi) ile uyumlu; “55A” ürün adı tek kanal/10 s anlamında kalabilir | SYS-010, 011, 012, 083, DOG-004/005/006/007 değişir (DT) |
| **KRR-C — Akım ölçümü** | 1) **0.1 mΩ 3920 + INA240A3, yüksek taraf** 2) 0.1 mΩ + INA186A3, SYS-021 gevşer 3) Alçak taraf + ucuz yükselteç 4) Akım ölçümü yok (B7) | **1.** Tek SYS-020 + SYS-021 uyumlu seçenek; V_CM 90 V geçici sorununu kökten çözer | +1.45 $/stack (2: +0.23) |
| **KRR-D — Geçici gerilim stratejisi** | 1) Yalnız TVS 2) **Set kondansatörü (zorunlu, kılavuz) + SMDJ24CA + 15 × 10 µF 50 V X7R** 3) Kartta elektrolitik | **2.** Hesap: set kondansatörsüz pil takma ≈ 42 V, set kondansatörlü ≤ 32 V; TVS yedek | −0.31 $/stack; SYS-061/063 kılavuz metni |
| **KRR-E — Kapı sürücü** | 1) JSM6288Q (stoklu, UVLO 7 V) + PVDD ≥ 10.5 V (3S desteklenmez) 2) **JSM6288Q1 (UVLO 4.5 V)** 3) FD6288Q (stok 0) | **2.** Pin/mantık aynı, PVDD 8.07 V ve 3S korunur | +0.30 $/stack |
| **KRR-F — FMU buck** | 1) TPS54202 + ön koruma (mümkün değil) 2) **SY8303AAIC** 3) LMR51430 (pin uyumlu, 38 V) | **2.** 40 V mutlak, V_REF ±%1.5, mevcut FB dirençleri geçerli | +0.43 $/stack; FMU PCB’de TSOT-23-8 |
| **KRR-G — Anahtarlama ayarları** | PWM 24/48 kHz; R_G 22/10 Ω; firmware ölü zaman | **24 kHz, R_G 10 Ω, ölü zaman ek ≥ 200 ns** | 0 $; `gomulu-yazilim` Bluejay hedefi |
| **KRR-H — Maliyet hedefi** (müşteri, DT-001 güncellemesi) | 1) Hedef ≈ 31 $/stack 2) ≤ 28 $’a yaklaşmak için B3 APM32 + B6 BMI270 (≈ 28.7 $) 3) Ekonomik paket (≈ 29.3 $, 4 × 28 A sınıfı, SYS-021 gevşer) | Ekip önerisi **1** (ya da 2, müşteri tercihi) | PRJ-004, RSK-004 |
| **KRR-I — FMU besleme yolu** (`sistem-mimari` ile) | 1) Tek SH pini (mevcut) 2) **Ayrı BAT pedleri + kılavuzda BEC yük sınırı** 3) İki VBAT pini | **2** | SYS-062, RSK-006; U9 kaybı |

## 14. İP-03 güç açısından kapanabilir mi

**Hayır.** Ü-öncesi analizlerin tamamı yapıldı; sonuç: 18 DOG’dan **12 Kaldı, 4 Kısmen, 2 Geçti** (mevcut tasarım). Öneriler uygulanırsa: 10 Geçti, 7 Kısmen, 1 Kaldı (DOG-004, akım sınıfı yeniden tanımlanmadıkça).

Kapanış için:
1. **Müşteri kararları (yönetici):** KRR-B (akım sınıfı), KRR-H (maliyet hedefi), KRR-C seçeneği (SYS-021), SOR-011 set kondansatörünün “zorunlu” olarak kılavuza yazılması.
2. **Ekip kararları:** KRR-A, D, E, F, G, I → `docs/gereksinimler/kararlar.md`.
3. **İP-05 (sematik-muhendisi):** G1, G3–G13, G17, G20, G23–G25; özellikle G8 (U9 yönü) görselle teyit.
4. **test-muhendisi:** DOG-021’i gerçek bölücüyle yeniden; DOG-013/015/017/019/037 sonuç dosyalarını bu rapordaki düzeltmelerle (INA199C1 ×50, V_FB ±%2.5) güncelle; ısıl modeli `test/analiz/`’e alıp DOG-005 ölçümüyle kalibre et.
5. **bom-tedarik:** §1 veri sayfaları, §10 maliyetleri `bom-maliyet.md`’ye, BLP016 stok ayırma, INA199C1 stok düşüşü.
6. Kart DOG’ları (DOG-005, -007, -012, -016, -044, -048) prototipte; ısıl model belirsizliği (R_kart-hava 1.6–4.9 K/W) yalnız ölçümle kapanır.
