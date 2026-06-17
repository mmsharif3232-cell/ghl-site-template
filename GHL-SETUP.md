# Putting these templates into GoHighLevel

The design lives **inside GHL** as Custom-Code pages, driven by GHL **custom values**, cloned to
clients via **snapshot**. CSS/images load from a hosted base (our build, or re-host in GHL Media
Library). The `ghl/` folder has each page ready to paste.

## A. One-time — build a design as a GHL template (in a "template" sub-account)

1. **Funnels / Websites → New Website.** Add one blank page per file in `ghl/`
   (Home, Air Conditioning, Heating, About, Contact, Reviews, Service Areas, …).
   *(For GHL, a lean 6–10 page set converts best — you don't have to use all 22.)*
2. On each page: add a full-width **Section → 1 Column → Custom Code/HTML element**, and paste the
   matching `ghl/<page>.html`. CSS/JS/images are already linked to the hosted base.
   *(Optional: upload `styles.css` + `assets/` to GHL **Media Library** and swap `ASSET_BASE`
   at the top of `ghl_build.py`, then re-run, to host everything in GHL.)*
3. **Forms & Calendar:** replace the form placeholder in the contact section with a **native GHL
   Form** element (leads flow into the CRM), and drop a **GHL Calendar/booking** element where the
   "Request Service / Book Online" buttons point. **Chat:** enable the account **Chat Widget**
   (Sites → Chat Widget) — it shows site-wide, no per-page work.
4. Set each page's **path** to match the nav (`/`, `/about`, `/air-conditioning`, …).
5. **Settings → Custom Values:** create the values listed in `GHL-CUSTOM-VALUES.md`.
6. Save the funnel as a **Template**, and/or build a **Snapshot** of the sub-account.

## B. Per client — fast onboarding

1. Create (or pick) the client's **sub-account** → **load the snapshot** / import the template funnel.
2. Fill the **Business Profile** (name, phone, address, email, city, website) → every
   `{{location.*}}` built-in auto-populates across all pages.
3. Set the **Custom Values** (hero headline, years in business, social links, **brand colors**,
   logo URL, etc.) — fill once, the whole site updates.
4. Confirm the **GHL Form + Calendar** on the contact page and the **Chat Widget**.
5. Point the client's **domain** at the funnel. Live — hosted in GHL.

## C. The 5–6 designs

Each design is its own `ghl/` set + snapshot (Design 1 = the current build). On the client call:
pick the design, grab their brand colors → set custom values → live. Adding a design = a new
layout in the same token system, re-run `ghl_build.py`, snapshot.

> Want this automated? With a **GHL API key / private integration**, custom values, funnel
> creation, and snapshots can be pushed programmatically instead of pasted by hand.
