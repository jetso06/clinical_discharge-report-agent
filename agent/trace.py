def add_trace(state, reasoning, action, result, next_step):

    state.trace.append(
        {
            "reasoning": reasoning,
            "action": action,
            "result": result,
            "next_step": next_step,
        }
    )
