from kage_core import esc, rel, keyify, date_str, size_display, BUILD_V, jwrite, os

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=IBM+Plex+Mono:ital,wght@0,400;0,600;1,400&family=Silkscreen:wght@400;700&family=VT323&display=swap" rel="stylesheet">'
FAVICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 64 64\'%3E%3Crect x=\'5\' y=\'5\' width=\'54\' height=\'54\' rx=\'12\' fill=\'%23070707\' stroke=\'%23e8e8e8\' stroke-width=\'4\'/%3E%3Ctext x=\'32\' y=\'45\' font-family=\'monospace\' font-size=\'34\' font-weight=\'bold\' fill=\'%23e8e8e8\' text-anchor=\'middle\'%3E?%3C/text%3E%3C/svg%3E">'
CRT = '<div class="crt" aria-hidden="true"><div class="crt-scanlines"></div><div class="crt-vignette"></div></div>'
DIAMOND = ('<span class="logo-diamond" aria-hidden="true"><span class="pos pos-t">W</span>'
           '<span class="pos pos-l">A</span><span class="pos pos-b">?</span><span class="pos pos-r">D</span></span>')

def head(title, desc, depth, body_attr=""):
    css = rel("assets/css/style.css", None, depth)
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>' + esc(title) + '</title>'
            '<meta name="description" content="' + esc(desc) + '">' + FAVICON + FONTS +
            '<link rel="stylesheet" href="' + css + '?v=' + BUILD_V + '"></head>'
            '<body' + (' ' + body_attr if body_attr else '') + '>' + CRT)

def topbar(eng, depth, active, action=None):
    if action is None:
        action = rel("", "pages/search.html", depth)
    c = eng.sec_counts()
    page_n = {"games": 0, "software": 0, "mods": 0}
    for r in eng.rows:
        if r.get("page") and r["sec"] in page_n:
            page_n[r["sec"]] += 1
    npages = page_n
    def nav_link(label, href, key, n=None):
        cls = ' class="here"' if active == key else ""
        cnt = ' <span class="count">(%d)</span>' % n if n is not None else ""
        return '<a' + cls + ' href="' + href + '">' + label + cnt + '</a>'
    def nav_dead(label, n):
        return '<span class="dead">' + label + ' <span class="count">(' + str(n) + ')</span></span>'
    nav = []
    if c["games"] > 0:
        nav.append(nav_link("GAMES", rel("", "pages/games.html", depth), "games", page_n["games"]))
    else:
        nav.append(nav_dead("GAMES", 0))
    if c["software"] > 0:
        nav.append(nav_link("SOFTWARE", rel("", "pages/software.html", depth), "software", page_n["software"]))
    else:
        nav.append(nav_dead("SOFTWARE", 0))
    if c["mods"] > 0:
        nav.append(nav_link("MODS+PATCHES", rel("", "pages/mods.html", depth), "mods", page_n["mods"], ))
    else:
        nav.append(nav_dead("MODS+PATCHES", 0))
    if c["collections"] > 0:
        nav.append(nav_link("COLLECTIONS", rel("", "pages/collections.html", depth), "collections"))
    nav.append('<a href="' + rel("", "pages/random.html", depth) + '">RANDOM</a>')
    logo_href = rel("", "index.html", depth) if depth else "#top"
    return ('<header class="site-head"><a class="logo" href="' + logo_href + '" aria-label="WA?D - home">' + DIAMOND +
            '<span class="logo-word">GOODGAMES<em>SURVIVE</em></span></a>'
            '<nav class="site-nav">' + "".join(nav) + '</nav>'
            '<form class="head-search" action="' + action + '" method="get" role="search">'
            '<input type="search" name="q" placeholder="search the catalogue" aria-label="search the catalogue"></form></header>')

def foot_site(depth):
    return ('<footer class="site-foot"><div class="foot-brand">' +
            '<span class="foot-diamond" aria-hidden="true"><span class="pos pos-t">W</span><span class="pos pos-l">A</span>'
            '<span class="pos pos-b">?</span><span class="pos pos-r">D</span></span>'
            '<span class="foot-line">GOODGAMES SURVIVE</span></div>'
            '<div class="foot-meta"><a href="https://github.com/HAKORADev/GoodGamesSurvive" target="_blank" rel="noopener">GITHUB REPO</a>'
            '<span>&#169; 2026</span></div></footer>')

def foot_page(depth):
    return ('<footer class="page-foot"><span>GOODGAMES SURVIVE</span>'
            '<a href="' + rel("", "index.html", depth) + '">MAIN PAGE</a>'
            '<a href="https://github.com/HAKORADev/GoodGamesSurvive">GITHUB REPO</a>'
            '<span>&#169; 2026</span></footer>')

def chip(label, href=None, warn=False):
    cls = "chip chip-warn" if warn else "chip"
    if href:
        return '<a class="' + cls + '" href="' + href + '">' + esc(label) + '</a>'
    return '<span class="' + cls + '">' + esc(label) + '</span>'

GALLERY_JS = """
(function(){
  var MAIN=document.getElementById('gal-main');
  var vids=%VIDS%;
  document.querySelectorAll('.g-thumb').forEach(function(t){
    t.addEventListener('click',function(){
      document.querySelectorAll('.g-thumb').forEach(function(x){x.classList.remove('on')});
      t.classList.add('on');
      var k=t.getAttribute('data-kind');
      if(k==='img'){
        MAIN.innerHTML='<img src="'+t.getAttribute('data-src')+'" alt="in-game shot">';
      }else{
        var id=t.getAttribute('data-vid');
        MAIN.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'" title="gameplay video" allowfullscreen loading="lazy"></iframe>';
      }
    });
  });
  MAIN.addEventListener('error',function(){},true);
})();
""".replace("%VIDS%", "[]")

def gallery_html(p, title):
    g = p.get("gallery") or {}
    imgs = g.get("images") or []
    vids = g.get("videos") or []
    tiles = []
    for i, u in enumerate(imgs):
        on = ' on' if i == 0 else ''
        tiles.append(('<button class="g-thumb g-thumb-img' + on + '" data-kind="img" data-src="' + esc(u) + '" type="button">'
                      '<img src="' + esc(u) + '" alt="' + esc(title) + ' in-game shot" loading="lazy" '
                      'onerror="this.closest(\'.g-thumb\').classList.add(\'g-dead\');this.remove()"></button>'))
    for v in vids:
        tiles.append(('<button class="g-thumb g-thumb-vid" data-kind="vid" data-vid="' + esc(v["id"]) + '" type="button">'
                      '<img src="https://i.ytimg.com/vi/' + esc(v["id"]) + '/hqdefault.jpg" alt="gameplay video" loading="lazy" '
                      'onerror="this.closest(\'.g-thumb\').classList.add(\'g-dead\');this.remove()">'
                      '<span class="g-play" aria-hidden="true">&#9654;</span></button>'))
    main_img = imgs[0] if imgs else ""
    main = ('<div class="gallery-main" id="gal-main">' +
            ('<img src="' + esc(main_img) + '" alt="' + esc(title) + '" '
             'onerror="this.parentNode.innerHTML=\'<div class=media-dead>MEDIA NOT FOUND<span>the internet ate this one - it was verified when the page was built</span></div>\'">' if main_img else '<div class="media-dead">MEDIA NOT FOUND<span>no verified media for this title yet</span></div>') +
            '</div>')
    strip = '<div class="gallery-strip">' + "".join(tiles) + '</div>' if tiles else ""
    js = ("<script>(function(){var M=document.getElementById('gal-main');"
          "function deadMain(){M.innerHTML='<div class=\"media-dead\">MEDIA NOT FOUND<span>the internet ate this one - it was verified when the page was built</span></div>';}"
          "function showImg(u){var im=new Image();im.onload=function(){M.innerHTML='';M.appendChild(im)};im.onerror=deadMain;im.alt='in-game shot';im.src=u;}"
          "document.querySelectorAll('.g-thumb').forEach(function(t){t.addEventListener('click',function(){"
          "document.querySelectorAll('.g-thumb').forEach(function(x){x.classList.remove('on')});t.classList.add('on');"
          "if(t.getAttribute('data-kind')==='img'){showImg(t.getAttribute('data-src'));}"
          "else{M.innerHTML='<iframe src=\"https://www.youtube-nocookie.com/embed/'+t.getAttribute('data-vid')+'\" title=\"gameplay\" allowfullscreen loading=\"lazy\"></iframe>';}});});})();</script>")
    return main + strip + js

def req_html(f):
    tier = f.get("req", {}).get("tier")
    note = f.get("req", {}).get("note") or ""
    tiers = [("below", "LOWER THAN TARGET"), ("at", "AT TARGET"), ("above", "ABOVE TARGET")]
    cells = []
    for k, lab in tiers:
        cls = "req-cell on" if tier == k else "req-cell"
        cells.append('<div class="' + cls + '"><span>' + lab + '</span></div>')
    if not tier:
        cells.append('<div class="req-cell req-unknown"><span>TIER UNKNOWN</span></div>')
    return ('<div class="req-ladder">' + "".join(cells) + '</div>'
            '<p class="req-note">' + esc(note) + '</p>'
            '<p class="req-base">the target bar: haswell-class CPU with HD xxxx iGPU, windows 10. testing is a separate truth - see the status box.</p>')

def versions_html(eng, slug):
    v = eng.versions_of(slug)
    up = eng.upgrades_of(slug)
    out = []
    if v and len(v["siblings"]) > 1:
        opts = []
        for s in v["siblings"]:
            sel = " selected" if s["slug"] == v["current"] else ""
            opts.append('<option value="' + rel("", "pages/game/%s.html" % s["slug"], 2) + '"' + sel + '>' +
                        esc(s["label"]) + '</option>')
        out.append('<div class="ver-row"><span class="ver-k">RELEASES UNDER ' + esc((v["label"] or "").upper()) + '</span>'
                   '<select class="ver-select" onchange="if(this.value)location.href=this.value" aria-label="switch release">' + "".join(opts) + '</select></div>')
    ups = up.get("upgrades") or []
    if ups:
        links = []
        for u in ups:
            if u["page"]:
                links.append('<a href="' + rel("", "pages/game/%s.html" % u["slug"], 2) + '">' + esc(u["title"]) + '</a>')
            else:
                links.append('<span class="ver-nolink">' + esc(u["title"]) + ' (catalogued - no page yet)</span>')
        out.append('<p class="ver-up">UPGRADE: ' + " · ".join(links) + '</p>')
    if up.get("direct"):
        d = up["direct"]
        out.append('<p class="ver-up">THIS PAGE IS THE DIRECT UPGRADE OF <a href="' + rel("", "pages/game/%s.html" % d["slug"], 2) + '">' + esc(d["title"]) + '</a></p>')
    if up.get("superseded_by"):
        s = up["superseded_by"]
        out.append('<p class="ver-up">SUPERSEDED BY <a href="' + rel("", "pages/game/%s.html" % s["slug"], 2) + '">' + esc(s["title"]) + '</a> - the standalone release is gone; the content lives there now.</p>')
    return '<section><h2 class="sec-title">VERSIONS &amp; UPGRADES</h2>' + "".join(out) + '</section>' if out else ""

def downloads_html(p):
    lk = p.get("links") or {}
    rows = []
    off = lk.get("official") or []
    if off:
        items = "".join('<a href="' + esc(a["url"]) + '" target="_blank" rel="noopener">' + esc(a["label"]) + '</a>' for a in off)
        notes = " · ".join(filter(None, [a.get("note") for a in off]))
        rows.append('<div class="dl-row"><span class="dl-kind">OFFICIAL</span>' + items + '</div>')
        rows.append('<p class="dl-note">' + esc(notes) + '</p>')
    rows.append('<div class="dl-row"><span class="dl-kind">OFFICIAL STATUS</span><span class="dl-status">' + esc(lk.get("official_note") or "") + '</span></div>')
    anyw = lk.get("anyway") or []
    if anyw:
        items = "".join('<a href="' + esc(a["url"]) + '" target="_blank" rel="noopener">' + esc(a["label"]) + '</a>' for a in anyw)
        rows.append('<div class="dl-row"><span class="dl-kind">ANYWAY</span>' + items + '</div>')
    rows.append('<p class="dl-note">' + esc(lk.get("anyway_note") or "") + '</p>')
    return "".join(rows)

def game_page(eng, slug):
    g = eng.game_by_slug[slug]
    p = eng.page_by_slug[slug]
    f = eng.facts_of(slug)
    title = g["title"]
    depth = 2
    chips = []
    chips.append(chip((f["list"] or "").upper()))
    for gen in f["genres"][:5]:
        chips.append(chip(gen, rel("", "pages/games.html", depth) + "?genre=" + keyify(gen)))
    for t in f["tags"]:
        if t in ("single-player", "co-op", "multiplayer"):
            chips.append(chip(t.upper(), rel("", "pages/games.html", depth) + "?players=" + ("single" if t == "single-player" else ("coop" if t == "co-op" else "multi"))))
        elif t in ("big-size",):
            chips.append(chip("BIG-SIZE", rel("", "pages/games.html", depth) + "?status=big", warn=True))
        else:
            chips.append(chip(t.upper(), rel("", "pages/games.html", depth) + "?tag=" + keyify(t)))
    chips.append(chip("NOT TESTED" if not f["tested"] else "TESTED", warn=not f["tested"]))

    facts_rows = []
    facts_rows.append(("<tr><td class=\"k\">released</td><td class=\"v\"><a href=\"" + rel("", "pages/games.html", depth) + "?era=" + (f["year"][:3] + "0s" if f["year"] else "unknown") + "\">" + esc(f["released"]) + "</a></td></tr>"))
    if f["devs"]:
        facts_rows.append('<tr><td class="k">developer</td><td class="v">' + " · ".join('<a href="' + rel("", "pages/games.html", depth) + '?dev=' + keyify(d) + '">' + esc(d) + '</a>' for d in f["devs"]) + '</td></tr>')
    if f["pubs"]:
        facts_rows.append('<tr><td class="k">publisher</td><td class="v">' + " · ".join('<a href="' + rel("", "pages/games.html", depth) + '?pub=' + keyify(d) + '">' + esc(d) + '</a>' for d in f["pubs"]) + '</td></tr>')
    facts_rows.append('<tr><td class="k">platform</td><td class="v">' + " · ".join('<a href="' + rel("", "pages/games.html", depth) + '?platform=' + keyify(x) + '">' + esc(x) + '</a>' for x in f["platforms"]) + '</td></tr>')
    facts_rows.append('<tr><td class="k">players</td><td class="v"><a href="' + rel("", "pages/games.html", depth) + '?players=' + ("coop" if "co-op" in f["players"] else "single") + '">' + esc(f["players"]) + '</a></td></tr>')
    if f["series"]:
        facts_rows.append('<tr><td class="k">series</td><td class="v"><a href="' + rel("", "pages/games.html", depth) + '?series=' + esc(f["series"]) + '">' + esc((eng.series_map.get(f["series"]) or {}).get("title", f["series"])) + '</a>' + (' - part %s' % f["part"] if f["part"] else '') + '</td></tr>')
    if f["walls"]:
        facts_rows.append('<tr><td class="k">content walls</td><td class="v">' + " · ".join('<a class="wall" href="' + rel("", "pages/games.html", depth) + '?content=' + esc(w) + '">' + esc(w.upper()) + '</a>' for w in f["walls"]) + '</td></tr>')
    else:
        facts_rows.append('<tr><td class="k">content walls</td><td class="v">none</td></tr>')
    facts_rows.append('<tr><td class="k">size</td><td class="v">' + esc(f["size"]) + '</td></tr>')
    facts_rows.append('<tr><td class="k">still sold</td><td class="v">' + ("yes" if f["buyable"] else ("no - delisted or un-buyable" if f["buyable"] is False else "unknown")) + '</td></tr>')
    facts_rows.append('<tr><td class="k">test status</td><td class="v">' + ("tested" if f["tested"] else "not-tested") + '</td></tr>')
    facts_rows.append('<tr><td class="k">target</td><td class="v">windows 10 - haswell HD xxxx iGPU bar</td></tr>')

    sims = eng.similar.get(slug) or {"pages": [], "catalogued": []}
    sim_cards = []
    for s in sims["pages"][:10]:
        th = ('<span class="dir-thumb"><img src="' + esc(s["th"]) + '" alt="" loading="lazy" onerror="this.parentNode.classList.add(\'dead\');this.remove()"></span>' if s["th"] else '<span class="dir-thumb dead"></span>')
        sim_cards.append('<a class="dir-row sim-row" href="' + rel("", "pages/game/%s.html" % s["slug"], depth) + '">' + th +
                         '<span class="dir-main"><span class="dir-name">' + esc(s["title"]) + '</span>' +
                         '<span class="dir-meta">' + esc((s["y"] or "") + (" · " if s["y"] else "")) + esc(s.get("why") or "") + '</span></span>'
                         '<span class="dir-go">OPEN &#8594;</span></a>')
    sim_html = ('<section><h2 class="sec-title">MORE LIKE THIS</h2><div class="dir sim-dir">' + "".join(sim_cards) + '</div>' +
                ('<p class="dir-note">also in the catalogue, no page yet: ' + esc(" · ".join(sims["catalogued"])) + '</p>' if sims["catalogued"] else '') +
                '</section>') if sim_cards else ""

    cols = eng.collection_of(slug)
    col_line = ""
    if cols:
        col_line = '<section><h2 class="sec-title">COLLECTIONS</h2><p class="series-line">' + " · ".join('<a class="m now" href="' + rel("", "pages/collection/%s.html" % c["slug"], depth) + '">' + esc(c["title"]) + '</a>' for c in cols) + '</p></section>'

    chars = ""
    if f["characters"]:
        chars = '<section><h2 class="sec-title">CHARACTERS</h2><p class="chars-line">' + " · ".join('<span class="char">' + esc(c) + '</span>' for c in f["characters"]) + '</p></section>'

    ser = eng.series_line(slug)
    ser_html = ""
    if ser:
        ms = []
        for m in ser["members"]:
            label = esc(m["title"]) + (' · ' + str(m["y"]) if m["y"] else '')
            if m["now"]:
                ms.append('<span class="m now">' + label + ' - this page</span>')
            elif m["page"]:
                ms.append('<a class="m" href="' + rel("", "pages/game/%s.html" % m["slug"], depth) + '">' + label + '</a>')
            else:
                ms.append('<span class="m">' + label + '</span>')
        ser_html = '<section><h2 class="sec-title">SERIES - ' + esc(ser["title"].upper()) + '</h2><p class="series-line">' + "".join(m for m in ms) + '</p></section>'

    body = ['<main class="page-wrap">',
            '<p class="crumb"><a href="' + rel("", "index.html", depth) + '">GOODGAMES SURVIVE</a> / <a href="' + rel("", "pages/games.html", depth) + '">GAMES</a> / <b>' + esc(title) + '</b></p>',
            '<div class="game-top"><div class="game-cover"><img src="' + esc(p.get("thumbnail") or "") + '" alt="' + esc(title) + ' cover" onerror="this.parentNode.classList.add(\'dead\');this.remove()"></div>',
            '<div class="game-title"><h1>' + esc(title) + '</h1>',
            '<p class="game-caption">' + esc(p.get("caption") or "") + '</p>',
            '<p class="game-meta">' + esc((f["year"] or "year unknown") + " · " + " · ".join(f["devs"] or ["developer unknown"])) + '</p>',
            '<div class="chips">' + "".join(chips) + '</div></div></div>',
            '<section><h2 class="sec-title">GALLERY</h2>' + gallery_html(p, title) + '</section>',
            '<section><h2 class="sec-title">ABOUT ' + esc(title.upper()) + '</h2>' + "".join('<p class="about-p">' + esc(a) + '</p>' for a in (p.get("about") or [])) + '</section>',
            '<section><h2 class="sec-title">FACTS</h2><table class="facts">' + "".join(facts_rows) + '</table></section>',
            chars,
            '<section><h2 class="sec-title">REQUIREMENTS - VS THE TARGET</h2>' + req_html(f) + '</section>',
            versions_html(eng, slug),
            ser_html,
            col_line,
            '<section><h2 class="sec-title">DOWNLOADS</h2>' + downloads_html(p) + '</section>',
            sim_html,
            '<div class="status-box">' + (('<b>TESTED.</b> the owner took this build end to end: download, install, run, pathing, saves. what you read here was played, not assumed.') if f["tested"] else ('<b>NOT TESTED.</b> nobody has taken this build end to end yet: download, install, run, pathing, save games. the owner tests every game before its status flips to tested - and until then, this page says so.')) + '</div>',
            '</main>']

    desc = (p.get("caption") or title)[:150]
    html = (head(title + " — GOODGAMES SURVIVE", desc, depth, 'data-game="' + slug + '"') +
            topbar(eng, depth, "games") + "".join(body) + foot_page(depth) + '</body></html>')
    return html
