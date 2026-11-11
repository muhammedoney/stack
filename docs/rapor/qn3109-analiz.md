# QN3109 (Mamba F55 / GEPRC 55–60 A) — 4 kanal sürekli 55 A verebilir mi? (2026-11-11)

Soru (müşteri): Diatone Mamba 55 A ESC’de (EFM8BB21F16G) ve elimizdeki GEPRC stack ESC’sinde (FD6288Q, LF1026) **QN3109** MOSFET var (gövde yazısı “QN3109 / 418 / 43E”). Bu ESC tüm kanallardan sürekli 55 A verebilir mi?

Yöntem: `docs/rapor/guc-ip03.md` §2.4–2.5’teki kayıp ve kart ısıl modeli, aynı varsayımlarla (6S LiHV 26.1 V, 24 kHz PWM, 25 °C ortam, R_kart-hava 2.0 K/W ≈ 5 m/s hava + kablolar; ölçüt kılıf ≤ 110 °C, T_j ≤ T_j,maks − 15 °C). Rakip kartın bakır kalınlığı, iç katmanı, soğutucusu bilinmiyor; bizim esc55a kartıyla aynı boy ve yapı **varsayıldı** (tahmin).

## QN3109M6N (UBIQ) veri sayfası — `lib/datasheet/UBIQ-QN3109M6N.pdf` (Rev A.03, 2017)

| | QN3109M6N | Bizim seçim BLP016N04LC-Q |
|---|---|---|
| V_DS | **30 V** | 40 V |
| R_DS(on) 10 V tip / maks | 1.35 / 1.62 mΩ | 1.25 / 1.6 mΩ |
| R_DS(on) 4.5 V tip / maks | 1.9 / 2.5 mΩ | — / 2.4 mΩ |
| Q_g 10 V / Q_gd | 46.3 / 6.8 nC | 61 / 8.2 nC |
| Crss / Ciss | 44 / 3100 pF | 65 / — pF |
| Qrr | 67.1 nC | 80 nC |
| RθJC | 2.2 K/W | 1.3 K/W |
| T_j maks | 150 °C | 175 °C |
| “154 A” | T_C = 25 °C, paket sınırı; **T_A = 25 °C’de 29 A** (1 inç², 2 oz) | |

“154 A” kılıf 25 °C’de tutulursa geçerli kâğıt değeri; gerçek kartta sınırlayan kartın ısı atması.

## Sonuç (model, tahmin ±%50)

| Durum | QN3109 | BLP016 (bizim) |
|---|---|---|
| Kanal başına kayıp, 55 A, R_G 10 Ω | 15.3 W | 15.3 W |
| 4 × 55 A sürekli kart kaybı (FET’ler) | **≈ 61 W** | ≈ 61 W |
| Kartın atabildiği (5 m/s, 95 °C) | ≈ 35 W | ≈ 35 W |
| **4 kanal sürekli** (5 m/s; anahtarlamalı / tam gaz) | **≈ 35 / 39 A** | ≈ 34 / 40 A |
| 4 kanal sürekli, iyi hava (1.6 K/W) | ≈ 39 / 43 A | ≈ 38 / 45 A |
| 4 kanal sürekli, havasız (4.9 K/W) | ≈ 22 / 26 A | ≈ 21 / 26 A |
| 4 × 55 A, 10 s (T_j ölçütü) | **tutar** (T_j ≈ 119 °C, kılıf ≈ 112 °C) | tutar |
| Tek kanal sürekli | ≈ 60 A (tahmin, BLP ile aynı sınıf) | ≈ 62 A |

**Cevap: Hayır.** QN3109’lu Mamba/GEPRC ESC’si — bizim kartla aynı boy ve yapıdaysa — dört kanaldan aynı anda sürekli 55 A veremez; 5 m/s havada ≈ 35–39 A sürekli, 4 × 55 A’yı ≈ 10 s, tek kanalı ≈ 55–60 A sürekli taşır. Sınırlayan MOSFET değil, 41 × 48 mm kartın ısı atma kapasitesi; QN3109 ile bizim BLP016 ısıl olarak aynı sınıftadır. Bu, pazar analizindeki bulguyla (§8: “55 A” = tek kanal / süresi belirsiz sürekli değer) tutarlı.

## Notlar

- **Gerilim:** QN3109 30 V. 6S LiHV’de (26.1 V) pay %13; pazardaki 55 A ESC’lerin çoğu 30 V FET’le 6S satıyor. Bizim 40 V seçimimiz (SYS-014, geçici ≤ 35 V + 5 V) daha korumacı; maliyet farkı ≈ +1.6 $/stack (guc-ip03 §2.7).
- Eski esc55a Altium tasarımı ME7170 kullanıyor; tersine mühendislik yapılan gerçek kartlarda QN3109 var (`docs/esc55a.drawio`, `docs/esc65a.drawio`).
- Doğrulama: elimizdeki GEPRC stack ESC’si **DOG-005 düzeneğinde ölçülebilir** (4 kanal yük, ısıl kamera) — hem bu hesabı hem “pazar eşdeğeri” iddiasını kanıtlar (`pazar-analizi.md` §8 önerisi). Prosedür `test-muhendisi`.
- Hesap: guc-ip03 betikleri (`mos.py`, `isil.py`, `isil2.py`) + QN3109 satırı; betikler henüz `test/analiz/`’e taşınmadı (`test-muhendisi` işi).
