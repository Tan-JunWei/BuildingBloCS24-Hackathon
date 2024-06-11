# Import dependencies
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Overview",page_icon="🔥")
st.title("Ecobile")
st.header("An app for Sustainability")
st.title("")

# Static CSV file path
csv_path = 'PedestrianFacilities.csv'

def plot_pedestrian_facilities(csv_path):
    df = pd.read_csv(csv_path)

    # Pivot the DataFrame to have years as index and facilities as columns
    df_pivot = df.pivot(index='year', columns='facility', values='number')

    # Plot each facility type
    plt.figure(figsize=(12, 8))
    for column in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot[column], label=column)

    # Add title and labels
    plt.title('Number of Pedestrian Facilities Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Facilities')
    plt.legend(title='Facility Type')
    plt.grid(True)

    return plt

with st.container():
    st.subheader('Pedestrian Facilities Over Years')
    plt = plot_pedestrian_facilities(csv_path)
    st.pyplot(plt)
    st.write("As seen above, the Singapore government has continually added more pedestrian facilities over the years, to enable pedestrians \
            to travel safely and conveniently. By investing in pedestrian infrastructure and promoting walking, the Singapore government is not\
            only reducing carbon emissions and traffic congestion but also fostering a more sustainable urban environemnt.")
    st.write("")
    st.write("However, more must be done.")