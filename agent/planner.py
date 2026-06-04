REQUIRED_FIELDS = [
    "patient_demographics",
    "admission_date",
    "discharge_date",
    "principal_diagnosis",
    "hospital_course",
    "discharge_condition",
]


def is_missing(value):

    if value is None:
        return True

    if isinstance(value, str):
        normalized = value.strip().lower()

        if normalized in [
            "",
            "missing",
            "not specified",
            "unknown",
            "n/a",
        ]:
            return True

    return False


def determine_next_action(state):

    missing = []

    for field in REQUIRED_FIELDS:
        if field not in state.facts:
            missing.append(field)

            continue

        if is_missing(state.facts[field]):
            missing.append(field)

    state.missing_fields = missing

    if missing:
        return "search_missing"

    if state.conflicts:
        return "resolve_conflicts"

    return "generate_summary"
