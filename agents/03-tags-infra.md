# 03 — the tag infra

the owner was explicit: there is no "tag". the system below IS the tag
system — structured, capped, honest. it drives the facts table, the chips
and the store facets on every shelf.

## the vocabularies

| facet | source field | cap | notes |
|-------|-------------|-----|-------|
| GENRE | `genres` | 5 | the big families: stealth, shoot 'em up, time management... |
| SUB-GENRE | `subgenres` | 5 | the sharpening: social stealth, fixed shooter, resource management |
| CATEGORY | `category` | 1 | the owner's own list-section header, verbatim minus emoji |
| CONTENT | `content_walls` | free | the walls: sex, gore, +18... |
| PLAYERS | `players{}` | modes | single-player / local co-op / online co-op / local multiplayer / online multiplayer |
| PLATFORM | `platforms` | free | windows, linux, ps2... **never "PC" — it is windows** |
| ERA | derived from `release` | decade | 1990s, 2000s... |
| STATUS | derived | — | tested / verified / big-size / still sold / un-buyable |

## the hard rules

1. **sex and gore are content walls, not genres.** if they ever show up in
   `genres`/`subgenres`/`tags`, that is a bug — move them to
   `content_walls` and fix the source row.
2. **no field named `tags`.** the row schema has none; old rows were
   scrubbed (2026-10-09). anything that used to be a tag belongs to one of
   the vocabularies above or it does not exist.
3. **players is the five-mode vocabulary.** no "multiplayer" blob, no
   invented co-op claims. verify per game; when the sources disagree with
   the row, the row loses.
4. **one each on live rows**: a page-backed row carries exactly ONE genre,
   ONE sub-genre, ONE precise category (CI = shoot 'em up / fixed shooter /
   fixed shooters; hitman = action / stealth / stealth action; dash = casual /
   time management / restaurant management). the multi-value caps below are
   catalog-layer ceilings, not license to stack.
5. **caps are real**: max 5 genres, max 5 sub-genres per row. the facets UI
   shows the top 14 values per facet by live count — never a wall of chips.
5. **every facet value is a link.** chips on pages and facet chips on shelves
   both feed URL params (`?genre=`, `?sub=`, `?category=`, `?content=`,
   `?players=`, `?platform=`, `?era=`, `?status=`, `?character=`,
   `?series=`, `?dev=`, `?pub=`, `?q=`) — the shelf engine reads them all
   and shares state in the address bar, so every filtered view is a link.
6. **characters are indexed like facets.** the facts row links
   `?character=flo` and the shelf filters by it. characters come from page
   files, catalog rows carry none.
7. **category display strips emoji** (the monochrome law); the key keeps the
   owner's wording so his sections stay intact.

## where it lives in the engine

- vocab build + keyify: `tools/kage_core.py` `build_vocab()`.
- row facets: `index_row()` — `g`, `gs`, `cat`, `w`, `pl`, `p1/lc/oc/lm/om`,
  `era`, `ch`.
- facet UI + URL state: `LIST_JS` in `tools/kage_render2.py` — facet groups
  in the order GENRE, SUB-GENRE, CATEGORY, CONTENT, PLATFORM, PLAYERS, ERA,
  STATUS.
- when adding a new vocabulary: row field → index_row → facetOf → groups →
  chips/facts. one pass, then build + test (08).
