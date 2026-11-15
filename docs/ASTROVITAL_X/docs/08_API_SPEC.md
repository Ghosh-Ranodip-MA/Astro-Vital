# 08 — API Specification (Prototype)

**Version:** 1.0  
**Status:** Proposed API contract; not implemented by this document

## 1. API conventions

- Base path: `/api/v1`
- Format: JSON over HTTPS in any non-local deployment.
- Authentication: authenticated session or bearer token issued by the configured identity provider.
- Authorization: enforced server-side for every astronaut/case resource.
- Time: ISO 8601 timestamps; use UTC internally unless a mission time standard is explicitly defined.
- IDs: opaque UUIDs or stable string IDs.
- Pagination: cursor-based for larger lists; offset pagination acceptable in a small demo.
- Error response: consistent machine code and human-readable message.
- Do not return hidden records and rely on the UI to hide them.

## 2. Standard error envelope

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You are not authorized to access this resource.",
    "request_id": "req_demo_001"
  }
}
```

Suggested HTTP status usage: `400` validation error, `401` unauthenticated, `403` unauthorized, `404` missing or inaccessible resource, `409` conflict/idempotency mismatch, `422` semantically invalid payload, `429` rate limited, `500` unexpected server error.

## 3. Authentication and profile routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/me` | Current user and role |
| GET | `/astronauts` | List astronauts visible to the current clinician/admin |
| GET | `/astronauts/{astronaut_id}` | View authorized astronaut profile |
| GET | `/astronauts/{astronaut_id}/observations` | Query available observations |
| GET | `/astronauts/{astronaut_id}/timeline` | Get timeline-ready data |
| GET | `/astronauts/{astronaut_id}/cases` | List authorized cases |

### Example: create symptom check-in

`POST /api/v1/astronauts/{astronaut_id}/check-ins`

```json
{
  "symptoms": ["dizziness", "fatigue"],
  "onset_at": "2026-11-14T09:00:00Z",
  "severity_self_reported": 3,
  "trend": "unchanged",
  "description": "Demo scenario text.",
  "client_submission_id": "client-checkin-0001",
  "is_synthetic": true
}
```

Expected response:

```json
{
  "id": "checkin_demo_001",
  "astronaut_id": "astro_demo_01",
  "status": "received",
  "case_id": "case_demo_001",
  "submitted_at": "2026-11-14T09:15:00Z",
  "is_synthetic": true
}
```

## 4. Observations routes

| Method | Route | Purpose |
|---|---|---|
| POST | `/observations` | Ingest an authorized or synthetic observation |
| GET | `/observations/{observation_id}` | Retrieve observation with provenance |
| GET | `/astronauts/{astronaut_id}/observations` | Filter by data type and time range |

### Example observation ingestion

```json
{
  "astronaut_id": "astro_demo_01",
  "data_type": "heart_rate",
  "value_numeric": 82,
  "unit": "beats/min",
  "observed_at": "2026-11-14T08:30:00Z",
  "source_type": "synthetic_demo",
  "source_name": "ASTROVITAL X demonstration fixture",
  "source_record_id": "fixture_hr_001",
  "quality_status": "valid",
  "is_synthetic": true
}
```

The server must validate that the caller can submit data for the subject and that source metadata is allowed. External adapters should use service identities with narrow permissions.

## 5. Cases and alerts routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/cases` | List cases available to current clinician |
| GET | `/cases/{case_id}` | Get case detail and linked information |
| POST | `/cases` | Create a case where role permits |
| PATCH | `/cases/{case_id}` | Update permitted workflow fields |
| GET | `/alerts` | List visible alerts |
| POST | `/alerts/evaluate` | Run demo rules on eligible records |
| POST | `/alerts/{alert_id}/disposition` | Acknowledge, dismiss or escalate |

Example disposition:

```json
{
  "action": "acknowledge",
  "reason": "Reviewed source records and accepted for clinical review.",
  "expected_version": 1
}
```

## 6. Recommendations and follow-up routes

| Method | Route | Purpose |
|---|---|---|
| POST | `/cases/{case_id}/recommendations` | Create clinician-authored recommendation |
| GET | `/cases/{case_id}/recommendations` | List recommendations |
| POST | `/recommendations/{recommendation_id}/acknowledgement` | Astronaut acknowledgement |
| POST | `/recommendations/{recommendation_id}/follow-up` | Submit requested follow-up response |

Example recommendation:

```json
{
  "recommendation_type": "information_request",
  "content": "Please complete the requested follow-up assessment according to the mission medical team's approved procedure.",
  "follow_up_due_at": "2026-11-15T12:00:00Z"
}
```

The API must record the authenticated clinician as author; the client must not be allowed to impersonate a clinician by supplying an arbitrary author ID.

## 7. AI analysis routes

| Method | Route | Purpose |
|---|---|---|
| POST | `/cases/{case_id}/analysis` | Generate a structured, source-linked case summary |
| GET | `/analysis/{analysis_id}` | Retrieve analysis with model/rule version |

Example response:

```json
{
  "id": "analysis_demo_001",
  "case_id": "case_demo_001",
  "status": "completed",
  "model_or_rule_version": "demo-summary-v1",
  "summary": "The synthetic case contains a reported symptom and a change in the supplied synthetic time series.",
  "evidence_observation_ids": ["obs_demo_001", "obs_demo_002"],
  "missing_information": ["No recent blood-pressure observation was supplied."],
  "requires_clinician_review": true,
  "not_a_diagnosis": true,
  "is_synthetic": true
}
```

## 8. Messaging and synchronization routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/cases/{case_id}/messages` | List case messages |
| POST | `/cases/{case_id}/messages` | Submit a message |
| POST | `/sync/batch` | Submit queued local events using idempotency keys |
| GET | `/sync/status` | Return last sync and pending state |

Message example:

```json
{
  "body": "Please review the newly submitted check-in.",
  "recipient_user_id": "user_clinician_demo",
  "client_message_id": "local-msg-0001",
  "idempotency_key": "8d5c1a6b-demo-key",
  "created_at_client": "2026-11-14T09:17:00Z"
}
```

The response must report server receipt separately from recipient view/acknowledgement.

## 9. Audit routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/audit-events` | Authorized audit review |

The API should not expose a general endpoint to edit or delete audit events.

## 10. API security requirements

- Validate schemas on the server.
- Enforce authorization on every route and object.
- Use idempotency keys for retryable create operations.
- Apply pagination and query limits.
- Avoid returning more health data than the caller needs.
- Never include secrets or sensitive health records in error messages or logs.
- Do not expose model prompts, private system details or unrestricted database query access.
- Add request IDs for audit and troubleshooting.
