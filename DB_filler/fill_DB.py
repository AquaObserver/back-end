import requests
import json

# Replace this with the correct endpoint
url = "http://127.0.0.1:8000/readings/"

# Input file with the generated data
input_file = "new_mock_readings.json"

# Read data from the JSON file and send POST requests
with open(input_file, 'r') as file:
    for line in file:
        # Load each line (JSON record) from the file
        data = json.loads(line.strip())

        try:
            # Send a POST request to the specified endpoint
            response = requests.post(url, json=data)

            # Print the result
            print(f"Status Code: {response.status_code}, Date: {data['tstz']}")
        except Exception as e:
            print(f"Error: {e}")

print("Data sending completed.")

