#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ONBOARD A CLIENT  ->  edit config.json, then:  python3 generate.py
Produces a finished, fully-filled website in  dist/  (deploy that folder).

- Fills every {{TOKEN}} from config.json; anything omitted uses a generic default below.
- Expands the reviews + service-area city lists from config.
- Applies the client's brand colors.
- Copies assets/ + styles.css and writes sitemap.xml + robots.txt.
The token source pages (index.html, about.html, ... at repo root) are never modified.
"""
import json, os, re, shutil, itertools, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
SRC_PAGES = sorted(f for f in os.listdir(HERE)
                   if f.endswith(".html") and f not in ("template.html",))
# python3 generate.py [config.json | clients/<name>.json]
CFG_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "config.json")
cfg = json.load(open(CFG_PATH, encoding="utf-8"))

c = cfg.get("city", "your area")
n = cfg.get("business_name", "Our Company")
sn = cfg.get("business_short_name", n)
pd = cfg.get("phone_display", "(555) 555-5555")

# ---- generic copy defaults (used when config doesn't override) --------------
DEFAULTS = {
 "HERO_HEADLINE": "Reliable Heating & Air Conditioning You Can Count On",
 "HERO_SUBHEADLINE": "Fast, friendly, professional HVAC service for your home or business.",
 "SERVICES_EYEBROW": "Our Services",
 "SERVICES_HEADING": f"Heating & Air Conditioning in {c}",
 "SERVICES_INTRO": "From repairs and tune-ups to brand-new installations, our licensed technicians keep your home comfortable all year long.",
 "INTRO_HEADING": f"Heating & Air Conditioning in {c} and Surrounding Areas",
 "INTRO_PARAGRAPH_1": "We're a locally owned heating and air conditioning company built on honest work and dependable comfort. From the first call to the final walkthrough, we treat your home like our own.",
 "INTRO_PARAGRAPH_2": "Our trained technicians service, repair, and install every major brand of heating and cooling equipment, using up-to-date methods and quality parts.",
 "INTRO_PARAGRAPH_3": "Whatever your home needs, we have the experience to deliver a comfortable, efficient, and lasting solution.",
 "INTRO_CONTACT_NOTE": f"We're here for you 24/7! To get started with your service, repair, or replacement, contact {n} at {pd} or request service online.",
 "ABOUT_HEADING": f"Trusted Heating & Air Conditioning in {c}",
 "ABOUT_PARAGRAPH_1": "Looking for comfort you can count on? You're in the right place. Our team guides you from start to finish and recommends options that fit both your comfort and your budget.",
 "ABOUT_PARAGRAPH_2": "A new system is a big investment, so we take the time to understand your home and your goals before we recommend anything.",
 "ABOUT_PARAGRAPH_3": "We've built our reputation on clean, courteous, on-time service — and on systems that keep you comfortable for years to come.",
 "REVIEWS_EYEBROW": "Reviews",
 "REVIEWS_HEADING": "What Our Customers Say",
 "REVIEWS_SUBTEXT": "Highly rated for quality work, fair pricing, and friendly, professional service.",
 "REVIEWS_PROFILE_URL": "#",
 "AREAS_EYEBROW": "Service Areas",
 "AREAS_HEADING": f"Proudly Serving {c} and the Surrounding Areas",
 "BLOG_EYEBROW": "Resources",
 "BLOG_HEADING": "HVAC Tips for Homeowners",
 "SCHEDULE_EYEBROW": "We're Here For You",
 "SCHEDULE_HEADING": "Schedule Your Service Today",
 "SCHEDULE_INTRO": f"Comfort is just a call away. Contact {n} at {pd} or book online.",
 "FOOTER_ABOUT": f"{n} provides professional heating and air conditioning service to {c} and the surrounding areas. We're here for you!",
 "YEAR": "2026",
}

# ---- build the {{TOKEN}} -> value map ---------------------------------------
def s(key, default=""):
    return str(cfg.get(key, default))
TOK = {
 "BUSINESS_NAME": s("business_name"), "BUSINESS_SHORT_NAME": s("business_short_name"),
 "PHONE": s("phone"), "PHONE_DISPLAY": s("phone_display"), "EMAIL": s("email"),
 "CITY": c, "ADDRESS": s("address"), "LICENSE": s("license"), "OFFICE_HOURS": s("office_hours"),
 "YEAR_FOUNDED": s("year_founded"), "YEARS_IN_BUSINESS": s("years_in_business"),
 "SITE_URL": s("site_url").rstrip("/"),
 "GHL_CONTACT_FORM_ID": s("ghl_contact_form_id"), "GHL_CALENDAR_ID": s("ghl_calendar_id"),
 "GHL_CHAT_WIDGET_ID": s("ghl_chat_widget_id"),
 "SOCIAL_FACEBOOK": s("social_facebook", "#"), "SOCIAL_INSTAGRAM": s("social_instagram", "#"),
 "SOCIAL_YOUTUBE": s("social_youtube", "#"), "SOCIAL_LINKEDIN": s("social_linkedin", "#"),
 "LOGO_URL": s("logo_url", "assets/logo-placeholder.svg"),
 "OG_IMAGE_URL": s("og_image_url", "assets/placeholder.svg"),
 "FAVICON_URL": s("favicon_url", "assets/logo-placeholder.svg"),
 "FAVICON_SVG_URL": s("favicon_svg_url", "assets/logo-placeholder.svg"),
 "MANUFACTURER_BADGE_URL": s("manufacturer_badge_url"),
 "DIRECTIONS_URL": s("directions_url", "#"),
 "SERVICE_AREA_MAP_EMBED_URL": s("service_area_map_embed_url", "#"),
}
TOK.update(DEFAULTS)
for k, v in (cfg.get("copy_overrides") or {}).items():       # config copy overrides win
    if not k.startswith("_"):
        TOK[k.upper()] = v

BRAND_CSS = ("<style>/* client brand colors */"
 ".uk-button-primary{{background-color:{p}!important;border-color:{p}!important}}"
 ".tm-header,.tm-toolbar,.uk-section-secondary,.uk-section.uk-light,"
 ".tm-page>* .uk-background-cover.uk-section{{background-color:{d}}}"
 "a:hover,.uk-text-primary{{color:{p}!important}}</style>").format(
    p=cfg.get("brand_primary", "#fc7504"), d=cfg.get("brand_dark", "#182d43"))

reviews = cfg.get("reviews") or [{"author": "Happy Customer", "text": "Great service!", "time": "recently"}]
cities = cfg.get("cities") or [c]

# ---- fillers ----------------------------------------------------------------
def fill_reviews(html):
    # clone the home REPEAT card once per review, then fill every review card cyclically
    def expand(m):
        return m.group(1) * len(reviews)
    html = re.sub(r'<!-- BEGIN REPEAT: review.*?-->(.*?)<!-- END REPEAT: review -->',
                  expand, html, flags=re.S)
    for tok, key in (("REVIEW_AUTHOR", "author"), ("REVIEW_TEXT", "text"), ("REVIEW_TIME", "time")):
        it = itertools.cycle(reviews)
        html = re.sub(r"\{\{" + tok + r"\}\}", lambda mm, it=it, key=key: str(next(it)[key]), html)
    html = html.replace("{{REVIEW_RATING}}", "5").replace("{{REVIEW_PROVIDER}}", "google")
    html = html.replace("{{REVIEWS_PROFILE_URL}}", TOK["REVIEWS_PROFILE_URL"])
    return html

def fill_cities(html):
    def rebuild_from(li_tpl):
        out = ""
        for city in cities:
            x = re.sub(r"(<p[^>]*>).*?(</p>)", lambda mm: mm.group(1) + city + mm.group(2),
                       li_tpl, count=1, flags=re.S)
            x = re.sub(r'href="[^"]*"', 'href="#"', x)
            out += x
        return out
    # home REPEAT block
    def rep_block(m):
        li = re.search(r'<li class="el-item">.*?</li>', m.group(1), re.S)
        return rebuild_from(li.group(0)) if li else m.group(0)
    html = re.sub(r'<!-- BEGIN REPEAT: service_area_city.*?-->(.*?)<!-- END REPEAT: service_area_city -->',
                  rep_block, html, flags=re.S)
    # any remaining location-pin city list (e.g. the Cities page)
    def rep_list(m):
        ul = m.group(0)
        li = re.search(r'<li class="el-item">.*?</li>', ul, re.S)
        if not li:
            return ul
        return ul[:ul.index(">") + 1] + rebuild_from(li.group(0)) + "</ul>"
    html = re.sub(r'<ul[^>]*\buk-list\b[^>]*>(?:(?!</ul>).)*?icon: location;(?:(?!</ul>).)*?</ul>',
                  rep_list, html, flags=re.S)
    return html

def fill_page(html):
    html = re.sub(r'<!-- TEMPLATE —.*?-->\n?', '', html, flags=re.S)  # filled site is not a template
    html = html.replace("{{CITY}} County", "the {{CITY}} area")        # avoid invalid "Xville County"
    if not TOK.get("YEAR_FOUNDED"):                                    # no founding year -> year-free copy
        for a, b in [("in business since {{YEAR_FOUNDED}}", "in business for many years"),
                     ("Back in {{YEAR_FOUNDED}},", "Over the years,"),
                     ("since {{YEAR_FOUNDED}}", "for many years"),
                     ("in {{YEAR_FOUNDED}}", "over the years")]:
            html = html.replace(a, b)
    html = fill_reviews(html)
    html = fill_cities(html)
    for tok, val in TOK.items():
        html = html.replace("{{" + tok + "}}", val)
    html = html.replace("</head>", BRAND_CSS + "\n</head>", 1)
    return html

# ---- write dist/ ------------------------------------------------------------
shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)
shutil.copytree(os.path.join(HERE, "assets"), os.path.join(DIST, "assets"))
shutil.copy(os.path.join(HERE, "styles.css"), DIST)

for f in SRC_PAGES:
    out = fill_page(open(os.path.join(HERE, f), encoding="utf-8").read())
    open(os.path.join(DIST, f), "w", encoding="utf-8").write(out)

site = TOK["SITE_URL"]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for f in ["index.html"] + [p for p in SRC_PAGES if p != "index.html"]:
    loc = site + "/" + ("" if f == "index.html" else f)
    sm.append(f"  <url><loc>{loc}</loc><changefreq>monthly</changefreq></url>")
sm.append("</urlset>")
open(os.path.join(DIST, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
open(os.path.join(DIST, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {site}/sitemap.xml\n")

leftover = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", "".join(
    open(os.path.join(DIST, f), encoding="utf-8").read() for f in SRC_PAGES))))
print(f"Generated dist/ for '{n}' — {len(SRC_PAGES)} pages, {len(cities)} cities, {len(reviews)} reviews.")
if leftover:
    print("  WARNING unfilled tokens:", ", ".join(leftover))
else:
    print("  All tokens filled. Deploy:  vercel deploy dist --prod")
