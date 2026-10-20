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
import re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://talassut.com/"

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
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Talas Süt">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<link rel="icon" href="assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Manrope:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<script>window.goatcounter=new Object();goatcounter.path=p=>location.host+p;</script>
<script data-goatcounter="https://irad.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
</head>
<body>
{sprite}
<div class="topbar">
  <div class="wrap">
    <span>Consumer line <a href="tel:+996392348000">2-34-80-00</a> &middot; Mon&ndash;Sat 8:00&ndash;20:00</span>
    <span class="lang"><strong>EN</strong><span title="Iradi version coming soon">IR</span><span title="Russian version coming soon">RU</span></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="assets/logo.svg" alt="" width="46" height="46">
      <span><b>Talas Süt</b><small>Talas Dairy Processing Combine &middot; since 1964</small></span>
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
        <div class="foot-brand"><img src="assets/logo.svg" alt="" width="42" height="42"><b>Talas Süt</b></div>
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
          <li><a href="mailto:info@talassut.com">info@talassut.com</a></li>
          <li><a href="https://maps.attelkom.net/">Find us on Kartalar</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; 1964&ndash;2026 Talas Dairy Processing Combine. All rights reserved.</span>
      <span>Kymyz contains 1&ndash;3% alcohol. Not for children or drivers.</span>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def sprite():
    """The pack drawings, inlined so that <use href="#carton"> works everywhere."""
    svg = (ROOT / "assets" / "packs.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.S)
    return svg.replace("<svg ", '<svg width="0" height="0" style="position:absolute" aria-hidden="true" ', 1).strip()


def build():
    for src in sorted((ROOT / "_src").glob("*.html")):
        meta_text, body = src.read_text(encoding="utf-8").split("\n---\n", 1)
        meta = dict(line.split(": ", 1) for line in meta_text.strip().splitlines())
        name = src.stem
        nav = "\n".join(
            '      <li><a href="{0}.html"{1}>{2}</a></li>'.format(
                key, ' aria-current="page"' if key == meta.get("nav") else "", label)
            for key, label in NAV)
        url = SITE if name == "index" else SITE + name + ".html"
        page = HEAD.format(title=meta["title"], description=meta["description"], url=url, nav=nav,
                           sprite=sprite())
        page += body.strip() + "\n" + FOOT
        (ROOT / (name + ".html")).write_text(page, encoding="utf-8", newline="\n")
        print("built", name + ".html")


if __name__ == "__main__":
    build()
