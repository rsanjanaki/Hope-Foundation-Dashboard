import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Hope Foundation Dashboard",
    page_icon="🎗️",
    layout="wide"
)

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROC = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def load_csv(name, **kwargs):
    return pd.read_csv(os.path.join(PROC, name), **kwargs)

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "Ready for Review",
    "Support by Demographics",
    "Turnaround Time",
    "Under-utilization",
    "High-Level Summary"
])

if page == "Ready for Review":
    st.markdown("## 📋 Ready for Review")
    df = load_csv("ready_for_review.csv", parse_dates=["request_date"])
    df["signed_committee"] = df["signed_committee"].astype(str).str.lower()
    choice = st.sidebar.selectbox("Signed by Committee?", ["All", "Signed", "Unsigned"])
    if choice == "Signed":
        df = df[df["signed_committee"] == "yes"]
    elif choice == "Unsigned":
        df = df[df["signed_committee"] != "yes"]
    st.write(f"Showing **{len(df)}** applications")
    st.dataframe(df, use_container_width=True)

elif page == "Support by Demographics":
    st.markdown("## 🗺 Support by Demographics")
    df = load_csv("support_by_demographics.csv")
    demo = st.sidebar.selectbox("Group support by:", ["location", "gender", "application_year"])
    pivot = df.groupby(demo)["award_amount"].sum().reset_index()
    st.bar_chart(data=pivot, x=demo, y="award_amount", use_container_width=True)
    st.dataframe(pivot, use_container_width=True)

elif page == "Turnaround Time":
    st.markdown("## ⏱ Turnaround Time")
    summary = load_csv("turnaround_summary.csv")
    timeline = load_csv("turnaround_timeline.csv", parse_dates=["request_month"])
    st.subheader("Summary Statistics")
    st.table(summary)
    st.subheader("Median Turnaround by Month")
    fig = go.Figure([go.Scatter(
        x=timeline["request_month"],
        y=timeline["turnaround_days"],
        mode="lines+markers"
    )])
    fig.update_layout(xaxis_title="Month", yaxis_title="Days", template="simple_white")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Under-utilization":
    st.markdown("## 💸 Under-utilization")
    df = load_csv("underutilization.csv")
    year = st.sidebar.selectbox("Application Year", sorted(df["application_year"].unique()))
    sub = df[df["application_year"] == year]
    st.bar_chart(data=sub, x="assistance_type", y="avg_unused", use_container_width=True)
    st.dataframe(sub, use_container_width=True)

elif page == "High-Level Summary":
    st.markdown("## 📈 High-Level Impact & Progress")
    hl = load_csv("high_level_summary.csv").iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Applications", int(hl["total_applications"]))
    c2.metric("Total Dollars Awarded", f"${hl['total_dollars']:,.0f}")
    c3.metric("Avg Turnaround (days)", f"{hl['avg_turnaround_days']:.1f}")
    import ast
    raw = hl["yearly_pct_change"]
    if isinstance(raw, str):
        yoy_list = ast.literal_eval(raw)
    else:
        yoy_list = raw
    yoy = pd.DataFrame(yoy_list).set_index(pd.DataFrame(yoy_list).columns[0])
    st.subheader("Year-over-Year % Change in Awarded Amounts")
    st.line_chart(yoy["yoy_pct_change"], use_container_width=True)
