"""
AI Agent Performance Monitoring Dashboard
Run with: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Agent Performance Monitor", layout="wide", page_icon="🤖")

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    raw = pd.read_csv("../data/ai_agent_performance_dataset.csv")
    report = pd.read_csv("../reports/agent_benchmark_report.csv")
    return raw, report

raw_df, report_df = load_data()

STATUS_COLORS = {
    "Top Performer": "#2ecc71",
    "Solid Performer": "#3498db",
    "Needs Improvement": "#f39c12",
    "Underperforming": "#e74c3c",
}

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.title("🤖 Filters")
domains = ["All"] + sorted(raw_df["agent_domain"].unique().tolist())
selected_domain = st.sidebar.selectbox("Agent Domain", domains)

industries = ["All"] + sorted(raw_df["department_industry"].unique().tolist())
selected_industry = st.sidebar.selectbox("Client Industry", industries)

filtered_raw = raw_df.copy()
if selected_domain != "All":
    filtered_raw = filtered_raw[filtered_raw["agent_domain"] == selected_domain]
if selected_industry != "All":
    filtered_raw = filtered_raw[filtered_raw["department_industry"] == selected_industry]

filtered_agents = filtered_raw["agent_name"].unique().tolist()
filtered_report = report_df[report_df["agent_name"].isin(filtered_agents)].sort_values("rank")

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("AI Agent Performance Monitoring Platform")
st.caption("AssistanceFloxyz AI — Operations Intelligence Dashboard")

# ---------------------------------------------------------
# TOP KPI ROW
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Conversations", f"{len(filtered_raw):,}")
k2.metric("Avg Satisfaction", f"{filtered_raw['customer_satisfaction'].mean():.2f} / 5")
k3.metric("Avg Escalation Rate", f"{(filtered_raw['escalated']=='Yes').mean()*100:.1f}%")
k4.metric("Avg Cost / Conversation", f"${filtered_raw['cost_per_conversation_usd'].mean():.4f}")

st.divider()

# ---------------------------------------------------------
# AGENT BENCHMARK RANKINGS
# ---------------------------------------------------------
st.subheader("🏆 Agent Benchmark Rankings")

fig_rank = px.bar(
    filtered_report.sort_values("agent_health_score"),
    x="agent_health_score", y="agent_name", orientation="h",
    color="performance_status", color_discrete_map=STATUS_COLORS,
    text="agent_health_score",
    labels={"agent_health_score": "Agent Health Score", "agent_name": "Agent"},
)
fig_rank.update_layout(height=450, showlegend=True)
st.plotly_chart(fig_rank, use_container_width=True)

with st.expander("📋 Full Benchmark Table"):
    st.dataframe(
        filtered_report[[
            "rank", "agent_name", "agent_domain", "agent_health_score",
            "efficiency_score", "customer_experience_score", "reliability_score",
            "avg_satisfaction", "resolution_rate", "escalation_rate",
            "avg_cost_per_conv", "performance_status", "recommended_action"
        ]],
        use_container_width=True, hide_index=True
    )

st.divider()

# ---------------------------------------------------------
# SCORE BREAKDOWN
# ---------------------------------------------------------
st.subheader("📊 Score Breakdown by Agent")
score_cols = ["efficiency_score", "customer_experience_score", "reliability_score"]
melted = filtered_report.melt(id_vars="agent_name", value_vars=score_cols,
                               var_name="Score Type", value_name="Score")
fig_scores = px.bar(melted, x="agent_name", y="Score", color="Score Type", barmode="group")
fig_scores.update_layout(height=420, xaxis_tickangle=-30)
st.plotly_chart(fig_scores, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# COST vs SATISFACTION (Efficiency view)
# ---------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("💰 Cost vs Satisfaction")
    fig_scatter = px.scatter(
        filtered_report, x="avg_cost_per_conv", y="avg_satisfaction",
        size="total_conversations", color="performance_status",
        color_discrete_map=STATUS_COLORS, hover_name="agent_name",
        labels={"avg_cost_per_conv": "Avg Cost per Conversation ($)", "avg_satisfaction": "Avg Satisfaction"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with c2:
    st.subheader("📈 Escalation Rate by Agent")
    fig_esc = px.bar(
        filtered_report.sort_values("escalation_rate"),
        x="escalation_rate", y="agent_name", orientation="h",
        color="escalation_rate", color_continuous_scale="Reds",
        labels={"escalation_rate": "Escalation Rate (%)", "agent_name": "Agent"}
    )
    st.plotly_chart(fig_esc, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# DEPARTMENT / INDUSTRY VIEW
# ---------------------------------------------------------
st.subheader("🏢 Department-wise Performance")
dept_perf = filtered_raw.groupby("department_industry").agg(
    avg_satisfaction=("customer_satisfaction", "mean"),
    escalation_rate=("escalated", lambda s: (s == "Yes").mean() * 100),
    avg_cost=("cost_per_conversation_usd", "mean"),
    conversations=("conversation_id", "count"),
).reset_index().sort_values("avg_satisfaction", ascending=False)

fig_dept = px.bar(dept_perf, x="department_industry", y="avg_satisfaction",
                   color="escalation_rate", color_continuous_scale="RdYlGn_r",
                   labels={"department_industry": "Industry", "avg_satisfaction": "Avg Satisfaction"})
st.plotly_chart(fig_dept, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# SATISFACTION TREND OVER TIME
# ---------------------------------------------------------
st.subheader("📅 Satisfaction Trend Over Time")
trend_df = filtered_raw.copy()
trend_df["conversation_date"] = pd.to_datetime(trend_df["conversation_date"])
trend_df["month"] = trend_df["conversation_date"].dt.to_period("M").astype(str)
monthly_trend = trend_df.groupby("month")["customer_satisfaction"].mean().reset_index()

fig_trend = px.line(monthly_trend, x="month", y="customer_satisfaction", markers=True,
                     labels={"month": "Month", "customer_satisfaction": "Avg Satisfaction"})
st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ---------------------------------------------------------
# RECOMMENDATIONS PANEL
# ---------------------------------------------------------
st.subheader("🛠️ Optimization Recommendations")
for _, row in filtered_report.sort_values("rank").iterrows():
    color = STATUS_COLORS.get(row["performance_status"], "#999")
    st.markdown(
        f"""
        <div style="border-left: 5px solid {color}; padding: 8px 14px; margin-bottom: 8px; background-color: rgba(128,128,128,0.06); border-radius: 4px;">
        <b>#{int(row['rank'])} {row['agent_name']}</b> — {row['agent_domain']}
        &nbsp;|&nbsp; Health Score: <b>{row['agent_health_score']}</b>
        &nbsp;|&nbsp; Status: <b style="color:{color}">{row['performance_status']}</b><br>
        <span style="font-size: 0.9em;">💡 {row['recommended_action']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption("AI Agent Performance Monitoring Platform — Built for AssistanceFloxyz AI Operations Intelligence Team")
