"""Governed gate deliberation request/response models."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


VALID_GATES = frozenset({"G1", "G2", "G3", "G4", "G5"})


class SubjectArtifact(BaseModel):
    """Artifact reviewed at a council gate."""

    label: str
    path: str


class DeliberateRequest(BaseModel):
    """POST /deliberate body — gate-aware council invocation."""

    gate: str = Field(description="Council gate id (G1–G5)")
    program_id: str
    query: str = Field(description="Deliberation prompt / subject narrative")
    subject_artifacts: List[SubjectArtifact] = Field(default_factory=list)
    module_id: Optional[str] = None
    phase_id: Optional[str] = None
    tenant_id: Optional[str] = None
    run_id: Optional[str] = None


class DeliberateResponse(BaseModel):
    """Three-stage council output for LinkSkills mapping."""

    gate: str
    program_id: str
    stage1: List[Dict[str, Any]]
    stage2: List[Dict[str, Any]]
    stage3: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    deliberation_ref: str


def build_gate_prompt(request: DeliberateRequest) -> str:
    """Compose the user query sent to the 3-stage council."""
    artifact_lines = "\n".join(
        f"- {item.label}: {item.path}" for item in request.subject_artifacts
    )
    scope = []
    if request.module_id:
        scope.append(f"module_id={request.module_id}")
    if request.phase_id:
        scope.append(f"phase_id={request.phase_id}")
    scope_line = f"Scope: {', '.join(scope)}" if scope else ""

    return f"""LiNKtrend council gate {request.gate} deliberation for program "{request.program_id}".

{scope_line}

Subject:
{request.query}

Artifacts under review:
{artifact_lines or "(none listed)"}

Evaluate from security, architecture, developer experience, QA, and product perspectives.
State PASS, WARN, or BLOCKER per concern. If any BLOCKER exists, say BLOCKER explicitly in the synthesis.
"""
