-- Raw telemetry ingestion staging table
CREATE TABLE IF NOT EXISTS stg_raw_telemetry_events (
    event_id VARCHAR(64) PRIMARY KEY,
    user_id VARCHAR(64) NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    feature_key VARCHAR(64) NOT NULL,
    event_name VARCHAR(64) NOT NULL,
    client_platform VARCHAR(32) NOT NULL,
    duration_ms INTEGER DEFAULT 0,
    occurred_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ingested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stg_telemetry_user ON stg_raw_telemetry_events (user_id);
CREATE INDEX IF NOT EXISTS idx_stg_telemetry_occurred ON stg_raw_telemetry_events (occurred_at);
