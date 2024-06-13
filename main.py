# Import dependencies
import google.generativeai as genai
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import googlemaps
from datetime import datetime
from carbon_emissions import carbon_emissions_car
from parse_duration import parse_duration
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Ecobile", page_icon="🔥")
st.title("Ecobile")
st.header("Step into a Greener Future with Ecobile: Walk the Change!")

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

    plt.title('Number of Pedestrian Facilities Over Time')
    plt.xlabel('Year')
    plt.ylabel('Number of Facilities')
    plt.legend(title='Facility Type')
    plt.grid(True)

    return plt

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Application", "Gemini"])

if page == "Overview":
    st.header("Overview 📑")
    
    with st.container():
        st.subheader('Pedestrian Facilities Over Time')
        plt = plot_pedestrian_facilities(csv_path)
        st.pyplot(plt)
        st.write("As seen above, the Singapore government has continually added more pedestrian facilities over the years, to enable pedestrians \
                to travel safely and conveniently. By investing in pedestrian infrastructure and promoting walking, the Singapore government is not\
                only reducing carbon emissions and traffic congestion but also fostering a more sustainable urban environment.")
        st.write("")
        st.write("However, more must be done.")

    st.title("")
    st.header("Carbon Emissions Overview")
    col1, col2 = st.columns([2.5, 1])
    with col1:
        st.write("")
        st.write("")
        st.image("Singapore_Emissions_Profile_2021.png")
    with col2:
        st.write("In 2021, Transport continued to account for a significant portion of carbon emissions, compromising 14.2% of the total.")
        st.write("")
        st.write("")
        st.write("Singapore’s Emissions Profile. (n.d.). https://www.nccs.gov.sg/singapores-climate-action/singapores-climate-targets/singapore-emissions-profile/")
    st.title("")

    st.header("Rise of Global Carbon Emissions")
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
    st.write("The trajectory of carbon emissions reveals an alarming exponential increase over time, casting a looming shadow over the fate of our\
             planet. It is imperative for us to acknowledge this and adopt strategies to curb this ascent before the devastating implications\
             of climate change become irreversible.")
    st.write("The clock is ticking.")
    st.write("The time is now.")
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif page == "Application":
    st_lottie("https://lottie.host/6b986966-78ed-4fce-8758-90c19b07a73a/2UdJMhLYzJ.json")
    st.title("Our Idea💡")
    st.write("Our application assists users in deciding between walking and using public transport for their journeys, while illustrating the positive environmental impact of opting for these sustainable options instead of driving by calculating and displaying the saved carbon emissions.")
    st.subheader("")

    # Get API key
    api_key = st.text_input("Enter your Google Maps API key:")
    if not api_key:
        st.warning("Please enter your Google Maps API key above.")
        st.stop()
    gmaps = googlemaps.Client(key=api_key)

    # Get user inputs
    start = st.text_input("Where are you starting your journey?")
    goal = st.text_input("Where would you like to go?")
    age = st.text_input("What is your age?")
    departure_date = st.date_input("Departure Date", datetime.now().date())
    departure_time_input = st.text_input("Departure Time (HH\:MM)", datetime.now().strftime('%H:%M'))

    # Validate age input
    try:
        age = int(age)
    except ValueError:
        st.error("Please enter a valid age.")
        st.stop()

    if st.button("Get Directions"):
        # Parse leaving datetime
        try:
            departure_time = datetime.strptime(departure_time_input, '%H:%M')
        except ValueError:
            st.error("Please enter a valid time in HH:MM format.")
            st.stop()
        
        departure_datetime = datetime.combine(departure_date, departure_time.time())
        time_leaving = departure_datetime.timestamp()

        # Get walking directions
        try:
            directions_result = gmaps.directions(start, goal, mode="walking", departure_time=time_leaving)
        except Exception as e:
            st.error(f"Error fetching walking directions: {e}")
            st.stop()

        if directions_result:
            route = directions_result[0]
            legs = route['legs'][0]

            legs_distance = legs['distance']['text']
            legs_duration = legs['duration']['text']
            departure_time = departure_datetime.strftime('%I:%M %p')

            st.write(f"**Distance:** {legs_distance}")
            st.write(f"**Walking Duration:** {legs_duration}")
            st.write(f"**Departure Time:** {departure_time}")

            if 'arrival_time' in legs:
                st.write(f"**Arrival Time:** {datetime.fromtimestamp(legs['arrival_time']['value']).strftime('%I:%M %p')}")

            # Get public transport directions
            try:
                directions_result = gmaps.directions(start, goal, mode="transit", departure_time=time_leaving)
            except Exception as e:
                st.error(f"Error fetching public transport directions: {e}")
                st.stop()

            if directions_result:
                route = directions_result[0]
                legs = route['legs'][0]

                transit_duration = legs['duration']['text']
                transit_travel_time_s = sum(step['duration']['value'] for step in legs['steps'] if step['travel_mode'] == 'TRANSIT')

                bus_hours = transit_travel_time_s // 3600
                bus_minutes = (transit_travel_time_s % 3600) // 60
                transit_duration_only = f"**Total Travel Time on Buses:** {bus_hours} hours and {bus_minutes} minutes"
                transit_with_walk_duration = f"**Transit Duration:** {transit_duration}"

                # Recommendation based on age and walking duration
                walking_duration_minutes = parse_duration(legs_duration)
                if walking_duration_minutes > 15 or (age > 65 and walking_duration_minutes > 5):
                    if age > 65:
                        st.write("Your physical condition may not be suitable for such a long walk.")
                        st.write("Public transport might be more suitable.")
                    else:
                        st.write("**Walking duration exceeded 15 minutes.**")
                        st.write("**You may like to consider public transport options.**")

                    if not transit_travel_time_s > 0:
                        st.write("Sorry, walking is the only possible option")
                    else:
                        st.write("---------------------------------------------------------------------------")
                        st.write(transit_with_walk_duration)
                        st.write(f"Here are the directions to {goal} using:")
                        for step in legs['steps']:
                            if step['travel_mode'] == 'WALKING':
                                st.write(f"**{step['html_instructions']} ({step['duration']['text']}):**")
                            elif step['travel_mode'] == 'TRANSIT':
                                transit_details = step['transit_details']
                                line_name = transit_details['line'].get('short_name', transit_details['line']['name'])
                                st.write(f"**Take {transit_details['line']['vehicle']['type']} line {line_name} from {transit_details['departure_stop']['name']} to {transit_details['arrival_stop']['name']} ({step['duration']['text']}):**")
                elif age < 1:
                    st.write("You aren't old enough to walk or take public transport by yourself yet!")
                else:
                    st.write("**Walking duration is within 15 minutes, take a walk!**")
                    if transit_travel_time_s > 0:
                        saved_emissions = carbon_emissions_car(f'{bus_hours} hour {bus_minutes} min')
                        st.write(f"If you had taken public transport instead, you would have produced {saved_emissions:.2f}g of carbon emissions.")
                        st.write(f"This amount of carbon emissions saved is equivalent to planting {saved_emissions / 1000:.2f} trees.")
                        st.write(f"This amount of carbon emissions saved is equivalent to running an air conditioner for approximately {saved_emissions/500*60:.2f} minutes.")

                    else:
                        st.write("Walking is the only possible way too")
            else:
                st.write("No transit directions found.")
        else:
            st.write("No walking directions found.")
# -------------------------------------------------------------------------------------------------------------------------------------------------------------
elif page == "Gemini":
    st.title("Gemini API")

    # Display the Lottie animation
    st_lottie = st.lottie("https://lottie.host/8da495a6-7dd5-4370-9333-7204a9e3c33d/jgIvDHEXVS.json")

    st.write("To interact with Gemini, please enter your API credentials below:")

    api_key = st.text_input("Enter your Gemini API key:")

    if api_key:
        st.write("You've entered your API key. You can now ask Gemini questions.")
        st.subheader("")
        st.subheader("Prompt examples")
        st.write("How can I lower my carbon footprint in my daily life?")
        st.write("Why is lowering carbon footprint important?")
        st.write("How can changes in transportation habits lower your carbon footprint?")
        st.subheader("")

        # User input for query
        query = st.text_input("Enter your query:")

        if st.button("Ask"):
            if query:
                # Configure Google AI SDK
                genai.configure(api_key=api_key)

                # Create the model
                generation_config = {
                    "temperature": 1,
                    "top_p": 0.95,
                    "top_k": 64,
                    "max_output_tokens": 8192,
                    "response_mime_type": "text/plain",
                }

                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    generation_config=generation_config,
                    # Add safety_settings if needed
                )

                # Start a chat session and get response
                chat_session = model.start_chat(history=[])
                response = chat_session.send_message(query)

                # Display response
                st.write("Response from Gemini:")
                st.write(response.text)
            else:
                st.warning("Please enter a query.")
