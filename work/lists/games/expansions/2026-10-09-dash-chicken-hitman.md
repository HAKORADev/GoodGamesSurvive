# expansion log — 2026-10-09 — Dash universe, Chicken Invaders, Hitman

owner brief: expand the speedran lists without hallucination. the three
named universes got expanded this round. every fact below was checked
against sources during research (research stash: scripts/research*/ on the
agent side; cited inline). nothing was added to fill holes.

## 1. The Dash Universe -> every Dash game from PlayFirst + the Glu era

the owner's line ("The Dash Universe (Diner Dash, Hotel Dash, Doggie Dash,
SpongeBob Diner Dash 1 & 2, Delicious 1 & 2, Garden Dash, DinerTown Tycoon)")
was replaced by the full verified Dash family, 29 rows in games.json:

- Diner Dash main line: Diner Dash (2003-12-03, gameLab/PlayFirst),
  Diner Dash 2: Restaurant Rescue (2006), Flo on the Go (2006),
  Hometown Hero (2007), Flo Through Time (2008, Hometown Hero episode pack),
  Diner Dash 5: Boom! (2010)
- Wedding Dash: 2007 / 2: Rings Around the World 2008 / Ready Aim Love! 2009 /
  4-Ever 2010
- Cooking Dash: 2008 / DinerTown Studios 2009-09-03 / Thrills & Spills 2010
- Hotel Dash: Suite Success (2009, dev Kef Sensei) / Lost Luxuries (2011)
- Avenue Flo: 2009-10-13 / Special Delivery 2010-11-13
- DinerTown spin-offs: Doggie Dash 2008-01-31 (dev Viqua Games), Dairy Dash,
  Fashion Dash, Parking Dash, Fitness Dash (all 2008), Diaper Dash 2009,
  Garden Dash 2011-04-15
- DinerTown Tycoon 2009-06-16
- licensed: SpongeBob Diner Dash 2006, SpongeBob Diner Dash 2: Two Times the
  Trouble 2007 (dev Snap2play)
- Glu era (mobile, marked upgrade-of-normal): Diner Dash (2014, F2P),
  Diner DASH Adventures (2019)

sources: Wikipedia (Diner Dash), PCGamingWiki series pages, MobyGames
release records, SteamDB store pages, Old Games Download archive pages.

owner-line note: **Delicious 1 & 2 are NOT PlayFirst** (GameHouse series).
they were inside the owner's Dash line but they stay owner-listed as their
own thing, not part of this expansion.

## 2. Chicken Invaders collection -> the full games

the owner's line ("Chicken Invaders Series (1-5 & Chicken Invaders
Universe)") was replaced by the six main entries, 1999-2018, all by
InterAction studios (Konstantinos Prouskas, Greece):

1. Chicken Invaders - 1999-07-24 (DX Edition; remastered 2023; Steam 2025)
2. Chicken Invaders 2: The Next Wave - 2002-12-22 (+ Christmas Edition 2003)
3. Chicken Invaders 3: Revenge of the Yolk - 2007-01-20 regular
   (Christmas Edition preceded it, 2006-11-11; Easter Edition 2010)
4. Chicken Invaders 4: Ultimate Omelette - 2010-12-06
   (Christmas/Easter/Thanksgiving editions 2011-2013)
5. Chicken Invaders 5: Cluck of the Dark Side - 2014-11-21
   (Steam 2015-03-13; Halloween/Christmas editions 2015/2016)
6. Chicken Invaders Universe - 2018-12-14 early access (MMO spin-off)

source: Wikipedia "Chicken Invaders" (full article in the research stash).

## 3. Hitman series -> the PC classics

the owner's line ("Hitman Series (Hitman 2, Contracts, Blood Money)" +
separate "Hitman: Absolution") was expanded to the classic five, all
IO Interactive:

1. Hitman: Codename 47 - 2000-11-19
2. Hitman 2: Silent Assassin - 2002-10-01
3. Hitman 3: Contracts - 2004-04-20
4. Hitman: Blood Money - 2006-05-26 EU / 2006-05-30 NA
5. Hitman: Absolution - 2012 (Professional Edition = big-size, ~24GB)

source: Wikipedia + IO Interactive timeline pages (research stash).
the modern World of Assassination trilogy (HITMAN 2016 / HITMAN 2 2018 /
HITMAN III 2021) is registered in series.json as the series upgrade path,
not as archive targets: too heavy for haswell HDxxxx iGPUs.

## 4. PlayFirst non-Dash (owner brief: "any non-Dash game from them")

added, verified-title: Dream Chronicles (2007), Dream Chronicles: The
Chosen Child (2009, dev KatGames), Dream Chronicles: The Book of Air
(2010-08-10), Emerald City Confidential (2009-03-23), Wandering Willows
(2009-03-24), Oasis (year unverified = null), Egg vs. Chicken (year
unverified = null), Chessmaster Challenge (2005).

## 5. tag fixes applied this round (owner law)

- the `sex` hard wall replaced every `+18` mark (8 rows). the `gore` wall
  applied to Hatred and Manhunt 2 (2 rows). GTA being +18 is not a wall.
- big-size re-audit against the +15GB-installed (full tier, all DLC) law.
  verified adds: Grand Theft Auto IV Complete (~31GB), L.A. Noire Complete
  (~27GB), Batman: Arkham City (~17GB), Assassin's Creed III (~17GB),
  Dragon's Dogma: Dark Arisen (~20GB), Ni no Kuni Remastered (~45GB),
  Bayonetta (~20GB), Mortal Kombat X (~36GB).
  confirmed NOT big: Fallout 3 GOTY (~9GB), Skyrim Legendary (~8.5-12GB),
  Saints Row IV (~10GB), Mafia II classic (~8GB), Tales of Zestiria (~12GB),
  Red Dead Redemption PC port (~12GB).
- the owner's big-size tag that sat on the "Assassin's Creed Series" line
  got rebound to a standalone Assassin's Creed IV: Black Flag row.
- typo fixed in passing: "Chocolatier 2: Secret Agent" is
  "Chocolatier 2: Secret Ingredients" (verified against PlayFirst lists).

## flagged for the owner (not silently changed)

- "Talismania" (casual, marble section) vs "TailsMania Deluxe" (casual,
  racing section) look like the same PopCap game. both rows kept;
  name-check will surface the collision. owner decides.
- "Sonic Riders (2006/2008)" kept as one row with both years in the notes.
