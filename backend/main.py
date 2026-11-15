import json
import os
import secrets
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.analysis import evaluate_trend
from backend.database import SessionLocal, engine, get_db
from backend.models import (
    Alert,
    AstronautProfile,
    AuditEvent,
    FollowUpResponse,
    MedicalCase,
    Observation,
    Recommendation,
    SymptomCheckIn,
    User,
    Base,
)
from backend.schemas import (
    CheckInRequest,
    DispositionRequest,
    FollowUpRequest,
    LoginRequest,
    RecommendationRequest,
    SyncRequest,
)
from backend.seed import reset_demo_data, seed_demo_data

SESSIONS: dict[str, tuple[str, datetime]] = {}
SESSION_TTL_SECONDS = 8 * 60 * 60


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_demo_data(db)
    yield
    SESSIONS.clear()


app = FastAPI(
    title="ASTROVITAL X API",
    version="1.0.0",
    description="Synthetic-data astronaut health collaboration hackathon API.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

Db = Annotated[Session, Depends(get_db)]
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def as_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value.astimezone(timezone.utc)


def write_audit(
    db: Session,
    actor: User,
    action: str,
    object_type: str,
    object_id: str,
    outcome: str = "success",
) -> None:
    db.add(AuditEvent(
        id=str(uuid.uuid4()),
        actor_user_id=actor.id,
        action=action,
        object_type=object_type,
        object_id=object_id,
        outcome=outcome,
        occurred_at=utcnow(),
    ))


def get_optional_user(
    db: Db,
    session_token: Annotated[str | None, Cookie(alias="astro_session")] = None,
) -> User | None:
    if not session_token:
        return None
    session = SESSIONS.get(session_token)
    if not session:
        return None
    user_id, expires_at = session
    if expires_at <= utcnow():
        SESSIONS.pop(session_token, None)
        return None
    return db.get(User, user_id)


def require_user(user: Annotated[User | None, Depends(get_optional_user)]) -> User:
    if user is None:
        raise HTTPException(status_code=401, detail={"code": "UNAUTHENTICATED", "message": "Sign in with a demo account to continue."})
    return user


CurrentUser = Annotated[User, Depends(require_user)]


def require_role(user: User, *roles: str) -> None:
    if user.role not in roles:
        raise HTTPException(status_code=403, detail={"code": "FORBIDDEN", "message": "This action is not available for your role."})


def assigned_profile(db: Session, user: User, astronaut_id: str) -> AstronautProfile:
    profile = db.get(AstronautProfile, astronaut_id)
    allowed = profile is not None and (
        (user.role == "astronaut" and profile.user_id == user.id)
        or (user.role in {"flight_surgeon", "specialist"} and profile.assigned_clinician_id == user.id)
    )
    if not allowed:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "The requested profile is not available."})
    return profile


def accessible_case(db: Session, user: User, case_id: str) -> MedicalCase:
    case = db.get(MedicalCase, case_id)
    profile = db.get(AstronautProfile, case.astronaut_id) if case else None
    allowed = case is not None and profile is not None and (
        (user.role == "astronaut" and profile.user_id == user.id)
        or (user.role in {"flight_surgeon", "specialist"} and case.assigned_clinician_id == user.id)
    )
    if not allowed:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "The requested case is not available."})
    return case


def serialize_observation(item: Observation) -> dict:
    return {
        "id": item.id,
        "dataType": item.data_type,
        "value": item.value_numeric if item.value_numeric is not None else item.value_text,
        "unit": item.unit,
        "observedAt": as_utc(item.observed_at),
        "receivedAt": as_utc(item.received_at),
        "source": item.source_name,
        "quality": item.quality_status,
        "isSynthetic": item.is_synthetic,
    }


def serialize_alert(item: Alert) -> dict:
    return {
        "id": item.id,
        "caseId": item.case_id,
        "title": item.title,
        "status": item.status,
        "priority": item.priority,
        "ruleVersion": item.rule_version,
        "explanation": item.explanation,
        "evidenceIds": json.loads(item.evidence_ids),
        "dispositionReason": item.disposition_reason,
        "createdAt": as_utc(item.created_at),
        "isDemoOnly": item.is_demo_only,
    }


def serialize_recommendation(db: Session, item: Recommendation) -> dict:
    author = db.get(User, item.author_user_id)
    responses = db.scalars(
        select(FollowUpResponse)
        .where(FollowUpResponse.recommendation_id == item.id)
        .order_by(FollowUpResponse.created_at.asc())
    ).all()
    return {
        "id": item.id,
        "caseId": item.case_id,
        "authorUserId": item.author_user_id,
        "authorName": author.display_name if author else "Clinician",
        "type": item.recommendation_type,
        "content": item.content,
        "dueAt": as_utc(item.follow_up_due_at),
        "status": item.status,
        "createdAt": as_utc(item.created_at),
        "acknowledgedAt": as_utc(item.acknowledged_at),
        "followUps": [{
            "id": response.id,
            "authorUserId": response.author_user_id,
            "content": response.content,
            "createdAt": as_utc(response.created_at),
        } for response in responses],
    }


def serialize_case(db: Session, item: MedicalCase) -> dict:
    checkin = db.get(SymptomCheckIn, item.checkin_id) if item.checkin_id else None
    alerts = db.scalars(select(Alert).where(Alert.case_id == item.id).order_by(Alert.created_at.desc())).all()
    recommendations = db.scalars(
        select(Recommendation).where(Recommendation.case_id == item.id).order_by(Recommendation.created_at.desc())
    ).all()
    observations = db.scalars(
        select(Observation)
        .where(Observation.astronaut_id == item.astronaut_id)
        .order_by(Observation.observed_at.asc())
    ).all()
    checkin_payload = None
    if checkin:
        checkin_payload = {
            "id": checkin.id,
            "symptoms": json.loads(checkin.symptoms),
            "severity": checkin.severity,
            "trend": checkin.trend,
            "description": checkin.description,
            "submittedAt": as_utc(checkin.submitted_at),
            "isSynthetic": checkin.is_synthetic,
        }
    return {
        "id": item.id,
        "astronautId": item.astronaut_id,
        "title": item.title,
        "status": item.status,
        "priority": item.priority,
        "createdAt": as_utc(item.created_at),
        "checkIn": checkin_payload,
        "alerts": [serialize_alert(alert) for alert in alerts],
        "recommendations": [serialize_recommendation(db, recommendation) for recommendation in recommendations],
        "observations": [serialize_observation(observation) for observation in observations],
    }


def create_checkin(db: Session, user: User, body: CheckInRequest) -> tuple[MedicalCase, bool]:
    existing = db.scalar(
        select(SymptomCheckIn).where(SymptomCheckIn.client_submission_id == body.client_submission_id)
    )
    if existing:
        existing_case = db.scalar(select(MedicalCase).where(MedicalCase.checkin_id == existing.id))
        if not existing_case or existing.astronaut_id != user.astronaut_id:
            raise HTTPException(status_code=409, detail={"code": "IDEMPOTENCY_CONFLICT", "message": "Submission ID is already in use."})
        return existing_case, True
    profile = db.scalar(select(AstronautProfile).where(AstronautProfile.user_id == user.id))
    if not profile:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "Astronaut profile is unavailable."})
    checkin = SymptomCheckIn(
        id=str(uuid.uuid4()),
        astronaut_id=profile.id,
        submitted_by_user_id=user.id,
        symptoms=json.dumps(body.symptoms),
        severity=body.severity,
        trend=body.trend,
        description=body.description,
        submitted_at=utcnow(),
        client_submission_id=body.client_submission_id,
        is_synthetic=True,
    )
    db.add(checkin)
    db.flush()
    case = MedicalCase(
        id=str(uuid.uuid4()),
        astronaut_id=profile.id,
        assigned_clinician_id=profile.assigned_clinician_id,
        checkin_id=checkin.id,
        title=f"Symptom check-in: {', '.join(body.symptoms)}",
        status="new",
        priority="review",
        created_at=utcnow(),
    )
    db.add(case)
    db.flush()
    write_audit(db, user, "check_in_submitted", "case", case.id)
    return case, False


@app.get("/api/health")
def health_check(db: Db):
    db.execute(select(1))
    return {"status": "ok", "database": "connected"}


@app.get("/api/me")
def get_me(user: Annotated[User | None, Depends(get_optional_user)]):
    if user is None:
        return {"user": None}
    return {"user": {"id": user.id, "name": user.display_name, "role": user.role}}


@app.post("/api/login")
def login(body: LoginRequest, response: Response, db: Db):
    user = db.scalar(select(User).where(User.username == body.username.lower()))
    if not user:
        raise HTTPException(status_code=401, detail={"code": "INVALID_DEMO_USER", "message": "Choose one of the listed demo accounts."})
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = (user.id, utcnow() + timedelta(seconds=SESSION_TTL_SECONDS))
    response.set_cookie(
        "astro_session",
        token,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
        path="/",
    )
    write_audit(db, user, "signed_in", "session", user.id)
    db.commit()
    return {"user": {"id": user.id, "name": user.display_name, "role": user.role}}


@app.post("/api/logout")
def logout(
    response: Response,
    db: Db,
    session_token: Annotated[str | None, Cookie(alias="astro_session")] = None,
    user: Annotated[User | None, Depends(get_optional_user)] = None,
):
    if session_token:
        SESSIONS.pop(session_token, None)
    if user:
        write_audit(db, user, "signed_out", "session", user.id)
        db.commit()
    response.delete_cookie("astro_session", path="/", httponly=True, samesite="lax")
    return {"ok": True}


@app.get("/api/dashboard")
def dashboard(db: Db, user: CurrentUser):
    if user.role == "admin":
        events = db.scalars(select(AuditEvent).order_by(AuditEvent.occurred_at.desc()).limit(100)).all()
        return {
            "role": user.role,
            "summary": {
                "accounts": db.query(User).count(),
                "cases": db.query(MedicalCase).count(),
                "auditEvents": db.query(AuditEvent).count(),
            },
            "audit": [{
                "id": event.id,
                "actorName": (db.get(User, event.actor_user_id).display_name if event.actor_user_id else "System"),
                "role": (db.get(User, event.actor_user_id).role if event.actor_user_id else "system"),
                "action": event.action,
                "objectType": event.object_type,
                "objectId": event.object_id,
                "outcome": event.outcome,
                "occurredAt": as_utc(event.occurred_at),
            } for event in events],
        }
    require_role(user, "astronaut", "flight_surgeon", "specialist")
    if user.role == "astronaut":
        profile = db.scalar(select(AstronautProfile).where(AstronautProfile.user_id == user.id))
    else:
        profile = db.scalar(select(AstronautProfile).where(AstronautProfile.assigned_clinician_id == user.id))
    if not profile:
        return {"role": user.role, "cases": [], "observations": [], "profile": None}
    write_audit(db, user, "profile_viewed", "astronaut_profile", profile.id)
    db.commit()
    observations = db.scalars(
        select(Observation).where(Observation.astronaut_id == profile.id).order_by(Observation.observed_at.asc())
    ).all()
    cases = db.scalars(
        select(MedicalCase)
        .where(
            MedicalCase.astronaut_id == profile.id if user.role == "astronaut"
            else MedicalCase.assigned_clinician_id == user.id
        )
        .order_by(MedicalCase.created_at.desc())
    ).all()
    return {
        "role": user.role,
        "profile": {
            "id": profile.id,
            "name": profile.mission_alias,
            "mission": profile.mission_context,
            "status": "Synthetic demonstration profile",
            "isSynthetic": profile.is_synthetic,
        },
        "observations": [serialize_observation(observation) for observation in observations],
        "cases": [serialize_case(db, case) for case in cases],
        "lastSyncAt": as_utc(utcnow()),
    }


@app.get("/api/cases/{case_id}")
def get_case(case_id: str, db: Db, user: CurrentUser):
    case = accessible_case(db, user, case_id)
    write_audit(db, user, "case_viewed", "medical_case", case.id)
    db.commit()
    return {"case": serialize_case(db, case)}


@app.post("/api/check-ins", status_code=status.HTTP_201_CREATED)
def submit_checkin(body: CheckInRequest, db: Db, user: CurrentUser):
    require_role(user, "astronaut")
    case, duplicate = create_checkin(db, user, body)
    db.commit()
    return {"ok": True, "caseId": case.id, "duplicate": duplicate, "deliveryStatus": "delivered"}


@app.post("/api/sync/check-ins")
def sync_checkins(body: SyncRequest, db: Db, user: CurrentUser):
    require_role(user, "astronaut")
    results = []
    for item in body.items:
        case, duplicate = create_checkin(db, user, item)
        results.append({
            "clientSubmissionId": item.client_submission_id,
            "caseId": case.id,
            "duplicate": duplicate,
            "deliveryStatus": "delivered",
        })
    db.commit()
    return {"ok": True, "results": results, "serverReceivedAt": utcnow()}


@app.post("/api/analysis/evaluate")
def run_analysis(db: Db, user: CurrentUser):
    require_role(user, "flight_surgeon")
    profile = db.scalar(select(AstronautProfile).where(AstronautProfile.assigned_clinician_id == user.id))
    if not profile:
        return {"status": "insufficient_data", "finding": None}
    observations = db.scalars(
        select(Observation).where(Observation.astronaut_id == profile.id).order_by(Observation.observed_at.asc())
    ).all()
    finding = evaluate_trend(observations)
    if not finding:
        return {"status": "insufficient_data", "finding": None}
    case = db.scalar(
        select(MedicalCase)
        .where(MedicalCase.astronaut_id == profile.id, MedicalCase.status != "closed")
        .order_by(MedicalCase.created_at.desc())
    )
    if not case:
        case = MedicalCase(
            id=str(uuid.uuid4()),
            astronaut_id=profile.id,
            assigned_clinician_id=user.id,
            title="Synthetic trend review",
            status="under_review",
            priority="review",
            created_at=utcnow(),
        )
        db.add(case)
        db.flush()
    existing_alerts = db.scalars(
        select(Alert).where(
            Alert.astronaut_id == profile.id,
            Alert.rule_version == finding["rule_version"],
        )
    ).all()
    evidence_ids = json.dumps(finding["evidence_ids"])
    alert = next((item for item in existing_alerts if item.evidence_ids == evidence_ids), None)
    if not alert:
        alert = Alert(
            id=str(uuid.uuid4()),
            case_id=case.id,
            astronaut_id=profile.id,
            title=finding["title"],
            status="new",
            priority="review",
            rule_version=finding["rule_version"],
            explanation=finding["explanation"],
            evidence_ids=json.dumps(finding["evidence_ids"]),
            created_at=utcnow(),
            is_demo_only=True,
        )
        db.add(alert)
        write_audit(db, user, "demo_analysis_flag_created", "alert", alert.id)
    db.commit()
    return {"status": "completed", "finding": serialize_alert(alert), "notADiagnosis": True}


@app.post("/api/alerts/{alert_id}/disposition")
def disposition_alert(alert_id: str, body: DispositionRequest, db: Db, user: CurrentUser):
    require_role(user, "flight_surgeon")
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "The requested alert is not available."})
    case = accessible_case(db, user, alert.case_id)
    if body.action != "acknowledged" and len(body.reason.strip()) < 3:
        raise HTTPException(status_code=400, detail={"code": "VALIDATION_ERROR", "message": "Add a reason before dismissing or escalating."})
    alert.status = body.action
    alert.disposition_reason = body.reason.strip()
    alert.disposed_at = utcnow()
    write_audit(db, user, f"alert_{body.action}", "alert", alert.id)
    db.commit()
    return {"ok": True, "caseId": case.id, "alert": serialize_alert(alert)}


@app.post("/api/recommendations", status_code=status.HTTP_201_CREATED)
def create_recommendation(body: RecommendationRequest, db: Db, user: CurrentUser):
    require_role(user, "flight_surgeon")
    case = accessible_case(db, user, body.case_id)
    recommendation = Recommendation(
        id=str(uuid.uuid4()),
        case_id=case.id,
        author_user_id=user.id,
        recommendation_type=body.recommendation_type,
        content=body.content.strip(),
        follow_up_due_at=as_utc(body.follow_up_due_at),
        status="sent",
        created_at=utcnow(),
    )
    db.add(recommendation)
    case.status = "awaiting_astronaut"
    write_audit(db, user, "recommendation_sent", "recommendation", recommendation.id)
    db.commit()
    db.refresh(recommendation)
    return {"ok": True, "recommendation": serialize_recommendation(db, recommendation)}


@app.post("/api/recommendations/{recommendation_id}/acknowledgement")
def acknowledge_recommendation(recommendation_id: str, db: Db, user: CurrentUser):
    require_role(user, "astronaut")
    recommendation = db.get(Recommendation, recommendation_id)
    case = accessible_case(db, user, recommendation.case_id) if recommendation else None
    if not recommendation or not case:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "The requested recommendation is not available."})
    if recommendation.status != "acknowledged":
        recommendation.status = "acknowledged"
        recommendation.acknowledged_at = utcnow()
        write_audit(db, user, "recommendation_acknowledged", "recommendation", recommendation.id)
    db.commit()
    return {"ok": True, "acknowledgedAt": as_utc(recommendation.acknowledged_at)}


@app.post("/api/recommendations/{recommendation_id}/follow-up", status_code=status.HTTP_201_CREATED)
def submit_followup(recommendation_id: str, body: FollowUpRequest, db: Db, user: CurrentUser):
    require_role(user, "astronaut")
    recommendation = db.get(Recommendation, recommendation_id)
    case = accessible_case(db, user, recommendation.case_id) if recommendation else None
    if not recommendation or not case:
        raise HTTPException(status_code=404, detail={"code": "NOT_FOUND", "message": "The requested recommendation is not available."})
    if recommendation.status not in {"acknowledged", "completed"}:
        raise HTTPException(status_code=409, detail={"code": "CONFLICT", "message": "Acknowledge the recommendation before sending a follow-up response."})
    followup = FollowUpResponse(
        id=str(uuid.uuid4()),
        recommendation_id=recommendation.id,
        author_user_id=user.id,
        content=body.content.strip(),
        created_at=utcnow(),
        is_synthetic=True,
    )
    db.add(followup)
    recommendation.status = "completed"
    case.status = "under_review"
    write_audit(db, user, "followup_submitted", "recommendation", recommendation.id)
    db.commit()
    return {"ok": True, "followUpId": followup.id, "createdAt": as_utc(followup.created_at)}


@app.post("/api/demo/reset")
def reset_demo(db: Db, user: CurrentUser):
    require_role(user, "admin")
    reset_demo_data(db)
    write_audit(db, user, "demo_reset", "dataset", "synthetic-demo")
    db.commit()
    return {"ok": True}
