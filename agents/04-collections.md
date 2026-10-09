# 04 — collections and meta-collections

collections are shelves inside a section. meta-collections are shelves of
shelves. the owner wants them structured, accurate, and never decorative.

## the design

- a **collection** holds pages of exactly one section (`"section": "games"`).
  its `items` are slugs of real pages (mainlines only — versions never ride
  a collection; the collection mentions them in notes if needed).
- `catalogued` lists rows belonging to the collection that have no page yet —
  they render as honest "IN CATALOGUE" rows under "ALSO IN THE CATALOGUE".
- a **meta-collection** holds collection slugs (`multi_collections`). its
  page lists the member collections; it appears on a shelf's collections
  block only when at least one member lives on that shelf.

## wiring

```json
{
  "slug": "chicken-invaders-collection",
  "title": "The Chicken Invaders Collection",
  "section": "games",
  "caption": "one breath long",
  "about": ["what the collection is", "the quirks it keeps honest"],
  "items": ["mainline page slugs"],
  "catalogued": ["row slugs without pages"],
  "notes": ["facts that protect accuracy"]
}
```

- the engine computes `n_pages` from `items` that actually have pages —
  never hardcode counts.
- collections appear in four places, all automatic: the shelf's
  "COLLECTIONS ON THIS SHELF" block, the main page collections strip, the
  global COLLECTIONS page, and each member page's "COLLECTIONS" line.

## the accuracy rules

1. a collection caption states scope in one breath: "the classic line: five
   wars, 1999 to 2014, every holiday release riding as a version."
2. `about` carries the collection's real story — what's inside, what's
   deliberately out, the quirk worth keeping honest (the CI Christmas that
   shipped before its own episode).
3. notes carry the boundary law: what is attic'd and why, what waits its dig.
4. no collection invents membership: every slug must exist as a page or a
   catalog row, or the build validates it out.
5. collections are structural, not vibes: a Hitman collection holds the
   Hitman the owner listed — not "every hitman game in the world" (the drift
   the owner already called out once).

## testing collections

dummy test pattern (see 08): add a fixture collection + a fixture
meta-collection with a test marker, build, verify shelf block / main strip /
collections page / meta page / search row all render, then REMOVE the
fixtures and build again. the engine must prove the dynamic path before the
real data rides it.
