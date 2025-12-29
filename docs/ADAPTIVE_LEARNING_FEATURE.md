# Adaptive Learning System

## Overview
The "Zero-Maintenance" promise of WAVE relies on its ability to tune itself. The `AdaptiveLearning` module acts as a feedback control loop for the ML Engine's sensitivity.

## How It Works

### 1. The Sensitivity Parameter
The core lever is the `contamination` parameter in the `IsolationForest` model (and potentially `nu` in SVM). 
- **Higher Contamination (e.g., 0.10)**: More sensitive, catches more anomalies, but higher False Positives.
- **Lower Contamination (e.g., 0.01)**: Stricter, catches only extreme outliers, lower False Positives.

### 2. The Feedback Loop
1. **Operator Action**: When an alert is displayed, the operator marks it as:
    - `TRUE_POSITIVE`: Real contamination.
    - `FALSE_POSITIVE`: False alarm (sensor noise, transient glitch).
2. **Buffer**: Feedbacks are collected in a rolling buffer (size=20).
3. **Evaluation**:
    - Calculate **False Positive Rate (FPR)** for the buffer.
    - **Thresholds**:
        - `FPR > 60%`: System is too sensitive ("Crying Wolf"). -> **Action**: Decrease sensitivity.
        - `FPR < 20%`: System is too conservative (Risk of missing events). -> **Action**: Increase sensitivity.
4. **Adjustment**:
    - The `contamination` rate is incremented/decremented by `0.01`.
    - Constraints: Rate is clamped between `0.01` and `0.10`.
5. **Retraining**: The model is immediately retrained with the new parameter to reflect the change.

## User Benefit
- **Day 1**: Generic production settings.
- **Day 30**: A system tunned specifically to the unique noise profile of that specific water station.
