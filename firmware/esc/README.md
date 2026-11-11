# ESC yazılımı — esc55a (EFM8BB21 × 4) → Bluejay düzen eşlemesi

Sahibi `gomulu-yazilim`. Tarih 2026-11-12. Ayrıntı ve kaynaklar: [`docs/rapor/yazilim-inceleme.md`](../../docs/rapor/yazilim-inceleme.md) §7.

**Sonuç: esc55a Rev B port ataması Bluejay `C` düzeniyle birebir aynı.** Yeni düzen yazılmaz, kaynak değiştirilmez, derleme gerekmez; resmî Bluejay v0.21.0 `C_H_<ölü zaman>_<PWM>` hex dosyası yüklenir (SYS-051 ✓ kaynak koduna göre; kartta DOG-051/052).

## 1. Port eşlemesi (kaynak: Rev B şematik netlisti ↔ Bluejay `src/Layouts/C.inc`)

Netlist: `kicad-cli sch export netlist boards/esc55a/esc55a/esc55a.kicad_sch` (geçici dizinde). Dört kanal (U11, U21, U31, U41) aynı.

| QFN20 pin | Port | Ağ (U11, kanal 1) | Bağlı olduğu yer | Bluejay `C` | Uyum |
|---|---|---|---|---|---|
| 2 | P0.0 | `ch1_in` | J0 M1 ← 220 Ω | `RTX_PIN EQU 0` (RX) | ✓ |
| 1 | P0.1 | boş (R99–R106 DNP) | — | kullanılmıyor (`__`) | ✓ |
| 20 | P0.2 | `ch1_com_all` | R31/R34/R37 yıldız (sanal nötr) | `V_Mux EQU 2` (Vn) | ✓ |
| 19 | P0.3 | `ch1_mux1` | R30 10 k ← M1a, R32 → GND | `A_Mux EQU 3` (Am) | ✓ |
| 18 | P0.4 | `ch1_mux2` | R33 ← M1b, R35 → GND | `B_Mux EQU 4` (Bm) | ✓ |
| 17 | P0.5 | `ch1_mux3` | R36 ← M1c, R38 → GND | `C_Mux EQU 5` (Cm) | ✓ |
| 16 | P0.6 | `ch1_hin1` | U12 HIN1 (22) → HO1 → faz a üst FET | `A_Pwm EQU 6` (Ap) | ✓ |
| 15 | P0.7 | `ch1_lin1` | U12 LIN1 (1) → LO1 → faz a alt FET | `A_Com EQU 7` (Ac) | ✓ |
| 14 | P1.0 | `ch1_hin2` | U12 HIN2 (23), faz b üst | `B_Pwm EQU 0` (Bp) | ✓ |
| 13 | P1.1 | `ch1_lin2` | U12 LIN2 (2), faz b alt | `B_Com EQU 1` (Bc) | ✓ |
| 11 | P1.2 | `ch1_hin3` | U12 HIN3 (24), faz c üst | `C_Pwm EQU 2` (Cp) | ✓ |
| 10 | P1.3 | `ch1_lin3` | U12 LIN3 (3), faz c alt | `C_Com EQU 3` (Cc) | ✓ |
| 9, 8, 7 | P1.4–P1.6 | boş | — | kullanılmıyor | ✓ |
| 5 | RSTb/C2CK | `ch1_c2ck` | C2 programlama pedi | — | — |
| 6 | P2.0/C2D | `ch1_c2d` | C2 programlama pedi | `DebugPin` (P2.0, yalnız hata ayıklama) | ✓ |

Polarite: `C` düzeni `PWM_ACTIVE_HIGH 1`, `COM_ACTIVE_HIGH 1`, `COMPARATOR_INVERT 0`. JSM6288Q1 / FD6288Q / HL6288Q’da HIN ve LIN aynı fazlı (yüksek = FET açık), dahili kilitleme var → ters çevirme gerekmez ✓.

Not (`docs/inceleme.md` §2.4 düzeltmesi): sinyal girişi QFN20 **pin 2 (P0.0)**, pin 1 değil; köprü pinleri **10, 11, 13–16** (7 değil, P1.6 boş).

## 2. MCU: EFM8BB21F16I (125 °C)

- Bluejay `MCU=H` hedefi = EFM8BB21 (`MCU_TYPE = MCU_BB2`, 49 MHz). Önyükleyici imzası derleme sabiti `0xE8 0xB2` (`Modules/Common.asm`); F16G ve F16I aynı aile/bellek, yalnız sıcaklık sınıfı farklı → **aynı hex** ✓.
- EFM8BB21 için pin uyumlu, Bluejay’de tanınan ikinci üretici yok (Bluejay yalnız EFM8BB21 `H` ve EFM8BB51 `X`; BB51 pin dizilimi farklı) → SYS-095 istisnası (RSK-021).

## 3. Ölü zaman ve PWM frekansı

- Bluejay’de ölü zaman **çalışma ayarı değil, derleme sabiti**: hex adındaki 3. alan (`DEADTIME`, `Bluejay.asm`: “20.4 ns per step”). Yayımlanan değerler 0 5 10 15 20 25 30 40 50 70 90 120.
- `guc-elektronigi` önerisi (guc-ip03 §3.5): sürücünün 200 ns’ine ek **≥ 200 ns** → `DEADTIME = 10` → 10 × 20.4 = **204 ns** (toplam ≈ 404 ns; sürücü 100 ns alt sınırında 304 ns).
- PWM frekansı da derleme sabiti (hex adındaki 4. alan); guc-ip03 §2.4 kayıp hesabı ve §3.5 → **24 kHz**.
- `DEADTIME > 0` → merkez hizalı tamamlayıcı PWM (`PWM_CENTERED`), aktif frenleme/tamamlayıcı sürme ölü zamanla korunur.

**Yüklenecek dosya:** `C_H_10_24_v0.21.0.hex` (Bluejay v0.21.0 sürüm ekleri, [GitHub release](https://github.com/bird-sanctuary/bluejay/releases/tag/v0.21.0)). esc-configurator’da “Bluejay → C_H_10 → 24 kHz” seçimi aynı dosyadır.

## 4. Yükleme yolu

| Adım | Araç | Not |
|---|---|---|
| İlk yükleme (boş MCU) | C2 arayüzü (pin 5 C2CK, pin 6 C2D, GND, 3V3 pedleri), Silabs programlayıcı veya Arduino/STM32 tabanlı C2 köprüsü | Yayımlanan hex BLHeli önyükleyicisini içerir (`BLHeliBootLoad.inc`, 0x1C00) |
| Güncelleme | Betaflight passthrough (4-way interface) + esc-configurator.com | Önyükleyici sinyal hattından |
| Ayarlar | esc-configurator | Yön, başlangıç gücü, sıcaklık koruması (aşağıda) |

## 5. Güvenlik davranışı (Bluejay v0.21.0 kaynak kodundan)

| Durum | Davranış | Kanıt / ayar |
|---|---|---|
| Açılışta | Yalnız DShot300/600 sinyali kabul edilir; ≈ 300 ms kesintisiz sıfır gaz görülmeden silahlanmaz (arm), motor dönmez | `arming_begin` / `arming_wait` (`Rcp_Stop_Cnt ≥ 10`) |
| Sinyal kopması | Zaman aşımında motor durur, “sinyal kayıp” bip | `Rcp_Timeout_Cntd`, `beep_signal_lost` |
| Aşırı sıcaklık | **Varsayılan kapalı** (`DEFAULT_PGM_ENABLE_TEMP_PROT EQU 0`); 1…7 = 80…140 °C, MCU iç sensörü | Eşik `sistem-mimari` / `guc-elektronigi` kararı (MCU T_J ≤ 130 °C; öneri 5 = 120 °C) — açık konu |
| Aşırı akım | Bluejay’de akım sınırı **yok** (ESC akım ölçümü yalnız FMU’ya) | FMU tarafında Betaflight akım limiti / sigorta |
| Düşük devirde güç | `Pgm_Rpm_Power_Slope`, başlangıç gücü sınırı | varsayılan |

## 6. Kartta yapılacak kontroller

1. Dört kanalda C2 ile yükleme, esc-configurator’da “C_H_10” tanınması.
2. Çift yönlü DShot (Betaflight `dshot_bidir ON`) ile devir okuması, 8 motorda `dshot telemetry info`.
3. Ölü zaman ölçümü: HO/LO kapı dalga şekli, kanal başı (DOG’a `test-muhendisi` ekler).
4. Yön, sinyal kopma ve açılışta dönmeme testi.
