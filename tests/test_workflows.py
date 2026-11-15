def sign_in(client, username):
    response = client.post("/api/login", json={"username": username})
    assert response.status_code == 200
    return response


def test_health_and_role_protected_dashboard(client):
    assert client.get("/api/health").json() == {"status": "ok", "database": "connected"}
    assert client.get("/api/dashboard").status_code == 401
    assert client.get("/api/me").json() == {"user": None}

    sign_in(client, "alex.demo")
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["profile"]["name"] == "Alex Demo"
    assert len(data["observations"]) == 9
    assert all(item["isSynthetic"] for item in data["observations"])
    assert data["observations"][0]["observedAt"].endswith("+00:00")
    assert data["cases"][0]["alerts"][0]["evidenceIds"]


def test_symptom_checkin_creates_clinician_assigned_case_and_is_idempotent(client):
    sign_in(client, "alex.demo")
    payload = {
        "client_submission_id": "offline-demo-1",
        "symptoms": ["dizziness", "fatigue"],
        "severity": 3,
        "trend": "unchanged",
        "description": "Synthetic test scenario.",
    }
    created = client.post("/api/check-ins", json=payload)
    assert created.status_code == 201
    assert created.json()["deliveryStatus"] == "delivered"
    duplicate = client.post("/api/sync/check-ins", json={"items": [payload]})
    assert duplicate.status_code == 200
    assert duplicate.json()["results"][0]["duplicate"] is True

    client.post("/api/logout")
    sign_in(client, "doctor.demo")
    cases = client.get("/api/dashboard").json()["cases"]
    checkin_case = next(item for item in cases if item["checkIn"])
    assert checkin_case["checkIn"]["symptoms"] == ["dizziness", "fatigue"]
    assert checkin_case["status"] == "new"


def test_analysis_alert_disposition_and_role_enforcement(client):
    sign_in(client, "alex.demo")
    client.post("/api/check-ins", json={
        "client_submission_id": "analysis-dedup-checkin",
        "symptoms": ["fatigue"],
        "severity": 1,
        "trend": "unchanged",
    })
    forbidden = client.post("/api/analysis/evaluate", json={})
    assert forbidden.status_code == 403
    client.post("/api/logout")
    sign_in(client, "doctor.demo")

    analysis = client.post("/api/analysis/evaluate", json={})
    assert analysis.status_code == 200
    assert analysis.json()["notADiagnosis"] is True
    assert len(analysis.json()["finding"]["evidenceIds"]) == 6
    repeated = client.post("/api/analysis/evaluate", json={})
    assert repeated.json()["finding"]["id"] == analysis.json()["finding"]["id"]

    missing_reason = client.post(
        "/api/alerts/alert_demo_001/disposition",
        json={"action": "dismissed", "reason": ""},
    )
    assert missing_reason.status_code == 400
    acknowledged = client.post(
        "/api/alerts/alert_demo_001/disposition",
        json={"action": "acknowledged"},
    )
    assert acknowledged.status_code == 200
    assert acknowledged.json()["alert"]["status"] == "acknowledged"


def test_clinician_recommendation_and_astronaut_followup_round_trip(client):
    sign_in(client, "doctor.demo")
    created = client.post("/api/recommendations", json={
        "case_id": "case_demo_001",
        "recommendation_type": "information_request",
        "content": "Please share an update with the medical team.",
    })
    assert created.status_code == 201
    recommendation = created.json()["recommendation"]
    assert recommendation["authorUserId"] == "user_clinician_demo"

    client.post("/api/logout")
    sign_in(client, "alex.demo")
    not_acknowledged = client.post(
        f"/api/recommendations/{recommendation['id']}/follow-up",
        json={"content": "I have completed the requested follow-up."},
    )
    assert not_acknowledged.status_code == 409
    acknowledged = client.post(f"/api/recommendations/{recommendation['id']}/acknowledgement")
    assert acknowledged.status_code == 200
    response = client.post(
        f"/api/recommendations/{recommendation['id']}/follow-up",
        json={"content": "I have completed the requested follow-up."},
    )
    assert response.status_code == 201

    client.post("/api/logout")
    sign_in(client, "doctor.demo")
    case = client.get("/api/cases/case_demo_001").json()["case"]
    assert case["recommendations"][0]["status"] == "completed"
    assert case["recommendations"][0]["followUps"][0]["content"] == "I have completed the requested follow-up."


def test_admin_can_reset_but_cannot_access_clinical_dashboard(client):
    sign_in(client, "doctor.demo")
    assert client.post("/api/demo/reset").status_code == 403
    client.post("/api/logout")
    sign_in(client, "admin.demo")
    dashboard = client.get("/api/dashboard").json()
    assert dashboard["summary"]["cases"] == 1
    assert client.post("/api/demo/reset").status_code == 200
    assert client.get("/api/dashboard").json()["summary"]["cases"] == 1
