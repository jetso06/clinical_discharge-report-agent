from typing import Any, Dict, List

from pydantic import BaseModel


class AgentState(BaseModel):
    facts: Dict[str, Any] = {}

    missing_fields: List[str] = []

    conflicts: List[str] = []

    resolutions: List[Dict[str, Any]] = []

    review_flags: List[Dict[str, Any]] = []

    trace: List[Dict[str, Any]] = []

    iteration_count: int = 0
