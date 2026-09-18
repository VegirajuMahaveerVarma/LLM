# ENGI-MIND Evaluation

Do not evaluate only on training examples. The benchmark is intended to measure whether the adapted model improves engineering tutoring behavior without degrading general usefulness.

## Required categories
- conceptual explanation
- mathematical derivation
- numerical problem solving
- misconception correction
- prerequisite consistency
- units and assumptions
- code/pseudocode reasoning
- project/application reasoning
- academic-integrity behavior

## Comparison
Run the same held-out prompts against:
1. the base model
2. the ENGI-MIND adapter

Track correctness, completeness, hallucination rate, reasoning quality, and refusal/redirect behavior. Do not claim specialization from training loss alone.
