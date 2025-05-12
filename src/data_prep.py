import pandas as pd
def load_raw(path="data/raw/data.csv"):
    return pd.read_csv(path)
def clean_data(df):

TODO: implement cleaning & aggregation
return df
if __name__ == "__main__":
    df = load_raw()
    print(df.head())
