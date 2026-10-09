# 09 — endless expansion

how the catalog grows from 692 to thousands without hallucinating, drifting
the design, or drowning the frontend. the owner's order: lists first, then
upgrades, pages dug one dig at a time.

## the pipeline

### 1. new rows from the owner's lists
- one owner line can hold many games ("Chicken Attack / Chicken's Revenge").
  split it into rows, one per real game, each traceable to the line.
- research pass per batch: name resolution first (the TailsMania → Talismania
  Deluxe lesson: the real title wins, the collision gets reported to the
  owner, never silently renamed).
- every row: title, slug, list, category (the owner's own section header),
  series guess, release, developers, publishers, platforms (windows, not
  PC), players (five-mode), buyable (null until verified), content_walls
  when the game needs a wall. confidence stays unverified until a source
  lands; verified needs the source listed.

### 2. the name-check gate
`tools/lists_check.py` regenerates `work/lists/games/name-check/games-added.txt`
(the full sorted name list) and flags duplicate titles. run it after every
batch. duplicate titles are owner decisions, not agent decisions.

### 3. the page decision
a row does not get a page by default. pages get dug when the owner points at
a game, a series, or a collection. the frontend tells the truth: "IN
CATALOGUE" until the dig. never mass-generate stub pages — a stub is slop.

### 4. when a series gets dug
dig the series in release order; the series registry (data/series.json)
gets the members; the pages cross-link automatically. holiday editions and
re-releases become **versions** (version_of + release_label + the mainline's
versions list) — never standalone catalog entries (the owner was explicit:
not every release is a catalog entry from day one).

### 5. when an upgrade lands
new mainline in the same chain → `upgrades` on the previous row (the direct
line). remaster covering old games + DLCs → `remaster` on every covered row
+ a hub row with `remaster_hub: true` (no page of its own unless the owner
asks). a reboot that replaces a standalone → `superseded_by`. the page
renders the lines automatically — pick the right field, not a new widget.

### 6. batch hygiene
- expand in themed batches (one series, one owner section) — context stays
  hot, sources stay comparable.
- worklog the batch: what was added, what was verified, what stayed unknown.
- push after the batch. the sandbox resets; the repo is the memory.

## the anti-hallucination checklist

- date not found? null. size not found? size unknown. players unclear?
  single only or null. sold-state unclear? null — the page says unknown.
- every "verified" row lists its sources. a source is a URL that was
  actually fetched this session, not a memory of a URL.
- store-first order: Steam / GOG / the studio's own site; then MobyGames,
  Wikipedia; then archive.org for the anyway route. cross-check two stores
  before writing a conflicting fact.
- the archive lists nothing it cannot defend. if a claim cannot survive the
  owner's "WTF" test, it does not ship.
