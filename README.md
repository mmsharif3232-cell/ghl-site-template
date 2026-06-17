# GHL Local-Services Site Template

A reusable, **WordPress-free** website template for local home-services businesses
(HVAC, plumbing, electrical, roofing, etc.), wired for **GoHighLevel (GHL)**.

It is a **pixel-exact rebuild** of a real, high-converting HVAC site — same layout, fonts,
colors, spacing, and motion — rebuilt as a **22-page static website** with the original's
form / chat / scheduler swapped for GHL embeds, and the homepage also provided as a fully
`{{VARIABLE}}`-tokenized template.

> **Live demo:** https://ghl-site-template.vercel.app
> **Repo:** https://github.com/mmsharif3232-cell/ghl-site-template
> **One template → many clients.** Clone the client's pages, swap content + images, paste 3
> GHL IDs, deploy.

---

## 1. What this is (and isn't)

- ✅ A static **`index.html` + `styles.css` + `assets/`** bundle. Opens in any browser, hosts
  anywhere (Vercel, Netlify, S3, GHL funnels, plain nginx).
- ✅ **No WordPress, no PHP, no Gravity Forms, no plugins, no analytics/tracking.** All of
  that was stripped. What remains is HTML, the real theme CSS, and the UIkit JS runtime.
- ✅ **GHL-native:** contact form, chat widget, and calendar booking are GoHighLevel embeds
  driven by 3 IDs.
- ❌ Not a CMS. There's no admin panel — you edit the HTML (or run it through our generator)
  to produce each client site.
- ❌ Not "themeable" by config alone — the **look is fixed** (that's the point: it's a proven
  design). You change *content and brand assets*, not the layout.

---

## 2. How it's structured

| File / folder | What it is | Do you edit it? |
|---|---|---|
| **`index.html` + 21 sibling pages** | The **live 22-page website** (home, services, about, contact, etc.). Real content, interlinked, deploy-ready. | **Yes** — edit content per client |
| **`template.html`** | The homepage as a fully `{{TOKEN}}`-ized template (54 variables + `REPEAT` blocks). The reusable starting point. | **Yes** — fill tokens |
| **`styles.css`** | The real compiled theme stylesheet (YOOtheme/UIkit). **This is what makes it look identical.** | **No** — leave it alone |
| **`assets/`** | Logos, badges, icons, photos (70 files) + `uikit.min.js` (the JS runtime). | **Yes** — swap brand images |
| **`VARIABLES.md`** | The full intake checklist: all 54 homepage tokens grouped, with examples. **Start here for a new client.** | Reference |
| `build.py` / `fill_preview.py` | How `template.html` was generated from a saved homepage + how it's filled. | Maintainers |
| `build_site.py` | How the 22-page site is assembled from the saved page exports (see §6). | Maintainers |

Root `/` serves `index.html` (the homepage). No `vercel.json` needed — it's a plain static site.

---

## 3. The 22 pages

All pages share the **same header, footer, navigation, fonts, colors, and CSS** — change the
chrome once and it updates everywhere (it's assembled from one shared frame).

**Cloned 1:1 from the real site (7):**
`index.html` (home) · `about.html` · `contact.html` · `reviews.html` · `cities.html` ·
`air-conditioning.html` (service category) · `ac-repair.html` (service detail)

**Generated from the two service templates (15)** — identical layout, correct service names:
- *Categories* (from `air-conditioning.html`): `heating.html`, `indoor-air-quality.html`
- *Details* (from `ac-repair.html`): `ac-maintenance.html`, `ac-replacement.html`,
  `ductless-mini-splits.html`, `thermostat-repair.html`, `heater-repair.html`,
  `heater-installation.html`, `heater-maintenance.html`, `heat-pumps.html`,
  `heat-pump-repair.html`, `furnaces.html`, `furnace-repair.html`,
  `furnace-installation.html`, `duct-cleaning.html`

> The generated service pages reuse the AC pages' layout with the service name swapped in
> headings/titles. Some body copy still reflects the AC source — **replace generated-page body
> copy with the client's real service copy before launch** (the layout is final; the words are
> placeholders). To clone a generated page exactly instead, save that real page and add it to
> the `SAVED` list in `build_site.py`.

**Add / edit / remove pages:** edit the page's `.html` directly, or re-run `build_site.py`
(§6). To add a new page type, save its export and register it in `build_site.py`.

## 4. What's interchangeable (the important part)

Everything a client sees is changeable. There are **four levels**, easiest → most hands-on:

### Level 1 — Variables (`{{TOKENS}}`) — find & replace
54 tokens cover the bulk of the content. Full list + examples in **`VARIABLES.md`**. Highlights:

| Category | Tokens |
|---|---|
| **Identity** | `{{BUSINESS_NAME}}`, `{{BUSINESS_SHORT_NAME}}` |
| **Contact / NAP** | `{{PHONE}}`, `{{PHONE_DISPLAY}}`, `{{EMAIL}}`, `{{ADDRESS}}`, `{{DIRECTIONS_URL}}`, `{{LICENSE}}`, `{{OFFICE_HOURS}}` |
| **Location & tenure** | `{{CITY}}` (used site-wide), `{{YEAR_FOUNDED}}`, `{{YEARS_IN_BUSINESS}}`, `{{MANUFACTURER_BADGE_URL}}` |
| **SEO / social meta** | `{{SEO_TITLE}}`, `{{SEO_DESCRIPTION}}`, `{{SITE_URL}}`, `{{OG_IMAGE_URL}}`, `{{YEAR}}` |
| **Hero** | `{{HERO_HEADLINE}}`, `{{HERO_SUBHEADLINE}}` |
| **Body copy** | intro band + about (`{{INTRO_*}}`, `{{ABOUT_*}}`), services (`{{SERVICES_*}}`), reviews (`{{REVIEWS_*}}`), areas (`{{AREAS_*}}`), blog (`{{BLOG_*}}`), schedule (`{{SCHEDULE_*}}`), footer (`{{FOOTER_ABOUT}}`) |
| **Social links** | `{{SOCIAL_FACEBOOK}}`, `{{SOCIAL_INSTAGRAM}}`, `{{SOCIAL_YOUTUBE}}`, `{{SOCIAL_LINKEDIN}}` |
| **GHL embeds** | `{{GHL_CONTACT_FORM_ID}}`, `{{GHL_CALENDAR_ID}}`, `{{GHL_CHAT_WIDGET_ID}}` |
| **Favicons** | `{{FAVICON_URL}}`, `{{FAVICON_SVG_URL}}` |
| **Internal links** | `{{SITE_URL}}` rewrites every nav/footer link to the client domain at once |

### Level 2 — Repeating lists (`REPEAT` blocks) — clone the block
Two lists vary in length. Each is wrapped in `<!-- BEGIN REPEAT: name -->…<!-- END REPEAT: name -->`.
Duplicate the inner block once per item:
- **`review`** — one card per Google/Facebook/Yelp review (`{{REVIEW_AUTHOR}}`, `{{REVIEW_TEXT}}`, `{{REVIEW_RATING}}`, `{{REVIEW_TIME}}`, `{{REVIEW_PROVIDER}}`).
- **`service_area_city`** — one `<li>` per city (name + link).

### Level 3 — Literal lists — edit the HTML directly
These are real HTML (not tokenized) because they're structural and vary a lot by client.
Edit them in `index.html`:
- **Top navigation** (menu items + dropdowns)
- **Hero CTA buttons** (Book Online / Instant Quote / Buy Filters / Duct Cleaning / Call)
- **Service cards & sub-tiles** (Air Conditioning / Heating + the AC Repair, Heater Repair… tiles)
- **Blog post cards** (title, date, link, image)
- **Footer link columns** (Helpful Links, Our Services)

### Level 4 — Brand assets — swap the files
The layout ships with the reference brand's images so it renders perfectly out of the box.
Replace per client:
- Files in **`assets/`** (logo `Mobile-nav-Logo.svg`, header logo, `telephone-3.svg`, award/BBB/NATE badges, the Google/Facebook/Yelp rating SVGs `Reviews*.svg`, service photos, team photo, blog thumbnails, Carrier lockup).
- **Section background photos** currently load from the reference host
  (`https://brodypennell.com/wp-content/…`). Point these at client-hosted images (search
  `brodypennell.com` in `index.html` — they're all `src`/`srcset`/`background-image` URLs).

### Fixed (do not change)
`styles.css`, the UIkit runtime, and the overall page **layout/structure**. That's the proven
design — changing it defeats the purpose.

---

## 5. Make a new client site

**A. Full multi-page site (what we did here):**
1. Save each of the client's real pages (**⌘S → "Web Page, Complete"**) into `~/Downloads`.
2. Point the `SAVED` / derivation lists at the top of `build_site.py` at those files; run
   `python3 build_site.py`.
3. Swap `assets/` images for the client's brand; edit the nav/footer link lists; paste the
   3 GHL IDs; deploy.

**B. Homepage-only from the token template:**
1. Copy `template.html`; collect the 54 values via **`VARIABLES.md`** (Noor's intake).
2. Find-and-replace every `{{TOKEN}}`; expand the `REPEAT` blocks; edit the Level-3 lists.
3. Swap `assets/` images; paste the 3 GHL IDs; save as `index.html`; deploy.

## 6. Deploy

Plain static site — any host works. With Vercel CLI from the project folder:
```bash
vercel --prod        # first run links/creates the project, then deploys
```
Root `/` serves `index.html` automatically. Re-run the same command to redeploy after edits.

## 7. How it was built (maintainers)

- **`build.py`** turns a **"Save Page As → Webpage, Complete"** export of the homepage into
  `template.html`: strips all `<script>`/WordPress/Gravity/analytics/chat code, keeps the exact
  DOM + real theme CSS (→ `styles.css`), copies brand images to `assets/`, swaps
  form/chat/scheduler for GHL embeds, and tokenizes client strings to `{{VARS}}`.
- **`fill_preview.py`** fills `template.html` with reference values (+ a static demo form).
- **`build_site.py`** assembles the 22-page site: it reuses one shared frame (head + header +
  footer + GHL runtime), pixel-clones each saved interior page's `<main>` (same cleaning as
  above), generates the remaining service pages from the AC templates, and rewrites every
  internal link to a flat local slug so the nav works as one connected site.

To rebuild after editing a source page, re-run the relevant script. For a different vertical,
start from fresh Save-Complete exports and adapt the path/anchor lists at the top of the scripts.

## 8. Notes & caveats

- **Template-safe by design.** Every page contains only (a) `{{TOKENS}}` for company data
  (name, phone, email, address, city, license, GHL IDs, social) or (b) generic copy that
  names no specific business. The "screams-specific" lines were removed/genericized: no
  "Serving … since 19xx", no "Award-Winning", no specific Google/Facebook/Yelp rating numbers,
  no brand lock-in. Reviews are `{{REVIEW_*}}` placeholders.
- **Brand imagery → neutral placeholders.** Logo → `assets/logo-placeholder.svg` ("YOUR LOGO"),
  award/cert badges → `assets/badge-placeholder.svg` ("Licensed & Insured"), rating badges →
  `assets/rating-stars.svg`, photos → `assets/placeholder.svg`, hero band → brand-navy. Swap
  these for the client's real assets at launch.
- **SEO included on every page:** unique tokenized `<title>` + meta description, `<link rel=canonical>`,
  Open Graph + Twitter tags, HVACBusiness JSON-LD schema, plus `sitemap.xml` and `robots.txt`
  (all using `{{SITE_URL}}`). Set `{{SITE_URL}}` to the client domain before submitting to search.
- **Demo forms are static mockups**; real sites use the GHL form iframe via
  `{{GHL_CONTACT_FORM_ID}}` (chat + calendar via their IDs).
- **Images load from the reference brand's host by default** (see §4 Level 4). For a launched
  client site, re-host images on the client's domain/CDN so nothing depends on a third party.
- **Generated service pages** carry the AC pages' body copy under correct service headings —
  replace that body copy with the client's real copy before launch (see §3).
- The original site used **two phone numbers**; this template **unifies both to `{{PHONE}}`**.
- **Brand/trademark:** the demo reproduces a real company's branding for reference. Ship client
  sites with the *client's* branding, copy, and assets.
