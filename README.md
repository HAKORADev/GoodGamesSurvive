# GOODGAMES SURVIVE

**an archive of good games that outlived their era.** downloads, cracks for
the un-buyable, mods, patches, upgrade paths. target: games that run on
whatever, specifically haswell devices with HDxxxx iGPUs, windows 10.

live at: `https://hakoradev.github.io/GoodGamesSurvive/`

## what this is

- **page per thing** — one page per game, per software, per mod, per patch,
  per collection. no hubs, no grids on the main page: the main page is clean
  ground (logo + brand mark + caption).
- **per-page gallery** — steam-style media strip on each game page, built
  from verified hot-linked sources only. no empty slots, ever.
- **recommendation engine** — every page says which series it belongs to
  (clickable) and which archive games are similar to it.
- **content walls, not age ratings** — hard-wall tags `sex` and `gore`
  describe what the game IS. a +18 age rating is not a wall.
- **big-size law** — `big_size` is true only when the full version (highest
  tier, all DLC) needs more than 15 GB of disk after repack download + unzip.
  the number is verified, not guessed.
- **honest test status** — every page says `tested` (the owner downloaded,
  played, pathed, modded it) or `not-tested`. nothing in between.

## the offering

| kind | meaning |
|---|---|
| `legal` | free/official distribution, link straight to it |
| `anyway` | game still sold in stores — archive link + "you can anyway buy it" link, both on the page |
| `un-buyable-crack` | the game needs a key that no living server can validate (think old Reflexive Arcade trial-unlock titles). nobody loses anything. we rescue it. |
| `redirect` | we point at trusted archives (oldgamesdownload, myabandonware, romsfun, fitgirl, rg mechanics) |

## repo map

```
index.html            main page: logo, brand mark, caption. nothing else.
assets/css/style.css  monochrome retro system
data/                 the public database (page-backed rows only), schema ggs.v1
pages/                page per thing (game/software/mod/collection pages)
pages/tpl/            page templates
work/                 the workspace: original lists as-is + sorted, the full
                      games database (owner-listed + verified), series registry,
                      name-check, expansion logs, software/mods lists
tools/lists_check.py  database health check: parses, validates, regenerates
                      the name-check file, writes counts
.github/workflows/    lists-check CI: runs the checker on every push
brand-style-more.md   the shared memory file: brand, laws, decisions
agents.md             field manual for agent sessions (how to add, check, scrape)
```

## how a game enters the site

1. check `work/lists/games/name-check/games-added.txt` — if the name is
   there, stop. the game is in.
2. verify the row (release date, developer, publisher, players, platforms,
   walls, big-size) with sources. unknown stays null. no invented facts.
3. add the row to `work/lists/games/games.json`. run `tools/lists_check.py`
   (or push — CI runs it and commits the regenerated name-check).
4. build the page from `pages/tpl/`, wire the row into `data/games.json`.
5. the page carries: facts block, series link, similar-to links, download
   links by kind, test status, content walls, size class.

## data flow

```
owner lists (work/original-lists/as-is/)
   -> debunk/verify pass
   -> work/lists/games/games.json   (full database, every row carries confidence)
   -> page-backed rows distilled into data/games.json
   -> pages render from data/
```

CI regenerates the name-check file and the counts on every push, so the
"what is already in" question always has a fresh answer.
