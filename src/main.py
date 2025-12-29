import pandas as pd
import json
from src.config import ALERTS_LOG_FILENAME, LEARNING_METRICS_FILENAME
from src.simulator import SensorSimulator
from src.pipeline import DataValidator, DataStorage
from src.ml_engine import AnomalyDetector, AdaptiveLearning
from src.explainer import AlertExplainer
from src.dashboard import DashboardGenerator, FeedbackInterface

class WAVESystem:
    def __init__(self):
        self.simulator = SensorSimulator()
        self.validator = DataValidator()
        self.detector = AnomalyDetector()
        self.learner = AdaptiveLearning(self.detector)
        self.explainer = AlertExplainer()
        self.dashboard = DashboardGenerator()
        self.storage = DataStorage()
        self.feedback_interface = FeedbackInterface()

    def run(self, num_readings: int = 1000):
        print(f"Starting WAVE System... generating {num_readings} readings.")
        
        # 1. Generate Dataset
        full_data = self.simulator.generate_dataset(num_readings)
        
        # 2. Training Phase (First 800)
        training_cutoff = 800
        training_data = full_data.iloc[:training_cutoff]
        clean_training_data = self.validator.preprocess_for_ml(training_data)
        
        print("Training models on initial 800 readings...")
        self.detector.train_models(clean_training_data)
        
        # 3. Monitoring Phase
        alerts = []
        
        print("Starting monitoring loop...")
        for i in range(training_cutoff, len(full_data)):
            reading_row = full_data.iloc[i]
            
            # Simulate real-time validation
            if not self.validator.validate_reading(reading_row):
                print(f"Skipping invalid reading at index {i}")
                continue
                
            # History for rolling stats (last N readings)
            history = full_data.iloc[max(0, i-100):i]
            
            # Detect
            result = self.detector.detect_anomaly(reading_row, history)
            
            if result['is_anomaly']:
                # Explain
                explanation = self.explainer.generate_explanation(
                    reading_row, result['models_triggered']
                )
                
                # Convert reading to dict and fix timestamp for JSON
                reading_dict = reading_row.to_dict()
                reading_dict['timestamp'] = str(reading_dict['timestamp'])

                alert = {
                    'id': len(alerts) + 1,
                    'timestamp': str(reading_row['timestamp']),
                    'reading': reading_dict,
                    'explanation': explanation,
                    'severity': 'CRITICAL' if explanation['confidence'] == 'HIGH' else 'WARNING'
                }
                alerts.append(alert)
                
                print(f"\n[ALERT] {alert['timestamp']} - {explanation['likely_cause']}")
                print(f"Confidence: {explanation['confidence']} | Models: {result['models_triggered']}")
                
                # Feedback loop
                feedback = self.feedback_interface.simulate_feedback(alert)
                self.learner.record_feedback(alert['id'], feedback, reading_row['timestamp'])
            
            # Periodic Dashboard (every 100 readings)
            if i % 100 == 0:
                self.dashboard.create_dashboard(full_data.iloc[:i+1], alerts)
                
        # 4. Final Save
        self.storage.save_dataset(full_data)
        
        # Save Logs
        with open(ALERTS_LOG_FILENAME, 'w') as f:
            json.dump(alerts, f, indent=2)
            
        # Save Metrics
        metrics = {
             'final_sensitivity': self.detector.contamination_rate,
             'total_alerts': len(alerts),
             'feedback_history_count': len(self.learner.feedback_history)
        }
        with open(LEARNING_METRICS_FILENAME, 'w') as f:
            json.dump(metrics, f, indent=2)
            
        print("\nSystem run complete.")
        print(f"Dataset saved.")
        print(f"Alerts logged: {len(alerts)}")
        print(f"Dashboard generated.")

if __name__ == "__main__":
    print("DEBUG: Starting main execution block")
    try:
        system = WAVESystem()
        print("DEBUG: System initialized")
        system.run()
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
