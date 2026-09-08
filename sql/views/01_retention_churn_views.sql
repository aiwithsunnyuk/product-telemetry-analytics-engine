-- Monthly Cohort Retention Matrix View
CREATE OR REPLACE VIEW vw_cohort_retention_matrix AS
WITH user_activity AS (
    SELECT
        f.user_id,
        c.cohort_month,
        DATE_TRUNC('month', f.event_date)::DATE AS activity_month,
        (EXTRACT(YEAR FROM f.event_date) - EXTRACT(YEAR FROM c.cohort_month)) * 12 +
        (EXTRACT(MONTH FROM f.event_date) - EXTRACT(MONTH FROM c.cohort_month)) AS period_number
    FROM fact_user_events f
    INNER JOIN dim_cohorts c ON f.cohort_id = c.cohort_id
    GROUP BY 1, 2, 3, 4
),
cohort_sizes AS (
    SELECT cohort_month, COUNT(DISTINCT user_id) AS cohort_size
    FROM user_activity
    WHERE period_number = 0
    GROUP BY 1
)
SELECT 
    ua.cohort_month,
    ua.period_number,
    cs.cohort_size,
    COUNT(DISTINCT ua.user_id) AS active_users,
    ROUND((COUNT(DISTINCT ua.user_id)::NUMERIC / NULLIF(cs.cohort_size, 0)::NUMERIC) * 100, 2) AS retention_rate_pct
FROM user_activity ua
JOIN cohort_sizes cs ON ua.cohort_month = cs.cohort_month
GROUP BY ua.cohort_month, ua.period_number, cs.cohort_size
ORDER BY ua.cohort_month, ua.period_number;

-- User Inactivity Churn Risk View (Inactive > 30 days)
CREATE OR REPLACE VIEW vw_user_churn_risk AS
SELECT 
    user_id,
    MAX(event_date) AS last_active_date,
    CURRENT_DATE - MAX(event_date) AS days_since_last_action,
    CASE 
        WHEN CURRENT_DATE - MAX(event_date) >= 60 THEN 'Churned'
        WHEN CURRENT_DATE - MAX(event_date) >= 30 THEN 'At Risk'
        WHEN CURRENT_DATE - MAX(event_date) >= 14 THEN 'Cooling Down'
        ELSE 'Active'
    END AS lifecycle_state
FROM fact_user_events
GROUP BY user_id;
