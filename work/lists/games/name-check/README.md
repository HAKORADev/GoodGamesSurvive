# name-check — "is it already in the site?"

`games-added.txt` = one canonical game name per line, case-preserving,
sorted case-insensitively. generated from `games.json` by
`tools/lists_check.py`; CI regenerates it on every push.

## how to check before adding anything

1. exact check (scripts do this):

```python
names = open("work/lists/games/name-check/games-added.txt", encoding="utf-8").read().splitlines()
if title.strip() in names:
    ...already in...
```

2. eyeball check (humans + agents): search the file case-insensitively
   before typing. watch for renames ("Watch Dogs 1" is filed as
   "Watch Dogs"), year suffixes (stripped), and platform suffixes
   (stripped; the platform lives in the row).

the file is the single source of truth for dedup. if a name is in there,
the game is in the database. adding it again is a mistake.

regenerate after editing games.json:

```bash
python3 tools/lists_check.py
```
