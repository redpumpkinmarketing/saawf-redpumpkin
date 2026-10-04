# Siliguri Aashray Welfare Foundation — website preview

Complete, local-only preview built from the supplied Website Structure and Content document. All 21 approved routes are implemented. Nothing has been publicly deployed.

## Open the preview

Open `dist/index.html` in a browser. Every page works directly from disk, including menus, archive filters and preview form validation.

For the suggested clean URLs, run `python serve.py` and visit `http://127.0.0.1:8765`. The server binds to this computer only. It never accepts enquiries or payments.

## Edit and rebuild

- `content.json`: approved page copy, headings, routes and search descriptions.
- `build.py`: shared header/footer, homepage composition, pillar pages, forms and policy layouts.
- `design_v2.py`: redesigned homepage, inner headers and 80-image archive.
- `assets/styles.css`, `assets/photo-design.css`, `assets/redesign.css`, `assets/editorial.css`: responsive visual system; editorial refinement and logo-blue palette are loaded last.
- `assets/redesign.js`: hero photo controls and progressively expanded photo categories.
- `photos.json` and `gallery.json`: photo descriptions, provenance and archive ordering.
- `assets/site.js`: navigation, accessible validation, query-string interests and filters.
- `assets/config.js`: disconnected enquiry configuration and explicit approval gate.
- `templates.py`: reusable future story, news and program detail layouts. No fabricated records or empty record routes are created.

Run `python build.py` after editing. No package installation or external fonts are required. The output is independent HTML pages with progressive JavaScript enhancement.

## What is included

The homepage follows the specified sequence: hero, Bharosa origin, six impact areas, work and next steps, Roti Challenge, impact archive, community stories, get involved, partnerships, transparency, support invitation and footer. The community stories are the two approved organisation-level narratives, linking to About Us and Roti Challenge.

The exact organisation name, weekly household contribution model, work undertaken, upcoming computer training, planned initiatives and North Bengal vision are preserved. Status badges use the four agreed terms. There are no invented figures, personal testimonials, leaders, credentials or partner records.

Four preview forms follow the documented fields, validation and consent requirements. Relevant links preselect an interest. No fields are stored in cookies, local storage or browser analytics. A valid preview reports that it was **not sent or stored**. A future connected endpoint must return `received: true` only after durable receipt. Success is never based on a timer or an unverified network response.

The Support Our Work page is enquiry based. Bank information, QR codes, payment controls, receipt promises and unverified tax eligibility are absent. Policies are visible as **drafts requiring approval**; every page and the local server discourage indexing. Those controls do not replace the separate public-publication review.

The footer credits **Crafted & Maintained by Red Pumpkin Marketing**, linked to https://redpumpkin.in, as explicitly requested.

## Remaining assets and launch configuration

1. **Brand assets — completed:** the supplied asset pack’s original PNG logo is integrated on every page, with its 1090 × 350 proportions and blue colours unchanged. The supplied 512px favicon and the same pack’s 32px browser icon are wired across all pages. Original PNG/JPG files are included in `assets/`. No transparency conversion was needed for the white header.
2. **Genuine field media — integrated:** 89 supplied photos reviewed; 80 selected photographs integrated into the redesigned site and filterable archive, with responsive WebP variants. See photo-handover.md and photos.json. Confirm dates, locations and publication permissions before launch; photographs are not assumed to be from 2020.
3. **Contact details:** official phone, email, public office address, WhatsApp and verified social URLs. Map/visitor details only after the public location is confirmed. No invented alternatives appear in the preview.
4. **Enquiry delivery:** choose the receiving backend/mailbox, retention criteria, authorised recipients, spam/rate limits and failure handling. Implement and verify server-side validation and durable receipt. Approve privacy practices and safeguarding/guardian requirements, then configure `enquiryEndpoint` and `formsApproved` together. Review client copy to replace preview notices only after verified connection. No backend is connected in this build.
5. **Policy approval:** complete effective dates, provider/data practices, retention, privacy contact, age/guardian rules, applicable terms and contribution/refund arrangements. Do not publish the draft text as approved policy.
6. **Organisation records:** verified leadership, entity and registration information, approved public documents and any confirmed fundraising/tax credentials. None are inferred or shown as credentials.
7. **Program and archive records:** health activity specifics, distribution records and verified figures; computer training dates, location, eligibility, course and registration process. Future story/news records need approval and factual publication dates before routes are generated.
8. **Future payments:** a separate approved financial, donation-policy, accounting and authorised receipt process is required before enabling any payment method. This website does not take donations.

## Verification

`qa-report.json` records browser checks across desktop, tablet and mobile widths. `audit-report.txt` records all local navigation and asset references, duplicate IDs, organisation spelling, status and policy checks. Screenshots are included for review. The validation checks use test inputs in a disconnected preview; no submissions are sent.

The QA script uses Playwright and Chrome installed in the authoring environment. Adapt its module/browser paths on another computer. Building and viewing the actual website do not require either dependency.

## Public publication is a separate step

Before a public release, confirm photo publication permissions and contact/backend details, approve policies, test actual receipt and failure handling, review the site with the foundation, then remove preview notices and indexing restrictions only as part of the approved publication. No publishing configuration or deployment has been created in this preview.

## Latest visual refinement

Calmer serif headings with selective italics, warm cream backgrounds, rounded imagery and pill buttons. The approved logo blue is the primary website colour; muted gold and restrained terracotta are secondary accents. The homepage has shorter summaries and a five-step Roti Challenge feature. Full content remains on the inner pages and all 80 selected gallery photographs remain accessible. No public deployment.

## Final frontend review

See `FRONTEND-HANDOVER.md` for the completed typography/header work, actual checks and precise launch dependencies. `assets/polish.css` is the final stylesheet, loaded after the editorial layer. This preview is prepared for the next GitHub step; form delivery and policy approval are not yet complete.
