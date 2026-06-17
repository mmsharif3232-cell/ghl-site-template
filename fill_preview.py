#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill index.html template with the real Brody values -> _preview.html (local
verification only; the delivered index.html stays templated). Long body copy is
pulled programmatically from the saved source so the render is faithful."""
import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.expanduser("~/Downloads/Brody Pennell Heating & Air Conditioning in Los Angeles, CA..html")
src  = open(SRC, encoding="utf-8", errors="replace").read()
D = re.DOTALL

def grab(pat):
    m = re.search(pat, src, D)
    return m.group(1).strip() if m else "(missing)"

V = {
 "SEO_TITLE": "Brody Pennell Heating &amp; Air Conditioning in Los Angeles, CA.",
 "SEO_DESCRIPTION": "Brody Pennell is a locally rated HVAC company in LA.",
 "SITE_URL": "https://brodypennell.com",
 "BUSINESS_NAME": "Brody Pennell Heating &amp; Air Conditioning",
 "BUSINESS_SHORT_NAME": "Brody Pennell",
 "PHONE": "4243263045", "PHONE_DISPLAY": "(424) 326-3045",
 "HERO_HEADLINE": "Proudly Serving <br>Los Angeles Since 1945",
 "HERO_SUBHEADLINE": "Los Angeles’ Premier Heating &amp; Air Conditioning Company",
 "SERVICES_EYEBROW": "Our Services",
 "SERVICES_HEADING": "Los Angeles Heating &amp; Air Conditioning",
 "INTRO_HEADING": "Heating and Air Conditioning in Los Angeles and Surrounding Areas",
 "ABOUT_HEADING": "Fixing Air Conditioners &amp; Heaters in Los Angeles for 80 Years",
 "REVIEWS_EYEBROW": "Ratings &amp; Reviews",
 "REVIEWS_HEADING": "Check Out Our 5-Star Reviews!",
 "REVIEWS_PROFILE_URL": "https://search.google.com/local/reviews",
 "AREAS_EYEBROW": "Areas We Serve",
 "AREAS_HEADING": "Serving Greater Los Angeles And The Surrounding Areas",
 "BLOG_EYEBROW": "The Blog",
 "BLOG_HEADING": "Expert HVAC Tips For Homeowners",
 "SCHEDULE_EYEBROW": "We Are Here For You",
 "SCHEDULE_HEADING": "Schedule Your Service Today",
 "ADDRESS": "8599 Venice Blvd., Los Angeles, CA 90034",
 "DIRECTIONS_URL": "https://maps.app.goo.gl/5bi9bmXTSVHsP9HC8",
 "LICENSE": "CA LIC# 256821",
 "OFFICE_HOURS": "Mon – Fri: 7:00am – 5:00pm<br>Sat: 8:00am − 1:00pm<br>Sun: CLOSED",
 "YEAR": "2026",
 "SOCIAL_FACEBOOK": "https://www.facebook.com/BrodyPennell",
 "SOCIAL_INSTAGRAM": "https://www.instagram.com/brodypennell/",
 "SOCIAL_YOUTUBE": "https://www.youtube.com/c/BrodyPennellLosAngeles",
 "SOCIAL_LINKEDIN": "https://www.linkedin.com/company/brody-pennell-hvac/",
 "FAVICON_URL": "https://brodypennell.com/wp-content/uploads/2023/01/Brody-Pennell-Favicon-1.png",
 "FAVICON_SVG_URL": "https://brodypennell.com/wp-content/uploads/2023/01/Brody-Pennell-Favicon-1.svg",
 "OG_IMAGE_URL": "https://brodypennell.com/wp-content/uploads/2022/08/PROUDLY-SERVING-LOS-ANGELES-SINCE-1945.jpg",
 "SERVICE_AREA_MAP_EMBED_URL": "https://www.google.com/maps/d/embed?mid=1EIzEADBVySeuqWsrYIEzVWhDTKgZW2I",
 "GHL_CONTACT_FORM_ID": "DEMO_FORM", "GHL_CALENDAR_ID": "DEMO_CAL", "GHL_CHAT_WIDGET_ID": "DEMO_CHAT",
 # body copy pulled from the saved source
 "SERVICES_INTRO":     grab(r'id="page#6"><p>(.*?)</p>'),
 "REVIEWS_SUBTEXT":    grab(r'id="page#16"><p>(.*?)</p>'),
 "INTRO_PARAGRAPH_1":  grab(r'<p>(Though we are one of the longest-running.*?)</p>'),
 "INTRO_PARAGRAPH_2":  grab(r'<p>(Opening our doors in 1945.*?)</p>'),
 "INTRO_PARAGRAPH_3":  grab(r'<p>(With 80 years of experience.*?)</p>'),
 "INTRO_CONTACT_NOTE": grab(r'<p>(We’re here for you 24/7.*?)</p>'),
 "ABOUT_PARAGRAPH_1":  grab(r'<p>(Ready to get a new air conditioner.*?)</p>'),
 "ABOUT_PARAGRAPH_2":  grab(r'<p>(A new AC is a big investment.*?)</p>'),
 "ABOUT_PARAGRAPH_3":  grab(r'<p>(We have a reputation.*?)</p>'),
 "SCHEDULE_INTRO":     grab(r'(<strong>We aren’t comfortable until you are!</strong>.*?)</p>'),
 "FOOTER_ABOUT":       grab(r'<span>(Since 1945, Brody Pennell.*?)</span>'),
 # single review sample (the REPEAT card)
 "REVIEW_PROVIDER": "google", "REVIEW_RATING": "5",
 "REVIEW_AUTHOR": "Juan Jose H.", "REVIEW_TIME": "2 days ago",
 "REVIEW_TEXT": "Great, fast, professional service. Highly recommend!",
}

html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()

# demo only: the live showcase has no real GHL form ID, so show a static mockup
# instead of an empty GHL "form not found" iframe (the template keeps the real embed)
DEMO_FORM = ('<div class="ghl-embed ghl-embed--form">'
 '<form onsubmit="return false" style="display:grid;gap:12px">'
 '<input class="uk-input" type="text" placeholder="Full Name*" style="background:#fff">'
 '<input class="uk-input" type="email" placeholder="Email Address*" style="background:#fff">'
 '<input class="uk-input" type="tel" placeholder="Phone Number*" style="background:#fff">'
 '<textarea class="uk-textarea" rows="4" placeholder="How Can We Help?*" style="background:#fff"></textarea>'
 '<button class="uk-button uk-button-primary uk-button-large" type="submit">Send Message</button>'
 '<p style="font-size:11px;opacity:.7;margin:0">Demo form — live client sites use a GoHighLevel form embed.</p>'
 '</form></div>')
html = re.sub(r'<div class="ghl-embed ghl-embed--form">.*?</iframe>\s*</div>', DEMO_FORM, html, flags=D)

# expand the single review REPEAT card into 8 sample cards so the slider looks populated
sample = [("Sarah M.","2 days ago","On time, professional, and fixed our AC fast. Couldn't be happier."),
          ("David R.","3 days ago","Technician explained everything clearly and the price was fair."),
          ("Lena P.","4 days ago","Best HVAC experience in LA. Clean, courteous, and efficient."),
          ("Marcus T.","5 days ago","Same-day service on a 100° day. Lifesavers!"),
          ("Priya K.","6 days ago","Installed a new system in one day. Works perfectly."),
          ("Tom B.","1 week ago","Honest assessment, no upsell. Will use again."),
          ("Grace L.","1 week ago","Friendly team, great communication start to finish."),
          ("Andre W.","2 weeks ago","Quiet, fast, and tidy. Five stars all the way.")]
m = re.search(r'<!-- BEGIN REPEAT: review.*?-->(.*?)<!-- END REPEAT: review -->', html, D)
card_tpl = m.group(1)
cards = ""
for name, time, text in sample:
    c = card_tpl
    c = c.replace("{{REVIEW_PROVIDER}}","google").replace("{{REVIEW_RATING}}","5")
    c = c.replace("{{REVIEWS_PROFILE_URL}}", V["REVIEWS_PROFILE_URL"])
    c = c.replace("{{REVIEW_AUTHOR}}",name).replace("{{REVIEW_TIME}}",time).replace("{{REVIEW_TEXT}}",text)
    cards += c
html = html.replace(m.group(0), cards)

for k, val in V.items():
    html = html.replace("{{%s}}" % k, val)

left = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', html)))
if left: print("unfilled:", left)
open(os.path.join(HERE, "demo.html"), "w", encoding="utf-8").write(html)
print("wrote demo.html (%d bytes)" % len(html))
