# 01 — Product Requirements Document (PRD)

**Product:** ASTROVITAL X  
**Version:** 1.0  
**Status:** Proposed baseline  
**Date:** 15 November 2026

## 1. Executive summary

ASTROVITAL X is a software-only astronaut health intelligence and Earth-to-space medical collaboration platform. It organizes health information from authorized existing sources, creates a longitudinal health profile for each astronaut, detects data-quality issues and potentially concerning patterns, and supports a human-led medical review workflow between astronauts and ground medical professionals.

The product does not build or operate sensors. It does not independently measure heart rate, ECG, oxygen saturation, blood pressure, temperature, hydration, sleep, or mental health. Those values must arrive from an authorized existing data source or be entered by an astronaut or clinician. In the hackathon prototype, synthetic data will be used and visibly labelled.

ASTROVITAL X is a clinical decision-support concept, not an autonomous doctor. AI can organize information and flag patterns for review; qualified medical professionals remain responsible for diagnosis and treatment decisions.

## 2. Problem statement

Astronaut health information may be produced by different monitoring systems, medical records, activity logs and astronaut-reported assessments. Ground medical teams need a coherent way to review this information, understand changes over time, follow up on concerns and communicate guidance. During communication interruptions or long-delay missions, information exchange with Earth may not be immediate.

The project explores whether a unified software workflow can make available astronaut health information more organized, interpretable and actionable while preserving clinician oversight and supporting constrained-connectivity operations.

## 3. Product vision

**Vision:** Help astronauts and authorized medical teams maintain a shared, trustworthy view of astronaut health by connecting existing data, personalized trend analysis and human medical expertise.

**One-line pitch:** ASTROVITAL X connects astronaut health records, onboard AI-assisted analysis and ground medical experts in one software platform.

## 4. Goals

### 4.1 Primary goals

- G1: Provide a unified profile containing available astronaut health records and observations.
- G2: Display the source, timestamp, unit and quality status of every health observation.
- G3: Compare observations with an astronaut's own baseline where enough valid history exists.
- G4: Identify potentially unusual patterns for human review without presenting them as diagnoses.
- G5: Allow authorized ground medical professionals to review cases and record recommendations.
- G6: Allow astronauts to submit symptoms, check-ins, consultation requests and follow-up responses.
- G7: Preserve local access to previously synchronized information during connectivity loss and synchronize queued records later.
- G8: Provide a realistic hackathon prototype using synthetic data without requiring new medical hardware.

### 4.2 Secondary goals

- Support multiple specialist roles and case assignment.
- Summarize health history and consultation events for faster review.
- Provide audit trails for access, edits, alerts and clinical recommendations.
- Make future integration with approved spacecraft data systems possible through documented interfaces.

## 5. Non-goals

The following are explicitly outside the project's current scope:

- Designing, building, procuring or certifying sensors, wearables, cameras, scanners or medical devices.
- Directly measuring physiological values from a laptop, phone or ordinary camera.
- Replacing NASA flight surgeons, physicians, psychologists or other clinical professionals.
- Automatically diagnosing diseases or prescribing medication.
- Automatically changing treatment, spacecraft operations or emergency procedures.
- Claiming that an unvalidated model predicts heart attacks, stroke, dehydration or other specific medical events.
- Claiming NASA endorsement, NASA deployment, flight certification or access to NASA operational systems.
- Assuming that a live video call to Earth is always possible during deep-space missions.
- Using real astronaut medical records in a public demo without formal authorization.

## 6. Target users and roles

| User role | Needs | Main capabilities |
|---|---|---|
| Astronaut / crew member | Understand own available health information, report symptoms, request help and receive instructions | View own profile, submit check-ins, create consultation request, acknowledge guidance, submit follow-up |
| Flight surgeon / primary medical officer | Review crew health, triage incoming concerns and coordinate follow-up | View assigned crew, review records, inspect trends, acknowledge alerts, create recommendations and assign follow-up |
| Specialist clinician | Review a referred case in their specialty | Access only assigned/referral case data, add specialist opinion and questions |
| Biomedical / mission support specialist | Review data quality and technical telemetry context | Inspect source metadata and ingestion status; no clinical decision authority unless separately assigned |
| System administrator | Manage accounts, roles, configuration and audit access | Manage users/roles, data-source configuration, system health and retention settings |
| Evaluator / demo user | Explore a simulated end-to-end workflow | Use seeded synthetic demo accounts and data only |

## 7. Core use cases

### UC-01: View astronaut health profile

1. An authorized user opens an astronaut profile.
2. The system displays available observations, timestamps, source, units and quality markers.
3. The system shows historical trends only where enough data exists.
4. Missing or stale data is clearly identified.

**Acceptance:** A user never sees a synthetic observation presented as a real measurement; each displayed observation has provenance and timestamp metadata.

### UC-02: Submit a symptom check-in

1. The astronaut opens the check-in form.
2. The astronaut selects symptoms, onset, severity and free-text context.
3. The astronaut submits the check-in.
4. The system stores it and creates a case or adds it to an existing open case.
5. The assigned medical team receives an in-app notification when connected.

**Acceptance:** Submission is timestamped, attributed to the submitting user and visible to authorized clinical roles.

### UC-03: Generate an AI-assisted review summary

1. A case contains health observations and a symptom report.
2. The AI service receives only the data permitted for that task.
3. The service produces a structured summary of facts, trends, missing data and possible reasons for review.
4. The system labels the summary as AI-generated and links each factual item to its source record.
5. A clinician reviews, edits or rejects the summary.

**Acceptance:** AI output is not saved as a clinician-authored finding, and unsupported inferences are not presented as facts.

### UC-04: Create and manage a medical alert

1. A rules engine or reviewed model flags a potentially unusual pattern.
2. The system creates an alert with evidence, data-quality status and reason.
3. The assigned medical team acknowledges, dismisses as non-actionable, or escalates the alert.
4. The system records the decision and user.

**Acceptance:** An alert always includes the input observations or rule that triggered it; no alert automatically issues treatment instructions.

### UC-05: Ground clinician reviews case and sends recommendation

1. The clinician opens an assigned case.
2. The clinician reviews health observations, symptom report and AI summary.
3. The clinician records a recommendation using a structured form.
4. The recommendation is marked as clinician-authored, time-stamped and versioned.
5. The astronaut receives it when communication is available.
6. The astronaut acknowledges and can submit requested follow-up information.

**Acceptance:** The clinician's identity, role, timestamp and recommendation history are retained in the audit trail.

### UC-06: Operate during communication interruption

1. The client detects that the remote service is unavailable.
2. It displays the last synchronization time and offline state.
3. Permitted new check-ins and messages are stored in a protected local queue.
4. The interface clearly indicates that a message has not yet reached the ground team.
5. When the connection returns, the client synchronizes queued items and records delivery status.

**Acceptance:** The UI never implies that a queued medical message has been received or read by a clinician before server acknowledgement.

## 8. Functional requirements

Priority definitions: **P0** = required for hackathon MVP; **P1** = important next increment; **P2** = future capability.

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | Users must authenticate before viewing protected astronaut information. | P0 |
| FR-002 | The system must enforce role-based access to astronaut profiles and clinical actions. | P0 |
| FR-003 | The system must display astronaut profile details and available health observations. | P0 |
| FR-004 | Every observation must include source, timestamp, unit, provenance and data-quality status. | P0 |
| FR-005 | The system must support clearly labelled synthetic demo records. | P0 |
| FR-006 | Astronauts must be able to submit symptom check-ins. | P0 |
| FR-007 | Authorized clinicians must be able to view assigned cases. | P0 |
| FR-008 | The system must generate a basic rules-based alert from seeded demo data. | P0 |
| FR-009 | Clinicians must be able to acknowledge, dismiss or escalate an alert with a reason. | P0 |
| FR-010 | Clinicians must be able to create a recommendation and request follow-up. | P0 |
| FR-011 | Astronauts must be able to view and acknowledge clinician recommendations. | P0 |
| FR-012 | The system must maintain an audit record of protected access and clinical actions. | P0 |
| FR-013 | The system must show data freshness and synchronization status. | P0 |
| FR-014 | The system must support a doctor dashboard and astronaut portal. | P0 |
| FR-015 | AI-generated content must be visibly labelled and distinguishable from clinician-authored content. | P0 |
| FR-016 | The system must support historical trend visualization when data is sufficient. | P1 |
| FR-017 | The system should maintain a personal baseline with confidence and minimum-data checks. | P1 |
| FR-018 | The system should include anomaly detection with explainable evidence. | P1 |
| FR-019 | The system should support specialist referrals and case assignment. | P1 |
| FR-020 | The system should queue permitted records during disconnection and sync after reconnection. | P1 |
| FR-021 | The system may generate a source-linked AI case summary. | P1 |
| FR-022 | The system may support secure asynchronous message threads. | P1 |
| FR-023 | The system may integrate with authorized external health-data interfaces. | P2 |
| FR-024 | The system may support approved medical knowledge retrieval with citations. | P2 |
| FR-025 | The system may support validated research models for mission-specific risk estimation. | P2 |

## 9. Non-functional requirements

| ID | Requirement | Target / guidance |
|---|---|---|
| NFR-001 | Security | TLS in transit, encryption at rest, secrets outside source code, least-privilege access |
| NFR-002 | Privacy | Collect minimum necessary data; use synthetic records in the public demo |
| NFR-003 | Auditability | Record user, action, object, timestamp and outcome for sensitive actions |
| NFR-004 | Reliability | Core read/write workflows must return clear success or failure states |
| NFR-005 | Offline resilience | Preserve queued, permitted user submissions and show delivery state |
| NFR-006 | Explainability | Alerts must show why they were raised and which records were used |
| NFR-007 | Accessibility | Keyboard-accessible controls, readable contrast, labels and non-color-only status cues |
| NFR-008 | Interoperability | Use documented, versioned APIs and normalized units |
| NFR-009 | Maintainability | Separate frontend, backend, data, AI and notification modules |
| NFR-010 | Performance | Prototype screens should remain responsive on ordinary development laptops and demo data volumes |
| NFR-011 | Data integrity | Validate ranges, units, timestamps, duplicates and missing values before analysis |
| NFR-012 | Clinical safety | No autonomous diagnosis, prescribing or treatment execution |

## 10. User stories

- US-01: As an astronaut, I want to see my latest available health status so I can understand what information is on record.
- US-02: As an astronaut, I want to report symptoms so that the medical team can review my concern.
- US-03: As a flight surgeon, I want to see my assigned crew's health timelines so I can review changes over time.
- US-04: As a flight surgeon, I want to see why an alert was generated so I can assess its relevance.
- US-05: As a clinician, I want to send a recommendation and follow-up request so the astronaut can act and report back.
- US-06: As a specialist, I want access to a referred case without unrestricted access to unrelated crew records.
- US-07: As a user, I want to know whether the system is offline and whether my message was delivered.
- US-08: As an administrator, I want to review audit events so that access and clinical actions are traceable.

## 11. Hackathon MVP scope

The recommended MVP demonstrates a complete software workflow with synthetic data:

1. Login with demo roles: astronaut, flight surgeon and administrator.
2. Astronaut profile with synthetic observations and clear synthetic-data labels.
3. Health timeline with at least three available indicators.
4. Symptom check-in form.
5. Simple explainable rule-based alert or anomaly flag.
6. Doctor dashboard with case list and detail view.
7. Doctor-authored recommendation and follow-up request.
8. Astronaut view and acknowledgement of recommendation.
9. Audit log and data freshness indicator.
10. Demonstration of offline/queued message state, even if simulated in the prototype.

## 12. MVP acceptance criteria

The MVP is accepted when all of the following can be demonstrated end to end:

- A demo astronaut can sign in and view only their own profile.
- A demo astronaut can submit a symptom check-in.
- A flight surgeon can sign in and see the case for an assigned astronaut.
- The system can show synthetic observations with units, timestamps, source and labels.
- At least one transparent rule can create an alert from a seeded scenario.
- The clinician can acknowledge the alert and record a recommendation.
- The astronaut can view and acknowledge the recommendation.
- The app records key actions in an audit log.
- The interface distinguishes AI-generated, clinician-authored, imported and synthetic information.
- A simulated disconnected state shows that an unsent item is queued, not delivered.

## 13. Success metrics for the prototype

These measure prototype completeness, not clinical performance:

- 100% of demo observations show a source, timestamp and synthetic/real-data status.
- 100% of clinician recommendations show author and timestamp.
- All protected views require authentication in the demo environment.
- The core astronaut-to-clinician workflow completes without manual database edits.
- The alert detail page explains the triggering rule and linked observations.
- Offline queue state is visibly distinguished from server-delivered state.

## 14. Risks and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| No access to real spacecraft medical data | Cannot demonstrate a live operational integration | Use realistic synthetic data; define adapter interfaces; never imply live NASA access |
| Clinical overclaiming | Safety and credibility risk | Use decision-support language; require clinician review; validate any medical model before use |
| Inconsistent units or timestamps | Incorrect trend analysis | Normalize units; store source units; validate timestamps and provenance |
| False alerts | Alert fatigue | Start with transparent demonstration rules; show evidence and confidence; allow clinician disposition |
| Communication delay | Ground response may not be immediate | Queue data; show delivery status; maintain approved onboard guidance |
| Privacy exposure | Sensitive medical information could be disclosed | Minimize data, enforce roles, encrypt, audit and use synthetic demo data |
| AI hallucination | Misleading summary or guidance | Restrict AI to source-grounded summaries; cite records; prohibit autonomous treatment advice |

## 15. Dependencies and assumptions

- The prototype has no direct connection to NASA or any operational spacecraft system.
- Real data access would require authorization, interface agreements, security review and clinical governance.
- Health observations are supplied by existing authorized systems or human entry; ASTROVITAL X is not a measurement device.
- Synthetic data will be used for public demonstrations.
- Medical thresholds and clinical workflows must be defined or approved by qualified spaceflight medical professionals before operational use.
- Connectivity and response times vary by mission distance, network availability and operational constraints.
