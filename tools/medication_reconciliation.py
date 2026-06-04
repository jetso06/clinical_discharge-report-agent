def normalize_medications(value):

    if value in [None, "", "MISSING"]:
        return []

    if isinstance(value, str):
        return [value]

    if isinstance(value, dict):
        return [value.get("name", str(value))]

    if isinstance(value, list):
        result = []

        for item in value:
            if isinstance(item, dict):
                result.append(item.get("name", str(item)))

            else:
                result.append(str(item))

        return result

    return [str(value)]


def reconcile_medications(state):

    facts = state.facts

    admission = set(normalize_medications(facts.get("admission_medications", [])))

    discharge = set(normalize_medications(facts.get("discharge_medications", [])))

    added = list(discharge - admission)

    stopped = list(admission - discharge)

    reconciliation = {
        "continued": list(admission & discharge),
        "added": added,
        "stopped": stopped,
        "changed": [],
        "review_required": [],
    }

    if added:
        reconciliation["review_required"].append(
            "Medication additions lack documented rationale"
        )

    if stopped:
        reconciliation["review_required"].append(
            "Medication discontinuations require review"
        )

    if not discharge:
        reconciliation["review_required"].append("No discharge medications found")

    return reconciliation
