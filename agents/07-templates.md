# 07 — templates: edit once, expand forever

the owner's law: **make templates so you edit once and expand easily
forever.** the template system is not a folder of html skeletons — it is the
engine itself.

## how it works

```
data (lists + pages + collections + redirects)
  -> tools/build.py  (the one entrypoint)
       tools/kage_core.py     — Engine: loads everything, builds vocab, index,
                                similars, versions, upgrade lines, facts
       tools/kage_render.py   — the page chrome (head/topbar/foot) + game pages
       tools/kage_render2.py  — shelves, search, random, main page, collections,
                                meta pages, redirect pages, the shelf JS
  -> every html file in pages/ + index.html + data/*.json
```

## the laws

1. **nothing in `pages/` is hand-edited.** a page is data + engine. to change
   how all game pages look, change `game_page()` once — 400 pages update on
   the next build. that is the whole point.
2. **a widget is a function.** versions dropdown, downloads blocks, req
   ladder, gallery, facts — each is one function in kage_render. if two
   renderers need it, it lives in kage_render and gets imported. no widget
   exists twice.
3. **no stale template files.** `pages/tpl/` was deleted (2026-10-09): a
   hand-maintained html skeleton that drifted from the engine is worse than
   none — it makes future sessions copy the wrong thing. the engine IS the
   reference; read its output, not a parallel copy.
4. **new page type = new render function + one branch in build.py.** wire it
   into: the shelf loop, the nav, the search index (if it belongs to the
   catalog layer), the random manifest, the main page (if it has "latest").
5. **counts are computed, never hardcoded.** sec_counts(), pages_dug(),
   n_pages, collection counts, the main page stats line — all derived at
   build time. a hardcoded number is a lie waiting to happen.
6. **build before commit** (law 18): `python3 tools/build.py` ends
   `BUILD: CLEAN` in the same breath as the commit. the engine deletes
   stale generated pages (cleanup()) — trust it, read its report.
7. **build stamp everywhere** (06): BUILD_V is time-based per build and is
   stamped on css + index + manifest fetches. stale caches can never show
   old data.

## adding a field end-to-end (the checklist)

row field → lists_check REQUIRED (if mandatory) → engine index_row/facts_of →
render (facts table / chips / downloads) → LIST_JS facet if it is a facet →
build → QA battery (08). one pass through all seven, or it does not ship.
