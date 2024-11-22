import argparse
import base64
from pathlib import Path
import time
import matplotlib.pyplot as plt
import io
import numpy as np
import streamlit as st
import pandas as pd
from scipy.interpolate import make_interp_spline, BSpline

from t3co.visualization.charts import T3COCharts

start = time.time()
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog="T3CO Charts",
    description="""The t3co_charts_app.py module is the Visualization script for T3CO""",
)
parser.add_argument(
    "--input-file",
    type=str,
    default=None,
    help="Filepath of Quickstats results CSV file",
)
args = parser.parse_args()
if args.input_file:
    df = pd.read_csv(args.input_file)
else:
    df = None

st.title("T3CO Charts")
uploaded_file = st.file_uploader("Choose a Quickstats results file")

if uploaded_file is not None or df is not None:
    st.subheader(f"Filename: {uploaded_file.name} ")

    print(f"uploaded_file: {uploaded_file.name}")
    tc = T3COCharts()
    df = tc.from_file(uploaded_file)
    

    # plot_col = st.selectbox("Select column", tc.value_cols, key=7, index=14)

    st.write(df)

    # Scatter Plots
    st.subheader("TCO Breakdown")

    # x_axis = st.selectbox("Select X-axis", tc.value_cols, index=15)
    # y_axis = st.selectbox("Select Y-axis", tc.value_cols, index=16)
    group_col = st.selectbox("Select Group-by column", tc.group_columns, index=0)

    fig = tc.generate_tco_plots(group_col = group_col)

    st.pyplot(fig)

    img = io.BytesIO()
    fig.savefig(img, format="png")

    st.download_button(
        key=1,
        label="Download plot as PNG",
        data=img,
        file_name="plot.png",
        mime="image/png",
    )

    