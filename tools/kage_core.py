import json, os, re, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_V = "10"
SEC_TPL = {"games": "game", "software": "software", "mods": "mod"}

def jload(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def jwrite(p, obj, compact=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        if compact:
            json.dump(obj, f, separators=(",", ":"), ensure_ascii=False)
        else:
            json.dump(obj, f, indent=1, ensure_ascii=False)

def esc(s):
    return (str(s if s is not None else "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;"))

def keyify(name):
    k = re.sub(r"[^a-z0-9]+", "-", str(name).casefold()).strip("-")
    return k or "unknown"

def rel(from_dir, to_rel=None, depth=None):
    if to_rel is None:
        to_rel = from_dir
        from_dir = ""
    if depth is not None:
        return ("../" * depth) + to_rel
    d = from_dir.strip("/").count("/")
    return ("../" * d) + to_rel if d else to_rel

def date_str(r):
    if not r:
        return None
    r = str(r)
    if re.match(r"^\d{4}-\d{2}-\d{2}$", r):
        months = ["", "January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        y, m, d = r.split("-")
        return "%s %s %s" % (int(d), months[int(m)], y)
    if re.match(r"^\d{4}-\d{2}$", r):
        months = ["", "January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        y, m = r.split("-")
        return "%s %s" % (months[int(m)], y)
    return r

def year_of(r):
    if not r:
        return None
    m = re.match(r"^(\d{4})", str(r))
    return m.group(1) if m else None

def size_label(row):
    mb = row.get("size_est_mb")
    if not mb:
        return None
    if mb >= 1024:
        v = mb / 1024.0
        return ("%.1f GB" % v).rstrip("0").rstrip(".").replace(".0", ".0")
    return "%d MB" % mb

def size_display(row):
    lab = size_label(row)
    src = row.get("size_source") or ""
    if not lab:
        return "size unknown"
    kind = "install" if src.startswith(("store", "repack")) else "estimate"
    return "%s (%s)" % (lab, kind)

class Engine:
    def __init__(self):
        self.games_db = jload(os.path.join(ROOT, "work", "lists", "games", "games.json"))
        self.series = jload(os.path.join(ROOT, "data", "series.json"))
        self.tone = jload(os.path.join(ROOT, "data", "tone.json"))
        self.pages = self._load_dir(os.path.join(ROOT, "work", "data", "pages"))
        self.collections_src = jload(os.path.join(ROOT, "work", "data", "collections.json"))
        self.redirects = jload(os.path.join(ROOT, "work", "data", "redirects.json"))
        self.software_rows = self._db_rows(os.path.join(ROOT, "work", "lists", "software", "tools.json"))
        self.mods_rows = self._db_rows(os.path.join(ROOT, "work", "lists", "mods", "mods.json"))
        self.page_by_slug = {p["slug"]: p for p in self.pages}
        self.game_by_slug = {g["slug"]: g for g in self.games_db["games"]}
        self.collections = self.collections_src.get("collections", [])
        self.series_map = {s["key"]: s for s in self.series.get("series", [])}
        self.build_vocab()
        self.build_collections()
        self.build_index()
        self.build_similars()

    def _load_dir(self, d):
        out = []
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".json"):
                    out.append(jload(os.path.join(d, f)))
        return out

    def _db_rows(self, p):
        if not os.path.exists(p):
            return []
        d = jload(p)
        return d.get("software", []) or d.get("mods", []) or []

    def build_vocab(self):
        self.devs, self.pubs, self.genres, self.subgenres, self.tags = {}, {}, {}, {}, {}
        self.plats, self.eras = {}, {}
        for sec_rows in (self.games_db["games"], self.software_rows, self.mods_rows):
            for g in sec_rows:
                for d_ in (g.get("developers") or []):
                    self.devs.setdefault(keyify(d_), d_)
                for p_ in (g.get("publishers") or []):
                    self.pubs.setdefault(keyify(p_), p_)
                for x in (g.get("genres") or []):
                    self.genres.setdefault(keyify(x), x)
                for x in (g.get("subgenres") or []):
                    self.subgenres.setdefault(keyify(x), x)
                for x in (g.get("tags") or []):
                    self.tags.setdefault(keyify(x), x)
                for x in (g.get("platforms") or []):
                    self.plats.setdefault(keyify(x), x)
                y = year_of(g.get("release"))
                if y:
                    self.eras.setdefault("%ss" % (y[:3] + "0"), "%ss" % (y[:3] + "0"))
                else:
                    self.eras.setdefault("unknown", "unknown")

    def collection_of(self, slug, kind="collection"):
        hits = []
        for c in self.collections:
            if kind == "multi":
                continue
            if slug in (c.get("items") or []):
                hits.append(c)
        return hits

    def build_collections(self):
        for c in self.collections:
            c["items"] = c.get("items") or []
            c["catalogued"] = c.get("catalogued") or []
            c["n_pages"] = len([s for s in c["items"] if s in self.page_by_slug])
        self.multis = self.collections_src.get("multi_collections", []) or []

    def index_row(self, g, sec):
        y = year_of(g.get("release"))
        page = None
        th = None
        if sec == "games" and g["slug"] in self.page_by_slug:
            page = "game/%s.html" % g["slug"]
            th = self.page_by_slug[g["slug"]].get("thumbnail")
        elif sec == "software" and g["slug"] in self.page_by_slug:
            page = "software/%s.html" % g["slug"]
        elif sec == "mods" and g["slug"] in self.page_by_slug:
            page = "mod/%s.html" % g["slug"]
        pl = g.get("players") or {}
        gn_disp = [self.genres.get(keyify(x), x) for x in (g.get("genres") or [])]
        dn_disp = [self.devs.get(keyify(x), x) for x in (g.get("developers") or [])]
        pn_disp = [self.pubs.get(keyify(x), x) for x in (g.get("publishers") or [])]
        cap = ""
        if sec == "games" and g["slug"] in self.page_by_slug:
            cap = (self.page_by_slug[g["slug"]].get("caption") or "")[:110]
        row = {
            "t": g.get("title") or "", "s": g["slug"], "sec": sec,
            "y": y, "date": g.get("release") or None,
            "g": [keyify(x) for x in (g.get("genres") or [])],
            "gn": gn_disp,
            "gs": [keyify(x) for x in (g.get("subgenres") or [])],
            "tg": [keyify(x) for x in (g.get("tags") or [])],
            "pl": [keyify(x) for x in (g.get("platforms") or [])],
            "p1": bool(pl.get("single")), "pc": bool(pl.get("coop")), "pm": bool(pl.get("multiplayer")),
            "w": g.get("content_walls") or [],
            "size": g.get("size_est_mb"), "szs": g.get("size_source"),
            "req": g.get("req_tier"), "ser": g.get("series"), "part": g.get("series_part"),
            "list": g.get("list"), "conf": g.get("confidence"),
            "tested": g.get("test_status") == "tested", "buy": g.get("buyable"),
            "big": bool(g.get("big_size")), "cat": g.get("category"),
            "dev": [keyify(x) for x in (g.get("developers") or [])],
            "dn": dn_disp,
            "pub": [keyify(x) for x in (g.get("publishers") or [])],
            "pn": pn_disp,
            "era": ("%ss" % (y[:3] + "0")) if y else "unknown",
            "page": page, "th": th, "cap": cap,
        }
        return row

    def build_index(self):
        self.rows = []
        for g in self.games_db["games"]:
            self.rows.append(self.index_row(g, "games"))
        for g in self.software_rows:
            self.rows.append(self.index_row(g, "software"))
        for g in self.mods_rows:
            self.rows.append(self.index_row(g, "mods"))
        for c in self.collections:
            self.rows.append({
                "t": c["title"], "s": c["slug"], "sec": "collections",
                "kind": c.get("kind", "collection"), "y": None, "date": None,
                "g": [], "gs": [], "tg": [], "pl": [], "w": [], "size": None,
                "req": None, "ser": None, "list": None, "conf": "verified",
                "tested": False, "buy": None, "big": False,
                "n": c["n_pages"], "page": "collection/%s.html" % c["slug"],
                "th": None, "cap": c.get("caption") or "",
            })
        for m in self.multis:
            self.rows.append({
                "t": m["title"], "s": m["slug"], "sec": "collections",
                "kind": "multi", "y": None, "date": None,
                "g": [], "gs": [], "tg": [], "pl": [], "w": [], "size": None,
                "req": None, "ser": None, "list": None, "conf": "verified",
                "tested": False, "buy": None, "big": False,
                "n": len(m.get("collections") or []), "page": "meta/%s.html" % m["slug"],
                "th": None, "cap": m.get("caption") or "",
            })

    def sec_counts(self):
        n = {"games": 0, "software": 0, "mods": 0, "collections": 0}
        for r in self.rows:
            n[r["sec"]] += 1
        return n

    def build_similars(self):
        self.similar = {}
        page_rows = [r for r in self.rows if r["sec"] == "games" and r["page"]]
        col_of = {}
        for c in self.collections:
            for s in c["items"]:
                col_of.setdefault(s, set()).add(c["slug"])
        for a in page_rows:
            pool = []
            for b in page_rows:
                if b["s"] == a["s"]:
                    continue
                if a["ser"] and b["ser"] == a["ser"]:
                    continue
                if col_of.get(a["s"], set()) & col_of.get(b["s"], set()):
                    continue
                why = []
                score = 0
                shared_g = sorted(set(a["g"]) & set(b["g"]))
                shared_s = sorted(set(a["gs"]) & set(b["gs"]))
                shared_t = sorted(set(a["tg"]) & set(b["tg"]))
                if shared_g:
                    score += 3 * len(shared_g)
                    why += [self.genres.get(k, k) for k in shared_g]
                if shared_s:
                    score += 2 * len(shared_s)
                    why += [self.subgenres.get(k, k) for k in shared_s]
                if shared_t:
                    score += 2 * len(shared_t)
                    why += [self.tags.get(k, k) for k in shared_t]
                if a["era"] == b["era"] and a["era"] != "unknown":
                    score += 1
                    why.append(a["era"])
                if set(a["dev"]) & set(b["dev"]):
                    score += 1
                    why.append(self.devs.get((set(a["dev"]) & set(b["dev"])).__iter__().__next__()))
                if a["pc"] and b["pc"]:
                    score += 1
                    why.append("co-op")
                if score > 0:
                    pool.append({"slug": b["s"], "title": b["t"], "th": b["th"], "y": b["y"],
                                 "score": score, "why": ", ".join(why[:4])})
            pool.sort(key=lambda x: (-x["score"], x["title"].casefold()))
            catalogued = []
            if len(pool) < 4:
                for b in self.rows:
                    if b["sec"] != "games" or b["page"] or b["s"] == a["s"]:
                        continue
                    if a["ser"] and b["ser"] == a["ser"]:
                        continue
                    shared = set(a["g"]) & set(b["g"]) or set(a["tg"]) & set(b["tg"])
                    if shared:
                        catalogued.append(b["t"])
                    if len(catalogued) >= 6:
                        break
            self.similar[a["s"]] = {"pages": pool[:10], "catalogued": catalogued}

    def versions_of(self, slug):
        p = self.page_by_slug.get(slug)
        if not p or not p.get("group"):
            return None
        sibs = []
        for s2, p2 in self.page_by_slug.items():
            if p2.get("group") == p["group"]:
                sibs.append({"slug": s2, "label": p2.get("release_label") or "standard",
                             "title": (self.game_by_slug.get(s2) or {}).get("title", s2)})
        sibs.sort(key=lambda x: (x["slug"] != slug, x["slug"]))
        return {"group": p["group"], "label": p["group_label"], "current": slug, "siblings": sibs}

    def upgrades_of(self, slug):
        out = {"direct": None, "spiritual": None, "superseded_by": None, "upgrades": []}
        g = self.game_by_slug.get(slug) or {}
        for u in (g.get("upgrades") or []):
            ug = self.game_by_slug.get(u)
            if ug:
                out["upgrades"].append({"slug": u, "title": ug["title"], "page": u in self.page_by_slug})
        for other, og in self.game_by_slug.items():
            if slug in (og.get("upgrades") or []):
                if other in self.page_by_slug:
                    out["direct"] = {"slug": other, "title": og["title"]}
        sb = g.get("superseded_by")
        if sb and sb in self.game_by_slug:
            out["superseded_by"] = {"slug": sb, "title": self.game_by_slug[sb]["title"]}
        return out

    def series_line(self, slug):
        g = self.game_by_slug.get(slug) or {}
        ser = g.get("series")
        if not ser or ser not in self.series_map:
            return None
        s = self.series_map[ser]
        members = []
        for m in s.get("members", []):
            members.append({
                "slug": m["slug"], "title": m["title"], "part": m.get("part"),
                "page": m["slug"] in self.page_by_slug,
                "now": m["slug"] == slug,
                "y": year_of((self.game_by_slug.get(m["slug"]) or {}).get("release")),
            })
        return {"key": ser, "title": s.get("title", ser), "members": members}

    def facts_of(self, slug):
        g = self.game_by_slug.get(slug) or {}
        p = self.page_by_slug.get(slug) or {}
        pl = g.get("players") or {}
        players_txt = []
        if pl.get("single"): players_txt.append("single-player")
        if pl.get("coop"): players_txt.append("local co-op")
        if pl.get("multiplayer"): players_txt.append("multiplayer")
        if not players_txt: players_txt.append("players unknown")
        plat_txt = ", ".join((g.get("platforms") or ["unknown"]))
        extra_plats = p.get("notes_extra") or ""
        return {
            "released": date_str(g.get("release")) or "unknown",
            "year": year_of(g.get("release")),
            "devs": g.get("developers") or [],
            "pubs": g.get("publishers") or [],
            "platforms": g.get("platforms") or [],
            "players": ", ".join(players_txt),
            "series": g.get("series"),
            "part": g.get("series_part"),
            "walls": g.get("content_walls") or [],
            "size": size_display(g),
            "buyable": g.get("buyable"),
            "tested": g.get("test_status") == "tested",
            "list": g.get("list"),
            "class": g.get("class"),
            "conf": g.get("confidence"),
            "genres": p.get("genres") or g.get("genres") or [],
            "subgenres": p.get("subgenres") or g.get("subgenres") or [],
            "tags": g.get("tags") or [],
            "req": p.get("req") or {},
            "characters": p.get("characters") or [],
            "extra_plats": extra_plats,
        }
