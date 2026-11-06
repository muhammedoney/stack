# Stack — FPV uçuş kontrol ve ESC kartları

**Stack**, FPV dronlar için bir uçuş kontrol kartı (FMU) ile 4’ü 1 arada ESC kartlarından oluşan, 30.5 × 30.5 mm montaj desenli bir yığındır. Tasarımlar cezeri reposundaki Altium çalışmalarından ve piyasadaki kartların tersine mühendisliğinden geliyor; KiCad 10’a taşınacak.

```
  RC alıcı / VTX / GPS ─► [ FMU: STM32F405, ICM-42688-P, BMP388, OSD, 9 V + 5 V BEC ] ─ 8 pin SM08B ─► [ ESC: 4 × EFM8BB21 + FD6288Q + 24 MOSFET ] ─► 4 motor
                                                    ▲                                                         │
                                                    └──────────────── CUR (akım), VBAT ◄──────────────────────┘
```

## Durum (2026-11-06)

| Kart | Kaynak | Şematik | PCB | Yazılım |
|---|---|---|---|---|
| [esc55a](boards/esc55a/README.md) — 4’ü 1 arada 55 A | Altium | 3 sayfa, 232 parça | 4 katman, 41 × 48 mm, yollu (bağlanmamış 0) | BLHeli_S/Bluejay düzeni doğrulanacak |
| esc65a — 4’ü 1 arada 65 A | drawio | yok (16 fotoğraf, 2 parça etiketi) | yok | — |
| [fmu](boards/fmu/README.md) — F405 uçuş kontrol | Altium | 1 sayfa, 143 parça | yok | Betaflight hedefi yazılacak |

Altium projeleri `boards/*/altium/` altında olduğu gibi duruyor; KiCad’e taşınmadı. Bulgular ve önerilen sıra: [docs/inceleme.md](docs/inceleme.md). Gereksinimler: 5" stack için 56 SYS, 90 DOG (53 Ü-öncesi) taslak; kapı 1 onayı bekleniyor ([docs/gereksinimler](docs/gereksinimler/README.md)).

## Belgeler

| Belge | İçerik |
|---|---|
| [İlk inceleme](docs/inceleme.md) | Kopyalanan dosyalar, mimari, hesaplar, bulgular (E1–E12, F1–F7), önerilen sıra |
| [Pazar analizi](docs/pazar-analizi.md) | Rakip stack’ler, özellikler, fiyatlar, hedef değer önerisi; ham veri `docs/pazar/rakipler.csv` |
| [BOM ve maliyet](docs/bom-maliyet.md) | 5" stack 5 / 100 / 1000 set maliyeti, muadiller, maliyet azaltma seçenekleri; ham BOM `boards/*/bom-maliyet.csv` |
| [Gereksinimler](docs/gereksinimler/README.md) | MUS/SYS/PRJ/DOG kaydı, açık sorular |
| `docs/esc55a.drawio`, `docs/esc65a.drawio` | ESC tersine mühendislik çizimleri |
| `docs/fmu-diatone-f405mk2.drawio`, `docs/fmu-geprc-f405-hd-v3.drawio` | FMU referans kart çizimleri; görseller `docs/reference/fmu/` |
| [CHANGELOG](CHANGELOG.md) | Değişiklik geçmişi |

## Klasörler

| Klasör | İçerik |
|---|---|
| `boards/` | Kart başına klasör: `altium/` (orijinal), `<ad>/` (KiCad projesi, taşımadan sonra), `README.md` |
| `lib/` | Ortak KiCad kütüphanesi (taşımada kurulacak); `lib/datasheet/` veri sayfaları |
| `firmware/` | ESC (Bluejay/BLHeli_S düzeni) ve FMU (Betaflight hedefi) yazılım dosyaları |
| `docs/` | Belgeler, drawio çizimleri, `docs/gereksinimler/`, `docs/reference/` |
| `test/` | Analiz betikleri, prosedürler, DOG sonuçları |
| `tools/` | Python betikleri: `altium_sch_dump.py` (SchDoc parça/ağ dökümü), `pcb_stat.py` (içe aktarılmış PCB özeti), `drawio_dump.py` |

## Geliştirici notları

Altium dosyalarını incelemek için (repo dışına, geçici dizine):

```bash
python3 -I tools/altium_sch_dump.py boards/esc55a/altium/main.SchDoc
```

```bash
LC_ALL=C.UTF-8 kicad-cli pcb import --format altium -o /tmp/esc55a.kicad_pcb boards/esc55a/altium/ESC_v0.PcbDoc
```

**Türkçe dil ayarı:** KiCad 10.0.7’nin Altium okuyucusu alan adlarını sistem diliyle büyük harfe çeviriyor; Türkçede “Location” “LOCATİON” olur. İçe aktarmayı `LC_ALL=C.UTF-8` ile yapın.
