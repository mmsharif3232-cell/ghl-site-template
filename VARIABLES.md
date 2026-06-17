# Template Variables — Intake Checklist

Everything Noor collects **before generating a client site** from this template.

This site is a 1:1 visual clone of the reference HVAC homepage, rebuilt as standalone
HTML/CSS with **no WordPress, no Gravity Forms, no chat/scheduler plugins, no analytics**.
Every client-specific string is a `{{DOUBLE_BRACKET}}` token. Fill all 54 tokens, clone the
`REPEAT` blocks to the right counts, drop in the 3 GoHighLevel IDs, and ship.

## Files

| File | What it is | Edit? |
|------|------------|-------|
| `index.html` | The page. Contains all `{{TOKENS}}` + `REPEAT` blocks. | Fill tokens |
| `styles.css` | The exact theme stylesheet (YOOtheme/UIkit). Drives the look. | Don't touch |
| `assets/` | Logos, icons, badges, photos + `uikit.min.js` runtime. | Swap per client |
| `VARIABLES.md` | This checklist. | — |
| `build.py` / `fill_preview.py` | Tooling that produced `index.html` / a filled demo. | Optional |
| `_preview.html` | A fully-filled example render (reference only — not shipped). | — |

> **Find-and-replace** each `{{TOKEN}}` with the client value. Tokens appear verbatim in
> `index.html`; nothing else needs editing for a basic launch.

---

## A. Business identity (2)

| Token | What | Example |
|-------|------|---------|
| `{{BUSINESS_NAME}}` | Full legal/brand name (used in alt text, ©, schema) | `Brody Pennell Heating & Air Conditioning` |
| `{{BUSINESS_SHORT_NAME}}` | Short name | `Brody Pennell` |

## B. Contact / NAP (5)

| Token | What | Example |
|-------|------|---------|
| `{{PHONE}}` | Phone, **digits only** (used in `tel:` links) | `4243263045` |
| `{{PHONE_DISPLAY}}` | Phone as shown to humans | `(424) 326-3045` |
| `{{ADDRESS}}` | Street address line | `8599 Venice Blvd., Los Angeles, CA 90034` |
| `{{DIRECTIONS_URL}}` | "Get Directions" link (Google Maps share URL) | `https://maps.app.goo.gl/…` |
| `{{LICENSE}}` | License line shown in footer | `CA LIC# 256821` |
| `{{OFFICE_HOURS}}` | Hours block — keep the `<br>` line breaks | `Mon – Fri: 7:00am – 5:00pm<br>Sat: 8:00am − 1:00pm<br>Sun: CLOSED` |

> Note: the source site used a separate call-tracking number in the header and an office
> number in the footer. This template unifies both to `{{PHONE}}`. If you need two numbers,
> search `tel:{{PHONE}}` in the footer and swap it for a second token.

## C. SEO & social meta (5)

| Token | What | Example |
|-------|------|---------|
| `{{SEO_TITLE}}` | `<title>` + OG title | `Brody Pennell Heating & Air Conditioning in Los Angeles, CA.` |
| `{{SEO_DESCRIPTION}}` | Meta description + OG description | `Locally rated HVAC company in LA…` |
| `{{SITE_URL}}` | Canonical site root, **no trailing slash** (rewrites every internal link) | `https://brodypennell.com` |
| `{{OG_IMAGE_URL}}` | Social-share image (1200×630) | `https://…/share-image.jpg` |
| `{{YEAR}}` | Copyright year | `2026` |

## D. GoHighLevel embeds (3) — **required**

| Token | What | Where to get it |
|-------|------|------|
| `{{GHL_CONTACT_FORM_ID}}` | Contact/"Request Service" form | GHL → Sites → Forms → Embed → the ID in `…/widget/form/<ID>` |
| `{{GHL_CALENDAR_ID}}` | Booking calendar (opens from every "Request Service"/"Book Online" button) | GHL → Calendars → Embed → the ID in `…/widget/booking/<ID>` |
| `{{GHL_CHAT_WIDGET_ID}}` | Chat widget bubble | GHL → Sites → Chat Widget → Install code → `data-widget-id` |

Embeds are already wired in `index.html`:
- Form → `<iframe src="https://api.leadconnectorhq.com/widget/form/{{GHL_CONTACT_FORM_ID}}">`
- Calendar → modal `<iframe src="https://api.leadconnectorhq.com/widget/booking/{{GHL_CALENDAR_ID}}">` (opened by `openGhlCalendar()`)
- Chat → `<script src="https://widgets.leadconnectorhq.com/loader.js" data-widget-id="{{GHL_CHAT_WIDGET_ID}}">`
- `https://link.msgsndr.com/js/form_embed.js` is included once and powers both form + calendar.

## E. Hero (2)

| Token | What | Example |
|-------|------|---------|
| `{{HERO_HEADLINE}}` | Big H1 (you may include a `<br>`) | `Proudly Serving <br>Los Angeles Since 1945` |
| `{{HERO_SUBHEADLINE}}` | Sub-headline under H1 | `Los Angeles' Premier Heating & Air Conditioning Company` |

Hero CTA buttons (Book Online, Instant Quote, Buy Filters, Duct Cleaning, Call) are literal
in `index.html` — edit labels/links there if the client's offers differ.

## F. Intro band + "About" copy (8)

| Token | What |
|-------|------|
| `{{INTRO_HEADING}}` | Heading beside the contact form (`Heating and Air Conditioning in …`) |
| `{{INTRO_PARAGRAPH_1}}` … `{{INTRO_PARAGRAPH_3}}` | Three intro paragraphs (HTML allowed) |
| `{{INTRO_CONTACT_NOTE}}` | The "24/7… contact us" note card |
| `{{ABOUT_HEADING}}` | About heading (`Fixing Air Conditioners & Heaters in … for 80 Years`) |
| `{{ABOUT_PARAGRAPH_1}}` … `{{ABOUT_PARAGRAPH_3}}` | Three about paragraphs (HTML allowed) |

## G. Services section (3)

| Token | What | Example |
|-------|------|---------|
| `{{SERVICES_EYEBROW}}` | Small label | `Our Services` |
| `{{SERVICES_HEADING}}` | Section H2 | `Los Angeles Heating & Air Conditioning` |
| `{{SERVICES_INTRO}}` | Intro paragraph (HTML allowed) | — |

The two service cards (Air Conditioning / Heating) and their sub-tiles (AC Repair, AC
Replacement, …) are literal HTML in `index.html` — edit names/links/icons there.

## H. Reviews (REPEAT) (8)

| Token | What | Example |
|-------|------|---------|
| `{{REVIEWS_EYEBROW}}` | Small label | `Ratings & Reviews` |
| `{{REVIEWS_HEADING}}` | Section heading | `Check Out Our 5-Star Reviews!` |
| `{{REVIEWS_SUBTEXT}}` | Sub-line under heading | `Highly rated for: …` |
| `{{REVIEWS_PROFILE_URL}}` | Link applied to every reviewer name | Google reviews URL |
| `{{REVIEW_PROVIDER}}` | `google` / `facebook` / `yelp` (sets the logo) | per card |
| `{{REVIEW_RATING}}` | `1`–`5` | per card |
| `{{REVIEW_AUTHOR}}` | Reviewer name | per card |
| `{{REVIEW_TIME}}` | Relative time | per card |
| `{{REVIEW_TEXT}}` | Review body | per card |

→ Inside `<!-- BEGIN REPEAT: review -->…<!-- END REPEAT: review -->`: **duplicate the
`.rpi-card` block once per review** and fill the 5 per-card tokens each time.

## I. Service areas (REPEAT) (3)

| Token | What | Example |
|-------|------|---------|
| `{{AREAS_EYEBROW}}` | Small label | `Areas We Serve` |
| `{{AREAS_HEADING}}` | Section heading | `Serving Greater Los Angeles And The Surrounding Areas` |
| `{{SERVICE_AREA_MAP_EMBED_URL}}` | Map iframe src (Google My Maps embed URL) | `https://www.google.com/maps/d/embed?mid=…` |

→ The city list is inside `<!-- BEGIN REPEAT: service_area_city -->…<!-- END REPEAT -->`.
**Clone one `<li class="el-item">` per city** and set its name + link.

## J. Blog (2)

| Token | What | Example |
|-------|------|---------|
| `{{BLOG_EYEBROW}}` | Small label | `The Blog` |
| `{{BLOG_HEADING}}` | Section heading | `Expert HVAC Tips For Homeowners` |

The two post cards are literal HTML — edit titles/dates/links in `index.html`, or wire them
to a feed later.

## K. Schedule band (3)

| Token | What | Example |
|-------|------|---------|
| `{{SCHEDULE_EYEBROW}}` | Small label | `We Are Here For You` |
| `{{SCHEDULE_HEADING}}` | Heading | `Schedule Your Service Today` |
| `{{SCHEDULE_INTRO}}` | Intro line (HTML allowed) | `We aren't comfortable until you are! …` |

## L. Footer (1) + M. Social (4)

| Token | What | Example |
|-------|------|---------|
| `{{FOOTER_ABOUT}}` | Footer blurb under the logo | `Since 1945, … award-winning HVAC service.` |
| `{{SOCIAL_FACEBOOK}}` | Facebook URL | `https://www.facebook.com/…` |
| `{{SOCIAL_INSTAGRAM}}` | Instagram URL | `https://www.instagram.com/…` |
| `{{SOCIAL_YOUTUBE}}` | YouTube URL | `https://www.youtube.com/…` |
| `{{SOCIAL_LINKEDIN}}` | LinkedIn URL | `https://www.linkedin.com/company/…` |

Footer "Helpful Links" + "Our Services" link columns are literal HTML — edit per client.

## N. Favicons (2) + images

| Token | What |
|-------|------|
| `{{FAVICON_URL}}` | PNG favicon URL |
| `{{FAVICON_SVG_URL}}` | SVG favicon URL |

**Images:** the layout ships with the reference brand's images so it renders identically out
of the box. Logos/icons/badges/photos live in `assets/` (referenced as `assets/<file>`);
section background photos load from the reference host (`https://brodypennell.com/wp-content/…`).
For a client, replace the files in `assets/` with same-named client files (or change the
`src`/`srcset`/`background-image` URLs), and update the four reviews/badge images
(`Reviews.svg`, `Reviews-1.svg`, `Reviews-2.svg`, the BBB/NATE/award badges) to the client's.

---

## Generation workflow

1. Copy this folder to the new client.
2. Find-and-replace all 54 `{{TOKENS}}` with client values.
3. Expand the two `REPEAT` blocks (reviews, cities) to the right counts.
4. Paste the 3 GHL IDs (Section D).
5. Swap `assets/` images for the client's brand assets.
6. Edit the literal lists (nav, hero CTAs, service cards/tiles, blog cards, footer link
   columns) to match the client's services.
7. Open `index.html` in a browser to confirm, then deploy (any static host).

**Token count: 54.** Variable-length REPEAT blocks: `review`, `service_area_city`.
