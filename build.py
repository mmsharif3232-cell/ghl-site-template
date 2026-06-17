#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transforms the saved brodypennell.com homepage ("Save Page As -> Complete")
into a standalone, WordPress-free, templated GHL site clone:

  * strips every <script>/<noscript>, all WordPress/Gravity/CleanTalk/analytics/Avoca code
  * keeps the EXACT YOOtheme/UIkit DOM + the real theme CSS  -> pixel-identical look
  * rewrites assets to local copies (assets/) or absolute brand URLs
  * swaps the 3 integrations for GHL embeds: contact form, chat widget, calendar booking
  * replaces every client-specific string with {{DOUBLE_BRACKET}} template variables
  * marks variable-length lists with <!-- BEGIN/END REPEAT --> blocks

Input : ~/Downloads/Brody Pennell ... .html   (the saved page)
Output: ./index.html
"""
import re, os, html

SRC = os.path.expanduser(
    "~/Downloads/Brody Pennell Heating & Air Conditioning in Los Angeles, CA..html")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

doc = open(SRC, encoding="utf-8", errors="replace").read()
SAVED = "Brody Pennell Heating &amp; Air Conditioning in Los Angeles, CA._files"

def sub(pattern, repl, flags=0, count=0, required=True, label=""):
    global doc
    # repl may be a string (backrefs like \1 expand) or a callable — re.subn handles both
    new, n = re.subn(pattern, repl, doc, count=count, flags=flags)
    if required and n == 0:
        print(f"  !! NO MATCH: {label or pattern[:60]}")
    elif n:
        print(f"  ok ({n}) {label or pattern[:50]}")
    doc = new

def rep(old, new, required=True):
    global doc
    n = doc.count(old)
    if required and n == 0:
        print(f"  !! NO STR : {old[:60]!r}")
    doc = doc.replace(old, new)
    if n:
        print(f"  ok ({n}) str {old[:46]!r}")

D = re.DOTALL

# ---------------------------------------------------------------- 1. strip JS
print("\n[1] strip scripts / noscripts")
sub(r"<script\b[^>]*>.*?</script>", "", D, required=False, label="scripts")
sub(r"<noscript\b[^>]*>.*?</noscript>", "", D, required=False, label="noscripts")
# leftover GTM html comments
sub(r"<!-- (?:End )?Google Tag Manager[^>]*-->", "", required=False, label="gtm comments")
sub(r"<!-- start new avoca script -->", "", required=False, label="avoca comment")

# --------------------------------------------------- 2. integration swaps
print("\n[2] swap integrations -> GHL")

# 2a. Gravity contact form  ->  GHL form embed
GHL_FORM = (
    '<div class="ghl-embed ghl-embed--form">\n'
    '  <iframe src="https://api.leadconnectorhq.com/widget/form/{{GHL_CONTACT_FORM_ID}}"\n'
    '          id="ghl-contact-form" title="Request Service" scrolling="no"\n'
    '          style="width:100%;height:640px;border:none;border-radius:6px;background:transparent"></iframe>\n'
    '</div>'
)
sub(r'<div class="gf_browser_chrome gform_wrapper.*?</form>\s*</div>',
    GHL_FORM, D, label="gravity form -> GHL form")

# 2b. Google My Maps service-area iframe  ->  templated map embed
sub(r'<iframe src="\./' + re.escape(SAVED) + r'/embed\.html"[^>]*></iframe>',
    '<iframe src="{{SERVICE_AREA_MAP_EMBED_URL}}" width="100%" height="700" '
    'style="border:0" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
    'title="Service Area Map"></iframe>',
    D, label="my-maps iframe -> templated map")

# 2c. scheduler triggers -> GHL calendar modal opener
rep('onclick="SimpleScheduler.open()"', 'onclick="openGhlCalendar();return false;"')

# 2d. remove leftover runtime DOM (a11y live-regions, empty flash-reviews popup,
#     Avoca chat widget, tracking beacons); scheduler modal handled in injection step
sub(r'<p id="a11y-speak-intro-text"[^>]*>.*?</p>', "", D, required=False, label="a11y intro")
sub(r'<div id="a11y-speak-(?:assertive|polite)"[^>]*></div>', "", required=False, label="a11y regions")
sub(r'<div class="rpi" style="" data-id="47830".*?<div class="rpi-x"></div></div></div></div></div>',
    "", D, required=False, label="empty flash-reviews popup")
sub(r'<div id="chat-widget">.*?(?=<div id="batBeacon)', "", D, required=False, label="avoca chat widget")
sub(r'<div id="batBeacon\d+"[^>]*>.*?</div>', "", D, required=False, label="bat beacon")

# ------------------------------------------------- 3. reviews slider -> REPEAT
print("\n[3] reviews slider -> templated REPEAT cards")
REVIEW_CARDS = (
    '<div class="rpi-cards rpi-slides-bite">\n'
    '<!-- BEGIN REPEAT: review (clone one .rpi-card per Google/Facebook review) -->\n'
    '<div class="rpi-card" data-provider="{{REVIEW_PROVIDER}}" data-rat="{{REVIEW_RATING}}">\n'
    '<div class="rpi-card-inner rpi-logo rpi-logo-{{REVIEW_PROVIDER}}">\n'
    '<div class="rpi-flex">\n'
    '<div class="rpi-info">\n'
    '<a href="{{REVIEWS_PROFILE_URL}}" class="rpi-name" target="_blank" rel="noopener nofollow">{{REVIEW_AUTHOR}}</a>\n'
    '<div class="rpi-time">{{REVIEW_TIME}}</div>\n'
    '<span class="rpi-stars" style="--rating:{{REVIEW_RATING}}"></span></div></div>\n'
    '<div class="rpi-body rpi-normal-up__body">\n'
    '<div class="rpi-text rpi-scroll" tabindex="0">{{REVIEW_TEXT}}</div></div></div></div>\n'
    '<!-- END REPEAT: review -->\n'
    '</div>'
)
sub(r'<div class="rpi-cards rpi-slides-bite"[^>]*>.*?(?=<button class="rpi-ltgt rpi-gt rpi-slider-next")',
    REVIEW_CARDS + "\n", D, label="43 review cards -> REPEAT")

# ----------------------------------- 4. headings / eyebrows / prose -> vars
print("\n[4] templatize headings & body copy")

# YOOtheme builder elements carry stable ids (page#N) -> replace inner text
def inner(idv, tag, var):
    sub(r'(id="page#' + re.escape(idv) + r'">)\s*.*?(\s*</' + tag + r'>)',
        lambda m: m.group(1) + var + m.group(2), D, label=f"page#{idv} -> {var}")

inner("0",  "h1", "{{HERO_HEADLINE}}")
inner("1",  "h2", "{{HERO_SUBHEADLINE}}")
inner("4",  "div", "{{SERVICES_EYEBROW}}")
inner("5",  "h2", "{{SERVICES_HEADING}}")
inner("14", "h2", "{{REVIEWS_EYEBROW}}")
inner("15", "h3", "{{REVIEWS_HEADING}}")
inner("22", "h2", "{{BLOG_EYEBROW}}")
inner("23", "h3", "{{BLOG_HEADING}}")

# id'd panels whose inner is a single <p>
sub(r'(id="page#6">)<p>.*?</p>', lambda m: m.group(1) + "<p>{{SERVICES_INTRO}}</p>", D, label="services intro")
sub(r'(id="page#16">)<p>.*?</p>', lambda m: m.group(1) + "<p>{{REVIEWS_SUBTEXT}}</p>", D, label="reviews subtext")

# headings without ids
rep("Heating and Air Conditioning in Los Angeles and Surrounding Areas", "{{INTRO_HEADING}}")
sub(r'Fixing Air Conditioners &amp; Heaters in Los Angeles for\s*<span>\d+</span>\s*Years',
    "{{ABOUT_HEADING}}", D, label="about heading (NN years)")
rep("Areas We Serve", "{{AREAS_EYEBROW}}")
rep("Serving Greater Los Angeles And The Surrounding Areas", "{{AREAS_HEADING}}")
rep("We Are Here For You", "{{SCHEDULE_EYEBROW}}")
rep("Schedule Your Service Today", "{{SCHEDULE_HEADING}}")
rep("Expert HVAC Tips For Homeowners", "{{BLOG_HEADING}}", required=False)  # also set via page#23

# prose paragraphs (match leading ASCII, swallow to </p> or </span>)
def para(prefix, var, closer="p"):
    sub(r'<' + closer + r'([^>]*)>' + prefix + r'.*?</' + closer + r'>',
        lambda m: f'<{closer}{m.group(1)}>{var}</{closer}>', D, label=var)

para(r'Though we are one of the longest-running', "{{INTRO_PARAGRAPH_1}}")
para(r'Opening our doors in 1945', "{{INTRO_PARAGRAPH_2}}")
para(r'With 80 years of experience', "{{INTRO_PARAGRAPH_3}}")
para(r'We[^<]*here for you 24/7', "{{INTRO_CONTACT_NOTE}}")
para(r'Ready to get a new air conditioner', "{{ABOUT_PARAGRAPH_1}}")
para(r'A new AC is a big investment', "{{ABOUT_PARAGRAPH_2}}")
para(r'We have a reputation', "{{ABOUT_PARAGRAPH_3}}")
sub(r'<p><strong>We aren[^<]*comfortable until you are!</strong>.*?</p>',
    "<p>{{SCHEDULE_INTRO}}</p>", D, label="{{SCHEDULE_INTRO}}")
sub(r'<span>Since 1945, Brody Pennell.*?</span>',
    "<span>{{FOOTER_ABOUT}}</span>", D, label="{{FOOTER_ABOUT}}")

# ------------------------------------------------ 5. list REPEAT markers
print("\n[5] mark variable-length lists as REPEAT blocks")
# service-area city list
sub(r'(<ul class="uk-list uk-column-1-3@m">)',
    r'\1\n<!-- BEGIN REPEAT: service_area_city (clone one <li class="el-item"> per city) -->',
    label="cities REPEAT begin")
sub(r'(</ul>\s*<div class="uk-margin">\s*<a class="el-content uk-button uk-button-primary uk-button-large" href="[^"]*cities-served)',
    r'<!-- END REPEAT: service_area_city -->\1', D, required=False, label="cities REPEAT end")

# ------------------------------------------------ 5b. asset paths (BEFORE name swap,
#     since the saved _files/ folder name literally contains the business name)
print("\n[5b] asset paths")
rep('./' + SAVED + '/', 'assets/')
rep(SAVED + '/', 'assets/', required=False)
sub(r'(["\'(\s])/wp-content/', r'\1https://brodypennell.com/wp-content/', label="/wp-content abs")
sub(r'\\/wp-content\\/', r'https:\\/\\/brodypennell.com\\/wp-content\\/', required=False, label="json wp-content")

def add_bg(m):
    tag = m.group(0)
    if "background-image" in tag:
        return tag
    ds = re.search(r'data-src="([^"]+)"', tag)
    if not ds:
        return tag
    url = ds.group(1)
    if 'style="' in tag:
        return tag.replace('style="', f'style="background-image:url(&quot;{url}&quot;);', 1)
    return tag[:-1] + f' style="background-image:url(&quot;{url}&quot;)">'
doc = re.sub(r'<div\b[^>]*\buk-img=""[^>]*>', add_bg, doc)
print("  ok inline bg fallback injected")

# ------------------------------------------------ 6. global client strings
print("\n[6] global client strings -> vars")
# business name (long first, then short)
rep("Brody Pennell Heating &amp; Air Conditioning", "{{BUSINESS_NAME}}")
rep("Brody Pennell Heating & Air Conditioning", "{{BUSINESS_NAME}}", required=False)
rep("Brody Pennell", "{{BUSINESS_SHORT_NAME}}")

# phones (display variants + tel:)
rep("tel:4243263045", "tel:{{PHONE}}")
rep("(424) 326-3045", "{{PHONE_DISPLAY}}")
rep("424-326-3045", "{{PHONE_DISPLAY}}")
rep("tel:424-455-0173", "tel:{{PHONE}}")
rep("424-455-0173", "{{PHONE_DISPLAY}}")

# NAP / footer
rep("8599 Venice Blvd., Los Angeles, CA 90034", "{{ADDRESS}}")
rep("https://maps.app.goo.gl/5bi9bmXTSVHsP9HC8", "{{DIRECTIONS_URL}}")
rep("CA LIC# 256821", "{{LICENSE}}")
sub(r'Mon[^<]*Fri:[^<]*<br>Sat:[^<]*<br>Sun: CLOSED', "{{OFFICE_HOURS}}", label="office hours")
rep("© 2026", "© {{YEAR}}")

# social profiles
rep("https://www.facebook.com/BrodyPennell", "{{SOCIAL_FACEBOOK}}")
rep("https://www.instagram.com/brodypennell/", "{{SOCIAL_INSTAGRAM}}")
rep("https://www.youtube.com/c/BrodyPennellLosAngeles", "{{SOCIAL_YOUTUBE}}")
rep("https://www.linkedin.com/company/brody-pennell-hvac/", "{{SOCIAL_LINKEDIN}}")

# ------------------------------------------------ 7. head meta + favicons + og
print("\n[7] head meta / og / favicon")
sub(r'<title>.*?</title>', "<title>{{SEO_TITLE}}</title>", D, label="title")
sub(r'(<meta name="description" content=").*?(">)', lambda m: m.group(1) + "{{SEO_DESCRIPTION}}" + m.group(2), label="description")
sub(r'(<meta property="og:title" content=").*?(">)', lambda m: m.group(1) + "{{SEO_TITLE}}" + m.group(2), label="og:title")
sub(r'(<meta property="og:description" content=").*?(">)', lambda m: m.group(1) + "{{SEO_DESCRIPTION}}" + m.group(2), label="og:description")
sub(r'(<meta property="og:url" content=").*?(">)', lambda m: m.group(1) + "{{SITE_URL}}/" + m.group(2), label="og:url")
sub(r'(<meta property="og:image(?::secure_url)?" content=").*?(">)', lambda m: m.group(1) + "{{OG_IMAGE_URL}}" + m.group(2), required=False, label="og:image")
sub(r'<link rel="icon" href="[^"]*\.png"[^>]*>', '<link rel="icon" href="{{FAVICON_URL}}" sizes="any">', required=False, label="favicon png")
sub(r'<link rel="icon" href="[^"]*\.svg"[^>]*>', '<link rel="icon" href="{{FAVICON_SVG_URL}}" type="image/svg+xml">', required=False, label="favicon svg")
sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="{{OG_IMAGE_URL}}">', required=False, label="twitter:image")
# strip dead WordPress head discovery / SEO cruft (no WP backend behind it anymore)
for pat in (r'<link rel="alternate"[^>]*oembed[^>]*>',
            r'<link rel="alternate"[^>]*type="application/rss\+xml"[^>]*>',
            r'<link rel="alternate"[^>]*type="application/json"[^>]*>',
            r'<link rel="https://api\.w\.org/"[^>]*>',
            r'<link rel="EditURI"[^>]*>',
            r'<link rel="(?:shortlink|wlwmanifest|pingback)"[^>]*>',
            r'<meta name="generator"[^>]*>',
            r'<style id="wp-emoji-styles-inline-css">.*?</style>\s*',):
    sub(pat, "", D, required=False, label="drop " + pat[:34])

# ------------------------------------------------ 8. anchor domain -> SITE_URL
print("\n[8] internal links -> {{SITE_URL}}")
rep('href="https://brodypennell.com', 'href="{{SITE_URL}}')
rep("href='https://brodypennell.com", "href='{{SITE_URL}}", required=False)

# ------------------------------------------------ 10. <head> stylesheet swap
print("\n[10] stylesheet links")
for sid in ("cleantalk-public-css", "cleantalk-email-decoder-css", "brb-public-main-css",
            "gravity_forms_theme_reset", "gravity_forms_theme_foundation",
            "gravity_forms_theme_framework", "gravity_forms_orbital_theme"):
    sub(r'<link rel="stylesheet" id="' + re.escape(sid) + r'[^>]*>', "", required=False, label=f"drop {sid}")
# theme.1.css -> local styles.css  (+ keep Typekit fonts, which were JS-loaded)
sub(r'<link href="assets/theme\.1\.css" rel="stylesheet">',
    '<link rel="stylesheet" href="https://use.typekit.net/qdb2hku.css">\n'
    '<link rel="stylesheet" href="styles.css">',
    label="theme.1.css -> styles.css + typekit")

# ------------------------------------------------ 11. inject GHL runtime + UIkit
print("\n[11] inject GHL runtime + UIkit before </body>")
INJECT = """
<!-- ===== GHL Calendar Booking (opened by every Request Service / Book Online button) ===== -->
<div id="ghl-calendar-modal" class="ghl-modal" role="dialog" aria-modal="true" aria-label="Book an appointment">
  <div class="ghl-modal__box">
    <button type="button" class="ghl-modal__close" aria-label="Close" onclick="closeGhlCalendar()">&times;</button>
    <iframe src="https://api.leadconnectorhq.com/widget/booking/{{GHL_CALENDAR_ID}}"
            title="Book an Appointment" scrolling="no" id="ghl-calendar-iframe"
            style="width:100%;height:80vh;border:none;border-radius:10px;background:#fff"></iframe>
  </div>
</div>

<!-- GHL embed scripts -->
<script src="https://link.msgsndr.com/js/form_embed.js"></script>

<!-- GHL Chat Widget (replaces the site chat bubble) -->
<script src="https://widgets.leadconnectorhq.com/loader.js"
        data-resources-url="https://widgets.leadconnectorhq.com/chat-widget/loader.js"
        data-widget-id="{{GHL_CHAT_WIDGET_ID}}"></script>

<!-- UIkit runtime (sticky header, mobile menu, dropdowns, lazy backgrounds, grid) -->
<script src="assets/uikit.min.js"></script>
<script src="assets/uikit-icons.min.js"></script>
<script>
  function openGhlCalendar(){var m=document.getElementById('ghl-calendar-modal');if(m){m.classList.add('is-open');document.body.style.overflow='hidden';}}
  function closeGhlCalendar(){var m=document.getElementById('ghl-calendar-modal');if(m){m.classList.remove('is-open');document.body.style.overflow='';}}
  document.addEventListener('click',function(e){if(e.target&&e.target.id==='ghl-calendar-modal')closeGhlCalendar();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')closeGhlCalendar();});
</script>
</body>"""
sub(r'<div id="simple-scheduler-modal".*?</body>', INJECT, D, label="scheduler modal -> GHL inject")

# ------------------------------------------------ done
open(OUT, "w", encoding="utf-8").write(doc)
toks = sorted(set(re.findall(r'\{\{[A-Z0-9_]+\}\}', doc)))
print(f"\nWROTE {OUT}  ({len(doc):,} bytes)")
print(f"{len(toks)} unique template variables:")
print("  " + ", ".join(toks))
for leak in ("brodypennell.com", "Brody Pennell", "gform", "avoca", "SimpleScheduler", "424"):
    c = doc.count(leak)
    if c:
        print(f"  leak? {leak!r} x{c}")
