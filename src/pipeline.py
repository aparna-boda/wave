import pandas as pd
import numpy as np
from typing import Dict, Any, List
import os
from src.config import (
    VALID_RANGE_PH, VALID_RANGE_TURBIDITY, VALID_RANGE_TDS, VALID_RANGE_TEMP,
    DATASET_FILENAME
)

class DataValidator:
    def validate_reading(self, reading: pd.Series) -> bool:
        """Check if reading values are within valid physical ranges."""
        try:
            if not (VALID_RANGE_PH[0] <= reading['pH'] <= VALID_RANGE_PH[1]):
                return False
            if not (VALID_RANGE_TURBIDITY[0] <= reading['turbidity_ntu'] <= VALID_RANGE_TURBIDITY[1]):
                return False
            if not (VALID_RANGE_TDS[0] <= reading['tds_mgl'] <= VALID_RANGE_TDS[1]):
                return False
            if not (VALID_RANGE_TEMP[0] <= reading['temp_celsius'] <= VALID_RANGE_TEMP[1]):
                return False
            return True
        except KeyError:
            return False

    def handle_missing_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Forward fill missing values up to limit."""
        return data.ffill(limit=3)

    def preprocess_for_ml(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML model (dropping non-feature columns)."""
        feature_cols = ['pH', 'turbidity_ntu', 'tds_mgl', 'temp_celsius']
        return data[feature_cols]

class DataStorage:
    def __init__(self):
        self.filename = DATASET_FILENAME

    def save_dataset(self, df: pd.DataFrame):
        """Save full dataset to CSV."""
        df.to_csv(self.filename, index=False)
        print(f"Data saved to {self.filename}")

    def append_reading(self, reading: Dict[str, Any]):
        """Append single reading to CSV (Simulation for real-time)."""
        df = pd.DataFrame([reading])
        if not os.path.exists(self.filename):
            df.to_csv(self.filename, index=False)
        else:
            df.to_csv(self.filename, mode='a', header=False, index=False)
