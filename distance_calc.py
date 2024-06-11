import googlemaps
from datetime import datetime 

gmaps = googlemaps.Client(key='AIzaSyBygqJSsYWT_z2G4o-KAU6F_5hyGTI7jY0')

start = input("Where are you starting your journey? ")
goal = input("Where would you like to go? ")
time_leaving_input = input("When will you be leaving? (HH:MM) Skip if you are leaving now ")

if time_leaving_input:
    current_date = datetime.now()
    hour, minute = time_leaving_input.split(":")
    time_leaving = datetime(current_date.year, current_date.month, current_date.day, int(hour), int(minute)).timestamp()
else:
    time_leaving = datetime.now().timestamp()

directions_result = gmaps.directions(start,goal,mode="walking",departure_time=time_leaving)


if directions_result:
    route = directions_result[0]  # Get the first route, assuming it's the primary one
    legs = route['legs']
    print("Directions from {} to {}:".format(start, goal))
    print("Distance: {}.".format(legs[0]['distance']['text']))
    print("Duration: {}.".format(legs[0]['duration']['text']))
    print("Departure Time: {}.".format(datetime.fromtimestamp(time_leaving).strftime('%Y-%m-%d %H:%M:%S')))
    if 'arrival_time' in legs[0]:
        print("Arrival Time: {}.".format(datetime.fromtimestamp(legs[0]['arrival_time']['value'])))
    else:
        print("Arrival Time information not available.")
else:
    print("No directions found.")