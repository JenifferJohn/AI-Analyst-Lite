import pandas as pd
from core.column_normalizer import normalize_dataframe

DATAFRAME = None


def set_dataframe(df: pd.DataFrame):
    global DATAFRAME
    DATAFRAME = normalize_dataframe(df)


def get_dataframe():
    return DATAFRAME