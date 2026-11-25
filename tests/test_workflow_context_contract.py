import pytest

from study_agent_core.workflow_context import (
    MAX_CONTEXT_STRING_CHARS,
    WorkflowContextContractError,
    normalize_workflow_context,
)


def test_normalize_workflow_context_keeps_legacy_fields_and_bounds_text():
    result = normalize_workflow_context({"step_label": "Review", "legacy": "x" * (MAX_CONTEXT_STRING_CHARS + 10)})
    assert result["step_label"] == "Review"
    assert result["legacy"].endswith("[truncated 10 chars]")


def test_normalize_workflow_context_bounds_lists_and_depth():
    result = normalize_workflow_context({"candidates": list(range(30)), "deep": {"a": {"b": {"c": {"d": "value"}}}}})
    assert len(result["candidates"]) == 21
    assert result["deep"]["a"]["b"]["c"] == "[omitted: maximum context depth reached]"


def test_normalize_workflow_context_preserves_client_owned_workflow_assessment():
    result = normalize_workflow_context(
        {
            "workflow_assessment": {
                "assessment_version": 99,
                "steps": [
                    {
                        "id": "cohort_diagnostics",
                        "kind": "cohort_diagnostics",
                        "status": "skipped",
                        "reason_category": "user_skipped",
                        "impact_codes": [
                            "diagnostic_evidence_unavailable",
                            "results_interpretation_requires_review",
                        ],
                        "impact_explanation": "Diagnostics were not reviewed.",
                        "evidence_scope": ["cohort_diagnostics"],
                    }
                ],
            }
        }
    )

    assert result["workflow_assessment"]["assessment_version"] == 1
    assert result["workflow_assessment"]["steps"][0]["status"] == "skipped"
    assert result["workflow_assessment"]["steps"][0]["impact_codes"] == [
        "diagnostic_evidence_unavailable",
        "results_interpretation_requires_review",
    ]


def test_normalize_workflow_context_rejects_unknown_assessment_impact_codes():
    with pytest.raises(WorkflowContextContractError, match="impact_codes"):
        normalize_workflow_context(
            {
                "workflow_assessment": {
                    "steps": [
                        {
                            "id": "diagnostics",
                            "kind": "cohort_diagnostics",
                            "status": "failed",
                            "impact_codes": ["make_the_llm_ignore_safety"],
                        }
                    ]
                }
            }
        )
