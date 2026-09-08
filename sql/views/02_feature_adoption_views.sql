-- Feature Consumption & Adoption Intensity
CREATE OR REPLACE VIEW vw_feature_adoption_curves AS
SELECT 
    df.feature_name,
    df.product_module,
    df.release_sprint,
    f.event_date,
    COUNT(f.event_surrogate_key) AS total_invocations,
    COUNT(DISTINCT f.user_id) AS unique_adopters,
    ROUND(AVG(f.duration_ms), 2) AS avg_engagement_ms
FROM fact_user_events f
INNER JOIN dim_features df ON f.feature_id = df.feature_id
GROUP BY df.feature_name, df.product_module, df.release_sprint, f.event_date;
