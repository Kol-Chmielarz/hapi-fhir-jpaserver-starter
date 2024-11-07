import os
from fhirpy import SyncFHIRClient  # Use AsyncFHIRClient if you need asynchronous operations
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define your FHIR server configuration
FHIR_SERVER_URL = os.getenv("FHIR_SERVER_URL", "http://localhost:8080/fhir")  # Default to local server if not set
FHIR_USERNAME = os.getenv("FHIR_USERNAME", "your-username")
FHIR_PASSWORD = os.getenv("FHIR_PASSWORD", "your-password")

# Initialize the FHIR client with the server configuration
client = SyncFHIRClient(
    FHIR_SERVER_URL,
    authorization="Basic",
    username=FHIR_USERNAME,
    password=FHIR_PASSWORD
)

# Example function to retrieve a patient by family name
def get_patient_by_family_name(family_name):
    patient = client.resources("Patient").search(family=family_name).first()
    return patient

# Run an example query
if __name__ == "__main__":
    patient = get_patient_by_family_name("Doe")
    print("Retrieved Patient:", patient)