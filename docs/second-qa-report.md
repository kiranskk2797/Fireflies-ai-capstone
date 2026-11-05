# Fireflies Prototype — Independent Second QA Report

**Execution date:** 2026-11-05  
**Application:** `artifacts/fireflies-commitments`, served at `http://localhost:5173`  
**Scope:** Independent browser verification of the original QA findings and remediation claims. Application source was not modified.  
**Method:** Shared Chromium browser, manual UI actions and browser-side controlled localStorage fixtures. Fixtures were removed with Reset demo after testing.

## Summary

Most lifecycle, reassignment, route, and 14-day cohort behaviors reported as remediated were reproduced successfully. The controlled Analytics cohort independently calculated to **4 / 9 = 44%**. The original sample has no structured confirmation or resolution timestamps and shows the 14-day metric as **Unavailable**.

Two issues remain before an unqualified prototype demonstration:

1. The empty Analytics sample shows a **0% snapshot** despite having no commitments. The separate 14-day rate correctly shows Unavailable, but the snapshot percentage can imply measured zero performance when there is no data.
2. An open task's check control is exposed to assistive technology as **“Open details”**, but clicking it marks the item Done immediately. This mismatch can resolve an item when the user expected to inspect it.

The in-app Project notes and Mini PRD also still describe dropping as optional-reason behavior, contradicting the implementation and updated acceptance checklist.

## Test results

| Test ID | Scenario | Expected result | Actual result | Status | Evidence | Severity if failed |
|---|---|---|---|---|---|---|
| LIFE-01 | Drop with an empty reason | Reject; status and history unchanged; show validation. | UI showed “A reason is required to deliberately drop this commitment.” Item remained Open and history stayed at one event. | **Pass** | Controlled Open fixture, browser status toast and localStorage state. | — |
| LIFE-02 | Drop with whitespace-only reason | Trim and reject; no resolution event. | Whitespace-only reason produced the same validation; item remained Open and history unchanged. | **Pass** | Same controlled Drop dialog; state re-read after attempt. | — |
| LIFE-03 | Drop with a valid reason | Become Deliberately Dropped; save reason and resolution type/event. | Item became `dropped`, stored the trimmed reason, `resolutionType: dropped`, and event reason. | **Pass** | Controlled fixture state after submitting “No longer required after decision.” | — |
| LIFE-04 | Reopen with an empty reason | Reject; retain resolved state and history. | UI showed “A reason is required to reopen this commitment.” Item remained Done and event count did not change. | **Pass** | Controlled Done fixture, modal validation and localStorage state. | — |
| LIFE-05 | Reopen with a valid reason | Return to Open; preserve prior resolution and append a reopen event. | Item returned to Open, current `resolvedAt`/resolution type cleared, reason stored, and a `reopened` event appended. The prior Done event remained. | **Pass** | Controlled Done fixture; state contained both events after reopen. | — |
| LIFE-06 | View reopened history | Show the prior resolution and the new reopen reason/event in detail. | Detail view showed status Open, “Commitment reopened” with its reason, and the retained “Marked done” event. | **Pass** | Opened controlled reopened commitment detail; both events were visible in Activity. | — |
| LIFE-07 | Save progress and refresh | Save short update with actor/time; preserve wording/status; display latest update and history after reload. | Update persisted after reload; status stayed Open, wording stayed unchanged, and detail showed latest update, Kirankumar S, timestamp, and `Progress updated` history entry. | **Pass** | Browser refresh on a controlled Open fixture; inspected detail and stored record. | — |
| LIFE-08 | Material wording change without reason | Reject and preserve existing wording/history. | UI showed “Add a reason for changing this confirmed commitment.” Original wording remained; no revision-pending state or event was added. | **Pass** | Controlled Open fixture; missing-reason attempt and state read. | — |
| LIFE-09 | Material wording change with reason | Preserve old/new wording, reason and prior history; require reconfirmation. | Wording changed, `revisionPending` became true, and a `material_change` event contained old/new wording, reason, and prior confirmation history remained. | **Pass** | Controlled fixture after “Requirements changed” save. | — |
| LIFE-10 | Owner reconfirms a material change | Clear pending revision and record owner reconfirmation/start timestamp. | Reconfirmation cleared `revisionPending`, refreshed `confirmedAt`, appended `revision_confirmed`, and restored normal Open actions. | **Pass** | Browser action followed by localStorage state check. | — |
| OWN-01 | Current owner marks Done | Become Done with explicit resolution type/time/event. | Kirankumar-owned controlled commitment became Done with `resolutionType: done` and a structured resolution timestamp/event. | **Pass** | Browser completion action; subsequent state inspection. | — |
| OWN-02 | Unrelated participant attempts Done | No state change; reject unauthorized action. | A Maya-owned Open fixture exposed no Done action. The row completion control attempt showed “Only the current owner can mark this commitment Done.” State remained Open and history unchanged. | **Pass in simulated actor UI** | Controlled non-owner fixture; toast and post-attempt state. | — |
| OWN-03 | Unrelated participant attempts reassignment | No reassignment action available to non-owner. | Maya-owned detail showed “Only the active owner can change this commitment.” No Done or reassignment controls were present; state stayed Open. | **Pass in simulated actor UI** | Controlled non-owner detail view; action list and stored state. | — |
| OWN-04 | Current owner requests reassignment | Request remains pending with original owner accountable and no resolution fields. | State became Pending, original owner remained Kirankumar S, proposed owner was Maya Chen, and no resolution timestamp/type was set. | **Pass** | Owner-side Reassign form and persisted state. | — |
| OWN-05 | Receiver has not accepted | Pending item remains unresolved and under original owner. | Pending fixture retained the original owner and displayed Awaiting acceptance. Analytics controlled cohort did not include it in the resolved numerator. | **Pass** | Pending state inspection and controlled Analytics results (ANA-01). | — |
| OWN-06 | Receiver accepts | Close prior instance as Reassigned and create linked Open successor for receiver. | The receiver accepted; predecessor became Reassigned with reassignment resolution type, and a linked successor opened under the receiving owner. | **Pass in same-browser simulation** | Controlled pending fixture; predecessor and linked successor state. | — |
| OWN-07 | Receiver declines | Return commitment to Open under original owner; no resolution. | Decline returned the item to Open under Maya Chen, removed the proposed owner, and left it unresolved. | **Pass in same-browser simulation** | Controlled pending fixture; post-decline state. | — |
| OWN-08 | Manager/independent user boundary | Verify manager cannot force a transfer or resolve for another user. | **Not tested.** The prototype exposes only one fixed simulated actor; it has no independent manager/owner sessions or server authorization. | **Not tested** | This boundary is disclosed in prototype documentation; same-browser fixture actions cannot prove multi-user enforcement. | N/A |
| ANA-01 | Controlled 14-record cohort | Independently calculate valid mature denominator and explicit-resolution numerator. | **Expected:** 9 denominator, 4 numerator, 4/9 = 44.44%, rounded to **44%**. **Observed:** 9 complete-window commitments, 4 explicit resolutions, UI 44%. | **Pass** | Browser-injected controlled data and Analytics benchmark text. Breakdown below. | — |
| ANA-02 | Day-13/day-14/day-15 observation boundary | Day 13 excluded; day 14 and day 15 eligible. | Day-13 Open and Done were excluded from the denominator. Day-14 Done and day-15 Open were included. The day-14 Done counted as resolved within its window. | **Pass** | Controlled UTC calendar-date fixtures; the UI denominator/numerator matched. | — |
| ANA-03 | Silent inaction, Blocked, Pending | Remain unresolved; count only in eligible denominator. | Open, Blocked, Pending reassignment and reopened Open records did not increase the 14-day numerator. | **Pass** | Controlled Analytics cohort; current statuses and rendered numerator checked. | — |
| ANA-04 | Candidate and Declined records | Exclude from valid commitment denominator and resolved numerator. | Candidate and Declined fixtures did not enter the 14-day denominator. | **Pass** | Controlled Analytics cohort and rendered 9-record denominator. | — |
| ANA-05 | Reopened commitment | Prior resolution event remains historical, but current Open state is not currently resolved. | Reopened record remained Open and was denominator-only; its historical Done event remained visible in detail but did not count in the current numerator. | **Pass** | Analytics fixture plus Activity view test LIFE-06. | — |
| ANA-06 | Missing timestamps / seed history | Do not infer or fabricate timestamps; exclude records without a complete observation window. | Controlled missing-time record remained without `confirmedAt` and was excluded. After Reset demo, all 8 original records had zero structured confirmation and resolution timestamps; metric showed Unavailable. | **Pass** | Browser localStorage check before/after reset and seed Analytics display. | — |
| ANA-07 | Empty dataset | Avoid NaN, division errors, and misleading rates. | No NaN or runtime error; North Star showed Unavailable. However, the separate all-time snapshot displayed **0%** for 0 commitments. | **Fail** | Empty localStorage dataset on Analytics; KPI cards displayed total 0, resolved 0, resolution rate 0%. | **Medium** |
| NAV-01 | Home, Meetings, valid meeting, invalid meeting, Analytics, Tasks | Each route renders its expected screen. | All six route checks rendered the expected heading/content. | **Pass** | Browser route smoke checks against `/`, `/meetings`, `/meetings/research-planning`, `/meetings/not-a-meeting`, `/analytics`, and `/tasks`. | — |
| NAV-02 | Meeting detail tabs and linked commitment | Summary, Transcript and Tasks tabs work; Tasks shows the selected meeting’s linked commitment. | Summary and Transcript rendered; Tasks tab showed the Research planning commitment “Draft the customer interview guide for the November study.” | **Pass** | Valid meeting detail; all three tabs interacted with and content inspected. | — |
| NAV-03 | Invalid meeting ID and return link | Show not-found state, not another meeting; return to Meetings. | `/meetings/not-a-meeting` showed “Meeting not found” without sample meeting content. Back to Meetings returned to the five-item Meetings list. | **Pass** | Invalid route and not-found link interaction. | — |
| REG-01 | Browser console/page errors | No application console or uncaught page errors during route smoke. | No console errors or `pageerror` events observed during the smoke sequence. | **Pass** | Playwright listeners around the six-route smoke pass. | — |
| REG-02 | TypeScript check | Typecheck succeeds. | `pnpm run typecheck` exited 0. | **Pass** | Package command executed in `artifacts/fireflies-commitments`. | — |
| REG-03 | Production build | Build succeeds with required `PORT` and `BASE_PATH`. | `PORT=5173`, `BASE_PATH=/`, `pnpm run build` exited 0; Vite 7.3.7 transformed 1,684 modules. | **Pass** | Package build output. | — |
| RESP-01 | 1440×900, 1280×800, 1024×768, 768×1024, 390×844 | No horizontal overflow; controls fit; navigation remains present. | Home, Meetings, meeting detail, Analytics and Tasks were visited at each size. No document horizontal overflow. At 390px, Tasks heading actions stacked vertically inside the viewport. | **Pass** | Browser viewport loop; document scroll width and main-heading control bounds recorded. | — |
| RESP-02 | Long-history detail modal at 390×844 | Modal remains usable without clipping; actions reachable. | Modal fit within viewport bounds and scrolled internally (2,163 px content). Confirm ownership was below the initial viewport, then became visible after scrolling the modal to its end. | **Pass with usability observation** | Controlled candidate with 24 history entries; measured footer before and after scrolling. Before: footer button top 2,171 px and not visible. After: button bounds 748–779 px, visible inside the viewport. | — |
| UI-01 | Open-row check control labeling/action | A control announced as “Open details” should open details or identify its completion action accurately. | Clicking the owner’s control announced as “Open details” immediately changed the commitment to Done; the dedicated Done button was no longer present. | **Fail** | Controlled Open owner fixture; inspected `aria-label`, clicked control, and re-read status/resolution type. | **Medium** |
| DOC-01 | Drop reason guidance consistency | PRD and user-facing notes should reflect mandatory reason behavior. | Remediation report and acceptance checklist say reason is required, but Mini PRD FR-5 and in-app Project notes still say drop reason is optional. | **Fail** | Read the requested Mini PRD/checklist and inspected the live Project notes screen. | **Low** |

## Controlled Analytics calculation

All fixture dates were generated relative to the browser’s current UTC calendar date for this check; no fixture was retained in the restored demo.

| Record | State at check | Denominator | Numerator |
|---|---|---:|---:|
| Valid mature Done | Done, explicit outcome | 1 | 1 |
| Valid mature Deliberately Dropped | Dropped with reason | 1 | 1 |
| Valid mature Accepted Reassignment | Reassigned after receiver acceptance | 1 | 1 |
| Valid mature Open | Open | 1 | 0 |
| Valid mature Blocked | Blocked | 1 | 0 |
| Pending reassignment | Pending; original owner retained | 1 | 0 |
| Candidate | Awaiting confirmation | 0 | 0 |
| Declined | Candidate declined | 0 | 0 |
| Reopened | Current Open; prior Done event preserved | 1 | 0 |
| Immature resolved | Done, confirmed 13 days before check | 0 | 0 |
| Day-13 boundary | Open | 0 | 0 |
| Day-14 boundary | Done, resolution on day 14 | 1 | 1 |
| Day-15 boundary | Open | 1 | 0 |
| Missing timestamps | Open with no confirmation/resolution timestamps | 0 | 0 |
| **Total** |  | **9** | **4** |

**Manual expected calculation:** (1 Done + 1 Dropped + 1 Accepted Reassignment + 1 day-14 Done) / (the 7 mature valid records among the first 9 lifecycle states + day-14 Done + day-15 Open) = **4 / 9 = 44.44%, displayed as 44%**. Candidate, Declined, both day-13 records, and missing-timestamp record are excluded. Pending, Open, Blocked and current-Open reopened work remain unresolved.

The separate snapshot showed 5 currently resolved statuses among 14 records (**36%**), including the immature Done record. It was labeled as a sample status snapshot, not the 14-day rate.

## Findings and recommended fixes

1. **Medium — misleading empty snapshot.** Show `Unavailable` or an em dash for the snapshot rate when total commitments are zero; retain zero counts. The 14-day metric already behaves this way.
2. **Medium — mislabeled completion control.** Rename the open-row check control to “Mark Done” (including its accessible name), or make it open details if that is the intended action. Ensure the completion affordance communicates that it immediately records a resolution.
3. **Low — stale lifecycle documentation.** Update Mini PRD FR-5 / flow wording and the in-app Project notes so they consistently require a non-empty drop reason. The current acceptance checklist and remediation report already describe the mandatory reason.
4. **Prototype limitation — real role separation unverified.** Demonstrated UI guards depend on the fixed Kirankumar S actor and browser-local state. Do not interpret these checks as manager/owner security validation.

## Readiness

**Prototype readiness: Ready after minor fixes.** The core lifecycle and cohort calculations passed this pass, but the two Medium findings should be corrected before a clean demonstration because they can mislead users about commitment completion and empty analytics.

**Production readiness: Not ready.** Authentication, server-side authorization, shared persistence, independent receiving-owner sessions, audit durability, and live Fireflies integrations are outside this prototype and were not tested.

The original 28% baseline and 45% six-month target remain case-study benchmarks. No measured performance or target achievement is claimed.

## Follow-up verification - 2026-11-05

The three findings above were corrected and manually retested in the browser. This follow-up records the current result; the original Fail entries above remain the independent pass's historical findings.

| Finding | Follow-up test and actual result | Status |
|---|---|---|
| LIFE-01/02/03 Drop reason consistency | Empty and whitespace-only Drop submissions left the Open record and history unchanged. A valid trimmed reason saved `status: dropped`, `resolutionType: dropped`, `resolvedAt`, and a typed history event containing the reason. | **Pass** |
| UI-01 Open details resolved accidentally | The row control's accessible name and title are “Open details”. Click, Enter, and Space opened the selected details dialog while the record stayed Open. The separate “Mark Done” action then wrote one Done event and its resolution timestamp/type. | **Pass** |
| ANA-07 empty Analytics snapshot | Empty localStorage records displayed `Unavailable` and “Not enough eligible commitments to calculate this metric.”; an eligible confirmed Open record displayed a valid 0% snapshot. | **Pass** |
| Analytics eligibility and calculations | Controlled synthetic cohort: 8 valid confirmed records produced a 4/8 current-status snapshot of 50%; the mature 14-day North Star cohort produced 3/7 = 43%. Candidate, Declined, Pending, Blocked, silent Open, reopened current-Open, and an immature Done did not enter the resolved numerator. Day 13 was immature; day 14 entered the denominator. | **Pass** |
| Reopen and reassignment regression | Reopening required a reason, returned Dropped to Open, and retained its prior Drop event. A requested reassignment remained Pending under the original owner without resolution fields; an acceptance fixture created a Reassigned predecessor and linked Open successor; decline returned the record to Open under the original owner. | **Pass** |
| Route and runtime regression | Home, Meetings, valid meeting detail, invalid meeting detail, Analytics, Tasks, and Project notes rendered; invalid detail showed the Meetings back link. Refresh restored seed localStorage data. No browser console or page errors were observed. | **Pass** |

Typecheck and production build passed after the application edits. No automated E2E suite is configured; these are manual browser results using synthetic QA fixtures, not live product performance measurements. The case-study 28% baseline and 45% target remain assignment benchmarks only.
