# 09 — Test Plan and Quality Strategy

**Version:** 1.0  
**Status:** Proposed; tests not yet executed

## 1. Testing objectives

- Confirm the software-only workflow works end to end.
- Verify data provenance, unit and timestamp handling.
- Verify authorization and role separation.
- Ensure AI findings are explainable and distinguishable from clinical decisions.
- Ensure offline states are accurately represented.
- Prevent the demo from implying that synthetic values are real measurements.

## 2. Test levels

| Test level | Coverage |
|---|---|
| Unit tests | Validators, unit conversion, status logic, baseline calculations, alert rules |
| API tests | Authentication, authorization, validation, CRUD and error responses |
| Integration tests | Astronaut check-in through clinician review and recommendation |
| UI tests | Main role-specific journeys, empty/loading/error states and accessibility |
| Security tests | Broken access control, session handling, input validation and audit behaviour |
| AI/data tests | Source grounding, missing data, model versioning, false-positive review and drift checks |
| Resilience tests | Disconnection, retry, duplicate submission and sync conflict handling |
| Demo regression | Repeatable seeded scenario from clean reset |

## 3. Functional test cases

| ID | Scenario | Expected result |
|---|---|---|
| TC-001 | Astronaut logs in | Astronaut portal opens and own profile is shown |
| TC-002 | Astronaut requests another astronaut profile | Server returns unauthorized/not found without leaking record details |
| TC-003 | Clinician opens assigned astronaut | Profile and observations are visible |
| TC-004 | Clinician opens unassigned astronaut | Access denied unless explicitly authorized |
| TC-005 | Astronaut submits symptom check-in | Check-in is stored with author and timestamp |
| TC-006 | Check-in creates a case | Case appears in assigned clinician queue |
| TC-007 | Observation has no unit where unit is required | Validation rejects or quarantines record |
| TC-008 | Observation has old observed_at timestamp | UI identifies it as stale according to configured demo policy |
| TC-009 | Demo rule detects seeded pattern | Alert appears with explanation and evidence links |
| TC-010 | Clinician acknowledges alert | Status and audit event update |
| TC-011 | Clinician dismisses alert without required reason | Server rejects request |
| TC-012 | Clinician sends recommendation | Recommendation is clinician-authored and visible to astronaut |
| TC-013 | Astronaut acknowledges recommendation | Acknowledgement is timestamped and visible to clinician |
| TC-014 | User views AI summary | AI label and source links are visible |
| TC-015 | User views synthetic data | Persistent synthetic-data label is visible |
| TC-016 | Network is unavailable | New eligible message shows queued locally, not delivered |
| TC-017 | Network returns | Queue item syncs once; duplicate retry does not create duplicate case event |
| TC-018 | User logs out | Protected pages require authentication again |

## 4. AI and analytics tests

- Verify the model/rule version is stored with each finding.
- Verify findings point to the observation IDs used.
- Verify missing values are not treated as normal values.
- Verify incompatible units are not compared.
- Verify a small sample size does not produce a confident personal baseline.
- Verify synthetic data remains labelled synthetic after processing and charting.
- Verify the AI summary does not invent a diagnosis, medication or treatment instruction.
- Verify a summary says “insufficient information” where source data is missing.
- Test false positives and false negatives on a held-out synthetic test set; do not treat those metrics as clinical validation.

## 5. Security and privacy tests

- Astronaut cannot access another astronaut's records by changing URL or API ID.
- Specialist can access only referred or assigned cases.
- Admin role does not automatically receive clinical permissions.
- Unauthenticated calls to protected APIs are rejected.
- Sensitive actions create audit events.
- Application logs do not contain symptom descriptions or unnecessary health values.
- Invalid input cannot inject executable content into the UI.
- Credentials are not present in the repository.
- Demo database contains only synthetic records.

## 6. Offline and synchronization tests

1. Open the astronaut portal while connected and record sync time.
2. Simulate network loss.
3. Submit a symptom check-in.
4. Verify the item is stored locally and shows “queued locally.”
5. Verify no clinician-side delivered notification appears yet.
6. Restore connectivity.
7. Synchronize the queue.
8. Verify one server-side record is created.
9. Retry the same item.
10. Verify idempotency prevents duplicate records.
11. Verify the UI updates to submitted/delivered only after server confirmation.

## 7. Usability and accessibility tests

- Complete primary workflows using keyboard only.
- Confirm all form controls have labels.
- Confirm alert state includes text and icon, not color alone.
- Verify chart labels and units are readable.
- Verify synthetic, stale and AI-generated markers are visible.
- Verify error messages explain how to recover without exposing private details.

## 8. Demo acceptance run

The demo is ready when the team can perform the following without direct database edits:

1. Reset seeded demo data.
2. Sign in as astronaut.
3. Review the synthetic health profile.
4. Submit a symptom check-in.
5. Switch to the clinician role.
6. Open the generated case and related alert.
7. Review source observations and AI/rule explanation.
8. Send a clinician-authored recommendation.
9. Return to astronaut role and acknowledge it.
10. Show audit history and simulated offline/queued state.

## 9. Clinical validation is separate

Passing this software test plan does not establish medical accuracy, clinical safety, flight readiness or regulatory compliance. Any operational clinical model or workflow needs appropriately designed validation, qualified medical review, mission-system approval and relevant regulatory/security assessment.
