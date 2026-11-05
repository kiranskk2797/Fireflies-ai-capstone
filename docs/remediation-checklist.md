# Remediation sprint checklist

Prepared before application edits on 2026-11-05. Verified against the current `src/App.tsx`, project docs, and available package scripts. No automated test runner or first-party tests are configured in this workspace.

| Item | Current code location | Planned remediation | Verification |
|---|---|---|---|
| Require drop reason | `App.tsx`: `runModalAction` drop branch; reason field in modal | Trim and reject empty reason; inline alert; persist reason in structured lifecycle event; guard owner | Exercise blank, whitespace, and valid reasons in browser; verify state/history/Analytics |
| Add progress update | `Commitment` / `EventItem`; commitment detail modal and `InspectActions` | Add short owner-only progress modal, ISO timestamp/actor, latest update and history display; no wording/status change | Submit update; inspect history and persisted localStorage after refresh |
| Add reopening | `InspectActions`, modal renderer, lifecycle helpers | Add owner-only resolved-item reopen action; mandatory reason; clear current resolution fields while retaining old resolution event; return to Open | Reopen Done and Dropped; empty reason rejected; verify event and snapshot state persist |
| Preserve/reconfirm material edits | `runModalAction` edit branch and edit form | Record revision {before, after, reason, actor, timestamp}; require reason for confirmed-item changes; mark revision pending and require current owner reconfirmation before normal resolution actions | Edit wording and due date; verify old version, new version, reason, actor/time, pending confirmation, and explicit reconfirm |
| Enforce simulated actor boundary | Task row callbacks, modal actions, transfer accept/decline helpers | Centralize owner/receiver checks for resolve/drop/reopen/progress/reassign and recipient acceptance; keep receiver acceptance same-browser simulated | Exercise authorized and non-owner controlled records; verify no state/history change for rejected actions |
| Handle unknown meeting | `MeetingDetail` meeting lookup | Render a missing-meeting state with link to `/meetings`; remove first-record fallback | Test a valid ID, invalid ID, and return-to-list link |
| Add credible 14-day support | `Commitment`, event helper, candidate confirmation, done/drop/transfer transitions, Analytics | Add optional ISO confirmation/resolution timestamps and resolution type; populate only on new explicit events; exclude candidates/declined; denominator requires full 14-calendar-day observation; use `Unavailable` when cohort cannot be calculated | Seed controlled browser data with explicit historical ISO values; manually verify eligible count/rate and immature exclusion |
| Align Drop documentation | `docs/mini-prd.md`, Project notes in `src/App.tsx`, downloadable Mini PRD, and acceptance checklist | Require non-empty reason, reject whitespace-only input, retain reason in history, and distinguish Drop from Done and accepted reassignment | Updated; verified source text in Markdown and generated DOCX |
| Details control opens without resolving | `src/App.tsx`: `TaskRow` row-details control; `src/index.css` | Show a visible “Details” label, use the matching “Open details” accessible name, route the button to details unconditionally, and retain separate explicit Mark Done | Browser checked with click, Enter, Space, and explicit Done history event |
| Empty snapshot is unavailable | `src/App.tsx`: `isValidCommitment`, `getFourteenDayMetric`, `AnalyticsPage` | Share valid confirmed-record eligibility; render Unavailable with explanation when snapshot denominator is zero and preserve true 0% | Browser checked: empty, zero-resolution eligible, and controlled non-empty cohorts |
| Deliver report | `docs/remediation-report.md` | Record defect, root cause, files, fix, test evidence, pass/fail, limitations | Confirm every listed scenario has an actual result or is explicitly unverified |
| Regression checks | Existing package scripts and browser | Re-run typecheck/build; visit Home, meetings, valid/invalid detail, Analytics, Tasks; check persisted state and browser errors | Record command and browser results; do not infer unrun scenarios |

## Constraints

- Preserve current React/Wouter/localStorage architecture and visual language; no new dependencies or backend/auth system.
- Existing seed records have human-readable dates only. Do not convert or infer those as structured lifecycle timestamps; their 14-day status must remain `Unavailable` until a real explicit event creates usable timestamps.
- Browser actor checks are prototype UI simulation only. They are not production authorization.

## Execution status — 2026-11-05

All planned remediation items were implemented and exercised as documented in [`remediation-report.md`](./remediation-report.md). Final `pnpm run typecheck` and the Vite production build passed. Browser checks covered drop validation, progress persistence, reopening, material-change reconfirmation, owner/receiver guards, meeting route handling, analytics empty and controlled data, and route smoke checks. The exact 14-day boundary check excluded a day-13 cohort and included a day-14 cohort; a day-15 cohort remained mature in the denominator. Temporary test data was removed with Reset demo. The package has no automated test runner, so workflow results are manual browser checks, not automated suite results.
