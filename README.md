# ENGI-MIND — Engineering Student LLM

ENGI-MIND is an engineering-learning AI platform for helping students learn concepts, solve problems, practice coding, work with course material, identify knowledge gaps, and build career-ready skills.

## V1

- FastAPI engineering tutor service
- Structured student profile
- Learning modes: learn, exam, practice, project, career
- Provider-agnostic LLM boundary
- Academic-integrity guardrails
- Roadmap for RAG, knowledge graph, tools, personalization, and model adaptation

## Architecture

```
Student -> API -> Orchestrator -> LLM
                         |-> Knowledge Base (planned)
                         |-> Knowledge Graph (planned)
                         |-> Tools (planned)
                         |-> Student Memory (planned)
```

## Run

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## API

GET /health

POST /v1/chat

Example:

```json
{
  "message": "Explain the difference between TCP and UDP.",
  "mode": "learn",
  "student": {
    "branch": "CSE",
    "semester": 5,
    "target_role": "software engineer",
    "known_skills": ["Python", "DSA"]
  }
}
```

V1 deliberately runs without an API key. The orchestration layer prepares structured model instructions; a real hosted or local model can be plugged in without redesigning the API.

## Product principles

1. Teach, not just answer.
2. Use tools for calculations and code execution.
3. Ground course-specific answers in retrieved sources.
4. Adapt difficulty to demonstrated knowledge.
5. Measure learning progress, not chat volume.
6. Keep academic-integrity boundaries explicit.

## Status

Foundation / V1.
