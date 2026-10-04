# Frontend handover — 4 October 2026

The existing frontend is ready for the next GitHub connection step. No GitHub repository, external deployment or payment integration was created by this review.

## Completed

- Consistent editorial headings with modern sans-serif navigation, cards, forms and body text. Larger photo captions and supporting text, readable paragraph widths and mobile inputs of at least 16px.
- Refined sticky header: original logo, compact desktop navigation, active section indicators, rounded dropdowns, clearer support action and a scrollable mobile/tablet menu. Keyboard focus and Escape behaviour retained.
- All 21 pages, six pillar statuses, approved origin story, five-step Roti Challenge and 80-image gallery retained.
- Contact, volunteer, partnership and support forms reviewed: required fields, email/phone validation, consent, query-driven interests, accessible error summary and honest preview completion state.
- Privacy Policy, Terms & Conditions and Donation and Refund Policy remain accessible, labelled drafts. Their organisation-dependent placeholders remain visible for review, not presented as verified public terms.
- Logo colours, favicon and linked Red Pumpkin Marketing footer credit preserved.

## Actual checks

126 route/viewport checks: 21 routes at 1440, 1200, 1024, 768, 390 and 320px. Checked headings, metadata, image loading, horizontal overflow and footer credit. Local audit passed 1,268 link/asset targets. Tested mobile navigation and submenus, Escape, all four forms with empty/invalid/valid preview and phone-only input, interest preselection, story filters, reduced motion, hero controls, gallery categories and 18/36/80 expansion, enlarged photo closing and restored focus. Desktop, tablet and mobile layouts were visually reviewed; contact form, tablet menu and privacy page received additional visual inspection.

## Still required before public launch

1. Official email, telephone, address, privacy contact and verified social links.
2. Enquiry backend and recipients, server-side validation, spam/rate limits, retention and security settings; test actual durable receipt and failure handling before enabling submission success.
3. Policy approval: effective date, service providers, retention criteria, minimum volunteer age/guardian arrangements, approved applicable terms and dispute handling. Review contribution/refund arrangements before introducing payments. No bank details, payment methods or receipt promises are enabled.
4. Verify publication permissions and final captions for supplied photographs. Confirm program specifics and organisation records before adding them.

## Source handoff

`build.py`, `design_v2.py`, `content.json`, `photos.json`, `gallery.json` and `assets/` are the editable source. `python build.py` generates `dist/`. `assets/polish.css` contains the latest typography/header refinement. Website fonts are system-native, with no external font calls or redistributed font files.

For the next repository step, include the source and build instructions, excluding logs, local screenshots and scratch scripts. `dist/` is the static frontend output for a later approved hosting step; do not upload backend configuration secrets or the full authoring archive into a public web directory. Preserve preview disclosures until the launch requirements above are resolved.
