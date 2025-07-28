import os
import matplotlib.pyplot as plt
import seaborn as sns
from app.config import VISUALS_PATH
import pandas as pd


def recommend_charts(df):
    """Generate chart recommendations based on column types."""
    recs = []

    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].nunique() < 20:
                recs.append({'column': col, 'type': 'bar'})
            else:
                recs.append({'column': col, 'type': 'pie'})
        elif df[col].dtype in ['int64', 'float64']:
            recs.append({'column': col, 'type': 'hist'})
            recs.append({'column': col, 'type': 'box'})
    return recs


def generate_visualizations(df, show=False):
    """Generates and saves charts as PNGs (for PDF use)."""
    recs = recommend_charts(df)

    # Ensure visuals folder exists
    os.makedirs(VISUALS_PATH, exist_ok=True)

    for rec in recs:
        col = rec['column']
        chart_type = rec['type']
        fig_path = os.path.join(VISUALS_PATH, f"{col}_{chart_type}.png")

        try:
            plt.figure(figsize=(8, 5))

            if chart_type == 'bar':
                df[col].value_counts().plot(kind='bar', color='skyblue')
                plt.title(f'Bar Chart: {col}')
                plt.xlabel(col)
                plt.ylabel("Count")

            elif chart_type == 'pie':
                df[col].value_counts().head(10).plot.pie(autopct='%1.1f%%')
                plt.title(f'Pie Chart: {col}')
                plt.ylabel("")

            elif chart_type == 'hist':
                df[col].dropna().plot.hist(bins=30, color='purple')
                plt.title(f'Histogram: {col}')
                plt.xlabel(col)
                plt.ylabel("Frequency")

            elif chart_type == 'box':
                sns.boxplot(x=df[col].dropna(), color='orange')
                plt.title(f'Boxplot: {col}')
                plt.xlabel(col)

            plt.tight_layout()
            plt.savefig(fig_path)
            plt.close()

        except Exception as e:
            print(f"⚠️ Failed to generate {chart_type} for {col}: {e}")

    # Add correlation heatmap
    numeric_df = df.select_dtypes(include=['int64', 'float64'])
    if not numeric_df.empty:
        try:
            plt.figure(figsize=(10, 8))
            sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
            plt.title("Correlation Heatmap")
            heatmap_path = os.path.join(VISUALS_PATH, "correlation_heatmap.png")
            plt.tight_layout()
            plt.savefig(heatmap_path)
            plt.close()
        except Exception as e:
            print(f"⚠️ Failed to generate heatmap: {e}")
