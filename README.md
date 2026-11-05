# Fireflies Commitments Prototype

A standalone React, Vite, and TypeScript capstone prototype for owner-confirmed meeting commitments and explicit resolution.

## Requirements

- Node.js 20.19+ or 22.12+
- npm 10+

## Run locally

Run these commands from this directory, the prototype root:

```bash
npm install
npm run dev
```

Vite prints the local development URL. For a production build and local preview:

```bash
npm run typecheck
npm run build
npm run preview
```

## Demo behavior and limitations

- People, meetings, candidate commitments, and activity are synthetic demonstration data.
- Prototype changes are saved in this browser's local storage. They do not sync between users or to Fireflies.
- Actor selection simulates different participants for demonstration; local storage does not provide authentication or production authorization.
- Follow-up and reminders are simulated interface state. The prototype does not send notifications.
- There is no live Fireflies integration, backend, or external service requirement.
- Use **Reset demo** to restore the example data.

## Project materials

- [Mini PRD](docs/mini-prd.md) — product requirements and lifecycle rules.
- [Acceptance checklist](docs/acceptance-checklist.md) — implementation status and checks.
- [QA report](docs/qa-report.md) and [remediation report](docs/remediation-report.md) — recorded findings and remediation evidence.
- [Second QA report](docs/second-qa-report.md) — independent verification record.
- [Reference analysis](docs/reference-analysis.md) — supplied screenshot summary.
- [Project notes](src/pages/ProjectNotesPage.tsx) — in-app capstone notes.
- `public/mini-prd.docx` — downloadable Mini PRD available in Project notes.
- `scripts/build_mini_prd.py` — standard-library script to rebuild the DOCX from its Markdown source.

To rebuild the downloadable document, run from this directory:

```bash
python scripts/build_mini_prd.py
```

## Scope

The prototype demonstrates continuity through owner-confirmed commitment handoff and lightweight explicit closure. It does not establish research findings or measured performance against the case-study 14-day resolution benchmarks. The 28% baseline and 45% target are case-study benchmarks, not prototype outcomes.
