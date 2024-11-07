import os
from fhirpy import SyncFHIRClient
from dotenv import load_dotenv
import base64

# Load environment variables from the .env file
load_dotenv()

# Define your FHIR server configuration
FHIR_SERVER_URL = os.getenv("FHIR_SERVER_URL", "http://localhost:8080/fhir")
FHIR_USERNAME = os.getenv("FHIR_USERNAME", "your-username")
FHIR_PASSWORD = os.getenv("FHIR_PASSWORD", "your-password")

# Encode the username and password in base64 for Basic Authentication
auth_token = base64.b64encode(f"{FHIR_USERNAME}:{FHIR_PASSWORD}".encode()).decode()

# Initialize the FHIR client with custom headers for Basic Authentication
client = SyncFHIRClient(
    FHIR_SERVER_URL,
    extra_headers={"Authorization": f"Basic {auth_token}"}
)

# Example function to retrieve a patient by family name
def get_patient_by_family_name(family_name):
    patient = client.resources("Patient").search(family=family_name).first()
    return patient

# Run an example query
if __name__ == "__main__":
    patient = get_patient_by_family_name("Doe")
    print("Retrieved Patient:", patient)