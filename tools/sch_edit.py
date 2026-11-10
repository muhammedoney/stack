#!/usr/bin/env python3
"""Small KiCad 10 schematic editor (copied from ../fiber/tools/sch_edit.py).

Parses a .kicad_sch into nested lists, lets a script remove and add symbols,
connect pins with labels or power symbols, and prune the wires a removed part
leaves dangling, then writes the file back. Used by tools/esc55a_revb.py.

Stack changes: seed_uuids() makes new_uuid() deterministic (uuid5 of a seed
and a counter), so a script that starts from the same input writes the same
file every time.

Coordinates are millimetres in schematic space (y down). A pin's position is
its connection point, computed from the library symbol and the instance's
position and rotation (no mirrored instances in these schematics).
"""

import copy
import math
import re
import uuid as uuidlib


_PWR = 0


class Str(str):
    """A quoted string atom."""


# ---------------------------------------------------------------- s-expressions

def parse(text):
    tokens = re.finditer(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+', text)
    stack = [[]]
    for m in tokens:
        t = m.group(0)
        if t == "(":
            stack.append([])
        elif t == ")":
            node = stack.pop()
            stack[-1].append(node)
        elif t[0] == '"':
            stack[-1].append(Str(_unescape(t[1:-1])))
        else:
            stack[-1].append(t)
    return stack[0][0]


_ESC = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}


def _unescape(s):
    return re.sub(r"\\(.)", lambda m: _ESC.get(m.group(1), "\\" + m.group(1)), s)


def _atom(a):
    if isinstance(a, Str):
        return '"' + a.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r") + '"'
    if isinstance(a, float):
        s = ("%.4f" % a).rstrip("0").rstrip(".")
        return "0" if s in ("-0", "") else s
    return str(a)


def dump(node, depth=0):
    head = [a for a in node if not isinstance(a, list)]
    kids = [a for a in node if isinstance(a, list)]
    if node and node[0] in ("pts",):
        inner = " ".join(dump(k, 0).strip() for k in kids)
        return "\t" * depth + "(pts\n" + "\t" * (depth + 1) + inner + "\n" + "\t" * depth + ")"
    if not kids:
        return "\t" * depth + "(" + " ".join(_atom(a) for a in head) + ")"
    out = "\t" * depth + "(" + " ".join(_atom(a) for a in head)
    for k in node[len(head):]:
        out += "\n" + (dump(k, depth + 1) if isinstance(k, list) else "\t" * (depth + 1) + _atom(k))
    return out + "\n" + "\t" * depth + ")"


def find(node, key):
    for k in node:
        if isinstance(k, list) and k and k[0] == key:
            return k
    return None


def find_all(node, key):
    return [k for k in node if isinstance(k, list) and k and k[0] == key]


def prop(node, name):
    for p in find_all(node, "property"):
        if p[1] == name:
            return p
    return None


_SEED = [None, 0]


def seed_uuids(name):
    """From now on new_uuid() returns uuid5(name/1), uuid5(name/2), ..."""
    _SEED[0], _SEED[1] = name, 0


def new_uuid():
    if _SEED[0] is None:
        return Str(str(uuidlib.uuid4()))
    _SEED[1] += 1
    return Str(str(uuidlib.uuid5(uuidlib.NAMESPACE_URL, "%s/%d" % (_SEED[0], _SEED[1]))))


def r4(v):
    return round(v + 0.0, 4)


# ---------------------------------------------------------------- schematic

SUBSHEET = """(kicad_sch (version 20260306) (generator "eeschema") (generator_version "10.0")
 (uuid "%s") (paper "A4") (title_block (title "%s") (rev "B") (date "%s"))
 (lib_symbols) (embedded_fonts no))"""


class Schematic:
    def __init__(self, path, project, inst_path=None, text=None):
        """inst_path: "/root-uuid" for the root sheet (default) or
        "/root-uuid/sheet-uuid" for a sub-sheet."""
        self.path = path
        self.project = project
        self.root = parse(text if text is not None else open(path, encoding="utf-8").read())
        self.root_uuid = find(self.root, "uuid")[1]
        self.inst_path = inst_path or "/" + self.root_uuid
        self.libsyms = find(self.root, "lib_symbols")
        self.glob = False  # connect() places global labels when True

    @classmethod
    def new_subsheet(cls, path, project, parent_path, sheet_uuid, title, date):
        text = SUBSHEET % (uuidlib.uuid4(), title, date)
        return cls(path, project, parent_path + "/" + sheet_uuid, text)

    def _insert(self, node):
        anchor = find(self.root, "sheet_instances") or find(self.root, "embedded_fonts")
        if anchor is None:
            self.root.append(node)
        else:
            self.root.insert(self.root.index(anchor), node)

    def save(self):
        open(self.path, "w", encoding="utf-8").write(dump(self.root) + "\n")

    # -- lookup
    def items(self, key):
        return find_all(self.root, key)

    def instances(self):
        return self.items("symbol")

    def inst(self, ref):
        for s in self.instances():
            p = prop(s, "Reference")
            if p and p[2] == ref:
                return s
        raise KeyError(ref)

    def libsym(self, inst):
        name = find(inst, "lib_name")
        name = name[1] if name else find(inst, "lib_id")[1]
        for s in find_all(self.libsyms, "symbol"):
            if s[1] == name:
                return s
        raise KeyError(name)

    def pins(self, inst):
        """{number: (x, y, outward_angle_deg)} for an instance."""
        ls = self.libsym(inst)
        unit = int(find(inst, "unit")[1])
        at = find(inst, "at")
        X, Y, R = float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0
        out = {}
        for sub in find_all(ls, "symbol"):
            m = re.search(r"_(\d+)_(\d+)$", sub[1])
            if not m or int(m.group(1)) not in (0, unit):
                continue
            for p in find_all(sub, "pin"):
                pa = find(p, "at")
                px, py, pr = float(pa[1]), float(pa[2]), float(pa[3]) if len(pa) > 3 else 0.0
                num = find(p, "number")[1]
                a = math.radians(R)
                # library y is up; schematic y is down
                x = X + px * math.cos(a) - py * math.sin(a)
                y = Y - (px * math.sin(a) + py * math.cos(a))
                # pin "at" angle points from the connection point into the body
                out[str(num)] = (r4(x), r4(y), (pr + R) % 360)
        return out

    # -- connectivity points
    def wire_ends(self):
        ends = []
        for w in self.items("wire"):
            pts = find(w, "pts")
            ends.append(tuple((r4(float(p[1])), r4(float(p[2]))) for p in pts[1:]))
        return ends

    def anchor_points(self):
        pts = set()
        for s in self.instances():
            for x, y, _ in self.pins(s).values():
                pts.add((x, y))
        for key in ("label", "global_label", "hierarchical_label", "junction", "no_connect"):
            for l in self.items(key):
                a = find(l, "at")
                pts.add((r4(float(a[1])), r4(float(a[2]))))
        return pts

    def geometry(self):
        segs, pts = [], set()
        for w in self.items("wire"):
            a, b = [(r4(float(p[1])), r4(float(p[2]))) for p in find(w, "pts")[1:]]
            segs.append((a, b))
        for s in self.instances():
            for x, y, _ in self.pins(s).values():
                pts.add((x, y))
        for key in ("label", "global_label", "junction", "no_connect"):
            for l in self.items(key):
                a = find(l, "at")
                pts.add((r4(float(a[1])), r4(float(a[2]))))
        return segs, pts, {id(n) for n in self.root if isinstance(n, list)}

    def collisions(self, base):
        """Points of items added since `base` that touch pre-existing geometry."""
        segs, pts, ids = base

        def touches(p):
            if p in pts:
                return True
            for (x1, y1), (x2, y2) in segs:
                x, y = p
                if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) < 1e-6 and \
                        min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6:
                    return True
            return False

        hits = []
        for n in self.root:
            if not isinstance(n, list) or id(n) in ids:
                continue
            if n[0] == "symbol":
                ref = prop(n, "Reference")[2]
                for num, (x, y, _) in self.pins(n).items():
                    if touches((x, y)):
                        hits.append((ref, num, x, y))
            elif n[0] == "wire":
                a, b = [(r4(float(p[1])), r4(float(p[2]))) for p in find(n, "pts")[1:]]
                # the stub starts on a pin by design; its far end and its body must be clear
                if touches(b):
                    hits.append(("wire-end", "", b[0], b[1]))
                ends = {e for sg in segs for e in sg} | pts
                for q in ends:
                    if q == a:
                        continue
                    (x1, y1), (x2, y2), (x, y) = a, b, q
                    if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) < 1e-6 and \
                            min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6:
                        hits.append(("wire-over", "", x, y))
            elif n[0] == "label":
                a = find(n, "at")
                p = (r4(float(a[1])), r4(float(a[2])))
                if touches(p):
                    hits.append(("label " + n[1], "", p[0], p[1]))
        return hits

    # -- edits
    def remove(self, ref):
        s = self.inst(ref)
        self.root.remove(s)

    def prune(self):
        """Drop wires with a free end, then labels and junctions left alone. Repeat."""
        removed = 0
        while True:
            pin_pts = set()
            for s in self.instances():
                for x, y, _ in self.pins(s).values():
                    pin_pts.add((x, y))
            wires = self.items("wire")
            ends = {}
            segs = []
            for w in wires:
                pts = find(w, "pts")
                a, b = [(r4(float(p[1])), r4(float(p[2]))) for p in pts[1:]]
                segs.append((w, a, b))
                for e in (a, b):
                    ends[e] = ends.get(e, 0) + 1
            labels = {}
            for key in ("label", "global_label"):
                for l in self.items(key):
                    at = find(l, "at")
                    labels.setdefault((r4(float(at[1])), r4(float(at[2]))), []).append(l)

            def on_segment(p, a, b):
                (x, y), (x1, y1), (x2, y2) = p, a, b
                if p in (a, b):
                    return False
                if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) > 1e-6:
                    return False
                return min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6

            def connected(p, own):
                if p in pin_pts or ends.get(p, 0) > 1:
                    return True
                if p in labels:
                    return True
                return any(on_segment(p, a, b) for w, a, b in segs if w is not own)

            dead = [w for w, a, b in segs if not connected(a, w) or not connected(b, w)]
            # a wire whose only company is a label at a free end is also dead
            for w, a, b in segs:
                if w in dead:
                    continue
                for e, o in ((a, b), (b, a)):
                    if e in labels and e not in pin_pts and ends.get(e, 0) == 1 and not any(
                            on_segment(e, s1, s2) for w2, s1, s2 in segs if w2 is not w):
                        if not (o in pin_pts or ends.get(o, 0) > 1 or any(on_segment(o, s1, s2) for w2, s1, s2 in segs if w2 is not w)):
                            dead.append(w)
                            break
            lone_labels = []
            for p, ls in labels.items():
                if p not in pin_pts and ends.get(p, 0) == 0 and not any(on_segment(p, a, b) for w, a, b in segs):
                    lone_labels += ls
            junk = []
            for j in self.items("junction"):
                at = find(j, "at")
                p = (r4(float(at[1])), r4(float(at[2])))
                n = ends.get(p, 0) + (p in pin_pts) + sum(on_segment(p, a, b) for w, a, b in segs) * 2
                if n < 3:
                    junk.append(j)
            pin_count = {}
            for inst in self.instances():
                for x, y, _ in self.pins(inst).values():
                    pin_count[(x, y)] = pin_count.get((x, y), 0) + 1
            lone_power = []
            for inst in self.instances():
                if find(inst, "lib_id")[1].endswith("GND_POWER_GROUND") or str(prop(inst, "Reference")[2]).startswith("#PWR"):
                    pts = [(x, y) for x, y, _ in self.pins(inst).values()]
                    if all(pin_count.get(p, 0) < 2 and ends.get(p, 0) == 0 and p not in labels
                           and not any(on_segment(p, a, b) for w, a, b in segs) for p in pts):
                        lone_power.append(inst)
            if not dead and not lone_labels and not junk and not lone_power:
                return removed
            for n in dead + lone_labels + junk + lone_power:
                if n in self.root:
                    self.root.remove(n)
                    removed += 1

    def add_libsym(self, full_name, body):
        """body: library symbol node named without the library prefix."""
        for s in find_all(self.libsyms, "symbol"):
            if s[1] == full_name:
                return
        node = copy.deepcopy(body)
        node[1] = Str(full_name)
        self.libsyms.append(node)

    def add_symbol(self, lib_id, ref, value, x, y, rot=0, footprint="", fields=None, power=False):
        ls = None
        for s in find_all(self.libsyms, "symbol"):
            if s[1] == lib_id:
                ls = s
        assert ls is not None, lib_id
        pins = []
        for sub in find_all(ls, "symbol"):
            for p in find_all(sub, "pin"):
                pins.append(find(p, "number")[1])
        node = [
            "symbol", ["lib_id", Str(lib_id)], ["at", r4(x), r4(y), rot], ["unit", 1], ["body_style", 1],
            ["exclude_from_sim", "no"], ["in_bom", "no" if power else "yes"], ["on_board", "no" if power else "yes"],
            ["in_pos_files", "no" if power else "yes"], ["dnp", "no"], ["uuid", new_uuid()],
        ]
        hidden = ["effects", ["font", ["size", 1.27, 1.27]], ["hide", "yes"]]
        shown = ["effects", ["font", ["size", 1.27, 1.27]]]
        node.append(["property", Str("Reference"), Str(ref), ["at", r4(x), r4(y - 3.81 if not power else y), 0],
                     hidden if power else shown])
        node.append(["property", Str("Value"), Str(value), ["at", r4(x), r4(y + 3.81), 0], shown])
        node.append(["property", Str("Footprint"), Str(footprint), ["at", r4(x), r4(y), 0], copy.deepcopy(hidden)])
        node.append(["property", Str("Datasheet"), Str(""), ["at", r4(x), r4(y), 0], copy.deepcopy(hidden)])
        for k, v in (fields or {}).items():
            node.append(["property", Str(k), Str(v), ["at", r4(x), r4(y), 0], copy.deepcopy(hidden)])
        for n in pins:
            node.append(["pin", Str(n), ["uuid", new_uuid()]])
        node.append(["instances", ["project", Str(self.project),
                                   ["path", Str(self.inst_path), ["reference", Str(ref)], ["unit", 1]]]])
        self._insert(node)
        return node

    def wire(self, a, b):
        node = ["wire", ["pts", ["xy", r4(a[0]), r4(a[1])], ["xy", r4(b[0]), r4(b[1])]],
                ["stroke", ["width", 0], ["type", "default"]], ["uuid", new_uuid()]]
        self._insert(node)

    def label(self, name, x, y, angle=0):
        just = {0: ["justify", "left", "bottom"], 180: ["justify", "right", "bottom"],
                90: ["justify", "left", "bottom"], 270: ["justify", "right", "bottom"]}[angle]
        node = ["label", Str(name), ["at", r4(x), r4(y), angle],
                ["effects", ["font", ["size", 1.27, 1.27]], just], ["uuid", new_uuid()]]
        self._insert(node)

    def global_label(self, name, x, y, angle=0, shape="bidirectional"):
        just = {0: "left", 180: "right", 90: "left", 270: "right"}[angle]
        node = ["global_label", Str(name), ["shape", shape], ["at", r4(x), r4(y), angle],
                ["effects", ["font", ["size", 1.27, 1.27]], ["justify", just]], ["uuid", new_uuid()],
                ["property", Str("Intersheetrefs"), Str("${INTERSHEET_REFS}"), ["at", r4(x), r4(y), 0],
                 ["hide", "yes"], ["effects", ["font", ["size", 1.27, 1.27]]]]]
        self._insert(node)

    def globalize(self, names):
        """Turn the local labels with these names into global labels (same place)."""
        n = 0
        for l in list(self.items("label")):
            if l[1] in names:
                at = find(l, "at")
                ang = int(float(at[3])) if len(at) > 3 else 0
                idx = self.root.index(l)
                self.root.remove(l)
                self.global_label(l[1], float(at[1]), float(at[2]), ang)
                node = self.root.pop(self.root.index(self.items("global_label")[-1]))
                self.root.insert(idx, node)
                n += 1
        return n

    def add_sheet(self, name, file, x, y, w, h, page):
        u = new_uuid()
        node = ["sheet", ["at", r4(x), r4(y)], ["size", r4(w), r4(h)], ["exclude_from_sim", "no"],
                ["in_bom", "yes"], ["on_board", "yes"], ["dnp", "no"],
                ["stroke", ["width", 0.1524], ["type", "solid"]], ["fill", ["color", 0, 0, 0, 0]], ["uuid", u],
                ["property", Str("Sheetname"), Str(name), ["at", r4(x), r4(y - 0.7), 0],
                 ["effects", ["font", ["size", 1.27, 1.27], ["bold", "yes"]], ["justify", "left", "bottom"]]],
                ["property", Str("Sheetfile"), Str(file), ["at", r4(x), r4(y + h + 0.6), 0],
                 ["effects", ["font", ["size", 1, 1]], ["justify", "left", "top"]]],
                ["instances", ["project", Str(self.project), ["path", Str(self.inst_path), ["page", Str(str(page))]]]]]
        self._insert(node)
        return str(u)

    def text(self, s, x, y, size=1.27, color=None):
        font = ["font", ["size", size, size]]
        if color:
            font.append(["color"] + list(color))
        node = ["text", Str(s), ["exclude_from_sim", "no"], ["at", r4(x), r4(y), 0],
                ["effects", font, ["justify", "left", "top"]], ["uuid", new_uuid()]]
        self._insert(node)

    def no_connect(self, x, y):
        node = ["no_connect", ["at", r4(x), r4(y)], ["uuid", new_uuid()]]
        self._insert(node)

    def connect(self, ref, pin, net, stub=2.54, power_lib="stack:GND_POWER_GROUND"):
        """Join a pin to a net: a short wire out of the pin, then a label
        (or the GND power symbol), placed so the text clears the body."""
        x, y, ang = self.pins(self.inst(ref))[str(pin)]
        # outward direction is opposite to the pin's "into body" angle
        out = math.radians((ang + 180) % 360)
        dx, dy = math.cos(out), -math.sin(out)
        ex, ey = r4(x + dx * stub), r4(y + dy * stub)
        self.wire((x, y), (ex, ey))
        if net == "GND":
            self.gnd(ex, ey, dx, dy, power_lib)
            return
        if net == "NC":
            self.root.remove(self.items("wire")[-1])
            self.no_connect(x, y)
            return
        put = self.global_label if self.glob else self.label
        if abs(dx) > 0.5:
            put(net, ex, ey, 0 if dx > 0 else 180)
        else:
            put(net, ex, ey, 90 if dy < 0 else 270)

    def gnd(self, x, y, dx=0, dy=1, power_lib="stack:GND_POWER_GROUND"):
        """GND symbol at (x, y), its body pointing along (dx, dy)."""
        global _PWR
        _PWR += 1
        if abs(dx) > 0.5:
            rot = 90 if dx > 0 else 270
        else:
            rot = 0 if dy > 0 else 180
        node = self.add_symbol(power_lib, "#PWR%d" % (900 + _PWR), "GND", x, y, rot, power=True)
        p = prop(node, "Value")
        p[3] = ["at", r4(x + 4.5 * dx), r4(y + 4.5 * dy), 0]
        find(p, "effects").append(["hide", "yes"])

    def connect_group(self, ref, pins, net, stub=2.54):
        """Pins on one side of a part, joined by a short bus; one label or GND at the end."""
        pts = [self.pins(self.inst(ref))[str(p)] for p in pins]
        ang = pts[0][2]
        out = math.radians((ang + 180) % 360)
        dx, dy = round(math.cos(out)), round(-math.sin(out))
        ends = []
        for x, y, _ in pts:
            e = (r4(x + dx * stub), r4(y + dy * stub))
            self.wire((x, y), e)
            ends.append(e)
        ends.sort(key=lambda e: (e[1], e[0]))
        self.wire(ends[0], ends[-1])
        for e in ends[1:-1]:
            self.junction(*e)
        # leave from the lowest end, one more step outward (clear of other stubs and labels)
        x, y = ends[-1]
        if dx:
            ox = r4(x + dx * 2.54)
            if len(ends) > 1:
                self.junction(x, y)
            self.wire((x, y), (ox, y))
            if net == "GND":
                self.gnd(ox, y, dx, 0)
            else:
                (self.global_label if self.glob else self.label)(net, ox, y, 0 if dx > 0 else 180)
        else:
            if net == "GND":
                self.gnd(x, y, dx, dy)
            else:
                (self.global_label if self.glob else self.label)(net, x, y, 270 if dy > 0 else 90)

    def junction(self, x, y):
        node = ["junction", ["at", r4(x), r4(y)], ["diameter", 0], ["color", 0, 0, 0, 0], ["uuid", new_uuid()]]
        self._insert(node)

    def set_field(self, ref, name, value):
        p = prop(self.inst(ref), name)
        if p is None:
            s = self.inst(ref)
            at = find(s, "at")
            s.insert(s.index(find(s, "pin")) if find(s, "pin") else len(s),
                     ["property", Str(name), Str(value), ["at", at[1], at[2], 0],
                      ["effects", ["font", ["size", 1.27, 1.27]], ["hide", "yes"]]])
        else:
            p[2] = Str(value)

    def set_lib(self, ref, lib_id):
        s = self.inst(ref)
        find(s, "lib_id")[2 - 1] = Str(lib_id)
        ln = find(s, "lib_name")
        if ln:
            s.remove(ln)


# ---------------------------------------------------------------- library helpers

def load_lib(path):
    root = parse(open(path, encoding="utf-8").read())
    return {s[1]: s for s in find_all(root, "symbol")}, root


def save_lib(path, root):
    open(path, "w", encoding="utf-8").write(dump(root) + "\n")


def box_symbol(name, ref, value, left, right, width=15.24, desc="", footprint="", fields=None):
    """A rectangle symbol. left/right: lists of (number, name, type) or None for a gap,
    top to bottom, 2.54 mm pitch. Pins are 2.54 mm long."""
    n = max(len(left), len(right))
    h = (n + 1) * 2.54
    top = h / 2
    hw = width / 2
    body = ["symbol", Str(name + "_0_1"),
            ["rectangle", ["start", r4(-hw), r4(top)], ["end", r4(hw), r4(-top)],
             ["stroke", ["width", 0.254], ["type", "default"]], ["fill", ["type", "background"]]]]
    pins = ["symbol", Str(name + "_1_1")]
    for side, lst in ((0, left), (1, right)):
        for i, p in enumerate(lst):
            if p is None:
                continue
            num, pname, ptype = p
            y = r4(top - 2.54 * (i + 1))
            x = r4(-hw - 2.54) if side == 0 else r4(hw + 2.54)
            ang = 0 if side == 0 else 180
            pins.append(["pin", ptype, "line", ["at", x, y, ang], ["length", 2.54],
                         ["name", Str(pname), ["effects", ["font", ["size", 1.016, 1.016]]]],
                         ["number", Str(num), ["effects", ["font", ["size", 1.016, 1.016]]]]])
    hidden = ["effects", ["font", ["size", 1.27, 1.27]], ["hide", "yes"]]
    node = ["symbol", Str(name), ["exclude_from_sim", "no"], ["in_bom", "yes"], ["on_board", "yes"],
            ["property", Str("Reference"), Str(ref), ["at", 0, r4(top + 1.27), 0], ["effects", ["font", ["size", 1.27, 1.27]]]],
            ["property", Str("Value"), Str(value), ["at", 0, r4(-top - 1.27), 0], ["effects", ["font", ["size", 1.27, 1.27]]]],
            ["property", Str("Footprint"), Str(footprint), ["at", 0, 0, 0], hidden],
            ["property", Str("Datasheet"), Str(""), ["at", 0, 0, 0], copy.deepcopy(hidden)],
            ["property", Str("Description"), Str(desc), ["at", 0, 0, 0], copy.deepcopy(hidden)]]
    for k, v in (fields or {}).items():
        node.append(["property", Str(k), Str(v), ["at", 0, 0, 0], copy.deepcopy(hidden)])
    node += [body, pins]
    return node


def clone_value(lib_root, src, new, value_fields):
    """Copy a passive symbol (e.g. RES0402_62 -> RES0402_82) and rewrite its fields."""
    syms = {s[1]: s for s in find_all(lib_root, "symbol")}
    if new in syms:
        return syms[new]
    node = copy.deepcopy(syms[src])
    node[1] = Str(new)
    for sub in find_all(node, "symbol"):
        sub[1] = Str(sub[1].replace(src, new, 1))
    for k, v in value_fields.items():
        p = prop(node, k)
        if p is None:
            node.insert(node.index(find(node, "symbol")), ["property", Str(k), Str(v), ["at", 0, 0, 0],
                        ["effects", ["font", ["size", 1.27, 1.27]], ["hide", "yes"]]])
        else:
            p[2] = Str(v)
    lib_root.append(node)
    return node
