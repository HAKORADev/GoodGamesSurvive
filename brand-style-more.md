# brand-style-more.md — GOODGAMES SURVIVE

> shared memory file. both of us add on this so we never lose context.
> last updated: 2026-10-09 (structure drop, main page skeleton live)

---

## 1. what this site is

**GOODGAMES SURVIVE** — an archive of good games that outlived their era.
not "any good game". the bar: the game survived its era and is still there — still playable, still loved, still worth your machine.

- we **show and direct** people, not lecture them. text serves the eyes, short and dry.
- we **offer download links for everything**: games, software, mods, patches. if it's on a page, it's reachable.
- the collection the owner holds: **+500 titles**, of which **+20 are deep-buried hidden games** that no search engine or AI could surface without deep multi-source digging. the +20 are the crown jewels — proof the archive is not a copy of a wiki list.
- pages are **page per thing**: one page per game, per software, per mod, per patch, per collection.
- **collections** hold games. **multi-collections** hold collections (a collection whose items are collections). nesting is a first-class feature.

## 2. brand identity

### the name
`GoodGamesSurvive` — reads as a sentence: good games survive.

### the logo — WA?D
four keycaps in a row, drawn like keyboard keys, each standing for a direction:

```
[W]=up   [A]=left   [?]=down   [D]=right
```

- it spells **WASD** — the PC gaming keys — with the **S replaced by ?**.
- S is the "down" key: dig down, look down, descend. replacing it with `?` makes the down direction unknown — **buried memory**. you know there's something below, you just can't see it.
- built in pure HTML/CSS (no image), arrows are inline SVG triangles. the `?` key occasionally flickers revealing a `↓` underneath (CSS animation `remember`) — the memory flashes, then buries again.
- favicon: single keycap with `?` (inline SVG data URI).

### the brand mark — WASTED → IT
the hero visual, referencing the death screen:

1. the word **WASTED** in big slab serif (Alfa Slab One), letterspaced, faint white glow.
2. **scratch gouges** cut across it — SVG diagonal strokes in the background color, so they only appear where they tear the letters. two thin light "glint" hairlines alongside.
3. a stamped **IT** on top — rotated ~-7°, white border, dark fill, stamps in with a scale-bounce animation on load.

meaning: they pronounced it *wasted*. we scratched it and stamped *IT*. the game didn't die — it survived. this mark is the whole site thesis in one image.

### tagline options (rotate, don't hardcode one)
- "not wasted. IT survived."
- "good games don't die. they get buried. we dig."
- "buried memory, dug back up."

## 3. visual style — monochrome retro

strict monochrome. no color anywhere. retro = CRT death-screen + terminal.

### palette
| role | hex |
|---|---|
| background | `#070707` |
| panel | `#0e0e0e` |
| panel raised | `#141414` |
| line | `#262626` |
| line strong | `#3d3d3d` |
| text ink | `#e8e8e8` |
| text white | `#f4f4f4` |
| dim text | `#9a9a9a` |
| faint text | `#5c5c5c` |
| ghost (placeholders) | `#2c2c2c` |

### typography (Google Fonts, hot-linked)
| use | font |
|---|---|
| display (WASTED, wordmark, big glyphs) | **Alfa Slab One** |
| pixel UI labels (section tags, slots, chips) | **Silkscreen** |
| body text | **IBM Plex Mono** |
| terminal accents (meta chips, file rows) | **VT323** |

### CRT atmosphere
- fixed scanlines overlay (repeating gradient, subtle flicker keyframes)
- vignette (radial gradient, darker corners)
- static-noise texture on empty slots (inline SVG `feTurbulence` data URI)
- placeholders speak the language: "EMPTY SLOT", "AWAITING SIGNAL", "SLOT RESERVED", "TBD", "?" glyphs

### rules
- desktop-first, but mobile shouldn't break (basic media query at 900px).
- no color accents ever. hierarchy = size, weight, borders, brightness.
- easter eggs allowed if cheap and on-theme (current: press **S** → toast "S NOT FOUND — BURIED MEMORY" + the ? keycap flashes).

## 4. writing system (switchable tones)

writing is **not hardcoded** in pages. plan:

- a tone registry lives in `data/tone.json` — `{"active":"neutral","tones":{...}}`.
- page copy comes from data/templates so we can **switch tone site-wide** (e.g. `neutral` / `dry` / `hype` / `terminal`) without touching markup.
- tone rules: short sentences. no marketing fluff. no AI-slop phrasing. dry humor allowed. the reader is a player, not a customer.
- for now the main page copy is static (structure phase); the tone system activates when content passes start.

## 5. site architecture (current + planned)

### live now (structure phase)
```
/
  index.html            main page, all sections, empty-state skeletons
  assets/css/style.css  full monochrome retro system
  assets/js/main.js     search teaser type-loop + S easter egg
  data/*.json           empty database skeletons (schema ggs.v0)
  brand-style-more.md   this file
```

### main page sections
| # | section | purpose |
|---|---|---|
| 00 | GALLERY | steam-style strip: 10 image slots + 3 video slots, one featured + thumbnail row |
| 01 | THE SHELF | game grid: thumbnail cards, one per game, links to game pages |
| 02 | MUST-HAVE TOOLBOX | software that is a must to have; each gets a page + download link |
| 03 | MODPACKS + PATCHES | community fixes wired to their target game pages |
| 04 | UPGRADE PATHS | per game: remaster / remake / spiritual successor indicator |
| 05 | COLLECTIONS + MULTI-COLLECTIONS | curated piles; nesting supported |

### planned next phases
- **page per thing**: `pages/game/<slug>.html`, `pages/software/<slug>.html`, `pages/mods/<slug>.html`, `pages/collections/<slug>.html`
- **gallery per game page**: same steam pattern (10 images + 3 videos) per game, not just homepage
- **search engine**: client-side, over the JSON database, with tagging + filters (era, type, tags, status)
- **downloads**: link fields on every thing; verify links during the debunk pass
- **tone switch**: activate `data/tone.json` + templated copy

## 6. data schema — ggs.v0 (draft, extensible)

all data lives in `data/*.json`, static, hot-linked by the frontend (code-only repo; media is hot-linked — repo stays tiny, bandwidth is code only).

```jsonc
// games.json — one entry per game page
{
  "slug": "", "title": "", "year": null, "era": "", "developers": [],
  "type": "game", "status": "survived",              // survived | lost | endangered
  "tags": [],                                        // free tags powering search
  "thumbnail": "",                                   // hot-linked
  "gallery": {"images": [], "videos": []},           // up to 10 + 3, steam-style
  "downloads": [{"label": "", "url": "", "kind": ""}],
  "upgrades": {"remaster": null, "remake": null, "spiritual_successor": null},
  "similar": [],                                     // cross-linked game slugs
  "collections": []                                  // collection slugs it belongs to
}

// collections.json — flat AND multi
{
  "slug": "", "title": "", "kind": "flat",           // flat | multi
  "items": [],                                       // game slugs (flat) or collection slugs (multi)
  "description": ""
}
```

`suggestions`: mods.json (per-mod target game), software.json (per-tool entries), upgrades.json (per-base-game paths) — same field style.

**debunking rule**: nothing enters the JSON unverified. owner's speedran list → we debunk each row (real? playable? link alive?) → only then it becomes a page.

## 7. platform notes

- hosting: **GitHub Pages** from `main` root (`https://hakoradev.github.io/GoodGamesSurvive/`).
- repo is **code-only**: images/videos hot-linked from the web, videos via embeds. GitHub soft limit 100GB — we'll never approach it since we serve only code.
- work style: **multi-pass commits**, verify live page after each pass, no comments in code (diagnostic markers are the exception).
- token workflow: raw REST via `scripts/ggs_push.py` (blobs→tree→commit→ref, handles root commit on empty repo).

## 8. next steps (agreed)

1. owner hands over the speedran lists (+500 / +20).
2. we **debunk** them together: verify each entry exists, is playable somewhere, drop fakes, merge dupes.
3. build the proper curated master list from the wreckage.
4. fill pages + collections from the master list, activate search + tags + tone system.

---

*add new decisions under this line, newest on top.*
