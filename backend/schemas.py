from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)


class CheckInRequest(BaseModel):
    client_submission_id: str = Field(min_length=1, max_length=100)
    symptoms: list[str] = Field(min_length=1, max_length=8)
    severity: int = Field(ge=1, le=5)
    trend: Literal["improving", "unchanged", "worsening", "unknown"]
    description: str = Field(default="", max_length=1000)


class SyncRequest(BaseModel):
    items: list[CheckInRequest] = Field(max_length=10)


class RecommendationRequest(BaseModel):
    case_id: str = Field(min_length=1, max_length=40)
    recommendation_type: Literal["information_request", "follow_up", "consultation"]
    content: str = Field(min_length=10, max_length=1200)
    follow_up_due_at: datetime | None = None


class DispositionRequest(BaseModel):
    action: Literal["acknowledged", "dismissed", "escalated"]
    reason: str = Field(default="", max_length=500)


class FollowUpRequest(BaseModel):
    content: str = Field(min_length=2, max_length=1000)
