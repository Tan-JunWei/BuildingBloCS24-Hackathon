import streamlit as st
import googlemaps
from datetime import datetime

# Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyBygqJSsYWT_z2G4o-KAU6F_5hyGTI7jY0')

# Streamlit interface
st.title("Walking Directions Finder")

start = st.text_input("Where are you starting your journey?")
goal = st.text_input("Where would you like to go?")
time_leaving_input = st.text_input("When will you be leaving? (HH\:MM) Leave blank if you are leaving now")

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
        st.write("**Journey from {} to {}:**".format(start, goal))
        st.write("**Distance:** {}".format(legs[0]['distance']['text']))
        st.write("**Duration:** {}".format(legs[0]['duration']['text']))
        st.write("**Departure Time:** {}".format(datetime.fromtimestamp(time_leaving).strftime('%Y-%m-%d %H:%M:%S')))
        if 'arrival_time' in legs[0]:
            st.write("**Arrival Time:** {}".format(datetime.fromtimestamp(legs[0]['arrival_time']['value']).strftime('%Y-%m-%d %H:%M:%S')))
    else:
        st.write("No directions found.")

