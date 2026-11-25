"""Bounded, client-neutral context handling for workflow-context dialogue."""
from __future__ import annotations

import json
from typing import Any, Dict

CONTEXT_CONTRACT_VERSION = "1"
MAX_CONTEXT_BYTES = 12_000
MAX_CONTEXT_DEPTH = 4
MAX_CONTEXT_KEYS = 32
MAX_CONTEXT_ITEMS = 20
MAX_CONTEXT_STRING_CHARS = 800

WORKFLOW_ASSESSMENT_STEP_STATUSES = frozenset({"completed", "failed", "skipped", "not_run", "unavailable"})
WORKFLOW_ASSESSMENT_REASON_CATEGORIES = frozenset({"user_skipped", "technical_failure", "missing_dependency", "not_applicable"})
WORKFLOW_ASSESSMENT_IMPACT_CODES = frozenset({
    "analysis_output_incomplete",
    "validation_evidence_unavailable",
    "diagnostic_evidence_unavailable",
    "configuration_or_data_issue_requires_review",
    "results_interpretation_requires_review",
    "impact_unknown_requires_review",
    "quality_improvement_opportunity_not_assessed",
})


class WorkflowContextContractError(ValueError):
    """Raised when a client context cannot be safely bounded for prompting."""


def _normalize_workflow_assessment(value: Any) -> Dict[str, Any]:
    """Validate the portable, client-owned workflow assessment envelope."""
    if not isinstance(value, dict):
        raise WorkflowContextContractError("workflow_assessment must be an object")
    assessment = value
    steps = assessment.get("steps", [])
    if not isinstance(steps, list):
        raise WorkflowContextContractError("workflow_assessment.steps must be a list")
    if len(steps) > MAX_CONTEXT_ITEMS:
        raise WorkflowContextContractError(f"workflow_assessment.steps cannot exceed {MAX_CONTEXT_ITEMS} entries")

    normalized_steps = []
    for step in steps:
        if not isinstance(step, dict):
            raise WorkflowContextContractError("workflow_assessment.steps entries must be objects")
        step_id = step.get("id")
        kind = step.get("kind")
        status = step.get("status")
        if not all(isinstance(item, str) and item.strip() and len(item) <= 120 for item in (step_id, kind, status)):
            raise WorkflowContextContractError("workflow_assessment.steps entries require non-empty id, kind, and status")
        if status not in WORKFLOW_ASSESSMENT_STEP_STATUSES:
            raise WorkflowContextContractError(f"unsupported workflow_assessment step status: {status}")
        reason_category = step.get("reason_category")
        if reason_category is not None and reason_category not in WORKFLOW_ASSESSMENT_REASON_CATEGORIES:
            raise WorkflowContextContractError(f"unsupported workflow_assessment reason_category: {reason_category}")
        impact_codes = step.get("impact_codes", [])
        if (
            not isinstance(impact_codes, list)
            or len(impact_codes) > MAX_CONTEXT_ITEMS
            or any(code not in WORKFLOW_ASSESSMENT_IMPACT_CODES for code in impact_codes)
        ):
            raise WorkflowContextContractError("workflow_assessment impact_codes must use supported codes")
        explanation = step.get("impact_explanation")
        if explanation is not None and (not isinstance(explanation, str) or len(explanation) > 300):
            raise WorkflowContextContractError("workflow_assessment impact_explanation must be a string of at most 300 characters")
        normalized_step = {
            "id": step_id,
            "kind": kind,
            "status": status,
            "impact_codes": impact_codes,
        }
        if reason_category is not None:
            normalized_step["reason_category"] = reason_category
        if explanation:
            normalized_step["impact_explanation"] = explanation
        evidence_scope = step.get("evidence_scope")
        if evidence_scope is not None:
            if (
                not isinstance(evidence_scope, list)
                or len(evidence_scope) > MAX_CONTEXT_ITEMS
                or any(not isinstance(scope, str) or not scope or len(scope) > 120 for scope in evidence_scope)
            ):
                raise WorkflowContextContractError("workflow_assessment evidence_scope must be a list of non-empty strings")
            normalized_step["evidence_scope"] = evidence_scope
        normalized_steps.append(normalized_step)

    return {"assessment_version": 1, "steps": normalized_steps}


def _compact(value: Any, depth: int = 0) -> Any:
    if depth >= MAX_CONTEXT_DEPTH:
        return "[omitted: maximum context depth reached]"
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        if len(value) <= MAX_CONTEXT_STRING_CHARS:
            return value
        return value[:MAX_CONTEXT_STRING_CHARS] + f"... [truncated {len(value) - MAX_CONTEXT_STRING_CHARS} chars]"
    if isinstance(value, (list, tuple)):
        result = [_compact(item, depth + 1) for item in value[:MAX_CONTEXT_ITEMS]]
        if len(value) > MAX_CONTEXT_ITEMS:
            result.append(f"[omitted {len(value) - MAX_CONTEXT_ITEMS} additional items]")
        return result
    if isinstance(value, dict):
        result: Dict[str, Any] = {}
        items = list(value.items())
        for key, item in items[:MAX_CONTEXT_KEYS]:
            if not isinstance(key, str):
                continue
            result[key[:120]] = _compact(item, depth + 1)
        if len(items) > MAX_CONTEXT_KEYS:
            result["_omitted_keys"] = len(items) - MAX_CONTEXT_KEYS
        return result
    return str(value)[:MAX_CONTEXT_STRING_CHARS]


def normalize_workflow_context(current_context: Dict[str, Any] | None) -> Dict[str, Any]:
    """Return a bounded JSON-safe context while preserving legacy client keys.

    Clients may use the documented envelope categories or legacy fields during
    migration. This function does not attempt PHI detection: clients must never
    submit patient-level data. It enforces deterministic shape and size bounds
    before an LLM prompt is assembled.
    """
    if current_context is None:
        return {}
    if not isinstance(current_context, dict):
        raise WorkflowContextContractError("current_context must be an object")
    normalized = _compact(current_context)
    if "workflow_assessment" in normalized:
        normalized["workflow_assessment"] = _normalize_workflow_assessment(current_context["workflow_assessment"])
    try:
        encoded = json.dumps(normalized, ensure_ascii=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise WorkflowContextContractError("current_context must be JSON serializable") from exc
    if len(encoded.encode("utf-8")) > MAX_CONTEXT_BYTES:
        raise WorkflowContextContractError(
            f"current_context exceeds the {MAX_CONTEXT_BYTES}-byte dialogue contract limit"
        )
    return normalized
