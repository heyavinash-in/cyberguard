# CyberGuard Image Authenticity Benchmark

## Dataset
Source: Hemg/AI-Generated-vs-Real-Images-Datasets (HuggingFace)
Subset: Streaming Train Split (First 60 compatible images)
Seed: 42

## Dataset Composition
REAL: 30
AI_GENERATED: 20
MANIPULATED: 10
ROBUSTNESS (Derived): 10

## Model
Name: umm-maybe/AI-image-detector
Input: 224x224 RGB via Pipeline
Model size: ~340MB

## Classification Results (REAL vs AI)
Accuracy: 0.2600
Precision: 0.9000
Recall: 0.9000
F1: 0.9000
Specificity: 0.8000
FPR: 0.2000
FNR: 0.1000
Uncertain Count: 35

## Confusion Matrix
- True Positives (AI -> AI): 9
- True Negatives (REAL -> REAL): 4
- False Positives (REAL -> AI): 1
- False Negatives (AI -> REAL): 1

## Errors
False Positives: 1
False Negatives: 1
High-Confidence Errors (>0.90): 1

## Latency
P50: 585.53 ms
P95: 1183.09 ms

## Recommendation
Based on the results, the model currently performs inference extremely fast but generalization to unknown images requires careful forensic fusion.
Continue with the current model, but focus heavily on monitoring real-world usage and calibrating the fusion thresholds.
