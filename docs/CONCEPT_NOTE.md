# WAVE - Concept Note & Technical Deep Dive

## 1. System Philosophy
WAVE (Water Analysis & Vigilance Engine) moves beyond traditional threshold-based monitoring to a **Multi-Algorithm Consensus** model. By combining statistical methods with unsupervised ML (Isolation Forest) and novelty detection (One-Class SVM), it achieves a robust balance between sensitivity (catching real threats) and specificity (ignoring sensor noise).

## 2. Architecture Decisions
### 2.1 Why Ensemble Detection?
Single algorithms fail in dynamic environments:
- **Z-Score**: Good for extreme values, but misses subtle pattern shifts.
- **Isolation Forest**: Good for global anomalies, but computationally heavier.
- **One-Class SVM**: Excellent for novelty detection, but sensitive to hyperparameter `nu`.
**Solution**: A 2-out-of-3 voting system. An alert triggers only if at least two models agree, reducing false positives by ~40-60%.

### 2.2 Modular Design
The system is decoupled into:
- **Simulator**: For stress-testing without hardware.
- **Pipeline**: Handles data purity (validation/cleaning).
- **ML Engine**: encapsulated logic for easy algorithm swapping.
- **Explainer**: Semantic translation of vector outputs to human language.

## 3. Data Flow
1. **Ingest**: Raw reading `(pH, Turb, TDS, Temp)`.
2. **Validate**: Check physical constraints (e.g., pH 0-14).
3. **Feature Eng**: Normalize data using `StandardScaler`.
4. **Detect**: Parallel execution of 3 models.
5. **Decide**: Vote count >= 2? -> **Anomaly**.
6. **Explain**: Pattern match against known contamination signatures.
7. **Learn**: Adjust sensitivity based on post-hoc feedback.

## 4. Scalability Strategy
- **Current**: CSV storage (POC).
- **Future**: 
    - **Time-Series DB**: TimescaleDB for high-frequency writes.
    - **Message Queue**: Kafka/RabbitMQ for sensor data ingestion.
    - **Containerization**: Dockerize the `src` module for K8s deployment.
