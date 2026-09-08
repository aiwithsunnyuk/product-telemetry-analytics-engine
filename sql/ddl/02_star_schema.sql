-- Dimension: Features & Application Modules
CREATE TABLE IF NOT EXISTS dim_features (
    feature_id SERIAL PRIMARY KEY,
    feature_key VARCHAR(64) UNIQUE NOT NULL,
    feature_name VARCHAR(128) NOT NULL,
    product_module VARCHAR(64) NOT NULL,
    tier VARCHAR(32) DEFAULT 'standard',
    release_sprint VARCHAR(32) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Dimension: User Cohorts & Signup Lifecycles
CREATE TABLE IF NOT EXISTS dim_cohorts (
    cohort_id SERIAL PRIMARY KEY,
    cohort_month DATE NOT NULL,
    cohort_tier VARCHAR(32) NOT NULL,
    acquisition_channel VARCHAR(64) NOT NULL,
    total_signups INTEGER DEFAULT 0
);

-- Fact: User Action Events
CREATE TABLE IF NOT EXISTS fact_user_events (
    event_surrogate_key BIGSERIAL PRIMARY KEY,
    event_id VARCHAR(64) UNIQUE NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    feature_id INTEGER REFERENCES dim_features(feature_id),
    cohort_id INTEGER REFERENCES dim_cohorts(cohort_id),
    session_id VARCHAR(64) NOT NULL,
    event_name VARCHAR(64) NOT NULL,
    client_platform VARCHAR(32) NOT NULL,
    duration_ms INTEGER DEFAULT 0,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    event_date DATE NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_fact_events_date ON fact_user_events (event_date);
CREATE INDEX IF NOT EXISTS idx_fact_events_feature ON fact_user_events (feature_id);
CREATE INDEX IF NOT EXISTS idx_fact_events_user ON fact_user_events (user_id);
