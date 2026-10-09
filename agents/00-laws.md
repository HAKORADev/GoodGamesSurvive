# 00 — the laws

everything else is technique. these are the laws. they exist because the
owner wrote them, or because breaking them already cost a round once.

## the owner's laws

1. **all replies in English.** no exceptions in chat, none in the site.
2. **the sandbox resets; the repo is the memory.** re-verify disk state every
   round. clone fresh when unsure. push mid-work so the hard parts survive.
3. **live-verify before every report.** never claim the site shows X without
   fetching the live URL and seeing X.
4. **no fake facts.** unknown = null. a null field is honest; a made-up
   number is a landmine. sizes, dates, players, sold-state: verify on the
   internet or mark unknown with the reason.
5. **no AI-slop.** no "welcome to", no "look no further", no emoji in copy,
   no placeholders, no self-describing design text ("this section shows...").
6. **no comments in code.** diagnostic marker comments are the exception.
7. **scope law: the catalog is the owner's lists first, then endorsed
   upgrades.** never add games the owner didn't list. versions/editions are
   not catalog entries. out-of-scope rows go to `work/lists/games/attic/`,
   never deleted.
8. **links law: official first where an official path exists, the archive
   route right next to it. a dead game gets only the anyway route.** every
   link must actually help: a store page where the game sells, an archive
   item that holds the game. search-result pages are filler — filler is slop.
9. **characters law: only the face(s) of the game.** diner dash is Flo, not
   her customers. hitman is 47, not his targets. the protagonist plus named
   icons that ARE the game's identity — nothing else.
10. **nothing called "tag".** the system is genre / sub-genre / category /
    content, plus players / platform / era / status. see 03-tags-infra.md.

## the design laws

11. **monochrome retro system.** ground #070707, ink #e8e8e8. the palette,
    the fonts (Silkscreen / Alfa Slab One / IBM Plex Mono / VT323), the CRT
    atmosphere — never drift. brand-style-more.md is the shared memory.
12. **every page shows its caption under the title** — on the page, in the
    index rows, in the latest-digs blocks. captions are one breath long.
13. **about sits directly under the gallery**, before facts, requirements,
    everything. gallery first (see the thing), then what it is (about), then
    the details (facts).
14. **the site is honest everywhere.** dead shelves don't fake life; empty
    states say so; "IN CATALOGUE" means no page yet; "NOT TESTED" means the
    owner hasn't played it. numbers are computed, never hardcoded.
15. **no interactivity the owner never asked for.** no easter eggs, no
    gimmicks. the coolness is the catalog working like a store.
16. **testing is the owner's time you are saving.** hand over work where 90
    of the 100 bugs are already dead. see 08-testing.md.

## the workflow laws

17. **worklog**: read `/home/z/my-project/worklog.md` first, append after
    every work stage. the repo holds project memory; the worklog holds the
    session story.
18. **build before commit, always.** `python3 tools/build.py` must end with
    `BUILD: CLEAN` in the same breath as the commit. a committed stale build
    is how "the versions area vanished" happened once.
19. **push mid-work.** one infra commit pushed before the content polish
    starts, so a sandbox wipe never eats the structural work.
20. **git only, no `gh` CLI.** raw REST with the token, plain
    `git push origin main` (token baked into the remote URL).
