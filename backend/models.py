from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(30), index=True)
    astronaut_id: Mapped[str | None] = mapped_column(String(40), nullable=True)


class AstronautProfile(Base):
    __tablename__ = "astronaut_profiles"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), unique=True)
    mission_alias: Mapped[str] = mapped_column(String(120))
    mission_context: Mapped[str] = mapped_column(String(160))
    assigned_clinician_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)


class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    data_type: Mapped[str] = mapped_column(String(40), index=True)
    value_numeric: Mapped[float | None] = mapped_column(Float, nullable=True)
    value_text: Mapped[str | None] = mapped_column(String(80), nullable=True)
    unit: Mapped[str] = mapped_column(String(32))
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    source_name: Mapped[str] = mapped_column(String(120))
    quality_status: Mapped[str] = mapped_column(String(32))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)


class SymptomCheckIn(Base):
    __tablename__ = "symptom_checkins"
    __table_args__ = (UniqueConstraint("client_submission_id", name="uq_checkin_submission"),)

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    submitted_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    symptoms: Mapped[str] = mapped_column(Text)
    severity: Mapped[int] = mapped_column(Integer)
    trend: Mapped[str] = mapped_column(String(24))
    description: Mapped[str] = mapped_column(Text, default="")
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    client_submission_id: Mapped[str] = mapped_column(String(100))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)


class MedicalCase(Base):
    __tablename__ = "medical_cases"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"), index=True)
    assigned_clinician_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    checkin_id: Mapped[str | None] = mapped_column(ForeignKey("symptom_checkins.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(32), index=True)
    priority: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("medical_cases.id"), index=True)
    astronaut_id: Mapped[str] = mapped_column(ForeignKey("astronaut_profiles.id"))
    title: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(32), index=True)
    priority: Mapped[str] = mapped_column(String(32))
    rule_version: Mapped[str] = mapped_column(String(40))
    explanation: Mapped[str] = mapped_column(Text)
    evidence_ids: Mapped[str] = mapped_column(Text)
    disposition_reason: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    disposed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_demo_only: Mapped[bool] = mapped_column(Boolean, default=True)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    case_id: Mapped[str] = mapped_column(ForeignKey("medical_cases.id"), index=True)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    recommendation_type: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    follow_up_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    acknowledged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class FollowUpResponse(Base):
    __tablename__ = "followup_responses"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    recommendation_id: Mapped[str] = mapped_column(ForeignKey("recommendations.id"), index=True)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(80), index=True)
    object_type: Mapped[str] = mapped_column(String(40))
    object_id: Mapped[str] = mapped_column(String(40))
    outcome: Mapped[str] = mapped_column(String(20))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
