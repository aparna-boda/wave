import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler
from datetime import datetime
from typing import Dict, Any, List, Tuple
from src.config import NU_PARAMETER, ANOMALY_CONTAMINATION_RATE_INIT, ROLLING_WINDOW_SIZE

class AnomalyDetector:
    def __init__(self):
        self.scaler = StandardScaler()
        self.contamination_rate = ANOMALY_CONTAMINATION_RATE_INIT
        
        # Initialize models
        self.isolation_forest = IsolationForest(contamination=self.contamination_rate, random_state=42)
        self.one_class_svm = OneClassSVM(kernel='rbf', nu=NU_PARAMETER)
        
        self.is_trained = False

    def train_models(self, normal_data: pd.DataFrame):
        """Train models on initial clean data."""
        self.training_data = self.scaler.fit_transform(normal_data) # Store for retraining
        self.isolation_forest.fit(self.training_data)
        self.one_class_svm.fit(self.training_data)
        self.is_trained = True
        print("ML Models trained successfully.")

    def update_contamination_rate(self, new_rate: float):
        """Update contamination rate and re-initialize IF model."""
        self.contamination_rate = new_rate
        self.isolation_forest = IsolationForest(contamination=self.contamination_rate, random_state=42)
        if hasattr(self, 'training_data'):
            self.isolation_forest.fit(self.training_data)
            print("Model retrained with new contamination rate.")

    def rolling_statistics_detection(self, reading: pd.Series, history: pd.DataFrame) -> bool:
        """Z-score based detection."""
        if len(history) < ROLLING_WINDOW_SIZE:
            return False
            
        # Check last window
        window = history.tail(ROLLING_WINDOW_SIZE)
        
        for col in ['pH', 'turbidity_ntu', 'tds_mgl', 'temp_celsius']:
            mean = window[col].mean()
            std = window[col].std()
            
            # Avoid division by zero
            if std == 0:
                continue
                
            z_score = abs(reading[col] - mean) / std
            if z_score > 3.0:
                return True
        return False

    def detect_anomaly(self, reading: pd.Series, history: pd.DataFrame) -> Dict[str, Any]:
        """Ensemble detection using 3 algorithms."""
        if not self.is_trained:
            return {'is_anomaly': False, 'votes': [], 'models': []}

        # Prepare input
        input_data = pd.DataFrame([reading])[['pH', 'turbidity_ntu', 'tds_mgl', 'temp_celsius']]
        X = self.scaler.transform(input_data)
        
        # 1. Rolling Stats
        vote_stats = self.rolling_statistics_detection(reading, history)
        
        # 2. Isolation Forest (-1 is anomaly, map to True)
        pred_if = self.isolation_forest.predict(X)[0]
        vote_if = True if pred_if == -1 else False
        
        # 3. One-Class SVM
        pred_svm = self.one_class_svm.predict(X)[0]
        vote_svm = True if pred_svm == -1 else False
        
        votes = [vote_stats, vote_if, vote_svm]
        is_anomaly = sum(votes) >= 2
        
        return {
            'is_anomaly': is_anomaly,
            'votes': votes,
            'models_triggered': [
                'Rolling Stats' if vote_stats else None,
                'Isolation Forest' if vote_if else None,
                'One-Class SVM' if vote_svm else None
            ]
        }

class AdaptiveLearning:
    def __init__(self, detector: AnomalyDetector):
        self.detector = detector
        self.feedback_history = []
        self.current_contamination_rate = ANOMALY_CONTAMINATION_RATE_INIT

    def record_feedback(self, alert_id: int, feedback: str, timestamp: datetime):
        print(f"Feedback received for Alert #{alert_id}: {feedback}")
        self.feedback_history.append({
            'alert_id': alert_id,
            'feedback': feedback,
            'timestamp': timestamp
        })
        
        if len(self.feedback_history) >= 20:
            self.evaluate_and_adjust()

    def evaluate_and_adjust(self):
        recent = self.feedback_history[-20:]
        fp_count = sum(1 for f in recent if f['feedback'] == 'FALSE_POSITIVE')
        fp_rate = fp_count / 20
        
        adjustment = 0.0
        reason = ""
        
        if fp_rate > 0.6:
            adjustment = -0.01
            reason = f"High FP rate ({fp_rate:.1%})"
        elif fp_rate < 0.2:
            adjustment = 0.01
            reason = f"Low FP rate ({fp_rate:.1%})"
            
        if adjustment != 0:
            new_rate = max(0.01, min(0.10, self.current_contamination_rate + adjustment))
            print(f"Adapting Sensitivity: {self.current_contamination_rate:.3f} -> {new_rate:.3f} | Reason: {reason}")
            self.current_contamination_rate = new_rate
            self.detector.update_contamination_rate(new_rate)
            # Reset history or keep sliding window? For POC, simple reset or just continue
            # If we reset, we wait for another 20. If we don't, we adjust every step.
            # Let's clear history to avoid continuous oscillation on same data
            self.feedback_history = [] 
