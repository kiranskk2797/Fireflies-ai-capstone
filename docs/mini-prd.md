# Fireflies Commitments — Mini PRD

**Product Management Launchpad Capstone · Step 4**  
**Author:** Kirankumar S  
**Document status:** Prototype specification for validation  
**Objective:** Help meeting commitments reach honest closure without assigning work without agreement or adding another project-management system.

## 1. Document overview

This Mini PRD specifies an in-product commitment handoff and resolution experience inside the existing Fireflies Tasks context. It translates the Step 3 direction into a testable prototype: owner-confirmed commitment handoff and lightweight explicit resolution. The deliverables are a browser prototype and a local-downloadable version of this document. The prototype uses synthetic examples and local browser state; it is not a production feature or live integration.

## 2. Problem statement

The capstone's working diagnosis is that an extracted action can be mistaken for an agreed commitment, ownership may be unclear, and follow-through can depend on memory or manual transfer to another tool. In that situation, silence and a checked box do not reliably communicate whether the commitment was completed, transferred, or intentionally dropped.

The proposed experience treats extraction as a candidate, asks the proposed owner to agree before activation, and gives the confirmed owner explicit ways to resolve or explain the commitment. The diagnosis is a hypothesis based on the supplied case-study and Step 3 materials; the available evidence does not establish how often each failure occurs or prove that this design will change outcomes.

## 3. Evidence and rationale

| Evidence type | What is known | How it is used |
|---|---|---|
| Case-study premise | 28% of commitments are resolved within 14 days; the stated target is 45% within six months. | Defines the assignment's baseline and target, not a prototype result or forecast. |
| Supplied interface observation | Screenshots show an existing Fireflies shell and a Tasks experience with task groups, owners, and completion controls. | Grounds where the proposed flow belongs and which visual patterns to preserve. |
| Step 3 report | Interview-tracker summaries describe fragmented tools and manual follow-up; one firsthand observation describes an unnecessary task being deleted and reminders considered irrelevant. | Supports testing task validity, context, user control, and reminder relevance. |
| Evidence limitations | Participant counts and some end-to-end outcomes are not reconciled; the proposed concepts have not been usability-tested or experimentally validated. | Prevents claims of prevalence, causality, or expected impact. |
| Product hypothesis | Context plus owner confirmation may improve trust; explicit outcomes may improve honest closure; restrained follow-up may help without increasing fatigue. | To validate in usability sessions and a measured pilot. |

The numeric Step 3 prioritization scores are directional estimates, not verified RICE inputs. They are not restated as measured evidence here.

## 4. Goals and success criteria

**North Star:** 14-day commitment resolution rate.

**Proposed eligible cohort:** confirmed commitment-owner instances whose first owner acceptance occurs during the selected measurement window. Start the 14-day clock at the timestamp that owner accepts the commitment. Count the instance as resolved inside the window only when it is explicitly marked Done, Deliberately dropped, or Reassigned after the proposed new owner accepts.

Exclude unconfirmed candidates, silent inactivity, blocked commitments, and pending reassignment. A declined candidate is not an accepted commitment and is excluded from this denominator. For reassignment, acceptance closes the prior owner's instance as Reassigned and starts a linked open instance for the new owner. This avoids calling the continuing obligation complete while preserving the case-study's owner-level resolution definition.

**Assignment premises:** baseline 28%; six-month target 45%. These are supplied case-study values, not observed prototype outcomes and not a prediction of lift.

Supporting measures: candidate confirmation/edit/decline/pending rates; time to confirmation; time to explicit outcome; blocked duration; accepted and rejected transfers; deliberate-drop share; sampled candidate quality; reminder dismissals/mutes; user-reported irrelevant reminders; and user-reported assignment pressure or surveillance. Guardrails should be reviewed alongside the North Star. More tasks, more confirmations, or more clicks are not success by themselves.

Before implementation, resolve the cohort window, treatment of a commitment transferred more than once, event timestamp source, reopened commitments, duplicate candidates, and exact day-14 boundary/time-zone rule.

## 5. Target users and needs

| User | Need |
|---|---|
| Individual contributor / proposed owner | Inspect what was said, correct wording, accept or decline without stigma, and control the outcome of work they agreed to own. |
| Commitment maker / meeting participant | See whether an action was accepted, transferred, blocked, completed, or deliberately dropped rather than infer from silence. |
| Suggested replacement owner | Review context and accept or reject before work becomes active under their name. |
| Manager | Coordinate aggregate work and blockers without ranking people or treating unresolved items as performance scores. A manager dashboard is out of scope for this prototype. |
| Administrator / buyer | Understand data handling, integrations, retention, and whether the experience fits existing workflows. These are discovery needs, not implemented configuration capabilities. |

## 6. Scope

**In scope:** meeting-linked candidate review; source/context display; confirm/edit/decline/suggest owner; owner acceptance; active open state; done, deliberate drop, blocked/unblocked, and pending/accepted/rejected reassignment; simulated status-aware follow-up; local synthetic examples; browser persistence; and supporting notes.

**Out of scope:** transcription or extraction changes; automatic commitment activation or assignment; real messages, reminders, or notification delivery; Fireflies authentication or data access; production persistence or multi-user sync; project-management boards; deep third-party integrations; manager performance rankings; and claims that the workflow improves the 14-day rate.

## 7. Current commitment lifecycle

The supplied case-study describes a path in which a meeting ends, an action appears in a summary, participants receive or view the action, and a person may copy it into another tool or rely on memory. If the wording is inaccurate, ownership is implicit, or status is not revisited, the action may remain unresolved with no explicit outcome.

This is a case-study-described and research-informed journey, not a verified end-to-end description of every current Fireflies workflow. The supplied screenshots establish that Tasks and task-assignment patterns exist; they do not verify candidate status, recipient acceptance, deliberate-drop, blocker, reminder, or reassignment behavior in the live product.

## 8. Proposed user flow

1. A meeting-linked extracted action appears as a **Candidate**, with proposed wording, source meeting, brief context, and suggested owner when known.
2. The proposed owner opens context and chooses **Confirm**, **Edit**, **Decline**, or **Suggest another owner**.
3. Confirming or saving edited wording creates an active open commitment under the confirming owner. Declining closes the candidate as not a commitment and stops its simulated follow-up.
4. Suggesting a replacement creates **Awaiting owner confirmation**. The item is not active under that person's ownership until they accept. Rejection returns the item for another owner decision; it does not silently reactivate under the requester.
5. An active owner can mark **Done**, deliberately **Drop** with a required reason, or mark **Blocked** with dependency details. A Drop reason must contain non-whitespace text and is retained in lifecycle history. Deliberate Drop is a resolution distinct from Done and accepted reassignment. Blocked stays unresolved; unblocking returns it to Open.
6. An owner can request reassignment. The item remains pending and unresolved until the proposed recipient accepts. Acceptance closes the previous owner's commitment instance as Reassigned, starts a linked Open instance for the new owner, and stops the previous owner's follow-up. Rejection returns the item to the current owner as Open.
7. Simulated follow-up applies only to confirmed open commitments and stops or adapts after decline, explicit resolution, transfer, or deletion. The prototype does not send notifications.

## 9. User stories

- As a proposed owner, I want meeting context and edit/decline controls so I can decide whether the candidate reflects a real commitment.
- As a proposed owner, I want confirmation to be explicit so an extracted phrase is not treated as accepted work.
- As a person suggesting an owner, I want the replacement to accept before the work becomes theirs.
- As a confirmed owner, I want Done, Deliberately dropped, Blocked, and reassignment choices so the recorded outcome reflects reality.
- As a replacement owner, I want to review and reject a transfer before taking responsibility.
- As a participant, I want a visible outcome so I do not have to infer closure from inactivity.
- As a manager, I want coordination signals that do not imply individual ranking or surveillance.
- As a product researcher, I want event definitions that separate candidate quality, owner agreement, and explicit resolution.

## 10. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | Display each candidate's wording, source meeting, context excerpt, proposed owner when available, and candidate/awaiting-confirmation status. |
| FR-2 | Allow the proposed owner to confirm, edit then confirm, decline with optional context, or suggest a different owner. Validate non-empty wording before save. |
| FR-3 | Keep a suggested replacement inactive until that person accepts. Provide accept and reject choices and a pending state. |
| FR-4 | Show confirmed owner, source, timing, and Open status for active commitments. |
| FR-5 | Allow explicit Done and Deliberately dropped outcomes. Deliberate Drop requires a non-empty, non-whitespace reason, which is retained in lifecycle history. Keep Drop distinct from Done and accepted reassignment. |
| FR-6 | Allow Blocked with a required brief dependency/reason and return to Open when unblocked. Blocked is not resolved. |
| FR-7 | Allow reassignment request, recipient acceptance/rejection, and visible state changes. Pending reassignment is not resolved. |
| FR-8 | On acceptance, stop the prior owner's follow-up, record the accepted transfer, and activate a linked commitment instance under the new owner. |
| FR-9 | Display simulated follow-up state and disclose that notifications are not sent. Resolved, declined, transferred, and deleted items receive no stale follow-up. |
| FR-10 | Provide reachable task navigation, search/filter, clear action feedback, empty/pending/blocked/resolved states, responsive layouts, and demo reset. |
| FR-11 | Persist demo interactions only in the current browser's local storage and label all sample data synthetic. |
| FR-12 | Show case-study metrics as assignment premises, never as measured results of the prototype. |

## 11. Acceptance criteria

| ID | Given / When / Then |
|---|---|
| AC-1 | **Given** an unconfirmed candidate with source context, **when** the proposed owner opens it, **then** the wording, meeting, context, suggested owner, and candidate status are visible before any activation action. |
| AC-2 | **Given** a candidate, **when** the owner confirms it, **then** it becomes Open under that owner and feedback confirms the transition. |
| AC-3 | **Given** an inaccurate candidate, **when** the owner edits the wording and saves, **then** the saved wording is non-empty, visible, and the item becomes an active commitment only after confirmation. |
| AC-4 | **Given** a false-positive candidate, **when** the owner declines it, **then** it is marked Declined/not a commitment, excluded from the resolution denominator, and receives no follow-up. |
| AC-5 | **Given** an owner suggests a replacement, **when** the recipient has not accepted, **then** the item is Pending confirmation and not active under the recipient. |
| AC-6 | **Given** a pending transfer, **when** the recipient accepts, **then** the prior owner instance is explicitly Reassigned, a linked Open instance starts under the recipient, and prior-owner follow-up stops. |
| AC-7 | **Given** a pending transfer, **when** the recipient rejects, **then** the current owner retains the Open commitment and the transfer is not counted as resolved. |
| AC-8 | **Given** an Open commitment, **when** the owner marks it Blocked, **then** the blocker is visible and it remains unresolved; unblocking returns it to Open. |
| AC-9 | **Given** an Open commitment, **when** the owner selects Done or deliberately Drops it with a trimmed, non-empty reason, **then** the matching explicit outcome is visible, the Drop reason appears in lifecycle history, and simulated follow-up stops. Deliberate Drop is recorded separately from Done and accepted reassignment. |
| AC-10 | **Given** a candidate, pending transfer, or blocked item at day 14, **then** it is not counted as resolved; only Done, deliberate drop, or accepted reassignment of the current owner instance qualifies. |
| AC-11 | **Given** any sample data, **when** a user views it, **then** the prototype identifies it as synthetic and discloses that no real integration or notification is active. |
| AC-12 | **Given** a user reloads the same browser, **when** they return to the prototype, **then** local demo changes persist; Reset demo restores the seed examples. |

## 12. States and transitions

| State / outcome | Meaning | Resolved for 14-day rate? |
|---|---|---|
| Candidate | Extracted action awaiting the proposed owner's decision. | No |
| Awaiting confirmation | A named owner or replacement has not accepted responsibility. | No |
| Open | Confirmed commitment currently owned and actionable. | No |
| Blocked | Confirmed commitment is prevented by a dependency or constraint. | No |
| Pending reassignment | Current owner requested transfer; recipient has not accepted. | No |
| Done | Current owner explicitly marked the commitment complete. | Yes |
| Reassigned | New owner accepted; previous owner instance closes and linked new owner instance opens. | Yes for prior owner instance |
| Deliberately dropped | Current owner explicitly records that the commitment is no longer needed with a non-empty, non-whitespace reason retained in lifecycle history. Distinct from Done and accepted reassignment. | Yes |
| Declined | Proposed owner says no commitment was made; candidate never becomes active. | Not eligible |

Allowed transitions are Candidate → Open, Declined, or Awaiting confirmation; Awaiting confirmation → Open or returned for owner selection; Open ↔ Blocked; Open → Pending reassignment → Open on rejection or Reassigned plus linked Open on acceptance; Open → Done or Deliberately dropped. No transition treats silence as resolution.

## 13. Edge cases

- **False positive:** decline without blame; do not create an active commitment or include in denominator.
- **Owner declines:** return to the proposer/meeting owner to choose another owner or drop the candidate; never auto-assign.
- **Invalid wording:** reject blank/whitespace-only edits and retain the candidate for correction.
- **Deliberate Drop:** reject an empty or whitespace-only reason without changing state; retain a valid reason in history. A reasoned Drop is an explicit resolution and remains distinguishable from Done and accepted reassignment.
- **Reassignment rejection or timeout:** retain current owner and Open status; do not count transfer as resolved. Timeout handling and any reminder require validation.
- **Deleted item:** stop simulated follow-up and preserve enough event data for metric integrity only if retention policy permits; production deletion/audit rules are unresolved.
- **Stale reminder:** check current status before sending any real reminder; prototype only updates local simulated state.
- **Abandoned confirmation:** leave pending and unresolved; define expiry/cleanup policy before implementation.
- **Repeated transfer:** create linked owner instances and count each accepted prior-owner transfer once; define how repeated transfers interact with the original 14-day cohort.
- **Duplicate extraction:** identify/deduplicate candidates before activation; dedupe mechanism is not specified here.
- **Due date missing or ambiguous:** do not invent one; allow no due date and avoid implying a date was agreed.
- **Conflicting edits:** prototype is single-browser; concurrent edits and conflict resolution are not covered.

## 14. Metrics and event tracking

**North Star formula:** number of eligible confirmed commitment-owner instances with an explicit qualifying outcome within 14 days ÷ all eligible confirmed commitment-owner instances in the cohort, using consistent censoring and day-boundary rules.

Suggested events: `candidate_created`, `candidate_viewed`, `candidate_confirmed`, `candidate_edited`, `candidate_declined`, `owner_suggested`, `owner_acceptance_requested`, `owner_acceptance_accepted`, `owner_acceptance_rejected`, `commitment_blocked`, `commitment_unblocked`, `commitment_done`, `commitment_dropped`, `reassignment_requested`, `reassignment_accepted`, `reassignment_rejected`, `followup_suppressed`, `followup_dismissed`, and `commitment_deleted`.

Minimum event properties: pseudonymous commitment and owner-instance identifiers; source meeting reference where permitted; actor role; prior/new state; event timestamp and timezone basis; candidate/owner confirmation timestamps; outcome reason category where voluntary; reminder channel/state if implemented; and parent instance for transfers. Do not collect transcript text or sensitive meeting context in analytics by default.

Guardrails: sampled candidate precision/correction/decline rates; confirmation friction and time; inappropriate-assignment reports; transfer acceptance/rejection; notification dismissals, mutes, and stale reminders; deliberate-drop share (watch for gaming, do not punish legitimate drops); user trust/autonomy reports; and privacy complaints. Review segment-level differences carefully and avoid individual performance rankings.

## 15. Risks and mitigations

| Risk | Mitigation |
|---|---|
| False or inaccurate candidates damage trust. | Show source context; make edit and decline first-class; monitor sampled quality. |
| Confirmation adds friction or candidates are abandoned. | Keep the action lightweight, test language and timing, measure time and pending rates. |
| Suggested ownership feels coercive. | Require recipient acceptance; make decline and rejection safe; never auto-activate. |
| Reminders cause fatigue or become stale. | Start with limited configurable follow-up; suppress on current status; monitor dismissals and reports. |
| Managers use status as surveillance. | Avoid individual rankings and productivity scores; research access, visibility, and retention needs. |
| Metric gaming raises apparent resolution. | Include deliberate-drop and reassignment guardrails; audit event semantics; report outcome mix. |
| Context leaks sensitive meeting information. | Minimize context shown and analytics collected; validate access controls and retention before launch. |
| Design implies unsupported Fireflies capabilities. | Label unverified existing behavior and keep the prototype disconnected from live accounts. |

## 16. Dependencies and assumptions

| Item | Status | Validation |
|---|---|---|
| Meeting-linked candidates can expose useful context. | Assumption; screenshots do not verify available fields. | Product/engineering discovery and user comprehension tests. |
| A proposed owner can be notified and respond in Fireflies. | Unverified production capability; simulated in prototype. | Technical discovery of recipient identity, permissions, and delivery channels. |
| Existing Tasks can support explicit candidate/commitment states. | Design assumption. | Check current data model and user workflow. |
| Reminder delivery can stop or adapt to status. | Unverified. | Trace existing reminder architecture and race conditions. |
| Users want this workflow in Fireflies rather than a connected tool. | Hypothesis from Step 3. | Ask users which systems are their source of truth. |
| 28% and 45% use a comparable eligible cohort. | Assignment premise; cohort details are not supplied. | Confirm denominator, start point, and baseline instrumentation with the case-study owner. |

## 17. Prototype limitations

All meetings, people, candidate wording, and task outcomes are synthetic. The prototype uses browser-local state; it does not connect to Fireflies, send notifications, authenticate users, synchronize across browsers, or persist data on a server. Actions simulate confirmation and recipient acceptance. Screenshots do not establish exact design tokens or hidden product behavior, so fidelity is reference-based and not claimed to be pixel-perfect. The displayed 28% / 45% values are case-study premises, not app analytics. No usability test, experiment, or outcome lift is claimed.

## 18. Open questions and validation plan

**Open questions:** What exactly qualifies as a candidate and how much context is safe/useful? Who proposes the first owner? What happens when nobody accepts? What are the reminder cadence, controls, and expiry? Does accepted transfer close the prior owner instance while preserving a linked obligation? Which time zone defines day 14? How are duplicates, reopenings, deletion, access, retention, and connected-tool sync handled? Is the baseline measured on the same cohort definition?

**Validation plan:** (1) Run moderated task-based sessions with proposed owners, commitment makers, and replacement owners; test candidate comprehension, correction/decline language, and acceptance. (2) Measure completion time, misinterpretations, abandonment, perceived pressure, and reminder expectations; do not treat preference statements as behavioral evidence. (3) Conduct engineering/privacy discovery for source context, permissions, event timestamps, reminder suppression, and deletion. (4) Revise the prototype and cohort definition. (5) Only then consider a limited pilot with predefined outcome and guardrail analysis; compare against a consistent baseline and do not claim causal impact without an appropriate experiment.

## Reference analysis and deliverable checklist

The supplied Tasks screenshots show an existing dark Fireflies shell, left navigation, global search, My Tasks / All Tasks controls, task groups by meeting, completion controls, owners, and compact bordered containers. The prototype adapts these patterns for candidate, ownership, and explicit-resolution states. Other supplied screenshots provide product context but their unrelated modules are not reproduced. The references do not establish exact responsive behavior or the new workflow's existing production capabilities.

The prototype, reference analysis, acceptance checklist, and source/run instructions are delivered alongside this document. Checklist coverage means requirements are represented; it is not evidence that a real Fireflies integration or outcome has been validated.
