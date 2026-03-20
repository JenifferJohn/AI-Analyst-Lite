import pandas as pd

DATAFRAME = None

def set_dataframe(df: pd.DataFrame):
    global DATAFRAME
    df["Month"] = pd.to_datetime(df["Month"])
    DATAFRAME = df

def get_dataframe():
    return DATAFRAME