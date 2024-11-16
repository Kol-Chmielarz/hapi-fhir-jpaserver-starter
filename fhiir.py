from fastapi import APIRouter, HTTPException
from fhir_client import create_patient, get_patient_by_mrn, get_studies_by_mrn, get_series_by_study

router = APIRouter()

@router.post("/fhir/patient")
async def create_fhir_patient(
    mrn: str,
    family_name: str,
    given_name: str,
    gender: str = "unknown",
    birth_date: str = "1900-01-01"
):
    """
    Create a new patient in the FHIR server.
    """
    try:
        patient = create_patient(mrn, family_name, given_name, gender, birth_date)
        return {"message": "Patient created successfully", "patient": patient.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create patient: {str(e)}")


@router.get("/fhir/patient/{mrn}")
async def get_fhir_patient_info(mrn: str):
    """
    Retrieve patient information from the FHIR server by MRN.
    """
    try:
        patient = get_patient_by_mrn(mrn)
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient with MRN {mrn} not found")
        return {"patient": patient.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve patient: {str(e)}")


@router.get("/orthanc/patient/{mrn}/studies")
async def get_studies_for_patient(mrn: str):
    """
    Retrieve studies from Orthanc for a patient by MRN.
    """
    try:
        studies = get_studies_by_mrn(mrn)
        if not studies:
            raise HTTPException(status_code=404, detail=f"No studies found for MRN {mrn}")
        return {"studies": studies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve studies: {str(e)}")


@router.get("/orthanc/study/{study_id}/series")
async def get_series_for_study(study_id: str):
    """
    Retrieve series for a specific study from Orthanc.
    """
    try:
        series = get_series_by_study(study_id)
        if not series:
            raise HTTPException(status_code=404, detail=f"No series found for study ID {study_id}")
        return {"series": series}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve series: {str(e)}")