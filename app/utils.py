def remove_outliers_iqr(df):
    """Removes outliers using IQR method from numeric columns."""
    from pandas.api.types import is_numeric_dtype
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df