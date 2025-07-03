import pandas as pd
from deltalake import DeltaTable
import os

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "delta", "web_results"))
dt = DeltaTable(base_path)

df = dt.to_pandas()

import streamlit as st
st.title("Delta Table Viewer")
st.dataframe(df.head(10000))
