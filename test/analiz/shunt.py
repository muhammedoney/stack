#!/usr/bin/env python3
"""Ü-öncesi akım ölçümü hesabı: shunt × yükselteç → tam ölçek, güç, doğruluk (test-muhendisi, İP-08).

DOG bağı (sorumlu guc-elektronigi; bu betik hesap katkısıdır):
  DOG-017 / SYS-020  tam ölçek ≥ 280 A, CUR ≤ 3.3 V, yükselteç V_CM
  DOG-019 / SYS-021  10–200 A ±%5, < 10 A ±1 A (tip ölçek, kart başına kalibrasyon yok)
  DOG-008 / SYS-012  ölçüm elemanı gücü 220 A sürekli / 280 A 10 s, sınıfın ≤ %70'i (yalnız eleman)

Kullanım:
  python3 -I test/analiz/shunt.py                      # tüm aday tablosu
  python3 -I test/analiz/shunt.py --r 0.1e-3 --n 2 --amp INA240A3 --p 3
      (--r: toplam shunt direnci Ω, --n: paralel eleman sayısı, --p: eleman güç sınıfı W)

Girdiler ve kaynakları:
  [ALT]  R00 ‖ R000 = 2 × 1 mΩ 2512 (TA-I RLM25FEER001), U2 INA199C1 (kazanç 200) — esc55a main.SchDoc,
         docs/inceleme.md §2.2 (E1, E2); boards/esc55a/bom-maliyet.csv
  [STM32] lib/datasheet/STM32F405RGT6.pdf Tablo 68: ET ±5 LSB; VREF+ = VDDA (LQFP64)
  [VAR]  yükselteç ve shunt veri sayfaları yerelde YOK (E5, İP-02): INA199 / INA240 değerleri TI
         genel özelliklerinden alınmış varsayımdır (VOS maks, kazanç hatası, V_CM, çıkış salınımı);
         shunt güç sınıfı ve TCR üretici sınıfı varsayımıdır. bom-tedarik veri sayfasını eklediğinde
         YUKSELTEC / ADAYLAR tabloları güncellenip betik yeniden çalıştırılır.
"""
import argparse
import math

I_SUREKLI = 220.0       # A, SYS-012 (4 × 55 A)
I_ANLIK = 280.0         # A, SYS-011/012 (4 × 70 A, 10 s)
P_ORAN = 0.70           # DOG-008: eleman gücü ≤ sınıfın %70'i
V_ESC_3V3 = 3.3         # ESC AMS1117 çıkışı (yükselteç beslemesi)
V_ESC_3V3_TOL = 0.015   # [VAR] AMS1117 ±%1.5
V_ADC_REF = 3.3         # FMU VDDA
ADC_ET_LSB = 5.0        # [STM32]
T_ORTAM = (-10.0, 50.0)  # SYS-083
DT_SHUNT = 60.0         # [VAR] shunt öz ısınması 220 A'da (DOG-004/008 ısıl modeli gelince güncellenir)
V_CM_MAX = 26.1 + 0.0   # SYS-013 sürekli; geçici 35 V (SYS-014) ayrıca kontrol

YUKSELTEC = {
    # ad: kazanç, VOS maks (V), kazanç hatası maks, V_CM maks (V), çıkış tavanı (V+ - x), fiyat notu
    "INA199A1": dict(g=50, vos=150e-6, ge=0.015, vcm=26.0, sw=0.2, fiyat="mevcut aile"),   # [VAR]
    "INA199B1": dict(g=100, vos=150e-6, ge=0.015, vcm=26.0, sw=0.2, fiyat="mevcut aile"),  # [VAR]
    "INA199C1": dict(g=200, vos=150e-6, ge=0.015, vcm=26.0, sw=0.2, fiyat="0.53 $ (bom)"),  # [ALT] parça, [VAR] özellik
    "INA240A1": dict(g=20, vos=25e-6, ge=0.002, vcm=80.0, sw=0.05, fiyat="tahmin 1–1.5 $"),  # [VAR]
    "INA240A2": dict(g=50, vos=25e-6, ge=0.002, vcm=80.0, sw=0.05, fiyat="tahmin 1–1.5 $"),  # [VAR]
    "INA240A3": dict(g=100, vos=25e-6, ge=0.002, vcm=80.0, sw=0.05, fiyat="tahmin 1–1.5 $"),  # [VAR]
}

ADAYLAR = [
    # ad, toplam R (Ω), paralel eleman, eleman sınıfı (W), tolerans, TCR (ppm/K), yükselteç
    dict(ad="MEVCUT 2×1mΩ 2512 + INA199C1", r=0.5e-3, n=2, p=2.0, tol=0.01, tcr=75e-6, amp="INA199C1"),
    dict(ad="2×1mΩ + INA199A1", r=0.5e-3, n=2, p=2.0, tol=0.01, tcr=75e-6, amp="INA199A1"),
    dict(ad="2×0.5mΩ (0.25) + INA199A1 [E1 önerisi]", r=0.25e-3, n=2, p=3.0, tol=0.01, tcr=75e-6, amp="INA199A1"),
    dict(ad="2×0.3mΩ (0.15) + INA199A1", r=0.15e-3, n=2, p=3.0, tol=0.01, tcr=75e-6, amp="INA199A1"),
    dict(ad="2×0.2mΩ (0.10) + INA199B1", r=0.10e-3, n=2, p=3.0, tol=0.01, tcr=75e-6, amp="INA199B1"),
    dict(ad="4×0.4mΩ (0.10) + INA199B1", r=0.10e-3, n=4, p=3.0, tol=0.01, tcr=75e-6, amp="INA199B1"),
    dict(ad="2×0.3mΩ (0.15) + INA240A2", r=0.15e-3, n=2, p=3.0, tol=0.01, tcr=75e-6, amp="INA240A2"),
    dict(ad="2×0.2mΩ (0.10) + INA240A3", r=0.10e-3, n=2, p=3.0, tol=0.01, tcr=75e-6, amp="INA240A3"),
    dict(ad="4×0.4mΩ (0.10) + INA240A3", r=0.10e-3, n=4, p=3.0, tol=0.01, tcr=75e-6, amp="INA240A3"),
    dict(ad="4×0.5mΩ (0.125) + INA240A3", r=0.125e-3, n=4, p=3.0, tol=0.01, tcr=75e-6, amp="INA240A3"),
]

NOKTALAR = (1.0, 5.0, 10.0, 30.0, 60.0, 100.0, 200.0)


def bf_scale(mv_per_a):
    """Betaflight ibata_scale birimi 0.1 mV/A (tamsayı) [VAR: gomulu-yazilim doğrulasın]."""
    s = int(round(mv_per_a * 10))
    return s, s / 10.0


def analiz(a, ayrinti=True):
    amp = YUKSELTEC[a["amp"]]
    g, r = amp["g"], a["r"]
    k = r * g                                   # V/A
    mva = k * 1e3
    scale, mva_bf = bf_scale(mva)
    v_tavan = V_ESC_3V3 * (1 - V_ESC_3V3_TOL) - amp["sw"]
    v_tavan = min(v_tavan, V_ADC_REF * (1 - 0.02))      # FMU ADC tavanı (VDDA −%2 en kötü)
    fs_nom = (V_ESC_3V3 - amp["sw"]) / k
    k_max = r * (1 + a["tol"]) * (1 + a["tcr"] * (T_ORTAM[1] + DT_SHUNT - 25)) * g * (1 + amp["ge"])
    fs_min = (v_tavan - amp["vos"] * g) / k_max
    p_el_s = I_SUREKLI ** 2 * r / a["n"]
    p_el_a = I_ANLIK ** 2 * r / a["n"]
    p_ok = p_el_s <= P_ORAN * a["p"] and p_el_a <= P_ORAN * a["p"] * 1.0
    p_ok_10s = p_el_a <= a["p"]                         # 10 s darbede sınıfı aşmama (gevşek)
    fs_ok = fs_min >= I_ANLIK
    vcm_ok = amp["vcm"] >= 26.1
    vcm35_ok = amp["vcm"] >= 35.0
    # doğruluk (tip ölçek, ofset kalibrasyonu yok): bileşenlerin en kötü toplamı ve RSS
    vref_err = 0.003                                    # VREFINT telafisi (bolucu.py ile aynı) ya da
    vref_err_ldo = 0.02                                 # telafisiz LDO
    tcr_err = a["tcr"] * max(25 - T_ORTAM[0], T_ORTAM[1] + DT_SHUNT - 25)
    q_err = abs(mva_bf / mva - 1)
    lsb_a = V_ADC_REF / 4096 / k
    satirlar = []
    dog019_ok = True
    dog019_alt_ok = True          # öneri ölçüt: max(%5, 1 A) — 10 A'daki süreksizliği kaldırır
    for i in NOKTALAR:
        rel = [a["tol"], tcr_err, amp["ge"], vref_err, q_err]
        add = [amp["vos"] / r, ADC_ET_LSB * lsb_a]
        wc = i * sum(rel) + sum(add)
        rss = math.sqrt(sum((i * x) ** 2 for x in rel) + sum(x * x for x in add))
        wc_ldo = wc + i * (vref_err_ldo - vref_err)
        lim = 1.0 if i < 10 else 0.05 * i
        ok = wc <= lim
        dog019_ok &= ok
        dog019_alt_ok &= wc <= max(0.05 * i, 1.0)
        satirlar.append((i, lim, wc, rss, wc_ldo, ok))
    if ayrinti:
        print("%s" % a["ad"])
        print("   R = %.3f mΩ (%d × %.3f mΩ), %s kazanç %d → %.2f mV/A; Betaflight ibata_scale %d (kuantalama %+.2f %%)"
              % (r * 1e3, a["n"], r * a["n"] * 1e3, a["amp"], g, mva, scale, 100 * (mva_bf / mva - 1)))
        print("   Tam ölçek: nominal %.0f A, en kötü (R+tol+TCR, G+hata, tavan %.2f V) %.0f A → ≥ 280 A %s"
              % (fs_nom, v_tavan, fs_min, "GEÇTİ" if fs_ok else "KALDI"))
        print("   Eleman gücü: 220 A'da %.2f W, 280 A'da %.2f W; sınıf %.1f W × %%70 = %.2f W → %s"
              % (p_el_s, p_el_a, a["p"], P_ORAN * a["p"],
                 "GEÇTİ" if p_ok else ("KALDI (10 s darbede sınıf içinde)" if p_ok_10s and p_el_s <= P_ORAN * a["p"]
                                      else "KALDI")))
        print("   Toplam shunt kaybı 220 A'da %.1f W, 280 A'da %.1f W" % (I_SUREKLI ** 2 * r, I_ANLIK ** 2 * r))
        print("   V_CM maks %.0f V: 26.1 V %s, 35 V geçici %s; CUR tavanı = yükselteç beslemesi (ESC 3.3 V) "
              "→ CUR ≤ 3.3 V koşullu*"
              % (amp["vcm"], "GEÇTİ" if vcm_ok else "KALDI", "GEÇTİ" if vcm35_ok else "KALDI"))
        print("   Doğruluk (VOS %.0f µV → %.2f A; ADC 5 LSB → %.2f A; TCR %.2f %%):"
              % (amp["vos"] * 1e6, amp["vos"] / r, ADC_ET_LSB * lsb_a, 100 * tcr_err))
        print("   %7s %7s %9s %7s %12s  %s" % ("I (A)", "sınır", "en kötü", "RSS", "LDO ref ile", "durum"))
        for i, lim, wc, rss, wcl, ok in satirlar:
            print("   %7.0f %7.2f %9.2f %7.2f %12.2f  %s"
                  % (i, lim, wc, rss, wcl, "GEÇTİ" if ok else ("RSS'te geçer" if rss <= lim else "KALDI")))
        print("-" * 96)
    return dict(fs_min=fs_min, fs_ok=fs_ok, p_ok=p_ok, vcm_ok=vcm_ok, vcm35_ok=vcm35_ok,
                dog019_ok=dog019_ok, dog019_alt_ok=dog019_alt_ok, p_el_s=p_el_s, p_el_a=p_el_a)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--r", type=float, help="toplam shunt direnci (Ω)")
    ap.add_argument("--n", type=int, default=1, help="paralel eleman sayısı")
    ap.add_argument("--p", type=float, default=3.0, help="eleman güç sınıfı (W)")
    ap.add_argument("--tol", type=float, default=0.01)
    ap.add_argument("--tcr", type=float, default=75e-6)
    ap.add_argument("--amp", default="INA240A3", choices=sorted(YUKSELTEC))
    arg = ap.parse_args()
    print("shunt.py — Stack akım ölçümü (DOG-017, DOG-019, DOG-008 eleman gücü)")
    print("Ölçüt: tam ölçek ≥ 280 A (en kötü); eleman gücü 220 A ve 280 A'da ≤ sınıfın %70'i;")
    print("       10–200 A ±%5, < 10 A ±1 A (tip ölçek, VREFINT telafili ADC varsayımı; 'LDO ref ile' sütunu telafisiz)")
    print("Varsayım: shunt öz ısınması %.0f K, ortam −10…+50 °C, Kelvin bağlantı (PCB bakırı ölçüm yolunda değil)" % DT_SHUNT)
    print("=" * 96)
    if arg.r:
        analiz(dict(ad="KOMUT SATIRI", r=arg.r, n=arg.n, p=arg.p, tol=arg.tol, tcr=arg.tcr, amp=arg.amp))
        return
    ozet = []
    for a in ADAYLAR:  # noqa
        ozet.append((a["ad"], analiz(a)))
    print("ÖZET  (FS = en kötü tam ölçek)")
    print("%-42s %7s %6s %7s %6s %7s %7s %8s" % ("Aday", "FS (A)", "FS", "güç", "VCM26", "VCM35", "DOG019",
                                                "019-alt"))
    for ad, o in ozet:
        print("%-42s %7.0f %6s %7s %6s %7s %7s %8s"
              % (ad, o["fs_min"], "ok" if o["fs_ok"] else "KALDI", "ok" if o["p_ok"] else "KALDI",
                 "ok" if o["vcm_ok"] else "KALDI", "ok" if o["vcm35_ok"] else "KALDI",
                 "ok" if o["dog019_ok"] else "KALDI", "ok" if o["dog019_alt_ok"] else "KALDI"))
    print("019-alt: ölçüt max(%5 × I, 1 A) ile (SYS-021 metninde 10 A'da 1 A → 0.5 A süreksizliği var; öneri).")
    print("* CUR, yükselteç beslemesini (ESC 3.3 V) aşamaz; ESC 3.3 V > FMU VDDA ise fark kadar (≤ ~0.1 V) ADC pinine")
    print("  enjeksiyon olur — FMU tarafında CUR hattına seri 1 k (enjeksiyon < 0.1 mA) önerilir.")


if __name__ == "__main__":
    main()
