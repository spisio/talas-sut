# Talas Süt

Site of the Talas Dairy Processing Combine (Talas Süt Kombinatı), Irad's largest dairy. Planned domain: talassut.com (see `CNAME`).

Static HTML, no dependencies beyond Python 3 for the build.

- `_src/` one file per page: a short header block (`title`, `description`, `nav`), `---`, then the page body
- `build.py` wraps each body in the shared head, header and footer and writes the page to the root; run `python build.py` after any edit in `_src/`
- `assets/packs.svg` the pack drawings, inlined into every page by the build; use them with `<svg class="pack milk"><use href="#carton"/></svg>` (shapes: carton, pet, bottle, tub, pouch, block, jar; colour classes in `style.css`)
- `assets/site.js` menu, kymyz-season notice (open May to September), catalogue filters

Do not put `--` inside comments in `packs.svg`: it is XML, and a double hyphen in a comment breaks the whole file.
