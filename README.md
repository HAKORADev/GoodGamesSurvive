# GOODGAMES SURVIVE

**an archive of good games that outlived their era.** downloads, cracks for
the un-buyable, mods, patches, upgrade paths. target: games that run on
whatever, specifically haswell devices with HDxxxx iGPUs, windows 10.

live at: `https://hakoradev.github.io/GoodGamesSurvive/`

## what this is

- **page per thing** — one page per game, per software, per mod, per
  collection. the main page stays clean: brand mark, the latest digs per
  section with jump-to links, the collections, live totals.
- **versions, not release spam** — holiday editions and re-releases live as
  switchable versions under their game's page (the dropdown), never as
  standalone catalog entries.
- **per-page gallery** — steam-style media strip on each game page: 10
  images + 3 no-commentary gameplay videos, hot-linked only. a dead URL
  renders MEDIA NOT FOUND and nothing breaks.
- **store-grade search** — facet chips with live counts (genre, sub-genre,
  category, content, platform, players, era, status), seeded random sort,
  shelf-scoped random button, site-wide search.
- **collections** — real shelves (The Hitman Collection, The Chicken
  Invaders Collection) plus meta-collections that hold collections.
- **honest everything** — official path first where one survives, the
  archive route next to it, anyway-only for the dead ones. tested /
  not-tested is a truth, not a decoration. counts are computed, never
  hardcoded.

## repo map

```
index.html            main page: brand mark, latest digs, collections, live stats
assets/css/style.css  monochrome retro system
data/                 generated: search index, random manifest, public rows
pages/                generated: every page (game/software/mod/collection/meta)
work/original-lists/  the owner's lists, as-is + sorted (sacred)
work/lists/           the databases: games.json (catalog), software, mods,
                      attic/ (out-of-scope rows, dated + reasoned), series,
                      name-check, expansion logs
work/data/pages/      page flesh: caption, about, gallery, links, req, characters
work/data/            collections.json, redirects.json
tools/build.py        THE ENGINE: renders every page + data files
tools/lists_check.py  database health check (CI runs it on every push)
agents.md             the field manual — points into agents/
agents/               the powerup rack: laws, page recipe, data model, tag
                      infra, collections, media, search, templates, testing,
                      expansion — one concern per file
.github/workflows/    lists-check CI
brand-style-more.md   the shared memory file: brand, laws, decisions
```

## how a game enters the site

1. check `work/lists/games/name-check/games-added.txt` — if the name is
   there, stop. the game is in.
2. verify the row (release, developer, publisher, players, platforms, walls,
   size + source, buyable) with sources. unknown stays null. no invented
   facts.
3. add the row to `work/lists/games/games.json`. run `tools/lists_check.py`.
4. when it earns a page: write `work/data/pages/<slug>.json` (the page
   recipe lives in `agents/01-page-recipe.md`), run `tools/build.py` until
   `BUILD: CLEAN`, commit, push.
5. versions/editions ride `version_of`; upgrades ride `upgrades` / `remaster`
   / `superseded_by`; collections ride `work/data/collections.json`.

## data flow

```
owner lists (work/original-lists/, as-is, sacred)
   -> verify pass (sources or null)
   -> work/lists/games/games.json     full catalog (versions flagged, attic for out-of-scope)
   -> work/data/pages/<slug>.json     page flesh when a dig happens
   -> tools/build.py                  every page + data/search-index.json
                                      + data/random-manifest.json + data/games.json
```

CI regenerates the name-check file and the counts on every push, so the
"what is already in" question always has a fresh answer.
