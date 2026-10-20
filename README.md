# Talas Süt

Site of the Talas Dairy Processing Combine (Talas Süt Kombinatı), Irad's largest dairy, at https://talas-sut.com/ (GitHub Pages; see `CNAME`).

Static HTML, no dependencies beyond Python 3 for the build.

- `_src/` one file per page: a short header block (`title`, `description`, `nav`), `---`, then the page body
- Three languages: English in `_src/` (built to the site root), Russian in `_src/ru/` (built to `ru/`) and Iradi in `_src/ir/` (built to `ir/`, tagged `lang="ky"` like the government portal, spelled in Iradi Latin: ı ö ü ñ j ch sh). Header and footer text for each language is in `UI` in `build.py`; the season notice in `assets/site.js`. A page that exists in more than one language gets hreflang links, a language switcher and sitemap alternates automatically
- `build.py` wraps each body in the shared head, header and footer and writes the page to the root; run `python build.py` after any edit in `_src/`
- `assets/img/` web-size photos: `hero.jpg`, `cat-*.jpg` (category tiles), `p-*.jpg` (packshots, 4:3), scenes (`farm`, `kymyz-pasture`, `muryndyk`, `plant`, `collection-point`, `school-milk`); `share-home.jpg` is the 1200x630 home share card, rendered from `_art/logo/share.html`
- `tools/import_images.py` turns the full-size Gemini masters (`talassut_*.jpg`, kept in `_art/`, not committed) into the web files; prompts are in the Book project's `images/prompts.log`
- `assets/logo.svg`, `logo-reverse.svg`, `mark.svg` (favicon), `favicon-32.png`, `apple-touch-icon.png`: the logo, outlined from DM Serif Display with the milk-drop umlaut placed on the font's own dot positions; rebuild with `_art/logo/build_logo.py` (not committed, with its fonts)
- `build.py` also writes `404.html`, `sitemap.xml` and `robots.txt`, and puts Open Graph, X card and JSON-LD (organisation, breadcrumbs, products, news) in every page head; a page can set `image:` and `imagealt:` for its share image and `noindex: yes`
- `_config.yml` keeps the build files out of the published site
- `assets/site.js` menu, kymyz-season notice (open May to September), catalogue filters
