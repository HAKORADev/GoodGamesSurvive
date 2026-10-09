from kage_core import esc, rel, keyify, BUILD_V, os
from kage_render import head, topbar, foot_site, foot_page, chip

LIST_JS = """
(function(){
var SEC=document.body.getAttribute('data-sec');
var MODE=document.body.getAttribute('data-mode')||'list';
var OUT=document.getElementById('out'),COUNT=document.getElementById('count'),
ACTIVE=document.getElementById('active'),FACETS=document.getElementById('facets'),
Q=document.getElementById('q'),SORTSEL=document.getElementById('sort'),SHUF=document.getElementById('shuf');
var ROWS=[],SHELF=0,VOCAB=window.VOCAB||{};
var P=new URLSearchParams(location.search);
var FK=['q','genre','sub','tag','content','platform','players','era','dev','pub','series','status','sort','seed','sec'];
function gp(k){return P.get(k)||''}
function sp(k,v){if(v)P.set(k,v);else P['delete'](k);var s=P.toString();history.replaceState(null,'',location.pathname+(s?('?'+s):''))}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;var t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function facetOf(r,k){
 if(k==='genre')return r.g; if(k==='sub')return r.gs; if(k==='tag')return r.tg;
 if(k==='content')return r.w; if(k==='platform')return r.pl;
 if(k==='era')return [r.era||'unknown']; if(k==='series')return r.ser?[r.ser]:[];
 if(k==='dev')return r.dev; if(k==='pub')return r.pub;
 if(k==='players'){var a=[];if(r.p1)a.push('single');if(r.pc)a.push('coop');if(r.pm)a.push('multi');return a}
 if(k==='status'){var b=[];b.push(r.tested?'tested':'not-tested');if(r.conf==='verified')b.push('verified');if(r.big)b.push('big-size');if(r.buy===true)b.push('still-sold');if(r.buy===false)b.push('un-buyable');return b}
 return[]}
function filters(){var f={};FK.forEach(function(k){var v=gp(k);if(v)f[k]=v});return f}
function matches(r,f,skip){
 if(MODE==='list'){if(r.sec!==SEC)return false}
 else{var sc=f.sec||'all';if(sc!=='all'&&r.sec!==sc)return false}
 if(f.q&&skip!=='q'){var hay=(r.t+' '+(r.ser||'')+' '+(r.cat||'')+' '+(r.y||'')+' '+(r.cap||'')+' '+(r.gn||[]).join(' ')+' '+(r.dn||[]).join(' ')+' '+(r.pn||[]).join(' ')+' '+(r.tg||[]).join(' ')).toLowerCase();
  var toks=f.q.toLowerCase().split(/\\s+/);for(var i=0;i<toks.length;i++){if(hay.indexOf(toks[i])===-1)return false}}
 if(f.genre&&skip!=='genre'&&r.g.indexOf(f.genre)<0)return false;
 if(f.sub&&skip!=='sub'&&r.gs.indexOf(f.sub)<0)return false;
 if(f.tag&&skip!=='tag'&&r.tg.indexOf(f.tag)<0)return false;
 if(f.content&&skip!=='content'&&r.w.indexOf(f.content)<0)return false;
 if(f.platform&&skip!=='platform'&&r.pl.indexOf(f.platform)<0)return false;
 if(f.era&&skip!=='era'&&(r.era||'unknown')!==f.era)return false;
 if(f.series&&skip!=='series'&&r.ser!==f.series)return false;
 if(f.dev&&skip!=='dev'&&r.dev.indexOf(f.dev)<0)return false;
 if(f.pub&&skip!=='pub'&&r.pub.indexOf(f.pub)<0)return false;
 if(f.players&&skip!=='players'&&facetOf(r,'players').indexOf(f.players)<0)return false;
 if(f.status&&skip!=='status'&&facetOf(r,'status').indexOf(f.status)<0)return false;
 return true}
function secPool(f){return ROWS.filter(function(r){return matches(r,f,null)})}
function chipHTML(k,v,lab,n,on){
 return '<button type="button" class="fchip'+(on?' on':'')+'" data-k="'+k+'" data-v="'+esc(v)+'">'+esc(lab)+'<i>'+n+'</i></button>'}
 function vlab(k,v,labs){var m={genre:'g',tag:'tg',content:'w',platform:'pl'}[k];return (m&&VOCAB[m]&&VOCAB[m][v])||(labs&&labs[v])||v}
function renderFacets(f){
 var groups=[['genre','GENRE'],['tag','TAG'],['content','CONTENT'],['platform','PLATFORM'],['players','PLAYERS'],['era','ERA'],['status','STATUS']];
 var h='';
 groups.forEach(function(gr){
  var k=gr[0],lab=gr[1];
  var pool=ROWS.filter(function(r){return matches(r,f,k)});
  var counts={};
  pool.forEach(function(r){facetOf(r,k).forEach(function(v){counts[v]=(counts[v]||0)+1})});
  var keys=Object.keys(counts).filter(function(v){return v!=='unknown'||k==='era'});
  keys.sort(function(a,b){return counts[b]-counts[a]||a.localeCompare(b)});
  if(k==='players'){keys=['single','coop','multi'].filter(function(v){return counts[v]})}
  if(!keys.length)return;
  var labs={single:'single-player',coop:'co-op',multi:'multiplayer',sex:'sex',gore:'gore','big-size':'big-size','still-sold':'still sold','un-buyable':'un-buyable',tested:'tested','not-tested':'not-tested',verified:'verified'};
  keys=(k==='status'?['tested','verified','big-size','still-sold','un-buyable']:keys).filter(function(v){return counts[v]});
  if(k!=='status'&&k!=='players'){keys=keys.slice(0,14)}
  h+='<div class="fgroup"><span class="fgroup-k">'+lab+'</span>'+keys.map(function(v){
   return chipHTML(k,v,vlab(k,v,labs),counts[v],f[k]===v)}).join('')+'</div>'});
 if(FACETS)FACETS.innerHTML=h||'<div class="fgroup"><span class="fgroup-k">FACETS</span><span class="fgroup-none">no facets for this pool</span></div>';
 if(!FACETS)return;
 FACETS.querySelectorAll('.fchip').forEach(function(b){
  b.addEventListener('click',function(){var k=b.getAttribute('data-k'),v=b.getAttribute('data-v');
   sp(k,f[k]===v?'':v);render()})})}
function renderActive(f){
 var h='',n=0;
 FK.forEach(function(k){if(k==='sort'||k==='seed'||k==='sec')return;var v=f[k];if(!v)return;n++;
  var lab=k==='q'?('"'+v+'"'):(k+': '+v);
  h+='<button type="button" class="achip" data-k="'+k+'">'+esc(lab)+' &#215;</button>'});
 h+=(n?'<button type="button" class="achip achip-clear" data-k="__all">CLEAR ALL</button>':'');
 ACTIVE.innerHTML=h;
 ACTIVE.querySelectorAll('.achip').forEach(function(b){b.addEventListener('click',function(){
  var k=b.getAttribute('data-k');if(k==='__all'){FK.forEach(function(x){if(x!=='sort'&&x!=='seed'&&x!=='sec')sp(x,'')})}else{sp(k,'')}render()})})}
function rowHTML(r){
 var flags=[];
 if(r.list)flags.push(r.list.toUpperCase());
 if(r.big)flags.push('BIG-SIZE');
 (r.w||[]).forEach(function(x){flags.push(x.toUpperCase())});
 (r.tg||[]).slice(0,5).forEach(function(x){flags.push(x.toUpperCase())});
 var meta=[r.y||'year unknown',(r.dn||[]).join(', '),(r.gn||[]).join(', ')].filter(Boolean).join(' · ');
 var sizeTxt=r.size?((r.size>=1024?(Math.round(r.size/102.4)/10)+' GB':r.size+' MB')+' est'):'—';
 var th=r.th?'<span class="dir-thumb"><img loading="lazy" alt="" src="'+esc(r.th)+'" onerror="this.parentNode.classList.add(\\'dead\\');this.remove()"></span>':'<span class="dir-thumb dead"></span>';
 var inner=th+'<span class="dir-main"><span class="dir-name">'+esc(r.t)+'</span><span class="dir-meta">'+esc(meta)+'</span><span class="dir-flags">'+flags.map(esc).join(' · ')+'</span></span><span class="dir-size">'+sizeTxt+'</span>'+(r.page?'<span class="dir-go">OPEN &#8594;</span>':'<span class="dir-go dir-go-dim">IN CATALOGUE</span>');
 return r.page?'<a class="dir-row" href="'+esc(r.page)+'">'+inner+'</a>':'<div class="dir-row dir-row-plain">'+inner+'</div>'}
function sortRows(rows,f){
 var s=f.sort||'name-asc';
 if(s==='random'){var seed=parseInt(f.seed||'1',10)||1;var r=rng(seed);rows=rows.slice();for(var i=rows.length-1;i>0;i--){var j=Math.floor(r()*(i+1));var t=rows[i];rows[i]=rows[j];rows[j]=t}return rows}
 rows=rows.slice();
 var num=function(v){return v==null?null:v};
 rows.sort(function(a,b){
  if(s==='name-asc')return a.t.localeCompare(b.t);
  if(s==='name-desc')return b.t.localeCompare(a.t);
  if(s==='date-desc'||s==='date-asc'){var x=a.date||'',y=b.date||'';if(x===y)return a.t.localeCompare(b.t);if(!x)return 1;if(!y)return -1;return s==='date-desc'?y.localeCompare(x):x.localeCompare(y)}
  if(s==='size-desc'||s==='size-asc'){var m=num(a.size),n=num(b.size);if(m===n)return a.t.localeCompare(b.t);if(m==null)return 1;if(n==null)return -1;return s==='size-desc'?n-m:m-n}
  return 0});
 return rows}
function render(){
 var f=filters();
 if(Q&&document.activeElement!==Q&&f.q)Q.value=f.q;
 var pool=ROWS.filter(function(r){return matches(r,f,null)});
 var pageN=pool.filter(function(r){return r.page}).length;
 if(SORTSEL)SORTSEL.value=f.sort||'name-asc';
 renderActive(f);if(FACETS)renderFacets(f);
 if(!pool.length){
  OUT.innerHTML='<div class="empty">no hits. the filters ate everything.<button type="button" id="clearbtn">clear all filters</button></div>';
  var cb=document.getElementById('clearbtn');if(cb)cb.addEventListener('click',function(){FK.forEach(function(x){if(x!=='sort'&&x!=='seed'&&x!=='sec')sp(x,'')});render()});
 }else{
  OUT.innerHTML=sortRows(pool,f).map(rowHTML).join('');
 }
 if(COUNT){
  if(MODE==='search'){COUNT.textContent=pool.length+' results across the whole catalogue ('+pageN+' with their own page)'}
  else{COUNT.textContent=pool.length+' of '+SHELF+' titles in this shelf · '+pageN+' pages dug'}
 }
}
if(SHUF)SHUF.addEventListener('click',function(){sp('sort','random');sp('seed',String(Math.floor(Math.random()*1000000)));render()});
if(SORTSEL)SORTSEL.addEventListener('change',function(){sp('sort',SORTSEL.value);if(SORTSEL.value==='random'&&!gp('seed'))sp('seed',String(Math.floor(Math.random()*1000000)));render()});
var QT=null;
if(Q)Q.addEventListener('input',function(){clearTimeout(QT);QT=setTimeout(function(){sp('q',Q.value.trim());render()},180)});
fetch(document.body.getAttribute('data-index')+'?v=__V__').then(function(r){return r.json()}).then(function(d){
 ROWS=d.rows;SHELF=ROWS.filter(function(r){return MODE==='search'||r.sec===SEC}).length;render();
}).catch(function(){COUNT.textContent='index failed to load - refresh once'});
})();
""".replace("__V__", BUILD_V)

def vocab_script(eng):
    import json as _json
    v = {"g": eng.genres, "tg": eng.tags, "pl": eng.plats,
         "w": {"sex": "sex", "gore": "gore"}}
    return '<script>window.VOCAB=' + _json.dumps(v, ensure_ascii=False) + ';</script>'

def facet_bar_html(eng, sec, depth):
    return ('<section class="store"><div class="store-tools">'
            '<input class="search-big" id="q" type="search" placeholder="search this shelf - title, series, developer..." autocomplete="off" aria-label="search input">'
            '<div class="store-sort"><select id="sort" aria-label="sort order">'
            '<option value="name-asc">name A-Z</option><option value="name-desc">name Z-A</option>'
            '<option value="date-desc">date new-old</option><option value="date-asc">date old-new</option>'
            '<option value="size-desc">size big-small</option><option value="size-asc">size small-big</option>'
            '<option value="random">random</option></select>'
            '<button type="button" id="shuf" class="shuf-btn">RANDOM</button></div>'
            '<p class="search-count" id="count">loading the index...</p></div>'
            '<div class="active" id="active"></div>'
            '<div class="facets" id="facets"></div>'
            '<div class="dir" id="out"></div></section>')

def collections_strip(eng, sec, depth):
    cards = []
    for c in eng.collections:
        if c.get("section") != sec:
            continue
        cards.append('<a class="col-card" href="' + rel("", "pages/collection/%s.html" % c["slug"], depth) + '">'
                     '<span class="col-title">' + esc(c["title"]) + '</span>'
                     '<span class="col-cap">' + esc(c.get("caption") or "") + '</span>'
                     '<span class="col-n">' + str(c["n_pages"]) + ' pages</span>'
                     '<span class="dir-go">OPEN &#8594;</span></a>')
    for m in eng.multis:
        cards.append('<a class="col-card col-multi" href="' + rel("", "pages/meta/%s.html" % m["slug"], depth) + '">'
                     '<span class="col-title">' + esc(m["title"]) + '</span>'
                     '<span class="col-cap">' + esc(m.get("caption") or "") + '</span>'
                     '<span class="col-n">' + str(len(m.get("collections") or [])) + ' collections</span>'
                     '<span class="dir-go">OPEN &#8594;</span></a>')
    if not cards:
        return ""
    return '<section><h2 class="sec-title">COLLECTIONS ON THIS SHELF</h2><div class="col-grid">' + "".join(cards) + '</div></section>'

def vocab_script(eng):
    import json as _json
    v = {"g": eng.genres, "tg": eng.tags, "pl": eng.plats,
         "w": {"sex": "sex", "gore": "gore"}}
    return '<script>window.VOCAB=' + _json.dumps(v, ensure_ascii=False) + ';</script>'

def list_page(eng, sec, title, desc, note):
    depth = 1
    counts = eng.sec_counts()
    n = counts[sec]
    if n == 0:
        body = ('<main class="page-wrap"><section><h2 class="sec-title">' + esc(title) + '</h2>'
                '<p class="dir-note">0 pages on this shelf. the engine stands ready - rows, facets, sorts and random come alive the moment the first page lands.</p></section>'
                + collections_strip(eng, sec, depth) + '</main>')
        return (head(title + " — GOODGAMES SURVIVE", desc, depth, 'data-sec="' + sec + '"') +
                topbar(eng, depth, sec) + body + foot_site(depth) + '</body></html>')
    body = ('<main class="page-wrap"><section><h2 class="sec-title">' + esc(title) + '</h2>'
            '<p class="dir-note">' + esc(note) + '</p></section>'
            + facet_bar_html(eng, sec, depth)
            + collections_strip(eng, sec, depth)
            + '</main>')
    html = (head(title + " — GOODGAMES SURVIVE", desc, depth,
                 'data-sec="' + sec + '" data-mode="list" data-index="' + rel("", "data/search-index.json", depth) + '"') +
            topbar(eng, depth, sec) + body + vocab_script(eng) +
            '<script>' + LIST_JS + '</script>' + foot_site(depth) + '</body></html>')
    return html

def search_page(eng):
    depth = 1
    body = ('<main class="page-wrap"><section><h2 class="sec-title">SEARCH THE CATALOGUE</h2>'
            '<input class="search-big" id="q" type="search" placeholder="title, series, developer, genre, tag..." autocomplete="off" aria-label="search input">'
            '<p class="search-count" id="count">loading the index...</p></section>'
            '<div class="active" id="active"></div><div class="dir" id="out"></div></main>')
    html = (head("SEARCH — GOODGAMES SURVIVE", "Search the whole catalogue - every shelf, live, offline, no tracking.", depth,
                 'data-sec="all" data-mode="search" data-index="' + rel("", "data/search-index.json", depth) + '"') +
            topbar(eng, depth, None) + body + vocab_script(eng) + '<script>' + LIST_JS + '</script>' + foot_site(depth) + '</body></html>')
    return html

def random_page(eng):
    depth = 1
    js = ("<script>(function(){fetch('../data/random-manifest.json?v=" + BUILD_V + "')"
          ".then(function(r){return r.json()}).then(function(d){"
          "var i=Math.floor(Math.random()*d.items.length);location.replace('../'+d.items[i].u);})"
          ".catch(function(){location.replace('../pages/games.html')});})();</script>")
    body = ('<main class="page-wrap"><section><h2 class="sec-title">ROLLING THE DICE</h2>'
            '<p class="dir-note">picking one page out of everything that exists - games, software, mods, collections.</p></section></main>')
    return (head("RANDOM — GOODGAMES SURVIVE", "One random page out of everything.", depth) +
            topbar(eng, depth, None) + body + js + foot_site(depth) + '</body></html>')

def main_page(eng):
    depth = 0
    body = ('<main id="top"><section class="hero">'
            '<div class="brand-mark" role="img" aria-label="WASTED - TED struck through, IT written over it">'
            '<span class="mark-word">WAS<span class="mark-ted">TED<span class="mark-it">IT</span></span></span></div>'
            '<p class="hero-caption">a memory no longer buried</p></section></main>')
    return (head("GOODGAMES SURVIVE — a memory no longer buried",
                 "Good games that outlived their era. Downloads, cracks for the un-buyable, mods, patches, upgrade paths.",
                 depth) + topbar(eng, depth, None) + body + foot_site(depth) + '</body></html>')

def collections_page(eng):
    depth = 1
    cards = []
    for c in eng.collections:
        cards.append('<a class="col-card" href="' + rel("", "pages/collection/%s.html" % c["slug"], depth) + '">'
                     '<span class="col-title">' + esc(c["title"]) + '</span>'
                     '<span class="col-cap">' + esc(c.get("caption") or "") + '</span>'
                     '<span class="col-n">' + str(c["n_pages"]) + ' pages</span>'
                     '<span class="dir-go">OPEN &#8594;</span></a>')
    body = ['<main class="page-wrap"><section><h2 class="sec-title">COLLECTIONS</h2>']
    if cards:
        body.append('<div class="col-grid">' + "".join(cards) + '</div>')
    else:
        body.append('<p class="dir-note">no collections yet.</p>')
    body.append('</section>')
    if eng.multis:
        mc = []
        for m in eng.multis:
            mc.append('<a class="col-card col-multi" href="' + rel("", "pages/meta/%s.html" % m["slug"], depth) + '">'
                      '<span class="col-title">' + esc(m["title"]) + '</span>'
                      '<span class="col-cap">' + esc(m.get("caption") or "") + '</span>'
                      '<span class="col-n">' + str(len(m.get("collections") or [])) + ' collections</span>'
                      '<span class="dir-go">OPEN &#8594;</span></a>')
        body.append('<section><h2 class="sec-title">MULTI-COLLECTIONS</h2><div class="col-grid">' + "".join(mc) + '</div></section>')
    body.append('</main>')
    return (head("COLLECTIONS — GOODGAMES SURVIVE", "Collections hold games. Multi-collections hold collections.", depth) +
            topbar(eng, depth, "collections") + "".join(body) + foot_site(depth) + '</body></html>')

def collection_page(eng, c):
    depth = 2
    items, plain = [], []
    for s in c.get("catalogued") or []:
        g = eng.game_by_slug.get(s)
        if not g:
            continue
        plain.append('<div class="dir-row dir-row-plain"><span class="dir-thumb dead"></span><span class="dir-main"><span class="dir-name">' + esc(g["title"]) + '</span><span class="dir-meta">catalogued - no page yet</span></span><span class="dir-go dir-go-dim">IN CATALOGUE</span></div>')
    for s in c["items"]:
        g = eng.game_by_slug.get(s)
        if not g:
            continue
        if s in eng.page_by_slug:
            th = eng.page_by_slug[s].get("thumbnail") or ""
            meta = " · ".join(filter(None, [g.get("release") and str(g["release"])[:4], (g.get("developers") or [""])[0], (g.get("genres") or [""])[0]]))
            items.append('<a class="dir-row" href="' + rel("", "pages/game/%s.html" % s, depth) + '">' +
                         ('<span class="dir-thumb"><img src="' + esc(th) + '" alt="" loading="lazy" onerror="this.parentNode.classList.add(\'dead\');this.remove()"></span>' if th else '<span class="dir-thumb dead"></span>') +
                         '<span class="dir-main"><span class="dir-name">' + esc(g["title"]) + '</span><span class="dir-meta">' + esc(meta) + '</span></span>'
                         '<span class="dir-go">OPEN &#8594;</span></a>')
        else:
            plain.append('<div class="dir-row dir-row-plain"><span class="dir-thumb dead"></span><span class="dir-main"><span class="dir-name">' + esc(g["title"]) + '</span><span class="dir-meta">catalogued - no page yet</span></span><span class="dir-go dir-go-dim">IN CATALOGUE</span></div>')
    body = ['<main class="page-wrap">',
            '<p class="crumb"><a href="' + rel("", "index.html", depth) + '">GOODGAMES SURVIVE</a> / <a href="' + rel("", "pages/collections.html", depth) + '">COLLECTIONS</a> / <b>' + esc(c["title"]) + '</b></p>',
            '<div class="game-title"><h1>' + esc(c["title"]) + '</h1><p class="game-caption">' + esc(c.get("caption") or "") + '</p>',
            '<p class="game-meta">' + str(c["n_pages"]) + ' pages · ' + str(len(c["catalogued"])) + ' catalogued-only</p></div>',
            '<section><h2 class="sec-title">ABOUT THIS COLLECTION</h2>' + "".join('<p class="about-p">' + esc(a) + '</p>' for a in (c.get("about") or [])) + '</section>',
            '<section><h2 class="sec-title">THE SHELF - ' + str(c["n_pages"]) + ' PAGES</h2><div class="dir">' + "".join(items) + '</div></section>']
    if plain:
        body.append('<section><h2 class="sec-title">ALSO IN THE CATALOGUE</h2><div class="dir">' + "".join(plain) + '</div></section>')
    if c.get("notes"):
        body.append('<section><h2 class="sec-title">NOTES</h2>' + "".join('<p class="about-p">' + esc(n) + '</p>' for n in c["notes"]) + '</section>')
    body.append('</main>')
    return (head(c["title"] + " — GOODGAMES SURVIVE", c.get("caption") or c["title"], depth) +
            topbar(eng, depth, "collections") + "".join(body) + foot_page(depth) + '</body></html>')

def meta_page(eng, m):
    depth = 2
    cards = []
    for cs in (m.get("collections") or []):
        c = next((x for x in eng.collections if x["slug"] == cs), None)
        if not c:
            continue
        cards.append('<a class="dir-row" href="' + rel("", "pages/collection/%s.html" % c["slug"], depth) + '">'
                     '<span class="dir-thumb dead"></span>'
                     '<span class="dir-main"><span class="dir-name">' + esc(c["title"]) + '</span><span class="dir-meta">' + str(c["n_pages"]) + ' pages</span></span>'
                     '<span class="dir-go">OPEN &#8594;</span></a>')
    body = ['<main class="page-wrap">',
            '<p class="crumb"><a href="' + rel("", "index.html", depth) + '">GOODGAMES SURVIVE</a> / <a href="' + rel("", "pages/collections.html", depth) + '">COLLECTIONS</a> / <b>' + esc(m["title"]) + '</b></p>',
            '<div class="game-title"><h1>' + esc(m["title"]) + '</h1><p class="game-caption">' + esc(m.get("caption") or "") + '</p></div>',
            '<section><h2 class="sec-title">ABOUT THIS MULTI-COLLECTION</h2>' + "".join('<p class="about-p">' + esc(a) + '</p>' for a in (m.get("about") or [])) + '</section>',
            '<section><h2 class="sec-title">COLLECTIONS INSIDE</h2><div class="dir">' + "".join(cards) + '</div></section>',
            '</main>']
    return (head(m["title"] + " — GOODGAMES SURVIVE", m.get("caption") or m["title"], depth) +
            topbar(eng, depth, "collections") + "".join(body) + foot_page(depth) + '</body></html>')

def redirect_page(eng, r, sec):
    depth = 2 if sec == "games" else 2
    target = rel("", "pages/game/%s.html" % r["to"], depth) if sec == "games" else r["to"]
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta http-equiv="refresh" content="0; url=' + esc(target) + '">'
            '<link rel="canonical" href="' + esc(target) + '"><title>redirecting...</title></head>'
            '<body><p class="crumb" style="padding:40px">this name is an alias - <a href="' + esc(target) + '">go to the real page</a></p></body></html>')
