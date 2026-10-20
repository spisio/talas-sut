#!/usr/bin/env python3
"""Build the Talas Süt site.

Each page body lives in _src/<name>.html. The first lines are a header block:

    title: Page title
    description: One-sentence description
    nav: products
    ---

The script wraps every body in the shared head, header and footer and writes
<name>.html at the site root. Run it after editing anything in _src/.
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://talas-sut.com/"

NAV = [
    ("index", "Home"),
    ("products", "Products"),
    ("kymyz", "Kymyz"),
    ("about", "About us"),
    ("farmers", "For farmers"),
    ("news", "News"),
    ("contact", "Contact"),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#1f4e8c">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Talas Süt">
<meta property="og:locale" content="en_GB">
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
<link rel="icon" href="assets/mark.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>window.goatcounter=new Object();goatcounter.path=p=>location.host+p;</script>
<script data-goatcounter="https://irad.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
<div class="topbar">
  <div class="wrap">
    <span>Consumer line <a href="tel:+996392348000">2-34-80-00</a> &middot; Mon&ndash;Sat 8:00&ndash;20:00</span>
    <span class="lang"><strong>EN</strong><span title="Iradi version coming soon">IR</span><span title="Russian version coming soon">RU</span></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="assets/logo.svg" alt="Talas Süt" width="170" height="54">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
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
        <div class="foot-brand"><img src="assets/logo-reverse.svg" alt="Talas Süt" width="200" height="64"></div>
        <p>Talas Dairy Processing Combine (<i>Talas Süt Kombinatı</i>), owned by the Talas Valley Milk Cooperative. Milk from the farms of the Talas valley, bottled in Talas since 1964.</p>
        <p><i>Ak süt, ak niet.</i> White milk, a clean heart.</p>
      </div>
      <div>
        <h4>Products</h4>
        <ul>
          <li><a href="products.html#milk">Milk and cream</a></li>
          <li><a href="products.html#fermented">Kefir, airan and qatiq</a></li>
          <li><a href="products.html#suzma">Suzma</a></li>
          <li><a href="kymyz.html">Ak Bee kymyz</a></li>
          <li><a href="products.html#kurut">Kurut</a></li>
          <li><a href="products.html#butter">Butter and kaymak</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About us</a></li>
          <li><a href="about.html#history">Our history</a></li>
          <li><a href="farmers.html">Selling us your milk</a></li>
          <li><a href="news.html">News</a></li>
          <li><a href="contact.html#jobs">Jobs</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li>41 Temir Jol Street, Western Industrial District, Talas</li>
          <li><a href="tel:+996392348000">2-34-80-00</a></li>
          <li><a href="mailto:info@talas-sut.com">info@talas-sut.com</a></li>
          <li><a href="https://maps.attelkom.net/">Find us on Kartalar</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 1964&ndash;2026 Talas Dairy Processing Combine. All rights reserved.</span>
      <span>Kymyz contains up to 2.4% alcohol. Not for children or drivers.</span>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


ORG = {
    "@type": "Organization",
    "@id": SITE + "#org",
    "name": "Talas Dairy Processing Combine",
    "alternateName": ["Talas Süt", "Talas Süt Kombinatı"],
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


def strip_tags(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def structured_data(name, meta, body, url):
    """JSON-LD graph: the organisation everywhere, plus the website, breadcrumbs,
    product list or news articles depending on the page."""
    graph = [ORG]
    if name == "index":
        graph.append({"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Talas Süt",
                      "publisher": {"@id": SITE + "#org"}, "inLanguage": "en"})
    else:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": meta["title"].split(" | ")[0], "item": url}]})
    if name == "products":
        items = []
        for block in body.split('<div class="product"')[1:]:
            title = strip_tags(re.search(r"<h3>(.*?)</h3>", block).group(1))
            img = re.search(r'src="([^"]+)"', block).group(1)
            desc = strip_tags(re.search(r"</div><p>(.*?)</p>", block, re.S).group(1))
            brand = "Ak Bee" if "kymyz" in img else "Talas Süt"
            items.append({"@type": "ListItem", "position": len(items) + 1, "item": {
                "@type": "Product", "name": title, "image": SITE + img, "description": desc,
                "brand": {"@type": "Brand", "name": brand}, "manufacturer": {"@id": SITE + "#org"}}})
        graph.append({"@type": "ItemList", "name": "Talas Süt products", "numberOfItems": len(items), "itemListElement": items})
    if name == "news":
        for art in re.findall(r'<article class="post" id="([^"]+)">(.*?)</article>', body, re.S):
            aid, text = art
            img = re.search(r'src="([^"]+)"', text)
            graph.append({"@type": "NewsArticle", "headline": strip_tags(re.search(r"<h2>(.*?)</h2>", text).group(1)),
                          "datePublished": re.search(r'datetime="([^"]+)"', text).group(1),
                          "url": url + "#" + aid, "image": SITE + img.group(1) if img else SITE + "assets/img/hero.jpg",
                          "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"}})
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def build():
    pages = []
    for src in sorted((ROOT / "_src").glob("*.html")):
        meta_text, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
        meta = dict(line.split(": ", 1) for line in meta_text.strip().splitlines())
        name = src.stem
        nav = "\n".join(
            '      <li><a href="{0}.html"{1}>{2}</a></li>'.format(
                key, ' aria-current="page"' if key == meta.get("nav") else "", label)
            for key, label in NAV)
        url = SITE if name == "index" else SITE + name + ".html"
        esc = lambda s: html.escape(s, quote=True)
        page = HEAD.format(title=esc(meta["title"]), description=esc(meta["description"]), url=url, nav=nav,
                           image=SITE + "assets/img/" + meta.get("image", "hero.jpg"), imagealt=esc(meta.get("imagealt", "Talas Süt")),
                           imagesize="".join(f'\n<meta property="og:image:{k}" content="{meta[k]}">' for k in ("width", "height") if k in meta),
                           robots="noindex, follow" if meta.get("noindex") else "index, follow",
                           jsonld=structured_data(name, meta, body, url))
        page += body.strip() + "\n" + FOOT
        if name == "404":
            # served at any missing path, so links and assets must be root-relative
            page = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|#|/)', r'\1="/', page)
            page = page.replace('<link rel="canonical" href="https://talas-sut.com/404.html">\n', "")
        else:
            pages.append(url)
        (ROOT / (name + ".html")).write_text(page, encoding="utf-8", newline="\n")
        print("built", name + ".html")

    today = date.today().isoformat()
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in pages)
        + "</urlset>\n", encoding="utf-8", newline="\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n", encoding="utf-8", newline="\n")
    print("built sitemap.xml and robots.txt")


if __name__ == "__main__":
    build()
