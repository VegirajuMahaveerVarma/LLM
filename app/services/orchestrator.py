from app.models import ChatRequest, ChatResponse
from app.services.prompts import SYSTEM_PRINCIPLES

def profile_context(request: ChatRequest) -> str:
    s = request.student
    parts = [f"Branch: {s.branch}"]
    if s.semester:
        parts.append(f"Semester: {s.semester}")
    if s.target_role:
        parts.append(f"Target role: {s.target_role}")
    if s.known_skills:
        parts.append("Known skills: " + ", ".join(s.known_skills))
    if s.weak_topics:
        parts.append("Weak topics: " + ", ".join(s.weak_topics))
    return " | ".join(parts)

def build_instruction(request: ChatRequest) -> str:
    guidance = {
        "learn": "Teach fundamentals, give a concise example, then ask one check-for-understanding question.",
        "exam": "Give an exam-ready explanation with definitions, key points, structure, and a compact final-answer version.",
        "practice": "Create practice first; encourage an attempt before revealing a full solution.",
        "project": "Cover requirements, architecture, implementation, testing, and risks.",
        "career": "Connect the topic to skills, portfolio evidence, and a practical next step.",
    }
    return (
        SYSTEM_PRINCIPLES.strip()
        + "\n\nStudent context: " + profile_context(request)
        + "\nMode guidance: " + guidance[request.mode]
        + "\nStudent request: " + request.message
    )

def respond(request: ChatRequest) -> ChatResponse:
    answer = (
        "ENGI-MIND foundation received your request.\n\n"
        f"Mode: {request.mode}\n"
        f"Student context: {profile_context(request)}\n\n"
        "The structured instruction is ready for the LLM provider integration."
    )
    steps = {
        "learn": ["Identify prerequisites", "Explain step-by-step", "Check understanding"],
        "exam": ["Map to marks", "Draft key points", "Practice recall"],
        "practice": ["Generate problem", "Attempt independently", "Review solution"],
        "project": ["Define requirements", "Design architecture", "Plan implementation and tests"],
        "career": ["Map skills", "Select a project", "Define measurable evidence"],
    }[request.mode]
    return ChatResponse(answer=answer, mode=request.mode, next_steps=steps)
