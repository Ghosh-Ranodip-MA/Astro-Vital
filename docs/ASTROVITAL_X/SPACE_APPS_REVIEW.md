# ASTROVITAL X — Space Apps reviewer assessment

**Review date:** 15 November 2026  
**Target challenge:** [Create Health Monitoring Software for Astronauts on Space Missions](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/)  
**Judging lens:** Impact, Creativity, Validity, Relevance, and Presentation, as stated on the [2026 Space Apps event judging page](https://www.spaceappschallenge.org/2026/local-events/ajmer/).

## Reviewer verdict

ASTROVITAL X is a coherent software prototype for the selected challenge. Its strongest contribution is the end-to-end crew-to-clinician workflow: a crew member sees available records and submits a check-in; a deterministic rule can flag a pattern; a clinician reviews the evidence and sends a follow-up; the crew member can acknowledge and respond. The interface also makes queued versus delivered states explicit.

The submission should not claim medical AI, a validated health assessment, NASA data integration, or operational readiness. The current dataset is entirely synthetic, the analysis is a small fixed rule, and the passwordless accounts and local-storage queue are demonstration mechanisms. The main judging risk is **Validity**: show what the software does, state its limits plainly, and describe how it would be evaluated with authorized data and subject-matter experts.

## Criterion review

| Criterion | Reviewer assessment | What strengthens the submission |
|---|---|---|
| **Impact** | Strong problem relevance for long-duration missions; actual mission benefit is still a proposal. | Explain the need as continuity of health context and asynchronous human follow-up during delayed or interrupted communication. Do not claim reduced medical risk or improved outcomes without evidence. |
| **Creativity** | Individual pieces are familiar; the integrated workflow and explicit delivery states are the useful design contribution. | Demo the complete astronaut → review → clinician → acknowledgement loop. Show how the workflow stays honest when a check-in is queued. Do not claim astronaut monitoring or telemedicine itself is novel. |
| **Validity** | Software behavior is inspectable, but health data and the comparison rule are synthetic and unvalidated. | Use the seeded rule only as an explainability demonstration. Open its evidence links, point out quality and unit filtering, and state the synthetic-data limitation. Make no diagnostic or predictive-performance claims. |
| **Relevance** | Direct fit to the 2026 astronaut health-monitoring challenge. | Name the exact challenge in the submission and opening slide. Explain that crew-facing status, self-report, health context and an action/follow-up loop answer the challenge's request for software that helps astronauts evaluate and act on health indicators. |
| **Presentation** | The prototype supports a clear live story; the distinction between a demo workflow and a deployable system must stay visible. | Use one seeded scenario, switch roles deliberately, and finish with the validation path. Prepare a short screen recording in case local services fail. |

## Findings fixed in this review

1. The clinician dashboard called its deterministic rule “AI health analysis.” It now calls it **Demo trend review**, avoiding a false capability claim.
2. The rule accepted numerical heart-rate values without checking unit, quality, or synthetic status. It now evaluates only records marked synthetic, valid, numeric, and in `beats/min`.
3. Alert evidence IDs were plain text. They now link to and highlight the underlying observation rows.
4. The chart's accessibility description implied only the final two samples were evidence, while the rule uses six. The description and highlighted samples now match the rule inputs.
5. The progress tracker and API spec described the software as unimplemented. They now distinguish the implemented demo from the proposed future design and outstanding validation.

## Remaining gaps that affect judging

- **No real or published health dataset is demonstrated.** Keep the values synthetic. A future study needs authorized data, a documented data dictionary, provenance, quality handling, and domain-expert review.
- **The 20% comparison is a demo-only rule.** It is not sourced from a medical standard and cannot establish risk. Do not describe it as an astronaut health threshold.
- **No AI is implemented.** Avoid “AI-powered” in the submission, interface, and pitch unless a model is later added, evaluated, and separated from clinician decisions.
- **The offline queue is local browser storage.** It demonstrates state transitions only; it is not an approved secure clinical store or resilient spacecraft communications system.
- **Authentication and audit are demo-grade.** Passwordless role selection and process-memory sessions are not suitable for operational use.
- **The displayed workflow is not a substitute for approved emergency procedures or medical care.** Say this plainly in the demo.

## Recommended 4-minute judge demonstration

1. **Problem and fit (20 seconds):** “Long missions need crew to understand the health information already available and coordinate with medical professionals when communication is delayed. This prototype addresses the 2026 astronaut health-monitoring challenge.”
2. **Crew view (45 seconds):** Show the synthetic label, latest observations, timestamps, source and quality labels, and time series. Submit one fictional check-in.
3. **Transparent review (45 seconds):** Switch to the clinician role, open the case, run the trend review, and click an evidence ID to show the exact input row. State that this is a deterministic demo rule on synthetic data.
4. **Human follow-up (60 seconds):** Record a disposition, author a follow-up, return to the crew role, acknowledge it, and send a response.
5. **Communication state (30 seconds):** Queue one check-in in offline simulation, show “not delivered,” reconnect, and show server receipt.
6. **Close with the validation path (20 seconds):** “Next we need authorized representative data, clinician-led requirements, privacy and security review, and prospective evaluation before any operational claim.”

## Suggested submission summary

> ASTROVITAL X is a synthetic-data software prototype for the 2026 “Create Health Monitoring Software for Astronauts on Space Missions” challenge. It brings available health observations, crew self-reports, transparent trend review, and clinician-authored follow-up into one workflow. Its deterministic rule is a demonstration, not medical AI or a clinical threshold. The prototype highlights the evidence behind each flag and distinguishes locally queued check-ins from those received by the service. Real mission data, clinical validation, and operational security are future requirements.

## Source references

- [Official 2026 challenge brief](https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/)
- [NASA Space Apps 2026 event and submission timeline](https://www.spaceappschallenge.org/2026/)
- [2026 local-event judging criteria page](https://www.spaceappschallenge.org/2026/local-events/ajmer/)
