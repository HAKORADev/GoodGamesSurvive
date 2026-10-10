#!/usr/bin/env python3
# sorted_lists.py - regenerate work/original-lists/sorted/ straight from the
# games.json database (owner law, 2026-10-10): the sorted lists are a generated
# view of the database, never hand-edited. re-run this instead of touching them.
#
#   outputs:
#     sorted/casual-sorted.txt        casual rows, one line per row
#     sorted/non-casual-sorted.txt    non-casual rows, one line per row
#     sorted/list.txt                 both in one file with an internal split
#
#   line format (owner spec):  - Name platform year #tags xN
#     - platform: windows rows show PC (the owner's "platform as PC for windows");
#       console rows show their tag (PS2/PSP/PS1/WII); rows without a platform
#       field inherit it from their section (PS2/PSP/DOLPHIN sections) or PC.
#     - year: the row's release year, ???? when unknown (no invented years).
#     - tags: #big-size, then the content walls (#sex #gore).
#     - xN: appended only when the title mechanically DECLARES multiple games
#       ("1 & 2", "Cake Mania 1, 2 & 3", "I & II", "1-4" ranges, "Series (...)"
#       paren lists, or owner-noted bundle sizes like Ezio Collection = 3).
#       joined titles without a declared count ("San Andreas & Vice City") stay
#       unmarked - a silent maybe beats a wrong number.
#     - sections keep the owner's category grouping (first-appearance order in
#       the database); rows sort alphabetically inside each section.
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "work", "original-lists", "sorted")
DB = os.path.join(ROOT, "work", "lists", "games", "games.json")

# owner-noted bundle sizes (2026-10-10): "ezio collection as example is 3 games"
BUNDLE_KNOWN = {"ezio collection": 3}

RULE = "=" * 67
SPLIT = "#" * 67

ROMAN = r"(?:X|IX|V?I{1,3})"
DIG_ENUM = re.compile(r"\d(?:\s*[,&]\s*\d)+")
AMP_ENUM = re.compile(r"(?:\d|%s|\))\s*&\s*[\w'(]" % ROMAN)
ROMAN_ENUM = re.compile(r"%s\s*&\s*%s" % (ROMAN, ROMAN))
RANGE = re.compile(r"^.*?\b(\d+)\s*-\s*(\d+)\b.*$")
BUNDLE_HEAD = re.compile(r"(?:Series|Universe|Collection|Trilogy|Anthology|Saga)\s*\((.*)\)$", re.S)


def strip_noise(t):
    t = re.sub(r"`[^`]*`", " ", t)      # `#big-size` style markup
    t = re.sub(r"#\+18\b", " ", t)      # owner's adult tag
    return t.strip()


def top_split(t, seps):
    """split on separators that sit OUTSIDE parentheses only"""
    parts, depth, cur, i = [], 0, "", 0
    low = t
    while i < len(low):
        hit = None
        if depth == 0:
            for s in seps:
                if low.startswith(s, i):
                    hit = s; break
        if hit:
            parts.append(cur); cur = ""; i += len(hit)
            continue
        if low[i] == "(":
            depth += 1
        elif low[i] == ")":
            depth -= 1
        cur += low[i]; i += 1
    parts.append(cur)
    return [p for p in (x.strip() for x in parts) if p]


def item_count(s):
    """how many declared games live inside one chunk"""
    low = s.lower().strip()
    if not low:
        return 0
    if low in BUNDLE_KNOWN:
        return BUNDLE_KNOWN[low]
    m = RANGE.match(s)  # "1-4" style declared ranges
    if m and 0 < int(m.group(2)) - int(m.group(1)) <= 9:
        return int(m.group(2)) - int(m.group(1)) + 1
    if DIG_ENUM.search(s):
        # "Cake Mania 1, 2 & 3" -> the digits themselves are the declared games
        return min(len(re.findall(r"\d+", "".join(DIG_ENUM.findall(s)))), 12)
    if AMP_ENUM.search(s) or ROMAN_ENUM.search(s):
        return 2
    return 1


def bundle_count(title):
    t = strip_noise(title)
    parts = top_split(t, [" / "])
    total = 0
    for part in parts:
        bm = BUNDLE_HEAD.search(part)
        if bm:
            inner = top_split(bm.group(1), [",", " & "])
            total += sum(item_count(x) for x in inner)
            continue
        total += item_count(part)
    return total


PLAT_UP = {"ps1": "PS1", "ps2": "PS2", "psp": "PSP", "wii": "WII", "gc": "GC",
           "windows": "PC"}


def plat_of(g):
    plats = g.get("platforms") or []
    if plats:
        if "windows" in plats:  # one-platform law: native windows wins -> PC
            return "PC"
        return PLAT_UP.get(plats[0], plats[0].upper())
    cat = g.get("category") or ""
    if "PS2" in cat: return "PS2"
    if "PSP" in cat: return "PSP"
    if "WII" in cat or "DOLPHIN" in cat: return "WII"
    return "PC"  # the vault is a windows vault; one-platform law, native pc wins


def year_of(g):
    r = g.get("release") or ""
    m = re.match(r"(\d{4})", str(r))
    return m.group(1) if m else "????"


def tags_of(g):
    tags = []
    if g.get("big_size"):
        tags.append("#big-size")
    for w in (g.get("content_walls") or []):
        tags.append("#" + str(w))
    return tags


def line_of(g):
    n = bundle_count(g["title"])
    bits = [g["title"], plat_of(g), year_of(g)] + tags_of(g)
    line = " ".join(bits)
    if n > 1:
        line += " x%d" % n
    return line


def build_body(rows):
    secs, order = {}, []
    for g in rows:
        c = g.get("category") or "[ NO CATEGORY ]"
        if c not in secs:
            secs[c] = []
            order.append(c)
        secs[c].append(g)
    out = []
    for c in order:
        out.append("")
        out.append("[ %s ]" % c)
        for g in sorted(secs[c], key=lambda x: x["title"].casefold()):
            out.append("- " + line_of(g))
    return out


def header(title, note):
    return [RULE, title, note, RULE]


def main():
    db = json.load(open(DB, encoding="utf-8"))
    groups = {"casual": [], "non-casual": []}
    skipped = []
    for g in db["games"]:
        lst = g.get("list")
        if lst in groups:
            groups[lst].append(g)
        else:
            skipped.append("%s (%s)" % (g.get("title"), lst))
    if skipped:
        print("WARN rows outside casual/non-casual (not listed):", skipped)

    bodies, files = {}, {}
    for lst in ("casual", "non-casual"):
        body = build_body(groups[lst])
        bodies[lst] = body
        h = header("  %s — SORTED (generated from the games.json database)" % lst.upper(),
                   "  one line per row:  name platform year #tags   (xN = declared entries)")
        files[lst + "-sorted.txt"] = h + body

    listh = header("  GGS MASTER LIST — casual + non-casual, generated from games.json",
                   "  generated by tools/sorted_lists.py — do not hand-edit, re-run instead")
    listf = listh + ["", SPLIT, "  PART 1/2 — CASUAL", SPLIT] + bodies["casual"] + \
            ["", SPLIT, "  PART 2/2 — NON-CASUAL", SPLIT] + bodies["non-casual"]

    os.makedirs(OUT, exist_ok=True)
    for name, lines in list(files.items()) + [("list.txt", listf)]:
        p = os.path.join(OUT, name)
        open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        print("wrote", os.path.relpath(p, ROOT), "(%d lines)" % len(lines))

    for lst in ("casual", "non-casual"):
        print("%s rows: %d" % (lst, len(groups[lst])))


if __name__ == "__main__":
    main()
