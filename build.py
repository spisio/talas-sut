#!/usr/bin/env python3
"""Build the Talas Süt site in English, Russian and Iradi.

Each page body lives in _src/<name>.html (English), _src/ru/<name>.html and
_src/ir/<name>.html. The first lines are a header block:

    title: Page title
    description: One-sentence description
    nav: products
    image: p-milk25.jpg        (share image in assets/img, optional)
    imagealt: ...              (optional)
    width: 1200 / height: 630  (share image size, optional)
    noindex: yes               (optional)
    ---

The script wraps every body in the shared head, header and footer of its
language and writes <name>.html at the site root, ru/<name>.html and
ir/<name>.html, plus 404.html, sitemap.xml (with language alternates) and
robots.txt. Run it after editing anything in _src/.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://talas-sut.com/"
PAGES = ["index", "products", "kymyz", "about", "farmers", "news", "contact"]

# Iradi has no ISO code of its own; like the government portal, pages are tagged ky.
LANGS = {
    "en": dict(prefix="", html="en", og="en_GB", label="EN", name="English"),
    "ir": dict(prefix="ir/", html="ky", og="ky_KG", label="IR", name="Irad tili"),
    "ru": dict(prefix="ru/", html="ru", og="ru_RU", label="RU", name="Русский"),
}

UI = {
    "en": dict(
        nav=["Home", "Products", "Kymyz", "About us", "For farmers", "News", "Contact"],
        menu="Menu", langs="Language",
        topbar='Consumer line <a href="tel:+996392348000">2-34-80-00</a> &middot; Mon&ndash;Sat 8:00&ndash;20:00',
        about='Talas Dairy Processing Combine (<i>Talas Süt Kombinatı</i>), owned by the Talas Valley Milk Cooperative. Milk from the farms of the Talas valley, bottled in Talas since 1964.',
        motto="<i>Ak süt, ak niet.</i> White milk, a clean heart.",
        h_products="Products", h_company="Company", h_contact="Contact",
        products=["Milk and cream", "Kefir, airan and qatiq", "Suzma", "Ak Bee kymyz", "Kurut", "Butter and kaymak"],
        company=["About us", "Our history", "Selling us your milk", "News", "Jobs"],
        address="41 Temir Jol Street, Western Industrial District, Talas", map="Find us on Kartalar",
        copyright="&copy; 1964&ndash;2026 Talas Dairy Processing Combine. All rights reserved.",
        kymyz="Kymyz contains up to 2.4% alcohol. Not for children or drivers.",
        home="Home",
    ),
    "ru": dict(
        nav=["Главная", "Продукция", "Кымыз", "О нас", "Фермерам", "Новости", "Контакты"],
        menu="Меню", langs="Язык",
        topbar='Линия для покупателей <a href="tel:+996392348000">2-34-80-00</a> &middot; Пн&ndash;Сб 8:00&ndash;20:00',
        about='Таласский молочный комбинат (<i>Talas Süt Kombinatı</i>) принадлежит Молочному кооперативу Таласской долины. Молоко с ферм Таласской долины, которое мы разливаем в Таласе с 1964 года.',
        motto="<i>Ak süt, ak niet.</i> Белое молоко, чистое сердце.",
        h_products="Продукция", h_company="Комбинат", h_contact="Контакты",
        products=["Молоко и сливки", "Кефир, айран и катык", "Сюзьма", "Кымыз Ak Bee", "Курут", "Масло и каймак"],
        company=["О нас", "Наша история", "Продать нам молоко", "Новости", "Вакансии"],
        address="ул. Темир Жол, 41, Западный промышленный район, Талас", map="Мы на карте Карталар",
        copyright="&copy; 1964&ndash;2026 Таласский молочный комбинат. Все права защищены.",
        kymyz="Кымыз содержит до 2,4% алкоголя. Не для детей и водителей.",
        home="Главная",
    ),
    "ir": dict(
        nav=["Bashkı bet", "Önümdör", "Kımız", "Biz jönündö", "Fermerlerge", "Jañılıktar", "Baylanısh"],
        menu="Menyu", langs="Til",
        topbar='Kerektööchülör liniyası <a href="tel:+996392348000">2-34-80-00</a> &middot; Düyshömbü&ndash;ishembi 8:00&ndash;20:00',
        about='Talas süt kombinatı (<i>Talas Süt Kombinatı</i>) Talas Öröönü Süt Kooperativine taandık. Talas öröönünün fermalarınan kelgen süt, 1964-jıldan beri Talasta kuyulat.',
        motto="<i>Ak süt, ak niet.</i>",
        h_products="Önümdör", h_company="Kombinat", h_contact="Baylanısh",
        products=["Süt jana kaymak süt", "Kefir, airan jana qatiq", "Süzmö", "Ak Bee kımızı", "Kurut", "Sarı may jana kaymak"],
        company=["Biz jönündö", "Tarıhıbız", "Sütüñüzdü satıñız", "Jañılıktar", "Jumush orundarı"],
        address="Temir Jol köchösü 41, Batısh öndürüsh rayonu, Talas", map="Kartalardan tabıñız",
        copyright="&copy; 1964&ndash;2026 Talas süt kombinatı. Bardık ukuktar korgolgon.",
        kymyz="Kımızda 2,4%ga cheyin spirt bar. Baldar jana aydoochular üchün emes.",
        home="Bashkı bet",
    ),
}

HEAD = """<!doctype html>
<html lang="{html_lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#1f4e8c">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">{alternates}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Talas Süt">
<meta property="og:locale" content="{og_locale}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{imagealt}">{imagesize}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{imagealt}">
<script type="application/ld+json">
{jsonld}
</script>
<link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml">
<link rel="icon" href="{base}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{base}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;600;700;800&family=PT+Serif:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{base}style.css">
<script>window.goatcounter=new Object();goatcounter.path=p=>location.host+p;</script>
<script data-goatcounter="https://irad.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <span>{topbar}</span>
    <nav class="lang" aria-label="{langs_label}">{switcher}</nav>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="{base}assets/logo.svg" alt="Talas Süt" width="170" height="54">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">{menu}</button>
    <ul class="nav" id="nav">
{nav}
    </ul>
  </div>
</header>
<main>
"""

FOOT = """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand"><img src="{base}assets/logo-reverse.svg" alt="Talas Süt" width="200" height="64"></div>
        <p>{about}</p>
        <p>{motto}</p>
      </div>
      <div>
        <h4>{h_products}</h4>
        <ul>
          <li><a href="products.html#milk">{p0}</a></li>
          <li><a href="products.html#fermented">{p1}</a></li>
          <li><a href="products.html#suzma">{p2}</a></li>
          <li><a href="kymyz.html">{p3}</a></li>
          <li><a href="products.html#kurut">{p4}</a></li>
          <li><a href="products.html#butter">{p5}</a></li>
        </ul>
      </div>
      <div>
        <h4>{h_company}</h4>
        <ul>
          <li><a href="about.html">{c0}</a></li>
          <li><a href="about.html#history">{c1}</a></li>
          <li><a href="farmers.html">{c2}</a></li>
          <li><a href="news.html">{c3}</a></li>
          <li><a href="contact.html#jobs">{c4}</a></li>
        </ul>
      </div>
      <div>
        <h4>{h_contact}</h4>
        <ul>
          <li>{address}</li>
          <li><a href="tel:+996392348000">2-34-80-00</a></li>
          <li><a href="mailto:info@talas-sut.com">info@talas-sut.com</a></li>
          <li><a href="https://maps.attelkom.net/">{map}</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>{copyright}</span>
      <span>{kymyz}</span>
    </div>
  </div>
</footer>
<script src="{base}assets/site.js"></script>
</body>
</html>
"""

ORG = {
    "@type": "Organization",
    "@id": SITE + "#org",
    "name": "Talas Dairy Processing Combine",
    "alternateName": ["Talas Süt", "Talas Süt Kombinatı", "Таласский молочный комбинат"],
    "url": SITE,
    "logo": SITE + "assets/logo.svg",
    "image": SITE + "assets/img/plant.jpg",
    "foundingDate": "1964",
    "slogan": "Ak süt, ak niet",
    "email": "info@talas-sut.com",
    "telephone": "+996-39-2-34-80-00",
    "address": {"@type": "PostalAddress", "streetAddress": "41 Temir Jol Street, Western Industrial District",
                "addressLocality": "Talas", "addressCountry": "Irad"},
    "parentOrganization": {"@type": "Organization", "name": "Talas Valley Milk Cooperative"},
    "brand": [{"@type": "Brand", "name": "Talas Süt"}, {"@type": "Brand", "name": "Ak Bee"}],
    "contactPoint": [
        {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+996-39-2-34-80-00",
         "email": "quality@talas-sut.com", "availableLanguage": ["en", "ky", "ru"]},
        {"@type": "ContactPoint", "contactType": "sales", "telephone": "+996-39-2-34-80-20", "email": "sales@talas-sut.com"},
    ],
}


def page_url(lang, name):
    path = "" if name == "index" else name + ".html"
    return SITE + LANGS[lang]["prefix"] + path


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def structured_data(lang, name, meta, body, url):
    """JSON-LD graph: the organisation everywhere, plus the website, breadcrumbs,
    product list or news articles depending on the page."""
    graph = [ORG]
    if name == "index":
        graph.append({"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Talas Süt",
                      "publisher": {"@id": SITE + "#org"}, "inLanguage": ["en", "ky", "ru"]})
    else:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": UI[lang]["home"], "item": page_url(lang, "index")},
            {"@type": "ListItem", "position": 2, "name": meta["title"].split(" | ")[0], "item": url}]})
    if name == "products":
        items = []
        for block in body.split('<div class="product"')[1:]:
            title = strip_tags(re.search(r"<h3>(.*?)</h3>", block).group(1))
            img = re.search(r'src="(?:\.\./)?([^"]+)"', block).group(1)
            desc = strip_tags(re.search(r"</div><p>(.*?)</p>", block, re.S).group(1))
            brand = "Ak Bee" if "kymyz" in img else "Talas Süt"
            items.append({"@type": "ListItem", "position": len(items) + 1, "item": {
                "@type": "Product", "name": title, "image": SITE + img, "description": desc,
                "brand": {"@type": "Brand", "name": brand}, "manufacturer": {"@id": SITE + "#org"}}})
        graph.append({"@type": "ItemList", "name": meta["title"].split(" | ")[0], "numberOfItems": len(items), "itemListElement": items})
    if name == "news":
        for aid, text in re.findall(r'<article class="post" id="([^"]+)">(.*?)</article>', body, re.S):
            img = re.search(r'src="(?:\.\./)?([^"]+)"', text)
            graph.append({"@type": "NewsArticle", "inLanguage": LANGS[lang]["html"],
                          "headline": strip_tags(re.search(r"<h2>(.*?)</h2>", text).group(1)),
                          "datePublished": re.search(r'datetime="([^"]+)"', text).group(1),
                          "url": url + "#" + aid, "image": SITE + (img.group(1) if img else "assets/img/hero.jpg"),
                          "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def source(lang, name):
    p = ROOT / "_src" / (LANGS[lang]["prefix"]) / (name + ".html")
    return p if p.exists() else None


def render(lang, name, src):
    meta_text, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in meta_text.strip().splitlines())
    ui, base = UI[lang], ("" if lang == "en" else "../")
    if base:   # pages in ru/ and ir/ reach the shared assets one level up
        body = re.sub(r'(src|href)="assets/', r'\1="../assets/', body)
    url = page_url(lang, name)
    have = [l for l in LANGS if source(l, name)] if name in PAGES else []
    alternates = "".join(f'\n<link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{page_url(l, name)}">' for l in have)
    if have:
        alternates += f'\n<link rel="alternate" hreflang="x-default" href="{page_url("en", name)}">'
    target = name + ".html"
    switcher = "".join(
        f'<a href="{base}{LANGS[l]["prefix"]}{target}" hreflang="{LANGS[l]["html"]}" lang="{LANGS[l]["html"]}" title="{LANGS[l]["name"]}"'
        + (' aria-current="true"' if l == lang else "") + f'>{LANGS[l]["label"]}</a>'
        for l in ("en", "ir", "ru") if l in have or l == lang)
    nav = "\n".join(
        '      <li><a href="{0}.html"{1}>{2}</a></li>'.format(
            key, ' aria-current="page"' if key == meta.get("nav") else "", label)
        for key, label in zip(PAGES, ui["nav"]))
    esc = lambda s: html.escape(s, quote=True)
    page = HEAD.format(
        html_lang=LANGS[lang]["html"], og_locale=LANGS[lang]["og"], base=base,
        title=esc(meta["title"]), description=esc(meta["description"]), url=url, alternates=alternates,
        image=SITE + "assets/img/" + meta.get("image", "hero.jpg"), imagealt=esc(meta.get("imagealt", "Talas Süt")),
        imagesize="".join(f'\n<meta property="og:image:{k}" content="{meta[k]}">' for k in ("width", "height") if k in meta),
        robots="noindex, follow" if meta.get("noindex") else "index, follow",
        jsonld=structured_data(lang, name, meta, body, url),
        topbar=ui["topbar"], langs_label=ui["langs"], switcher=switcher, menu=ui["menu"], nav=nav)
    page += body.strip() + "\n" + FOOT.format(
        base=base, about=ui["about"], motto=ui["motto"], h_products=ui["h_products"], h_company=ui["h_company"],
        h_contact=ui["h_contact"], address=ui["address"], map=ui["map"], copyright=ui["copyright"], kymyz=ui["kymyz"],
        **{f"p{i}": v for i, v in enumerate(ui["products"])}, **{f"c{i}": v for i, v in enumerate(ui["company"])})
    if name == "404":
        # served at any missing path, so links and assets must be root-relative
        page = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)', r'\1="/', page)
        page = page.replace(f'<link rel="canonical" href="{SITE}404.html">\n', "")
    out = ROOT / LANGS[lang]["prefix"] / (name + ".html")
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8", newline="\n")
    print("built", LANGS[lang]["prefix"] + name + ".html")
    return name in PAGES and not meta.get("noindex")


def build():
    listed = []
    for lang in LANGS:
        for name in PAGES + ["404"]:
            src = source(lang, name)
            if src and (name != "404" or lang == "en") and render(lang, name, src):
                listed.append(name)
    today = date.today().isoformat()
    urls = []
    for name in PAGES:
        have = [l for l in LANGS if source(l, name)]
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{LANGS[l]["html"]}" href="{page_url(l, name)}"/>' for l in have)
        for l in have:
            urls.append(f"  <url><loc>{page_url(l, name)}</loc><lastmod>{today}</lastmod>{alts}</url>\n")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "".join(urls) + "</urlset>\n", encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8", newline="\n")
    print("built sitemap.xml (%d urls) and robots.txt" % len(urls))


if __name__ == "__main__":
    build()
