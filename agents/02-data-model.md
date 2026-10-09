# 02 — the data model

three layers, one direction of flow: lists (sacred) → databases → engine
output. never edit generated files by hand.

## layer 1 — the owner's lists (sacred, as-is)

`work/original-lists/` — the owner's own text files, never rewritten,
mirrored sorted in `sorted/` for lookup only. every catalog row must trace
to a line in these files (law 7) or be an endorsed upgrade hub.

## layer 2 — the databases

### work/lists/games/games.json — the catalog

```json
{
 "slug": "chicken-invaders-3-revenge-of-the-yolk",
 "title": "Chicken Invaders 3: Revenge of the Yolk",
 "list": "casual",                      owner's list it came from
 "class": "...",                        owner's class marker
 "category": "fixed shooters",          LIVE rows: ONE precise category each.
                                       catalog rows keep the owner's own
                                       section header (his list organization)
 "series": "chicken-invaders",          series key (data/series.json)
 "series_part": 3,
 "content_walls": ["gore"],             sex/gore live HERE, nowhere else
 "big_size": false,
 "release": "2007-01-20",               ISO date, null when unknown
 "developers": [], "publishers": [],
 "platforms": ["windows"],              never "PC" — windows is the name
 "players": {                           the five-mode vocabulary (03)
   "single": true, "local_coop": false, "online_coop": false,
   "local_multi": false, "online_multi": false, "max_local": 1},
 "buyable": true,                       verified sold-state, null = unknown
 "download_kind": "...", "test_status": "not-tested",
 "target_os": "windows-10", "haswell_igpu_ok": true,
 "confidence": "verified",              verified = sourced row
 "size_est_mb": 170, "size_source": "store-stated",
 "genres": [], "subgenres": [],         caps: 5 + 5 (03)
 "upgrades": ["chicken-invaders-4-ultimate-omelette"],
 "remaster": "chicken-invaders-remastered",
 "superseded_by": null,
 "version_of": null,                    set = this row is a version, not catalog
 "sources": [], "notes": ""
}
```

laws:
- `version_of` set → the engine hides the row from the catalog layer (search,
  facets, counts, similars, collection items) while still rendering its page.
- `upgrades` = the direct line (next episode). `remaster` = the remaster hub
  covering old games + DLCs. `superseded_by` = the standalone is gone.
- out-of-scope rows sleep in `work/lists/games/attic/` with a dated file and
  a reason. restore only on explicit owner order.

### work/data/pages/<slug>.json — the page flesh

caption (one breath), about[] (what it is, how to patch, what software does —
never a meta "why this page exists"), gallery{images[10], videos[3]},
links{official[], official_note, anyway[], anyway_note}, req{tier,note},
characters[] (law 9), thumbnail, versions[] (mainlines declare, release
order), release_label (versions), dug_seq (dig order for latest-digs).

### work/data/collections.json + redirects.json

collections + multi-collections (04), slug aliases → meta-refresh pages.

## layer 3 — engine output (generated, never hand-edited)

- `pages/**/*.html` — every page, from tools/build.py.
- `data/search-index.json` — catalog-layer rows only (versions excluded).
- `data/random-manifest.json` — every real page incl. versions + collections.
- `data/games.json` — public catalog rows with pages, for embedders.
- `work/lists/games/counts.json` + `name-check/` — from tools/lists_check.py.

## series registry

`data/series.json` (engine copy) + `work/lists/games/series.json` (source):
key → members[]. members not in the catalog silently drop out of series
lines (attic'd games leave the line without editing anything).
