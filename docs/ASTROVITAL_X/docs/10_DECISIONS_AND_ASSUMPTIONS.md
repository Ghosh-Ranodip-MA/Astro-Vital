# 10 — Decisions, Assumptions, Open Questions and Risks

**Version:** 1.0  
**Status:** Initial decision log

## 1. Architecture Decision Records (ADRs)

### ADR-001 — Software-only product scope

**Status:** Accepted  
**Decision:** ASTROVITAL X will not design, build or operate hardware or measurement devices. It will consume authorized existing data, user-entered information and synthetic demo data.  
**Reason:** This keeps the hackathon scope achievable and differentiates the proposed product at the software integration, intelligence and clinical workflow layers.  
**Consequence:** The platform cannot claim to measure a vital sign by itself. Data-source integration and provenance are core capabilities.

### ADR-002 — Human clinician remains responsible for clinical decisions

**Status:** Accepted  
**Decision:** AI is used for data organization, trend analysis and review support only. Clinical decisions remain with authorized medical professionals and mission protocols.  
**Reason:** Medical safety, accountability and reliability.  
**Consequence:** The product needs clear clinician review and recommendation workflows.

### ADR-003 — Synthetic data for hackathon demonstration

**Status:** Accepted  
**Decision:** Use generated fictional astronaut data unless the team has a formally authorized dataset.  
**Reason:** No real astronaut medical data access is assumed.  
**Consequence:** Synthetic-data labels must appear in the UI, chart exports and presentation.

### ADR-004 — Connected and communication-constrained operation

**Status:** Accepted  
**Decision:** Design for connected synchronization and local queued operation during communication loss.  
**Reason:** Deep-space communication cannot be assumed to be continuous or low-latency.  
**Consequence:** Delivery states and last synchronization time must be explicit.

### ADR-005 — Modular source adapters

**Status:** Accepted  
**Decision:** External data integrations use source-specific adapters that normalize data into a common schema.  
**Reason:** No specific spacecraft API or partner interface is currently available.  
**Consequence:** The prototype uses a synthetic fixture adapter; real adapters are future authorized work.

### ADR-006 — Start with transparent rules before advanced prediction

**Status:** Accepted  
**Decision:** MVP uses deterministic, explainable demo rules. Advanced anomaly detection is an optional later increment.  
**Reason:** A small demo dataset cannot establish reliable clinical predictive performance.  
**Consequence:** Pitch the MVP as early pattern flagging/review support, not validated medical prediction.

## 2. Assumptions

- The target is a software prototype for a hackathon and a possible research project.
- The product is not currently deployed in space.
- No formal NASA affiliation, endorsement, data access or integration is assumed.
- Existing spacecraft medical systems or data sources would provide any real physiological observations.
- Synthetic data is acceptable for demonstrating application flow and software logic.
- Medical experts would define or approve operational workflows and thresholds.
- The ground medical team may not be reachable immediately during long-delay or disrupted communications.
- Real deployment would require mission-operator approval, cybersecurity engineering, medical governance and appropriate validation.

## 3. Open questions for the team

1. Which frontend framework will the team use: React or Next.js?
2. Which backend will be used: FastAPI or another framework?
3. Will the hackathon demo use PostgreSQL or a simple local SQLite database?
4. How many demo roles and astronaut profiles are needed?
5. Which three data types will be shown in the first dashboard?
6. Will the prototype include an LLM summary, or should it use deterministic templates only?
7. How will the team simulate offline mode: browser queue, mock network toggle or a test harness?
8. Who owns the synthetic scenario and the demo script?
9. Which clinician/advisor can review terminology and workflow assumptions?
10. What authorization and interface requirements would apply to a future real data source?

## 4. Risk register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---:|---:|---|
| R-01 | Judges assume the app measures vital signs itself | Medium | High | Repeat software-only scope on slides and in UI |
| R-02 | Judges challenge novelty because NASA has related systems | High | Medium | Present integration and prototype contribution accurately; do not claim individual components are new |
| R-03 | AI output is mistaken for medical diagnosis | Medium | High | Labels, clinician approval, safety rules and constrained outputs |
| R-04 | No real data access | High | Medium | Use labelled synthetic data and adapter abstraction |
| R-05 | Demo alert seems medically authoritative | Medium | High | Mark demo rules as non-clinical and avoid real treatment advice |
| R-06 | Offline workflow misrepresents delivery | Medium | High | Separate queued, delivered, viewed and acknowledged statuses |
| R-07 | Unauthorized user sees another astronaut's records | Medium | High | Server-side authorization tests and least privilege |
| R-08 | Inconsistent unit/time data corrupts trends | Medium | High | Normalization, provenance and validation |
| R-09 | Overly broad hackathon scope prevents a working demo | High | Medium | Prioritize the end-to-end astronaut-to-doctor workflow |

## 5. Claims discipline

Allowed claims:
- “We propose a software platform that integrates existing authorized health information.”
- “The prototype flags unusual patterns in synthetic demonstration data.”
- “The platform supports a human-reviewed medical workflow.”
- “The architecture is designed to handle delayed or intermittent synchronization.”

Do not claim without evidence:
- “NASA uses or has approved ASTROVITAL X.”
- “The system measures astronaut vitals without sensors.”
- “The AI predicts heart attacks or diagnoses dehydration.”
- “The platform provides guaranteed real-time doctor consultation from Mars.”
- “The prototype is clinically validated, radiation hardened or flight certified.”

## 6. Change-control template

```markdown
### Change request: CR-XXX
- Requested by:
- Date:
- Change:
- Reason:
- Requirements affected:
- Architecture/design impact:
- Safety/privacy impact:
- Decision: Accepted / Rejected / Deferred
- Approver:
```
