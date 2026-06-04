# Clinical Discharge Agent

## Overview

This project implements an agentic AI system that converts unstructured clinical source notes into a structured discharge summary draft for clinician review.

The system processes patient PDFs, extracts relevant clinical information, identifies missing data, detects potential conflicts, performs medication reconciliation, and generates a structured discharge summary while maintaining strict safety guardrails.

The primary design goal is clinical safety: the system never fabricates information and always escalates uncertainty for clinician review.

---

# Architecture

Patient PDF

↓

PDF Extraction (PyMuPDF)

↓

OCR Fallback (Tesseract)

↓

Fact Extraction (Gemini 2.5 Flash)

↓

Conflict Detection

↓

Agent Planner

↓

Missing Data Review OR Conflict Resolution

↓

Medication Reconciliation

↓

Discharge Summary Generation

↓

Trace Generation

---

# Agent Loop Design

The system uses a stateful agent loop rather than a fixed pipeline.

The agent:

1. Extracts structured facts from source notes.
2. Detects conflicts and missing information.
3. Uses a planner to determine the next action.
4. Routes execution to appropriate tools.
5. Records reasoning and actions in a trace.
6. Generates a clinician-review draft.

A hard iteration limit prevents infinite execution loops.

---

# Features

## PDF Ingestion

The system reads clinical source-note PDFs directly.

Tools used:

* PyMuPDF
* Tesseract OCR

OCR is used when embedded PDF text is unavailable or incomplete.

---

## Fact Extraction

The extraction stage identifies:

* Patient demographics
* Admission date
* Discharge date
* Principal diagnosis
* Secondary diagnoses
* Procedures
* Allergies
* Follow-up instructions
* Pending results
* Discharge condition
* Medications

Structured facts are saved to:

output/extracted_facts.json

---

## Missing Data Handling

The system never invents information.

If required information cannot be found:

* The field is marked as MISSING
* A clinician review flag is created
* The information is surfaced to the reviewer

Example:

patient_demographics = MISSING

---

## Medication Reconciliation

Admission and discharge medications are compared.

The system identifies:

* Added medications
* Stopped medications
* Continued medications

If a medication change lacks documented rationale, it is flagged for review rather than silently accepted.

---

## Conflict Detection

The agent detects clinically relevant issues requiring escalation.

Example:

* Patient discharged with pending laboratory results

Detected conflicts are surfaced to clinicians rather than automatically resolved.

---

## Conflict Resolution (Enhancement)

A conflict-resolution tool was added as an agent action.

When conflicts are detected and no higher-priority safety issue exists, the agent can generate a recommended resolution.

Example:

* Conflict: Patient discharged with pending results
* Resolution: Escalated for clinician review

---

# No-Fabrication Guardrail

Clinical safety is the highest-priority requirement.

The system is designed to:

* Never invent patient information
* Never guess missing values
* Explicitly mark unknown information as missing
* Escalate uncertainty through clinician review flags

The generated output is always a draft for review and is never considered a finalized clinical document.

---

# Failure Handling

The agent is designed to fail safely.

Implemented safeguards:

* Missing information is marked as MISSING
* Empty extraction results are escalated for review
* Tool failures are surfaced rather than silently ignored
* The agent maintains execution traces for debugging
* A hard iteration cap prevents infinite loops

The system prioritizes transparency over attempting to recover by guessing information.

---

# Observability

Every major decision is recorded.

Trace entries include:

* Reasoning
* Action selected
* Result
* Next step

These traces are stored in:

traces/trace.json

---

# Running the Project

Create a virtual environment:

python -m venv .venv

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

Run:

python main.py

---

# Generated Outputs

After running:

python main.py

the following outputs are generated:

### Extracted Facts

output/extracted_facts.json

Contains structured clinical facts extracted from the source documents.

### Discharge Summary (JSON)

output/discharge_summary.json

Machine-readable discharge summary including diagnoses, procedures, medications, pending results, clinician review flags, conflicts, and medication reconciliation.

### Discharge Summary (Markdown)

output/discharge_summary.md

Human-readable discharge summary draft intended for clinician review.

### Agent Report

output/agent_report.md

Summary of agent decisions, safety events, conflicts, and review flags.

### Agent Trace

traces/trace.json

Complete reasoning trace showing planner decisions, actions taken, results, and next steps.

---

# Example Output

Sample generated outputs are included in the repository:

* output/discharge_summary.json
* output/discharge_summary.md
* output/agent_report.md
* traces/trace.json

These files demonstrate discharge summary generation, medication reconciliation, clinician review flags, conflict detection, and agent observability.

---

# Technology Stack

* Python
* Gemini 2.5 Flash
* PyMuPDF
* Tesseract OCR
* Pydantic

---

# Part 2 Status

Part 2 was not fully implemented due to time constraints.

As an enhancement, a conflict-resolution capability was added to the agent workflow.

Given more time, the next planned steps would be:

* Simulated clinician reviewer
* Edit-based reward signal
* Learning from corrections
* Improvement tracking over time
* Evaluation on held-out patient cases

---

# Limitations

* OCR quality depends on source document quality.
* Medication extraction may be affected by handwriting or OCR errors.
* Current conflict detection uses a limited set of rule-based checks.
* The system is intended for clinician review and not autonomous clinical decision-making.

---

# Future Work

Potential improvements include:

* Additional conflict-detection rules
* Drug interaction lookup tools
* Improved medication normalization
* Multi-patient batch processing
* Learning from clinician edits
* Stronger evaluation framework

---

# Safety Statement

This system is intended as a clinical decision-support prototype.

It is not designed to replace clinician judgment.

All generated outputs must be reviewed and approved by a qualified healthcare professional before use.
