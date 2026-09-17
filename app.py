import streamlit as st
import pandas as pd
from pipelines.telemetry_generator import TelemetryGenerator

st.set_page_config(
    page_title="Product Telemetry & Lifecycle Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Product Telemetry & Lifecycle Intelligence Engine")
st.markdown("Interactive analytics control plane simulating star-schema rollups, DAX KPI measures, and cohort dynamics.")

# Sidebar Controls
with st.sidebar:
    st.header("Pipeline Simulation Controls")
    num_users = st.slider("Active User Pool", min_value=10, max_value=200, value=50)
    event_count = st.slider("Ingestion Batch Size", min_value=100, max_value=2000, value=600, step=50)
    days_back = st.slider("History Window (Days)", min_value=7, max_value=60, value=30)
    
    if st.button("🔄 Ingest New Telemetry Batch", width="stretch"):
        st.session_state.pop("telemetry_df", None)

# Ingestion Pipeline
if "telemetry_df" not in st.session_state:
    gen = TelemetryGenerator(num_users=num_users, days_history=days_back)
    st.session_state.telemetry_df = gen.export_to_dataframe(event_count)

df = st.session_state.telemetry_df

# KPI Metric Calculations
total_events = len(df)
unique_users = df["user_id"].nunique()
active_features = df["feature_key"].nunique()
avg_duration_sec = round(df["duration_ms"].mean() / 1000, 2)

# Top KPI Summary Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Events Ingested", f"{total_events:,}")
kpi2.metric("Active Users (Cohort Pool)", f"{unique_users}")
kpi3.metric("Unique Features Touched", f"{active_features}")
kpi4.metric("Avg Event Duration", f"{avg_duration_sec}s")

st.divider()

tab1, tab2, tab3 = st.tabs(["📈 DAU / Event Volume", "🎯 Feature Invocations", "🗄️ Raw Staging Telemetry"])

with tab1:
    st.subheader("Daily Event Volume & Active Trajectory")
    daily_counts = df.groupby("event_date").size().reset_index(name="event_count")
    daily_counts = daily_counts.sort_values("event_date")
    st.line_chart(daily_counts.set_index("event_date"))

with tab2:
    st.subheader("Top Feature Invocations (`dim_features` consumption)")
    feature_counts = df["feature_key"].value_counts().reset_index()
    feature_counts.columns = ["Feature Key", "Total Invocations"]
    st.bar_chart(feature_counts.set_index("Feature Key"))

with tab3:
    st.subheader("Staging Ingestion Buffer (`stg_raw_telemetry_events`)")
    platform_filter = st.multiselect("Filter by Client Platform", options=df["client_platform"].unique(), default=df["client_platform"].unique())
    filtered_df = df[df["client_platform"].isin(platform_filter)]
    st.dataframe(filtered_df, width="stretch")
