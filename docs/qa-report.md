# Fireflies Commitments Prototype — QA Report

## Initial state

**Inspection date:** 2026-11-05  
**Scope:** Existing React + Vite + TypeScript prototype in `artifacts/fireflies-commitments`.  
**Inspection phase:** Completed before any application code changes. No application files were changed during this initial inspection.

## Project structure and architecture

- This recovered workspace contains multiple projects: the Fireflies commitments frontend, a separate slide deck, a mockup sandbox, an API server scaffold, shared libraries, scripts, and supplied assets. The QA scope is the Fireflies commitments package only.
- The package uses React, TypeScript, Vite, and Wouter. Routes and most product UI, mock data, workflow transitions, and analytics calculations are in `src/App.tsx`; visual styles are in `src/index.css`.
- State is held in React component state. Commitments and theme preference persist in browser `localStorage` (`fireflies-commitments-demo-v1` and `fireflies-theme-preference-v1`). There is no connected application API or multi-user persistence in the prototype.
- Meeting records and participants are hard-coded sample data. The current actor is hard-coded as `Kirankumar S`; recipient acceptance can be simulated in the same browser. Reminder, playback, upload, and export controls disclose that their integrations are not connected.
- Existing documentation includes the README, Mini PRD, reference analysis, and Step 4 acceptance checklist. No test runner or application test suite was found in the package/workspace scan.

## Initial product surface inventory

- Routes found: Home (`/`), Meetings (`/meetings`), meeting detail (`/meetings/:meetingId`), Tasks (`/tasks`), Analytics (`/analytics`), Project notes (`/project-notes`), and a not-found route.
- Home has meeting search, synthetic recent-meeting previews, counts for active commitments, and links to Tasks and Project notes.
- Meetings has All/My meeting tabs, search, synthetic participants/date/duration, meeting details with Summary/Transcript/Tasks tabs, and back navigation.
- Tasks has My Tasks/All Tasks views, search, status filtering, meeting grouping, candidate review, details, create/edit actions, and lifecycle controls.
- Analytics shows status snapshot counts and a snapshot percentage, plus the case-study benchmark. The UI explicitly says this is synthetic data and not a measured 14-day cohort.
- Project notes contains prototype boundaries, reference screenshots, acceptance claims, and assumptions.

## Initial lifecycle and integrity observations

- The status model distinguishes candidate, open, blocked, pending, done, reassigned, dropped, and declined. The helper classifies only done, reassigned, and dropped as resolved. Candidate, blocked, and pending remain unresolved.
- Candidate confirmation checks the proposed owner against the single hard-coded viewer. Transfer acceptance checks the proposed recipient against that same simulated viewer; accepting creates a linked open successor and closes the prior instance as reassigned.
- State transitions append a human-readable event to the commitment history. Events use display strings rather than structured event types or reliable ISO timestamps.
- Drop and candidate-decline dialogs share reason state, but the inspected drop transition stores an empty reason as `undefined`; this appears inconsistent with the requested mandatory drop reason and requires interaction verification.
- No explicit progress-update workflow or reopen workflow was found in the inspected route/state model. The presence of generic edit controls needs further interaction testing to establish what they permit.
- Material edits require a closer check: the model contains no revision/confirmation state, so edit behavior may overwrite the active commitment while only retaining a generic event label.
- The analytics calculation is an all-time local snapshot over the current array. It has no date-range filtering, structured resolution timestamps, or complete-observation-window denominator for the 14-day metric. The shown resolution rate must not be described as the case-study measure.
- Ownership/security is a UI simulation only. A single fixed actor means the app cannot demonstrate independent user sessions, enforce real authorization, or validate manager-vs-owner permissions at a server boundary.

## Initial known integration limits

The prototype README and UI disclose that sample meetings/content are synthetic, changes are browser-local, and notifications, recording playback, meeting synchronization, transcript generation, uploads, and analytics export are not connected. These are scoped prototype boundaries, not claims of live product capabilities.

## QA execution status

This report records the initial code and product-surface inspection only. Build/type checks and interactive route/workflow scenarios are to be recorded in the follow-up results section after they are executed. Findings below must be kept separate from the case-study premises (28% baseline and 45% six-month target).

### Follow-up results

**Execution date:** 2026-11-05  
**Application changes:** None. Only this QA report was added/updated. Controlled test data was reset to the original synthetic sample after the browser checks.

### Validation evidence

- `pnpm run typecheck` in the package: **passed**.
- `pnpm run build` without environment variables: **fails at startup as configured**, because `vite.config.ts` requires `PORT` and `BASE_PATH`.
- `PORT=5173`, `BASE_PATH=/`, `pnpm run build`: **passed**, Vite 7.3.7 transformed 1,684 modules and produced the production assets.
- Browser opened the app at `/`: **passed**. The Home view rendered without a visible runtime error. Its initial synthetic sample showed 8 commitments, 2 resolved, 5 active/unresolved, including 2 candidates, 1 blocked, and 1 awaiting acceptance.
- Browser Meetings list: **passed basic rendering** with five synthetic meetings, participants, dates, durations, and linked-commitment counts. Detail route rendered Summary and linked commitment. Meeting list/detail search, My meetings, Transcript/Tasks tab content, and back navigation were not exhaustively exercised.
- Invalid meeting route `/meetings/not-a-meeting`: **failed**. It silently displayed the first sample meeting rather than a missing-meeting state.
- Browser Analytics with controlled dataset of 10 items (3 done, 1 dropped, 1 reassigned, 2 open, 1 blocked, 1 pending, 1 candidate): **passed snapshot arithmetic**. UI showed total 10, resolved 5, 50%; breakdown showed 3 Done, 1 Dropped, 1 Reassigned, 4 Open/pending (including candidate), and 1 Blocked. Ownership health showed 1 candidate, 1 pending, 1 blocked, and 1 dropped. Snapshot label correctly disclaimed a 14-day cohort. Data was reset afterward.
- Browser Tasks: **passed basic rendering** with active filter and status/owner/action controls. Empty/search/filter behavior, create form validation, detail/history, and actual acceptance/decline flows were not exhaustively exercised.
- Drop action was exercised on a controlled open task: **failed requirement**. The reason field is labeled optional, and submitting it empty successfully changed the item to Dropped. This violates the required deliberate reason.
- Reset demo was exercised and restored the original synthetic sample.
- Project scan found no configured test runner or first-party test suite. No automated end-to-end tests are available in this checkout.

### Findings

| ID | Severity | Finding | Evidence / impact |
|---|---|---|---|
| QA-01 | High | Dropping does not require a reason. | The Drop dialog calls the reason optional; empty submission succeeds and records a Dropped state with no reason. This makes the required honest rationale unenforceable. |
| QA-02 | High | Progress updates are not implemented. | No progress field/action or progress history transition exists. Generic editing changes wording/due date only. |
| QA-03 | High | Reopening is not implemented. | Resolved states have no reopen action/state transition, reason capture, or preserved resolution/re-resolution event model. |
| QA-04 | High | Material changes do not require owner reconfirmation or preserve a prior version. | Owner edit writes new wording/due directly into the same record and adds only a generic “Commitment wording updated” event. There is no revision snapshot or reconfirmation state. |
| QA-05 | High (scope limitation) | Permissions are simulated by one fixed actor in one browser. | Actor is hard-coded as Kirankumar S. Some UI guards compare against this value, but there are no independent user sessions or server-side authorization. The prototype cannot establish that another participant or a manager is technically prevented from changing local state. |
| QA-06 | Medium | Missing meeting IDs render the first meeting. | `/meetings/:meetingId` uses `meetingSamples[0]` as a fallback, so a typo or stale link is misleading instead of showing a missing-record state. |
| QA-07 | Medium | Analytics is only a status snapshot, not a 14-day metric. | No structured meeting/confirmation/resolution timestamps, observation-window eligibility, or 14-day cohort calculation exist. Current events are human-readable strings; the screen appropriately labels its percentage as a snapshot. |
| QA-08 | Medium | Analytics conversation count and date range are hard-coded. | The displayed 11 conversations and Oct 22–28, 2026 range do not derive from the commitment dataset; no range control/filter exists. They should not be interpreted as responsive metrics. |
| QA-09 | Low | Global search accessible name is inconsistent on non-Home routes. | The Meetings and Analytics search controls expose the accessible name “Search tasks” while their placeholder says meetings/analytics. This may confuse assistive-technology users. |
| QA-10 | Informational | Several visible controls are intentionally simulated/unconnected. | Upload, playback, analytics export, reminders/notifications, transcription, and synchronization disclose their prototype status; no external integration was verified. |

### Requirement coverage summary

- **Home/dashboard:** rendered and sample counts checked; recent meeting/commitment links visible. Empty dataset behavior and every navigation/action not fully tested.
- **Meetings:** list and one valid detail observed. Search/tab behavior, transcript/tasks contents, linked-record integrity across all examples, back navigation, empty list, and missing item cases remain partially/unverified. Missing-item case is defective (QA-06).
- **Analytics:** controlled 10-item snapshot arithmetic passed. Empty dataset would guard the percentage division in code, but was not browser-tested. No 14-day eligibility/numerator can be tested because the data model has no structured dates. Date filter is not implemented.
- **Tasks:** active list and lifecycle affordances observed. Controlled empty-reason drop failed the acceptance requirement. Search/filter/sorting (sorting is not exposed), validation, due-date accuracy, and all history paths were not exhaustively browser-tested.
- **Ownership, reassignment, manager behavior:** source inspection shows proposed-owner and recipient actions are gated against a fixed viewer value, and pending reassignment remains unresolved. Accepted transfer code creates a linked open successor and marks the prior record reassigned. Real role isolation, manager-vs-owner access, and independent recipient acceptance cannot be tested in this single-actor frontend simulation.
- **Progress, reopen, and material revision scenarios:** not supported by current UI/state model (QA-02 through QA-04).

### Overall assessment

The existing prototype builds and type-checks with its required environment configured. Its basic Home, Meetings, Tasks, and Analytics surfaces render, and the requested 10-item status snapshot calculates to 50% resolved while keeping pending, candidate, and blocked items unresolved. The prototype is **not ready to claim full lifecycle or end-to-end acceptance**: drop rationale is optional, progress and reopening are missing, edits do not preserve/reconfirm revisions, missing meeting IDs show the wrong record, and permissions/notifications remain local simulations. The 28% baseline and 45% target are case-study inputs only; neither the 25% sample snapshot nor the controlled 50% snapshot is a measured 14-day rate.

The source request ended mid-sentence after “Pending” in its 14-day metric requirements. Any additional clauses after that point were unavailable for this audit.
