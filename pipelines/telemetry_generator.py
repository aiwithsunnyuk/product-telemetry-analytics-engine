import uuid
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd

class TelemetryGenerator:
    """Generates synthetic product event streams for testing ingestion and schema models."""
    
    MODULES = {
        "Workflow Builder": ["node_added", "workflow_published", "workflow_run"],
        "Analytics Dashboard": ["filter_applied", "chart_exported", "dashboard_shared"],
        "Settings & Admin": ["user_invited", "sso_enabled", "role_updated"]
    }
    PLATFORMS = ["web_desktop", "ios_mobile", "android_mobile", "api_client"]

    def __init__(self, num_users: int = 50, days_history: int = 30):
        self.num_users = num_users
        self.days_history = days_history
        self.user_ids = [f"usr_{uuid.uuid4().hex[:8]}" for _ in range(num_users)]

    def generate_events(self, num_records: int = 1000) -> List[Dict[str, Any]]:
        events = []
        now = datetime.utcnow()

        for _ in range(num_records):
            user = random.choice(self.user_ids)
            module = random.choice(list(self.MODULES.keys()))
            action = random.choice(self.MODULES[module])
            platform = random.choice(self.PLATFORMS)
            delta_days = random.uniform(0, self.days_history)
            timestamp = now - timedelta(days=delta_days)

            events.append({
                "event_id": f"evt_{uuid.uuid4().hex[:12]}",
                "user_id": user,
                "session_id": f"ses_{uuid.uuid4().hex[:8]}",
                "feature_key": f"{module.lower().replace(' ', '_')}_{action}",
                "event_name": action,
                "client_platform": platform,
                "duration_ms": random.randint(120, 4500),
                "occurred_at": timestamp.isoformat() + "Z",
                "event_date": timestamp.date().isoformat()
            })

        return events

    def export_to_dataframe(self, num_records: int = 1000) -> pd.DataFrame:
        return pd.DataFrame(self.generate_events(num_records))

if __name__ == "__main__":
    gen = TelemetryGenerator(num_users=20, days_history=14)
    df = gen.export_to_dataframe(500)
    print(f"Generated {len(df)} synthetic events.")
    print(df.head(3))
