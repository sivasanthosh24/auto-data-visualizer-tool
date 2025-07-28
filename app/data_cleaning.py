# app/data_cleaning.py

import pandas as pd
import numpy as np

def clean_data(df: pd.DataFrame, threshold: float = 0.4) -> pd.DataFrame:
    # Drop columns with too many nulls
    df = df.copy()
    null_ratio = df.isnull().mean()
    df = df.loc[:, null_ratio < threshold]

    # Fill remaining nulls
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    return df


def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df
