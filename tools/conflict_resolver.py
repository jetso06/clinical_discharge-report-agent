def resolve_conflicts(state):

    resolutions = []

    for conflict in state.conflicts:
        if conflict == "Patient discharged with pending results":
            resolutions.append(
                {
                    "conflict": conflict,
                    "resolution": "Escalated for clinician review",
                }
            )

        else:
            resolutions.append(
                {
                    "conflict": conflict,
                    "resolution": "Manual review required",
                }
            )

    return resolutions
