import streamlit as st
import pandas as pd
import os

# --- Helper to load CSVs
@st.cache_data
def load_csv(name, **kwargs):
    path = os.path.join("data", "processed", name)
    return pd.read_csv(path, **kwargs)

# --- Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "All Cleaned Data",
    "Ready for Review",
    "Support by Demographics",
    "Under-utilization"
])

# --- Page: All Cleaned Data
if page == "All Cleaned Data":
    st.header("All Cleaned Applications")
    df = load_csv("data_cleaned.csv", parse_dates=["request_date"])
    st.dataframe(df, use_container_width=True)

# --- Page: Ready for Review
elif page == "Ready for Review":
    st.header("Ready for Review")
    df = load_csv("ready_for_review.csv", parse_dates=["request_date"])
    st.dataframe(df, use_container_width=True)

# --- Page: Support by Demographics
elif page == "Support by Demographics":
    st.header("Support by Demographics")
    df = load_csv("support_by_demographics.csv")
    st.dataframe(df, use_container_width=True)
    st.bar_chart(data=df, x="location", y="award_amount")

# --- Page: Under-utilization
elif page == "Under-utilization":
    st.header("Under-utilization of Grants")
    df = load_csv("underutilization.csv")
    st.dataframe(df, use_container_width=True)
    avg_unused = df.groupby("assistance_type")["avg_unused"].mean().reset_index()
    st.bar_chart(data=avg_unused, x="assistance_type", y="avg_unused")
