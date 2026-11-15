import json
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from backend.analysis import evaluate_trend
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
)

DEMO_USERS = [
    ("user_astronaut_demo", "alex.demo", "Alex Demo", "astronaut", "astro_demo_01"),
    ("user_clinician_demo", "doctor.demo", "Dr. Maya Chen", "flight_surgeon", None),
    ("user_admin_demo", "admin.demo", "Mission Admin", "admin", None),
]


def seed_demo_data(db: Session) -> None:
    if db.scalar(select(User.id).limit(1)):
        return
    for user_id, username, display_name, role, astronaut_id in DEMO_USERS:
        db.add(User(id=user_id, username=username, display_name=display_name, role=role, astronaut_id=astronaut_id))
    db.flush()
    db.add(AstronautProfile(
        id="astro_demo_01",
        user_id="user_astronaut_demo",
        mission_alias="Alex Demo",
        mission_context="Expedition Demo",
        assigned_clinician_id="user_clinician_demo",
    ))

    now = datetime.now(timezone.utc)
    heart_rates = [62, 64, 61, 63, 82, 84]
    for index, value in enumerate(heart_rates):
        db.add(Observation(
            id=f"obs_hr_{index + 1:02}",
            astronaut_id="astro_demo_01",
            data_type="heart_rate",
            value_numeric=value,
            unit="beats/min",
            observed_at=now - timedelta(hours=(5 - index) * 4),
            received_at=now - timedelta(hours=(5 - index) * 4),
            source_name="Synthetic demo feed",
            quality_status="valid",
            is_synthetic=True,
        ))
    other_observations = [
        ("obs_spo2_01", "spo2", 97, None, "%", 30, "Synthetic demo feed"),
        ("obs_sleep_01", "sleep_duration", 5.5, None, "hours", 45, "Synthetic demo log"),
        ("obs_bp_01", "blood_pressure", None, "118/76", "mmHg", 40, "Synthetic demo record"),
    ]
    for observation_id, data_type, numeric, text, unit, minutes_ago, source in other_observations:
        db.add(Observation(
            id=observation_id,
            astronaut_id="astro_demo_01",
            data_type=data_type,
            value_numeric=numeric,
            value_text=text,
            unit=unit,
            observed_at=now - timedelta(minutes=minutes_ago),
            received_at=now - timedelta(minutes=minutes_ago),
            source_name=source,
            quality_status="valid",
            is_synthetic=True,
        ))
    case = MedicalCase(
        id="case_demo_001",
        astronaut_id="astro_demo_01",
        assigned_clinician_id="user_clinician_demo",
        title="Synthetic trend review",
        status="under_review",
        priority="review",
        created_at=now - timedelta(minutes=20),
    )
    db.add(case)
    db.flush()
    analysis = evaluate_trend(db.scalars(select(Observation).where(Observation.astronaut_id == "astro_demo_01")).all())
    if analysis:
        db.add(Alert(
            id="alert_demo_001",
            case_id=case.id,
            astronaut_id=case.astronaut_id,
            title=analysis["title"],
            status="new",
            priority="review",
            rule_version=analysis["rule_version"],
            explanation=analysis["explanation"],
            evidence_ids=json.dumps(analysis["evidence_ids"]),
            created_at=now - timedelta(minutes=20),
            is_demo_only=True,
        ))
    db.commit()


def reset_demo_data(db: Session) -> None:
    for model in (AuditEvent, FollowUpResponse, Recommendation, Alert, MedicalCase, SymptomCheckIn, Observation, AstronautProfile, User):
        db.execute(delete(model))
    db.commit()
    seed_demo_data(db)
