from tools.medication_reconciliation import reconcile_medications


def generate_summary(state):

    facts = state.facts

    summary = {
        "patient_demographics": facts.get("patient_demographics", "MISSING"),
        "admission_date": facts.get("admission_date", "MISSING"),
        "discharge_date": facts.get("discharge_date", "MISSING"),
        "principal_diagnosis": facts.get("principal_diagnosis", "MISSING"),
        "secondary_diagnoses": facts.get("secondary_diagnoses", []),
        "hospital_course": facts.get("hospital_course", "MISSING"),
        "procedures": facts.get("procedures", []),
        "allergies": facts.get("allergies", "MISSING"),
        "follow_up": facts.get("follow_up", []),
        "pending_results": facts.get("pending_results", []),
        "discharge_condition": facts.get("discharge_condition", "MISSING"),
        "medication_reconciliation": reconcile_medications(state),
        "clinician_review_flags": state.review_flags,
    }

    return summary
