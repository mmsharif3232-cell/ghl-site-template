#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the full 22-page Brody Pennell site clone.

- Shared chrome (head + header + footer + GHL runtime) is taken from the already-filled
  homepage (demo.html) so every page is byte-identical in its frame.
- 6 interior pages are pixel-cloned from the saved "Save Complete" exports in ~/Downloads:
  About, Contact, Reviews, Cities Served, Air Conditioning (category), AC Repair (detail).
- 15 more service pages are generated from the AC category/detail templates with the
  service name substituted (same exact layout, correct names) to reach 22 pages.
- All internal links are rewritten to flat local slugs so the nav works as one real site.
- Forms -> static demo form, scheduler buttons -> GHL calendar modal (in shared chrome).

Output: index.html (home) + 21 sibling pages, all deploy-ready.
"""
import re, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DOWN = os.path.expanduser("~/Downloads")
ASSETS = os.path.join(HERE, "assets")
D = re.DOTALL
IMG_EXT = (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico")

# ---- static demo contact form (same as the homepage demo) -------------------
DEMO_FORM = ('<div class="ghl-embed ghl-embed--form">'
 '<form onsubmit="return false" style="display:grid;gap:12px">'
 '<input class="uk-input" type="text" placeholder="Full Name*" style="background:#fff">'
 '<input class="uk-input" type="email" placeholder="Email Address*" style="background:#fff">'
 '<input class="uk-input" type="tel" placeholder="Phone Number*" style="background:#fff">'
 '<textarea class="uk-textarea" rows="4" placeholder="How Can We Help?*" style="background:#fff"></textarea>'
 '<button class="uk-button uk-button-primary uk-button-large" type="submit">Send Message</button>'
 '<p style="font-size:11px;opacity:.7;margin:0">Demo form — live client sites use a GoHighLevel form embed.</p>'
 '</form></div>')

# ---- internal-link map: brodypennell path (no slashes) -> local slug ---------
LINKMAP = {
 "": "index.html",
 "services/air-conditioning": "air-conditioning.html",
 "services/heating": "heating.html",
 "services/indoor-air-quality": "indoor-air-quality.html",
 "services/air-conditioning/ac-repair": "ac-repair.html",
 "services/air-conditioning/ac-maintenance": "ac-maintenance.html",
 "services/air-conditioning/ac-installation-and-replacement": "ac-replacement.html",
 "services/ductless-mini-splits": "ductless-mini-splits.html",
 "services/ductless-services": "ductless-mini-splits.html",
 "services/air-conditioning/thermostat-repair": "thermostat-repair.html",
 "services/heating/heater-repair": "heater-repair.html",
 "services/heating/heater-installation": "heater-installation.html",
 "services/heating/heater-maintenance": "heater-maintenance.html",
 "services/heat-pumps": "heat-pumps.html",
 "services/heat-pumps/heat-pump-repair": "heat-pump-repair.html",
 "services/furnaces": "furnaces.html",
 "services/furnaces/furnace-repair": "furnace-repair.html",
 "services/furnaces/furnace-installation": "furnace-installation.html",
 "services/ductwork/duct-cleaning": "duct-cleaning.html",
 "about-us": "about.html",
 "about-us/testimonials": "reviews.html",
 "cities-served": "cities.html",
 "contact-us": "contact.html",
 "contact": "contact.html",
}
def slug_for(path):
    path = path.strip("/").split("#")[0].split("?")[0]
    if path in LINKMAP:
        return LINKMAP[path]
    # sensible fallbacks so nothing 404s
    if path.startswith("cities-served"): return "cities.html"
    if path.startswith("about-us"):      return "about.html"
    if path.startswith("services/air-conditioning"): return "air-conditioning.html"
    if path.startswith("services/heating"):          return "heating.html"
    if path.startswith("services/heat-pumps"):       return "heat-pumps.html"
    if path.startswith("services/furnaces"):         return "furnaces.html"
    if path.startswith("services/ductless"):         return "ductless-mini-splits.html"
    if path.startswith(("services/indoor-air","services/ductwork","services/connected")): return "indoor-air-quality.html"
    if path.startswith("services"): return "air-conditioning.html"
    return "index.html"

def rewrite_links(html):
    html = re.sub(r'href=(["\'])https?://brodypennell\.com([^"\']*)\1',
                  lambda m: f'href={m.group(1)}{slug_for(m.group(2))}{m.group(1)}', html)
    # root-relative internal links (not protocol-relative //)
    html = re.sub(r'href="(/(?!/)[^"]*)"',
                  lambda m: f'href="{slug_for(m.group(1))}"', html)
    return html

# ---- asset handling ----------------------------------------------------------
def vendor_assets(stem):
    """Copy a saved page's _files images into assets/ (skip if present)."""
    src = os.path.join(DOWN, stem + "_files")
    if not os.path.isdir(src):
        print("  !! no _files for", stem); return
    n = 0
    for f in os.listdir(src):
        if f.lower().endswith(IMG_EXT):
            dst = os.path.join(ASSETS, f)
            if not os.path.exists(dst):
                try: shutil.copy(os.path.join(src, f), dst); n += 1
                except Exception: pass
    print(f"  assets +{n} from {stem}_files")

# ---- clean a saved page's <main> --------------------------------------------
def extract_main(stem):
    html = open(os.path.join(DOWN, stem + ".html"), encoding="utf-8", errors="replace").read()
    a = html.index('<main id="tm-main"'); b = html.index("</main>") + len("</main>")
    return html[a:b]

def clean_main(stem):
    main = extract_main(stem)
    main = re.sub(r"<script\b[^>]*>.*?</script>", "", main, flags=D)
    main = re.sub(r"<noscript\b[^>]*>.*?</noscript>", "", main, flags=D)
    # Gravity form -> static demo form (matches homepage demo)
    main = re.sub(r'<div class="gf_browser[^"]*gform_wrapper.*?</form>\s*</div>', DEMO_FORM, main, flags=D)
    main = re.sub(r'<div[^>]*gform_wrapper.*?</form>\s*</div>', DEMO_FORM, main, flags=D)
    # scheduler triggers -> GHL calendar modal opener
    main = main.replace('onclick="SimpleScheduler.open()"', 'onclick="openGhlCalendar();return false;"')
    # assets: local saved copies -> assets/ ; root-relative wp-content -> brand host
    vendor_assets(stem)
    main = main.replace("./" + stem + "_files/", "assets/").replace(stem + "_files/", "assets/")
    main = re.sub(r'(["\'(\s])/wp-content/', r'\1https://brodypennell.com/wp-content/', main)
    main = re.sub(r'\\/wp-content\\/', r'https:\\/\\/brodypennell.com\\/wp-content\\/', main)
    # inline bg for lazy uk-img divs (so backgrounds show without JS)
    def add_bg(m):
        tag = m.group(0)
        if "background-image" in tag: return tag
        ds = re.search(r'data-src="([^"]+)"', tag)
        if not ds: return tag
        url = ds.group(1)
        if 'style="' in tag:
            return tag.replace('style="', f'style="background-image:url(&quot;{url}&quot;);', 1)
        return tag[:-1] + f' style="background-image:url(&quot;{url}&quot;)">'
    main = re.sub(r'<div\b[^>]*\buk-img=""[^>]*>', add_bg, main)
    return main

# ---- shared chrome from the filled homepage (demo.html) ----------------------
home = open(os.path.join(HERE, "demo.html"), encoding="utf-8").read()
PRE  = home[:home.index('<main id="tm-main"')]
POST = home[home.index("</main>") + len("</main>"):]
HOME_MAIN = home[home.index('<main id="tm-main"'):home.index("</main>") + len("</main>")]

def set_title(pre, title):
    pre = re.sub(r"<title>.*?</title>", "<title>" + title + "</title>", pre, flags=D)
    pre = re.sub(r'(<meta property="og:title" content=").*?(">)', r"\g<1>" + title + r"\g<2>", pre)
    pre = re.sub(r'(<meta name="twitter:title" content=").*?(">)', r"\g<1>" + title + r"\g<2>", pre)
    return pre

def assemble(title, main):
    return rewrite_links(set_title(PRE, title) + main + POST)

# ---- service-page derivations (same layout, swapped names) -------------------
def detail_pairs(label, label_lc, unit, unit_lc, heating):
    """Substitutions applied to the AC Repair main to retarget a detail page."""
    p = [("Award-Winning AC Repair Los Angeles", "Award-Winning " + label + " Los Angeles"),
         ("Reliable AC Repair in Los Angeles, CA", "Reliable " + label + " in Los Angeles, CA"),
         ("AC Repair", label), ("AC repair", label_lc), ("ac repair", label_lc),
         ("Air Conditioning Repair", label), ("air conditioning repair", label_lc)]
    if heating:
        p += [("air conditioner", unit_lc), ("Air Conditioner", unit),
              ("air conditioning", "heating"), ("Air Conditioning", "Heating"),
              ("AC unit", unit_lc), ("A/C", unit), (" AC ", " " + unit_lc + " "),
              ("cooling", "heating")]
    else:  # still a cooling service (maintenance/replacement/etc.)
        p += [("air conditioner", unit_lc), ("Air Conditioner", unit)]
    return p

# detail: (slug, title, h1-label, pairs)
DETAILS = [
 ("ac-maintenance", "AC Maintenance in Los Angeles, CA | Brody Pennell",
   detail_pairs("AC Maintenance", "AC maintenance", "air conditioner", "air conditioner", False)),
 ("ac-replacement", "AC Installation & Replacement in Los Angeles, CA | Brody Pennell",
   detail_pairs("AC Replacement", "AC replacement", "air conditioner", "air conditioner", False)),
 ("ductless-mini-splits", "Ductless Mini-Splits in Los Angeles, CA | Brody Pennell",
   detail_pairs("Ductless Mini-Splits", "ductless mini-splits", "mini-split", "mini-split", False)),
 ("thermostat-repair", "Thermostat Repair in Los Angeles, CA | Brody Pennell",
   detail_pairs("Thermostat Repair", "thermostat repair", "thermostat", "thermostat", False)),
 ("heater-repair", "Heater Repair in Los Angeles, CA | Brody Pennell",
   detail_pairs("Heater Repair", "heater repair", "Heater", "heater", True)),
 ("heater-installation", "Heater Installation in Los Angeles, CA | Brody Pennell",
   detail_pairs("Heater Installation", "heater installation", "Heater", "heater", True)),
 ("heater-maintenance", "Heater Maintenance in Los Angeles, CA | Brody Pennell",
   detail_pairs("Heater Maintenance", "heater maintenance", "Heater", "heater", True)),
 ("heat-pumps", "Heat Pumps in Los Angeles, CA | Brody Pennell",
   detail_pairs("Heat Pump Services", "heat pump services", "Heat Pump", "heat pump", True)),
 ("heat-pump-repair", "Heat Pump Repair in Los Angeles, CA | Brody Pennell",
   detail_pairs("Heat Pump Repair", "heat pump repair", "Heat Pump", "heat pump", True)),
 ("furnaces", "Furnace Services in Los Angeles, CA | Brody Pennell",
   detail_pairs("Furnace Services", "furnace services", "Furnace", "furnace", True)),
 ("furnace-repair", "Furnace Repair in Los Angeles, CA | Brody Pennell",
   detail_pairs("Furnace Repair", "furnace repair", "Furnace", "furnace", True)),
 ("furnace-installation", "Furnace Installation in Los Angeles, CA | Brody Pennell",
   detail_pairs("Furnace Installation", "furnace installation", "Furnace", "furnace", True)),
 ("duct-cleaning", "Duct Cleaning in Los Angeles, CA | Brody Pennell",
   detail_pairs("Duct Cleaning", "duct cleaning", "duct system", "duct system", True)),
]
# category derivations from the Air Conditioning category page
def cat_pairs(label, label_lc, heating):
    p = [("Professional AC Services In Los Angeles", "Professional " + label + " Services In Los Angeles"),
         ("Expert Air Conditioning Service in Los Angeles, CA", "Expert " + label + " Service in Los Angeles, CA")]
    if heating:
        p += [("Air Conditioning", label), ("air conditioning", label_lc),
              ("air conditioner", "system"), ("AC unit", "system"), (" AC ", " " + label_lc + " "),
              ("cooling", "heating")]
    else:
        p += [("Air Conditioning", label), ("air conditioning", label_lc)]
    return p
CATEGORIES = [
 ("heating", "Expert Heating Service in Los Angeles, CA | Brody Pennell",
   cat_pairs("Heating", "heating", True)),
 ("indoor-air-quality", "Indoor Air Quality Services in Los Angeles, CA | Brody Pennell",
   cat_pairs("Indoor Air Quality", "indoor air quality", False)),
]

def apply_pairs(main, pairs):
    for a, b in pairs:
        main = main.replace(a, b)
    return main

# =============================================================================
print("[home] index.html")
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(rewrite_links(home))

# saved interior pages: (stem, slug, title)
SAVED = [
 ("About Our HVAC Technicians at Brody Pennell _ Brody Pennell", "about.html",
   "About Our HVAC Technicians at Brody Pennell | Brody Pennell"),
 ("Contact - Brody Pennell", "contact.html", "Contact - Brody Pennell"),
 ("Reviews - Brody Pennell", "reviews.html", "Reviews - Brody Pennell"),
 ("Cities Served - Brody Pennell", "cities.html", "Cities Served - Brody Pennell"),
 ("Expert Air Conditioning Service in Los Angeles, CA", "air-conditioning.html",
   "Expert Air Conditioning Service in Los Angeles, CA | Brody Pennell"),
 ("Reliable AC Repair in Los Angeles, CA _ Brody Pennell", "ac-repair.html",
   "Reliable AC Repair in Los Angeles, CA | Brody Pennell"),
]
CLEAN = {}
for stem, slug, title in SAVED:
    print("[clone]", slug)
    m = clean_main(stem)
    CLEAN[slug] = m
    open(os.path.join(HERE, slug), "w", encoding="utf-8").write(assemble(title, m))

# derived category pages (from air-conditioning.html main)
for slug, title, pairs in CATEGORIES:
    print("[derive cat]", slug)
    m = apply_pairs(CLEAN["air-conditioning.html"], pairs)
    open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8").write(assemble(title, m))

# derived detail pages (from ac-repair.html main)
for slug, title, pairs in DETAILS:
    print("[derive]", slug)
    m = apply_pairs(CLEAN["ac-repair.html"], pairs)
    open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8").write(assemble(title, m))

pages = sorted(f for f in os.listdir(HERE) if f.endswith(".html") and f not in ("template.html", "demo.html"))
print(f"\nWROTE {len(pages)} pages:")
print("  " + "  ".join(pages))
