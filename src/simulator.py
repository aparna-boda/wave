import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
from src.config import (
    BASELINE_PH, BASELINE_TURBIDITY, BASELINE_TDS, BASELINE_TEMP,
    RANDOM_SEED
)

class SensorSimulator:
    def __init__(self, seed: int = RANDOM_SEED):
        np.random.seed(seed)
        random.seed(seed)
        self.current_time = datetime.now()

    def generate_normal_reading(self, hour_of_day: int) -> Dict[str, float]:
        """Generate normal reading with time-based variations."""
        
        # pH slightly higher during day (photosynthesis effect simulation)
        ph_noise = np.random.normal(0, 0.05)
        ph_variation = 0.1 if 10 <= hour_of_day <= 16 else 0.0
        ph = np.random.uniform(BASELINE_PH[0], BASELINE_PH[1]) + ph_variation + ph_noise
        
        # Turbidity
        turb_noise = np.random.normal(0, 0.1)
        turb = np.random.uniform(BASELINE_TURBIDITY[0], BASELINE_TURBIDITY[1]) + turb_noise
        
        # TDS
        tds_noise = np.random.normal(0, 5.0)
        tds = np.random.uniform(BASELINE_TDS[0], BASELINE_TDS[1]) + tds_noise
        
        # Temperature (higher during day)
        temp_variation = 2.0 * np.sin((hour_of_day - 6) * np.pi / 12) if 6 <= hour_of_day <= 18 else 0.0
        temp = np.random.uniform(BASELINE_TEMP[0], BASELINE_TEMP[1]) + temp_variation + np.random.normal(0, 0.2)

        return {
            'pH': round(ph, 2),
            'turbidity_ntu': round(max(0, turb), 2),
            'tds_mgl': round(max(0, tds), 1),
            'temp_celsius': round(temp, 1)
        }

    def inject_anomaly(self, anomaly_type: str) -> Dict[str, float]:
        """Generate anomalous reading based on type."""
        reading = self.generate_normal_reading(12) # Use midday as base
        
        if anomaly_type == 'chemical_spill':
            # High pH (Alkaline), normal turbidity
            reading['pH'] += np.random.uniform(2.0, 4.0)
            
        elif anomaly_type == 'sewage_discharge':
            # High Turbidity, High TDS
            reading['turbidity_ntu'] += np.random.uniform(10.0, 50.0)
            reading['tds_mgl'] += np.random.uniform(200.0, 500.0)
            
        elif anomaly_type == 'industrial_waste':
            # Low pH (Acidic), High Temp
            reading['pH'] -= np.random.uniform(2.0, 3.0)
            reading['temp_celsius'] += np.random.uniform(5.0, 10.0)
            
        return reading

    def generate_dataset(self, num_readings: int = 1000) -> pd.DataFrame:
        """Generate complete time-series dataset with injected anomalies."""
        data = []
        start_time = datetime.now() - timedelta(minutes=num_readings)
        
        # Inject 2 anomalies if dataset is large enough
        if num_readings > 800:
             anomaly_indices = sorted(random.sample(range(800, num_readings), 2))
        else:
             anomaly_indices = [] # No anomalies for small sets

        for i in range(num_readings):
            timestamp = start_time + timedelta(minutes=i)
            hour = timestamp.hour
            
            if i in anomaly_indices:
                # Alternate between types
                atype = 'chemical_spill' if i == anomaly_indices[0] else 'sewage_discharge'
                reading = self.inject_anomaly(atype)
                dataset_type = 'anomaly'
            else:
                reading = self.generate_normal_reading(hour)
                dataset_type = 'normal'
                
            entry = {
                'timestamp': timestamp,
                **reading,
                'dataset_type': dataset_type 
            }
            data.append(entry)
            
        return pd.DataFrame(data)
