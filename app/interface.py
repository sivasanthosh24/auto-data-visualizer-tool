import streamlit as st
import pandas as pd
import os

from app.visualizer import generate_visualizations
from app.report_generator import generate_pdf_report
from app.utils import remove_outliers_iqr
from app.config import DATA_PATH, REPORT_PATH, VISUALS_PATH


def show_interface():
    st.set_page_config(page_title="📊 Auto Data Visualizer", layout="wide")
    st.title("📊 Auto Data Visualizer")
    st.write("Upload a CSV or Excel file and download a PDF report with automatic visualizations.")

    uploaded_file = st.file_uploader("Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx", "xls"])

    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1].lower()

        try:
            if file_extension == "csv":
                df = pd.read_csv(uploaded_file)
            elif file_extension in ["xls", "xlsx"]:
                df = pd.read_excel(uploaded_file)
            else:
                st.error("Unsupported file type!")
                return
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        # Save the current dataset to a temp file
        df.to_csv(DATA_PATH, index=False)
        st.success("✅ File uploaded and saved!")

        # Clear previous charts from visuals folder
        for file in os.listdir(VISUALS_PATH):
            if file.endswith(".png"):
                os.remove(os.path.join(VISUALS_PATH, file))

        st.subheader("🧹 Step 1: Data Cleaning")
        df_cleaned = df.dropna()
        df_cleaned = remove_outliers_iqr(df_cleaned)
        st.dataframe(df_cleaned.head())

        st.subheader("📈 Step 2: Generating Visualizations")
        generate_visualizations(df_cleaned, show=False)
        st.success("✅ Visualizations generated and saved in the visuals/ folder.")

        st.subheader("📝 Step 3: Generating Report")
        pdf_path = generate_pdf_report()

        if pdf_path and os.path.exists(pdf_path):
            st.success("✅ PDF Report successfully created!")

            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=f,
                    file_name="visualization_report.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("⚠️ Report generation failed.")
    else:
        st.info("📁 Please upload a CSV or Excel file to begin.")
