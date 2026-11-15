# 06 — Project Progress Tracker

**Baseline date:** 15 November 2026  
**Project status:** Documentation baseline prepared; software implementation not yet evidenced in this project record.

## 1. Current status summary

| Area | Status | Notes |
|---|---|---|
| Product concept | Defined | Software-only astronaut health intelligence and medical collaboration |
| Scope / non-goals | Defined | No sensor, scanner, wearable or hardware development |
| PRD | Draft baseline complete | Requirements need team review and prioritization |
| Architecture | Proposed | Logical design; not deployed or flight-approved |
| UX / design | Proposed | Screen specifications prepared; visual UI not yet evidenced |
| Rules / safety | Draft baseline complete | Requires expert review before any clinical use |
| Task backlog | Prepared | Implementation tasks are not started unless marked otherwise below |
| Data model | Proposed | Requires implementation and migrations |
| API specification | Proposed | Requires implementation and contract tests |
| Test plan | Prepared | Tests have not been executed in this status record |
| Hackathon prototype | Not started / not evidenced | No working application is claimed by this document set |

## 2. Milestones

| Milestone | Definition of done | Status |
|---|---|---|
| M0 — Documentation baseline | PRD, architecture, design, rules and backlog available | Complete for document-pack creation |
| M1 — Local app foundation | Repository, frontend, backend and database run locally | Not Started |
| M2 — Astronaut experience | Profile, timeline and symptom check-in work | Not Started |
| M3 — Medical expert workflow | Case queue, alert review and recommendation workflow work | Not Started |
| M4 — AI/demo analytics | Synthetic data and explainable demo alert work | Not Started |
| M5 — Resilience and audit | Offline-state demo and audit events work | Not Started |
| M6 — Hackathon-ready MVP | End-to-end demo passes acceptance criteria | Not Started |
| M7 — Post-hackathon validation | Expert, security and data-governance reviews completed | Not Started |

## 3. Task status board

Copy task IDs from `05_TASKS_BACKLOG.md` and update the status as work progresses.

| Task group | Task IDs | Status | Owner | Notes |
|---|---|---|---|---|
| Scope and setup | T-001 to T-005 | Not Started | Unassigned | Confirm team decisions and repository |
| Data foundation | T-010 to T-015 | Not Started | Unassigned | Schema, seed data, auth and access control |
| Astronaut portal | T-020 to T-025 | Not Started | Unassigned | Profile, timeline and check-in |
| Doctor dashboard | T-030 to T-036 | Not Started | Unassigned | Case management and recommendations |
| AI and analytics | T-040 to T-046 | Not Started | Unassigned | Start with transparent rules |
| Communication | T-050 to T-054 | Not Started | Unassigned | Notification and offline-state demo |
| QA and demo | T-060 to T-068 | Not Started | Unassigned | Security, tests and pitch readiness |
| Research integration | T-070 to T-075 | Not Started | Unassigned | Future authorized operational work |

## 4. Blockers and dependencies

| Item | Type | Impact | Owner | Next action |
|---|---|---|---|---|
| No authorized real astronaut dataset | Data dependency | Real-data integration cannot be demonstrated | Unassigned | Use synthetic records; document future authorization need |
| No approved external spacecraft API | Integration dependency | No live spacecraft connection can be claimed | Unassigned | Build source adapter interface and synthetic fixture loader |
| No clinical threshold approval | Clinical governance | No operational clinical alert threshold can be claimed | Unassigned | Use clearly labelled demo-only rules |
| No validated medical model | Validation dependency | No diagnostic or predictive accuracy claim can be made | Unassigned | Use explainable anomaly flags; plan validation |

## 5. Progress log

Add new entries at the top. Record facts, not intentions.

### 15 November 2026 — Documentation baseline

- Created a structured project documentation set covering PRD, architecture, UX, product and engineering rules, task backlog, progress, data model, API contract, test plan, decisions and hackathon demo.
- Confirmed software-only project scope.
- Confirmed synthetic data for the hackathon prototype unless an authorized dataset becomes available.
- No application implementation or clinical validation is claimed by this entry.

## 6. Weekly review template

Copy this section for each review:

```markdown
### YYYY-MM-DD — Review

**Completed:**
- [ ] Task ID — evidence/link

**In progress:**
- Task ID — owner — expected next step

**Blocked:**
- Task ID — blocker — action to unblock

**Decisions made:**
- Decision and reason

**Risks:**
- New or changed risk

**Next review goals:**
- [ ] Goal 1
- [ ] Goal 2
```

## 7. Release checklist

Before calling a build “hackathon MVP ready”:

- [ ] All screens clearly label synthetic data.
- [ ] Astronaut role cannot access another astronaut's data.
- [ ] Clinician role can only access assigned cases in the demo.
- [ ] Observations include timestamp, unit, source and data status.
- [ ] The alert explanation links to actual input records.
- [ ] Clinician recommendations are distinct from AI summaries.
- [ ] Astronaut acknowledgement is recorded.
- [ ] Offline/queued state is not falsely shown as delivered.
- [ ] Audit events are generated for key actions.
- [ ] Error, empty and loading states are usable.
- [ ] Demo data can be reset and the story repeated.
- [ ] Presentation claims match the working prototype.
