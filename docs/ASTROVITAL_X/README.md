# ASTROVITAL X — Project Documentation

**Project type:** Software-only astronaut health intelligence and medical collaboration platform  
**Document set version:** 1.0  
**Baseline date:** 15 November 2026  
**Project maturity:** Concept and hackathon-prototype planning

## Project in one paragraph

ASTROVITAL X is a proposed software platform that organizes health information already collected by authorized spacecraft medical systems, approved monitoring devices, and astronaut self-reports. It creates a longitudinal astronaut health profile, checks data quality, highlights unusual trends for clinical review, and gives authorized ground medical professionals a workspace to review cases and send recommendations. The platform is designed with two operating conditions in mind: connected operations, when data exchange and consultation are available, and communication-constrained operations, when onboard software must continue local recordkeeping and provide only pre-approved, non-diagnostic support.

> **Scope boundary:** ASTROVITAL X does not design, manufacture, or directly operate medical sensors, cameras, wearables, or other hardware. It does not claim to measure vital signs independently. It consumes data from existing authorized systems or clearly labelled synthetic data in the prototype.

## Documentation map

| File | Purpose |
|---|---|
| [`docs/01_PRD.md`](docs/01_PRD.md) | Product requirements, users, scope, user stories and acceptance criteria |
| [`docs/02_ARCHITECTURE.md`](docs/02_ARCHITECTURE.md) | Logical architecture, components, data flows, deployment and resilience |
| [`docs/03_DESIGN_UX.md`](docs/03_DESIGN_UX.md) | UX principles, roles, screens, workflows and interaction design |
| [`docs/04_PRODUCT_AND_ENGINEERING_RULES.md`](docs/04_PRODUCT_AND_ENGINEERING_RULES.md) | Clinical safety, AI, security, privacy, data and engineering rules |
| [`docs/05_TASKS_BACKLOG.md`](docs/05_TASKS_BACKLOG.md) | Phased implementation plan and actionable task backlog |
| [`docs/06_PROGRESS.md`](docs/06_PROGRESS.md) | Honest project status, milestones, blockers and progress log |
| [`docs/07_DATA_MODEL.md`](docs/07_DATA_MODEL.md) | Core entities, fields, provenance and sample synthetic records |
| [`docs/08_API_SPEC.md`](docs/08_API_SPEC.md) | Prototype API routes, payload examples and error conventions |
| [`docs/09_TEST_PLAN.md`](docs/09_TEST_PLAN.md) | Functional, safety, security, AI and offline-mode test plan |
| [`docs/10_DECISIONS_AND_ASSUMPTIONS.md`](docs/10_DECISIONS_AND_ASSUMPTIONS.md) | Architecture decisions, assumptions, open questions and risks |
| [`docs/11_HACKATHON_DEMO.md`](docs/11_HACKATHON_DEMO.md) | Suggested demo story, sample data and judge-facing explanation |

## Recommended reading order

1. Read the PRD to understand what is being built and what is deliberately excluded.
2. Read the architecture and data model before implementation.
3. Agree the product and engineering rules before building AI or clinical workflows.
4. Use the task backlog to divide work between team members.
5. Update the progress file whenever a task changes state.
6. Use the API and test plans to keep frontend, backend and AI work aligned.

## Suggested repository layout

```text
astrovital-x/
├── README.md
├── docs/
│   ├── 01_PRD.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DESIGN_UX.md
│   ├── 04_PRODUCT_AND_ENGINEERING_RULES.md
│   ├── 05_TASKS_BACKLOG.md
│   ├── 06_PROGRESS.md
│   ├── 07_DATA_MODEL.md
│   ├── 08_API_SPEC.md
│   ├── 09_TEST_PLAN.md
│   ├── 10_DECISIONS_AND_ASSUMPTIONS.md
│   └── 11_HACKATHON_DEMO.md
└── src/                  # Application code, to be created by the team
```

## Prototype truth statement

For the hackathon, use synthetic astronaut profiles and synthetic health observations unless the team has a formally authorized, privacy-safe dataset. Label all synthetic values clearly in the interface and demo. A successful prototype demonstrates software workflows, data handling, trend analysis, case review and messaging; it does **not** prove medical accuracy or flight readiness.

## Versioning guidance

- Update the document-set version when scope, requirements, architecture or safety rules materially change.
- Add dated entries to `docs/06_PROGRESS.md` rather than rewriting history.
- Record consequential design choices in `docs/10_DECISIONS_AND_ASSUMPTIONS.md`.
- Keep requirements IDs stable once referenced by tasks or tests.
