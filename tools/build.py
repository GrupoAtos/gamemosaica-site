#!/usr/bin/env python3
"""Gera as páginas do gamemosaica.com em 8 idiomas.
Uso: python3 tools/build.py   (a partir da raiz do repositório)
pt-BR fica na raiz; os outros idiomas em /en/, /es/, /fr/, /de/, /it/, /ja/, /zh/.
"""
import json, os, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from textos import T, LANGS, HTML_LANG, LANG_NAME, EMAIL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STORIES = json.load(open(os.path.join(os.path.dirname(__file__), "historias-clas.json")))
CLANS = ["brasa", "mare", "raiz", "geada", "duna", "vento", "fera", "lume", "automato", "astro", "espectro", "colosso"]
SPECIAL = {"automato", "astro", "espectro", "colosso"}
COLOR = {"brasa": "#ef7f5e", "mare": "#45c2d1", "raiz": "#7fcf68", "geada": "#a7b4ff", "duna": "#f0c04f", "vento": "#e08ad0",
         "fera": "#b5703f", "lume": "#f3e3a2", "automato": "#9aa7b8", "astro": "#b6f24a", "espectro": "#8c6cf0", "colosso": "#c2506e"}
FEAT_COL = ["--c1", "--c2", "--c3", "--c4", "--c5", "--c6"]
PAGES = ["", "clas/", "suporte/", "privacidade/", "termos/"]
SITE = "https://gamemosaica.com"


def base(l):
    return "/" if l == "pt" else f"/{l}/"


def url(l, page):
    return base(l) + page


def head(l, page, title, desc, extra=""):
    alts = "\n".join(f'<link rel="alternate" hreflang="{HTML_LANG[x]}" href="{SITE}{url(x, page)}">' for x in LANGS)
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{url("pt", page)}">'
    return f'''<!doctype html>
<html lang="{HTML_LANG[l]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#141236">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{SITE}/img/og.jpg">
<meta property="og:url" content="{SITE}{url(l, page)}">
<meta property="og:type" content="website">
<link rel="canonical" href="{SITE}{url(l, page)}">
{alts}
<link rel="icon" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css">
{extra}</head>
<body>'''


def header(l, page, current):
    t = T[l]
    def a(p, label):
        cur = ' aria-current="page"' if p == current else ""
        return f'<a href="{url(l, p)}"{cur}>{label}</a>'
    opts = "".join(f'<option value="{url(x, page)}"{" selected" if x == l else ""} lang="{HTML_LANG[x]}">{LANG_NAME[x]}</option>' for x in LANGS)
    return f'''<div class="wrap">
  <header class="top">
    <a class="brand" href="{base(l)}"><img src="/img/icone.webp" alt=""><span>MOSAICA</span></a>
    <nav class="top"><a href="/jogar/">{t["nav_play"]}</a>{a("clas/", t["nav_clans"])}{a("suporte/", t["nav_support"])}
      <label class="lang-pick"><span class="sr">{t["lang_label"]}</span><select aria-label="{t["lang_label"]}" onchange="try{{localStorage.setItem('site-idioma',this.options[this.selectedIndex].lang)}}catch(e){{}};location.href=this.value">{opts}</select></label></nav>
  </header>'''


def footer(l):
    t = T[l]
    return f'''</div>
<footer><div class="wrap">
  <a href="/jogar/">{t["nav_play"]}</a><a href="{url(l, "clas/")}">{t["nav_clans"]}</a><a href="{url(l, "suporte/")}">{t["nav_support"]}</a><a href="{url(l, "privacidade/")}">{t["nav_privacy"]}</a><a href="{url(l, "termos/")}">{t["nav_terms"]}</a>
  <div style="margin-top:10px">© 2026 Paulo Ricardo Pereira Serra</div>
</div></footer>
</body>
</html>
'''


REDIRECT = '''<script>
(function(){try{
  var map={pt:'/',en:'/en/',es:'/es/',fr:'/fr/',de:'/de/',it:'/it/',ja:'/ja/',zh:'/zh/'};
  var saved=null;try{saved=localStorage.getItem('site-idioma')}catch(e){}
  if(saved){return;}
  var l=(navigator.languages&&navigator.languages[0]||navigator.language||'pt').toLowerCase().slice(0,2);
  if(l!=='pt'&&map[l]&&location.pathname==='/'&&!/[?&]lang=pt/.test(location.search))location.replace(map[l]);
}catch(e){}})();
</script>
'''


def home(l):
    t = T[l]
    feats = "\n".join(f'      <div class="card"><h3><span class="dot" style="background:var({FEAT_COL[i]})"></span>{h}</h3><p>{p}</p></div>' for i, (h, p) in enumerate(t["f"]))
    extra = REDIRECT if l == "pt" else ""
    return head(l, "", t["title"], t["meta"], extra) + header(l, "", "") + f'''

  <div class="hero">
    <div>
      <h1 class="title">MOSAICA</h1>
      <div class="tag">{t["tagline"]}</div>
      <p class="lead">{t["lead"]}</p>
      <div class="badges">
        <a class="btn primary" href="/jogar/">{t["btn_play"]}</a>
        <a class="btn ghost" href="{url(l, "clas/")}">{t["btn_clans"]}</a>
      </div>
      <p class="soon">{t["soon"]}</p>
    </div>
    <div class="phones">
      <img src="/img/inicio.webp" width="390" height="844" alt="{t["alt_home"]}">
      <img src="/img/jogo.webp" width="390" height="844" alt="{t["alt_game"]}">
    </div>
  </div>

  <section>
    <div class="grid">
{feats}
    </div>
  </section>
''' + footer(l)


def clans(l):
    t = T[l]
    cards = []
    for k in CLANS:
        s = STORIES[k][l]
        tag = f'<span class="badge">{t["special"]}</span>' if k in SPECIAL else ""
        cards.append(f'''    <article class="clan" id="{k}" style="--clan:{COLOR[k]}">
      <h2><span class="dot" style="background:{COLOR[k]}"></span>{html.escape(s["nome"])}{tag}</h2>
      <p class="cap">{t["capital"]}: {html.escape(s["capital"])}</p>
      <p>{html.escape(s["historia"])}</p>
    </article>''')
    return head(l, "clas/", f'{t["clans_title"]} · Mosaica', t["clans_meta"]) + header(l, "clas/", "clas/") + f'''

  <main class="doc wide">
    <h1>{t["clans_title"]}</h1>
    <p class="meta">{t["clans_lead"]}</p>
    <div class="clans">
{chr(10).join(cards)}
    </div>
    <p style="margin-top:28px"><a class="btn primary" href="/jogar/">{t["clans_cta"]}</a></p>
  </main>
''' + footer(l)


def support(l):
    t = T[l]
    subj = t["mail_subject"].replace(" ", "%20")
    faq = "\n".join(f'    <details><summary>{q}</summary><p>{a}</p></details>' for q, a in t["faq"])
    return head(l, "suporte/", f'{t["sup_title"]} · Mosaica', t["sup_meta"]) + header(l, "suporte/", "suporte/") + f'''

  <main class="doc">
    <h1>{t["sup_title"]}</h1>
    <p class="meta">{t["sup_lead"]}</p>

    <div class="box">
      <strong>{t["sup_email"]}:</strong> <a href="mailto:{EMAIL}?subject={subj}">{EMAIL}</a><br>
      {t["sup_reply"]}
    </div>

    <h2>{t["faq_title"]}</h2>
{faq}
  </main>
''' + footer(l)


def legal(l, page, title, meta, summary, sections):
    t = T[l]
    body = "\n".join(f'    <h2>{h}</h2>\n    <p>{p.replace("{priv}", url(l, "privacidade/"))}</p>' for h, p in sections)
    return head(l, page, f'{title} · Mosaica', meta) + header(l, page, page) + f'''

  <main class="doc">
    <h1>{title}</h1>
    <p class="meta">{t["updated"]}</p>

    <div class="box">{summary}</div>

{body}

    <h2>{t["contact"]}</h2>
    <p><a href="mailto:{EMAIL}?subject=Mosaica">{EMAIL}</a></p>
  </main>
''' + footer(l)


def notfound():
    l = "pt"; t = T[l]
    links = " · ".join(f'<a href="{base(x)}" lang="{HTML_LANG[x]}">{T[x]["nf_back"]}</a>' for x in LANGS)
    return head(l, "", f'{t["nf_title"]} · Mosaica', t["nf_text"]) + header(l, "", "") + f'''

  <main class="doc">
    <h1>{t["nf_title"]} · {T["en"]["nf_title"]}</h1>
    <p>{t["nf_text"]} {T["en"]["nf_text"]}</p>
    <p class="lang">{links}</p>
  </main>
''' + footer(l)


def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


for l in LANGS:
    b = "" if l == "pt" else f"{l}/"
    t = T[l]
    write(b + "index.html", home(l))
    write(b + "clas/index.html", clans(l))
    write(b + "suporte/index.html", support(l))
    write(b + "privacidade/index.html", legal(l, "privacidade/", t["priv_title"], t["priv_meta"], t["priv_summary"], t["priv"]))
    write(b + "termos/index.html", legal(l, "termos/", t["terms_title"], t["terms_meta"], t["terms_summary"], t["terms"]))
write("404.html", notfound())

# sitemap
urls = "\n".join(f"  <url><loc>{SITE}{url(l, p)}</loc></url>" for l in LANGS for p in PAGES)
write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n  <url><loc>{SITE}/jogar/</loc></url>\n</urlset>\n')
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("ok:", len(LANGS) * len(PAGES) + 1, "páginas")
