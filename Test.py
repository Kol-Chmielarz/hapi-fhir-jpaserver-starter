import requests

# Define the FHIR server URL and patient ID
fhir_url = "http://localhost:8080/fhir"
patient_id = "1"

# Endpoint for retrieving a patient's details
endpoint = f"{fhir_url}/Patient/{patient_id}"

try:
    # Send GET request to retrieve patient data
    response = requests.get(endpoint, headers={"Accept": "application/json"})
    
    # Check if the request was successful
    if response.status_code == 200:
        print("Patient data retrieved successfully!")
        print(response.json())  # Print JSON response
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)  # Print error message from server

except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")