# GHL Local-Services Site Template

A reusable, **WordPress-free** website template for local home-services businesses
(HVAC, plumbing, electrical, roofing, etc.), wired for **GoHighLevel (GHL)**.

It is a **pixel-exact rebuild** of a real, high-converting HVAC homepage — same layout,
fonts, colors, spacing, and motion — but with **every client-specific value turned into a
`{{VARIABLE}}`** and the original site's form / chat / scheduler swapped for GHL embeds.

> **Live demo:** _(added after first deploy — see Vercel project URL)_
> **One template → many clients.** Copy the folder, fill the variables, swap the images,
> paste 3 GHL IDs, deploy.

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
| **`index.html`** | The template page. Holds every `{{TOKEN}}` and the `REPEAT` blocks. | **Yes** — fill tokens per client |
| **`styles.css`** | The real compiled theme stylesheet (YOOtheme/UIkit). **This is what makes it look identical.** | **No** — leave it alone |
| **`assets/`** | Logos, badges, icons, photos + `uikit.min.js` (the JS runtime). | **Yes** — swap brand images |
| **`VARIABLES.md`** | The full intake checklist: all 54 tokens grouped, with examples. **Start here for a new client.** | Reference |
| `demo.html` | A fully-filled example (the original brand) — what the live demo serves. | Reference only |
| `vercel.json` | Tells Vercel to serve the demo at `/`. | Rarely |
| `build.py` / `fill_preview.py` | How the template was generated from a saved page + how the demo is filled. | Maintainers only |

---

## 3. What's interchangeable (the important part)

Everything a client sees is changeable. There are **four levels**, easiest → most hands-on:

### Level 1 — Variables (`{{TOKENS}}`) — find & replace
54 tokens cover the bulk of the content. Full list + examples in **`VARIABLES.md`**. Highlights:

| Category | Tokens |
|---|---|
| **Identity** | `{{BUSINESS_NAME}}`, `{{BUSINESS_SHORT_NAME}}` |
| **Contact / NAP** | `{{PHONE}}`, `{{PHONE_DISPLAY}}`, `{{ADDRESS}}`, `{{DIRECTIONS_URL}}`, `{{LICENSE}}`, `{{OFFICE_HOURS}}` |
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

## 4. Make a new client site (checklist)

1. **Copy** this folder to a new client folder/repo.
2. Open **`VARIABLES.md`**, collect all 54 values from the client (Noor's intake).
3. **Find-and-replace** every `{{TOKEN}}` in `index.html` with the client value.
4. **Expand** the two `REPEAT` blocks (reviews, cities) to the right counts.
5. **Edit** the literal lists (Level 3) to match the client's actual services/nav/links.
6. **Swap** `assets/` images for the client's brand (Level 4).
7. Paste the **3 GHL IDs** (form, calendar, chat) — see GHL → Sites/Calendars.
8. Open `index.html` in a browser to QA, then **deploy** (below).

---

## 5. Deploy

Any static host works. With Vercel CLI from the project folder:

```bash
vercel --prod        # first run links/creates the project, then deploys
```

`vercel.json` makes `/` serve `demo.html` (the showcase). For a **real client**, set `/` to
serve their filled `index.html` instead (edit the rewrite, or just rename their filled file to
`index.html` and delete the rewrite).

---

## 6. How it was built (maintainers)

The template was generated mechanically from a browser **"Save Page As → Webpage, Complete"**
export of the reference homepage, via **`build.py`**:

- strips all `<script>`/`<noscript>`, WordPress/Gravity/CleanTalk/analytics/chat code;
- keeps the exact DOM + the real theme CSS (vendored into `styles.css`);
- copies brand images into `assets/`, rewrites asset URLs;
- swaps the form/chat/scheduler for GHL embeds;
- replaces client strings with `{{TOKENS}}` and marks repeating lists.

`fill_preview.py` produces `demo.html` by filling the tokens with the reference values (and a
static demo form). To regenerate the template from an updated source, re-point the paths at the
top of `build.py` and re-run. To clone a **different** vertical, start from a fresh
Save-Complete export and adapt the anchors in `build.py`.

---

## 7. Notes & caveats

- **Demo GHL embeds are placeholders** (`DEMO_*` IDs) — the contact form on the live demo is a
  static mockup; real sites use the GHL iframe via `{{GHL_CONTACT_FORM_ID}}`.
- **Images load from the reference brand's host by default** (see Level 4). For a launched
  client site, re-host images on the client's domain/CDN so nothing depends on a third party.
- The original site used **two phone numbers** (a call-tracking number in the header, the
  office line in the footer). This template **unifies both to `{{PHONE}}`**. Split it back if a
  client needs two (search `tel:{{PHONE}}`).
- **Brand/trademark:** the demo reproduces a real company's branding for reference. Use it as a
  layout/template reference; ship client sites with the *client's* branding, copy, and assets.
