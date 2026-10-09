# 08 — the QA battery

the owner's deal: "you can spot 90 and the last 10 be hidden and i mess
around and detect them, team work." 90 is the minimum, not the target.

## before every push

### 1. the build gate
```
python3 tools/lists_check.py   # json parses, slugs unique, required fields
python3 tools/build.py         # must end: BUILD: CLEAN
```
a warning is a blocker. every WARN (gallery count, missing caption/about)
gets fixed or consciously justified in the worklog.

### 2. the link gate
the build validates every internal href/src and every relative target. any
"FAIL broken internal ref" blocks the push.

### 3. the browser battery (local http.server, then live after push)
- **overflow at 390px**: every key page — main, games shelf, a game page, an
  edition page, a collection page, search. horizontal scroll = fail. the
  series line, facts table, chips and download rows are the usual suspects
  (word-break / wrap rules live in the @media block of style.css).
- **console**: zero errors on every page. a red console is a broken promise.
- **click-through**: nav → shelf → facet toggle → row → game page → version
  dropdown → edition page → back. the dropdown must land on the right page
  (check a xmas edition ends on ITS episode, never a neighbor's).
- **facets**: toggle genre, players, era, status — counts react, rows
  filter, url params ride, clear-all resets.
- **search**: type a partial title, a developer, a character — tokens AND
  together; zero results shows the empty state with its reset button.
- **random**: top-bar random lands on a real page; shelf random lands inside
  the shelf; repeat 5x each.
- **main page**: latest digs per section (≤10, newest first), jump-to links,
  the stats line matches reality (catalog rows / pages dug / pages live /
  collections).

### 4. the media error case (fixture test)
temporarily point a fixture page's gallery at dead URLs → build → open →
the MEDIA NOT FOUND panel renders, dead thumbs collapse, no console errors
→ remove fixture → build again. the error path is a feature; test it like
one.

### 5. the honesty gate
- every page: gallery → about → facts order intact.
- characters: faces only (law 9). series cell: series name only.
- official/anyway: official exists → both blocks; dead game → anyway only,
  with the official-status strip explaining the death.
- no hardcoded numbers anywhere (grep the generated html for suspicious
  literals — counts come from the engine).
- dead shelves do not render as links; empty states read honest.

### 6. the live gate
after push: fetch the live URLs (index + one game page + the search index
json) and byte-compare the markers you changed. the site is not "done" when
the push returns ok — it is done when the live site shows the work.

## when a round starts

re-verify disk state (clone if the sandbox reset), read the worklog, run the
build gate before touching anything, and live-verify the previous round's
claims before building on them.
