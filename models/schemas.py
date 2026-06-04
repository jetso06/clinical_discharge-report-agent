from typing import List

from pydantic import BaseModel


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str
    status: str


class DischargeSummary(BaseModel):
    patient_demographics: str
    admission_date: str
    discharge_date: str

    principal_diagnosis: str

    secondary_diagnoses: List[str]

    hospital_course: str

    procedures: List[str]

    discharge_medications: List[Medication]

    allergies: List[str]

    follow_up: List[str]

    pending_results: List[str]

    discharge_condition: str

    clinician_review_flags: List[str]
