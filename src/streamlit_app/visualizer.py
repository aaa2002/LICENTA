import pandas as pd
from deltalake import DeltaTable
import os

# Load the delta table
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "delta", "web_results"))
dt = DeltaTable(base_path)

# Convert to pandas
df = dt.to_pandas()

# Visualize in Streamlit
import streamlit as st
st.title("Delta Table Viewer")
st.dataframe(df.head(10000))
