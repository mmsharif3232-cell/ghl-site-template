#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convert the token source pages into GHL-ready custom-code pages.

Output -> ghl/<slug>.html : paste each into a GoHighLevel page's Custom Code element.
Tokens become GHL merge fields:
  * built-ins  -> {{location.name}}, {{location.phone}}, {{location.full_address}}, {{location.city}}, ...
  * everything else -> {{custom_values.<field>}}  (set once per sub-account in Settings -> Custom Values)
CSS/JS/images load from ASSET_BASE (our hosted build; re-host in GHL Media Library if you prefer).
Also writes GHL-CUSTOM-VALUES.md (the exact list of custom values to create).
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ghl")
ASSET_BASE = "https://ghl-site-template.vercel.app"   # serves styles.css + assets/
SRC = sorted(f for f in os.listdir(HERE) if f.endswith(".html") and f != "template.html")

# token -> GHL built-in merge field (auto-populated from the sub-account's business profile)
BUILTIN = {
 "BUSINESS_NAME": "{{location.name}}",
 "PHONE": "{{location.phone}}", "PHONE_DISPLAY": "{{location.phone}}",
 "EMAIL": "{{location.email}}", "ADDRESS": "{{location.full_address}}",
 "CITY": "{{location.city}}", "SITE_URL": "{{location.website}}",
}
# slug (no .html) -> GHL funnel page path
def page_path(slug):
    return "/" if slug == "index.html" else "/" + slug[:-5]

# generic placeholder content for the repeating lists (edit per client in GHL, or use GHL widgets)
CITIES = ["Your City", "Nearby Town", "Suburb One", "Suburb Two", "Suburb Three",
          "Suburb Four", "Suburb Five", "Suburb Six"]
REVIEWS = [("Sarah M.", "Fast, professional, and friendly — fixed it same day. Highly recommend!", "2 days ago"),
           ("David R.", "Honest pricing and great communication. No upsell, just good work.", "1 week ago"),
           ("Lena P.", "Explained everything clearly and left the place spotless. Five stars.", "2 weeks ago"),
           ("Marcus T.", "New system installed in a day. Works perfectly and runs quietly.", "3 weeks ago"),
           ("Priya K.", "Quick response and a fair quote. We'll use them again.", "1 month ago"),
           ("Tom B.", "Maintenance plan is worth it — runs better than ever.", "1 month ago")]

used = set()
def to_merge(tok):
    if tok in BUILTIN:
        return BUILTIN[tok]
    field = tok.lower()
    used.add(field)
    return "{{custom_values." + field + "}}"

def fill_reviews(html):
    html = re.sub(r'<!-- BEGIN REPEAT: review.*?-->(.*?)<!-- END REPEAT: review -->',
                  lambda m: m.group(1) * len(REVIEWS), html, flags=re.S)
    import itertools
    for tok, idx in (("REVIEW_AUTHOR", 0), ("REVIEW_TEXT", 1), ("REVIEW_TIME", 2)):
        it = itertools.cycle(REVIEWS)
        html = re.sub(r"\{\{" + tok + r"\}\}", lambda mm, it=it, i=idx: next(it)[i], html)
    return (html.replace("{{REVIEW_RATING}}", "5").replace("{{REVIEW_PROVIDER}}", "google")
                .replace("{{REVIEWS_PROFILE_URL}}", "#"))

def fill_cities(html):
    def rebuild(li):
        return "".join(re.sub(r"(<p[^>]*>).*?(</p>)", lambda mm: mm.group(1) + ct + mm.group(2),
                              re.sub(r'href="[^"]*"', 'href="#"', li), count=1, flags=re.S) for ct in CITIES)
    html = re.sub(r'<!-- BEGIN REPEAT: service_area_city.*?-->(.*?)<!-- END REPEAT: service_area_city -->',
                  lambda m: (lambda li: rebuild(li.group(0)) if li else m.group(0))(
                      re.search(r'<li class="el-item">.*?</li>', m.group(1), re.S)), html, flags=re.S)
    html = re.sub(r'<ul[^>]*\buk-list\b[^>]*>(?:(?!</ul>).)*?icon: location;(?:(?!</ul>).)*?</ul>',
                  lambda m: (lambda li: m.group(0)[:m.group(0).index(">") + 1] + rebuild(li.group(0)) + "</ul>"
                             if li else m.group(0))(re.search(r'<li class="el-item">.*?</li>', m.group(0), re.S)),
                  html, flags=re.S)
    return html

GHL_FORM = ('\n<!-- GHL: drop a native GHL FORM element here (leads flow into the CRM). '
            'Or embed: --><div class="ghl-embed ghl-embed--form">'
            '<iframe src="https://api.leadconnectorhq.com/widget/form/{{custom_values.ghl_form_id}}" '
            'style="width:100%;height:600px;border:none;border-radius:6px" title="Request Service"></iframe>'
            '<script src="https://link.msgsndr.com/js/form_embed.js"></script></div>\n')

def convert(html):
    html = re.sub(r'<!-- TEMPLATE —.*?-->\n?', '', html, flags=re.S)
    html = fill_reviews(html)
    html = fill_cities(html)
    # static demo form -> GHL form (native element preferred; iframe shown as fallback)
    html = re.sub(r'<div class="ghl-embed ghl-embed--form">.*?</form></div>', GHL_FORM, html, flags=re.S)
    # tokens -> GHL merge fields
    html = re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: to_merge(m.group(1)), html)
    # assets + stylesheet -> absolute hosted base
    html = html.replace('href="styles.css"', f'href="{ASSET_BASE}/styles.css"')
    html = re.sub(r'(src|href)="assets/', rf'\1="{ASSET_BASE}/assets/', html)
    # internal nav links (slug.html) -> GHL page paths (/slug)
    html = re.sub(r'href="([a-z0-9-]+)\.html"', lambda m: f'href="{page_path(m.group(1)+".html")}"', html)
    html = html.replace('href="index.html"', 'href="/"')
    return html

os.makedirs(OUT, exist_ok=True)
for f in SRC:
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(
        convert(open(os.path.join(HERE, f), encoding="utf-8").read()))

# manifest of custom values to create in GHL
lines = ["# GHL Custom Values to create", "",
 "Settings → Custom Values (per sub-account). Built-ins below are auto-filled from the",
 "sub-account's Business Profile — you don't create those.", "",
 "## Auto-filled built-ins (no setup)",
 "`{{location.name}}` · `{{location.phone}}` · `{{location.email}}` · `{{location.full_address}}` · `{{location.city}}` · `{{location.website}}`",
 "", "## Custom values to add", ""]
for field in sorted(used):
    lines.append(f"- `{{{{custom_values.{field}}}}}`")
open(os.path.join(HERE, "GHL-CUSTOM-VALUES.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")

print(f"Wrote ghl/ ({len(SRC)} pages) + GHL-CUSTOM-VALUES.md")
print(f"{len(used)} custom values: " + ", ".join(sorted(used)))
