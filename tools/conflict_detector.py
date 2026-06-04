def detect_conflicts(state):

    facts = state.facts

    conflicts = []

    if facts.get("principal_diagnosis") == "MISSING":
        conflicts.append("Principal diagnosis missing")

    if facts.get("discharge_condition") == "MISSING":
        conflicts.append("Discharge condition missing")

    pending = facts.get("pending_results")

    if pending:
        conflicts.append("Patient discharged with pending results")

    return conflicts
