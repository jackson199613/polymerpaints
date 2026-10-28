#!/usr/bin/env python3
"""Static site generator for polymerpaints.com. Run from repo root: python3 build/build.py"""
import json, os, re, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_site import SYS, FINISHES, IND, DIST, STATS, IND_PHOTOS
from content_i18n import T as I18N
IMG2 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img2_sizes.json')))
IMG2.update(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img_real.json'))))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://polymerpaints.com'
CSS = '/assets/css/polymer-v12.css'
JS = '/assets/js/polymer-v3.js'
TEL = '+86 596 2600611'
EMAIL = 'sales@polymerpaints.com'
WA = [('+86 158 2472 9376', '8615824729376'), ('+86 188 5021 3808', '8618850213808')]
WA_MSG = 'Hello%20POLYMER%2C%20I%27m%20interested%20in%20your%20powder%20coatings.'
WA_ICON = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.23 8.23 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.18 8.18 0 0 1 2.41 5.83c0 4.54-3.7 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.17.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.85-.2-.48-.41-.42-.56-.43h-.48a.92.92 0 0 0-.67.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.02 2.56.12.17 1.75 2.67 4.24 3.74.59.26 1.05.41 1.41.52.6.19 1.14.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>'


def wa_link(i=0):
    return f'https://wa.me/{WA[i][1]}?text={WA_MSG}'
ADDR = 'No. 2 Zhuli Road, Xiangcheng District, Zhangzhou, Fujian, China'
E = html.escape
GEO = json.load(open(os.path.join(ROOT, 'build/content_geo.json')))
GEO['faq'] += json.load(open(os.path.join(ROOT, 'build/content_faq2.json')))
_FAQ_META = {  # category + source page for the original 15 answers
    'which-powder-system-outdoor-indoor': ('products', ['Products', '/products/']), 'can-hybrid-powder-be-used-outdoors': ('products', ['Hybrid', '/products/hybrid/']),
    'why-epoxy-yellows-indoor-only': ('products', ['Epoxy', '/products/epoxy/']), 'when-to-use-low-cure-powder': ('products', ['Low-cure grades', '/products/#cure']),
    'colour-matching-ral-or-sample': ('colour', ['Colours & finishes', '/finishes/']), 'available-finishes-and-effects': ('colour', ['Colours & finishes', '/finishes/']),
    'what-is-bonded-metallic-powder': ('colour', ['Metallic finishes', '/finishes/#metallic']), 'approved-panel-version-repeat-orders': ('colour', ['Quality & testing', '/quality/']),
    'minimum-order-quantity': ('orders', ['Contact', '/contact/']), 'powder-coating-lead-time': ('orders', ['About POLYMER', '/company/']),
    'what-qualicoat-class-1-covers': ('quality', ['Quality & certificates', '/quality/']), 'in-house-testing-scope-and-limits': ('quality', ['Quality & testing', '/quality/']),
    'documents-available-tds-sds-certificates': ('quality', ['Downloads', '/downloads/']), 'how-to-request-a-sample': ('samples', ['Request a sample', '/request-sample/']),
    'distributor-cooperation-terms': ('distributors', ['Distributors', '/distributors/'])}
for _f in GEO['faq']:
    if _f['slug'] in _FAQ_META: _f['cat'], _f['src'] = _FAQ_META[_f['slug']]
FAQ_CATS = [('products', 'Products & systems'), ('colour', 'Colour, gloss & effects'), ('orders', 'Orders, supply & shipping'), ('quality', 'Certificates & quality'),
            ('samples', 'Samples & trials'), ('company', 'Company & export'), ('distributors', 'Distributors & importers')]
PAGES = []  # (path, title) for sitemap
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
INDMAP = {i['slug']: i for i in IND}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org",
       "name": "POLYMER", "legalName": "Fujian Polymer Industry & Trade Co., Ltd.", "alternateName": "玻利玛",
       "url": BASE + "/", "logo": BASE + "/assets/img/logo-mark.svg", "foundingDate": "2019-04-22", "taxID": "91350602MA32PFWW73", "telephone": TEL, "email": EMAIL, "contactPoint": [{"@type": "ContactPoint", "contactType": "sales", "telephone": t, "email": EMAIL, "availableLanguage": ["English", "Chinese"]} for t in ["+86-158-2472-9376", "+86-188-5021-3808"]],
       "slogan": "You apply powder, we apply care.",
       "address": {"@type": "PostalAddress", "streetAddress": "No. 2 Zhuli Road, Xiangcheng District", "addressLocality": "Zhangzhou", "addressRegion": "Fujian", "postalCode": "363005", "addressCountry": "CN"},
       "description": "Manufacturer of epoxy, polyester and epoxy-polyester hybrid powder coatings for metal finishing, with a Qualicoat Class 1 approved polyester system.",
       "hasCredential": [
           {"@type": "EducationalOccupationalCredential", "name": "Qualicoat Class 1 approval, polyester system PLM100611", "identifier": "P-2199", "validUntil": "2026-12-31"},
           {"@type": "EducationalOccupationalCredential", "name": "ISO 9001:2015 quality management system", "identifier": "05326Q01777R001", "validUntil": "2029-10-11", "recognizedBy": {"@type": "Organization", "name": "Beijing NGV Certification Center Co., Ltd."}},
           {"@type": "EducationalOccupationalCredential", "name": "ISO 14001:2015 environmental management system", "identifier": "05326E01349R001", "validUntil": "2029-10-11", "recognizedBy": {"@type": "Organization", "name": "Beijing NGV Certification Center Co., Ltd."}}],
       "award": ["National High-Tech Enterprise (China)", "Fujian Province Specialised, Refined, Distinctive and Innovative SME", "Fujian Province Innovative SME", "Science and Technology-based SME"]}


def img(name, w, h, alt, sizes='100vw', small=None, lazy=True, cls=''):
    small = small or (IMG2[name][2] if name in IMG2 else (600 if w > 900 else 400))
    srcset = f'/assets/img/{name}-{small}.webp {small}w, /assets/img/{name}.webp {w}w'
    return (f'<img{" class=%s" % cls if cls else ""} src="/assets/img/{name}-{small}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}"{" loading=lazy" if lazy else " fetchpriority=high"} alt="{E(alt)}">')


LANG_ALT = {'/': 'en', '/ru/': 'ru', '/es/': 'es'}


def head(title, desc, path, ld=None, og='/assets/img/home/og.jpg', extra='', lang='en'):
    if path in LANG_ALT:
        extra = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{u}">\n' for u, l in LANG_ALT.items()) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/">\n' + extra
    lds = [ORG] + (ld or [])
    if path != '/':
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
        parts = [p for p in path.strip('/').split('/') if p]
        acc = ''
        for i, p in enumerate(parts):
            acc += '/' + p
            crumbs.append({"@type": "ListItem", "position": i + 2, "name": p.replace('-', ' ').title(), "item": BASE + acc + '/'})
        lds.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs})
    ldtxt = '\n'.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{BASE}{og}">
<meta property="og:url" content="{BASE}{path}">
<meta name="theme-color" content="#121416">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/instrument-serif-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{CSS}">
{extra}{ldtxt}
</head>
<body>'''


NAV_PRODUCTS = [('Polyester', '/products/polyester/', 'Outdoor'), ('Hybrid', '/products/hybrid/', 'Indoor · decorative'), ('Epoxy', '/products/epoxy/', 'Indoor · functional')]


def header(active=''):
    def cur(k): return ' aria-current="page"' if active == k else ''
    prod = ''.join(f'<a href="{u}">{n}</a>' for n, u, _ in NAV_PRODUCTS)
    inds = ''.join(f'<a href="/industries/{i["slug"]}/">{E(i["short"])}</a>' for i in IND) + '<a href="/distributors/">Powder distributors</a>'
    mob_inds = inds
    return f'''
<a class="hp" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <div class="l"><span class="lng"><a href="/" hreflang="en">EN</a><a href="/ru/" hreflang="ru" lang="ru">RU</a><a href="/es/" hreflang="es" lang="es">ES</a></span><span>Qualicoat Class 1 polyester system</span><span>ISO 9001</span><span>ISO 14001</span></div>
  <div class="r"><span>MOQ 1,000 kg</span><span>Lead time within 10 days</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span><span><a href="tel:+865962600611">{TEL}</a></span></div>
</div></div>
<header class="site"><div class="wrap">
  <a class="logo" href="/" aria-label="POLYMER home"><img src="/assets/img/logo-mark-dark.svg" width="30" height="35" alt=""><b>POLYMER</b><small>Powder coatings</small></a>
  <nav class="main" aria-label="Main">
    <div class="dd"><a href="/products/"{cur('products')}>Products</a><div class="menu wide"><div><small>By system</small>{prod}<a href="/products/#cure">Low-cure grades</a></div><div><small>Choose &amp; compare</small><a href="/finishes/">Colours &amp; finishes</a><a href="/selector/">System selector</a><a href="/selector/#matrix">Industry × system table</a></div></div></div>
    <div class="dd"><a href="/industries/"{cur('industries')}>Industries</a><div class="menu"><small>By application</small>{inds}</div></div>
    <a href="/finishes/"{cur('finishes')}>Finishes</a>
    <a href="/distributors/"{cur('distributors')}>Distributors</a>
    <a href="/quality/"{cur('quality')}>Quality</a>
    <a href="/faq/"{cur('faq')}>FAQ</a>
    <div class="dd"><a href="/how-to/"{cur('resources')}>Resources</a><div class="menu"><a href="/how-to/">How-to guides</a><a href="/downloads/">Downloads</a><a href="/selector/">System selector</a><a href="/faq/">FAQ · 40 answers</a></div></div>
    <a href="/company/"{cur('company')}>Company</a>
    <a href="/contact/"{cur('contact')}>Contact</a>
  </nav>
  <a class="btn btn-primary hdr-cta" href="/request-sample/">Request a sample</a>
  <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
</div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">
  <h4>Products</h4><a href="/products/">All products</a>{prod}<a href="/finishes/">Colours &amp; finishes</a><a href="/selector/">System selector</a>
  <h4>Industries</h4>{mob_inds}
  <h4>FAQ</h4><a href="/faq/">FAQ · 40 answers</a>
  <h4>Language</h4><a href="/">English</a><a href="/ru/" lang="ru">Русский</a><a href="/es/" lang="es">Español</a>
  <h4>Company</h4><a href="/quality/">Quality &amp; certificates</a><a href="/company/">About POLYMER</a><a href="/faq/">Technical FAQ</a><a href="/how-to/">How-to guides</a><a href="/downloads/">Downloads</a><a href="/contact/">Contact</a>
  <a class="btn btn-primary" href="/request-sample/">Request a sample</a>
</nav>
<main id="main">'''


def footer():
    inds = ''.join(f'<li><a href="/industries/{i["slug"]}/">{E(i["short"])}</a></li>' for i in IND)
    return f'''</main>
<footer><div class="wrap">
  <div><a class="logo" href="/"><img src="/assets/img/logo-mark-dark.svg" width="30" height="35" alt=""><b style="color:#fff">POLYMER</b><small>Powder coatings</small></a>
    <p class="slogan">You apply powder,<br>we apply care.</p>
    <p>Fujian Polymer Industry &amp; Trade Co., Ltd.<br>No. 2 Zhuli Road, Xiangcheng District,<br>Zhangzhou, Fujian 363005, China<br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:+865962600611">Tel {TEL}</a><br>WhatsApp <a href="{wa_link(0)}" rel="noopener">{WA[0][0]}</a> · <a href="{wa_link(1)}" rel="noopener">{WA[1][0]}</a></p></div>
  <div><h4>Products</h4><ul><li><a href="/products/polyester/">Polyester</a></li><li><a href="/products/hybrid/">Hybrid</a></li><li><a href="/products/epoxy/">Epoxy</a></li><li><a href="/finishes/">Colours &amp; finishes</a></li><li><a href="/selector/">System selector</a></li></ul></div>
  <div><h4>Industries</h4><ul>{inds}<li><a href="/distributors/">Distributors</a></li></ul></div>
  <div><h4>Company</h4><ul><li><a href="/company/">About POLYMER</a></li><li><a href="/quality/">Quality &amp; certificates</a></li><li><a href="/faq/">Technical FAQ</a></li><li><a href="/how-to/">How-to guides</a></li><li><a href="/downloads/">Downloads</a></li><li><a href="/contact/">Contact</a></li><li><a href="/request-sample/">Request a sample</a></li></ul></div>
  <div class="f-bottom"><span>© 2026 Fujian Polymer Industry &amp; Trade Co., Ltd. · <a href="/privacy/">Privacy &amp; cookies</a></span><span>USCC 91350602MA32PFWW73 · Product data apply to stated conditions. Certificates apply to the scope stated on each certificate.</span></div>
</div></footer>
<details class="wa-float"><summary aria-label="Chat on WhatsApp">{WA_ICON}<span>WhatsApp</span></summary><div class="wa-pop"><p>Chat with our sales team<small>Reply within one working day · UTC+8</small></p><a href="{wa_link(0)}" target="_blank" rel="noopener">{WA_ICON}<span><b>Sales</b>{WA[0][0]}</span></a><a href="{wa_link(1)}" target="_blank" rel="noopener">{WA_ICON}<span><b>Sales</b>{WA[1][0]}</span></a></div></details>
<script src="{JS}" defer></script>
</body>
</html>'''


def cta(title='Send us your most-used colour <em>and your hardest one.</em>', text='Tell us the part, environment, process and expected volume. We reply with a proposed system and a sample plan. Orders from 1,000 kg.', btn=('Send project details', '/contact/'), btn2=('Request a sample', '/request-sample/')):
    return f'''
<section class="cta" aria-label="Start a project">
  {bgimg('cta-red')}
  <div class="wrap">
    <p class="eyebrow" style="color:#d9b0ab">Start a project</p>
    <h2 class="h2">{title}</h2>
    <p>{E(text)}</p>
    <div class="hero-ctas" style="margin-top:0"><a class="btn btn-primary" href="{btn[1]}">{btn[0]} {ARROW}</a><a class="btn btn-line" href="{btn2[1]}">{btn2[0]}</a></div>
  </div>
</section>'''


PH_BG = {'Industries': 'industries', 'System selector': 'selector', 'Contact': 'contact', 'FAQ': 'resources', 'How-to guides': 'resources', 'How-to': 'resources'}


def phero(crumbs, h1, lead, figure='', facts=None, ctas=None, bg=None):
    if bg is None and not figure:
        names = [n for n, u in crumbs]
        bg = next((PH_BG[n] for n in names if n in PH_BG and (n != 'Industries' or len(crumbs) == 1)), None)
    cr = '<a href="/">Home</a>' + ''.join((f'<a href="{u}">{E(n)}</a>' if u else f'<span>{E(n)}</span>') for n, u in crumbs)
    fx = ('<div class="facts">' + ''.join(f'<span>{E(f)}</span>' for f in facts) + '</div>') if facts else ''
    ct = ''
    if ctas:
        ct = '<div class="hero-ctas">' + ''.join(f'<a class="btn {c}" href="{u}">{t}{" " + ARROW if c == "btn-primary" else ""}</a>' for t, u, c in ctas) + '</div>'
    return f'''
<section class="phero{' has-img' if figure else ''}{' has-bg' if bg else ''}">{bgimg(bg, lazy=False) if bg else ''}
  <div class="wrap">
    <div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><h1>{h1}</h1><p class="lead">{lead}</p>{fx}{ct}</div>
    {figure}
  </div>
</section>'''


def write(path, title, desc, body, active='', ld=None, og='/assets/img/home/og.jpg', sitemap=True, extra_head='', pre='', lang='en'):
    out = head(title, desc, path, ld, og, extra_head + ('' if sitemap else '<meta name="robots" content="noindex">\n'), lang) + pre + header(active) + body + footer()
    fp = os.path.join(ROOT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(out)
    if sitemap: PAGES.append((path, title))


def bgimg(name, lazy=True):
    sm = 640 if name == 'cta-red' else 960
    w, h = (1024, 1024) if name == 'cta-red' else (1916, 821)
    return (f'<img class="bg-img bg-{name}" src="/assets/img/bg/{name}-{sm}.webp" srcset="/assets/img/bg/{name}-{sm}.webp {sm}w, /assets/img/bg/{name}.webp {w}w" '
            f'sizes="100vw" width="{w}" height="{h}" alt=""{" loading=lazy" if lazy else " fetchpriority=high"}>')


def fig2(name, alt, cap):
    w, h, sm = IMG2[name]
    return f'<figure class="figure rv">{img(name, w, h, alt, "(min-width:1280px) 1192px, 100vw", sm)}<figcaption><b>{E(cap[0])}.</b> {E(cap[1])}</figcaption></figure>'


def photos(items, cls='c3'):
    figs = ''.join(f'<figure class="rv">{img(n, IMG2[n][0], IMG2[n][1], alt, "(min-width:1060px) 25vw, 50vw", IMG2[n][2])}<figcaption>{E(cap)}</figcaption></figure>' for n, alt, cap in items)
    return f'<div class="photos {cls}">{figs}</div>'


def chips(main, opt, extra=None):
    s = ''.join(f'<span class="chip main">{SYS[m]["name"]}</span>' for m in main)
    s += ''.join(f'<span class="chip">{SYS[o]["name"]}</span>' for o in opt)
    if extra: s += f'<span class="chip">{extra}</span>'
    return f'<div class="chips">{s}</div>'


def faq_block(slugs, dark=False):
    items = [f for f in GEO['faq'] if f['slug'] in slugs]
    out = '<div class="faq">'
    for f in items:
        body = ''.join(f'<p>{E(p)}</p>' for p in f['body'])
        out += f'<details id="{f["slug"]}"><summary>{E(f["q"])}</summary><div class="a"><p class="short">{E(f["short"])}</p>{body}<p class="basis">Basis: {E(f["basis"])}{f' · <a href="{f["src"][1]}">{E(f["src"][0])} →</a>' if f.get("src") else ''}</p></div></details>'
    return out + '</div>'


# ---------------------------------------------------------------- home
def build_home():
    src = open(os.path.join(ROOT, 'build/home_main.html')).read()
    src = src.replace('{{PHOTOS}}', photos([('real/extruder', 'Twin-screw powder coating extruder with cooling belt', 'Melt extrusion'), ('real/bonding', 'Metallic bonding machine', 'Metallic bonding'),
                                             ('real/gloss', '60° gloss measurement on a green panel', '60° gloss check'), ('real/particle', 'Loading powder into the laser particle size analyser', 'Particle size')], 'c4'))
    lp = json.load(open(os.path.join(ROOT, 'build/logo_paths.json')))
    word = ''.join(f'<span style="transition-delay:{.06 * i:.2f}s">{c}</span>' for i, c in enumerate('POLYMER'))
    lay = ''.join(f'<div class="pi-l pi-{k}" data-src="/assets/img/intro/{k}.webp" data-sm="/assets/img/intro/{k}-{sm}.webp"></div>' for k, sm in [('charge', 900), ('burst', 640), ('melt', 900), ('palette', 900), ('panels', 640)])
    intro = f'''<div id="pi" data-s="0">
<div aria-hidden="true">{lay}<canvas></canvas><div class="pi-fl"></div><div class="pi-sweep"></div><div class="pi-vig"></div><div class="pi-grain"></div><div class="pi-lb t"></div><div class="pi-lb b"></div>
<div class="pi-brand"><img src="/assets/img/logo-mark-dark.svg" alt="">POLYMER<small>Powder coatings · Since 2019</small></div>
<svg class="pi-mark" viewBox="{lp['vb']}"><path class="b" pathLength="1" fill-rule="evenodd" d="{lp['blue']}"/><path class="r" pathLength="1" fill-rule="evenodd" d="{lp['red']}"/></svg>
<div class="pi-word"><b>{word}</b><em>You apply powder, <i>we apply care.</i></em><small>Epoxy · Polyester · Hybrid powder coatings · Zhangzhou, China</small></div>
<div class="pi-cap"></div><div class="pi-bar"><i></i></div></div>
<button class="pi-skipb" type="button">Skip intro</button>
</div>
'''
    hs = ('<script>(function(){try{var r=document.documentElement,f=/[?&]intro=1\\b/.test(location.search),s=false,m=false;'
          'try{s=sessionStorage.getItem("pl-intro")==="1"}catch(e){}try{m=matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){}'
          'if(f||(!s&&!m))r.classList.add("pi-on")}catch(e){}})()</script>\n'
          '<link rel="preload" as="image" href="/assets/img/intro/charge.webp" media="(min-width:760px)">\n'
          '<script src="/assets/js/intro-v1.js" defer></script>\n')
    write('/', 'POLYMER Powder Coatings | Epoxy, Polyester & Hybrid Powder Coatings, China',
          'Fujian Polymer manufactures epoxy, polyester and epoxy-polyester hybrid powder coatings for metal finishing, with a Qualicoat Class 1 approved polyester system, colour matching, special finishes and lead times within 10 days.',
          src, ld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "POLYMER Powder Coatings", "url": BASE + "/"}], extra_head=hs, pre=intro)


# ---------------------------------------------------------------- products
def build_products():
    cards = ''
    for k, s in SYS.items():
        cards += f'<a class="card rv" href="{s["url"]}"><small>{s["env"]}</small><h3>{s["name"]}{"<span class=badge>Qualicoat</span>" if k == "polyester" else ""}</h3><p>{E(s["lead"])}</p><span class="link">{s["name"]} range</span></a>'
    body = phero([('Products', None)], 'Three systems, <em>chosen by environment.</em>',
                 'Polyester for outdoor parts, hybrid for indoor decorative parts and epoxy for indoor functional parts. Every system comes in RAL and custom colours, three gloss bands, ten surface effects, and standard or low-cure grades.',
                 figure=f'<figure>{img("home/gloss-trio", 1536, 1024, "Three anthracite powder-coated panels in dead matt, satin and high gloss", "(min-width:980px) 45vw, 100vw", 768, lazy=False)}</figure>',
                 facts=['Standard & low-cure', 'RAL & custom colours', 'MOQ 1,000 kg', 'Lead time ≤ 10 days'],
                 ctas=[('Use the selector', '/selector/', 'btn-primary'), ('Request a sample', '/request-sample/', 'btn-line')])
    body += f'<section class="sec"><div class="wrap"><div class="cards c3">{cards}</div></div></section>'
    rows = ''
    for k, s in SYS.items():
        rows += f'<tr><td><b>{s["name"]}</b></td><td>{s["env"]}</td><td>{E("; ".join(s["props"][:3]))}</td><td>{E(s["parts"].split(",")[0] + ", " + s["parts"].split(",")[1].strip())} …</td></tr>'
    body += f'''<section class="sec tight alt"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Compare</p><h2 class="h2">The three systems <em>side by side.</em></h2></div><p class="lead">The environment decides the chemistry. Final suitability is confirmed on your part and line.</p></div>
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>System</th><th>Environment</th><th>Key properties (catalogue)</th><th>Typical parts</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="tbl-note">Epoxy and hybrid are for indoor use. Qualicoat Class 1 applies to polyester system PLM100611 only.</p>
</div></section>
<section class="sec tight" id="cure"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Shared across all systems</p><h2 class="h3" style="margin-top:20px">Cure, gloss, colour <em>and powder.</em></h2></div>
  <div class="rv"><dl class="kv">
    <dt>Cure grades</dt><dd>Standard cure and low-cure grades in every system. Low-cure is considered for lines that need a lower oven temperature or faster line speed; it is confirmed against your actual oven profile. Cure conditions are on each product’s TDS.</dd>
    <dt>Gloss</dt><dd>High gloss ≥ 90 · satin and matt 11–80 · dead matt ≤ 10, as specified by you.</dd>
    <dt>Effects</dt><dd>Smooth, sand, wrinkle, vein, fine texture, hammer tone, pattern, metallic, transparent or translucent, fluorescent. <a class="link" href="/finishes/">See finishes</a></dd>
    <dt>Colour</dt><dd>RAL and customer-specified colours, matched from a colour code or a physical sample.</dd>
    <dt>Powder (polyester catalogue)</dt><dd>Specific gravity 1.4–1.8 g/cm³ depending on colour and gloss · average particle size 30–38 µm · more than 90% of particles between 10 and 84 µm; adjustable on request.</dd>
    <dt>Supply</dt><dd>Minimum order 1,000 kg · standard lead time within 10 days; complex custom colours and large volumes confirmed per order.</dd>
  </dl></div>
</div></section>'''
    body += cta()
    write('/products/', 'Powder Coating Products: Polyester, Hybrid & Epoxy | POLYMER',
          'Polyester for outdoor parts, epoxy-polyester hybrid for indoor decorative parts and epoxy for indoor functional parts, in RAL and custom colours, ten effects and standard or low-cure grades.', body, 'products')

    for k, s in SYS.items():
        w, h = s['imgw']
        fig = f'<figure class="{"tall" if s["tall"] else ""}">{img(s["img"], w, h, s["name"] + " powder coating", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>'
        props = ''.join(f'<li><span>{i+1:02d}</span><div>{E(p)}</div></li>' for i, p in enumerate(s['props']))
        indcards = ''.join(f'<a class="ind rv" href="/industries/{x}/"><figure>{img(INDMAP[x]["img"], *INDMAP[x]["imgw"], INDMAP[x]["name"], "(min-width:1060px) 25vw, (min-width:640px) 50vw, 100vw")}</figure><span class="n">{INDMAP[x]["n"]}</span><h3>{E(INDMAP[x]["short"])}</h3></a>' for x in s['inds'] if x in INDMAP)
        extra = ''
        if k == 'polyester':
            extra = '''<section class="sec dark qc-band">''' + bgimg('qualicoat') + '''<div class="wrap"><div class="qc-in">
  <div class="rv"><p class="eyebrow">Architectural approval</p><h2 class="h3" style="margin-top:20px;color:#fff">Qualicoat Class 1, <em style="color:var(--accent-hi)">with its scope.</em></h2></div>
  <div class="rv"><dl class="kv" style="border-color:var(--night-line)">
   <dt>Licence</dt><dd style="color:#e8eaec">P-2199</dd><dt>System</dt><dd style="color:#e8eaec">Polyester PLM100611, gloss category 3</dd><dt>Valid</dt><dd style="color:#e8eaec">Until 31 December 2026</dd><dt>Scope</dt><dd style="color:#e8eaec">The approved polyester system only. Not all products or colours; no structured-texture or metallic extension; not Class 2 or Class 3.</dd></dl>
   <p class="mt24"><a class="link" href="/quality/">Quality &amp; certificates</a></p></div></div></div></section>'''
        faqs = {'polyester': ['which-powder-system-outdoor-indoor', 'what-qualicoat-class-1-covers'],
                'hybrid': ['can-hybrid-powder-be-used-outdoors', 'which-powder-system-outdoor-indoor'],
                'epoxy': ['why-epoxy-yellows-indoor-only', 'which-powder-system-outdoor-indoor']}[k]
        body = phero([('Products', '/products/'), (s['name'], None)], s['h1'], E(s['lead']), figure=fig,
                     facts=[s['env'], 'Standard & low-cure', 'Ten effects', 'MOQ 1,000 kg'],
                     ctas=[(f'Request a {s["name"].lower()} sample', f'/request-sample/?system={s["name"]}', 'btn-primary'), ('Ask for the TDS', '/downloads/', 'btn-line')])
        body += f'''<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Properties</p><h2 class="h3" style="margin-top:20px">What {s["name"].lower()} <em>is good at.</em></h2><p class="prose mt24">Typical properties from our product catalogue. Values for each grade are on its technical data sheet.</p></div>
  <div class="rv"><ol class="list">{props}</ol></div>
</div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Where it is used</p><h2 class="h3" style="margin-top:20px">Typical parts.</h2></div>
  <div class="rv"><p class="prose">{E(s["parts"])}</p><div class="note-box">{E(s["limits"])}</div></div>
</div></section>
{extra}
<section class="sec tight"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Options</p><h2 class="h3" style="margin-top:20px">Colour, gloss, effect <em>and cure.</em></h2></div><p class="lead">RAL or your sample · high gloss ≥ 90, satin and matt 11–80, dead matt ≤ 10 · ten surface effects · standard or low-cure.</p></div>
  <div class="atlas" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">{''.join(f'<a class="tile rv" href="/finishes/#{fk}" style="color:var(--ink)"><figure>{img("finish/" + fk, 800, 800, fn + " finish", "200px", 400)}</figure><h3 style="color:var(--ink)">{fn}</h3></a>' for fk, fn, _ in FINISHES)}</div>
</div></section>
<section class="sec tight alt"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Industries</p><h2 class="h3" style="margin-top:20px">Where we recommend {s["name"].lower()}.</h2></div></div>
  <div class="inds">{indcards}</div>
</div></section>
<section class="sec tight"><div class="wrap split"><div class="rv"><p class="eyebrow">Questions</p><h2 class="h3" style="margin-top:20px">Before you specify.</h2></div><div class="rv">{faq_block(faqs)}</div></div></section>'''
        body += cta(btn=('Send project details', '/contact/'), btn2=(f'Request a {s["name"].lower()} sample', f'/request-sample/?system={s["name"]}'))
        write(s['url'], f'{s["title"]} | POLYMER', s['lead'], body, 'products')


# ---------------------------------------------------------------- finishes
def build_finishes():
    tiles = ''.join(f'<div class="tile rv" id="{k}"><figure>{img("finish/" + k, 800, 800, n + " powder coating, macro", "(min-width:1060px) 20vw, (min-width:700px) 33vw, 50vw", 400)}</figure><h3>{n}</h3><p style="text-transform:none;letter-spacing:0;font-family:var(--sans);font-size:13.5px">{E(d)}</p></div>' for k, n, d in FINISHES)
    body = phero([('Colours & finishes', None)], 'Ten surface effects, <em>one approved version.</em>',
                 'RAL shades and customer samples in every effect, across all three systems. Each finish is confirmed on a physical panel under your spraying conditions, then recorded as the version for repeat orders.',
                 figure=f'<figure class="tall">{img("home/hero-panels", 1122, 1402, "Five powder-coated panels in different finishes", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>',
                 ctas=[('Match a colour', '/request-sample/?topic=colour', 'btn-primary'), ('How colour matching works', '/how-to/prepare-colour-matching-request/', 'btn-line')])
    body += f'<section class="sec dark"><div class="wrap"><div class="atlas">{tiles}</div></div></section>'
    pn = [(6875, 'Black fine texture'), (6890, 'Black sand texture'), (6877, 'Red sand texture'), (6886, 'Black high gloss'), (6882, 'Silver metallic, matt'), (6884, 'Silver metallic'),
          (6885, 'Champagne metallic'), (6887, 'Gold metallic'), (6888, 'Bright gold metallic'), (6889, 'Bronze metallic'), (6881, 'Translucent lime, high gloss'), (6883, 'Translucent magenta, high gloss')]
    body += f'''<section class="sec tight"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">From our panel library</p><h2 class="h2">Real panels, <em>photographed in our lab.</em></h2></div><p class="lead">Sprayed and cured on aluminium profile sections. Unretouched studio photos; colour on screen is a guide, and the physical panel is the reference.</p></div>
  {photos([(f'real/panel-{n}', c + ' powder coating on an aluminium profile section', c) for n, c in pn], 'c4 panels')}
</div></section>'''
    body += f'''<section class="sec tight"><div class="wrap gloss" style="margin-top:0">
  {img("home/gloss-trio", 1536, 1024, "Dead matt, satin and high gloss panels", "(min-width:980px) 60vw, 100vw", 768)}
  <div><h2 class="h3">Three gloss bands.</h2><div class="bands" style="border-color:var(--line)"><div style="border-color:var(--line)">Dead matt<span style="color:var(--accent)">≤ 10</span></div><div style="border-color:var(--line)">Satin &amp; matt<span style="color:var(--accent)">11 – 80</span></div><div style="border-color:var(--line)">High gloss<span style="color:var(--accent)">≥ 90</span></div></div><p class="prose mt24">Gloss is agreed per project with a measuring condition and a physical reference, because colour, texture and film thickness all change how gloss looks.</p></div>
</div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">How we confirm a finish</p><h2 class="h3" style="margin-top:20px">Colour code <em>plus a physical sample.</em></h2></div>
  <div class="rv"><div class="tbl-wrap"><table class="tbl" style="min-width:520px"><thead><tr><th>Choice</th><th>Best way to specify</th><th>What we check</th></tr></thead><tbody>
   <tr><td><b>Colour</b></td><td>Colour code and a physical sample; your current powder as a reference if you have one</td><td>Sample condition, light source, film thickness and colour-difference tolerance</td></tr>
   <tr><td><b>Gloss</b></td><td>The measuring and acceptance condition, plus a physical reference</td><td>How colour, texture and film affect the visual result</td></tr>
   <tr><td><b>Texture</b></td><td>A physical sample of the target texture</td><td>Size, evenness, feel and the effect on your real part</td></tr>
   <tr><td><b>Metallic</b></td><td>The target look and a reference part</td><td>Viewing angle, spraying conditions and effect consistency</td></tr>
  </tbody></table></div>
  <p class="tbl-note">Each panel is linked to its system, colour, gloss, texture, film thickness and cure. Samples, trial orders and bulk supply all refer to the same approved version.</p></div>
</div></section>
<section class="sec tight"><div class="wrap split"><div class="rv"><p class="eyebrow">Questions</p><h2 class="h3" style="margin-top:20px">About finishes.</h2></div><div class="rv">{faq_block(['available-finishes-and-effects', 'what-is-bonded-metallic-powder', 'colour-matching-ral-or-sample', 'approved-panel-version-repeat-orders'])}</div></div></section>'''
    body += cta(btn=('Match a colour', '/request-sample/?topic=colour'), btn2=('Send project details', '/contact/'))
    write('/finishes/', 'Powder Coating Colours & Finishes: Textures, Metallics, Gloss | POLYMER',
          'Ten powder coating effects including sand, wrinkle, hammer tone, bonded metallic, transparent and fluorescent, in three gloss bands, RAL and custom colours.', body, 'finishes')


# ---------------------------------------------------------------- selector + matrix
def build_selector():
    def opt(name, v, label, checked=False):
        return f'<label><input type="radio" name="{name}" value="{v}"{" checked" if checked else ""}><span>{E(label)}</span></label>'
    envs = [('out', 'Outdoor / UV'), ('dec', 'Indoor · decorative'), ('fun', 'Indoor · functional')]
    data = {
        'envSys': {'out': 'polyester', 'dec': 'hybrid', 'fun': 'epoxy'},
        'envName': {'out': 'outdoor, exposed to UV and weather', 'dec': 'indoor, appearance-led', 'fun': 'indoor, needs chemical resistance, hardness or insulation'},
        'sys': {k: {'name': s['name'], 'why': s['why'], 'url': s['url']} for k, s in SYS.items()},
        'ind': {i['slug']: {'name': i['short'], 'main': i['main'], 'opt': i['opt'], 'note': i['note'], 'selective': bool(i.get('selective'))} for i in IND},
        'fin': {k: n for k, n, _ in FINISHES},
        'gl': {'dm': 'dead matt (≤ 10)', 'sm': 'satin or matt (11–80)', 'hg': 'high gloss (≥ 90)'},
        'cu': {'std': 'standard cure.', 'low': 'low-cure grade, confirmed against your oven profile and line speed.'},
    }
    data['ind']['distributors'] = {'name': 'Powder distributors', 'main': ['polyester', 'hybrid', 'epoxy'], 'opt': [], 'note': 'full range from one supplier', 'selective': False}
    inds = ''.join(opt('ind', i['slug'], i['short']) for i in IND) + opt('ind', 'distributors', 'Distributor')
    fins = ''.join(opt('fin', k, n) for k, n, _ in FINISHES)
    rows = ''
    for i in IND + [dict(slug='distributors', short='Powder distributors', main=['polyester', 'hybrid', 'epoxy'], opt=[], parts='Importers and wholesalers serving applicators and manufacturers')]:
        cell = lambda k: '<span class="y">● Main</span>' if k in i['main'] else ('<span class="o">○ Option</span>' if k in i['opt'] else '<span class="n">—</span>')
        link = f'/industries/{i["slug"]}/' if i['slug'] != 'distributors' else '/distributors/'
        rows += f'<tr><td><a href="{link}"><b>{E(i["short"])}</b></a><br><span style="color:var(--muted);font-size:13px">{E(i["parts"])}</span></td><td>{cell("epoxy")}</td><td>{cell("polyester")}</td><td>{cell("hybrid")}</td></tr>'
    body = phero([('Resources', '/faq/'), ('System selector', None)], 'Find the right system <em>in four questions.</em>',
                 'Choose where the part will live, your industry, the finish and the cure. The suggestion follows our catalogue rules; your part and a line trial confirm it.')
    body += f'''<section class="sec tight"><div class="wrap tool" id="selector">
  <div>
   <fieldset class="q"><legend>1 · Where will the part live?</legend><div class="opts">{''.join(opt('env', v, l) for v, l in envs)}</div></fieldset>
   <fieldset class="q"><legend>2 · Industry</legend><div class="opts">{inds}</div></fieldset>
   <fieldset class="q"><legend>3 · Finish (optional)</legend><div class="opts">{fins}</div></fieldset>
   <fieldset class="q"><legend>4 · Gloss and cure (optional)</legend><div class="opts">{opt('gl', 'dm', 'Dead matt')}{opt('gl', 'sm', 'Satin / matt')}{opt('gl', 'hg', 'High gloss')}</div><div class="opts" style="margin-top:8px">{opt('cu', 'std', 'Standard cure')}{opt('cu', 'low', 'Low-cure')}</div></fieldset>
  </div>
  <aside class="result" id="sel-out" aria-live="polite"><small>Recommendation</small><h3>Choose an environment or industry</h3><p class="alt-sys">The result updates as you select. Without JavaScript, use the table below.</p></aside>
  <script type="application/json" id="sel-data">{json.dumps(data, ensure_ascii=False)}</script>
</div></section>
<section class="sec tight alt" id="matrix"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Industry × system</p><h2 class="h2">Which system <em>for which industry.</em></h2></div><p class="lead">● main recommendation · ○ option for specific parts or environments · — not recommended. Epoxy indoors, polyester outdoors, hybrid for indoor decorative parts.</p></div>
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>Industry</th><th>Epoxy</th><th>Polyester</th><th>Hybrid</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="tbl-note">A starting point only. Final suitability depends on your part, pretreatment, film thickness, cure conditions, specification and a line trial.</p>
</div></section>'''
    body += cta()
    write('/selector/', 'Powder Coating System Selector: Epoxy, Polyester or Hybrid | POLYMER',
          'Choose environment, industry, finish and cure to see which powder coating system we recommend, with the full industry × system table.', body, 'resources')


# ---------------------------------------------------------------- industries
def build_industries():
    cards = ''.join(f'<a class="ind rv" href="/industries/{i["slug"]}/"><figure>{img(i["img"], *i["imgw"], i["name"], "(min-width:1060px) 25vw, (min-width:640px) 50vw, 100vw")}</figure><span class="n">{i["n"]}</span><h3>{E(i["short"])}</h3>{chips(i["main"], i["opt"], "Selective" if i.get("selective") else None)}</a>' for i in IND)
    cards += f'<a class="ind rv" href="/distributors/"><figure>{img(DIST["img"], *DIST["imgw"], "Powder distribution warehouse", "(min-width:1060px) 25vw, (min-width:640px) 50vw, 100vw")}</figure><span class="n">08</span><h3>Powder distributors</h3><div class="chips"><span class="chip main">Full range</span></div></a>'
    body = phero([('Industries', None)], 'Eight industries, <em>matched part by part.</em>',
                 'Each solution sets out the buyer’s problems, the system we propose, what we can support and what we verify on your part before bulk supply.',
                 ctas=[('Use the selector', '/selector/', 'btn-primary'), ('Industry × system table', '/selector/#matrix', 'btn-line')])
    body += f'<section class="sec"><div class="wrap"><div class="inds">{cards}</div><p class="ind-note">Recommendations are a starting point. Final suitability depends on your part, pretreatment, film thickness, cure, specification and a line trial.</p></div></section>'
    body += cta()
    write('/industries/', 'Powder Coating Solutions by Industry | POLYMER',
          'Powder coating solutions for architectural aluminium, metal furniture, appliances, electrical enclosures, equipment, automotive parts, coating applicators and distributors.', body, 'industries')

    for i in IND:
        w, h = i['imgw']
        fig = f'<figure>{img(i["img"], w, h, i["name"], "(min-width:980px) 45vw, 100vw", lazy=False)}</figure>'
        probs = ''.join(f'<li><span>{k+1:02d}</span><div>{E(p)}</div></li>' for k, p in enumerate(i['problems']))
        recs = ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>' for a, b, c, d in i['recs'])
        caps = ''.join(f'<li><span>{k+1:02d}</span><div>{E(p)}</div></li>' for k, p in enumerate(i['caps']))
        ver = ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>' for a, b in i['verify'])
        others = ''.join(f'<a class="card rv" href="/industries/{o["slug"]}/"><small>{o["n"]}</small><h3 style="font-size:24px">{E(o["short"])}</h3><span class="link">View solution</span></a>' for o in IND if o['slug'] != i['slug'])[:0]
        sysq = '&'.join([f'industry={E(i["short"])}', f'system={SYS[i["main"][0]]["name"]}'])
        body = phero([('Industries', '/industries/'), (i['short'], None)], E(i['name']) + '.', E(i['oneliner']), figure=fig,
                     facts=[('Main: ' + ', '.join(SYS[m]['name'] for m in i['main']))] + ([('Option: ' + ', '.join(SYS[o]['name'] for o in i['opt']))] if i['opt'] else []) + (['Selective project'] if i.get('selective') else []),
                     ctas=[('Request a sample', f'/request-sample/?{sysq}', 'btn-primary'), ('Talk to us', '/contact/', 'btn-line')])
        body += f'''<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Who this is for</p><h2 class="h3" style="margin-top:20px">{E(i["parts"])}.</h2></div>
  <div class="rv"><p class="prose">{E(i["intro"])}</p></div>
</div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Buyer problems</p><h2 class="h3" style="margin-top:20px">What usually <em>goes wrong.</em></h2></div>
  <div class="rv"><ol class="list">{probs}</ol></div>
</div><div class="wrap">{fig2("ind/" + IND_PHOTOS[i["slug"]][0] + "-a", i["name"] + " parts on a powder coating line", IND_PHOTOS[i["slug"]][1])}</div></section>
<section class="sec tight"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Recommended systems</p><h2 class="h3" style="margin-top:20px">By part and environment.</h2></div><p class="lead">Based on our product catalogue. Suitability is confirmed on your part, film thickness, cure and specification.</p></div>
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>Need / use</th><th>Recommended</th><th>Basis</th><th>How we start</th></tr></thead><tbody>{recs}</tbody></table></div>
</div></section>
<section class="sec tight dark"><div class="wrap split">
  <div class="rv"><p class="eyebrow">What we bring</p><h2 class="h3" style="margin-top:20px;color:#fff">Capabilities <em style="color:var(--accent-hi)">you can use.</em></h2></div>
  <div class="rv"><ol class="list">{caps}</ol></div>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">What is verified</p><h2 class="h3" style="margin-top:20px">Before bulk supply.</h2><p class="prose mt24">From need to bulk: needs → selection and colour → sample evaluation on your line → order confirmation → ongoing supply to the approved version.</p></div>
  <div class="rv"><div class="tbl-wrap"><table class="tbl" style="min-width:420px"><thead><tr><th>Check</th><th>Focus</th></tr></thead><tbody>{ver}</tbody></table></div><div class="note-box"><b>Scope.</b> {E(i["scope"])}</div></div>
</div><div class="wrap">{fig2("ind/" + IND_PHOTOS[i["slug"]][0] + "-b", i["name"] + " coating close-up", IND_PHOTOS[i["slug"]][2])}</div></section>
<section class="sec tight alt"><div class="wrap center rv" style="max-width:860px"><p class="eyebrow" style="justify-content:center">How to start</p><p class="h3" style="margin-top:20px">“{E(i["quote"])}”</p></div></section>'''
        body += cta(btn=('Request a sample', f'/request-sample/?{sysq}'), btn2=('Send project details', '/contact/'))
        write(f'/industries/{i["slug"]}/', f'{i["name"]} Powder Coatings | POLYMER', i['oneliner'] + ' ' + i['intro'][:110] + '…', body, 'industries', og=f'/assets/img/ind/{IND_PHOTOS[i["slug"]][0]}-a.webp')


# ---------------------------------------------------------------- distributors
def build_distributors():
    fig = f'<figure>{img(DIST["img"], *DIST["imgw"], "Powder coating distribution warehouse with colour panels", "(min-width:980px) 45vw, 100vw", lazy=False)}</figure>'
    body = phero([('Distributors', None)], 'One source for <em>your whole market.</em>',
                 'Importers and wholesalers are our main channel. We supply polyester, hybrid and epoxy plus the effects series, so you can serve applicators and manufacturers from one supplier and replenish within 10 days.',
                 figure=fig, facts=['Full range', 'Lead time ≤ 10 days', 'Non-exclusive start', 'MOQ 1,000 kg'],
                 ctas=[('Become a distributor', '#apply', 'btn-primary'), ('Downloads', '/downloads/', 'btn-line')])
    probs = ['End-user colour demand is scattered, stock is a burden and powder has a shelf life.', 'Unstable supplier lead times cause stock-outs and broken promises to end users.', 'Without texture, metallic and certified products, higher-value orders are lost.', 'A new supplier’s batch consistency is unknown, and complaints are costly.', 'Price competition is intense; low price alone does not keep end users.']
    kit = [('Polyester, incl. Qualicoat Class 1 system', 'Aluminium, windows, outdoor furniture, lighting, farm machinery', 'Outdoor and architectural orders'),
           ('Epoxy-polyester hybrid', 'Furniture, shelving, appliances, indoor cabinets and lighting', 'Main indoor decorative orders'),
           ('Epoxy', 'Instrument housings, security doors, industrial and fitness equipment', 'Indoor functional orders'),
           ('Sand, wrinkle, hammer, metallic, fluorescent', 'Cabinets, outdoor products, equipment housings, lighting', 'Decorative, higher-margin orders'),
           ('Colour cards, panels and documents', 'All end users', 'Showing and quoting to end users')]
    rows = ''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in kit)
    body += f'''<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Distributor problems</p><h2 class="h3" style="margin-top:20px">What we help <em>you solve.</em></h2></div>
  <div class="rv"><ol class="list">{''.join(f'<li><span>{k+1:02d}</span><div>{E(p)}</div></li>' for k, p in enumerate(probs))}</ol></div>
</div><div class="wrap">{fig2("ind/distributors-a", "Pallets of powder cartons beside a shipping container", IND_PHOTOS["distributors"][1])}</div></section>
<section class="sec tight alt"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">First range</p><h2 class="h3" style="margin-top:20px">Product and material mix.</h2></div><p class="lead">Built around your end-user structure: the three systems, the effects series and custom colours.</p></div>
  <div class="tbl-wrap rv"><table class="tbl"><thead><tr><th>Product / material</th><th>End uses</th><th>Sales angle</th></tr></thead><tbody>{rows}</tbody></table></div>
  {fig2("ind/distributors-b", "Distributor starter kit with panels, colour card and powder sample", IND_PHOTOS["distributors"][2])}
</div></section>
<section class="sec tight dark"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Working together</p><h2 class="h3" style="margin-top:20px;color:#fff">Four steps, <em style="color:var(--accent-hi)">from pack to repeat orders.</em></h2></div>
  <div class="rv"><ol class="list">
   <li><span>01</span><div><b>Starter pack.</b> Catalogue, certificates, colour cards, panels and application limits, so you can screen end users without over-promising.</div></li>
   <li><span>02</span><div><b>End-user screening.</b> A list of applicators, aluminium, furniture, cabinet and appliance makers with coating lines and colour needs.</div></li>
   <li><span>03</span><div><b>Sample trials.</b> You bring the part and colour need; we match and support the trial so each project can be verified.</div></li>
   <li><span>04</span><div><b>Repeat orders.</b> Managed by colour, batch and customer ownership. We start non-exclusive and discuss regional terms on results.</div></li>
  </ol></div>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Supply</p><h2 class="h3" style="margin-top:20px">Built for <em>replenishment.</em></h2></div>
  <div class="rv"><dl class="kv"><dt>Capacity</dt><dd>5,000 t per year on 8 production lines, plus 5 sampling lines</dd><dt>Lead time</dt><dd>Standard within 10 days; complex custom colours and large volumes confirmed per order</dd><dt>Minimum order</dt><dd>1,000 kg per order</dd><dt>Export</dt><dd>About 20 countries and regions; experienced with export documents, packing and sea freight</dd><dt>Documents</dt><dd>ISO 9001 and ISO 14001 certificates and the Qualicoat Class 1 certificate for your sales pack</dd></dl></div>
</div></section>
<section class="sec tight alt" id="apply"><div class="wrap form-grid">
  {form_distributor()}
  {std_aside([('Cooperation terms FAQ', '/faq/#distributor-cooperation-terms')])}
</div></section>'''
    body += cta(title='Serve your whole market <em>from one supplier.</em>', text='Tell us your market, end-user mix and monthly volume. We propose a first range and a starter pack.', btn=('Apply as distributor', '#apply'), btn2=('Downloads', '/downloads/'))
    write('/distributors/', 'Powder Coating Distributors & Importers: Partner Programme | POLYMER',
          'A combined polyester, hybrid and epoxy range plus effects for powder coating importers and distributors, with a standard lead time within 10 days and a non-exclusive start.', body, 'distributors')


# ---------------------------------------------------------------- forms
def consent():
    return '<label class="consent"><input type="checkbox" name="consent" required> <span>I agree that POLYMER may store and process the information above in order to respond to this enquiry, as described in the <a href="/privacy/">privacy notice</a>. <i>*</i></span></label>'


ROLES = ['Purchasing / sourcing', 'Technical / QC', 'Production / coating line', 'Management / owner', 'Distributor / trader']


def std_form(name, btn, placeholder, hidden=(), summary=False):
    """One form template for every form on the site (reference layout: vistamatt.com/contact)."""
    hid = ''.join(f'<input type="hidden" name="{h}" data-prefill="{h}">' for h in hidden)
    roles = ''.join(f'<option>{r}</option>' for r in ROLES)
    return f'''<form class="f" name="{name}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="{name}"><p class="hp"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>{hid}
<div class="row two"><div class="fld"><label for="{name}-name">Name <i>*</i></label><input id="{name}-name" name="name" autocomplete="name" required></div><div class="fld"><label for="{name}-co">Company <i>*</i></label><input id="{name}-co" name="company" autocomplete="organization" required></div></div>
<div class="row two"><div class="fld"><label for="{name}-mail">Work email <i>*</i></label><input id="{name}-mail" type="email" name="email" autocomplete="email" required></div><div class="fld"><label for="{name}-country">Country / region <i>*</i></label><input id="{name}-country" name="country" autocomplete="country-name" required></div></div>
<div class="row two"><div class="fld"><label for="{name}-role">Your role</label><select id="{name}-role" name="role"><option value="">Select</option>{roles}</select></div></div>
<div class="row"><div class="fld"><label for="{name}-need">What do you need <i>*</i></label><textarea id="{name}-need" name="message" required{" data-prefill-summary" if summary else ""} placeholder="{E(placeholder)}"></textarea></div></div>
{consent()}
<div class="submit"><button class="btn btn-primary" type="submit">{btn}</button></div>
<p class="form-note">Fields marked * are required. We use these details only to respond to your enquiry and do not share them with third parties.</p></form>'''


def std_aside(extra=()):
    links = [('System selector', '/selector/'), ('Colours &amp; finishes', '/finishes/'), ('Technical FAQ', '/faq/'), ('Quality &amp; certificates', '/quality/')] + list(extra)
    li = ''.join(f'<li><a href="{u}">{t}</a></li>' for t, u in links)
    return f'''<aside class="aside">
 <div class="grp"><h3>Direct contact</h3><dl><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>Phone</dt><dd><a href="tel:+865962600611">{TEL}</a></dd><dt>WhatsApp</dt><dd><a href="{wa_link(0)}" target="_blank" rel="noopener">{WA[0][0]}</a><br><a href="{wa_link(1)}" target="_blank" rel="noopener">{WA[1][0]}</a></dd><dt>Response time</dt><dd>Within one working day, Monday to Saturday (UTC+8).</dd></dl></div>
 <div class="grp"><h3>Regional coverage</h3><dl class="reg"><dd><b>Russia &amp; Europe</b> · Russia, Latvia, Turkey</dd><dd><b>Latin America</b> · Mexico, Colombia, Peru, Brazil, Chile</dd><dd><b>Middle East &amp; Africa</b> · Saudi Arabia, UAE, Oman, Kenya, Nigeria</dd><dd><b>South &amp; Southeast Asia</b> · Sri Lanka, Vietnam, Thailand, Malaysia, Indonesia</dd></dl><p>All enquiries are handled by our team in Zhangzhou, China. Tell us the destination early and we prepare export documents, packing and freight together with the samples.</p></div>
 <div class="grp"><h3>Useful before you write</h3><ul>{li}</ul></div>
</aside>'''


WHY = '''<section class="sec tight alt"><div class="wrap">
 <div class="head rv"><div><p class="eyebrow">Before samples ship</p><h2 class="h2">What we ask for, <em>and why.</em></h2></div><p class="lead">A described part gets a matched panel and a system recommendation. A bare colour code gets a guess.</p></div>
 <div class="cards c4">
 <div class="card rv"><small>Part</small><h3 style="font-size:24px">What it is</h3><p>Use, substrate, size and a photo or sample. This decides the system.</p></div>
 <div class="card rv"><small>Environment</small><h3 style="font-size:24px">Where it lives</h3><p>Indoor or outdoor, humidity, coastal, chemicals, temperature.</p></div>
 <div class="card rv"><small>Appearance</small><h3 style="font-size:24px">How it looks</h3><p>Colour code or sample, gloss, texture or metallic target.</p></div>
 <div class="card rv"><small>Process</small><h3 style="font-size:24px">How you coat</h3><p>Pretreatment, film thickness, spray equipment and actual cure. Usually the most useful line.</p></div></div>
</div></section>'''


def form_distributor():
    return std_form('distributor', 'Apply as distributor', 'Your market and territory, the end users you serve (applicators, aluminium, furniture, cabinets, appliances), current suppliers, monthly powder volume and warehousing.')


def build_forms():
    aside = std_aside()
    sample = std_form('sample', 'Request samples', 'Tell us the part and substrate, indoor or outdoor use, target colour (RAL or sample) and finish, pretreatment, cure, your current powder and expected volume (orders from 1,000 kg). Please add the shipping address for the samples.',
                      hidden=('industry', 'system', 'finish', 'gloss', 'cure', 'topic'), summary=True)
    fig = f'<figure>{img("home/sample-kit", 1536, 1024, "Sample box with three powder-coated panels and powder sachets", "(min-width:980px) 45vw, 100vw", 768, lazy=False)}</figure>'
    body = phero([('Request a sample', None)], 'Panels in your colour, <em>before you commit.</em>',
                 'The more you tell us about the part, the more useful the first panels will be. We propose a system, match the colour and send panels or powder for a trial on your line.', figure=fig,
                 facts=['Matched to your colour', 'Approved version recorded', 'Orders from 1,000 kg'])
    body += f'<section class="sec tight"><div class="wrap"><div class="form-grid">{sample}{aside}</div></div></section>' + WHY
    write('/request-sample/', 'Request a Powder Coating Sample | POLYMER', 'Request powder coating panels or powder in your colour and finish for evaluation and line trials.', body)

    contact = std_form('contact', 'Send enquiry', 'If you tell us the part, where it is used, the colour and finish you need and the powder you use now, we can recommend the right system and match your product faster.', hidden=('topic',))
    body = phero([('Contact', None)], 'Start a project <em>with our team.</em>', 'For projects, colour matching, documents or distributor cooperation. A described problem gets a sample plan; a bare colour code gets a guess.',
                 facts=[EMAIL, 'Tel ' + TEL, 'Zhangzhou, Fujian, China'])
    body += f'<section class="sec tight"><div class="wrap"><div class="form-grid">{contact}{aside}</div></div></section>' + WHY
    write('/contact/', 'Contact POLYMER Powder Coatings', 'Contact Fujian Polymer about powder coating projects, colour matching, documents or distributor cooperation.', body, 'contact')

    body = phero([('Thank you', None)], 'Thank you, <em>we have it.</em>', 'We reply within one working day. If your request is urgent, email ' + EMAIL + ' or call ' + TEL + '.',
                 ctas=[('Back to home', '/', 'btn-primary'), ('Read the technical FAQ', '/faq/', 'btn-line')])
    write('/thanks/', 'Thank you | POLYMER', 'Your message has been received.', body, sitemap=False)

    docs = [('Product catalogue', 'Three systems, cure grades, gloss bands and effects'), ('Technical data sheets (TDS)', 'Per product: properties, cure conditions, storage'), ('Safety data sheets (SDS)', 'Per product: safe handling and transport'),
            ('Qualicoat Class 1 certificate', 'Polyester system PLM100611, P-2199, valid until 31 Dec 2026'), ('ISO 9001:2015 certificate', 'No. 05326Q01777R001, valid until 11 Oct 2029'), ('ISO 14001:2015 certificate', 'No. 05326E01349R001, valid until 11 Oct 2029'), ('SGS EU RoHS report', 'XMNEC26001081101, black powder sample, (EU) 2015/863'), ('Colour cards and panels', 'Physical samples for evaluation')]
    cards = ''.join(f'<div class="card rv"><small>On request</small><h3 style="font-size:24px">{E(n)}</h3><p>{E(d)}</p></div>' for n, d in docs)
    dform = std_form('documents', 'Request documents', 'Which documents you need (catalogue, TDS, SDS, Qualicoat, ISO or the SGS report) and for which products, colours or project.')
    body = phero([('Resources', '/faq/'), ('Downloads', None)], 'Documents for <em>your approval file.</em>', 'Catalogue, TDS, SDS and certificates are sent by email on request, so each file matches the product you are evaluating and the latest version.',
                 figure=f'<figure>{img("ind/distributors-b", 1536, 1024, "Colour panels, colour card and powder sample", "(min-width:980px) 45vw, 100vw", 768, lazy=False)}</figure>', facts=['TDS', 'SDS', 'Certificates', 'Catalogue'])
    body += f'<section class="sec tight"><div class="wrap"><div class="cards c4">{cards}</div></div></section><section class="sec tight alt"><div class="wrap form-grid">{dform}{aside}</div></section>'
    body += cta()
    write('/downloads/', 'Downloads: TDS, SDS, Certificates & Catalogue | POLYMER', 'Request powder coating technical data sheets, safety data sheets, ISO and Qualicoat certificates and the product catalogue.', body, 'resources')


# ---------------------------------------------------------------- quality
def build_quality():
    tests = [('Colour', 'Colorimeter; visual check in a standard light box', 'Colour difference against the approved panel'), ('Gloss', '60° gloss meter', 'Gloss band and consistency'),
             ('Film thickness', 'Electromagnetic film thickness gauge', 'Film build on test panels'), ('Particle size', 'Laser particle size analyser', 'Particle size distribution of the powder'),
             ('Sieving', 'Screen mesh', 'Oversize particles removed before packing'), ('Appearance', 'Visual inspection', 'Surface defects on the cured film'),
             ('Pencil hardness', 'Pencil hardness tester', 'Surface hardness'), ('Impact', 'Erichsen impact tester', 'Resistance to impact'),
             ('Flexibility', '180° bend', 'Flexibility of the film on bending'), ('Adhesion', 'Cross-cut, 1 mm × 100 squares', 'Adhesion of the film to the substrate'),
             ('Salt spray', 'Salt spray corrosion test chamber', 'Corrosion behaviour on panels'), ('UV ageing', 'UV accelerated weathering tester', 'Colour and gloss change under UV'),
             ('Cure', 'Oven temperature data logger', 'Real metal temperature profile on the line'), ('Storage stability', '6 months below 30 °C', 'Powder stays free-flowing in storage')]
    rows = ''.join(f'<tr><td><b>{a}</b></td><td>{m}</td><td>{b}</td></tr>' for a, m, b in tests)
    labs = photos([('real/colorimeter', 'Colour measurement with a colorimeter', 'Colorimeter'), ('real/light-box', 'Standard light box for visual colour matching', 'Light box'), ('real/gloss', '60° gloss measurement on a green panel', '60° gloss'),
                   ('real/particle', 'Loading powder into the laser particle size analyser', 'Particle size'), ('real/pencil', 'Pencil hardness test on a coated panel', 'Pencil hardness'), ('real/bending', 'Bend test on a coated panel', 'Bend test'),
                   ('real/salt-spray', 'Salt spray corrosion test chamber', 'Salt spray'), ('real/uv-tester', 'UV accelerated weathering tester', 'UV ageing')], 'c4')

    body = phero([('Quality', None)], 'Every claim, <em>with its scope.</em>', 'What each certificate covers, how we test panels and batches, and how the approved version keeps repeat orders consistent.',
                 figure=f'<figure class="tall">{img("home/panel-single", 1122, 1402, "An approved test panel on a black plinth", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>',
                 facts=['Qualicoat Class 1 · P-2199', 'ISO 9001', 'ISO 14001', 'SGS RoHS report'])
    body += f'''<section class="sec tight"><div class="wrap">
  <div class="certs">
   <article class="cert key rv"><small>Architectural coating approval</small><h3>Qualicoat Class 1</h3><dl><dt>Licence</dt><dd>P-2199</dd><dt>System</dt><dd>Polyester PLM100611 · gloss category 3</dd><dt>Granted</dt><dd>20 Oct 2025 · Standard approval</dd><dt>Valid</dt><dd>Until 31 Dec 2026</dd><dt>Scope</dt><dd>The approved polyester system only. Not all products or colours; no structured-texture or metallic extension; not Class 2 or 3.</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
   <article class="cert rv"><small>Quality management</small><h3>ISO 9001:2015</h3><dl><dt>Cert. no.</dt><dd>05326Q01777R001</dd><dt>Valid</dt><dd>12 Oct 2026 – 11 Oct 2029</dd><dt>Issuer</dt><dd>Beijing NGV Certification Center Co., Ltd.</dd><dt>Scope</dt><dd>Design, manufacture and sales of thermosetting powder coatings. A management system certificate, not a product approval.</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
   <article class="cert rv"><small>Environmental management</small><h3>ISO 14001:2015</h3><dl><dt>Cert. no.</dt><dd>05326E01349R001</dd><dt>Valid</dt><dd>12 Oct 2026 – 11 Oct 2029</dd><dt>Issuer</dt><dd>Beijing NGV Certification Center Co., Ltd.</dd><dt>Scope</dt><dd>Design, manufacture and sales of thermosetting powder coatings. A management system certificate, not a product approval.</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
  </div>
  <p class="tbl-note">ISO certificates can be verified on the issuer’s website, www.ngv.org.cn.</p></div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Third-party test report</p><h2 class="h3" style="margin-top:20px">EU RoHS, <em>tested by SGS.</em></h2><p class="prose mt24">An independent laboratory report, stated with its sample. Reports for other products or other regulations can be arranged for a project.</p></div>
  <div class="rv"><article class="cert"><small>Restricted substances</small><h3>SGS · EU RoHS</h3><dl><dt>Report</dt><dd>XMNEC26001081101 · 12 May 2026</dd><dt>Laboratory</dt><dd>SGS-CSTC Standards Technical Services Co., Ltd., Xiamen Branch</dd><dt>Standard</dt><dd>(EU) 2015/863 amending Directive 2011/65/EU Annex II: Pb, Hg, Cd, Cr(VI), PBB, PBDE, DEHP, BBP, DBP, DIBP</dd><dt>Result</dt><dd>Pass; all ten substances not detected</dd><dt>Sample</dt><dd>One black powder coating sample as submitted. It does not cover other colours or products.</dd></dl><a class="link" href="/downloads/">Request the report</a></article></div>
</div></section>
<section class="sec tight alt"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">In-house laboratory</p><h2 class="h2">What we check <em>on panels and batches.</em></h2></div><p class="lead">Our technical research lab, QC lab and sample room test every new colour and every batch before release. These are internal test conditions, not third-party reports.</p></div>
  {labs}
  <div class="tbl-wrap rv" style="margin-top:40px"><table class="tbl" style="min-width:620px"><thead><tr><th>Test</th><th>Method / equipment</th><th>What it shows</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Two checkpoints</p><h2 class="h3" style="margin-top:20px">No batch is packed <em>before it passes.</em></h2></div>
  <div class="rv"><ol class="list">
   <li><span>01</span><div><b>Self-check after sieving.</b> The production team checks the finished powder. A failure goes back to the formula and premix stage.</div></li>
   <li><span>02</span><div><b>Laboratory test.</b> QC tests the batch against the approved panel. Only qualified batches are cooled, weighed, packed and put into the warehouse.</div></li>
  </ol></div>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">The approved version</p><h2 class="h3" style="margin-top:20px">How repeat orders <em>stay the same.</em></h2></div>
  <div class="rv"><ol class="list">
   <li><span>01</span><div><b>Panel linked to its settings.</b> System, colour, gloss, texture, film thickness and cure are recorded with each approved panel.</div></li>
   <li><span>02</span><div><b>One reference for everyone.</b> Samples, trial orders and bulk supply all refer to the same version.</div></li>
   <li><span>03</span><div><b>Batch checked against it.</b> Colour, gloss and appearance are compared with the approved panel before shipment.</div></li>
   <li><span>04</span><div><b>Changes are new versions.</b> A new colour, part or condition becomes a new approved version, not a silent change.</div></li>
  </ol></div>
</div></section>
<section class="sec tight alt"><div class="wrap split"><div class="rv"><p class="eyebrow">Questions</p><h2 class="h3" style="margin-top:20px">About quality.</h2></div><div class="rv">{faq_block(['what-qualicoat-class-1-covers', 'in-house-testing-scope-and-limits', 'approved-panel-version-repeat-orders', 'documents-available-tds-sds-certificates'])}</div></div></section>'''
    body += cta()
    write('/quality/', 'Quality & Certificates: Qualicoat Class 1, ISO 9001, ISO 14001, RoHS | POLYMER',
          'Qualicoat Class 1 for polyester system PLM100611 (P-2199), ISO 9001 and ISO 14001 certificates valid to 2029, an SGS EU RoHS report, in-house laboratory tests and approved-panel version control.', body, 'quality')


# ---------------------------------------------------------------- company
def build_company():
    stats = ''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in STATS)
    body = phero([('Company', None)], 'Powder coatings for metal, <em>made with care.</em>',
                 'Fujian Polymer Industry &amp; Trade Co., Ltd. was founded on 22 April 2019 in Zhangzhou, Fujian. We make thermosetting powder coatings for metal protection and decoration, and supply distributors, metal product manufacturers and coating applicators.',
                 figure=f'<figure class="tall">{img("home/hero-panels", 1122, 1402, "Powder-coated panels in five finishes", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>')
    body += f'''<section class="proof" style="background:var(--night)"><div class="wrap">{stats}</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">What we do</p><h2 class="h3" style="margin-top:20px">The right system, the matched colour, <em>on time.</em></h2></div>
  <div class="rv prose"><p>We produce three powder systems: epoxy for indoor functional parts, polyester for outdoor parts, and epoxy-polyester hybrid for indoor decorative parts. Our polyester system PLM100611 is Qualicoat Class 1 approved.</p><p>Our work starts from the customer’s part and where it will be used. We recommend the system, match the colour and finish, and record the approved panel so every batch can be checked against it. Standard lead time is within 10 days, and we do not make low-end powder.</p><h3>Who we supply</h3><ul><li>Powder importers and distributors, our main channel</li><li>Aluminium extruders, metal furniture, appliance, enclosure and equipment manufacturers</li><li>Professional coating applicators ordering from 1 t</li></ul></div>
</div></section>
<section class="sec tight alt" id="factory"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Inside the factory</p><h2 class="h2">From formula <em>to warehouse.</em></h2></div><p class="lead">Eight production lines, five sampling lines for panels and small trial batches, and two bonding machines for gold, silver and other metallic effects. Monthly output up to 500 t.</p></div>
  {photos([('real/premixer', 'Operator loading raw materials into the premixer', 'Premix'), ('real/extruder', 'Twin-screw powder coating extruder with cooling belt', 'Melt extrusion'), ('real/grinder', 'Grinding and classifying mill', 'Grinding & sieving'),
           ('real/cone-mixer', 'Double-cone mixer', 'Cone mixer'), ('real/bonding', 'Metallic bonding machine', 'Metallic bonding'), ('real/loading', 'Forklift loading powder cartons into a container', 'Export loading')])}
  <ol class="flow rv">
   <li>Work out the scheme</li><li>Weigh to formula</li><li>Premix</li><li>Melt extrusion</li><li>Cool</li><li>Grind &amp; sieve</li><li class="chk">Self-check</li><li class="chk">Lab test</li><li>Weigh &amp; pack</li><li>Warehouse</li>
  </ol>
  <p class="tbl-note">A batch that fails the self-check or the lab test goes back to the formula stage. See <a class="link" href="/quality/">quality and testing</a>.</p>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Company facts</p><h2 class="h3" style="margin-top:20px">Capacity, <em>people and labs.</em></h2></div>
  <div class="rv"><dl class="kv"><dt>Founded</dt><dd>22 April 2019, Zhangzhou, Fujian</dd><dt>Capacity</dt><dd>5,000 t per year; up to 500 t per month</dd><dt>Production</dt><dd>8 production lines and 5 sampling lines</dd><dt>Metallics</dt><dd>2 metallic bonding machines, which help reduce separation of metallic pigment during spraying and reclaim</dd><dt>Laboratories</dt><dd>Technical research lab, QC lab and sample development room</dd><dt>Testing</dt><dd>Colour, 60° gloss, film thickness, particle size, salt spray, UV accelerated ageing, pencil hardness, impact, bend, cross-cut adhesion, oven temperature profiling</dd><dt>Certificates</dt><dd>Qualicoat Class 1 (P-2199) · ISO 9001:2015 · ISO 14001:2015 · SGS EU RoHS report</dd><dt>China offices</dt><dd>Fuzhou, Quanzhou, Xiamen and Longyan in Fujian; Guangdong; Zhejiang</dd></dl></div>
</div></section>
<section class="sec tight dark"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Recognition</p><h2 class="h3" style="margin-top:20px">Recognised <em>at home.</em></h2><p class="prose mt24" style="color:#b4b8bd">Awarded by national and Fujian provincial authorities. Certificates are available on request.</p></div>
  <div class="rv"><ol class="list">
   <li><span>01</span><div><b>National High-Tech Enterprise.</b> Recognised under China’s high-tech enterprise programme.</div></li>
   <li><span>02</span><div><b>Fujian “Specialised, Refined, Distinctive and Innovative” SME.</b> Fujian Department of Industry and Information Technology, 2025–2028.</div></li>
   <li><span>03</span><div><b>Fujian Innovative SME.</b> Fujian Department of Industry and Information Technology, 2025.</div></li>
   <li><span>04</span><div><b>Science and Technology-based SME.</b> Registered with the Fujian Provincial Department of Science and Technology.</div></li>
   <li><span>05</span><div><b>Utility-model patents.</b> Granted by the China National Intellectual Property Administration for production equipment and processes.</div></li>
   <li><span>06</span><div><b>Vice-chair member.</b> Xiangcheng District Enterprise and Entrepreneur Association, Zhangzhou.</div></li>
  </ol></div>
</div></section>
<section class="sec tight"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Where we export</p><h2 class="h2">About 20 countries <em>and regions.</em></h2></div><p class="lead">Experienced with export documents, packing and sea freight to our established markets.</p></div>
  <div class="regions light">
   <div class="region rv"><h3>Russia &amp; Europe</h3><p>Russia · Latvia · Turkey</p></div>
   <div class="region rv"><h3>Latin America</h3><p>Mexico · Dominican Republic · Colombia · Peru · Brazil · Chile</p></div>
   <div class="region rv"><h3>Middle East &amp; Africa</h3><p>Saudi Arabia · UAE · Oman · Lebanon · Kenya · Nigeria</p></div>
   <div class="region rv"><h3>South &amp; Southeast Asia</h3><p>Sri Lanka · Vietnam · Thailand · Malaysia · Indonesia</p></div>
  </div>
</div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Environment</p><h2 class="h3" style="margin-top:20px">Powder, <em>by nature.</em></h2></div>
  <div class="rv prose"><p>Powder coatings are applied as a dry powder and contain no solvent carrier, and oversprayed powder can be reclaimed and reused on many lines. Our environmental management system is certified to ISO 14001:2015, and an SGS test of a black powder sample found none of the ten EU RoHS restricted substances.</p><p>We make no further environmental claims without data. If your purchasing team needs specific declarations, ask us and we will confirm what can be supplied for the product concerned.</p></div>
</div></section>'''
    body += cta()
    write('/company/', 'About POLYMER | Fujian Polymer Industry & Trade Co., Ltd.',
          'Founded in 2019 in Zhangzhou, Fujian, POLYMER makes epoxy, polyester and hybrid powder coatings with 5,000 t annual capacity, 8 production lines and a standard lead time within 10 days.', body, 'company')


# ---------------------------------------------------------------- faq + how-to
def build_geo():
    qa = [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['short'] + ' ' + ' '.join(f['body'])}} for f in GEO['faq']]
    n = len(GEO['faq'])
    cnt = {k: sum(1 for f in GEO['faq'] if f.get('cat') == k) for k, _ in FAQ_CATS}
    toc = ''.join(f'<a href="#t-{k}"><span>{E(t)}</span><b>{cnt[k]}</b></a>' for k, t in FAQ_CATS) + '<a class="spec" href="#specialist"><span>Talk to our team</span><b>→</b></a>'
    glance = f'''<div class="fq-glance rv"><p class="eyebrow">POLYMER at a glance</p><dl>
<dt>Company</dt><dd>Fujian Polymer Industry &amp; Trade Co., Ltd., Zhangzhou, China · founded 22 April 2019</dd>
<dt>Systems</dt><dd>Polyester (outdoor) · Epoxy-polyester hybrid (indoor decorative) · Epoxy (indoor functional) · standard &amp; low-cure</dd>
<dt>Finishes</dt><dd>RAL &amp; custom colours · 3 gloss bands · 10 surface effects · bonded metallics on 2 machines</dd>
<dt>Supply</dt><dd>5,000 t/year · 8 production + 5 sampling lines · MOQ 1,000 kg · standard lead time within 10 days</dd>
<dt>Approvals</dt><dd>Qualicoat Class 1 · P-2199 (polyester PLM100611, to 31 Dec 2026) · ISO 9001:2015 · ISO 14001:2015 · SGS EU RoHS report</dd>
<dt>Storage</dt><dd>Cool and dry · stability tested 6 months below 30 °C · not dangerous goods for transport</dd>
<dt>Contact</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a> · {TEL} · WhatsApp {WA[0][0]} / {WA[1][0]} · reply within one working day</dd></dl></div>'''
    cats = ''
    for i, (k, t) in enumerate(FAQ_CATS):
        slugs = [f['slug'] for f in GEO['faq'] if f.get('cat') == k]
        cats += f'<section class="fq-cat rv" id="t-{k}"><p class="eyebrow">{i + 1:02d} · {cnt[k]} answers</p><h2 class="h3">{E(t)}</h2>{faq_block(slugs)}</section>'
        if k == 'colour':
            cats += ('<figure class="fq-band rv"><img src="/assets/img/intro/palette-900.webp" srcset="/assets/img/intro/palette-900.webp 900w, /assets/img/intro/palette.webp 1672w" sizes="(min-width:1060px) 860px, 100vw" width="1672" height="941" loading="lazy" alt="A fan of powder-coated colour panels in reds, blues, greys, metallics and greens">'
                     '<figcaption><p class="eyebrow">Colour library</p><p class="fq-band-t">Matched on a physical panel, <em>not on a screen.</em></p><a class="link" href="/finishes/">Colours &amp; finishes</a></figcaption></figure>')
        if k == 'quality':
            labs = ''.join(f'<figure>{img(n, IMG2[n][0], IMG2[n][1], alt, "(min-width:1060px) 210px, 50vw", IMG2[n][2])}<figcaption>{c}</figcaption></figure>' for n, alt, c in
                           [('real/colorimeter', 'Colour measurement with a colorimeter', 'Colour'), ('real/gloss', '60° gloss measurement on a panel', '60° gloss'), ('real/particle', 'Laser particle size analysis', 'Particle size'), ('real/bending', 'Bend test on a coated panel', 'Bend test')])
            cats += f'<div class="fq-lab rv"><div class="fq-lab-h"><p class="eyebrow">Inside our laboratory · real photos</p><p class="fq-band-t">Every batch is tested <em>before it is packed.</em></p><a class="link" href="/quality/">Quality &amp; testing</a></div><div class="fq-lab-g">{labs}</div></div>'
    body = phero([('FAQ', None)], 'Powder coating questions, <em>answered.</em>',
                 f'{n} answers about POLYMER powder coatings: systems, colour and effects, orders and supply, certificates, samples, the company and distributor cooperation. Short answer first, then the detail and the page behind it.',
                 facts=[f'{n} answers', '7 topics', 'Updated 27 October 2026'], ctas=[('Ask our team', '/contact/', 'btn-primary'), ('How-to guides', '/how-to/', 'btn-line')])
    body += f'''<section class="sec tight"><div class="wrap fq-layout">
  <aside class="fq-toc"><p class="eyebrow">Topics</p><label class="fq-search"><span class="hp">Search questions</span><input type="search" id="fq-q" placeholder="Search questions…" autocomplete="off"></label><nav aria-label="FAQ topics">{toc}</nav></aside>
  <div class="fq-main">{glance}{cats}<p class="fq-none" id="fq-none" hidden>No question matches your search. <a class="link" href="/contact/">Ask our team</a></p>
   <section class="fq-spec rv" id="specialist">{bgimg('cta-red')}<div class="fq-spec-in"><p class="eyebrow">When to talk to our team directly</p><h2 class="h3">Some answers depend <em>on your part.</em></h2>
    <ul><li>Volume pricing and annual supply</li><li>Projects that name Qualicoat or another specification</li><li>Custom colours, textures and metallic effects from your sample</li><li>Distributor ranges and regional terms</li><li>Documents for a tender or supplier approval file</li></ul>
    <div class="hero-ctas"><a class="btn btn-primary" href="/contact/">Send project details {ARROW}</a><a class="btn btn-line" href="/request-sample/">Request a sample</a></div></div></section>
  </div></div></section>
<script>(function(){{var q=document.getElementById('fq-q');if(!q)return;var ds=[].slice.call(document.querySelectorAll('.fq-cat details')),cs=[].slice.call(document.querySelectorAll('.fq-cat')),no=document.getElementById('fq-none');
q.addEventListener('input',function(){{var v=q.value.trim().toLowerCase(),hit=0;ds.forEach(function(d){{var m=!v||d.textContent.toLowerCase().indexOf(v)>-1;d.hidden=!m;if(m)hit++;if(v&&m&&v.length>2)d.open=true}});cs.forEach(function(c){{c.hidden=!c.querySelector('details:not([hidden])')}});no.hidden=hit>0;var g=document.querySelector('.fq-glance');if(g)g.hidden=!!v}});
if(location.hash){{var t=document.getElementById(location.hash.slice(1));if(t&&t.tagName==='DETAILS'){{t.open=true;}}}}}})();</script>'''
    write('/faq/', 'Powder Coating FAQ: Systems, Colours, MOQ, Certificates & Samples | POLYMER', f'{n} answers on POLYMER powder coatings: choosing epoxy, polyester or hybrid, Qualicoat Class 1 scope, ISO certificates, RoHS, MOQ, lead time, colour matching, samples, export and distributors.', body, 'faq',
          ld=[{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": qa}])

    cards = ''.join(f'<a class="card rv" href="/how-to/{h["slug"]}/"><small>How-to · {len(h["steps"])} steps</small><h3 style="font-size:26px">{E(h["title"])}</h3><p>{E(h["summary"])}</p><span class="link">Read guide</span></a>' for h in GEO['howto'])
    body = phero([('Resources', None), ('How-to guides', None)], 'Practical guides <em>for the coating line.</em>', 'Step-by-step guidance on choosing, trialling, checking and handling powder coatings.')
    body += f'<section class="sec tight"><div class="wrap"><div class="cards c3">{cards}</div></div></section>' + cta()
    write('/how-to/', 'Powder Coating How-to Guides | POLYMER', 'Guides on choosing a powder system, colour-matching requests, line trials, reading a TDS, cure checks, film thickness, coverage, batch consistency, textures and storage.', body, 'resources')

    for h in GEO['howto']:
        steps = ''.join(f'<li><div><b>{E(s["name"])}</b><p>{E(s["text"])}</p></div></li>' for s in h['steps'])
        params = ''.join(f'<dt>{E(p["k"])}</dt><dd>{E(p["v"])}</dd>' for p in h['params'])
        mist = ''.join(f'<li>{E(m)}</li>' for m in h['mistakes'])
        rel = [f for f in GEO['faq'] if h['slug'] in f.get('related', [])][:3]
        relq = ''.join(f'<li><a class="link" href="/faq/#{f["slug"]}">{E(f["q"])}</a></li>' for f in rel)
        ld = {"@context": "https://schema.org", "@type": "HowTo", "name": h['title'], "description": h['summary'],
              "step": [{"@type": "HowToStep", "position": k + 1, "name": s['name'], "text": s['text']} for k, s in enumerate(h['steps'])]}
        body = phero([('Resources', None), ('How-to', '/how-to/'), (h['title'], None)], E(h['title']) + '.', E(h['summary']))
        body += f'''<section class="sec tight"><div class="wrap split">
  <aside class="rv"><p class="eyebrow">When you need this</p><p class="prose mt24">{E(h["scene"])}</p>{f'<h3 class="h3" style="font-size:26px;margin-top:40px">Related questions</h3><ul style="margin-top:12px;list-style:none;display:grid;gap:10px">{relq}</ul>' if relq else ''}</aside>
  <article class="article rv">
   <h2>Steps</h2><ol class="steps-a">{steps}</ol>
   {f'<h2>Parameters</h2><dl class="kv">{params}</dl>' if params else ''}
   <h2>Common mistakes</h2><ul class="mistakes">{mist}</ul>
   <div class="aside-cta"><h3>Next step</h3><p>{E(h["cta"])}</p><a class="btn btn-primary" href="/request-sample/">Request a sample {ARROW}</a></div>
  </article>
</div></section>'''
        write(f'/how-to/{h["slug"]}/', f'{h["title"]} | POLYMER Powder Coatings', h['summary'], body, 'resources', ld=[ld])


# ---------------------------------------------------------------- legal + 404
def build_legal():
    body = phero([('Privacy & cookies', None)], 'Privacy <em>&amp; cookies.</em>', 'How we handle the details you send us through this website. Last updated 27 October 2026.')
    body += f'''<section class="sec tight"><div class="wrap legal">
<p>This notice is provided by Fujian Polymer Industry &amp; Trade Co., Ltd., {ADDR} (“POLYMER”, “we”). It explains what personal data we collect through this website and how we use it.</p>
<h2>What we collect</h2><p>When you submit a form we receive the details you enter: name, company, work email, country or region, role, phone, shipping address for samples, and the content of your message. We do not ask for sensitive personal data.</p>
<h2>Why we use it</h2><ul><li>To answer your request, prepare samples, documents or quotations, and follow up on your project (steps taken at your request before a contract, and our legitimate interest in responding to business enquiries).</li><li>To keep records of business correspondence as required by law.</li></ul><p>We do not sell your data or use it for third-party marketing.</p>
<h2>Who processes it</h2><p>The website is hosted by Netlify, Inc., which also receives form submissions on our behalf. Data may therefore be processed outside your country, including in the United States and China, with appropriate safeguards where required.</p>
<h2>How long we keep it</h2><p>Enquiries that do not lead to business are deleted within 24 months. Records linked to orders are kept as long as accounting and legal rules require.</p>
<h2>Your rights</h2><p>Depending on where you live, including under the EU and UK GDPR, you may ask to access, correct or delete your data, object to or restrict its use, or receive a copy. You may also complain to your data protection authority. To exercise a right, email <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>, use the <a class="link" href="/contact/">contact form</a> or call {TEL}.</p>
<h2>Cookies</h2><p>This website does not use advertising or analytics cookies and does not track you across sites. Fonts and images are served from our own site. If we add analytics in the future, we will update this notice and ask for consent where the law requires it.</p>
<h2>Changes</h2><p>We may update this notice; the date above shows the latest version.</p>
<p class="tbl-note">This notice is provided for transparency and should be reviewed by legal counsel for your target markets.</p>
</div></section>'''
    write('/privacy/', 'Privacy & Cookies | POLYMER', 'How POLYMER handles personal data submitted through this website, and our cookie policy.', body)

    out = head('Page not found | POLYMER', 'The page you are looking for does not exist.', '/404.html', extra='<meta name="robots" content="noindex">\n') + header() + phero([('Not found', None)], 'This page <em>is not here.</em>', 'The link may be old or mistyped.', ctas=[('Back to home', '/', 'btn-primary'), ('Products', '/products/', 'btn-line')]) + footer()
    open(os.path.join(ROOT, '404.html'), 'w').write(out)


def build_meta():
    urls = ''.join(f'<url><loc>{BASE}{p}</loc><lastmod>2026-10-27</lastmod></url>\n' for p, _ in PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    facts = """- Company: Fujian Polymer Industry & Trade Co., Ltd. (brand POLYMER, 玻利玛), No. 2 Zhuli Road, Xiangcheng District, Zhangzhou, Fujian 363005, China. Founded 22 April 2019. USCC 91350602MA32PFWW73. China offices in Fuzhou, Quanzhou, Xiamen, Longyan, Guangdong and Zhejiang.
- Recognition: National High-Tech Enterprise; Fujian Specialised, Refined, Distinctive and Innovative SME (2025–2028); Fujian Innovative SME; Science and Technology-based SME; utility-model patents.
- Products: thermosetting powder coatings for metal — epoxy (indoor only), polyester (outdoor), epoxy-polyester hybrid (indoor decorative); standard-cure and low-cure grades.
- Certification: Qualicoat Class 1 for polyester system PLM100611 only (licence P-2199, gloss category 3, valid until 31 Dec 2026). ISO 9001:2015 (No. 05326Q01777R001) and ISO 14001:2015 (No. 05326E01349R001), issued by Beijing NGV Certification Center, valid 12 Oct 2026 – 11 Oct 2029, scope: design, manufacture and sales of thermosetting powder coatings (management systems, not product approvals). SGS report XMNEC26001081101 (12 May 2026): one black powder sample passed EU RoHS (EU) 2015/863, all ten substances not detected.
- Capacity and supply: 5,000 t per year (up to 500 t per month), 8 production lines, 5 sampling lines, 2 metallic bonding machines, standard lead time within 10 days, minimum order 1,000 kg, exports to about 20 countries and regions.
- Colours and finishes: RAL and customer colours; high gloss ≥90, satin/matt 11–80, dead matt ≤10; smooth, sand, wrinkle, vein, fine texture, hammer tone, pattern, bonded metallic, transparent/translucent, fluorescent.
- Testing (in-house): colorimeter and light box, 60° gloss meter, electromagnetic film thickness gauge, laser particle size analyser, screen-mesh sieving, pencil hardness, Erichsen impact, 180° bend, cross-cut adhesion 1 mm × 100, salt spray, UV accelerated weathering, oven temperature logging, storage stability 6 months below 30 °C.
- Process: formula → weighing → premix → melt extrusion → cooling → grinding and sieving → self-check → lab test → weighing and packing → warehouse; failed batches return to the formula stage.
- Not offered: Qualicoat Class 2/3, UL or flame-retardant coatings, IATF 16949, FBE/3PE pipeline or heavy-duty anticorrosion systems, orders below 1,000 kg, low-end powder.
- Contact: sales@polymerpaints.com; Tel +86 596 2600611; WhatsApp +86 158 2472 9376 / +86 188 5021 3808; https://polymerpaints.com/contact/"""
    pages = '\n'.join(f'- [{t}]({BASE}{p})' for p, t in PAGES)
    open(os.path.join(ROOT, 'llms.txt'), 'w').write(f"# POLYMER Powder Coatings\n\n> Manufacturer of epoxy, polyester and epoxy-polyester hybrid powder coatings for metal finishing, with a Qualicoat Class 1 approved polyester system, colour matching, special finishes and lead times within 10 days.\n\n## Key facts\n{facts}\n\n## Pages\n{pages}\n")
    full = f"# POLYMER Powder Coatings — full facts\n\n{facts}\n\n## Industry × system\n" + '\n'.join(f"- {i['name']}: main {', '.join(SYS[m]['name'] for m in i['main'])}" + (f"; option {', '.join(SYS[o]['name'] for o in i['opt'])}" if i['opt'] else '') + f". {i['oneliner']}" for i in IND) + "\n- Powder distributors: full range of all three systems plus effects.\n\n## FAQ\n"
    full += '\n'.join(f"### {f['q']}\n{f['short']} {' '.join(f['body'])}\n" for f in GEO['faq'])
    full += '\n## How-to guides\n' + '\n'.join(f"### {h['title']}\n{h['summary']}\n" + '\n'.join(f"{k+1}. {s['name']}: {s['text']}" for k, s in enumerate(h['steps'])) + '\n' for h in GEO['howto'])
    open(os.path.join(ROOT, 'llms-full.txt'), 'w').write(full)


def build_css():
    ff = open(os.path.join(ROOT, 'build/fontface.css')).read()
    home = open(os.path.join(ROOT, 'build/home.css')).read()
    extra = open(os.path.join(ROOT, 'build/extra.css')).read()
    open(os.path.join(ROOT, CSS.lstrip('/')), 'w').write(ff + '\n' + home + '\n' + extra)


# ---------------------------------------------------------------- RU / ES landing pages
def build_lang(code):
    L = I18N[code]; f = L['f']; a = L['aside']; nm = f'contact-{code}'
    fig = f'<figure class="tall">{img("home/hero-panels", 1122, 1402, "", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>'
    ct = f'<div class="hero-ctas"><a class="btn btn-primary" href="#contact">{L["cta1"]} {ARROW}</a><a class="btn btn-line" href="{wa_link(0)}" target="_blank" rel="noopener">{L["cta2"]}</a></div><p class="lng-en"><a href="/">{L["en"]} →</a></p>'
    body = f'''<section class="phero has-img"><div class="wrap"><div><nav class="crumbs" aria-label="Breadcrumb"><a href="/">POLYMER</a><span>{L["name"]}</span></nav><p class="eyebrow" style="margin-top:24px">{L["eyebrow"]}</p><h1>{L["h1"]}</h1><p class="lead">{L["lead"]}</p>{ct}</div>{fig}</div></section>
<section class="proof" style="background:var(--night)"><div class="wrap">{''.join(f'<div><strong>{x}</strong><span>{y}</span></div>' for x, y in L["stats"])}</div></section>'''
    cards = ''.join(f'<a class="card rv" href="{u}"><small>{e}</small><h3>{n}{"<span class=badge>Qualicoat</span>" if u.endswith("polyester/") else ""}</h3><p>{t}</p><span class="link">{L["more"]}</span></a>' for n, e, t, u in L['sys'])
    body += f'''<section class="sec"><div class="wrap"><div class="head rv"><div><p class="eyebrow">{L["sys_eyebrow"]}</p><h2 class="h2">{L["sys_h"]}</h2></div><p class="lead">{L["sys_lead"]}</p></div><div class="cards c3">{cards}</div></div></section>'''
    tiles = ''.join(f'<div class="tile rv"><figure>{img("finish/" + k, 800, 800, L["fin"][k], "(min-width:1060px) 20vw, (min-width:700px) 33vw, 50vw", 400)}</figure><h3>{L["fin"][k]}</h3></div>' for k, _, _ in FINISHES)
    bands = ''.join(f'<div>{n}<span>{v}</span></div>' for n, v in L['gloss'])
    body += f'''<section class="sec dark"><div class="wrap"><div class="head rv"><div><p class="eyebrow">{L["fin_eyebrow"]}</p><h2 class="h2">{L["fin_h"]}</h2></div><p class="lead">{L["fin_lead"]}</p></div><div class="atlas">{tiles}</div>
 <div class="gloss rv">{img("home/gloss-trio", 1536, 1024, "", "(min-width:980px) 60vw, 100vw", 768)}<div><div class="bands">{bands}</div></div></div></div></section>'''
    steps = ''.join(f'<li><span>{i + 1:02d}</span><div><b>{h}.</b> {t}</div></li>' for i, (h, t) in enumerate(L['proc']))
    body += f'''<section class="sec tight"><div class="wrap split"><div class="rv"><p class="eyebrow">{L["proc_eyebrow"]}</p><h2 class="h3" style="margin-top:20px">{L["proc_h"]}</h2></div><div class="rv"><ol class="list">{steps}</ol></div></div></section>'''
    certs = ''.join(f'<article class="cert{" key" if i == 0 else ""} rv"><h3>{h}</h3><p>{t}</p></article>' for i, (h, t) in enumerate(L['certs']))
    labs = photos([(n, c, c) for n, c in zip(['real/colorimeter', 'real/gloss', 'real/particle', 'real/bending'], L['lab_caps'])], 'c4')
    body += f'''<section class="sec tight alt"><div class="wrap"><div class="head rv"><div><p class="eyebrow">{L["q_eyebrow"]}</p><h2 class="h2">{L["q_h"]}</h2></div><p class="lead">{L["lab"]}</p></div><div class="certs lang-certs">{certs}</div><div style="margin-top:28px">{labs}</div></div></section>'''
    fac = photos([(n, c, c) for n, c in zip(['real/premixer', 'real/extruder', 'real/grinder', 'real/cone-mixer', 'real/bonding', 'real/loading'], L['fac_caps'])])
    body += f'''<section class="sec tight"><div class="wrap"><div class="head rv"><div><p class="eyebrow">{L["fac_eyebrow"]}</p><h2 class="h2">{L["fac_h"]}</h2></div><p class="lead">{L["fac_lead"]}</p></div>{fac}</div></section>'''
    dsteps = ''.join(f'<li><span>{i + 1:02d}</span><div><b>{h}</b> · {t}</div></li>' for i, (h, t) in enumerate(L['dist']))
    body += f'''<section class="sec tight dark"><div class="wrap split"><div class="rv"><p class="eyebrow">{L["dist_eyebrow"]}</p><h2 class="h3" style="margin-top:20px;color:#fff">{L["dist_h"]}</h2><p class="prose mt24" style="color:#b4b8bd">{L["dist_lead"]}</p></div><div class="rv"><ol class="list">{dsteps}</ol></div></div></section>'''
    faq = ''.join(f'<details><summary>{q}</summary><div class="a"><p>{t}</p></div></details>' for q, t in L['faq'])
    body += f'''<section class="sec tight"><div class="wrap split"><div class="rv"><p class="eyebrow">FAQ</p><h2 class="h3" style="margin-top:20px">{L["faq_h"]}</h2><p class="prose mt24"><a class="link" href="/faq/">FAQ · 40 answers (EN)</a></p></div><div class="rv"><div class="faq">{faq}</div></div></div></section>'''
    roles = ''.join(f'<option>{r}</option>' for r in f['roles'])
    form = f'''<form class="f" name="{nm}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="{nm}"><input type="hidden" name="language" value="{code}"><p class="hp"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
<div class="row two"><div class="fld"><label for="{nm}-name">{f["name"]} <i>*</i></label><input id="{nm}-name" name="name" autocomplete="name" required></div><div class="fld"><label for="{nm}-co">{f["company"]} <i>*</i></label><input id="{nm}-co" name="company" autocomplete="organization" required></div></div>
<div class="row two"><div class="fld"><label for="{nm}-mail">{f["email"]} <i>*</i></label><input id="{nm}-mail" type="email" name="email" autocomplete="email" required></div><div class="fld"><label for="{nm}-country">{f["country"]} <i>*</i></label><input id="{nm}-country" name="country" autocomplete="country-name" required></div></div>
<div class="row two"><div class="fld"><label for="{nm}-role">{f["role"]}</label><select id="{nm}-role" name="role"><option value="">{f["select"]}</option>{roles}</select></div></div>
<div class="row"><div class="fld"><label for="{nm}-need">{f["need"]} <i>*</i></label><textarea id="{nm}-need" name="message" required placeholder="{E(f["ph"])}"></textarea></div></div>
<label class="consent"><input type="checkbox" name="consent" required> <span>{f["consent"]} <i>*</i></span></label>
<div class="submit"><button class="btn btn-primary" type="submit">{f["btn"]}</button></div><p class="form-note">{f["note"]}</p></form>'''
    aside = f'''<aside class="aside"><div class="grp"><h3>{a["h"]}</h3><dl><dt>{a["email"]}</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd><dt>{a["phone"]}</dt><dd><a href="tel:+865962600611">{TEL}</a></dd><dt>{a["wa"]}</dt><dd><a href="{wa_link(0)}" target="_blank" rel="noopener">{WA[0][0]}</a><br><a href="{wa_link(1)}" target="_blank" rel="noopener">{WA[1][0]}</a></dd><dt>{a["resp"]}</dt><dd>{a["resp_v"]}</dd></dl></div></aside>'''
    body += f'''<section class="sec tight alt" id="contact"><div class="wrap"><div class="head rv"><div><p class="eyebrow">{L["c_eyebrow"]}</p><h2 class="h2">{L["c_h"]}</h2></div><p class="lead">{L["c_lead"]}</p></div><div class="form-grid">{form}{aside}</div></div></section>'''
    write(L['path'], L['title'], L['desc'], body, lang=code)


if __name__ == '__main__':
    build_css()
    build_home(); build_products(); build_finishes(); build_selector(); build_industries(); build_distributors()
    build_forms(); build_quality(); build_company(); build_geo(); build_legal(); build_lang('ru'); build_lang('es'); build_meta()
    print(len(PAGES), 'pages')
