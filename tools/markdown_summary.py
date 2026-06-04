def create_markdown_summary(summary):

    md = []

    md.append("# Discharge Summary\n")

    demographics = summary.get("patient_demographics", {})

    md.append("## Patient Information\n")

    if isinstance(demographics, dict):
        md.append(f"- Weight: {demographics.get('weight', 'MISSING')}")

        md.append(f"- Age: {demographics.get('age', 'MISSING')}")

        md.append(f"- Gender: {demographics.get('gender', 'MISSING')}")

    md.append(f"\n## Admission Date\n{summary.get('admission_date', 'MISSING')}")

    md.append(f"\n## Discharge Date\n{summary.get('discharge_date', 'MISSING')}")

    md.append(
        f"\n## Principal Diagnosis\n{summary.get('principal_diagnosis', 'MISSING')}"
    )

    md.append("\n## Secondary Diagnoses")

    for item in summary.get("secondary_diagnoses", []):
        md.append(f"- {item}")

    md.append("\n## Medication Reconciliation")

    meds = summary.get("medication_reconciliation", {})

    md.append("\n### Added")

    for item in meds.get("added", []):
        md.append(f"- {item}")

    md.append("\n### Stopped")

    for item in meds.get("stopped", []):
        md.append(f"- {item}")

    md.append("\n## Pending Results")

    pending = summary.get("pending_results", [])

    if isinstance(pending, str):
        pending = [pending]

    for item in pending:
        md.append(f"- {item}")

    md.append("\n## Conflicts")

    for item in summary.get("conflicts", []):
        md.append(f"- {item}")

    md.append("\n## Clinician Review Flags")

    for item in summary.get("clinician_review_flags", []):
        md.append(f"- {item}")

    return "\n".join(md)
