# 5-Minute Proof — Template #1 in GoHighLevel

Goal: confirm in a real sub-account that (1) the **custom design renders** inside GHL and
(2) **merge fields fill**. Just the homepage — once this works, every page follows the same recipe.

## Steps (~5 min, one test sub-account)

1. **Business Profile** — Settings → Business Info: set **Business Name, Phone, Email, Address**.
   *(These feed `{{location.name}}`, `{{location.phone}}`, `{{location.email}}`, `{{location.full_address}}`, `{{location.city}}`.)*
2. **One custom value** — Settings → Custom Values → **Add**: name it `hero_headline`,
   value e.g. `Chicago's Trusted Heating & Air Conditioning Experts`.
   *(This proves the `{{custom_values.*}}` mechanism — the rest of the copy is hardcoded for the test.)*
3. **New page** — Sites → Websites (or Funnels) → New → add a blank page “Home”.
4. **Paste the design** — drag in a full-width **Section → 1 Column → "Custom Code / HTML"** element,
   and paste the **entire contents of `ghl/HOME-PASTE.html`**. Save.
5. **Publish / Preview** — open the page's **live preview URL** (not the editor canvas — merge fields
   only render on the published page).

## What you should see (the proof)
- ✅ The full custom design — navy/orange brand, Cinzel headings, hero band, star badges, stacked CTA buttons, services, footer — **styled exactly like our build**.
- ✅ **Business name, phone, address, city** pulled live from the Business Profile.
- ✅ The **hero headline** showing your `hero_headline` custom value.

That confirms the whole approach: your custom design, hosted in GHL, filled by GHL.

## Notes
- **Head/SEO** (title, meta, canonical, JSON-LD) isn't needed for this render test — it goes in the
  page's SEO/Head settings in the full build.
- **Forms / calendar / chat** aren't in this proof block — in the full build they're native GHL
  Form/Calendar elements + the account Chat Widget.
- If GHL's editor strips or wraps anything and it looks off on the preview, **screenshot the GHL
  preview and send it to me** — I'll adjust the block to GHL's quirks. (Or connect a GHL
  private-integration token and I'll run the proof via the API myself.)

## After it's proven
Replicate to all pages (paste each `ghl/<page>.html`), create the full custom-values list
(`GHL-CUSTOM-VALUES.md`), wire native Form/Calendar/Chat, set page paths, **save as a Snapshot** —
then clone to clients and build the other 5 designs.
