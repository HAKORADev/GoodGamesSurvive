# agents.md — the field manual

this file exists so the next agent session (me, later, with wiped memory)
spends zero time re-figuring the system. read this + brand-style-more.md
and you know everything.

## 0. standing rules

1. all replies in English.
2. re-verify disk state + token every round. the sandbox resets; the repo
   is the memory. clone fresh when unsure:
   `git clone https://<TOKEN>@github.com/HAKORADev/GoodGamesSurvive.git`
3. worklog at `/home/z/my-project/worklog.md` — read it first, append after.
4. no comments in code (diagnostic markers are the exception).
5. no fake facts, no invented names, no hallucinated dates. unknown = null.
   a null field is honest; a made-up date is a landmine.
6. no AI-slop text anywhere. no "welcome to", no "look no further", no
   emoji in copy, no placeholders ("EMPTY SLOT" era is over — owner killed it).
7. do not add interactivity the owner never asked for.

## 1. the shape of the system

```
owner lists (as-is, sacred)
  -> work/lists/games/games.json            (full DB, 708 rows, schema ggs.v2)
  -> work/data/pages/<slug>.json            (rich page content: caption/about/gallery/links/req/characters)
  -> work/data/collections.json             (collections + multi-collections source)
  -> work/data/redirects.json               (slug aliases -> meta-refresh pages)
  -> tools/build.py  (THE ENGINE)           -> every html page + data/search-index.json + random manifest
  -> tools/lists_check.py                   -> validates DBs, regenerates name-check + counts (CI)
```

- KAGE ENGINE LAW: `tools/build.py` owns ALL page HTML and `data/search-index.json`.
  never hand-edit generated pages - edit the source data and rebuild. the only
  hand-maintained files are the data sources + tools.
- ASSET VERSION LAW: bump `BUILD_V` in tools/kage_core.py on any css/js/index
  change; it propagates to every page automatically.
- media law: every gallery URL is verified live (HTTP 200, image/*) by
  scripts before it enters page JSON; every page renders a "MEDIA NOT FOUND"
  fallback via onerror at runtime. galleries are URL links only - 10 images
  + 3 no-commentary videos per game page, exact.
- similars law: build-time scoring (genres x3, subgenres x2, tags x2, era/dev/co-op x1),
  same-section only, same-series and same-collection excluded, top 10, why-line shown.
- versions law: same-title releases share a `group`; pages render a release
  switcher. `upgrades` on a row points TO its upgrade (direct or remaster);
  `superseded_by` marks delisted-absorbed releases (WoA case).
- requirements law: tier ladder vs the target bar (below / at / above
  haswell HDxxxx + win10). test status stays a separate truth.
- official/anyway law: both buckets on every page. official may be dead
  (delisted note) - anyway carries the rescue. Diner Dash is the model case.
- counts law: top-bar nav counts are PAGE-BACKED counts (pages dug), not DB rows.


## 2. how to add a game (full protocol)

1. **name-check**: search `work/lists/games/name-check/games-added.txt`
   (case-insensitive). found = already in, stop. watch renames ("Watch Dogs
   1" is filed as "Watch Dogs"; year/platform suffixes are stripped into
   fields).
2. **research**: hunt facts. most-referenced sources:
   oldgamesdownload, myabandonware (games), romsfun (console), steam/gog
   store pages (release dates, devs, publishers, players, sizes), fitgirl /
   rg mechanics / steam-unlocked / gog-unlocked / torrent trackers (repack
   size reality check), youtube descriptions for mediafire/gdrive links.
   save every source URL into the row's `sources` array.
3. **fill the row** in `work/lists/games/games.json`:
   - required: title, slug, list, class, series, content_walls, big_size,
     test_status, confidence, platforms, players, sources
   - `series`: check work/lists/games/series.json — extend the registry if
     it's a new series
   - `content_walls`: `sex` and `gore` only. judge by what the game IS.
     age ratings are not walls (GTA is +18, not a wall).
   - `big_size`: true only if full version (highest tier, all DLC) needs
     >15GB installed after repack + unzip. put the verified number in
     big_size_gb. when unsure: false + a note to verify at page time.
   - `buyable`: still sold somewhere? true -> page gets an "anyway" link
     next to the archive links.
   - `test_status`: "not-tested" unless the owner says they tested it.
     the owner is the only tester.
   - `haswell_igpu_ok`: null until tested or clearly documented.
4. **run** `python3 tools/lists_check.py` locally (or push — CI runs it and
   commits the regenerated name-check + counts).
5. **page**: copy `pages/tpl/game.html`, fill from the row, add to
   `data/games.json` (this is the step that makes it public), commit.
6. **media**: gallery = steam-style (up to 10 images + 3 videos). sources:
   Steam CDN (`cdn.cloudflare.steamstatic.com/steam/apps/<appid>/...`),
   GOG images. HEAD-verify every URL. no slots, no placeholders: the
   gallery renders only what exists. thumbnails: header.jpg pattern.

## 3. how to edit pages safely (multi-editing)

- pages are plain HTML; each has a `data-game` slug attribute on
  `<body data-game="...">` so tooling can find them.
- regenerate rows from games.json, not by hand, when numbers change.
- style changes go in `assets/css/style.css` once, never per-page.
- new template variants for other things (software/mod/collection) go in
  `pages/tpl/` — Kage direction: every thing is a page template.

## 4. scraping notes

- steam appdetails API: `store.steampowered.com/api/appdetails?appids=N`
  works for most games; age-gated ones return success:false even with
  cookies -> use the GOG page instead, or the header.jpg CDN pattern.
- steam CDN patterns (verify with HEAD before use):
  - header: `.../steam/apps/<id>/header.jpg`
  - capsule: `.../steam/apps/<id>/capsule_616x353.jpg`
  - screenshot: `.../store_item_assets/steam/apps/<id>/ss_<hash>.1920x1080.jpg`
- oldgamesdownload returns 403 to scripts (bot wall) but its pages are
  real and reachable in browsers — link them, don't scrape them.
- youtube descriptions: use for mediafire/gdrive links; verify they open.

## 5. CI

`.github/workflows/lists-check.yml` runs `tools/lists_check.py` on every
push: parses all JSON, checks slug uniqueness + required fields, regenerates
the name-check file and counts.json, commits them if changed. if CI goes
red: the row you just added broke the schema — fix the row, not the checker.

## 6. the future (owner's stated direction)

- Kage / Kage-Pages rebrand: one engine, page template per thing
  (app/mod/character/site/other). databases are built slug-first so they
  integrate into it later.
- expansions along the spine: "good sites survive", "good characters survive".
- /admin: main link + /admin checks the logged-in github account; owner gets
  visual editing (add/edit pages). mechanism TBD.
- top bar will carry tags/contents/genres/numbers, clickable to sort, for
  games AND software AND mods.

## 7. first pages (shipped 2026-10-09)

- `pages/game/hitman-blood-money.html` — non-casual classic, still sold
  (steam + gog anyway links), series hitman, not-tested
- `pages/game/chicken-invaders-5.html` — casual arcade, still sold (steam
  + official site), series chicken-invaders, multiplayer, not-tested
- `pages/game/diner-dash.html` — casual root of the Dash universe,
  un-buyable-crack (dead unlock servers), series diner-dash, not-tested

## 8. browser-facing laws (learned 2026-10-09, owner hit a stale-cache break)

- ASSET VERSIONING LAW: every time style.css / any js / search-index.json
  changes, bump the `?v=N` on its link/fetch in ALL html files (grep
  `style.css?v=` to find them). browsers held an old style.css and the owner
  saw the new html unstyled — never ship css changes without the bump.
- TOP BAR LAW: the site-head (logo + nav counts + search box) is site-wide —
  every page carries it, counts are real (3 games, 0 software, 0 mods today).
  the GAMES link gets class="here" on pages/games.html.
- SEARCH LAW: pages/search.html is the site-wide search. the index
  data/search-index.json is regenerated by tools/lists_check.py on every push
  (CI too). page-backed slugs auto-detect from pages/game/*.html filenames;
  each page's game-cover img is its thumb. new game page + lists_check run =
  it appears in search with thumb, zero bookkeeping.
- THUMBS: steam headers (cdn.cloudflare.steamstatic.com/steam/apps/ID/header.jpg)
  for steam games; self-hosted assets/media/ for un-buyable games (diner-dash
  cover = official XBLA key art, cropped front). no hotlinking fragile fansites.
