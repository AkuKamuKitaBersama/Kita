"""
Author: Ivan Chiari
Date: 01/03/2024
This is the dashboard.py module.
Usage:
- This module is used to create a dashboard for the bike sharing data.
"""

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    try:
        # Print current directory for debugging
        st.write("Current directory:", os.getcwd())

        # List files in the directory for debugging
        st.write("Files in directory:", os.listdir())

        # Load data
        file_path = "dashboard/main_data.csv"
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        st.error("Failed to load data. File not found.")
        return None



def monthly_count(data):
    # Define the order of the months
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Convert 'month' column to categorical with the specified order
    data['month'] = pd.Categorical(data['month'], categories=month_order, ordered=True)
    
    # Group by 'month' and aggregate the total counts
    return data.groupby('month').agg({'total_count': 'sum'}).reset_index()


# Set the page configuration
st.set_page_config(
    page_title="Bike Sharing Data Visualization",
    page_icon="🚲",
    layout="wide",
)

# Load the cleaned data
main_data = load_data()


# Center-align the title
st.markdown("<h1  style='text-align: center;'>Bike Sharing Data Visualization</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# call functions
monthly_counts = monthly_count(main_data)

with st.container():
    st.subheader('Monthly Bike Sharing User')
    chart1, chart2 = st.columns(2)

    with chart1:
        chart1 = plt.figure(figsize=(8, 5), facecolor='w')  
        sns.lineplot(x='month', y='total_count', data=monthly_counts, color='skyblue', marker='o', sort=False)
        plt.title('Monthly Bike sharing User', color='w')
        plt.xlabel('Month', color='w')
        plt.ylabel('Total Rental Counts', color='w')
        plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.grid(True)
        st.pyplot(chart1)
        
    with chart2:
        # Sorting the monthly counts
        sorted_monthly_counts = monthly_counts.sort_values(by='total_count', ascending=True)
        # Assigning colors to highest and lowest months
        colors = ['red' if x in sorted_monthly_counts.head(1)['month'].values else 'green' if x in sorted_monthly_counts.tail(1)['month'].values else 'gray' for x in sorted_monthly_counts['month']]
        chart2 = plt.figure(figsize=(8, 5))
        plt.barh(sorted_monthly_counts['month'], sorted_monthly_counts['total_count'], color=colors)
        plt.title('Monthly Performance of Bike Sharing Users (2011-2012)')
        plt.xlabel('Total Count')
        plt.ylabel('Month')
        plt.grid(axis='x')
        plt.legend(handles=[plt.Rectangle((0,0),1,1,color='red',ec="k"), plt.Rectangle((0,0),1,1,color='green',ec="k"), plt.Rectangle((0,0),1,1,color='gray',ec="k")],
                labels=['Lowest Performing Month', 'Highest Performing Month', 'Other Months'], loc='lower right')
        st.pyplot(chart2)
    
    st.write("""
            **Analisis:**
            Berdasarkan analisis grafik, jumlah pengguna bike sharing mengalami peningkatan dari bulan Januari hingga Mei, mencapai puncaknya pada bulan Agustus, dan kemudian mengalami penurunan dari bulan Oktober hingga Desember.
            - Pada bulan Mei, terjadi peningkatan signifikan dalam jumlah pengguna, yang mencapai puncaknya pada bulan Agustus. 
            - Pada bulan Agustus, jumlah pengguna mencapai titik tertinggi dengan total 345,991 pengguna. Sebaliknya, jumlah pengguna terendah tercatat pada bulan Januari, dengan hanya 134,933 pengguna.
            
            Ini menunjukkan bahwa musim panas (agustus) cenderung menjadi waktu yang paling populer bagi pengguna bike sharing, sedangkan penggunaan cenderung menurun selama bulan-bulan dengan cuaca yang lebih dingin.
            """)



st.caption('Copyright (c) Ivan Chiari 2024')

