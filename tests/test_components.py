import unittest
import pandas as pd
import numpy as np
from src.simulator import SensorSimulator
from src.pipeline import DataValidator
from src.ml_engine import AnomalyDetector
from src.explainer import AlertExplainer
from src.config import BASELINE_PH, BASELINE_TURBIDITY

class TestWAVEComponents(unittest.TestCase):

    def setUp(self):
        self.simulator = SensorSimulator(seed=42)
        self.validator = DataValidator()
        self.detector = AnomalyDetector()
        self.explainer = AlertExplainer()

    def test_simulator_output_structure(self):
        """Test if simulator generates correct dictionary structure."""
        reading = self.simulator.generate_normal_reading(12)
        expected_keys = {'pH', 'turbidity_ntu', 'tds_mgl', 'temp_celsius'}
        self.assertTrue(expected_keys.issubset(reading.keys()))
        
    def test_simulator_ranges_normal(self):
        """Test if normal readings are roughly within baselines."""
        # Generate 100 readings and check means
        readings = [self.simulator.generate_normal_reading(12) for _ in range(100)]
        df = pd.DataFrame(readings)
        
        # pH should be around 7.0-7.4
        self.assertTrue(6.8 <= df['pH'].mean() <= 7.6)

    def test_validator_valid_reading(self):
        """Test validation of a valid reading."""
        valid_reading = pd.Series({
            'pH': 7.2, 'turbidity_ntu': 1.5, 'tds_mgl': 150, 'temp_celsius': 22
        })
        self.assertTrue(self.validator.validate_reading(valid_reading))

    def test_validator_invalid_reading(self):
        """Test validation of an out-of-bounds reading."""
        invalid_reading = pd.Series({
            'pH': 15.0, # Invalid
            'turbidity_ntu': 1.5, 'tds_mgl': 150, 'temp_celsius': 22
        })
        self.assertFalse(self.validator.validate_reading(invalid_reading))

    def test_ml_engine_training(self):
        """Test if models can be trained without error."""
        # Generate dummy data
        data = pd.DataFrame([
            self.simulator.generate_normal_reading(12) for _ in range(100)
        ])
        
        try:
            self.detector.train_models(data)
        except Exception as e:
            self.fail(f"train_models raised {e} unexpectedly!")
            
        self.assertTrue(self.detector.is_trained)

    def test_explainer_logic(self):
        """Test if explainer identifies high pH correctly."""
        high_ph_reading = pd.Series({
            'pH': 9.0, # High
            'turbidity_ntu': 1.5, # Normal
            'tds_mgl': 150,
            'temp_celsius': 22
        })
        
        status = self.explainer.get_parameter_status(high_ph_reading)
        self.assertEqual(status['pH'], 'HIGH')
        self.assertEqual(status['turbidity'], 'NORMAL')
        
        cause, _ = self.explainer.match_pattern(status)
        self.assertEqual(cause, "Alkaline Discharge")

if __name__ == '__main__':
    unittest.main()
