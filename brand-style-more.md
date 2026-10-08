# brand-style-more.md — GOODGAMES SURVIVE

> shared memory file. both of us add on this so we never lose context.
> last updated: 2026-10-09 (corrections round: ground cleaned, logo fixed to joystick diamond, laws added)

---

## 0. correction log (2026-10-09, owner verbatim)

- the logo WASD was supposed to be the **playstation joystick layout but as letters** — diamond, not a keycap row. fixed: W top (triangle position), A left (square position), ? bottom (cross position), D right (circle position).
- **? is not interactive.** no flicker animation, no press-S easter egg, no toast. never was requested. removed everywhere.
- WASTED → WAS(IT): **normal text, normal markdown mid-letter line (strikethrough) through TED, "IT" written over it.** not banner-like. no stamp box, no SVG gouges, no animation.
- **the whole site was AISlop.** all placeholders ("EMPTY SLOT", "AWAITING SIGNAL", "SLOT RESERVED", "TBD", "?" glyphs) are banned. we want the ground clean so we can build on it normally.
- **gallery is per-page** (per game page, steam-style). not on the main page. not on top of the site.
- **main page holds nothing per-thing.** no games grid, no must-have tools, no upgrade paths, no collections demo. clean ground: logo + brand mark + caption + footer. content lives on pages.
- site caption: **"a memory no longer buried"**.
- main page does not describe its own design. we are not writing "you have never seen google do something like this". no meta-commentary on pages.
- top bar: currently good for now. later, when pages open, it carries tags, contents, genres and numbers under it — clickable, to sort. games, software, mods, everything. (most sites use a side panel; we keep the top bar.)

## 1. what this site is

**GOODGAMES SURVIVE** — an archive of good games that outlived their era.
not "any good game". the bar: the game survived its era and is still there — still playable, still loved, still worth your machine.

- we **show and direct** people, not lecture them. text serves the eyes, short and dry.
- we **offer download links for everything**: games, software, mods, patches. if it's on a page, it's reachable.
- the collection the owner holds: **+500 titles**, of which **+20 are deep-buried hidden games** that no search engine or AI could surface without deep multi-source digging. the +20 are the crown jewels — proof the archive is not a copy of a wiki list.
- pages are **page per thing**: one page per game, per software, per mod, per patch, per collection.
- **collections** hold games. **multi-collections** hold collections (a collection whose items are collections). nesting is a first-class feature.
- **the goal is not "old games".** the goal is cool games — amazing ones, that work on whatever, **specifically haswell devices with haswell HDxxxx iGPUs**, target OS **windows 10**. some games even after 2020 qualify. we are not hunting quantity.

## 2. brand identity

### the name
`GoodGamesSurvive` — reads as a sentence: good games survive.

### the logo — WA?D in the joystick diamond
four letters arranged like the **playstation button diamond**, but as letters:

```
        [W]        W = triangle position (top)
     [A]   [D]     A = square position (left)   D = circle position (right)
        [?]        ? = cross position (bottom)
```

- it spells **WASD** — the PC gaming keys — with the **S replaced by ?**.
- directions match the controller exactly: up = W (triangle), left = A (square), down = ? (cross), right = D (circle). the down direction is unknown — **buried memory**. you know there's something below, you just can't see it.
- **? is NOT interactive.** it does not flicker, does not reveal, does not react. it sits there being a question. that is the whole point.
- built in pure HTML/CSS (no image), monochrome keycaps in a CSS-grid diamond. favicon: single keycap with `?` (inline SVG data URI).

### the brand mark — WASTED → WAS( IT )
plain text. the word **WASTED** in the slab display font. **TED carries a normal markdown-style strikethrough line** (mid-letter, through the letters). **"IT" is written over the struck part** — plain text, same type system, no box, no border, no rotation, no stamp, no animation.

reading: **WAS + IT** — "instead of wasted, it was it." past tense (WAS) buried inside the death word, present tense (IT) written on top. the survival story in five letters.

### caption
**"a memory no longer buried"** — the site caption under the mark.

### taglines (rotate when writing, don't hardcode)
- "a memory no longer buried"
- "good games don't die. they get buried. we dig."
- "not wasted. IT survived."

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

### typography (Google Fonts, hot-linked)
| use | font |
|---|---|
| display (WASTED, wordmark, big glyphs) | **Alfa Slab One** |
| pixel UI labels (chips, meta) | **Silkscreen** |
| body text | **IBM Plex Mono** |
| terminal accents (captions, meta rows) | **VT323** |

### CRT atmosphere
- fixed scanlines overlay (repeating gradient, subtle flicker keyframes)
- vignette (radial gradient, darker corners)
- **no static-noise textures, no placeholder glyph language.** empty is empty. the ground stays clean until real content lands on it.

### rules
- desktop-first, but mobile shouldn't break (media query at 700px).
- no color accents ever. hierarchy = size, weight, borders, brightness.
- **easter eggs: none.** owner never asked for them. do not add interactivity that was not requested.
- no AI-slop phrasing anywhere. no "welcome to", no "look no further", no emoji in copy.

## 4. the offering — how we provide games (owner law)

### 4.1 download kinds
- **legal download** — the game is sold/officially distributed and free, or officially freeware. link straight to the source.
- **anyway link** — the game still exists in stores (like AC or GTA V): we still give our links, marked "you can anyway buy it" — the archive link is for keeping, the store link is for supporting. both live on the page.
- **un-buyable cracks** — games that need a key to unlock and **no one can give or generate a valid key anymore** (example: the original **Reflexive Arcade** games — every publisher account is dead, the key servers are dead). since no one is going to lose something, **we will do this, even if it looked sketchy.** the crack is not theft here: there is nothing to steal from anyone. this is the rescue arm of the site.
- **redirects** — when we don't host or verify, we point at trusted archives. marked as such, honest.

### 4.2 test status (every page carries it)
- **tested** — the owner actually did it: downloaded, played, checked pathing, made it run, tested mods, everything.
- **not-tested** — the page carries links and verified facts, but nobody played this build yet. stated plainly on the page, never hidden.

### 4.3 reference sites (where hunting happens)
most referenced: **oldgamesdownload** and **myabandonware**.
also: torrent trackers, steam unlocked, gog unlocked, **fitgirl repacks**, **rg mechanics** — for games; **romsfun** for all console games.
mediafire / google drive links from scraped youtube descriptions, plus any useful link found.
mods: many sites. patches: simple DLL replacement, wrappers, and the like.
also: **online fixes for cracked AAA games**, and **VPN LAN** play to make games feel online again.

## 5. content laws — tags

### 5.1 hard-wall content tags (NOT steam-like genre tags)
- **sex** — replaces "+18". the game's content contains explicit sexual material. hard wall tag.
- **gore** — the game's content is gore-first (examples per owner: **Hatred**, **Manhunt**). hard wall tag.
- GTA being +18 does not make GTA a wall game. age ratings are not content walls. the walls are about what the game IS, not who may buy it.

### 5.2 big-size tag (accurate definition, replaces the loose one)
**big-size** = the game itself needs **+15 GB of disk space after repack download + unzip, at the full version** — meaning **deluxe / ultimate / highest tier with all DLCs**. the old tag missed games; every entry gets checked against the definition, not against a feeling.
verified so far (round of 2026-10-09): watch dogs, max payne 3, hitman absolution, far cry 3, call of duty mw2 (2009), metal gear rising, ac iv black flag, dbz kakarot, gta v, sleeping dogs (definitive), the sims 3 (complete) — kept; **added**: gta iv (complete ~31 GB), l.a. noire (complete ~27 GB), batman arkham city (~17-25 GB), assassin's creed iii (~17 GB), dragon's dogma dark arisen (~20-22 GB), ni no kuni remastered (~45 GB), bayonetta (~20 GB), mortal kombat x (~36 GB). **confirmed NOT big**: fallout 3 goty (~9 GB), skyrim legendary (~8.5-12 GB), saints row iv (~10 GB), mafia ii classic (~8 GB), tales of zestiria (~12 GB), red dead redemption pc port (~12 GB).

## 6. recommendation engine (planned, law decided)

- every game page says which **series** it is part of — the series name is clickable, leads to the series listing.
- every game page carries **"similar to"** links to other games in the archive. cross-linked by hand at page time, not by some algorithm nobody can audit.
- this engine also drives the **top bar sorting**: tags, contents, genres, numbers — clickable, sortable, for games and software and mods and everything else.

## 7. the future — Kage

possible rebrand: **"Kage"**, the site becoming **Kage-Pages** — where each thing (app, mod, character, sites, other) is just a **different page template** on one engine. big target, saved by the owner. even if the rebrand never lands, **the databases are built to integrate into it later**: slug-first, template-first, one data shape per thing. possible expansions along the same spine: **"good sites survive"**, **"good characters survive"**.

## 8. admin-like stuff (future)

main link + `/admin`: the page checks the **logged-in github account**. if it's the owner → owner mode: add extra pages, edit current pages, visually. everyone else: nothing special. exact identity mechanism (OAuth vs Pages-side check) gets decided when it gets built.

## 9. writing system (switchable tones)

writing is **not hardcoded** in pages. plan:

- a tone registry lives in `data/tone.json` — `{"active":"neutral","tones":{...}}`.
- page copy comes from data/templates so we can **switch tone site-wide** (e.g. `neutral` / `dry` / `hype` / `terminal`) without touching markup.
- tone rules: short sentences. no marketing fluff. no AI-slop phrasing. dry humor allowed. the reader is a player, not a customer.
- active tone until content passes say otherwise: **neutral**.

## 10. site architecture (current)

```
/
  index.html            clean ground: logo + brand mark + caption + footer. nothing else.
  assets/css/style.css  monochrome retro system
  data/*.json           the public-facing database (schema ggs.v1)
  brand-style-more.md   this file
  README.md             describes the site itself
  agents.md             the field manual for future agent sessions
  work/                 repo-related workspace (NOT source code, NOT served as site nav)
    original-lists/as-is/    the owner's uploads, byte-exact (casual.txt, non-casual.txt)
    original-lists/sorted/   same entries, sorted, one per line
    lists/games/             the games database (classes, series, name-check)
    lists/software/          apps, crack tools, mod tools (NOT mods)
    lists/mods/              mods, patches, fixes
  tools/                repo scripts (CI checkers, pushers)
  pages/                page per thing (game/software/mod/collection pages)
```

## 11. data schema — ggs.v1 (the backend shape)

the backend lives in `work/lists/`. the frontend serves a distilled copy in `data/`. same field names both places.

```jsonc
// one game entry (work/lists/games/games.json)
{
  "id": "g-<series-key>-<n>",          // stable id, never reused
  "title": "",                          // canonical, verified spelling
  "slug": "",                           // url name, unique across the whole site
  "list": "casual | non-casual",        // which owner list it came from
  "class": "normal | upgrade-of-normal",// upgrade-of-normal = remaster/remake entry that upgrades a normal one
  "upgrades": [],                       // ids of entries that upgrade this one
  "category": "",                       // section from the owner's lists
  "series": null | "series-key",        // series.json registry key
  "series_part": null,
  "developers": [], "publishers": [],
  "release": "YYYY-MM-DD | YYYY | null",
  "platforms": [],                      // windows | psp | ps2 | wii | ...
  "players": {"single": true, "coop": false, "multiplayer": false, "max_local": 1},
  "content_walls": [],                  // "sex" | "gore" only, hard walls
  "big_size": false,                    // true only per the +15GB law, verified
  "big_size_gb": null,                  // the verified number when true
  "buyable": null,                      // still sold somewhere → anyway link applies
  "download_kind": "legal | anyway | un-buyable-crack | redirect | null",
  "test_status": "not-tested",          // tested | not-tested (owner is the only tester)
  "target_os": "windows-10",
  "haswell_igpu_ok": null,              // true | false | unknown until tested
  "sources": [],                        // where facts came from
  "confidence": "owner-listed | verified",
  "notes": ""
}
```

**name-check law**: before anything enters, search `work/lists/games/name-check/games-added.txt` (one canonical name per line). exists → it's in. do not add again. the file is generated from games.json by `tools/lists_check.py` and also runs in CI.

**debunking rule**: nothing becomes a PAGE unverified. owner's speedran list → we debunk each row (real? playable? link alive?) → only then it becomes a page. list entries can carry `confidence: owner-listed` while waiting; pages cannot.

## 12. platform notes

- hosting: **GitHub Pages** from `main` root (`https://hakoradev.github.io/GoodGamesSurvive/`).
- repo is **code-only**: images/videos hot-linked from the web, videos via embeds. github soft limit 100GB — we'll never approach it since we serve only code.
- work style: **multi-pass commits**, verify live page after each pass, no comments in code (diagnostic markers are the exception).
- token workflow: raw REST or git over https; pusher script pattern in `scripts/ggs_push.py` (blobs→tree→commit→ref, handles root commit on empty repo).
- CI: `tools/lists_check.py` on every push — validates JSON, slug uniqueness, name-check duplicates, regenerates the name-check file, writes the counts.

---

*add new decisions under this line, newest on top.*
