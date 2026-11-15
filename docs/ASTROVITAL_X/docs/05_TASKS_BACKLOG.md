# 05 — Tasks and Implementation Backlog

**Version:** 1.0  
**Status:** Initial backlog; all implementation tasks are not started unless updated in `06_PROGRESS.md`.

## 1. Prioritization

- **P0:** Must be completed for a credible hackathon MVP.
- **P1:** Valuable next increment; implement if time allows.
- **P2:** Future research or operational integration.

Estimate guide: S = small, M = medium, L = large. Estimates are relative team effort, not promised delivery times.

## 2. Suggested team workstreams

| Workstream | Responsibilities |
|---|---|
| Product / presentation | Scope, user stories, demo narrative, requirements and judging pitch |
| Frontend | Astronaut portal, doctor dashboard, reusable components and charts |
| Backend | Authentication, APIs, persistence, cases, recommendations and audit trail |
| AI / data | Synthetic data, validation, baselines, anomaly rules and source-linked summaries |
| Integration / QA | End-to-end wiring, offline simulation, test plan and demo reliability |

One person may own multiple workstreams in a small team. Every task should have one accountable owner.

## 3. Phase 0 — Project setup and scope lock

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-001 | Confirm software-only scope and non-goals | P0 | S | Team agrees no hardware build, no direct measurement claim, no autonomous diagnosis |
| T-002 | Confirm roles and demo personas | P0 | S | Astronaut, flight surgeon and admin roles documented |
| T-003 | Create repository and branch strategy | P0 | S | README, docs folder and initial branches exist |
| T-004 | Select frontend/backend/database stack | P0 | S | Stack choice recorded in decisions file |
| T-005 | Create synthetic-data policy and demo banner | P0 | S | All demo data visibly marked synthetic |

## 4. Phase 1 — Foundation and data model

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-010 | Define astronaut, user and assignment entities | P0 | M | Schema supports role and astronaut assignment |
| T-011 | Define observation and provenance schema | P0 | M | Source, timestamp, unit, quality and synthetic marker included |
| T-012 | Define case, alert, recommendation and follow-up entities | P0 | M | Full lifecycle can be represented |
| T-013 | Implement database migrations and seed data | P0 | M | Demo environment initializes reproducibly |
| T-014 | Implement authentication for demo roles | P0 | M | Astronaut, clinician and admin can sign in separately |
| T-015 | Implement server-side role checks | P0 | M | Unauthorized cross-astronaut access is rejected |

## 5. Phase 2 — Astronaut portal

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-020 | Build astronaut overview page | P0 | M | Shows profile, synthetic observations and freshness |
| T-021 | Build health timeline | P0 | M | Shows at least three synthetic data series with units and timestamps |
| T-022 | Build symptom check-in form | P0 | M | Submissions are persisted and attributed to user |
| T-023 | Build consultation request flow | P0 | M | Request appears in clinician queue |
| T-024 | Build recommendations page | P0 | M | Astronaut can view and acknowledge recommendations |
| T-025 | Add data-state labels | P0 | S | Synthetic, stale, missing and queued states are visible |

## 6. Phase 3 — Medical expert dashboard

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-030 | Build clinician mission overview | P0 | M | Lists assigned astronauts and open cases |
| T-031 | Build case list and filters | P0 | M | Supports status, priority and astronaut filters |
| T-032 | Build astronaut detail view | P0 | M | Shows observations, symptoms and history |
| T-033 | Build alert detail view | P0 | M | Shows reason, linked observations and data quality |
| T-034 | Implement alert disposition | P0 | M | Clinician can acknowledge, dismiss with reason or escalate |
| T-035 | Implement recommendation composer | P0 | M | Clinician can author and send a recommendation |
| T-036 | Implement follow-up request and response | P0 | M | Astronaut response returns to the case |

## 7. Phase 4 — AI and analytics

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-040 | Create synthetic astronaut time-series data | P0 | M | Dataset has source, unit, timestamp and synthetic marker |
| T-041 | Implement data validation and normalization | P0 | M | Invalid units/timestamps are rejected or quarantined |
| T-042 | Implement transparent demo alert rules | P0 | M | At least one deterministic rule generates an explainable alert |
| T-043 | Implement personal baseline summary | P1 | M | Baseline requires minimum sample count and displays method/window |
| T-044 | Implement anomaly detection experiment | P1 | L | Model output includes version, evidence and limitations |
| T-045 | Implement source-linked AI case summary | P1 | L | Every factual claim references supplied source record IDs |
| T-046 | Add model/rule version registry | P1 | M | Findings record the rule/model version used |

## 8. Phase 5 — Communication and resilience

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-050 | Implement in-app notification list | P0 | M | New case/alert appears to assigned clinician |
| T-051 | Implement consultation message thread | P1 | M | Astronaut and clinician messages are case-linked |
| T-052 | Simulate offline mode | P0 | M | UI shows offline and queued-not-delivered states |
| T-053 | Implement retry/idempotency for queued items | P1 | L | Retry does not create duplicate case events |
| T-054 | Display last synchronization and receipt state | P0 | S | User can distinguish queued, delivered and acknowledged |

## 9. Phase 6 — Security, QA and demo readiness

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-060 | Add audit events for protected actions | P0 | M | Login, profile access, alert and recommendation actions are logged |
| T-061 | Add API and form validation | P0 | M | Invalid inputs return safe errors |
| T-062 | Test role-based access | P0 | M | Astronaut cannot access another astronaut's record |
| T-063 | Test complete consultation workflow | P0 | M | Astronaut-to-doctor-to-astronaut flow passes |
| T-064 | Test offline queue state | P0 | M | Message is not shown as delivered before server confirmation |
| T-065 | Add error, loading and empty states | P0 | S | Each primary page handles loading/error/no-data states |
| T-066 | Prepare deterministic demo scenario | P0 | S | Demo can be reset and repeated with same outcome |
| T-067 | Prepare pitch and architecture visuals | P0 | S | Slides match actual implemented capabilities |
| T-068 | Review safety and claims | P0 | S | No unsupported diagnosis, prediction or NASA-integration claims |

## 10. Phase 7 — Post-hackathon research and integration

| ID | Task | Priority | Size | Acceptance criteria |
|---|---|---:|---:|---|
| T-070 | Identify authorized source-system interface requirements | P2 | L | Data contract and authorization dependencies documented |
| T-071 | Review clinical workflow with qualified medical stakeholders | P2 | L | Review comments and required controls recorded |
| T-072 | Establish dataset governance and validation plan | P2 | L | Data rights, provenance, labels and evaluation protocol documented |
| T-073 | Evaluate model performance and subgroup behaviour | P2 | L | Validation report includes limitations and error analysis |
| T-074 | Perform threat modelling and security assessment | P2 | L | Risks, controls and residual risks documented |
| T-075 | Assess mission/offline deployment constraints | P2 | L | Target environment and operational requirements recorded |

## 11. Recommended hackathon build order

If time is limited, build in this exact sequence:

1. Seed synthetic astronaut and health-observation data.
2. Build the astronaut profile and timeline.
3. Build symptom check-in submission.
4. Build clinician case queue and case detail.
5. Add one explainable rules-based alert.
6. Add clinician recommendation and astronaut acknowledgement.
7. Add synthetic-data, freshness and offline status labels.
8. Add audit events and run the end-to-end demo.

Do not spend the limited build window attempting advanced medical prediction. A reliable, transparent workflow is more convincing than a sophisticated model with no validation.

## 12. Task status conventions

Use one status per task:
- `Not Started`
- `In Progress`
- `Blocked`
- `In Review`
- `Done`

A task is not `Done` until its acceptance criteria are met and the result is demonstrated or tested. Update `06_PROGRESS.md` when changing status.
