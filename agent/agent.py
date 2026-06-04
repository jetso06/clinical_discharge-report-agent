from agent.planner import determine_next_action
from agent.trace import add_trace
from tools.clinician_review import flag_missing_fields
from tools.conflict_resolver import resolve_conflicts

MAX_ITERATIONS = 5


def run_agent(state):

    while state.iteration_count < MAX_ITERATIONS:
        state.iteration_count += 1

        add_trace(
            state,
            reasoning="Agent iteration started",
            action="increment_iteration",
            result=f"Iteration {state.iteration_count}",
            next_step="planner",
        )

        next_action = determine_next_action(state)

        add_trace(
            state,
            reasoning="Planner evaluated state",
            action="determine_next_action",
            result=f"Selected: {next_action}. Missing fields: {state.missing_fields}",
            next_step=next_action,
        )

        if next_action == "search_missing":
            flag_missing_fields(state)

            add_trace(
                state,
                reasoning="Missing fields found",
                action="flag_missing_fields",
                result=f"{len(state.review_flags)} flags created",
                next_step="generate_summary",
            )

            break

        elif next_action == "resolve_conflicts":
            state.resolutions = resolve_conflicts(state)

            add_trace(
                state,
                reasoning="Conflicts detected",
                action="resolve_conflicts",
                result=f"{len(state.resolutions)} resolutions created",
                next_step="generate_summary",
            )

            break

        elif next_action == "generate_summary":
            break

    return state
