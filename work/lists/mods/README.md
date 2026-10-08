# mods list — work/lists/mods/

scope (owner law): mods, modpacks, patches, fixes. one mod per entry.
a mod MUST carry its target game (the game page it wires into).
also: online fixes for cracked AAA games, VPN-LAN play setups, simple DLL
replacements, wrappers.

status: empty until the mods pass. same rules as the games database
(../games/README.md): name-check, sources, unknown = null.

`mods.json` schema (ggs.v1):

```jsonc
{
  "_meta": {"schema": "ggs.v1", "updated": null},
  "mods": [
    {
      "title": "", "slug": "",
      "kind": "mod | modpack | patch | fix | wrapper | online-fix | vpn-lan",
      "target_game_slug": "",           // the game page it belongs to
      "authors": [], "release": null,
      "platforms": ["windows"],
      "download": [],                   // {"label", "url", "kind"}
      "install_notes": "",
      "test_status": "not-tested",
      "confidence": "owner-listed",
      "sources": [], "notes": ""
    }
  ]
}
```
