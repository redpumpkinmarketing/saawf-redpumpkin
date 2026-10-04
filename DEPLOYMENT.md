# GitHub frontend handoff

The reviewed Siliguri Aashray Welfare Foundation frontend is stored on `main` in `redpumpkinmarketing/saawf-redpumpkin`.

## Static hosting

- Publish directory: `dist/`.
- Optional rebuild: `python build.py` from the repository root.
- Validation: `python audit.py`.
- This is a static HTML/CSS/JavaScript site. It does not require an npm package, Node.js server, or Python on the hosting server.
- Deploy the contents of `dist/` to the web document root, preserving all folders and assets. Keep the editable Python/JSON source outside the public web directory.

The frontend has 21 pages and the 80-photo gallery, with responsive image variants. This repository handoff does not enable Hostinger hosting or GitHub Pages.

## Remaining launch work

Forms remain disconnected preview forms. Privacy, Terms and Donation/Refund policies remain drafts. Confirm official contact details, photo publication permissions and policy wording, and connect and test enquiry delivery before public launch. See `FRONTEND-HANDOVER.md` for the complete list.

## Verification at handoff

The editable source rebuilt all 21 pages successfully. The local audit passed 1,268 link/asset targets, metadata, unique IDs, organisation name, program statuses and draft-policy labels. Existing assets and prepared source files were checked against their original Git blob hashes during upload.
