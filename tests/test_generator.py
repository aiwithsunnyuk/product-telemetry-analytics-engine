import pytest
from pipelines.telemetry_generator import TelemetryGenerator

def test_telemetry_generator_output():
    generator = TelemetryGenerator(num_users=10, days_history=7)
    events = generator.generate_events(num_records=50)

    assert len(events) == 50
    first = events[0]
    assert "event_id" in first
    assert "user_id" in first
    assert "feature_key" in first
    assert first["duration_ms"] >= 120

def test_telemetry_dataframe_conversion():
    generator = TelemetryGenerator(num_users=5, days_history=3)
    df = generator.export_to_dataframe(num_records=25)
    assert not df.empty
    assert len(df) == 25
    assert "event_date" in df.columns
