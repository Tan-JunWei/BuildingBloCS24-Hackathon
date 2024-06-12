from parse_duration import parse_duration
# Function to calculate carbon emission saved if walk instead of car 
def carbon_emissions_car(duration_text):
    # The average diesel vehicle emits around 10g of carbon emissions per minute
    # Source: https://8billiontrees.com/
    duration_parts = duration_text.split()
    total_minutes = 0
    for i in range(0, len(duration_parts), 2):
        value = int(duration_parts[i])
        unit = duration_parts[i+1]
        if "hour" in unit:
            total_minutes += value * 60
        elif "min" in unit:
            total_minutes += value
    return total_minutes * 0.1 * 1000  # convert kg to grams