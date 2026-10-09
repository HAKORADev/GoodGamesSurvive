import json, os, re, hashlib, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_V = "12-" + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
SEC_TPL = {"games": "game", "software": "software", "mods": "mod"}
SERIES_TITLES = {
    "chicken-invaders": "Chicken Invaders",
    "diner-dash": "Diner Dash",
    "hitman": "Hitman",
}

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

def clean_cat(c):
    if not c:
        return ""
    return re.sub(r"[^A-Za-z0-9 ,&/'()+-]", "", str(c)).strip(" ,")

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
    months = ["", "January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    if re.match(r"^\d{4}-\d{2}-\d{2}$", r):
        y, m, d = r.split("-")
        return "%s %s %s" % (int(d), months[int(m)], y)
    if re.match(r"^\d{4}-\d{2}$", r):
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
        return ("%.1f GB" % v).rstrip("0").rstrip(".")
    return "%d MB" % mb

def size_display(row):
    lab = size_label(row)
    src = row.get("size_source") or ""
    if not lab:
        return "size unknown"
    if src.startswith("store"):
        kind = "install, store-stated"
    elif "installer" in src:
        kind = "installer, measured"
    elif "hosted" in src:
        kind = "hosted original"
    else:
        kind = "estimate"
    return "%s (%s)" % (lab, kind)

PLAYER_LABELS = [
    ("single", "single-player"),
    ("local_coop", "local co-op"),
    ("online_coop", "online co-op"),
    ("local_multi", "local multiplayer"),
    ("online_multi", "online multiplayer"),
]

def players_text(pl):
    pl = pl or {}
    out = [lab for k, lab in PLAYER_LABELS if pl.get(k)]
    return ", ".join(out) if out else "players unknown"

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
        self.version_rows = {s: g for s, g in self.game_by_slug.items() if g.get("version_of")}
        self.catalog_games = [g for g in self.games_db["games"] if not g.get("version_of")]
        self.row_index = {}
        for g in self.games_db["games"]:
            self.row_index[g["slug"]] = g
        for g in self.software_rows + self.mods_rows:
            self.row_index[g["slug"]] = g
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
        for key in ("software", "tools", "mods"):
            if d.get(key):
                return d[key]
        return []

    def title_of(self, slug):
        g = self.game_by_slug.get(slug) or {}
        return g.get("title") or slug

    def build_vocab(self):
        self.devs, self.pubs, self.genres, self.subgenres = {}, {}, {}, {}
        self.cats, self.plats, self.chars = {}, {}, {}
        for g in self.games_db["games"]:
            for d_ in (g.get("developers") or []):
                self.devs.setdefault(keyify(d_), d_)
            for p_ in (g.get("publishers") or []):
                self.pubs.setdefault(keyify(p_), p_)
            for x in (g.get("genres") or []):
                self.genres.setdefault(keyify(x), x)
            for x in (g.get("subgenres") or []):
                self.subgenres.setdefault(keyify(x), x)
            c = clean_cat(g.get("category"))
            if c:
                self.cats.setdefault(keyify(c), c)
            for x in (g.get("platforms") or []):
                self.plats.setdefault(keyify(x), x)
        for s, p in self.page_by_slug.items():
            for c in (p.get("characters") or []):
                self.chars.setdefault(keyify(c), c)

    def page_url_of(self, slug):
        if slug not in self.page_by_slug:
            return None
        if slug in self.game_by_slug:
            return "pages/game/%s.html" % slug
        if slug in {r["slug"] for r in self.software_rows}:
            return "pages/software/%s.html" % slug
        if slug in {r["slug"] for r in self.mods_rows}:
            return "pages/mod/%s.html" % slug
        return None

    def is_version(self, slug):
        return slug in self.version_rows

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
            c["items"] = [s for s in (c.get("items") or []) if not self.is_version(s)]
            c["catalogued"] = [s for s in (c.get("catalogued") or []) if s in self.row_index]
            c["n_pages"] = len([s for s in c["items"] if s in self.page_by_slug])
        self.multis = self.collections_src.get("multi_collections", []) or []
        for m in self.multis:
            secs = {c.get("section") for cs in (m.get("collections") or [])
                    for c in self.collections if c["slug"] == cs}
            m["_sec"] = secs.pop() if len(secs) == 1 else None

    def collection_url(self, slug):
        c = next((x for x in self.collections if x["slug"] == slug), None)
        if c:
            return "pages/%s/collections/%s.html" % (c.get("section") or "games", slug)
        m = next((x for x in self.multis if x["slug"] == slug), None)
        if m:
            if m.get("_sec"):
                return "pages/%s/collections/%s.html" % (m["_sec"], slug)
            return "pages/meta/%s.html" % slug
        return None

    def collections_index_url(self, sec):
        return "pages/%s/collections.html" % sec

    def index_row(self, g, sec):
        y = year_of(g.get("release"))
        page = None
        th = None
        if sec == "games" and g["slug"] in self.page_by_slug:
            page = "game/%s.html" % g["slug"]
            th = self.th_root(self.page_by_slug[g["slug"]].get("thumbnail"))
        elif sec == "software" and g["slug"] in self.page_by_slug:
            page = "software/%s.html" % g["slug"]
        elif sec == "mods" and g["slug"] in self.page_by_slug:
            page = "mod/%s.html" % g["slug"]
        pl = g.get("players") or {}
        gn_disp = [self.genres.get(keyify(x), x) for x in (g.get("genres") or [])]
        dn_disp = [self.devs.get(keyify(x), x) for x in (g.get("developers") or [])]
        pn_disp = [self.pubs.get(keyify(x), x) for x in (g.get("publishers") or [])]
        cat_disp = clean_cat(g.get("category"))
        cap = ""
        ch, chn = [], []
        if sec == "games" and g["slug"] in self.page_by_slug:
            p = self.page_by_slug[g["slug"]]
            cap = (p.get("caption") or "")[:110]
            ch = [keyify(c) for c in (p.get("characters") or [])]
            chn = [self.chars.get(k, k) for k in ch]
        row = {
            "t": g.get("title") or "", "s": g["slug"], "sec": sec,
            "y": y, "date": g.get("release") or None,
            "g": [keyify(x) for x in (g.get("genres") or [])],
            "gn": gn_disp,
            "gs": [keyify(x) for x in (g.get("subgenres") or [])],
            "cat": keyify(cat_disp) if cat_disp else None,
            "catn": cat_disp or None,
            "w": g.get("content_walls") or [],
            "size": g.get("size_est_mb"), "szs": g.get("size_source"),
            "req": g.get("req_tier"), "ser": g.get("series"), "part": g.get("series_part"),
            "pl": [keyify(x) for x in (g.get("platforms") or [])],
            "p1": bool(pl.get("single")), "lc": bool(pl.get("local_coop")),
            "oc": bool(pl.get("online_coop")), "lm": bool(pl.get("local_multi")),
            "om": bool(pl.get("online_multi")),
            "era": ("%ss" % (y[:3] + "0")) if y else "unknown",
            "list": g.get("list"), "conf": g.get("confidence"),
            "tested": g.get("test_status") == "tested", "buy": g.get("buyable"),
            "big": bool(g.get("big_size")),
            "dev": [keyify(x) for x in (g.get("developers") or [])],
            "dn": dn_disp,
            "pub": [keyify(x) for x in (g.get("publishers") or [])],
            "pn": pn_disp,
            "ch": ch, "chn": chn,
            "page": page, "th": th, "cap": cap,
        }
        return row

    def build_index(self):
        self.rows = []
        for g in self.catalog_games:
            self.rows.append(self.index_row(g, "games"))
        for g in self.software_rows:
            self.rows.append(self.index_row(g, "software"))
        for g in self.mods_rows:
            self.rows.append(self.index_row(g, "mods"))
        for c in self.collections:
            self.rows.append({
                "t": c["title"], "s": c["slug"], "sec": "collections",
                "kind": c.get("kind", "collection"), "y": None, "date": None,
                "g": [], "gs": [], "w": [], "size": None, "pl": [],
                "req": None, "ser": None, "list": None, "conf": "verified",
                "tested": False, "buy": None, "big": False,
                "p1": False, "lc": False, "oc": False, "lm": False, "om": False,
                "ch": [], "chn": [], "cat": None, "catn": None,
                "n": c["n_pages"], "page": (self.collection_url(c["slug"]) or "")[len("pages/"):],
                "th": None, "cap": c.get("caption") or "",
            })
        for m in self.multis:
            self.rows.append({
                "t": m["title"], "s": m["slug"], "sec": "collections",
                "kind": "multi", "y": None, "date": None,
                "g": [], "gs": [], "w": [], "size": None, "pl": [],
                "req": None, "ser": None, "list": None, "conf": "verified",
                "tested": False, "buy": None, "big": False,
                "p1": False, "lc": False, "oc": False, "lm": False, "om": False,
                "ch": [], "chn": [], "cat": None, "catn": None,
                "n": len(m.get("collections") or []), "page": (self.collection_url(m["slug"]) or "")[len("pages/"):],
                "th": None, "cap": m.get("caption") or "",
            })

    def sec_counts(self):
        n = {"games": 0, "software": 0, "mods": 0, "collections": 0}
        for r in self.rows:
            n[r["sec"]] += 1
        return n

    def pages_dug(self):
        n = {"games": 0, "software": 0, "mods": 0}
        for s, p in self.page_by_slug.items():
            if self.is_version(s):
                continue
            if s in self.game_by_slug:
                n["games"] += 1
            elif s in {r["slug"] for r in self.software_rows}:
                n["software"] += 1
            elif s in {r["slug"] for r in self.mods_rows}:
                n["mods"] += 1
        return n

    def dig_order(self):
        return [p["slug"] for p in sorted(self.pages, key=lambda p: (p.get("dug_seq") or 0, p["slug"]))]

    def th_root(self, th):
        if not th:
            return None
        parts = th.split("/")
        while parts and parts[0] == "..":
            parts.pop(0)
        return "/".join(parts)

    def thumb_at(self, th, depth):
        if not th:
            return None
        if th.startswith(("http://", "https://", "data:")):
            return th
        return ("../" * depth) + self.th_root(th)

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
                shared_c = a["cat"] and a["cat"] == b["cat"]
                if shared_g:
                    score += 3 * len(shared_g)
                    why += [self.genres.get(k, k) for k in shared_g]
                if shared_s:
                    score += 2 * len(shared_s)
                    why += [self.subgenres.get(k, k) for k in shared_s]
                if shared_c:
                    score += 1
                    why.append(a["catn"])
                if a["era"] == b["era"] and a["era"] != "unknown":
                    score += 1
                    why.append(a["era"])
                if set(a["dev"]) & set(b["dev"]):
                    score += 1
                    why.append(self.devs.get((set(a["dev"]) & set(b["dev"])).__iter__().__next__()))
                if score > 0:
                    pool.append({"slug": b["s"], "title": b["t"], "th": b["th"], "y": b["y"], "cap": b.get("cap") or "",
                                 "score": score, "why": ", ".join(why[:4])})
            pool.sort(key=lambda x: (-x["score"], x["title"].casefold()))
            catalogued = []
            if len(pool) < 4:
                for b in self.rows:
                    if b["sec"] != "games" or b["page"] or b["s"] == a["s"]:
                        continue
                    if a["ser"] and b["ser"] == a["ser"]:
                        continue
                    shared = set(a["g"]) & set(b["g"]) or (a["cat"] and a["cat"] == b["cat"])
                    if shared:
                        catalogued.append(b["t"])
                    if len(catalogued) >= 6:
                        break
            self.similar[a["s"]] = {"pages": pool[:10], "catalogued": catalogued}

    def versions_of(self, slug):
        row = self.game_by_slug.get(slug) or {}
        main = row.get("version_of") or slug
        mp = self.page_by_slug.get(main)
        if not mp:
            return None
        sibs = [{"slug": main, "label": "standard", "title": self.title_of(main)}]
        for e in (mp.get("versions") or []):
            if e == main or e not in self.page_by_slug:
                continue
            sibs.append({"slug": e, "label": self.page_by_slug[e].get("release_label") or "edition",
                         "title": self.title_of(e)})
        if len(sibs) < 2:
            return None
        return {"group": mp.get("group_label") or self.title_of(main),
                "current": slug, "siblings": sibs}

    def upgrades_of(self, slug):
        out = {"direct": [], "superseded_by": None, "upgrades": [], "remaster": None}
        g = self.game_by_slug.get(slug) or {}
        for u in (g.get("upgrades") or []):
            ug = self.game_by_slug.get(u)
            if ug and not ug.get("version_of"):
                out["upgrades"].append({"slug": u, "title": ug["title"], "page": u in self.page_by_slug})
        for other, og in self.game_by_slug.items():
            if slug in (og.get("upgrades") or []) and other in self.page_by_slug:
                out["direct"].append({"slug": other, "title": og["title"]})
        out["direct"].sort(key=lambda d: d["title"].casefold())
        sb = g.get("superseded_by")
        if sb and sb in self.game_by_slug:
            out["superseded_by"] = {"slug": sb, "title": self.game_by_slug[sb]["title"]}
        if g.get("remaster"):
            rg = self.game_by_slug.get(g["remaster"])
            if rg:
                out["remaster"] = {"slug": g["remaster"], "title": rg["title"],
                                   "page": g["remaster"] in self.page_by_slug,
                                   "note": g.get("remaster_note")}
        return out

    def series_line(self, slug):
        g = self.game_by_slug.get(slug) or {}
        ser = g.get("series")
        if not ser or ser not in self.series_map:
            return None
        s = self.series_map[ser]
        members = []
        for m in s.get("members", []):
            row = self.game_by_slug.get(m["slug"])
            if row and row.get("version_of"):
                continue
            members.append({
                "slug": m["slug"], "title": m["title"], "part": m.get("part"),
                "kind": m.get("kind"), "cat": m["slug"] in self.game_by_slug,
                "page": m["slug"] in self.page_by_slug and not self.is_version(m["slug"]),
                "now": m["slug"] == slug,
                "y": m.get("y") or year_of((row or {}).get("release")),
            })
        members.sort(key=lambda m: (m["part"] is None, m["part"] or 0,
                                    m["y"] or "9999", m["title"].casefold()))
        return {"key": ser, "title": SERIES_TITLES.get(ser, s.get("title", ser)), "members": members}

    def facts_of(self, slug):
        g = self.game_by_slug.get(slug) or {}
        p = self.page_by_slug.get(slug) or {}
        return {
            "released": date_str(g.get("release")) or "unknown",
            "year": year_of(g.get("release")),
            "devs": g.get("developers") or [],
            "pubs": g.get("publishers") or [],
            "platforms": g.get("platforms") or [],
            "players": players_text(g.get("players")),
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
            "category": clean_cat(g.get("category")),
            "req": p.get("req") or {},
            "characters": p.get("characters") or [],
        }
