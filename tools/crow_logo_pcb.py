#!/usr/bin/env python3
"""Crow PCB logo: place CROW left of beak, export JPG + SVG + DXF.

Usage:
  python3 tools/crow_logo_pcb.py \\
    /path/to/crow-beak-only.jpg \\
    docs/pazar/crow-fpv-logo-pcb
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def compose(src: Path, out_stem: Path) -> Image.Image:
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    # Head cheek sits left of the beak (beak opens right).
    # Knockout letters inside the white head, left of the beak (cheek).
    font_size = max(32, int(w * 0.07))
    font = ImageFont.truetype(FONT, font_size)
    text = "CROW"
    draw = ImageDraw.Draw(im)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # Cheek: left of beak tip, right of crest — inside filled head.
    x = int(w * 0.46) - tw // 2
    y = int(h * 0.47) - th // 2
    # Slight stroke so letter holes survive contour tracing.
    draw.text((x, y), text, font=font, fill=(0, 0, 0, 255), stroke_width=1, stroke_fill=(0, 0, 0, 255))
    rgb = Image.new("RGB", im.size, (0, 0, 0))
    rgb.paste(im, mask=im.split()[3])
    jpg = out_stem.with_suffix(".jpg")
    rgb.save(jpg, quality=95)
    print("wrote", jpg)
    return rgb


def binary_mask(im: Image.Image, thr: int = 40) -> np.ndarray:
    g = np.asarray(im.convert("L"))
    return g > thr


def neighbors8(y: int, x: int):
    # Clockwise from E
    return (
        (y, x + 1),
        (y + 1, x + 1),
        (y + 1, x),
        (y + 1, x - 1),
        (y, x - 1),
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
    )


def trace_boundary(mask: np.ndarray, start: tuple[int, int]) -> list[tuple[int, int]]:
    """Moore-neighbor outer boundary walk. Points are (x, y) pixel corners-ish (pixel centers)."""
    h, w = mask.shape
    sy, sx = start
    # Start direction: coming from left, looking for first FG
    contour = []
    y, x = sy, sx
    # Find initial backtrack (west of start)
    back = 4  # index into neighbors8: W
    for _ in range(h * w * 2):
        contour.append((x, y))
        nbrs = neighbors8(y, x)
        # Start search from next after backtrack (back+1)
        found = None
        for k in range(1, 9):
            i = (back + k) % 8
            ny, nx = nbrs[i]
            if 0 <= ny < h and 0 <= nx < w and mask[ny, nx]:
                found = (ny, nx, i)
                break
        if found is None:
            break
        y, x, i = found
        # New back is opposite of entry direction
        back = (i + 4) % 8
        if (x, y) == (sx, sy) and len(contour) > 8:
            break
        if len(contour) > h * w:
            break
    return contour


def label_components(mask: np.ndarray) -> list[np.ndarray]:
    """Connected components (4-conn) without scipy."""
    h, w = mask.shape
    seen = np.zeros_like(mask, dtype=bool)
    comps = []
    for y in range(h):
        for x in range(w):
            if not mask[y, x] or seen[y, x]:
                continue
            stack = [(y, x)]
            seen[y, x] = True
            cells = []
            while stack:
                cy, cx = stack.pop()
                cells.append((cy, cx))
                for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
            comps.append(np.array(cells))
    return comps


def component_mask(shape, cells) -> np.ndarray:
    m = np.zeros(shape, dtype=bool)
    m[cells[:, 0], cells[:, 1]] = True
    return m


def find_boundary_start(comp_mask: np.ndarray) -> tuple[int, int] | None:
    h, w = comp_mask.shape
    for y in range(h):
        for x in range(w):
            if not comp_mask[y, x]:
                continue
            for ny, nx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
                if not (0 <= ny < h and 0 <= nx < w) or not comp_mask[ny, nx]:
                    return y, x
    return None


def simplify(pts: list[tuple[int, int]], eps: float) -> list[tuple[float, float]]:
    """Ramer–Douglas–Peucker."""
    if len(pts) < 3:
        return [(float(x), float(y)) for x, y in pts]

    def _rdp(points, epsilon):
        start, end = points[0], points[-1]
        sx, sy = start
        ex, ey = end
        max_d, idx = 0.0, 0
        for i in range(1, len(points) - 1):
            px, py = points[i]
            # distance point to line
            num = abs((ey - sy) * px - (ex - sx) * py + ex * sy - ey * sx)
            den = ((ey - sy) ** 2 + (ex - sx) ** 2) ** 0.5 or 1.0
            d = num / den
            if d > max_d:
                max_d, idx = d, i
        if max_d > epsilon:
            left = _rdp(points[: idx + 1], epsilon)
            right = _rdp(points[idx:], epsilon)
            return left[:-1] + right
        return [start, end]

    return _rdp([(float(x), float(y)) for x, y in pts], eps)


def flood_background(mask: np.ndarray) -> np.ndarray:
    """True = background black reachable from image border."""
    h, w = mask.shape
    bg = np.zeros_like(mask, dtype=bool)
    stack = []
    for x in range(w):
        for y in (0, h - 1):
            if not mask[y, x]:
                stack.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if not mask[y, x]:
                stack.append((y, x))
    while stack:
        y, x = stack.pop()
        if y < 0 or y >= h or x < 0 or x >= w or bg[y, x] or mask[y, x]:
            continue
        bg[y, x] = True
        stack.extend(((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)))
    return bg


def contour_of(cm: np.ndarray, eps: float) -> list[tuple[float, float]] | None:
    start = find_boundary_start(cm)
    if start is None:
        return None
    raw = trace_boundary(cm, start)
    if len(raw) < 12:
        return None
    simp = simplify(raw, eps)
    return simp if len(simp) >= 3 else None


def contours_from_image(im: Image.Image, min_area: int = 40, eps: float = 1.8):
    """Outer white body + internal holes (eye, CROW letters) for even-odd fill."""
    mask = binary_mask(im)
    bg = flood_background(mask)
    # White body components
    white_comps = label_components(mask)
    outer_paths = []
    for cells in white_comps:
        if len(cells) < min_area:
            continue
        cm = component_mask(mask.shape, cells)
        p = contour_of(cm, eps)
        if p:
            outer_paths.append(p)
    # Black islands = holes (not background)
    hole_mask = ~mask & ~bg
    hole_paths = []
    for cells in label_components(hole_mask):
        if len(cells) < 8:
            continue
        cm = component_mask(mask.shape, cells)
        p = contour_of(cm, eps)
        if p:
            hole_paths.append(p)
    return outer_paths, hole_paths, mask.shape


def write_svg(outers, holes, shape, out: Path, scale_mm: float = 12.0):
    h, w = shape
    s = scale_mm / max(w, h)
    parts = []
    for pts in outers + holes:
        parts.append("M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z")
    d = " ".join(parts)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * s:.3f}mm" height="{h * s:.3f}mm" '
        f'viewBox="0 0 {w} {h}">',
        '<rect width="100%" height="100%" fill="black"/>',
        f'<path fill="white" fill-rule="evenodd" d="{d}"/>',
        "</svg>",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out)


def write_dxf(outers, holes, shape, out: Path, scale_mm: float = 12.0):
    """Minimal DXF R12 closed polylines in mm (outer + hole outlines)."""
    h, w = shape
    s = scale_mm / max(w, h)
    ents = []
    for pts in outers + holes:
        if len(pts) < 2:
            continue
        closed = pts + [pts[0]]
        ents.append("0\nPOLYLINE\n8\n0\n66\n1\n70\n1\n")
        for x, y in closed:
            ents.append(
                f"0\nVERTEX\n8\n0\n10\n{x * s:.4f}\n20\n{(h - y) * s:.4f}\n30\n0.0\n"
            )
        ents.append("0\nSEQEND\n")
    body = "".join(ents)
    dxf = (
        "0\nSECTION\n2\nHEADER\n0\nENDSEC\n"
        "0\nSECTION\n2\nTABLES\n0\nENDSEC\n"
        "0\nSECTION\n2\nBLOCKS\n0\nENDSEC\n"
        "0\nSECTION\n2\nENTITIES\n"
        f"{body}"
        "0\nENDSEC\n0\nEOF\n"
    )
    out.write_text(dxf, encoding="utf-8")
    print("wrote", out)


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "/home/user/.cursor/projects/home-user-calismalar-stack/assets/crow-beak-only.jpg"
    )
    stem = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "docs/pazar/crow-fpv-logo-pcb"
    stem.parent.mkdir(parents=True, exist_ok=True)
    rgb = compose(src, stem)
    outers, holes, shape = contours_from_image(rgb, min_area=80, eps=2.0)
    print(f"outers: {len(outers)} holes: {len(holes)}")
    write_svg(outers, holes, shape, stem.with_suffix(".svg"))
    write_dxf(outers, holes, shape, stem.with_suffix(".dxf"))


if __name__ == "__main__":
    main()
