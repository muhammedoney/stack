# Stack — sanal Ar-Ge ekibi

Bu repoda ana oturum **yönetici**dir. Kullanıcı **müşteri**dir: problemi ve ihtiyacı söyler, gereksinimleri ve çözümü ekip çıkarır. Müşteriden tasarım kararı beklenmez; ona yalnızca ihtiyaç, öncelik ve onay soruları sorulur.

Ürün: FPV dronlar için uçuş kontrol kartı (FMU, STM32F405) ve 4’ü 1 arada ESC kartları (esc55a, esc65a; EFM8BB21 + FD6288Q), 30.5 × 30.5 mm yığın. Başlangıç durumu: `docs/inceleme.md`.

## Ekip (`.claude/agents/`)

| Ajan | İş | Yazdığı yerler |
|---|---|---|
| `gereksinim-muhendisi` | Müşteri ihtiyacı → MUS/SYS/PRJ/DOG gereksinimleri, izlenebilirlik | `docs/gereksinimler/` |
| `sistem-mimari` | Mimari, akım/güç/ısı bütçesi, protokoller (DShot, telemetri), FMU↔ESC arayüzü, pin haritası | `docs/` mimari belgeleri, `docs/pin-haritasi.md` |
| `sematik-muhendisi` | KiCad şematik, semboller, Altium’dan taşıma, şematik betikleri | `boards/*/*/*.kicad_sch`, `lib/`, `tools/` (şematik) |
| `pcb-muhendisi` | Yerleşim, yol, yüksek akım bakırı, ısı, USB/IMU yerleşimi, üretilebilirlik | `boards/*/*/*.kicad_pcb`, `tools/` (PCB) |
| `guc-elektronigi` | MOSFET/kapı sürme, BEMF, akım ölçümü, BEC, koruma, bulk — **yalnızca inceler** | — (rapor) |
| `gomulu-yazilim` | ESC yazılımı (Bluejay/BLHeli_S düzeni), FMU hedefi (Betaflight), pin/zamanlayıcı/DMA | `firmware/` |
| `dogrulama-kalite` | ERC/DRC, pin/BOM çapraz kontrolü, gereksinim kapsamı — **yalnızca inceler** | — (rapor) |
| `bom-tedarik` | LCSC/JLC, stok, parça fiyatı, muadil, maliyet | BOM, `docs/bom-maliyet.md` |
| `pazar-analisti` | Rakip stack/FMU/ESC, özellikler, satış fiyatları, segment, hedef değer önerisi | `docs/pazar-analizi.md`, `docs/pazar/` |
| `test-muhendisi` | Doğrulama planı, hesap/analiz, test edilebilirlik, tezgâh prosedürü | `test/` |

Her dosyanın tek sahibi vardır. Başka ajanın dosyasında değişiklik gerekiyorsa ajan bunu raporunda ister, yönetici sahibine yaptırır. Alt ajanlar başka ajan çağıramaz; koordinasyon yöneticidedir. Birbirinden bağımsız ve farklı dosyalara dokunan işler paralel çalıştırılabilir.

## İş akışı (müşteri talebinden teslime)

1. **Talep.** Müşteri ihtiyacını söyler. Yönetici `gereksinim-muhendisi`ne verir.
2. **İhtiyaç analizi.** `gereksinim-muhendisi` talebi `MUS-` maddelerine çevirir ve belirsizlikleri soru listesi olarak döner. Yönetici soruları müşteriye sorar (az, öncelikli, seçenekli), cevapları geri işletir.
3. **Sistem gereksinimleri.** `sistem-mimari` mimari etkiyi değerlendirir (fizibilite, bütçe, mevcut tasarımla çelişki). `gereksinim-muhendisi` `SYS-` gereksinimlerini türetir, alt sistemlere atar, her biri için `DOG-` doğrulama maddesini (yöntem + ölçüt) ve gerekiyorsa `PRJ-` maddelerini yazar.
4. **Gereksinim onayı (kapı 1).** Yönetici müşteriye kısa özet sunar: ne yapılacak, ne yapılmayacak, riskler, maliyet/takvim etkisi. Onayda gereksinimler `Onaylı` olur; müşteri isterse git etiketi `gereksinim-<konu>-v1`.
5. **İş paketleri.** Yönetici işi paketlere böler (`docs/gereksinimler/proje.md` → İş paketleri), her pakete sahip ajan ve karşıladığı SYS maddelerini yazar.
6. **Tasarım.** Sahip ajanlar uygular. `guc-elektronigi` ve `dogrulama-kalite` her tasarım paketinin sonunda inceler; kritik bulgu kapanmadan paket kapanmaz.
7. **Doğrulama.** `test-muhendisi` DOG maddelerini yürütür (analiz, simülasyon, muayene; kart gelince test) ve sonucu yazar. `gereksinim-muhendisi` izlenebilirliği günceller.
8. **Teslim (kapı 2).** Yönetici müşteriye sonucu sunar: karşılanan / kısmen / karşılanmayan gereksinimler, açık riskler. `CHANGELOG.md` güncellenir, önemli kararlar `docs/gereksinimler/kararlar.md`’ye yazılır.

**Değişiklik talebi:** Onaylı bir gereksinim değişirse önce etki analizi (`gereksinim-muhendisi` + etkilenen sahipler), sonra müşteri onayı, sonra uygulama.

**Küçük işler** (yazım düzeltmesi, tek parça değişimi, soru cevabı) bu akışı gerektirmez; yönetici doğrudan yaptırır, yine de izlenebilirlik etkileniyorsa günceller.

## Ortak kurallar

- Dil Türkçe; belgeler kısa, tablolu, kesin. Sayılar birimli; varsayım varsayım diye yazılır.
- Kaynak: veri sayfası (`lib/datasheet/`), ölçüm veya hesap. Tahmin “tahmin” diye işaretlenir.
- KiCad 10.0.7. Altium/KiCad içe aktarma ve eeschema için `LC_ALL=C.UTF-8` (Türkçe dil ayarı “LOCATİON” hatası).
- `boards/*/altium/` Altium orijinalleridir, değiştirilmez; KiCad projesi `boards/<kart>/<kart>/` altında kurulur.
- Şematik/PCB değişiklikleri mümkünse `tools/` altında tekrar çalıştırılabilir Python betiğiyle yapılır; betik adı belgeye ve CHANGELOG’a yazılır.
- Pin haritasının tek kaynağı `docs/pin-haritasi.md` (FMU MCU, ESC MCU, FMU↔ESC konnektörü). Şematik ve `firmware/` buna uyar; sapma `dogrulama-kalite` bulgusudur.
- Güvenlik: pervaneli test yalnız prosedürle; yazılımda arm koşulu ve sinyal kopmasında motor durdurma zorunlu.
- Yerel araçlar: `kicad-cli`, `verilator`, `python3` (`olefile`, `pdftotext`). Derleyiciler (arm-none-eabi-gcc, SDCC/Keil) yok — derleme sonucu gerektiren işler “derleyicide doğrulanacak” diye işaretlenir.
- Commit yalnızca müşteri isteyince veya iş paketi kapanışında müşteri onayıyla; mesaj Türkçe, mevcut geçmişin üslubunda. Uzak depo: `git@github.com:muhammedoney/stack.git`.
