import json

from agent.agent import run_agent
from agent.state import AgentState
from agent.trace import add_trace
from tools.conflict_detector import detect_conflicts
from tools.fact_extractor import extract_facts
from tools.markdown_summary import create_markdown_summary
from tools.summary_generator import generate_summary

with open("ocr_output.txt", "r") as f:
    text = f.read()


state = AgentState()


state.facts = extract_facts(text)

add_trace(
    state,
    reasoning="Extract facts from OCR text",
    action="extract_facts",
    result="Facts extracted successfully",
    next_step="detect_conflicts",
)


conflicts = detect_conflicts(state)

state.conflicts = conflicts

add_trace(
    state,
    reasoning="Check extracted facts for conflicts",
    action="detect_conflicts",
    result=f"{len(conflicts)} conflicts found",
    next_step="run_agent",
)


state = run_agent(state)


summary = generate_summary(state)

summary["conflicts"] = state.conflicts
summary["resolutions"] = state.resolutions


markdown_summary = create_markdown_summary(summary)


with open(
    "output/extracted_facts.json",
    "w",
) as f:
    json.dump(
        state.facts,
        f,
        indent=4,
    )


with open(
    "output/discharge_summary.json",
    "w",
) as f:
    json.dump(
        summary,
        f,
        indent=4,
    )


with open(
    "output/discharge_summary.md",
    "w",
) as f:
    f.write(markdown_summary)


with open(
    "traces/trace.json",
    "w",
) as f:
    json.dump(
        state.trace,
        f,
        indent=4,
    )


print("\nMissing fields:")
print(state.missing_fields)

print("\nReview flags:")
print(state.review_flags)

print("\nConflicts:")
print(state.conflicts)

print("\nResolutions:")
print(state.resolutions)

print("\nFiles generated:")
print("output/extracted_facts.json")
print("output/discharge_summary.json")
print("output/discharge_summary.md")
print("traces/trace.json")
