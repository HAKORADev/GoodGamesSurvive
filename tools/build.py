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
        "games": ("GAMES", "The games shelf - only the pages that are actually dug. the full %d-row catalogue stays reachable through search." % len(eng.catalog_games),
                  "this shelf shows the dug pages only - one dig at a time. everything catalogued but not dug yet lives in search, honestly marked."),
        "software": ("SOFTWARE", "The software shelf - emulators, tools, fixes.",
                     "this shelf shows the dug pages only. the first software dig lights it up."),
        "mods": ("MODS+PATCHES", "The mods and patches shelf.",
                 "this shelf shows the dug pages only. the first mod or patch dig lights it up."),
    }
    for sec, (t, d, note) in list_pages.items():
        p = os.path.join(ROOT, "pages", sec + ".html")
        open(p, "w", encoding="utf-8").write(R2.list_page(eng, sec, t, d, note))
        written.append("pages/%s.html" % sec)
        p = os.path.join(ROOT, "pages", sec, "collections.html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(R2.section_collections_page(eng, sec))
        written.append("pages/%s/collections.html" % sec)

    open(os.path.join(ROOT, "pages", "search.html"), "w", encoding="utf-8").write(R2.search_page(eng))
    written.append("pages/search.html")
    open(os.path.join(ROOT, "pages", "random.html"), "w", encoding="utf-8").write(R2.random_page(eng))
    written.append("pages/random.html")
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(R2.main_page(eng))
    written.append("index.html")

    for c in eng.collections:
        sec = c.get("section") or "games"
        p = os.path.join(ROOT, "pages", sec, "collections", c["slug"] + ".html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(R2.collection_page(eng, c))
        written.append("pages/%s/collections/%s.html" % (sec, c["slug"]))
        legacy = os.path.join(ROOT, "pages", "collection", c["slug"] + ".html")
        os.makedirs(os.path.dirname(legacy), exist_ok=True)
        target = R2.rel("", "pages/%s/collections/%s.html" % (sec, c["slug"]), 2)
        open(legacy, "w", encoding="utf-8").write(
            '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta http-equiv="refresh" content="0; url=' + target + '">'
            '<link rel="canonical" href="' + target + '"><title>redirecting...</title></head>'
            '<body><p class="crumb" style="padding:40px">collections live under their shelves now - '
            '<a href="' + target + '">go to ' + esc(c["title"]) + '</a></p></body></html>')
        written.append("pages/collection/%s.html (legacy redirect)" % c["slug"])
    for m in eng.multis:
        if m.get("_sec"):
            p = os.path.join(ROOT, "pages", m["_sec"], "collections", m["slug"] + ".html")
        else:
            p = os.path.join(ROOT, "pages", "meta", m["slug"] + ".html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(R2.meta_page(eng, m))
        written.append(os.path.relpath(p, ROOT).replace("\\", "/"))
    top_legacy = os.path.join(ROOT, "pages", "collections.html")
    open(top_legacy, "w", encoding="utf-8").write(
        '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta http-equiv="refresh" content="0; url=' + R2.rel("", "pages/games/collections.html", 1) + '">'
        '<title>redirecting...</title></head><body><p class="crumb" style="padding:40px">'
        'collections live under their own shelves now - <a href="' + R2.rel("", "pages/games/collections.html", 1) + '">games collections</a></p></body></html>')
    written.append("pages/collections.html (legacy redirect)")

    for r in eng.redirects.get("redirects", []):
        sec = r.get("sec", "games")
        d = {"games": "game", "software": "software", "mods": "mod"}[sec]
        p = os.path.join(ROOT, "pages", d, r["from"] + ".html")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(R2.redirect_page(eng, r, sec))
        written.append("pages/%s/%s.html (redirect)" % (d, r["from"]))

    idx_meta = {"_meta": {"built_by": "tools/build.py", "v": BUILD_V, "rows": len(eng.rows),
                          "law": "catalog layer only - version sub-pages do not ride the index"}}
    jwrite(os.path.join(ROOT, "data", "search-index.json"), {"_meta": idx_meta["_meta"], "rows": eng.rows}, compact=True)

    manifest = {"_meta": {"built_by": "tools/build.py", "v": BUILD_V}, "items": []}
    for slug in sorted(eng.page_by_slug):
        u = eng.page_url_of(slug)
        if u:
            manifest["items"].append({"u": u, "t": eng.title_of(slug)})
    for c in eng.collections:
        manifest["items"].append({"u": eng.collection_url(c["slug"]), "t": c["title"]})
    for m in eng.multis:
        manifest["items"].append({"u": eng.collection_url(m["slug"]), "t": m["title"]})
    jwrite(os.path.join(ROOT, "data", "random-manifest.json"), manifest, compact=True)

    for sec in ("games", "software", "mods"):
        shelf = [r for r in eng.rows if r["sec"] == sec and r.get("page")]
        jwrite(os.path.join(ROOT, "data", "shelf-%s.json" % sec),
               {"_meta": {"built_by": "tools/build.py", "v": BUILD_V, "rows": len(shelf),
                          "law": "the shelf layer: dug pages of this section only. the full catalogue rides search-index.json"},
                "rows": shelf}, compact=True)

    public_rows = []
    for g in eng.catalog_games:
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
        "_meta": {"schema": "ggs.v2", "updated": "2026-10-10",
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
    page_dirs = ["game", "software", "mod", "collection", "meta"]
    for sec in ("games", "software", "mods"):
        page_dirs.append(os.path.join(sec, "collections"))
    for d in page_dirs:
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
