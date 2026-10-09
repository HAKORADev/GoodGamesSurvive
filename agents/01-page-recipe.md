# 01 — the page recipe

how any page (game, software tool, mod, collection, meta-collection) gets
created. same shape every time — this is how the site stays one design.

## the five moves

### move 1 — collect
- the thing must earn a page: it is on the owner's lists, or it is an
  endorsed upgrade path (law 7).
- gather: exact title, release date, developer, publisher, platforms,
  players modes, series + part, size with source, buyable state, content
  walls, genre/sub-genre/category, characters (law 9).
- mass-spam-info-collection: run the same queries for every candidate field
  in one pass (stores first: Steam / GOG / publisher site; then MobyGames /
  Wikipedia for dates and ports; then archive.org for the anyway route).
  one research pass per thing, every claim written down with its source.

### move 2 — verify
- every factual claim carries a source or does not ship (law 4).
- dates: store page or MobyGames. sold-state: the store page answers "add to
  cart" yes/no TODAY. size: the store's stated download/install size, or the
  archive item's file listing. never guess from memory.
- official path exists? test the URL returns 200 and actually sells or
  distributes the game. demos are not the game — label them honestly.
- anyway route: a real archive.org item, a real mirror. curl it. if it 404s
  in the future, the gallery law (05) keeps the site unharmed — but links
  verified at build time is the standard.

### move 3 — data
- catalog row first: `work/lists/games/games.json` (schema: 02-data-model.md).
- then the page file: `work/data/pages/<slug>.json` — caption, about,
  gallery, links, req, characters, thumbnail, dug_seq.
- slug law: lowercase, hyphens, full title (`chicken-invaders-3-revenge-of-
  the-yolk`). editions/versions get `version_of` + `release_label`, and the
  mainline gets `versions: [slugs in release order]`.
- run `python3 tools/lists_check.py` — it validates and regenerates the
  name-check and counts.

### move 4 — build
- `python3 tools/build.py` must end `BUILD: CLEAN`. the engine renders every
  page from the data; nothing is hand-edited in `pages/` (see 07).
- new page appears automatically: shelf index, search index, facets, random
  manifest, main-page latest digs, collection membership if wired.

### move 5 — connect the dots
- series: the page links its series line automatically from
  `data/series.json` membership.
- collections: add the slug to the collection's `items` in
  `work/data/collections.json` (04-collections.md).
- versions: mainline declares the version list; every version page gets the
  dropdown; upgrade lines come from `upgrades` / `remaster` / `superseded_by`
  fields on the rows.
- similars: computed by the engine from shared genre/sub-genre/category +
  era + developer, series-mates and collection-mates excluded. no manual
  "you may also like" lists.

## what a page shows, in order

crumb → title + caption + chips → GALLERY → ABOUT {TITLE} → FACTS
(characters live here, as linkable entries) → REQUIREMENTS vs the haswell
target → VERSIONS & UPGRADES → SERIES line → COLLECTIONS line → DOWNLOADS
(official / official-status strip / anyway) → MORE LIKE THIS → the
tested/not-tested box.

the same skeleton fits a software tool or a mod — facts trimmed to what the
row carries, downloads same law, gallery when media exists.
