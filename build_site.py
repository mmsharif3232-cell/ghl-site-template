#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the 22-page site as a TRUE TEMPLATE:
  * shared chrome comes from template.html (tokenized: {{BUSINESS_NAME}}, {{PHONE}}, ...)
  * every company-specific value -> {{TOKEN}} (GHL custom value / placeholder)
  * "screams-specific" copy genericized: no "Since 19xx", no "Award-Winning",
    no specific Google/Facebook/Yelp rating numbers, no Carrier brand lock-in
  * city -> {{CITY}}, founding/tenure -> {{YEAR_FOUNDED}}/{{YEARS_IN_BUSINESS}}
  * full SEO: per-page title/description/canonical/OG/Twitter + JSON-LD, sitemap.xml, robots.txt
  * one-line TEMPLATE marker on every page
Output: index.html + 21 sibling template pages, sitemap.xml, robots.txt.
"""
import re, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DOWN = os.path.expanduser("~/Downloads")
ASSETS = os.path.join(HERE, "assets")
D = re.DOTALL
IMG_EXT = (".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico")
MARKER = ("<!-- TEMPLATE — every {{TOKEN}} is a GHL custom value / placeholder; fill before "
          "launch. Copy is generic and not company-specific. -->\n")

# static demo contact form (template uses GHL; this keeps the form area presentable)
DEMO_FORM = ('<div class="ghl-embed ghl-embed--form">'
 '<form onsubmit="return false" style="display:grid;gap:12px">'
 '<input class="uk-input" type="text" placeholder="Full Name*" style="background:#fff">'
 '<input class="uk-input" type="email" placeholder="Email Address*" style="background:#fff">'
 '<input class="uk-input" type="tel" placeholder="Phone Number*" style="background:#fff">'
 '<textarea class="uk-textarea" rows="4" placeholder="How Can We Help?*" style="background:#fff"></textarea>'
 '<button class="uk-button uk-button-primary uk-button-large" type="submit">Send Message</button>'
 '</form></div>')

# ---------------------------------------------------------------- link mapping
LINKMAP = {
 "": "index.html",
 "services/air-conditioning": "air-conditioning.html", "services/heating": "heating.html",
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
 "about-us": "about.html", "about-us/testimonials": "reviews.html",
 "cities-served": "cities.html", "contact-us": "contact.html", "contact": "contact.html",
}
def slug_for(path):
    path = path.strip("/").split("#")[0].split("?")[0]
    if path in LINKMAP: return LINKMAP[path]
    if path.startswith("cities-served"): return "cities.html"
    if path.startswith("about-us"): return "about.html"
    if path.startswith("services/air-conditioning"): return "air-conditioning.html"
    if path.startswith("services/heating"): return "heating.html"
    if path.startswith("services/heat-pumps"): return "heat-pumps.html"
    if path.startswith("services/furnaces"): return "furnaces.html"
    if path.startswith("services/ductless"): return "ductless-mini-splits.html"
    if path.startswith(("services/indoor-air","services/ductwork","services/connected")): return "indoor-air-quality.html"
    if path.startswith("services"): return "air-conditioning.html"
    return "index.html"

def rewrite_links(html):
    html = re.sub(r'href="\{\{SITE_URL\}\}([^"]*)"', lambda m: f'href="{slug_for(m.group(1))}"', html)
    html = re.sub(r'href=(["\'])https?://brodypennell\.com([^"\']*)\1',
                  lambda m: f'href={m.group(1)}{slug_for(m.group(2))}{m.group(1)}', html)
    html = re.sub(r'href="(/(?!/)[^"]*)"', lambda m: f'href="{slug_for(m.group(1))}"', html)
    return html

# ---------------------------------------------- genericize + tokenize a page
GENERIC = [
 # specific brand lock-in
 ("the only Carrier Dealer in the West Los Angeles area and the only Carrier Presidents Award Recipient for 2021 in all of LA and Orange Counties",
  "a trusted installer of leading heating and cooling brands"),
 ("Carrier Presidents Award", "manufacturer's top dealer award"),
 ("Carrier heating and cooling systems", "leading heating and cooling systems"),
 ("Carrier", "leading-brand"),
 # specific ratings / review counts
 ("3,000+", "hundreds of"), ("3000+", "hundreds of"),
 ("4.9 rating on Facebook", "top ratings on Facebook"),
 ("4.9 rating", "top ratings"), ("4.8 rating", "top ratings"), ("4.9", "5"), ("4.8", "5"),
]
GENERIC_RE = [
 # "screams-specific" claims -> generic / removed
 (r'[Aa]ward[- ][Ww]inning', 'Professional'),
 (r'President[’\']s Award', 'top industry award'), (r'Presidents Award', 'top industry award'),
 (r'\b\d{1,2} (?:consecutive years|years in a row)', 'multiple years'),
 # founding year / tenure -> tokens
 (r'\bSince 1945\b', 'Since {{YEAR_FOUNDED}}'), (r'\bsince 1945\b', 'since {{YEAR_FOUNDED}}'),
 (r'\bin 1945\b', 'in {{YEAR_FOUNDED}}'), (r'\b1945\b', '{{YEAR_FOUNDED}}'),
 (r'\bover (?:80|75)(?:&nbsp;|&#160;|\s)+years', '{{YEARS_IN_BUSINESS}} years'),
 (r'\b(?:80|75)(?:&nbsp;|&#160;|\s)+[Yy]ears\b', '{{YEARS_IN_BUSINESS}} years'),
]
TOKENIZE = [
 # NAP / license  (address BEFORE city)
 ("8599 Venice Blvd., Los Angeles, CA 90034", "{{ADDRESS}}"),
 ("8599 Venice Blvd.", "{{ADDRESS}}"),
 ("CA LIC# 256821", "{{LICENSE}}"),
 # business name (long then short)
 ("Brody Pennell Heating &amp; Air Conditioning", "{{BUSINESS_NAME}}"),
 ("Brody Pennell Heating & Air Conditioning", "{{BUSINESS_NAME}}"),
 ("Brody Pennell", "{{BUSINESS_SHORT_NAME}}"),
 ("Brody Comfort Club", "{{BUSINESS_SHORT_NAME}} Comfort Club"),
 ("mailto:customercare@brodypennell.com", "mailto:{{EMAIL}}"),
 ("customercare@brodypennell.com", "{{EMAIL}}"),
 # phones
 ("tel:4243263045", "tel:{{PHONE}}"), ("tel:424-455-0173", "tel:{{PHONE}}"),
 ("(424) 326-3045", "{{PHONE_DISPLAY}}"), ("424-326-3045", "{{PHONE_DISPLAY}}"),
 ("424-455-0173", "{{PHONE_DISPLAY}}"), ("4243263045", "{{PHONE}}"),
 # social
 ("https://www.facebook.com/BrodyPennell", "{{SOCIAL_FACEBOOK}}"),
 ("https://www.instagram.com/brodypennell/", "{{SOCIAL_INSTAGRAM}}"),
 ("https://www.youtube.com/c/BrodyPennellLosAngeles", "{{SOCIAL_YOUTUBE}}"),
 ("https://www.linkedin.com/company/brody-pennell-hvac/", "{{SOCIAL_LINKEDIN}}"),
 # city (Greater first)
 ("Greater Los Angeles", "Greater {{CITY}}"),
 ("Los Angeles and Orange Counties", "{{CITY}} and surrounding areas"),
 ("Los Angeles", "{{CITY}}"),
]
def templatize(html):
    html = html.replace("https://www.brodypennell.com", "https://brodypennell.com")  # normalize www
    # reviews carry brand-naming customer text -> tokenize to placeholders
    html = re.sub(r'(<div class="rpi-text[^"]*"[^>]*>).*?(</div>)', r'\1{{REVIEW_TEXT}}\2', html, flags=D)
    html = re.sub(r'(<a[^>]*class="rpi-name"[^>]*>).*?(</a>)', r'\1{{REVIEW_AUTHOR}}\2', html, flags=D)
    html = re.sub(r'(<div class="rpi-time"[^>]*>).*?(</div>)', r'\1{{REVIEW_TIME}}\2', html, flags=D)
    for a, b in GENERIC: html = html.replace(a, b)
    for pat, rep in GENERIC_RE: html = re.sub(pat, rep, html)
    for a, b in TOKENIZE: html = html.replace(a, b)
    html = re.sub(r'\bLA\b', '{{CITY}}', html)
    # specific rating-badge images -> neutral 5-star badge
    html = re.sub(r'<img[^>]*Reviews(?:-1|-2)?\.svg[^>]*>',
                  '<img src="assets/rating-stars.svg" width="150" height="30" class="el-image" '
                  'alt="5-star rated" loading="lazy">', html)
    # drop the Carrier manufacturer lockup (brand-specific)
    html = re.sub(r'<img[^>]*CAR-ForTheWorldWeShare[^>]*>',
                  '<!-- optional: manufacturer badge {{MANUFACTURER_BADGE_URL}} -->', html)
    # ---- neutralize brand imagery (logo / award badges / photos / bg photos) ----
    html = html.replace("assets/Mobile-nav-Logo.svg", "assets/logo-placeholder.svg")
    html = html.replace("assets/logo-brody-large-e1651600417485-2.png", "assets/logo-placeholder.svg")
    # award / trust / cert badges -> neutral "licensed & insured" seal
    html = re.sub(r'<img[^>]*(?:BBB-resized\.svg|7x-final\.svg|Nate-Cert-Brody[^"]*)[^>]*>',
                  '<img src="assets/badge-placeholder.svg" width="275" height="275" '
                  'class="el-image" alt="Licensed and insured" loading="lazy">', html)
    # strip brand <picture> sources + lazy/srcset/background photos (degrade to section color)
    html = re.sub(r'<source[^>]*brodypennell\.com[^>]*>', '', html)
    html = re.sub(r'\s*srcset="[^"]*brodypennell\.com[^"]*"', '', html)
    html = re.sub(r'\s*data-sources="[^"]*"', '', html)
    html = re.sub(r'data-src="[^"]*brodypennell\.com[^"]*"', 'data-src=""', html)
    # hero photo had baked brand text + light overlay text -> neutral navy so hero text stays readable
    html = re.sub(r'background-image:\s*url\([^)]*Brody-Pennell-6[^)]*\)\s*;?', 'background-color:#182d43;', html)
    html = re.sub(r'background-image:\s*url\([^)]*brodypennell\.com[^)]*\)\s*;?', '', html)
    # remaining brand content photos -> neutral image placeholder
    html = re.sub(r'assets/(?:Brody-[^"]*|Los-Angeles-[^"]*|HVAC-Blog[^"]*)', 'assets/placeholder.svg', html)
    # strip plugin JS fallback handlers + any absolute brand-hosted <img src>
    html = re.sub(r'\s*onerror="[^"]*"', '', html)
    html = re.sub(r'src="https://brodypennell\.com/[^"]*"', 'src="assets/placeholder.svg"', html)
    # company-specific external profile / award links (BBB profile, LA Times best-of) -> neutral
    html = re.sub(r'href="https://(?:www\.)?(?:bbb\.org|latimes\.com)/[^"]*"', 'href="#"', html)
    # leftover brand-name mentions in prose (AFTER image paths handled, so filenames are safe)
    html = html.replace("Brody-Pennell", "{{BUSINESS_SHORT_NAME}}").replace("Brody", "{{BUSINESS_SHORT_NAME}}")
    # final safety net: any remaining brand-domain ref -> SITE_URL token (hrefs localized after)
    html = html.replace("https://brodypennell.com", "{{SITE_URL}}").replace("brodypennell.com", "{{SITE_URL}}")
    return html

# ---------------------------------------------- asset + main extraction
def vendor_assets(stem):
    src = os.path.join(DOWN, stem + "_files")
    if not os.path.isdir(src): return
    for f in os.listdir(src):
        if f.lower().endswith(IMG_EXT):
            dst = os.path.join(ASSETS, f)
            if not os.path.exists(dst):
                try: shutil.copy(os.path.join(src, f), dst)
                except Exception: pass

def clean_main(stem):
    html = open(os.path.join(DOWN, stem + ".html"), encoding="utf-8", errors="replace").read()
    main = html[html.index('<main id="tm-main"'):html.index("</main>") + len("</main>")]
    main = re.sub(r"<script\b[^>]*>.*?</script>", "", main, flags=D)
    main = re.sub(r"<noscript\b[^>]*>.*?</noscript>", "", main, flags=D)
    main = re.sub(r'<div class="gf_browser[^"]*gform_wrapper.*?</form>\s*</div>', DEMO_FORM, main, flags=D)
    main = re.sub(r'<div[^>]*gform_wrapper.*?</form>\s*</div>', DEMO_FORM, main, flags=D)
    main = main.replace('onclick="SimpleScheduler.open()"', 'onclick="openGhlCalendar();return false;"')
    vendor_assets(stem)
    main = main.replace("./" + stem + "_files/", "assets/").replace(stem + "_files/", "assets/")
    main = re.sub(r'(["\'(\s])/wp-content/', r'\1https://brodypennell.com/wp-content/', main)
    main = re.sub(r'\\/wp-content\\/', r'https:\\/\\/brodypennell.com\\/wp-content\\/', main)
    def add_bg(m):
        tag = m.group(0)
        if "background-image" in tag: return tag
        ds = re.search(r'data-src="([^"]+)"', tag)
        if not ds: return tag
        u = ds.group(1)
        return tag.replace('style="', f'style="background-image:url(&quot;{u}&quot;);', 1) if 'style="' in tag \
               else tag[:-1] + f' style="background-image:url(&quot;{u}&quot;)">'
    return re.sub(r'<div\b[^>]*\buk-img=""[^>]*>', add_bg, main)

# ---------------------------------------------- shared chrome from template.html
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
PRE  = tpl[:tpl.index('<main id="tm-main"')]
POST = tpl[tpl.index("</main>") + len("</main>"):]
HOME_MAIN = tpl[tpl.index('<main id="tm-main"'):tpl.index("</main>") + len("</main>")]

JSONLD = ('<script type="application/ld+json">{"@context":"https://schema.org",'
 '"@type":"HVACBusiness","name":"{{BUSINESS_NAME}}","telephone":"{{PHONE_DISPLAY}}",'
 '"url":"{{SITE_URL}}","image":"{{OG_IMAGE_URL}}","areaServed":"{{CITY}}",'
 '"address":{"@type":"PostalAddress","streetAddress":"{{ADDRESS}}","addressLocality":"{{CITY}}"},'
 '"sameAs":["{{SOCIAL_FACEBOOK}}","{{SOCIAL_INSTAGRAM}}","{{SOCIAL_YOUTUBE}}","{{SOCIAL_LINKEDIN}}"]}</script>')

# brand hero photos are removed for the template; keep the hero band readable (white text)
TEMPLATE_CSS = ('<style>/* template: light-text (uk-light) sections keep a dark backdrop where brand photos were removed */'
 '.tm-page .uk-section.uk-light,.tm-page .uk-section-default.uk-light,'
 '.tm-page .uk-section-muted.uk-light{background-color:#182d43}</style>')

def seo(page, slug, title, desc):
    canon = "{{SITE_URL}}/" + ("" if slug == "index.html" else slug)
    page = page.replace("{{SEO_TITLE}}", title).replace("{{SEO_DESCRIPTION}}", desc)
    page = re.sub(r'(<title>).*?(</title>)', lambda m: m.group(1) + title + m.group(2), page, flags=D)
    page = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + desc + m.group(2), page)
    page = re.sub(r'(<link rel="canonical" href=")[^"]*(">)', lambda m: m.group(1) + canon + m.group(2), page)
    page = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', lambda m: m.group(1) + canon + m.group(2), page)
    if "application/ld+json" not in page:
        page = page.replace("</head>", JSONLD + TEMPLATE_CSS + "\n</head>", 1)
    return page

def build(slug, title, desc, main):
    page = PRE + main + POST
    page = templatize(page)
    page = rewrite_links(page)
    page = seo(page, slug, title, desc)
    return MARKER + page

# =============================================================================
print("[home] index.html")
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(
    build("index.html", "{{BUSINESS_NAME}} | Heating & Air Conditioning in {{CITY}}",
          "{{BUSINESS_NAME}} provides professional heating and air conditioning services in "
          "{{CITY}} and surrounding areas. Call {{PHONE_DISPLAY}} to schedule service today.",
          HOME_MAIN))

# saved interior pages: (stem, slug, title, desc)
SAVED = [
 ("About Our HVAC Technicians at Brody Pennell _ Brody Pennell", "about.html",
  "About {{BUSINESS_NAME}} | {{CITY}} HVAC Experts",
  "Meet {{BUSINESS_NAME}}, your local heating and air conditioning team serving {{CITY}}. "
  "Licensed, insured, and trusted by homeowners. Call {{PHONE_DISPLAY}}."),
 ("Contact - Brody Pennell", "contact.html",
  "Contact {{BUSINESS_NAME}} | {{CITY}} Heating & Air Conditioning",
  "Contact {{BUSINESS_NAME}} for heating and air conditioning service in {{CITY}}. "
  "Call {{PHONE_DISPLAY}} or request service online."),
 ("Reviews - Brody Pennell", "reviews.html",
  "Customer Reviews | {{BUSINESS_NAME}}",
  "Read what {{CITY}} homeowners say about {{BUSINESS_NAME}}'s heating and air conditioning service."),
 ("Cities Served - Brody Pennell", "cities.html",
  "Service Areas | {{BUSINESS_NAME}}",
  "{{BUSINESS_NAME}} provides heating and air conditioning service across {{CITY}} and the "
  "surrounding areas. Call {{PHONE_DISPLAY}}."),
 ("Expert Air Conditioning Service in Los Angeles, CA", "air-conditioning.html",
  "Air Conditioning Services in {{CITY}} | {{BUSINESS_NAME}}",
  "Professional air conditioning installation, repair, and maintenance in {{CITY}} from "
  "{{BUSINESS_NAME}}. Call {{PHONE_DISPLAY}}."),
 ("Reliable AC Repair in Los Angeles, CA _ Brody Pennell", "ac-repair.html",
  "AC Repair in {{CITY}} | {{BUSINESS_NAME}}",
  "Fast, reliable AC repair in {{CITY}} from {{BUSINESS_NAME}}. Licensed technicians, "
  "upfront pricing. Call {{PHONE_DISPLAY}}."),
]
CLEAN = {}
for stem, slug, title, desc in SAVED:
    print("[clone]", slug)
    CLEAN[slug] = clean_main(stem)
    open(os.path.join(HERE, slug), "w", encoding="utf-8").write(build(slug, title, desc, CLEAN[slug]))

# derived pages share a layout; swap the service noun in the (already-templatized) base main
def desc_for(svc): return (f"Professional {svc.lower()} in {{{{CITY}}}} from {{{{BUSINESS_NAME}}}}. "
                           f"Licensed, insured technicians. Call {{{{PHONE_DISPLAY}}}}.")
def pairs_detail(label, lc, unit, unit_lc, heating):
    p = [("Award-Winning AC Repair Los Angeles", label), ("AC Repair", label),
         ("AC repair", lc), ("ac repair", lc), ("Air Conditioning Repair", label),
         ("air conditioning repair", lc)]
    if heating:
        p += [("air conditioner", unit_lc), ("Air Conditioner", unit),
              ("air conditioning", "heating"), ("Air Conditioning", "Heating"),
              ("AC unit", unit_lc), ("A/C", unit), (" AC ", " " + unit_lc + " "), ("cooling", "heating")]
    else:
        p += [("air conditioner", unit_lc), ("Air Conditioner", unit)]
    return p
def pairs_cat(label, lc, heating):
    p = [("Professional AC Services In", "Professional " + label + " Services In"),
         ("Air Conditioning", label), ("air conditioning", lc)]
    if heating: p += [("air conditioner", "system"), ("AC unit", "system"), (" AC ", " " + lc + " "), ("cooling", "heating")]
    return p

CATEGORIES = [
 ("heating", "Heating Services in {{CITY}} | {{BUSINESS_NAME}}", desc_for("heating services"), pairs_cat("Heating", "heating", True)),
 ("indoor-air-quality", "Indoor Air Quality in {{CITY}} | {{BUSINESS_NAME}}", desc_for("indoor air quality services"), pairs_cat("Indoor Air Quality", "indoor air quality", False)),
]
DETAILS = [
 ("ac-maintenance", "AC Maintenance", pairs_detail("AC Maintenance","AC maintenance","air conditioner","air conditioner",False)),
 ("ac-replacement", "AC Replacement", pairs_detail("AC Replacement","AC replacement","air conditioner","air conditioner",False)),
 ("ductless-mini-splits", "Ductless Mini-Splits", pairs_detail("Ductless Mini-Splits","ductless mini-splits","mini-split","mini-split",False)),
 ("thermostat-repair", "Thermostat Repair", pairs_detail("Thermostat Repair","thermostat repair","thermostat","thermostat",False)),
 ("heater-repair", "Heater Repair", pairs_detail("Heater Repair","heater repair","Heater","heater",True)),
 ("heater-installation", "Heater Installation", pairs_detail("Heater Installation","heater installation","Heater","heater",True)),
 ("heater-maintenance", "Heater Maintenance", pairs_detail("Heater Maintenance","heater maintenance","Heater","heater",True)),
 ("heat-pumps", "Heat Pump Services", pairs_detail("Heat Pump Services","heat pump services","Heat Pump","heat pump",True)),
 ("heat-pump-repair", "Heat Pump Repair", pairs_detail("Heat Pump Repair","heat pump repair","Heat Pump","heat pump",True)),
 ("furnaces", "Furnace Services", pairs_detail("Furnace Services","furnace services","Furnace","furnace",True)),
 ("furnace-repair", "Furnace Repair", pairs_detail("Furnace Repair","furnace repair","Furnace","furnace",True)),
 ("furnace-installation", "Furnace Installation", pairs_detail("Furnace Installation","furnace installation","Furnace","furnace",True)),
 ("duct-cleaning", "Duct Cleaning", pairs_detail("Duct Cleaning","duct cleaning","duct system","duct system",True)),
]
def apply_pairs(main, pairs):
    for a, b in pairs: main = main.replace(a, b)
    return main

for slug, title, desc, pairs in CATEGORIES:
    print("[derive cat]", slug)
    m = apply_pairs(CLEAN["air-conditioning.html"], pairs)
    open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8").write(
        build(slug + ".html", title, desc, m))
for slug, label, pairs in DETAILS:
    print("[derive]", slug)
    m = apply_pairs(CLEAN["ac-repair.html"], pairs)
    open(os.path.join(HERE, slug + ".html"), "w", encoding="utf-8").write(
        build(slug + ".html", label + " in {{CITY}} | {{BUSINESS_NAME}}", desc_for(label), m))

# ---------------------------------------------- sitemap + robots
pages = ["index.html"] + sorted(f for f in os.listdir(HERE)
         if f.endswith(".html") and f not in ("template.html", "index.html"))
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in pages:
    loc = "{{SITE_URL}}/" + ("" if p == "index.html" else p)
    sm.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq></url>")
sm.append("</urlset>")
open(os.path.join(HERE, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(HERE, "robots.txt"), "w").write(
    "User-agent: *\nAllow: /\n\nSitemap: {{SITE_URL}}/sitemap.xml\n")

print(f"\nWROTE {len(pages)} pages + sitemap.xml + robots.txt")
