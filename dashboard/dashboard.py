"""
Author: Ivan Chiari
Date: 01/03/2024
This is the dashboard.py module.
Usage:
- This module is used to create a dashboard for the bike sharing data.
"""

import os
import pandas as pd
import streamlit as st

@st.cache
def load_data():
    try:
        # Print current directory for debugging
        print("Current directory:", os.getcwd())

        # List files in the directory for debugging
        print("Files in directory:", os.listdir())

        # Load data
        file_path = "dashboard/main_data.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. File not found.")
        return None

# Load data
main_data = load_data()

# Check the first few rows of the loaded data for further debugging
print(main_data.head())

