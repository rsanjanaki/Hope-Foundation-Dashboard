import os
import streamlit as st
import pandas as pd

# —————————————————————————————————————————————————————————————
# Setup absolute paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PROC    = os.path.join(BASE_DIR, "data", "processed")

@st.cache_data
def load_csv(name, **kwargs):
    return pd.read_csv(os.path.join(PROC, name), **kwargs)

# —————————————————————————————————————————————————————————————
st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Ready for Review",
    "Support by Demographics",
    "Turnaround Time",
    "Under-utilization",
    "High-Level Summary"
])

# 1) READY FOR REVIEW
if page == "Ready for Review":
    st.header("Ready for Review")
    df = load_csv("ready_for_review.csv", parse_dates=["request_date"])
    choice = st.radio("Signed by committee?", ["All", "Signed", "Unsigned"])
    if choice == "Signed":
        df = df[df["signed_committee"].str.lower() == "yes"]
    elif choice == "Unsigned":
        df = df[df["signed_committee"].str.lower() != "yes"]
    st.dataframe(df, use_container_width=True)

# 2) SUPPORT BY DEMOGRAPHICS
elif page == "Support by Demographics":
    st.header("Support by Demographics")
    df = load_csv("support_by_demographics.csv")
    demo = st.selectbox("Group by:", ["location", "gender", "application_year"])
    pivot = df.groupby(demo)["award_amount"].sum().reset_index()
    st.dataframe(pivot, use_container_width=True)
    st.bar_chart(data=pivot, x=demo, y="award_amount")

# 3) TURNAROUND TIME
elif page == "Turnaround Time":
    st.header("Turnaround Time")
    sum_df = load_csv("turnaround_summary.csv")
    tl_df  = load_csv("turnaround_timeline.csv", parse_dates=["request_month"])
    st.subheader("Summary Statistics")
    st.table(sum_df)
    st.subheader("Median Turnaround by Month")
    tl_df = tl_df.set_index("request_month")
    st.line_chart(tl_df["turnaround_days"])

# 4) UNDER-UTILIZATION
elif page == "Under-utilization":
    st.header("Under-utilization by Year & Assistance Type")
    df = load_csv("underutilization.csv")
    year = st.selectbox("Application Year", sorted(df["application_year"].unique()))
    sub = df[df["application_year"] == year]
    st.dataframe(sub, use_container_width=True)
    st.bar_chart(data=sub, x="assistance_type", y="avg_unused")

# 5) HIGH-LEVEL SUMMARY
elif page == "High-Level Summary":
    st.header("High-Level Impact & Progress")
    hl = load_csv("high_level_summary.csv").iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Applications", int(hl["total_applications"]))
    col2.metric("Total Dollars Awarded", f"${hl['total_dollars']:,.0f}")
    col3.metric("Avg Turnaround Days", f"{hl['avg_turnaround_days']:.1f}")
    st.subheader("Year-over-Year % Change")
    yoy = pd.read_json(hl["yearly_pct_change"]) if isinstance(hl["yearly_pct_change"], str) else pd.DataFrame(hl["yearly_pct_change"])
    yoy = yoy.set_index(yoy.columns[0])
    st.line_chart(yoy["yoy_pct_change"])
