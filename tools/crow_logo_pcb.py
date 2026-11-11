#!/usr/bin/env python3
"""Crow PCB silkscreen logo: clean vector beak mark, KiCad footprints + previews.

The silkscreen mark is the beak silhouette of docs/pazar/crow-fpv-logo.jpg drawn
as one solid polygon (no raster tracing, no letters cut into it: at 6-8 mm the
letter holes are below JLC silkscreen limits and do not print). The word "CROW"
is a separate KiCad stroke-font text next to the mark, in the "_Text" variant.

JLC silkscreen limits used: line >= 0.153 mm, text height >= 1.0 mm.
Text: 6 mm mark -> 1.2 mm / 0.18 mm, 8 mm mark -> 1.6 mm / 0.2 mm.

Outputs (written every run, deterministic):
  lib/stack.pretty/Crow_Logo_{6,8}mm.kicad_mod        mark only (F.SilkS)
  lib/stack.pretty/Crow_Logo_Text_{6,8}mm.kicad_mod   mark + "CROW" stroke text
  docs/pazar/crow-fpv-logo-pcb.{svg,dxf,jpg}          8 mm mark (+ text preview)

Usage:  python3 tools/crow_logo_pcb.py
"""
from __future__ import annotations

import uuid
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PRETTY = ROOT / "lib" / "stack.pretty"
DOCS = ROOT / "docs" / "pazar"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Beak silhouette (outer contour of the earlier traced mark, cleaned: notch and
# letter holes removed). Units: source pixels, y down. Beak tip points right-down.
BEAK = [(322, 366), (478, 366), (594, 439), (694, 542), (739, 626),
        (667, 593), (540, 564), (367, 672), (449, 550), (449, 445)]

def text_size(width_mm: float):
    """CROW text height/stroke: 0.2 x mark width, never below JLC limits (1.0 / 0.153 mm)."""
    h = max(1.2, round(0.2 * width_mm, 2))
    return h, max(0.18, round(h * 0.125, 3))


def norm(width_mm: float):
    """Polygon in mm, origin at the mark centre, y down (KiCad)."""
    xs = [p[0] for p in BEAK]
    ys = [p[1] for p in BEAK]
    s = width_mm / (max(xs) - min(xs))
    cx = (max(xs) + min(xs)) / 2
    cy = (max(ys) + min(ys)) / 2
    pts = [((x - cx) * s, (y - cy) * s) for x, y in BEAK]
    return pts, (max(ys) - min(ys)) * s


def uid(name: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "stack/crow/" + name))


def footprint(name: str, width_mm: float, text: bool) -> str:
    pts, h = norm(width_mm)
    xy = " ".join(f"(xy {x:.4f} {y:.4f})" for x, y in pts)
    tx = width_mm / 2 + 0.6  # text starts 0.6 mm right of the mark
    th, tw = text_size(width_mm)
    lines = [
        f'(footprint "{name}"',
        '\t(version 20241229)',
        '\t(generator "stack_crow_logo")',
        '\t(layer "F.Cu")',
        f'\t(descr "Crow FPV silkscreen mark, {width_mm:g} mm wide{" + CROW text" if text else ""}; tools/crow_logo_pcb.py")',
        '\t(attr exclude_from_pos_files exclude_from_bom allow_missing_courtyard)',
        f'\t(property "Reference" "LOGO**" (at 0 {-h / 2 - 1:.3f} 0) (layer "F.SilkS") (hide yes) (uuid "{uid(name + "/ref")}")',
        '\t\t(effects (font (size 1 1) (thickness 0.15))))',
        f'\t(property "Value" "{name}" (at 0 {h / 2 + 1:.3f} 0) (layer "F.Fab") (hide yes) (uuid "{uid(name + "/val")}")',
        '\t\t(effects (font (size 1 1) (thickness 0.15))))',
        f'\t(fp_poly (pts {xy}) (stroke (width 0) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{uid(name + "/poly")}"))',
    ]
    if text:
        lines += [
            f'\t(fp_text user "CROW" (at {tx:.3f} 0 0) (layer "F.SilkS") (uuid "{uid(name + "/txt")}")',
            f'\t\t(effects (font (size {th} {th}) (thickness {tw}) (bold yes)) (justify left)))',
        ]
    lines.append(")")
    return "\n".join(lines) + "\n"


def write_svg(path: Path, width_mm: float):
    pts, h = norm(width_mm)
    d = "M " + " L ".join(f"{x + width_mm / 2:.4f} {y + h / 2:.4f}" for x, y in pts) + " Z"
    path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm:.3f}mm" height="{h:.3f}mm" '
        f'viewBox="0 0 {width_mm:.4f} {h:.4f}">\n'
        f'<path fill="white" d="{d}"/>\n</svg>\n', encoding="utf-8")


def write_dxf(path: Path, width_mm: float):
    pts, h = norm(width_mm)
    v = "".join(f"0\nVERTEX\n8\n0\n10\n{x:.4f}\n20\n{-y:.4f}\n30\n0.0\n" for x, y in pts + [pts[0]])
    path.write_text(
        "0\nSECTION\n2\nENTITIES\n0\nPOLYLINE\n8\n0\n66\n1\n70\n1\n" + v +
        "0\nSEQEND\n0\nENDSEC\n0\nEOF\n", encoding="utf-8")


def write_preview(path: Path):
    """Preview from KiCad's own F.SilkS export of the footprints (green mask, white silk)."""
    import os, re, subprocess, tempfile
    ppm, W, H = 32, 1000, 820
    im = Image.new("RGB", (W, H), (10, 40, 20))
    dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT.replace("-Bold", ""), 18)
    dr.text((30, 15), "PCB ipek baskı — KiCad çıktısı (yeşil maske, beyaz ipek; 32 px/mm)", font=f, fill=(200, 230, 200))
    with tempfile.TemporaryDirectory() as tmp:
        for n, oy in (("Crow_Logo_8mm", 70), ("Crow_Logo_Text_8mm", 330), ("Crow_Logo_Text_6mm", 590)):
            subprocess.run(["kicad-cli", "fp", "export", "svg", "--footprint", n, "--layers", "F.SilkS",
                            "-o", tmp, str(PRETTY)], check=True, capture_output=True,
                           env=dict(os.environ, LC_ALL="C.UTF-8"))
            svg = re.sub(r"<text.*?</text>", "", Path(tmp, n + ".svg").read_text(), flags=re.S)
            polys, lines = [], []
            for m in re.finditer(r'<path[^>]*d="([^"]+)"', svg):
                v = [float(x) for x in re.findall(r"-?\d+\.?\d*", m.group(1))]
                (polys if "Z" in m.group(1) else lines).append(list(zip(v[0::2], v[1::2])))
            pts = [p for q in polys + lines for p in q]
            mx, my = min(p[0] for p in pts), min(p[1] for p in pts)
            w, h = max(p[0] for p in pts) - mx, max(p[1] for p in pts) - my
            ox, o2 = 60, oy + 35
            for q in polys:
                dr.polygon([(ox + (x - mx) * ppm, o2 + (y - my) * ppm) for x, y in q], fill=(240, 240, 240))
            for q in lines:
                dr.line([(ox + (x - mx) * ppm, o2 + (y - my) * ppm) for x, y in q], fill=(240, 240, 240), width=6)
            dr.text((60, oy), f"{n}  ({w:.1f} × {h:.1f} mm)", font=f, fill=(180, 220, 180))
    im.save(path, quality=95)


def main():
    PRETTY.mkdir(parents=True, exist_ok=True)
    for w in (6, 8):
        for text in (False, True):
            name = f"Crow_Logo{'_Text' if text else ''}_{w}mm"
            (PRETTY / f"{name}.kicad_mod").write_text(footprint(name, w, text), encoding="utf-8")
            print("wrote", PRETTY / f"{name}.kicad_mod")
    write_svg(DOCS / "crow-fpv-logo-pcb.svg", 8.0)
    write_dxf(DOCS / "crow-fpv-logo-pcb.dxf", 8.0)
    write_preview(DOCS / "crow-fpv-logo-pcb.jpg")
    print("wrote previews in", DOCS)


if __name__ == "__main__":
    main()
