# 11 — Hackathon Demonstration Plan

**Purpose:** Demonstrate a complete, credible software workflow in a short pitch.  
**Data policy:** All example records in this scenario are fictional and synthetic.

## 1. Demo story

**Scenario:** A fictional astronaut, Alex Demo, submits a symptom check-in. ASTROVITAL X organizes the available synthetic health observations, highlights a pattern using a clearly labelled demo rule, routes the case to a ground medical expert, and records the clinician's follow-up request.

This scenario demonstrates workflow capability only. It is not a medical simulation and does not establish clinical performance.

## 2. Demo roles

- Astronaut: `alex.demo`
- Flight surgeon: `doctor.demo`
- Administrator: `admin.demo`

Use temporary demo credentials managed outside the public repository. Do not include production-like passwords in slides or source control.

## 3. Synthetic case contents

Profile:
- Astronaut alias: Alex Demo
- Profile ID: `astro_demo_01`
- Data status: Synthetic demonstration data

Example observations:

| Observation | Example value | Unit | Source label |
|---|---:|---|---|
| Heart rate | 82 | beats/min | Synthetic demo feed |
| SpO₂ | 97 | % | Synthetic demo feed |
| Sleep duration | 5.5 | hours over stated sleep window | Synthetic demo log |
| Blood pressure | 118/76 | mmHg | Synthetic demo record |

These numbers are fictional interface examples, not recommended clinical thresholds or a diagnosis. Include timestamps and show data quality on screen.

Example symptom report:
- Symptoms: dizziness and fatigue
- Trend: unchanged
- Description: “Synthetic scenario for demonstration.”

## 4. Demo sequence (4–6 minutes)

### Part 1 — Introduce the software-only scope (30 seconds)

Say: “ASTROVITAL X does not build new medical hardware. It organizes data already produced by authorized medical systems, astronaut check-ins and health records, then connects AI-assisted review with ground medical professionals.”

### Part 2 — Astronaut portal (60 seconds)

- Sign in as Alex Demo.
- Show the profile and timeline.
- Point out source labels, units, timestamps and synthetic-data banner.
- Submit the fictional symptom check-in.

### Part 3 — AI/data review (60 seconds)

- Show the case summary.
- Show the demo alert and the observations that triggered it.
- Explain: “This is a transparent software rule on synthetic data, not a clinical diagnosis or validated prediction.”

### Part 4 — Ground medical dashboard (90 seconds)

- Switch to the flight surgeon account.
- Open the new case.
- Review available observations and data-quality details.
- Acknowledge the alert or request more information.
- Create a clinician-authored follow-up recommendation.

### Part 5 — Astronaut follow-up (60 seconds)

- Return to the astronaut portal.
- Show the recommendation.
- Acknowledge it and submit a follow-up response.
- Show the updated case and audit history.

### Part 6 — Offline mode (30 seconds)

- Toggle the demo network state to offline.
- Submit a permitted message/check-in.
- Show “queued locally — not yet delivered.”
- Restore the simulated connection and show synchronization.

## 5. Judge-facing explanation of novelty

Do not claim that astronaut monitoring, flight surgeons or telemedicine are new. Explain the project's proposed contribution as a coherent software workflow:

- Unified health record and provenance layer.
- Individual baseline and time-based context.
- Explainable anomaly flags and source-linked summaries.
- Ground clinician case review and recommendation workflow.
- Explicit connected/offline message states.

The hackathon value is the integrated workflow and working prototype, not invention of every underlying component.

## 6. Backup plan

If a live service or AI model fails:
- Use pre-seeded synthetic cases.
- Use a deterministic demo rule.
- Use a prepared clinician response.
- Keep screenshots or a short local recording as backup.
- Clearly tell judges which outputs are pre-seeded or simulated.

## 7. Suggested 30-second closing

“ASTROVITAL X does not replace medical experts and does not create another sensor. It makes existing astronaut health information more organized and actionable. Our software connects personalized health history, explainable AI-assisted review, astronauts and ground medical professionals, while clearly handling the communication delays that deep-space missions may face. Our goal is to make expert-supported healthcare more coordinated beyond Earth.”
