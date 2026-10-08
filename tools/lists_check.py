#!/usr/bin/env python3
# lists_check.py - repo health check for the GGS databases.
# run locally or in CI on every push:
#   1. every *.json in work/lists and data must parse
#   2. work/lists/games/games.json: slug unique, required fields present
#   3. duplicate titles -> warning (name-check surfaces them for the owner)
#   4. regenerate work/lists/games/name-check/games-added.txt from games.json
#   5. write work/lists/games/counts.json + print a summary
# exit 1 on hard errors (bad json, slug collision, missing fields).
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ("title", "slug", "list", "series", "content_walls",
            "big_size", "test_status", "confidence", "platforms")

def fail(msg):
    print("FAIL:", msg)
    sys.exit(1)

def load(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception as e:
        fail("%s does not parse: %s" % (path, e))

def walk_json(base):
    for dirpath, _, files in os.walk(base):
        for f in files:
            if f.endswith(".json"):
                yield os.path.join(dirpath, f)

def main():
    errors = 0
    for base in ("work/lists", "data"):
        p = os.path.join(ROOT, base)
        if not os.path.isdir(p):
            continue
        for f in walk_json(p):
            load(f)
    print("json parse: ok")

    gpath = os.path.join(ROOT, "work", "lists", "games", "games.json")
    if not os.path.exists(gpath):
        fail("games.json missing")
    db = load(gpath)
    games = db.get("games") or fail("games.json has no games array")
    slugs, titles = {}, {}
    for g in games:
        slug = g.get("slug")
        if not slug:
            fail("row without slug: %r" % g.get("title"))
        if slug in slugs:
            fail("slug collision: %s (%s / %s)"
                 % (slug, slugs[slug], g.get("title")))
        slugs[slug] = g.get("title")
        for field in REQUIRED:
            if field not in g:
                fail("%s missing field %s" % (slug, field))
        t = g.get("title", "")
        titles.setdefault(t.casefold(), []).append(t)
    dups = {t: rows for t, rows in titles.items() if len(rows) > 1}
    print("games rows: %d | unique slugs: ok" % len(games))

    nc = os.path.join(ROOT, "work", "lists", "games", "name-check",
                      "games-added.txt")
    os.makedirs(os.path.dirname(nc), exist_ok=True)
    names = sorted({g.get("title", "") for g in games}, key=str.casefold)
    open(nc, "w", encoding="utf-8").write("\n".join(names) + "\n")
    print("name-check regenerated: %d names" % len(names))

    big = [g["title"] for g in games if g.get("big_size")]
    walls = [g["title"] for g in games
             if g.get("content_walls")]
    tested = [g["title"] for g in games if g.get("test_status") == "tested"]
    verified = sum(1 for g in games if g.get("confidence") == "verified")
    series = load(os.path.join(ROOT, "work", "lists", "games", "series.json"))
    counts = {
        "games": len(games),
        "verified": verified,
        "owner_listed": len(games) - verified,
        "big_size": len(big),
        "content_walls": len(walls),
        "tested": len(tested),
        "series": len(series.get("series", [])),
        "duplicate_titles": {k: v for k, v in dups.items()},
    }
    cpath = os.path.join(ROOT, "work", "lists", "games", "counts.json")
    json.dump({"_meta": {"updated_by": "tools/lists_check.py"}, **counts},
              open(cpath, "w", encoding="utf-8"), indent=1)

    # site search index: page-backed slugs auto-detected from pages/game/*.html,
    # thumbs auto-pulled from each page's game-cover img (no bookkeeping).
    gdir = os.path.join(ROOT, "pages", "game")
    page_slugs = {}
    if os.path.isdir(gdir):
        for f in sorted(os.listdir(gdir)):
            if f.endswith(".html"):
                html = open(os.path.join(gdir, f), encoding="utf-8").read()
                m = re.search(r'<div class="game-cover">\s*<img src="([^"]+)"',
                              html)
                page_slugs[f[:-5]] = m.group(1) if m else None
    idx = []
    for g in games:
        rel = g.get("release") or ""
        idx.append({
            "t": g.get("title", ""),
            "s": g.get("slug", ""),
            "y": rel[:4] if rel[:4].isdigit() else None,
            "c": g.get("category"),
            "ser": g.get("series"),
            "l": g.get("list", ""),
            "p": "pages/game/%s.html" % g["slug"] if g["slug"] in page_slugs
                 else None,
            "th": page_slugs.get(g["slug"]),
            "b": bool(g.get("big_size")),
            "w": g.get("content_walls") or [],
            "v": g.get("confidence") == "verified",
        })
    idx.sort(key=lambda r: r["t"].casefold())
    ipath = os.path.join(ROOT, "data", "search-index.json")
    json.dump({"_meta": {"updated_by": "tools/lists_check.py",
                         "rows": len(idx)},
               "rows": idx},
              open(ipath, "w", encoding="utf-8"),
              indent=None, separators=(",", ":"), ensure_ascii=False)
    print("search index: %d rows (%d page-backed)"
          % (len(idx), len(page_slugs)))

    print("counts:", json.dumps({k: v for k, v in counts.items()
                                 if k != "duplicate_titles"}))
    if dups:
        print("WARN duplicate titles (owner decides):")
        for k, rows in sorted(dups.items()):
            print("  -", rows)
    print("lists_check: PASS")

if __name__ == "__main__":
    main()
