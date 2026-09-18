# Architecture

## V1 request flow

1. Client sends ChatRequest.
2. FastAPI validates it.
3. The orchestrator applies mode guidance and student context.
4. A provider adapter will send the structured instruction to the selected LLM.
5. Retrieval and tools will be added around the model.

## Planned model boundary

```
Orchestrator
   |
   +-- hosted API
   +-- local inference server
   +-- open-weight model
   +-- future engineering-tuned model
```

The application stays provider-agnostic.

## Grounded learning flow

Question -> student state + curriculum + retrieved sources + prerequisites + tools -> orchestrator -> LLM -> answer + sources + next action

## Future knowledge graph

Entities: Branch, Program, Semester, Subject, Topic, Concept, Prerequisite, Skill, Tool, Project, Career Role.

Example: Control Systems -> requires -> Differential Equations.
