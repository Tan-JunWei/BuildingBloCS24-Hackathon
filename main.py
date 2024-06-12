# Import dependencies
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import googlemaps
from datetime import datetime

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

carbon_emission_csv_path = 'historical_emissions.csv'

def load_data():
    try:
        data = pd.read_csv(carbon_emission_csv_path)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")

data = load_data()

if data is not None:
    countries = data['Country'].unique() #only unique countries

    years = [int(col) for col in data.columns if col.isdigit()]

    # Plot for each country
    plt.figure(figsize=(15, 8))
    for country in countries:
        country_data = data[data['Country'] == country]
        emissions = country_data.iloc[:, 5:].values.flatten()
        plt.plot(years, emissions, label=country)

    plt.title('CO2 Emissions by Country Over the Years')
    plt.xlabel('Year')
    plt.ylabel('CO2 Emissions (MtCO₂e)')
    plt.xticks(years, rotation=45)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=6)
    plt.grid(True)
    plt.tight_layout()

    st.pyplot(plt)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import googlemaps
from datetime import datetime

# Streamlit interface
st.title("Walking Directions Finder")

api_key = st.text_input("Enter your Google Maps API key:")

if not api_key:
    st.warning("Please enter your Google Maps API key above.")
    st.stop()

gmaps = googlemaps.Client(key=api_key)

start = st.text_input("Where are you starting your journey?")
goal = st.text_input("Where would you like to go?")
time_leaving_input = st.text_input("When will you be leaving? (HH\:MM) Leave blank if you are leaving now")

# Function to convert duration (eg. 3 hours 31 mins) to number of minutes
def parse_duration(duration):
    total_minutes = 0 #initialise 0
    parts = duration.split()
    
    i = 0
    while i < len(parts):
        value = int(parts[i])
        unit = parts[i+1]

        if "hour" in unit:
            total_minutes += value * 60 #convert hours to minutes
        elif "min" in unit:
            total_minutes += value
        # else is NOT used here since google maps shows hours and mins, unless user enters a ridiculous input
        i += 2

    return total_minutes

# Function to calculate carbon emission saved if walk instead of car
def carbon_emissions_car(duration):
    # The average diesel vehicle emits around 10g of carbon emissions per minute
    # Source: https://8billiontrees.com/
    minutes = parse_duration(duration)
    average_car_carbon_emission = 10
    car_carbon_emission_reduced = average_car_carbon_emission * minutes

    return car_carbon_emission_reduced


if st.button("Get Directions"):
    if time_leaving_input:
        current_date = datetime.now()
        hour, minute = map(int, time_leaving_input.split(":"))
        time_leaving = datetime(current_date.year, current_date.month, current_date.day, hour, minute).timestamp()
    else:
        time_leaving = datetime.now().timestamp()

    directions_result = gmaps.directions(start, goal, mode="walking", departure_time=time_leaving)

    if directions_result:
        route = directions_result[0]  # Get the first route, assuming it's the primary one
        legs = route['legs']

        # Declare variables
        legs_distance = legs[0]['distance']['text']
        legs_duration = legs[0]['duration']['text']
        departure_time = datetime.fromtimestamp(time_leaving).strftime('%Y-%m-%d %H:%M:%S')

        st.markdown("**Directions from {} to {}:**".format(start, goal), unsafe_allow_html=True)  # Underline effect
        st.write("**Distance:** {}".format(legs_distance))
        st.write("**Duration:** {}".format(legs_duration))
        st.write("**Departure Time:** {}".format(departure_time))

        if 'arrival_time' in legs[0]:
            st.write("**Arrival Time:** {}".format(datetime.fromtimestamp(legs[0]['arrival_time']['value']).strftime('%Y-%m-%d %H:%M:%S')))

        # Recommendation of transport options
        if parse_duration(legs_duration) > 10:
            st.write("**Walking duration exceeded 10 minutes.**")
            st.write("**You may like to consider public transport options.**")
            
        elif parse_duration(legs_duration):
            st.write("**Walking duration is within 10 minutes, take a walk!**")
            st.write("The average diesel vehicle ie. car emits around 10g of carbon emissions per minute.\
                     By taking a walk for {} minutes instead of driving, you are reducing carbon emissions by approximately {}g.".format(parse_duration(legs_duration),carbon_emissions_car(legs_duration)))
    else:
        st.write("No directions found.")
