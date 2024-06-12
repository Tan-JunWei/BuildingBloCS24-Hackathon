# Function to convert duration (eg. 3 hour 31 min) to number of minutes
# Function to parse duration text into minutes
def parse_duration(duration_text):
    duration_parts = duration_text.split()
    total_minutes = 0
    for i in range(0, len(duration_parts), 2):
        value = int(duration_parts[i])
        unit = duration_parts[i+1]
        if "hour" in unit:
            total_minutes += value * 60
        elif "min" in unit:
            total_minutes += value
    return total_minutes
