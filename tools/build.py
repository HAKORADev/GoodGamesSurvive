#!/usr/bin/env python3
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kage_core import (Engine, jwrite, jload, ROOT, BUILD_V, esc)
import kage_render as R
import kage_render2 as R2

def main():
    eng = Engine()
    written = []

    for slug in sorted(eng.page_by_slug):
        if slug in eng.game_by_slug:
            p = os.path.join(ROOT, "pages", "game", slug + ".html")
            open(p, "w", encoding="utf-8").write(R.game_page(eng, slug))
            written.append("pages/game/%s.html" % slug)
        elif slug in {r["slug"] for r in eng.software_rows}:
            p = os.path.join(ROOT, "pages", "software", slug + ".html")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(R2.thing_page(eng, slug, "software"))
            written.append("pages/software/%s.html" % slug)
        elif slug in {r["slug"] for r in eng.mods_rows}:
            p = os.path.join(ROOT, "pages", "mod", slug + ".html")
            os.makedirs(os.path.dirname(p), exist_ok=True)
            open(p, "w", encoding="utf-8").write(R2.thing_page(eng, slug, "mods"))
            written.append("pages/mod/%s.html" % slug)

    list_pages = {
        "games": ("GAMES", "The games index - every title catalogued, filterable, sortable, searchable.", "692+ titles catalogued. pages get dug one dig at a time - the rest are searchable rows, honestly marked."),
        "software": ("SOFTWARE", "The software index - emulators, tools, fixes.", "tools and emulators live here when the first page lands."),
        "mods": ("MODS+PATCHES", "The mods and patches index.", "mods and patches live here when the first page lands."),
    }
    for sec, (t, d, note) in list_pages.items():
        p = os.path.join(ROOT, "pages", sec + ".html")
        open(p, "w", encoding="utf-8").write(R2.list_page(eng, sec, t, d, note))
        written.append("pages/%s.html" % sec)

    open(os.path.join(ROOT, "pages", "search.html"), "w", encoding="utf-8").write(R2.search_page(eng))
    written.append("pages/search.html")
    open(os.path.join(ROOT, "pages", "random.html"), "w", encoding="utf-8").write(R2.random_page(eng))
    written.append("pages/random.html")
    open(os.path.join(ROOT, "pages", "collections.html"), "w", encoding="utf-8").write(R2.collections_page(eng))
    written.append("pages/collections.html")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(R2.main_page(eng))
    written.append("index.html")

    os.makedirs(os.path.join(ROOT, "pages", "collection"), exist_ok=True)
    for c in eng.collections:
        p = os.path.join(ROOT, "pages", "collection", c["slug"] + ".html")
        open(p, "w", encoding="utf-8").write(R2.collection_page(eng, c))
        written.append("pages/collection/%s.html" % c["slug"])
    os.makedirs(os.path.join(ROOT, "pages", "meta"), exist_ok=True)
    for m in eng.multis:
        p = os.path.join(ROOT, "pages", "meta", m["slug"] + ".html")
        open(p, "w", encoding="utf-8").write(R2.meta_page(eng, m))
        written.append("pages/meta/%s.html" % m["slug"])

    for r in eng.redirects.get("redirects", []):
        sec = r.get("sec", "games")
        d = {"games": "game", "software": "software", "mods": "mod"}[sec]
        p = os.path.join(ROOT, "pages", d, r["from"] + ".html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(R2.redirect_page(eng, r, sec))
        written.append("pages/%s/%s.html (redirect)" % (d, r["from"]))

    idx_meta = {"_meta": {"built_by": "tools/build.py", "v": BUILD_V, "rows": len(eng.rows)}}
    jwrite(os.path.join(ROOT, "data", "search-index.json"), {"_meta": idx_meta["_meta"], "rows": eng.rows}, compact=True)

    manifest = {"_meta": {"built_by": "tools/build.py"}, "items": []}
    for r in eng.rows:
        if r.get("page"):
            manifest["items"].append({"u": "pages/" + r["page"], "t": r["t"]})
    jwrite(os.path.join(ROOT, "data", "random-manifest.json"), manifest, compact=True)

    public_rows = []
    for g in eng.games_db["games"]:
        slug = g["slug"]
        if slug not in eng.page_by_slug:
            continue
        p = eng.page_by_slug[slug]
        public_rows.append({
            "title": g["title"], "slug": slug, "list": g.get("list"), "class": g.get("class"),
            "category": g.get("category"), "series": g.get("series"), "series_part": g.get("series_part"),
            "content_walls": g.get("content_walls"), "big_size": g.get("big_size"),
            "big_size_gb": g.get("big_size_gb"), "release": g.get("release"),
            "developers": g.get("developers"), "publishers": g.get("publishers"),
            "platforms": g.get("platforms"), "players": g.get("players"),
            "buyable": g.get("buyable"), "download_kind": g.get("download_kind"),
            "test_status": g.get("test_status"), "target_os": g.get("target_os"),
            "haswell_igpu_ok": g.get("haswell_igpu_ok"), "confidence": g.get("confidence"),
            "genres": g.get("genres"), "subgenres": g.get("subgenres"), "tags": g.get("tags"),
            "size_est_mb": g.get("size_est_mb"), "size_source": g.get("size_source"),
            "req_tier": g.get("req_tier"), "sources": g.get("sources"), "notes": g.get("notes"),
            "page_url": "pages/game/%s.html" % slug, "thumbnail": p.get("thumbnail"),
            "caption": p.get("caption"),
        })
    jwrite(os.path.join(ROOT, "data", "games.json"), {
        "_meta": {"schema": "ggs.v2", "updated": "2026-10-09",
                  "law": "public copy: only page-backed rows, regenerated by tools/build.py. full DB is work/lists/.",
                  "count": len(public_rows)},
        "count": len(public_rows), "games": public_rows})

    report = validate(eng, written)
    removed = cleanup(eng, written)
    print("build: %d files written, %d stale removed" % (len(written), removed))
    for line in report:
        print(line)

def cleanup(eng, written):
    keep = {w.split(" (")[0] for w in written}
    removed = 0
    for d in ("game", "software", "mod", "collection", "meta"):
        pdir = os.path.join(ROOT, "pages", d)
        if not os.path.isdir(pdir):
            continue
        for f in sorted(os.listdir(pdir)):
            if not f.endswith(".html"):
                continue
            relp = "pages/%s/%s" % (d, f)
            if relp not in keep:
                os.remove(os.path.join(pdir, f))
                removed += 1
    return removed

def validate(eng, written):
    out = []
    problems = 0
    for slug, p in eng.page_by_slug.items():
        if slug not in eng.game_by_slug:
            continue
        g = (p.get("gallery") or {})
        if len(g.get("images") or []) != 10:
            out.append("WARN %s gallery images %d/10" % (slug, len(g.get("images") or [])))
            problems += 1
        if len(g.get("videos") or []) != 3:
            out.append("WARN %s gallery videos %d/3" % (slug, len(g.get("videos") or [])))
            problems += 1
        if not p.get("caption"):
            out.append("WARN %s missing caption" % slug)
            problems += 1
        if not p.get("about"):
            out.append("WARN %s missing about" % slug)
            problems += 1
    for w in written:
        real = w.split(" (")[0]
        path = os.path.join(ROOT, real)
        if not os.path.exists(path):
            out.append("FAIL missing output %s" % real)
            problems += 1
            continue
        html = open(path, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src|action)="([^"#]+)"', html):
            u = m.group(1)
            if u.startswith(("http://", "https://", "data:", "mailto:")):
                continue
            if u.startswith("//") or "'" in u or "+" in u or "javascript" in u:
                continue
            base = u.split("?")[0].split("#")[0]
            if not base:
                continue
            tgt = os.path.normpath(os.path.join(os.path.dirname(path), base))
            if not os.path.exists(tgt):
                out.append("FAIL broken internal ref %s -> %s" % (real, u))
                problems += 1
    c = eng.sec_counts()
    out.append("counts: games %d / software %d / mods %d / collections %d" % (c["games"], c["software"], c["mods"], c["collections"]))
    out.append("similars: %d page rows scored, pools %s" % (len(eng.similar), [len(v["pages"]) for v in list(eng.similar.values())[:6]]))
    out.append("index rows: %d (compact json)" % len(eng.rows))
    out.append("validation problems: %d" % problems)
    if problems:
        out.append("BUILD: DONE WITH WARNINGS")
    else:
        out.append("BUILD: CLEAN")
    return out

if __name__ == "__main__":
    main()
