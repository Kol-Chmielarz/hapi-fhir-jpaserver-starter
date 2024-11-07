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

# Function to create a new patient
def create_patient(family_name, given_name, gender, birth_date):
    new_patient = client.resource(
        "Patient",
        name=[{"use": "official", "family": family_name, "given": [given_name]}],
        gender=gender,
        birthDate=birth_date
    )
    new_patient.save()
    return new_patient

# Function to retrieve a patient by family name
def get_patient_by_family_name(family_name):
    patient = client.resources("Patient").search(family=family_name).first()
    return patient

# Run example to create and then retrieve a patient
if __name__ == "__main__":
    # Create a test patient
    created_patient = create_patient("Doe", "John", "male", "1985-01-01")
    print("Created Patient:", created_patient)

    # Retrieve the patient by family name
    patient = get_patient_by_family_name("Doe")
    print("Retrieved Patient:", patient)