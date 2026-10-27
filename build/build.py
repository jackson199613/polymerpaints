#!/usr/bin/env python3
"""Static site generator for polymerpaints.com. Run from repo root: python3 build/build.py"""
import json, os, re, html, sys
sys.path.insert(0, os.path.dirname(__file__))
from content_site import SYS, FINISHES, IND, DIST, STATS, IND_PHOTOS
IMG2 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img2_sizes.json')))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://polymerpaints.com'
CSS = '/assets/css/polymer-v1.css'
JS = '/assets/js/polymer-v1.js'
TEL = '+86 596 2600611'
ADDR = 'No. 2 Zhuli Road, Xiangcheng District, Zhangzhou, Fujian, China'
E = html.escape
GEO = json.load(open(os.path.join(ROOT, 'build/content_geo.json')))
PAGES = []  # (path, title) for sitemap
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
INDMAP = {i['slug']: i for i in IND}

ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": BASE + "/#org",
       "name": "POLYMER", "legalName": "Fujian Polymer Industry & Trade Co., Ltd.", "alternateName": "玻利玛",
       "url": BASE + "/", "foundingDate": "2019", "telephone": TEL,
       "slogan": "You apply powder, we apply care.",
       "address": {"@type": "PostalAddress", "streetAddress": "No. 2 Zhuli Road, Xiangcheng District", "addressLocality": "Zhangzhou", "addressRegion": "Fujian", "addressCountry": "CN"},
       "description": "Manufacturer of epoxy, polyester and epoxy-polyester hybrid powder coatings for metal finishing, with a Qualicoat Class 1 approved polyester system.",
       "hasCredential": [
           {"@type": "EducationalOccupationalCredential", "name": "Qualicoat Class 1 approval, polyester system PLM100611", "identifier": "P-2199", "validUntil": "2026-12-31"},
           {"@type": "EducationalOccupationalCredential", "name": "ISO 9001 quality management system"},
           {"@type": "EducationalOccupationalCredential", "name": "ISO 14001 environmental management system"}]}


def img(name, w, h, alt, sizes='100vw', small=None, lazy=True, cls=''):
    small = small or (IMG2[name][2] if name in IMG2 else (600 if w > 900 else 400))
    srcset = f'/assets/img/{name}-{small}.webp {small}w, /assets/img/{name}.webp {w}w'
    return (f'<img{" class=%s" % cls if cls else ""} src="/assets/img/{name}-{small}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{h}"{" loading=lazy" if lazy else " fetchpriority=high"} alt="{E(alt)}">')


def head(title, desc, path, ld=None, og='/assets/img/home/og.jpg'):
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
<html lang="en">
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
<link rel="preload" href="/assets/fonts/instrument-serif-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/manrope-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{CSS}">
{ldtxt}
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
  <div class="l"><span>Qualicoat Class 1 polyester system</span><span>ISO 9001</span><span>ISO 14001</span></div>
  <div class="r"><span>MOQ 1,000 kg</span><span>Lead time within 10 days</span><span><a href="tel:+865962600611">{TEL}</a></span></div>
</div></div>
<header class="site"><div class="wrap">
  <a class="logo" href="/" aria-label="POLYMER home"><b>POLYMER</b><small>Powder coatings</small></a>
  <nav class="main" aria-label="Main">
    <div class="dd"><a href="/products/"{cur('products')}>Products</a><div class="menu wide"><div><small>By system</small>{prod}<a href="/products/#cure">Low-cure grades</a></div><div><small>Choose &amp; compare</small><a href="/finishes/">Colours &amp; finishes</a><a href="/selector/">System selector</a><a href="/selector/#matrix">Industry × system table</a></div></div></div>
    <div class="dd"><a href="/industries/"{cur('industries')}>Industries</a><div class="menu"><small>By application</small>{inds}</div></div>
    <a href="/finishes/"{cur('finishes')}>Finishes</a>
    <a href="/distributors/"{cur('distributors')}>Distributors</a>
    <a href="/quality/"{cur('quality')}>Quality</a>
    <div class="dd"><a href="/faq/"{cur('resources')}>Resources</a><div class="menu"><a href="/faq/">Technical FAQ</a><a href="/how-to/">How-to guides</a><a href="/downloads/">Downloads</a><a href="/selector/">System selector</a></div></div>
    <a href="/company/"{cur('company')}>Company</a>
    <a href="/contact/"{cur('contact')}>Contact</a>
  </nav>
  <a class="btn btn-primary hdr-cta" href="/request-sample/">Request a sample</a>
  <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 7h18M3 12h18M3 17h18"/></svg></button>
</div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">
  <h4>Products</h4><a href="/products/">All products</a>{prod}<a href="/finishes/">Colours &amp; finishes</a><a href="/selector/">System selector</a>
  <h4>Industries</h4>{mob_inds}
  <h4>Company</h4><a href="/quality/">Quality &amp; certificates</a><a href="/company/">About POLYMER</a><a href="/faq/">Technical FAQ</a><a href="/how-to/">How-to guides</a><a href="/downloads/">Downloads</a><a href="/contact/">Contact</a>
  <a class="btn btn-primary" href="/request-sample/">Request a sample</a>
</nav>
<main id="main">'''


def footer():
    inds = ''.join(f'<li><a href="/industries/{i["slug"]}/">{E(i["short"])}</a></li>' for i in IND)
    return f'''</main>
<footer><div class="wrap">
  <div><a class="logo" href="/"><b style="color:#fff">POLYMER</b><small>Powder coatings</small></a>
    <p class="slogan">You apply powder,<br>we apply care.</p>
    <p>Fujian Polymer Industry &amp; Trade Co., Ltd.<br>No. 2 Zhuli Road, Xiangcheng District,<br>Zhangzhou, Fujian, China<br><a href="tel:+865962600611">Tel {TEL}</a></p></div>
  <div><h4>Products</h4><ul><li><a href="/products/polyester/">Polyester</a></li><li><a href="/products/hybrid/">Hybrid</a></li><li><a href="/products/epoxy/">Epoxy</a></li><li><a href="/finishes/">Colours &amp; finishes</a></li><li><a href="/selector/">System selector</a></li></ul></div>
  <div><h4>Industries</h4><ul>{inds}<li><a href="/distributors/">Distributors</a></li></ul></div>
  <div><h4>Company</h4><ul><li><a href="/company/">About POLYMER</a></li><li><a href="/quality/">Quality &amp; certificates</a></li><li><a href="/faq/">Technical FAQ</a></li><li><a href="/how-to/">How-to guides</a></li><li><a href="/downloads/">Downloads</a></li><li><a href="/contact/">Contact</a></li><li><a href="/request-sample/">Request a sample</a></li></ul></div>
  <div class="f-bottom"><span>© 2026 Fujian Polymer Industry &amp; Trade Co., Ltd. · <a href="/privacy/">Privacy &amp; cookies</a></span><span>Product data apply to stated conditions. Certificates apply to the scope stated on each certificate.</span></div>
</div></footer>
<script src="{JS}" defer></script>
</body>
</html>'''


def cta(title='Send us your most-used colour <em>and your hardest one.</em>', text='Tell us the part, environment, process and expected volume. We reply with a proposed system and a sample plan. Orders from 1,000 kg.', btn=('Send project details', '/contact/'), btn2=('Request a sample', '/request-sample/')):
    return f'''
<section class="cta" aria-label="Start a project">
  {img("home/cta-powder", 1916, 821, "", small=960).replace('<img ', '<img class="bg" ')}
  <div class="wrap">
    <p class="eyebrow" style="color:#c9a795">Start a project</p>
    <h2 class="h2">{title}</h2>
    <p>{E(text)}</p>
    <div class="hero-ctas" style="margin-top:0"><a class="btn btn-primary" href="{btn[1]}">{btn[0]} {ARROW}</a><a class="btn btn-line" href="{btn2[1]}">{btn2[0]}</a></div>
  </div>
</section>'''


def phero(crumbs, h1, lead, figure='', facts=None, ctas=None):
    cr = '<a href="/">Home</a>' + ''.join((f'<a href="{u}">{E(n)}</a>' if u else f'<span>{E(n)}</span>') for n, u in crumbs)
    fx = ('<div class="facts">' + ''.join(f'<span>{E(f)}</span>' for f in facts) + '</div>') if facts else ''
    ct = ''
    if ctas:
        ct = '<div class="hero-ctas">' + ''.join(f'<a class="btn {c}" href="{u}">{t}{" " + ARROW if c == "btn-primary" else ""}</a>' for t, u, c in ctas) + '</div>'
    return f'''
<section class="phero{' has-img' if figure else ''}">
  <div class="wrap">
    <div><nav class="crumbs" aria-label="Breadcrumb">{cr}</nav><h1>{h1}</h1><p class="lead">{lead}</p>{fx}{ct}</div>
    {figure}
  </div>
</section>'''


def write(path, title, desc, body, active='', ld=None, og='/assets/img/home/og.jpg', sitemap=True):
    out = head(title, desc, path, ld, og) + header(active) + body + footer()
    fp = os.path.join(ROOT, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(ROOT, path.strip('/'))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(out)
    if sitemap: PAGES.append((path, title))


def fig2(name, alt, cap):
    w, h, sm = IMG2[name]
    return f'<figure class="figure rv">{img(name, w, h, alt, "(min-width:1280px) 1192px, 100vw", sm)}<figcaption><b>{E(cap[0])}.</b> {E(cap[1])}</figcaption></figure>'


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
        out += f'<details id="{f["slug"]}"><summary>{E(f["q"])}</summary><div class="a"><p class="short">{E(f["short"])}</p>{body}<p class="basis">Basis: {E(f["basis"])}</p></div></details>'
    return out + '</div>'


# ---------------------------------------------------------------- home
def build_home():
    src = open(os.path.join(ROOT, 'build/home_main.html')).read()
    write('/', 'POLYMER Powder Coatings | Epoxy, Polyester & Hybrid Powder Coatings, China',
          'Fujian Polymer manufactures epoxy, polyester and epoxy-polyester hybrid powder coatings for metal finishing, with a Qualicoat Class 1 approved polyester system, colour matching, special finishes and lead times within 10 days.',
          src, ld=[{"@context": "https://schema.org", "@type": "WebSite", "name": "POLYMER Powder Coatings", "url": BASE + "/"}])


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
            extra = '''<section class="sec tight dark"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Architectural approval</p><h2 class="h3" style="margin-top:20px;color:#fff">Qualicoat Class 1, <em style="color:var(--accent-hi)">with its scope.</em></h2></div>
  <div class="rv"><dl class="kv" style="border-color:var(--night-line)">
   <dt>Licence</dt><dd style="color:#e9e6e0">P-2199</dd><dt>System</dt><dd style="color:#e9e6e0">Polyester PLM100611, gloss category 3</dd><dt>Valid</dt><dd style="color:#e9e6e0">Until 31 December 2026</dd><dt>Scope</dt><dd style="color:#e9e6e0">The approved polyester system only. Not all products or colours; no structured-texture or metallic extension; not Class 2 or Class 3.</dd></dl>
   <p class="mt24"><a class="link" href="/quality/">Quality &amp; certificates</a></p></div></div></section>'''
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
  <div class="rv"><dl class="kv"><dt>Capacity</dt><dd>5,000 t per year on 9 production lines</dd><dt>Lead time</dt><dd>Standard within 10 days; complex custom colours and large volumes confirmed per order</dd><dt>Minimum order</dt><dd>1,000 kg per order</dd><dt>Export</dt><dd>About 20 countries and regions; experienced with export documents, packing and sea freight</dd><dt>Documents</dt><dd>ISO 9001 and ISO 14001 certificates and the Qualicoat Class 1 certificate for your sales pack</dd></dl></div>
</div></section>
<section class="sec tight alt" id="apply"><div class="wrap form-grid">
  {form_distributor()}
  <aside class="aside"><h3>What happens next</h3><p>We reply within one working day with the starter pack and a call to understand your end-user structure.</p><h3>Direct</h3><ul><li><a href="tel:+865962600611">Tel {TEL}</a></li><li>{ADDR}</li></ul><h3>Useful</h3><ul><li><a href="/selector/#matrix">Industry × system table</a></li><li><a href="/faq/#distributor-cooperation-terms">Cooperation terms FAQ</a></li></ul></aside>
</div></section>'''
    body += cta(title='Serve your whole market <em>from one supplier.</em>', text='Tell us your market, end-user mix and monthly volume. We propose a first range and a starter pack.', btn=('Apply as distributor', '#apply'), btn2=('Downloads', '/downloads/'))
    write('/distributors/', 'Powder Coating Distributors & Importers: Partner Programme | POLYMER',
          'A combined polyester, hybrid and epoxy range plus effects for powder coating importers and distributors, with a standard lead time within 10 days and a non-exclusive start.', body, 'distributors')


# ---------------------------------------------------------------- forms
def consent():
    return '<label class="consent"><input type="checkbox" name="consent" required> <span>I agree that POLYMER may use these details to answer my request, as described in the <a href="/privacy/">privacy notice</a>. <i style="color:var(--accent);font-style:normal">*</i></span></label>'


def common_fields():
    return '''<div class="row two"><div class="fld"><label for="f-name">Name <i>*</i></label><input id="f-name" name="name" autocomplete="name" required></div><div class="fld"><label for="f-co">Company <i>*</i></label><input id="f-co" name="company" autocomplete="organization" required></div></div>
<div class="row two"><div class="fld"><label for="f-mail">Work email <i>*</i></label><input id="f-mail" type="email" name="email" autocomplete="email" required></div><div class="fld"><label for="f-country">Country / region <i>*</i></label><input id="f-country" name="country" autocomplete="country-name" required></div></div>
<div class="row two"><div class="fld"><label for="f-role">Your role</label><select id="f-role" name="role"><option value="">Select</option><option>Purchasing</option><option>Owner / General manager</option><option>Sourcing</option><option>Production / coating line</option><option>Technical / QC</option><option>Distributor</option><option>Other</option></select></div><div class="fld"><label for="f-phone">Phone / WhatsApp</label><input id="f-phone" name="phone" autocomplete="tel"></div></div>'''


def form_open(name):
    return f'<form class="f" name="{name}" method="POST" action="/thanks/" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="{name}"><p class="hp"><label>Leave empty <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>'


def form_close(btn):
    return f'{consent()}<button class="btn btn-primary" type="submit">{btn} {ARROW}</button><p class="form-note">* Required. We use your details only to answer this request and do not share them for marketing.</p></form>'


def form_distributor():
    return (form_open('distributor') + common_fields() +
            '''<div class="row two"><div class="fld"><label for="f-mk">Market / territory <i>*</i></label><input id="f-mk" name="market" required></div><div class="fld"><label for="f-vol">Monthly powder volume</label><select id="f-vol" name="volume"><option value="">Select</option><option>1–5 t</option><option>5–20 t</option><option>20–50 t</option><option>50 t +</option></select></div></div>
<div class="row"><div class="fld"><label for="f-need">Your business <i>*</i></label><textarea id="f-need" name="message" required placeholder="End users you serve (applicators, aluminium, furniture, cabinets, appliances), current suppliers, warehousing and technical sales"></textarea></div></div>''' + form_close('Apply as distributor'))


def build_forms():
    why = '''<div class="why"><p class="eyebrow">What we ask for, and why</p><div class="cards c4">
 <div class="card"><small>Part</small><h3 style="font-size:24px">What it is</h3><p>Use, substrate, size and a photo or sample. It decides the system.</p></div>
 <div class="card"><small>Environment</small><h3 style="font-size:24px">Where it lives</h3><p>Indoor or outdoor, humidity, coastal, chemicals, temperature.</p></div>
 <div class="card"><small>Appearance</small><h3 style="font-size:24px">How it looks</h3><p>Colour code or sample, gloss, texture or metallic target.</p></div>
 <div class="card"><small>Process</small><h3 style="font-size:24px">How you coat</h3><p>Pretreatment, film thickness, spray equipment and actual cure.</p></div></div></div>'''
    sys_opts = ''.join(f'<option>{s["name"]}</option>' for s in SYS.values())
    fin_opts = ''.join(f'<option>{n}</option>' for _, n, _ in FINISHES)
    ind_opts = ''.join(f'<option>{E(i["short"])}</option>' for i in IND) + '<option>Powder distributor</option><option>Other</option>'
    sample = (form_open('sample') + common_fields() +
              f'''<div class="row two"><div class="fld"><label for="f-ind">Industry</label><select id="f-ind" name="industry" data-prefill="industry"><option value="">Select</option>{ind_opts}</select></div><div class="fld"><label for="f-sys">System of interest</label><select id="f-sys" name="system" data-prefill="system"><option value="">Not sure</option>{sys_opts}</select></div></div>
<div class="row two"><div class="fld"><label for="f-fin">Finish</label><select id="f-fin" name="finish" data-prefill="finish"><option value="">Select</option>{fin_opts}</select></div><div class="fld"><label for="f-col">Colour reference</label><input id="f-col" name="colour" placeholder="e.g. RAL 7016, or physical sample to follow"></div></div>
<div class="row"><div class="fld"><label for="f-need">What do you need? <i>*</i></label><textarea id="f-need" name="message" required data-prefill-summary placeholder="Part and substrate, indoor or outdoor, gloss, pretreatment, film thickness, cure, current product and expected volume (from 1,000 kg)"></textarea></div></div>
<div class="row"><div class="fld"><label for="f-ship">Shipping address for samples <i>*</i></label><textarea id="f-ship" name="address" required style="min-height:90px" autocomplete="street-address"></textarea></div></div>''' + form_close('Request samples'))
    aside = f'''<aside class="aside"><h3>Direct contact</h3><ul><li><a href="tel:+865962600611">Tel {TEL}</a></li><li>Replies within one working day, Mon–Sat (UTC+8)</li></ul><h3>Company</h3><p>Fujian Polymer Industry &amp; Trade Co., Ltd.<br>{ADDR}</p><h3>Useful</h3><ul><li><a href="/selector/">System selector</a></li><li><a href="/how-to/prepare-colour-matching-request/">Prepare a colour-matching request</a></li><li><a href="/downloads/">Downloads</a></li><li><a href="/faq/">Technical FAQ</a></li></ul></aside>'''
    fig = f'<figure>{img("home/sample-kit", 1536, 1024, "Sample box with three powder-coated panels and powder sachets", "(min-width:980px) 45vw, 100vw", 768, lazy=False)}</figure>'
    body = phero([('Request a sample', None)], 'Panels in your colour, <em>before you commit.</em>',
                 'Tell us the part, environment and target appearance. We propose a system, match the colour and send panels or powder for a trial on your line.', figure=fig,
                 facts=['Matched to your colour', 'Approved version recorded', 'Orders from 1,000 kg'])
    body += f'<section class="sec tight"><div class="wrap"><div class="form-grid">{sample}{aside}</div>{why}</div></section>'
    write('/request-sample/', 'Request a Powder Coating Sample | POLYMER', 'Request powder coating panels or powder in your colour and finish for evaluation and line trials.', body)

    contact = (form_open('contact') + common_fields() +
               '''<div class="row"><div class="fld"><label for="f-topic">Topic</label><select id="f-topic" name="topic" data-prefill="topic"><option value="">Select</option><option value="project">New project / quotation</option><option value="colour">Colour matching</option><option value="documents">Documents (TDS, SDS, certificates)</option><option value="distributor">Distributor cooperation</option><option value="other">Other</option></select></div></div>
<div class="row"><div class="fld"><label for="f-need">What do you need? <i>*</i></label><textarea id="f-need" name="message" required placeholder="Part and substrate, environment, colour and finish, process, current product and expected volume"></textarea></div></div>''' + form_close('Send message'))
    body = phero([('Contact', None)], 'Talk to <em>our team.</em>', 'For projects, colour matching, documents or distributor cooperation. We reply within one working day.',
                 facts=['Tel ' + TEL, 'Zhangzhou, Fujian, China'])
    body += f'<section class="sec tight"><div class="wrap"><div class="form-grid">{contact}{aside}</div>{why}</div></section>'
    write('/contact/', 'Contact POLYMER Powder Coatings', 'Contact Fujian Polymer about powder coating projects, colour matching, documents or distributor cooperation.', body, 'contact')

    body = phero([('Thank you', None)], 'Thank you, <em>we have it.</em>', 'We reply within one working day. If your request is urgent, call us on ' + TEL + '.',
                 ctas=[('Back to home', '/', 'btn-primary'), ('Read the technical FAQ', '/faq/', 'btn-line')])
    write('/thanks/', 'Thank you | POLYMER', 'Your message has been received.', body, sitemap=False)

    docs = [('Product catalogue', 'Three systems, cure grades, gloss bands and effects'), ('Technical data sheets (TDS)', 'Per product: properties, cure conditions, storage'), ('Safety data sheets (SDS)', 'Per product: safe handling and transport'),
            ('Qualicoat Class 1 certificate', 'Polyester system PLM100611, P-2199'), ('ISO 9001 certificate', 'Quality management system'), ('ISO 14001 certificate', 'Environmental management system'), ('Colour cards and panels', 'Physical samples for evaluation')]
    checks = ''.join(f'<label><input type="checkbox" name="documents" value="{E(n)}"> {E(n)}</label>' for n, _ in docs)
    cards = ''.join(f'<div class="card rv"><small>On request</small><h3 style="font-size:24px">{E(n)}</h3><p>{E(d)}</p></div>' for n, d in docs)
    dform = (form_open('documents') + common_fields() + f'<div class="row"><div class="fld"><label>Documents needed <i>*</i></label><div class="checks">{checks}</div></div></div><div class="row"><div class="fld"><label for="f-need">Products or project</label><textarea id="f-need" name="message" style="min-height:90px" placeholder="Which products or applications the documents are for"></textarea></div></div>' + form_close('Request documents'))
    body = phero([('Resources', '/faq/'), ('Downloads', None)], 'Documents for <em>your approval file.</em>', 'Catalogue, TDS, SDS and certificates are sent by email on request, so each file matches the product you are evaluating and the latest version.',
                 figure=f'<figure>{img("ind/distributors-b", 1536, 1024, "Colour panels, colour card and powder sample", "(min-width:980px) 45vw, 100vw", 768, lazy=False)}</figure>', facts=['TDS', 'SDS', 'Certificates', 'Catalogue'])
    body += f'<section class="sec tight"><div class="wrap"><div class="cards c4">{cards}</div></div></section><section class="sec tight alt"><div class="wrap form-grid">{dform}{aside}</div></section>'
    body += cta()
    write('/downloads/', 'Downloads: TDS, SDS, Certificates & Catalogue | POLYMER', 'Request powder coating technical data sheets, safety data sheets, ISO and Qualicoat certificates and the product catalogue.', body, 'resources')


# ---------------------------------------------------------------- quality
def build_quality():
    tests = [('Colour measurement', 'Colour difference against the approved panel'), ('Gloss', 'Gloss band and consistency'), ('Film thickness', 'Coverage and film build on panels'), ('Particle size', 'Powder particle size distribution'),
             ('Salt spray', 'Corrosion behaviour on panels'), ('UV accelerated ageing', 'Colour and gloss behaviour under UV'), ('Hardness', 'Surface hardness'), ('Impact', 'Resistance to impact'), ('Bend', 'Flexibility on bending'), ('Adhesion', 'Coating adhesion to the substrate')]
    rows = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in tests)
    body = phero([('Quality', None)], 'Every claim, <em>with its scope.</em>', 'What each certificate covers, how we test panels and batches, and how the approved version keeps repeat orders consistent.',
                 figure=f'<figure class="tall">{img("home/panel-single", 1122, 1402, "An approved test panel on a black plinth", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>',
                 facts=['Qualicoat Class 1 · P-2199', 'ISO 9001', 'ISO 14001'])
    body += f'''<section class="sec tight"><div class="wrap">
  <div class="certs">
   <article class="cert key rv"><small>Architectural coating approval</small><h3>Qualicoat Class 1</h3><dl><dt>Licence</dt><dd>P-2199</dd><dt>System</dt><dd>Polyester PLM100611 · gloss category 3</dd><dt>Valid</dt><dd>Until 31 Dec 2026</dd><dt>Scope</dt><dd>The approved polyester system only. Not all products or colours; no structured-texture or metallic extension; not Class 2 or 3.</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
   <article class="cert rv"><small>Quality management</small><h3>ISO 9001</h3><dl><dt>Type</dt><dd>Management system certification, not a product approval</dd><dt>Use</dt><dd>Supplier approval and distributor packs</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
   <article class="cert rv"><small>Environmental management</small><h3>ISO 14001</h3><dl><dt>Type</dt><dd>Management system certification, not a product approval</dd><dt>Use</dt><dd>Environmental purchasing questions</dd></dl><a class="link" href="/downloads/">Request certificate</a></article>
  </div></div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">In-house test conditions</p><h2 class="h3" style="margin-top:20px">What we check <em>on panels and batches.</em></h2><p class="prose mt24">Used for panel evaluation, outgoing inspection and project discussions. These are internal test conditions, not third-party reports. If your project needs an independent report, tell us early.</p></div>
  <div class="rv"><div class="tbl-wrap"><table class="tbl" style="min-width:420px"><thead><tr><th>Test</th><th>What it shows</th></tr></thead><tbody>{rows}</tbody></table></div></div>
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
    write('/quality/', 'Quality & Certificates: Qualicoat Class 1, ISO 9001, ISO 14001 | POLYMER',
          'Qualicoat Class 1 for polyester system PLM100611 (P-2199), ISO 9001 and ISO 14001 management systems, in-house test conditions and approved-panel version control.', body, 'quality')


# ---------------------------------------------------------------- company
def build_company():
    stats = ''.join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in STATS)
    body = phero([('Company', None)], 'Powder coatings for metal, <em>made with care.</em>',
                 'Fujian Polymer Industry &amp; Trade Co., Ltd. was founded in 2019 in Zhangzhou, Fujian. We make thermosetting powder coatings for metal protection and decoration, and supply distributors, metal product manufacturers and coating applicators.',
                 figure=f'<figure class="tall">{img("home/hero-panels", 1122, 1402, "Powder-coated panels in five finishes", "(min-width:980px) 40vw, 100vw", lazy=False)}</figure>')
    body += f'''<section class="proof" style="background:var(--night)"><div class="wrap">{stats}</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">What we do</p><h2 class="h3" style="margin-top:20px">The right system, the matched colour, <em>on time.</em></h2></div>
  <div class="rv prose"><p>We produce three powder systems: epoxy for indoor functional parts, polyester for outdoor parts, and epoxy-polyester hybrid for indoor decorative parts. Our polyester system PLM100611 is Qualicoat Class 1 approved.</p><p>Our work starts from the customer’s part and where it will be used. We recommend the system, match the colour and finish, and record the approved panel so every batch can be checked against it. Standard lead time is within 10 days, and we do not make low-end powder.</p><h3>Who we supply</h3><ul><li>Powder importers and distributors, our main channel</li><li>Aluminium extruders, metal furniture, appliance, enclosure and equipment manufacturers</li><li>Professional coating applicators ordering from 1 t</li></ul></div>
</div></section>
<section class="sec tight dark"><div class="wrap">
  <div class="head rv"><div><p class="eyebrow">Where we export</p><h2 class="h2">About 20 countries <em>and regions.</em></h2></div><p class="lead">Experienced with export documents, packing and sea freight to our established markets.</p></div>
  <div class="regions">
   <div class="region rv"><h3>Russia &amp; CIS</h3><p>Distributors and manufacturers; colours, textures and effects that complement local supply.</p></div>
   <div class="region rv"><h3>Latin America</h3><p>Distributors and end users in aluminium, furniture and appliance supply chains.</p></div>
   <div class="region rv"><h3>Africa</h3><p>Importers and wholesalers serving applicators and manufacturers.</p></div>
  </div>
</div></section>
<section class="sec tight"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Manufacturing</p><h2 class="h3" style="margin-top:20px">Capacity <em>and control.</em></h2></div>
  <div class="rv"><dl class="kv"><dt>Capacity</dt><dd>5,000 t per year</dd><dt>Production</dt><dd>9 production lines</dd><dt>Metallics</dt><dd>2 metallic bonding machines, which help reduce separation of metallic pigment during spraying and reclaim</dd><dt>Testing</dt><dd>Colour, gloss, film thickness, particle size, salt spray, UV accelerated ageing, hardness, impact, bend and adhesion (in-house)</dd><dt>Systems</dt><dd>ISO 9001 quality management · ISO 14001 environmental management</dd></dl><p class="tbl-note">Factory and laboratory photographs will be added here.</p></div>
</div></section>
<section class="sec tight alt"><div class="wrap split">
  <div class="rv"><p class="eyebrow">Environment</p><h2 class="h3" style="margin-top:20px">Powder, <em>by nature.</em></h2></div>
  <div class="rv prose"><p>Powder coatings are applied as a dry powder and contain no solvent carrier, and oversprayed powder can be reclaimed and reused on many lines. Our environmental management system is certified to ISO 14001.</p><p>We make no further environmental claims without data. If your purchasing team needs specific declarations, ask us and we will confirm what can be supplied for the product concerned.</p></div>
</div></section>'''
    body += cta()
    write('/company/', 'About POLYMER | Fujian Polymer Industry & Trade Co., Ltd.',
          'Founded in 2019 in Zhangzhou, Fujian, POLYMER makes epoxy, polyester and hybrid powder coatings with 5,000 t annual capacity, 9 lines and a standard lead time within 10 days.', body, 'company')


# ---------------------------------------------------------------- faq + how-to
def build_geo():
    qa = [{"@type": "Question", "name": f['q'], "acceptedAnswer": {"@type": "Answer", "text": f['short'] + ' ' + ' '.join(f['body'])}} for f in GEO['faq']]
    body = phero([('Resources', None), ('Technical FAQ', None)], 'Questions buyers <em>ask first.</em>', 'Short answers first, then the detail and what each answer is based on.',
                 ctas=[('How-to guides', '/how-to/', 'btn-line')])
    body += f'<section class="sec tight"><div class="wrap split"><div class="rv"><p class="eyebrow">{len(GEO["faq"])} answers</p><h2 class="h3" style="margin-top:20px">Systems, colour, supply <em>and documents.</em></h2><p class="prose mt24">Not covered here? <a class="link" href="/contact/">Ask our team</a></p></div><div class="rv">{faq_block([f["slug"] for f in GEO["faq"]])}</div></div></section>'
    body += cta()
    write('/faq/', 'Powder Coating Technical FAQ | POLYMER', 'Answers on choosing epoxy, polyester or hybrid, Qualicoat Class 1 scope, MOQ, lead time, colour matching, effects, low-cure, documents and testing.', body, 'resources',
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
<h2>Your rights</h2><p>Depending on where you live, including under the EU and UK GDPR, you may ask to access, correct or delete your data, object to or restrict its use, or receive a copy. You may also complain to your data protection authority. To exercise a right, use the <a class="link" href="/contact/">contact form</a> or call {TEL}.</p>
<h2>Cookies</h2><p>This website does not use advertising or analytics cookies and does not track you across sites. Fonts and images are served from our own site. If we add analytics in the future, we will update this notice and ask for consent where the law requires it.</p>
<h2>Changes</h2><p>We may update this notice; the date above shows the latest version.</p>
<p class="tbl-note">This notice is provided for transparency and should be reviewed by legal counsel for your target markets.</p>
</div></section>'''
    write('/privacy/', 'Privacy & Cookies | POLYMER', 'How POLYMER handles personal data submitted through this website, and our cookie policy.', body)

    out = head('Page not found | POLYMER', 'The page you are looking for does not exist.', '/404.html') + header() + phero([('Not found', None)], 'This page <em>is not here.</em>', 'The link may be old or mistyped.', ctas=[('Back to home', '/', 'btn-primary'), ('Products', '/products/', 'btn-line')]) + footer()
    open(os.path.join(ROOT, '404.html'), 'w').write(out)


def build_meta():
    urls = ''.join(f'<url><loc>{BASE}{p}</loc><lastmod>2026-10-27</lastmod></url>\n' for p, _ in PAGES)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    facts = """- Company: Fujian Polymer Industry & Trade Co., Ltd. (brand POLYMER, 玻利玛), Zhangzhou, Fujian, China. Founded 2019.
- Products: thermosetting powder coatings for metal — epoxy (indoor only), polyester (outdoor), epoxy-polyester hybrid (indoor decorative); standard-cure and low-cure grades.
- Certification: Qualicoat Class 1 for polyester system PLM100611 only (licence P-2199, gloss category 3, valid until 31 Dec 2026). ISO 9001 and ISO 14001 management systems (not product approvals).
- Capacity and supply: 5,000 t per year, 9 production lines, 2 metallic bonding machines, standard lead time within 10 days, minimum order 1,000 kg, exports to about 20 countries and regions.
- Colours and finishes: RAL and customer colours; high gloss ≥90, satin/matt 11–80, dead matt ≤10; smooth, sand, wrinkle, vein, fine texture, hammer tone, pattern, bonded metallic, transparent/translucent, fluorescent.
- Testing: in-house colour, gloss, film thickness, particle size, salt spray, UV accelerated ageing, hardness, impact, bend, adhesion (internal, not third-party reports).
- Not offered: Qualicoat Class 2/3, UL or flame-retardant coatings, IATF 16949, FBE/3PE pipeline or heavy-duty anticorrosion systems, orders below 1,000 kg, low-end powder.
- Contact: Tel +86 596 2600611; https://polymerpaints.com/contact/"""
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


if __name__ == '__main__':
    build_css()
    build_home(); build_products(); build_finishes(); build_selector(); build_industries(); build_distributors()
    build_forms(); build_quality(); build_company(); build_geo(); build_legal(); build_meta()
    print(len(PAGES), 'pages')
