# Engineering Model Strategy

The target is an engineering tutor, not a replacement for a general foundation model.

Fine-tuning should improve explanation style, engineering terminology, problem-solving workflows, misconception handling, exam/practice/project behavior, and tool-use patterns. Frequently changing facts should remain in retrieval.

## Stages

1. Instruction tuning across target domains.
2. Tool-use tuning for calculators, code execution, retrieval, and engineering tools.
3. Personalization through a separate student-state system rather than putting private student data into global model weights.
4. Held-out evaluation against the base model.

## Quality gates

Check licensing metadata, duplicates, malformed examples, domain balance, hallucination rate, numerical accuracy, prerequisite consistency, explanation quality, and academic-integrity behavior.

Do not claim the model is trained on all engineering until evaluation demonstrates meaningful coverage.
