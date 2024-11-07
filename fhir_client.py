import os
from fhirpy import SyncFHIRClient
from dotenv import load_dotenv
import base64

# Load environment variables from the .env file
load_dotenv()

# Define FHIR server configuration
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

# CREATE: Function to create a new patient
def create_patient(family_name, given_name, gender, birth_date):
    new_patient = client.resource(
        "Patient",
        name=[{"use": "official", "family": family_name, "given": [given_name]}],
        gender=gender,
        birthDate=birth_date
    )
    new_patient.save()
    print("Created Patient:", new_patient)
    return new_patient

# READ: Function to retrieve a patient by family name
# READ: Function to retrieve a patient by family name and print detailed info
def get_patient_by_family_name(family_name):
    patient = client.resources("Patient").search(family=family_name).first()
    
    if patient:
        # Print basic information about the patient
        print("Retrieved Patient:")
        print("ID:", patient.id)
        print("Name:", " ".join(patient["name"][0]["given"]) + " " + patient["name"][0]["family"])
        print("Gender:", patient.get("gender", "N/A"))
        print("Birth Date:", patient.get("birthDate", "N/A"))
    else:
        print("No patient found with family name:", family_name)
    
    return patient

# UPDATE: Function to update a patient's information
def update_patient(patient, new_family_name):
    patient["name"][0]["family"] = new_family_name
    patient.save()
    print("Updated Patient:", patient)
    return patient

# DELETE: Function to delete a patient
def delete_patient(patient):
    patient.delete()
    print("Deleted Patient with ID:", patient.id)

# DELETE ALL: Function to delete all patients
def clear_all_patients():
    patients = client.resources("Patient").fetch_all()
    for patient in patients:
        patient.delete()
        print("Deleted Patient with ID:", patient.id)
    print("All patients have been deleted.")

# Run example CRUD operations
if __name__ == "__main__":
    # CREATE: Add a test patient
    created_patient = create_patient("Davis", "Logan", "female", "2003-01-01")
    created_patient = create_patient("Mary", "Beth", "female", "2002-02-02")
    created_patient = create_patient("Doe", "John", "male", "2001-03-03")
    
    # READ: Retrieve the patient by family name
    retrieved_patient = get_patient_by_family_name("Davis")

    # Uncomment if you want to update and delete specific patients
    # if retrieved_patient:
    #     updated_patient = update_patient(retrieved_patient, "Smith")
    #     delete_patient(updated_patient)

    # CLEAR ALL: Delete all patients
    #clear_all_patients()