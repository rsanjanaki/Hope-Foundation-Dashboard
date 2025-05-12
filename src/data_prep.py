import os
import pandas as pd

def load_raw(path="data/raw/Cancer.xlsx", sheet_name=0):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xls", ".xlsx"):
        return pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    return pd.read_csv(path)

def clean_raw(df):
    df["request_date"] = pd.to_datetime(df["Grant Req Date"])
    df = df.rename(columns={
        "Request Status": "status",
        "Application Signed?": "signed_committee",
        "Amount": "award_amount",
        "App Year": "application_year",
        "Type of Assistance (CLASS)": "assistance_type",
        "DOB": "date_of_birth",
        "Gender": "gender",
        "Total Household Gross Monthly Income": "income",
        "Pt City": "city",
        "Pt State": "state",
        "Remaining Balance": "remaining_balance"
    })
    df["location"] = df["city"].str.strip() + ", " + df["state"].str.strip()
    df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce").fillna(0)
    df["income"]       = pd.to_numeric(df["income"], errors="coerce").fillna(0)
    df["remaining_balance"] = pd.to_numeric(df["remaining_balance"], errors="coerce").fillna(0)
    return df

def get_ready_for_review(df):
    ready = df[df["status"].str.lower() == "ready"]
    return ready[["Patient ID#", "request_date", "status", "signed_committee"]]

def support_by_demographics(df):
    return (
        df.groupby(["location", "gender", "application_year"])["award_amount"]
          .sum()
          .reset_index()
          .sort_values("award_amount", ascending=False)
    )

def underutilization(df):
    return (
        df.groupby(["application_year", "assistance_type"])["remaining_balance"]
          .agg(count="count", avg_unused="mean")
          .reset_index()
    )

if __name__ == "__main__":
    raw   = load_raw()
    clean = clean_raw(raw)
    os.makedirs("data/processed", exist_ok=True)
    clean.to_csv("data/processed/data_cleaned.csv", index=False)
    get_ready_for_review(clean).to_csv("data/processed/ready_for_review.csv", index=False)
    support_by_demographics(clean).to_csv("data/processed/support_by_demographics.csv", index=False)
    underutilization(clean).to_csv("data/processed/underutilization.csv", index=False)
    print("✅ data_prep complete.")
