def flag_missing_fields(state):

    for field in state.missing_fields:
        state.review_flags.append(
            {
                "field": field,
                "reason": "Information not found in source documents",
            }
        )

    demographics = state.facts.get("patient_demographics", {})

    if isinstance(demographics, dict):
        age = demographics.get("age", "")

        gender = demographics.get("gender", "")

        if str(age).lower() in ["not specified", "missing", ""]:
            state.review_flags.append(
                {
                    "field": "patient_demographics.age",
                    "reason": "Age not available",
                }
            )

        if str(gender).lower() in ["not specified", "missing", ""]:
            state.review_flags.append(
                {
                    "field": "patient_demographics.gender",
                    "reason": "Gender not available",
                }
            )

    return state.review_flags
