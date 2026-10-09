# 05 — media: galleries, thumbnails, dead links

the owner's spec, verbatim in spirit: **10 images + 3 videos per page, no-
commentary gameplay and direct in-game shots, loaded from wherever the
internet can serve them. the gallery is URL linking only. if a URL dies, the
page says MEDIA NOT FOUND and nothing breaks.**

## the spec

- exactly 10 images + exactly 3 videos per game page (the build validates
  and warns otherwise).
- images: direct in-game shots — screenshots, store screenshots. no box art
  walls, no memes.
- videos: no-commentary gameplay. longplay/i-nocredits style uploads. the
  embed is youtube-nocookie; the thumb comes from i.ytimg.com.
- the gallery is **URL-only**: nothing self-hosted in the gallery, no asset
  pipeline. covers/thumbnails may be self-hosted (`assets/media/`) when no
  remote cover survives — that is the only exception.
- every gallery element carries its `onerror` law: a dead image removes its
  thumb and marks the slot g-dead ("MEDIA NOT FOUND"); a dead main image
  swaps to the media-dead panel; the viewer's JS re-tests every image before
  showing it (onerror → media-dead panel with the honest line "the internet
  ate this one - it was verified when the page was built").

## verification at dig time

1. images: curl each URL — expect 200 and an image content-type.
2. videos: confirm the video is gameplay without commentary (title +
   channel check), confirm the id resolves.
3. store the raw URLs in `work/data/pages/<slug>.json` gallery.images /
   gallery.videos[{id}].
4. the error case is part of the QA battery (08): build a temp fixture page
   with dead URLs, confirm MEDIA NOT FOUND renders, remove the fixture.

## thumbnails

- page files may carry `thumbnail` — used in index rows, latest digs,
  collection rows, similars.
- paths in page files are depth-2 relative (`../../assets/...`); the engine
  normalizes to root-relative for the index and re-anchors per depth
  (`thumb_at`). never store root-relative in a page file.
- a dead thumb collapses to the "no thumb" slot via onerror — the row
  survives, the layout survives.

## the resilience law

the site links out to the internet; the internet rots. the design answer is
not "host everything" (the owner chose URL-only) — it is graceful death:
MEDIA NOT FOUND states, dashed dead slots, honest lines. even things getting
killed should not kill us — we are the cool guys who save the day.
