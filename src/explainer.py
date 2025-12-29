import pandas as pd
from typing import Dict, Any, List
from src.config import BASELINE_PH, BASELINE_TURBIDITY, BASELINE_TDS, BASELINE_TEMP

class AlertExplainer:
    def get_parameter_status(self, reading: pd.Series) -> Dict[str, str]:
        """Determine if parameters are High, Low, or Normal."""
        status = {}
        
        # pH
        if reading['pH'] > BASELINE_PH[1] + 0.5: status['pH'] = 'HIGH'
        elif reading['pH'] < BASELINE_PH[0] - 0.5: status['pH'] = 'LOW'
        else: status['pH'] = 'NORMAL'
        
        # Turbidity (only high matters)
        if reading['turbidity_ntu'] > BASELINE_TURBIDITY[1] + 1.0: status['turbidity'] = 'HIGH'
        else: status['turbidity'] = 'NORMAL'
        
        # TDS
        if reading['tds_mgl'] > BASELINE_TDS[1] + 50: status['tds'] = 'HIGH'
        else: status['tds'] = 'NORMAL'
        
        # Temp
        if reading['temp_celsius'] > BASELINE_TEMP[1] + 3.0: status['temp'] = 'HIGH'
        else: status['temp'] = 'NORMAL'
        
        return status

    def match_pattern(self, status: Dict[str, str]) -> tuple[str, str]:
        """Match parameter patterns to likely causes."""
        ph = status['pH']
        turb = status['turbidity']
        temp = status['temp']
        
        if ph == 'HIGH' and turb == 'NORMAL':
            return "Alkaline Discharge", "Check nearby industrial outlets for alkaline waste."
            
        if ph == 'LOW' and turb == 'NORMAL':
            return "Acidic Discharge", "Potentially acidic industrial runoff. Inspect upstream."
            
        if turb == 'HIGH' and status['tds'] == 'HIGH':
            return "Significant Contamination", "High turbidity and dissolved solids. Possible sewage or mixed waste."

        if turb == 'HIGH' and ph == 'NORMAL':
            return "Sewage/Sediment", "Likely sewage discharge or high sediment load. Check structural integrity."
            
        if temp == 'HIGH':
            return "Thermal Pollution", "Abnormal temperature rise. Check coolant discharge lines."
            
        if ph != 'NORMAL' and turb == 'HIGH':
             return "Complex Chemical Spill", "Multiple parameters deviation indicates complex spill. Immediate isolation required."

        return "Unknown Anomaly", "Unusual pattern detected. Manual sampling recommended."

    def generate_explanation(self, reading: pd.Series, models_triggered: List[str]) -> Dict[str, Any]:
        """Generate human-readable alert explanation."""
        status = self.get_parameter_status(reading)
        cause, action = self.match_pattern(status)
        
        # Calculate Deviation
        anomalies = []
        for param, val in status.items():
            if val != 'NORMAL':
                anomalies.append(f"{param} is {val}")

        active_models = [m for m in models_triggered if m]
        confidence = "HIGH" if len(active_models) == 3 else "MEDIUM"
        
        return {
            'anomalous_parameters': anomalies,
            'likely_cause': cause,
            'recommended_action': action,
            'confidence': confidence,
            'models_triggered': active_models
        }
