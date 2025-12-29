import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Dict, Any
from src.config import DASHBOARD_FILENAME

class DashboardGenerator:
    def create_dashboard(self, data: pd.DataFrame, alerts: List[Dict[str, Any]]):
        """Generate static dashboard image."""
        if data.empty:
            return

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'WAVE System Dashboard (Last {len(data)} Readings)', fontsize=16)
        
        # Plot parameters
        params = [
            ('pH', 'pH Level', axes[0, 0], 'blue'),
            ('turbidity_ntu', 'Turbidity (NTU)', axes[0, 1], 'brown'),
            ('tds_mgl', 'TDS (mg/L)', axes[1, 0], 'green'),
            ('temp_celsius', 'Temperature (°C)', axes[1, 1], 'red')
        ]
        
        timestamps = pd.to_datetime(data['timestamp'])
        
        for col, title, ax, color in params:
            ax.plot(timestamps, data[col], label=col, color=color)
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            
            # Highlight anomalies from recent data
            # (In a real dashboard we'd map alerts to timestamps exactly)
            
        # Add Alert Summary Text (simplified for static image)
        alert_text = f"Active Alerts: {len(alerts)}\n"
        if alerts:
            last_alert = alerts[-1]
            alert_text += f"Latest: {last_alert['explanation']['likely_cause']} ({last_alert['timestamp']})"
            
        fig.text(0.5, 0.02, alert_text, ha='center', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        plt.savefig(DASHBOARD_FILENAME)
        plt.close()
        print(f"Dashboard updated: {DASHBOARD_FILENAME}")

class FeedbackInterface:
    def simulate_feedback(self, alert: Dict[str, Any]) -> str:
        """Simulate operator feedback based on ground truth."""
        # Check if the alert corresponds to a real injected anomaly
        reading_type = alert['reading'].get('dataset_type', 'normal')
        
        if reading_type == 'anomaly':
            # It was a real anomaly
            return 'TRUE_POSITIVE'
        else:
            # It was normal data, but flagged -> False Positive
            return 'FALSE_POSITIVE'
