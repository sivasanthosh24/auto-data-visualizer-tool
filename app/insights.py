import pandas as pd

def basic_insights(df):
    """Returns basic insights as text."""
    num_rows, num_cols = df.shape
    summary = df.describe(include='all').to_string()
    info = f"Dataset contains {num_rows} rows and {num_cols} columns.\n\nSummary:\n{summary}"
    return info

