# WAVE - Water Analysis & Vigilance Engine

## Overview
WAVE is an intelligent water quality monitoring system that discriminates between harmless variants and real contamination events using a multi-algorithm ensemble (Rolling Stats, Isolation Forest, One-Class SVM). It features an update-learning loop where operator feedback tunes the model's sensitivity over time.

## Directory Structure
- `src/`: Source code modules
- `data/`: Storage for generated datasets and logs
- `requirements.txt`: Python dependencies

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the system:
   ```bash
   python src/main.py
   ```

## Features
- **Real-time Simulation**: Generates realistic sensor data (pH, Turbidity, TDS, Temp).
- **Ensemble Detection**: Reduces false positives by voting.
- **Explainable Alerts**: Human-readable descriptions of *why* an alert triggered.
- **Adaptive Learning**: Tunes sensitivity based on "Operator" feedback.
- **Visualization**: Generates dashboard images of water quality trends.
