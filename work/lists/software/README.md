# software list — work/lists/software/

scope (owner law): apps, crack tools, mod tools. NOT mods (mods live in
`../mods/`). every must-have tool gets a page and a download link when it
ships.

status: empty until the software pass. when adding rows, same rules as the
games database (see ../games/README.md): name-check before adding, sources
on every verified fact, unknown = null.

`tools.json` schema (ggs.v1, same field names where they overlap):

```jsonc
{
  "_meta": {"schema": "ggs.v1", "updated": null},
  "tools": [
    {
      "title": "", "slug": "", "kind": "app | crack-tool | mod-tool",
      "developers": [], "release": null,
      "platforms": ["windows"],
      "license": null,                    // freeware | open-source | abandonware | other
      "download": [],                     // {"label", "url", "kind": "official|mirror|redirect"}
      "test_status": "not-tested",        // tested = owner used it end to end
      "confidence": "owner-listed",
      "sources": [], "notes": ""
    }
  ]
}
```
