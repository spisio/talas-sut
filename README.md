# Talas Süt

Site of the Talas Dairy Processing Combine (Talas Süt Kombinatı), Irad's largest dairy, at https://talas-sut.com/ (GitHub Pages; see `CNAME`).

Static HTML, no dependencies beyond Python 3 for the build.

- `_src/` one file per page: a short header block (`title`, `description`, `nav`), `---`, then the page body
- `build.py` wraps each body in the shared head, header and footer and writes the page to the root; run `python build.py` after any edit in `_src/`
- `assets/img/` web-size photos: `hero.jpg`, `cat-*.jpg` (category tiles), `p-*.jpg` (packshots, 4:3), scenes (`farm`, `kymyz-pasture`, `muryndyk`, `plant`, `collection-point`, `school-milk`)
- `tools/import_images.py` turns the full-size Gemini masters (`talassut_*.jpg`, kept in `_art/`, not committed) into the web files; prompts are in the Book project's `images/prompts.log`
- `assets/logo.svg`, `logo-reverse.svg`, `mark.svg` (favicon), `favicon-32.png`, `apple-touch-icon.png`: the logo, outlined from DM Serif Display with the milk-drop umlaut placed on the font's own dot positions; rebuild with `_art/logo/build_logo.py` (not committed, with its fonts)
- `assets/site.js` menu, kymyz-season notice (open May to September), catalogue filters
