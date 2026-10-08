# work/ — the workspace (not the site)

this tree is **repo-related workspace**. it is not source code and not served
as part of the site UI. the site serves `data/`; `work/` is where the raw
lists, the sorted copies, and the databases live.

```
work/
  original-lists/
    as-is/        the owner's uploads, byte-exact, never edited
    sorted/       same entries mechanically sorted (one line per owner entry,
                  alphabetical inside each section, grouping untouched)
  lists/
    games/        the games database (games.json + series.json + name-check/)
    software/     apps, crack tools, mod tools (NOT mods)
    mods/         mods, patches, fixes (one mod per entry, target game required)
  ...
```

## laws

1. `original-lists/as-is/` is sacred. never edit, never reformat. the sorted
   copies are generated from it, but the as-is files are the owner's word.
2. entries flow: as-is list -> debunk/verify -> `lists/*/` database -> `data/`
   public copy -> page. an entry can sit in the database with
   `confidence: owner-listed` forever if it is not yet verified. it can NOT
   become a page until its row is verified.
3. every verified fact carries its source in the row's `sources` array.
   no source, no verified status. no invented facts, no fake names, no
   made-up dates to fill holes. unknown = null.
4. before adding any new game, check `lists/games/name-check/games-added.txt`.
   if the name is there, the game is already in. do not add twice.
