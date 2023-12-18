import json
from datetime import datetime, timedelta
import random

# Output file to store the generated data
output_file = "mock_readings.json"

# Start date for the loop
start_date = datetime(2023, 12, 1, 0, 0, 0)

# End date for the loop (current date)
end_date = datetime(2024, 1, 1, 0, 0, 0)

# Time interval between readings (in seconds)
interval_seconds = 120

# Open the file in append mode to avoid overwriting existing data
with open(output_file, 'a') as file:
    # Loop through each day from start_date to end_date
    current_date = start_date
    while current_date <= end_date:
        # Generate readings every two minutes for the current day
        while current_date < current_date.replace(hour=23, minute=59, second=59) and current_date <= end_date:
            # Generate a timestamp in the specified format
            timestamp = current_date.strftime("%Y-%m-%dT%H:%M:%S")

            # Create a data payload with random waterLevel values
            data = {
                "tstz": timestamp,
                "deviceId": 1,
                "waterLevel": round(random.uniform(15.0, 42.0), 2)
            }

            # Serialize the data to JSON and write to the file
            print(timestamp)
            json.dump(data, file)
            file.write('\n')  # Add a newline to separate entries

            # Move to the next timestamp (two minutes later)
            current_date += timedelta(seconds=interval_seconds)

        # Move to the next day
        current_date += timedelta(days=1)

print(f"Mock data saved to {output_file}.")
