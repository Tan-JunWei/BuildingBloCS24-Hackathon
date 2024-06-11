import googlemaps
from datetime import datetime
import streamlit as st

# Initialize Google Maps client
gmaps = googlemaps.Client(key='AIzaSyBygqJSsYWT_z2G4o-KAU6F_5hyGTI7jY0')

# Streamlit UI elements
st.title("Get Walking Directions")
start = st.text_input("Where are you starting your journey?")
goal = st.text_input("Where would you like to go?")
time_leaving_input = st.text_input("When will you be leaving? (HH:MM) Skip if you are leaving now")

if time_leaving_input:
    # Parse input time
    current_date = datetime.now()
    hour, minute = time_leaving_input.split(":")
    time_leaving = datetime(current_date.year, current_date.month, current_date.day, int(hour), int(minute)).timestamp()
else:
    time_leaving = datetime.now().timestamp()

# Get directions from Google Maps
directions_result = gmaps.directions(start, goal, mode="walking", departure_time=time_leaving)

if directions_result:
    route = directions_result[0]  # Get the first route, assuming it's the primary one
    legs = route['legs']
    st.write("Directions from {} to {}:".format(start, goal))
    st.write("Distance: {}.".format(legs[0]['distance']['text']))
    st.write("Duration: {}.".format(legs[0]['duration']['text']))
    st.write("Departure Time: {}.".format(datetime.fromtimestamp(time_leaving).strftime('%Y-%m-%d %H:%M:%S')))
    if 'arrival_time' in legs[0]:
        st.write("Arrival Time: {}.".format(datetime.fromtimestamp(legs[0]['arrival_time']['value'])))
    else:
        st.write("Arrival Time information not available.")
else:
    st.write("No directions found.")
