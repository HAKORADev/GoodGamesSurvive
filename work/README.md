# work/ — the workspace (not the site)

this tree is **repo-related workspace**. it is not source code and not served
as part of the site UI. the site serves `data/`; `work/` is where the raw
lists, the sorted copies, and the databases live.

```
work/
  original-lists/
    as-is/        the owner's uploads, byte-exact, never edited
    sorted/       GENERATED view of lists/games/games.json by tools/sorted_lists.py
                  (one line per row: name platform year #tags, xN = declared
                  entries; casual-sorted.txt, non-casual-sorted.txt and
                  list.txt = both in one file with an internal split)
  lists/
    games/        the games database (games.json + series.json + name-check/)
    software/     apps, crack tools, mod tools (NOT mods)
    mods/         mods, patches, fixes (one mod per entry, target game required)
  ...
```

## laws

1. `original-lists/as-is/` is sacred. never edit, never reformat. the as-is
   files are the owner's word.
2. `original-lists/sorted/` is a generated view of `lists/games/games.json`
   (owner law 2026-10-10, replaces the old sort-of-as-is flow). regenerate with
   `python3 tools/sorted_lists.py` after any database change; never hand-edit
   it. format per line: `name platform year #tags`, platform shows PC for
   windows rows, year is ???? when unknown, tags are #big-size #sex #gore, and
   xN marks only titles that mechanically DECLARE multiple games.
3. entries flow: as-is list -> debunk/verify -> `lists/*/` database -> `data/`
   public copy -> page. an entry can sit in the database with
   `confidence: owner-listed` forever if it is not yet verified. it can NOT
   become a page until its row is verified.
4. every verified fact carries its source in the row's `sources` array.
   no source, no verified status. no invented facts, no fake names, no
   made-up dates to fill holes. unknown = null.
5. before adding any new game, check `lists/games/name-check/games-added.txt`.
   if the name is there, the game is already in. do not add twice.
6. platform law pointer (brand-style-more.md section 12.1): one platform per
   game, native windows wins, supported consoles = ps1/ps2/psp/gc/wii; ps3,
   ps4, xbox, wii u, switch, android never appear in the database or on the
   site (the hitman HD remasters went to attic/ over this).
