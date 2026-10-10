# 10 — sorted lists are a generated view of the database (2026-10-10)

## the systems this round

1. **sorted-lists generator** (`tools/sorted_lists.py`): the
   `work/original-lists/sorted/` files are no longer a mechanical sort of the
   as-is files. they are generated straight from `work/lists/games/games.json`
   and regenerated on every database change. one line per ROW (not per owner
   line): `- Name platform year #tags`. platform = PC for windows rows (the
   owner's "platform as PC for windows"), console tags for console rows (empty
   platform inherits the section's console). year = release year, ???? when
   unknown. tags = #big-size then #sex/#gore walls. `xN` marks only titles
   that mechanically DECLARE multiple games ("Cake Mania 1, 2 & 3" -> x3,
   "1-4" ranges, "Series (...)" lists, `BUNDLE_KNOWN` owner notes like
   Ezio Collection = 3). joined titles without a declared count stay unmarked
   ("San Andreas & Vice City") — a silent maybe beats a wrong number.
   outputs: casual-sorted.txt, non-casual-sorted.txt, list.txt (both lists in
   one file with an internal split, the owner's "next to casual.txt" ask).

2. **legacy batch**: +16 owner-listed non-casual rows (dark shadows,
   hellforces, inhabited island: prisoner of power, scorpion disfigured,
   cernaja metka, morphx, beowulf: the game, d.i.r.t.: origin of the species,
   bad day l.a., hamster heroes, i-ninja, metro 2033, brothers in arms: hell's
   highway, spartan: total warrior (ps2 per owner), the warriors: street
   brawl, infernal). no-search round: rows are owner-listed, unknown = null,
   only well-known dev/pub facts filled (4A/THQ, Gearbox/Ubisoft, CA/SEGA,
   Metropolis). evil twin: cyprien's chronicles already existed — updated to
   release 2001 + windows per the owner's "evil twin 2001" disambiguation and
   the one-platform law. ninjabread man was already in (casual) — left alone.
   3 rows with empty platforms got the console their own title/section
   declares (shinobido tales of the ninja -> psp, ssx on tour -> ps2,
   b-boy -> ps2).

3. **platform law enforcement (section 12.1)**: hitman HD trilogy +
   hitman HD enhanced collection (ps3/ps4/xbox-only remasters) removed from
   games.json -> attic (count 10), page sources deleted, upgrade_notes/
   upgrade_kinds/upgrades refs cleaned on the four remaining hitman rows,
   hitman-collection rebuilt around the four windows builds (caption/about/
   items), series registry (work + data copies) hitman members back to the
   windows line + reference entries. the platform filter map is built from
   row data, so ps3/ps4/xbox-one vanish from the site filters on rebuild.

## run order after any database change

```
python3 tools/sorted_lists.py     # regenerate the sorted views
python3 tools/lists_check.py      # name-check + counts
python3 tools/build.py            # rebuild the site
```
