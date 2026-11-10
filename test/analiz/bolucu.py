#!/usr/bin/env python3
"""Ü-öncesi bölücü hesapları (test-muhendisi, İP-08).

Kapsam ve DOG bağı:
  1. FMU VBAT bölücüsü R95 100 k / R92 10 k ............ DOG-021 (SYS-022)
  2. ESC BEMF bölücü + sanal nötr 10 k / 1 k / 3.3 k ..... DOG-013 (SYS-015) katkı
  3. ESC PVDD buck geri beslemesi JW5026 90.9 k / 10 k .... DOG-015 (SYS-016) katkı
  4. FMU BEC geri beslemesi TPS54202 5 V ve 9 V ......... DOG-037, DOG-039 (SYS-040/041) katkı

Kullanım:  python3 -I test/analiz/bolucu.py  [> test/sonuc/bolucu_ham.txt]
Çıkış kodu: 0 her zaman (sonuç metinde "GEÇTİ / KALDI"); betik deterministiktir.

Girdi kaynakları (her sayı yanında):
  [STM32]  lib/datasheet/STM32F405RGT6.pdf  Tablo 67/68 (ADC), Tablo 72/73 (VREFINT), I/O Ilkg ±1 µA
  [EFM8]   lib/datasheet/EFM8BB21F16G-C-QFN20_C1339974.pdf Tablo 4.13 (karşılaştırıcı), 4.16 (mutlak sınır), 4.2 (IDD)
  [FD]     lib/datasheet/Fortior-Tech-FD6288Q_C328453_eng.pdf Tablo 3-1/3-2, VCCUV±/VBSUV±
  [ALT]    boards/*/altium/*.SchDoc (tools/altium_sch_dump.py) ve docs/inceleme.md §2.2, §4.1
  [BOM]    boards/fmu/bom-maliyet.csv (0603WAF = %1)
  [VAR]    varsayım: veri sayfası yerelde yok (JW5026, TPS54202, ME6211, AMS1117) — sayı doğrulanacak
"""
import itertools
import math

# ---------------------------------------------------------------- ortak
SYS_AR = (9.0, 16.8, 25.2, 26.1)          # SYS-022 doğruluk noktaları (V)
T_REF = 25.0                              # °C
T_MIN, T_MAX = -10.0, 50.0                # SYS-083 çalışma ortamı
DT_MAX = max(T_REF - T_MIN, T_MAX - T_REF)  # 35 K

ADC_BITS = 12
ADC_ET_LSB = 5.0       # [STM32] Tablo 68 toplam ayarsız hata, maks (RAIN < 10 kΩ)
ADC_RAIN_MAX = 10e3    # [STM32] Tablo 68 koşulu
ILKG = 1e-6            # [STM32] I/O giriş kaçağı maks ±1 µA
VREF_NOM = 3.3


def par(a, b):
    return a * b / (a + b)


def hline(c="-", n=96):
    print(c * n)


# ---------------------------------------------------------------- 1. VBAT
VBAT_SECENEK = [
    # ad, R_ust, R_alt, tolerans, TCR ppm/K, referans türü, ref toleransı (oran)
    dict(ad="MEVCUT 100k/10k %1, ref=LDO", r1=100e3, r2=10e3, tol=0.01, tcr=100e-6,
         ref="ldo", reftol=0.02),   # [ALT][BOM]; ME6211 ±%2 [VAR]; TCR ±100 ppm [VAR]
    dict(ad="100k/10k %1, VREFINT telafili", r1=100e3, r2=10e3, tol=0.01, tcr=100e-6,
         ref="vrefint", reftol=0.0),
    dict(ad="100k/10k %0.5 25ppm, VREFINT", r1=100e3, r2=10e3, tol=0.005, tcr=25e-6,
         ref="vrefint", reftol=0.0),
    dict(ad="100k/10k %0.1 25ppm, VREFINT", r1=100e3, r2=10e3, tol=0.001, tcr=25e-6,
         ref="vrefint", reftol=0.0),
    dict(ad="20k/2k %0.5 25ppm, VREFINT", r1=20e3, r2=2e3, tol=0.005, tcr=25e-6,
         ref="vrefint", reftol=0.0),
    dict(ad="20k/2k %0.1 25ppm, VREFINT", r1=20e3, r2=2e3, tol=0.001, tcr=25e-6,
         ref="vrefint", reftol=0.0),
    dict(ad="20k/2k %0.1 25ppm, ref=LDO ±%0.5", r1=20e3, r2=2e3, tol=0.001, tcr=25e-6,
         ref="ldo", reftol=0.005),   # hassas 3.3 V LDO (±%0.5 sınıfı) VDDA'yı besler [VAR]
    dict(ad="20k/2k %0.5 25ppm, ref=LDO", r1=20e3, r2=2e3, tol=0.005, tcr=25e-6,
         ref="ldo", reftol=0.02),
]


def vrefint_hata():
    """VREFINT telafisinde kalan referans hatası (oran).
    VREFIN_CAL 30 °C / 3.3 V'ta fabrika ölçümü [STM32 Tablo 73]; TCoeff maks 50 ppm/K
    [STM32 Tablo 72]; kalibrasyon kelimesi kuantalaması ±0.5 LSB / ~1500 LSB; okuma
    gürültüsü için ±1 LSB [VAR]."""
    tc = 50e-6 * max(30 - T_MIN, T_MAX - 30)      # 40 K
    q = 1.5 / 1500.0
    return tc + q


def bf_k(k):
    """Betaflight vbat_scale (vbat_divider=10, multiplier=1): K_bf = round(10K)/10.
    Formül Betaflight src/main/sensors/voltage.c [VAR: gomulu-yazilim doğrulasın]."""
    return round(k * 10) / 10.0, int(round(k * 10))


def vbat_vaka(s, v, r1f, r2f, dtf, reff, leakf, etf):
    """Bir köşe için Betaflight'ın okuyacağı gerilim."""
    k_nom = 1 + s["r1"] / s["r2"]
    kbf, _ = bf_k(k_nom)
    dT = dtf * DT_MAX
    r1 = s["r1"] * (1 + r1f * s["tol"]) * (1 + dT * s["tcr"] * r1f)   # TCR en kötü yönde
    r2 = s["r2"] * (1 + r2f * s["tol"]) * (1 - dT * s["tcr"] * r1f)
    rth = par(r1, r2)
    vpin = v * r2 / (r1 + r2) + leakf * ILKG * rth
    if s["ref"] == "ldo":
        vref_act = VREF_NOM * (1 + reff * s["reftol"])
        vref_est = VREF_NOM
    else:
        vref_act = VREF_NOM * (1 + reff * 0.02)        # LDO ne olursa olsun
        vref_est = vref_act * (1 + reff * vrefint_hata())
    lsb = vref_act / 2 ** ADC_BITS
    code = vpin / lsb + etf * ADC_ET_LSB
    return code * vref_est / 2 ** ADC_BITS * kbf


def vbat_analiz():
    hline("=")
    print("1. FMU VBAT bölücüsü — DOG-021 / SYS-022")
    print("   Ölçüt: 9–26.1 V'ta |hata| ≤ %1 × V + 0.1 V; tam ölçek ≥ 30 V; ADC pini ≤ VDDA")
    print("   Kaynak: [ALT] R95 100k / R92 10k (fmu.SchDoc); [BOM] 0603WAF %1; [STM32] ET ±5 LSB,")
    print("   Ilkg ±1 µA, RAIN < 10 kΩ; LQFP64'te VREF+ = VDDA (ayrı VREF+ pini yok)")
    print("   VREFINT telafisi kalan hata = %.2f %% (TCoeff 50 ppm/K × 40 K + kuantalama)"
          % (100 * vrefint_hata()))
    hline()
    sonuc = {}
    for s in VBAT_SECENEK:
        k = 1 + s["r1"] / s["r2"]
        kbf, scale = bf_k(k)
        rth = par(s["r1"], s["r2"])
        fs_min = VREF_NOM * (1 - (s["reftol"] if s["ref"] == "ldo" else 0.02)) * k * (1 - 2 * s["tol"])
        i_q = 26.1 / (s["r1"] + s["r2"])
        print("%s" % s["ad"])
        print("   K = %.4f  Betaflight vbat_scale = %d (K_bf %.1f, kuantalama %.3f %%)"
              % (k, scale, kbf, 100 * (kbf / k - 1)))
        print("   Thevenin %.2f kΩ (%s RAIN < 10 kΩ); kaçak ±1 µA → pinde ±%.1f mV → VBAT'ta ±%.0f mV"
              % (rth / 1e3, "≤" if rth <= ADC_RAIN_MAX else "> !", ILKG * rth * 1e3,
                 ILKG * rth * k * 1e3))
        print("   Tam ölçek (en kötü düşük) %.1f V; 26.1 V'ta bölücü akımı %.2f mA, güç %.1f mW;"
              " 35 V geçicide pin %.2f V"
              % (fs_min, i_q * 1e3, 26.1 * i_q * 1e3, 35.0 / k))
        print("   %7s %9s %9s %9s %9s  %s" % ("V", "sınır", "en kötü", "RSS", "pay(ek)", "durum"))
        gecti_ek = True
        gecti_rss = True
        for v in SYS_AR:
            lim = 0.01 * v + 0.1
            worst = 0.0
            for r1f, r2f, dtf, reff, leakf, etf in itertools.product((-1, 1), (-1, 1), (0, 1),
                                                                    (-1, 1), (-1, 1), (-1, 1)):
                e = vbat_vaka(s, v, r1f, r2f, dtf, reff, leakf, etf) - v
                worst = max(worst, abs(e))
            # RSS: bileşen bazlı (her biri kendi en kötü değerinde, karekök toplam)
            a = (k - 1) / k
            comp = [a * s["tol"] * v, a * s["tol"] * v,
                    a * 2 * s["tcr"] * DT_MAX * v,
                    (s["reftol"] if s["ref"] == "ldo" else vrefint_hata()) * v,
                    ILKG * rth * k,
                    ADC_ET_LSB * VREF_NOM / 2 ** ADC_BITS * k,
                    abs(kbf / k - 1) * v]
            rss = math.sqrt(sum(c * c for c in comp))
            ok_ek = worst <= lim
            ok_rss = rss <= lim
            gecti_ek &= ok_ek
            gecti_rss &= ok_rss
            print("   %7.1f %9.3f %9.3f %9.3f %+9.3f  %s"
                  % (v, lim, worst, rss, lim - worst,
                     "GEÇTİ" if ok_ek else ("RSS'te geçer" if ok_rss else "KALDI")))
        fs_ok = fs_min >= 30.0
        durum = ("GEÇTİ" if gecti_ek and fs_ok else
                 "KISMEN (en kötüde kalır, RSS'te geçer)" if gecti_rss and fs_ok else "KALDI")
        print("   → tam ölçek %s; doğruluk %s" % ("GEÇTİ" if fs_ok else "KALDI", durum))
        sonuc[s["ad"]] = durum
        hline()
    return sonuc


# ---------------------------------------------------------------- 2. BEMF
R_FAZ, R_ALT, R_NOTR = 10e3, 1e3, 3.3e3     # [ALT] mcu.SchDoc R70/R72/R71 … ; inceleme §2.1
CMP_VIN_MAX = 3.3 + 0.25                    # [EFM8] Tablo 4.13 VDD + 0.25 V
IO_ABS_MAX = 3.3 + 2.5                      # [EFM8] Tablo 4.16 (VDD < 3.3 V: VDD + 2.5; 5.8 V tavan)
CMP_VOFF = 10e-3                            # [EFM8] Tablo 4.13 ±10 mV maks
V_DIYOT = 0.7                               # gövde diyotu iletim (tahmin) — faz BAT+0.7'ye çıkar


def coz(A, b):
    """Küçük yoğun Gauss eleme (numpy gerektirmesin)."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c:
                f = M[r][c] / M[c][c]
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    return [M[i][n] / M[i][i] for i in range(n)]


def bemf_ag(va, vb, vc):
    """Düğümler: muxA, muxB, muxC, com. Her faz → R_FAZ → mux; mux → R_ALT → GND;
    mux → R_NOTR → com. Döndürür (muxA, muxB, muxC, com)."""
    g1, g2, g3 = 1 / R_FAZ, 1 / R_ALT, 1 / R_NOTR
    A = [[g1 + g2 + g3, 0, 0, -g3],
         [0, g1 + g2 + g3, 0, -g3],
         [0, 0, g1 + g2 + g3, -g3],
         [-g3, -g3, -g3, 3 * g3]]
    b = [g1 * va, g1 * vb, g1 * vc, 0.0]
    return coz(A, b)


def bemf_analiz():
    hline("=")
    print("2. ESC BEMF bölücü + sanal nötr — DOG-013 / SYS-015 (sorumlu guc-elektronigi; hesap katkısı)")
    print("   Ağ: faz → %.0f k → muxN; muxN → %.0f k → GND; muxN → %.1f k → com_all  [ALT]"
          % (R_FAZ / 1e3, R_ALT / 1e3, R_NOTR / 1e3))
    print("   Ölçüt: mux ≤ 3.3 V (DOG-013); EFM8 karşılaştırıcı giriş aralığı ≤ %.2f V, mutlak ≤ %.1f V [EFM8]"
          % (CMP_VIN_MAX, IO_ABS_MAX))
    print("   Not: inceleme §2.2 'com'u GND sayıp 25.2 V → 1.8 V buldu; burada com düğümü çözülüyor.")
    hline()
    print("   %-36s %7s %7s %7s %7s %7s  %s" % ("Durum", "VBAT", "muxA", "muxB", "muxC", "com", "en büyük"))
    vakalar = []
    for vb in (8.4, 9.0, 16.8, 25.2, 26.1, 35.0):
        vakalar.append(("A=B=C=VBAT+Vd (en kötü statik)", vb, vb + V_DIYOT, vb + V_DIYOT, vb + V_DIYOT))
        vakalar.append(("A=VBAT, B=0, C=VBAT+Vd (demag.)", vb, vb, 0.0, vb + V_DIYOT))
    worst_026 = 0.0
    worst_35 = 0.0
    for ad, vb, a, b_, c in vakalar:
        m = bemf_ag(a, b_, c)
        mx = max(m[:3])
        if vb <= 26.1:
            worst_026 = max(worst_026, mx)
        else:
            worst_35 = max(worst_35, mx)
        print("   %-36s %7.1f %7.3f %7.3f %7.3f %7.3f  %.3f %s"
              % (ad, vb, m[0], m[1], m[2], m[3], mx,
                 "" if mx <= 3.3 else ("> 3.3 V!" if mx <= CMP_VIN_MAX else "> CMP aralığı!")))
    hline()
    # sıfır geçiş kazancı: C yüzerken d(muxC - com)/dVC, A=V, B=0
    v = 16.8
    m0 = bemf_ag(v, 0, v / 2)
    m1 = bemf_ag(v, 0, v / 2 + 0.1)
    kaz = ((m1[2] - m1[3]) - (m0[2] - m0[3])) / 0.1
    print("   Sıfır geçişte (A=V, B=0, C=V/2) muxC − com = %.4f V (ideal 0)" % (m0[2] - m0[3]))
    print("   Karşılaştırıcı farkı kazancı d(muxC−com)/dVC = %.4f V/V" % kaz)
    print("   EFM8 Voff ±10 mV → faza yansıyan ±%.0f mV; histerezis ±20 mV seçilirse ±%.0f mV"
          % (CMP_VOFF / kaz * 1e3, 20e-3 / kaz * 1e3))
    for kv, vb in ((1750, 25.2), (1960, 25.2), (2400, 16.8), (2750, 16.8)):
        # BEMF faz–nötr tepe ≈ (rpm/KV)/√3 [tahmin, sinüs yaklaşımı]; 5× Voff yansıması için rpm
        rpm_min = 5 * (CMP_VOFF / kaz) * math.sqrt(3) * kv
        print("   %4d KV: faz-nötr BEMF tepe 5 × Voff_faz olduğunda rpm ≈ %.0f (tahmin; boşta rpm ≫ bu ise pay var)"
              % (kv, rpm_min))
    durum = "GEÇTİ (26.1 V'a kadar)" if worst_026 <= 3.3 else "KALDI"
    print("   → 26.1 V + Vd'de en büyük mux %.3f V: %s; 35 V geçicide %.3f V (%s)"
          % (worst_026, durum, worst_35,
             "≤ 3.3 V" if worst_35 <= 3.3 else ("CMP aralığında" if worst_35 <= CMP_VIN_MAX else "CMP aralığı dışı")))
    print("   Açık: E6 '????' dirençleri (mcu/mcu2 R? 3k/1k) ağın parçasıysa sonuç değişir.")
    return worst_026, worst_35, kaz


# ---------------------------------------------------------------- 3/4. buck geri besleme
def buck(ad, vfb, vfb_tol, rtop, rbot, rtol, hedef, alt, ust):
    vn = vfb * (1 + rtop / rbot)
    lo = vfb * (1 - vfb_tol) * (1 + rtop * (1 - rtol) / (rbot * (1 + rtol)))
    hi = vfb * (1 + vfb_tol) * (1 + rtop * (1 + rtol) / (rbot * (1 - rtol)))
    ok = (alt is None or lo >= alt) and (ust is None or hi <= ust)
    print("   %-26s VFB %.3f V ±%.1f %%, %6.2fk/%6.2fk ±%.0f %% → nominal %.3f V, en kötü %.3f…%.3f V"
          % (ad, vfb, 100 * vfb_tol, rtop / 1e3, rbot / 1e3, 100 * rtol, vn, lo, hi))
    if hedef:
        print("   %-26s hedef %.2f V: nominal sapma %+.2f %%, en kötü %+.2f / %+.2f %%; pencere %s…%s → %s"
              % ("", hedef, 100 * (vn / hedef - 1), 100 * (lo / hedef - 1), 100 * (hi / hedef - 1),
                 "%.2f" % alt if alt else "-", "%.2f" % ust if ust else "-", "GEÇTİ" if ok else "KALDI"))
    return vn, lo, hi, ok


def buck_analiz():
    hline("=")
    print("3. ESC PVDD — JW5026, R02 90.9 k / R01 10 k — DOG-015 / SYS-016 (sorumlu guc-elektronigi; katkı)")
    print("   [VAR] JW5026 VFB 0.8 V ±2 % (veri sayfası yok, E5). [FD] VCC önerilen 5–20 V, mutlak 25 V,")
    print("   VCCUV+ maks 5.0 V; VBSUV+ maks 5.0 V. Bootstrap 1N4148WT Vf ≈ 0.7–1.0 V (tahmin).")
    hline()
    vn, lo, hi, _ = buck("PVDD", 0.8, 0.02, 90.9e3, 10e3, 0.01, None, 5.0, 20.0)
    print("   PVDD penceresi FD6288Q VCC 5–20 V içinde: %s" % ("GEÇTİ" if lo >= 5 and hi <= 20 else "KALDI"))
    print("   UVLO payı (PVDD_min − VCCUV+maks) = %.2f V (ölçüt ≥ 1 V): %s"
          % (lo - 5.0, "GEÇTİ" if lo - 5.0 >= 1 else "KALDI"))
    print("   VBS = PVDD − Vf(1.0) = %.2f V; VBSUV+ maks 5.0 V payı %.2f V" % (lo - 1.0, lo - 1.0 - 5.0))
    for vin in (8.4, 9.0):
        for dmax in (0.90, 0.95):
            pv = min(vn, vin * dmax - 0.1)
            print("   VIN %.1f V, D_maks %.0f %% [VAR] → PVDD ≈ %.2f V (düşüm bölgesi), UVLO payı %.2f V, "
                  "VBS ≈ %.2f V" % (vin, 100 * dmax, pv, pv - 5.0, pv - 1.0))
    i3v3 = 4 * 10.1e-3 + 0.1e-3 + 5e-3       # [EFM8] IDD 49 MHz maks 10.1 mA ×4, INA199 ~0.1 mA [VAR], LED/çekme 5 mA [VAR]
    print("   AMS1117: 3V3 yükü ≈ %.1f mA (4 × 10.1 mA EFM8 @49 MHz [EFM8] + INA + 5 mA [VAR]); "
          "kayıp (%.2f − 3.3) × I = %.0f mW" % (i3v3 * 1e3, hi, (hi - 3.3) * i3v3 * 1e3))
    print("   Açık: JW5026 VIN maks (26.1 V + geçici 35 V?), D_maks, VFB toleransı — veri sayfası (İP-02).")

    hline("=")
    print("4. FMU BEC — TPS54202 — DOG-037 (5 V, R42 100k / R43 13.7k), DOG-039 (9 V, R32 100k / R33 7.15k)")
    print("   [ALT] fmu.SchDoc; VFB 0.596 V [boards/fmu/README.md]; VFB toleransı ±2 % [VAR — TPS54202 DS yok]")
    hline()
    r5 = buck("5 V BEC", 0.596, 0.02, 100e3, 13.7e3, 0.01, 5.0, 4.75, 5.25)
    r9 = buck("9 V BEC", 0.596, 0.02, 100e3, 7.15e3, 0.01, 9.0, 8.55, 9.45)
    # öneri: 9 V için nominali merkeze çeken E96 değer
    print("   9 V nominal −0.8 % merkez dışı. E96 alternatif R33:")
    for rb in (6.98e3, 7.06e3, 7.15e3):
        buck("  R33 = %.2fk" % (rb / 1e3), 0.596, 0.02, 100e3, rb, 0.01, 9.0, 8.55, 9.45)
    print("   Not: 9 V BEC şematik notu 'VIN 10–28 V'; 3S (9.0 V) girişte düşüm bölgesi — DOG-039/040 ayrı.")
    return r5, r9


def main():
    print("bolucu.py — Stack Ü-öncesi bölücü hesapları (test-muhendisi)")
    s = vbat_analiz()
    b = bemf_analiz()
    p = buck_analiz()
    hline("=")
    print("ÖZET")
    for k, v in s.items():
        print("  DOG-021 %-34s %s" % (k, v))
    print("  DOG-013 BEMF mux en büyük (≤26.1 V+Vd) %.3f V, 35 V geçici %.3f V, ZC kazancı %.4f" % b)
    print("  DOG-037 5 V BEC en kötü %.3f…%.3f V → %s" % (p[0][1], p[0][2], "GEÇTİ" if p[0][3] else "KALDI"))
    print("  DOG-039 9 V BEC en kötü %.3f…%.3f V → %s" % (p[1][1], p[1][2], "GEÇTİ" if p[1][3] else "KALDI"))


if __name__ == "__main__":
    main()
