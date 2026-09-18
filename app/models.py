from typing import Literal
from pydantic import BaseModel, Field

Mode = Literal["learn", "exam", "practice", "project", "career"]

class StudentProfile(BaseModel):
    branch: str = "Engineering"
    semester: int | None = Field(default=None, ge=1, le=12)
    target_role: str | None = None
    known_skills: list[str] = Field(default_factory=list)
    weak_topics: list[str] = Field(default_factory=list)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    mode: Mode = "learn"
    student: StudentProfile = Field(default_factory=StudentProfile)

class ChatResponse(BaseModel):
    answer: str
    mode: Mode
    next_steps: list[str] = Field(default_factory=list)
