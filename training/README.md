# ENGI-MIND Training Pipeline

This directory prepares a legally usable engineering-focused instruction dataset for later supervised fine-tuning.

## Target

Build a model that is better at teaching engineering students, not merely memorizing textbooks.

Initial domains: Engineering Mathematics, CSE/IT, ECE, EEE, Mechanical, Civil, Chemical, Robotics/Automation, Instrumentation, Aerospace, Biomedical, Environmental, Industrial/Production, Materials, Mining, and Agricultural Engineering.

## Principles

1. Prefer public-domain, openly licensed, synthetic, or explicitly permitted material.
2. Keep source and license metadata.
3. Do not ingest copyrighted textbooks wholesale without permission.
4. Train explanation, derivation, worked-example, misconception, practice, exam, project, and career behaviors.
5. Keep evaluation data separate from training data.
6. Prove improvement against the base model with held-out evaluation.

## Pipeline

raw sources -> normalized records -> curriculum tags -> instruction examples -> validation -> train/validation split -> fine-tuning -> evaluation

See training/configs/target_domains.json for the curriculum map.
