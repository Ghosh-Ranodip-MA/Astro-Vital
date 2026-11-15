from collections.abc import Sequence

from backend.models import Observation

RULE_VERSION = "demo-trend-v1"


def evaluate_trend(observations: Sequence[Observation]) -> dict | None:
    """Return a source-linked demo flag; this is not a clinical threshold."""
    readings = sorted(
        (item for item in observations if item.data_type == "heart_rate" and item.value_numeric is not None),
        key=lambda item: item.observed_at,
    )
    if len(readings) < 6:
        return None
    baseline = readings[-6:-2]
    recent = readings[-2:]
    baseline_mean = sum(item.value_numeric for item in baseline) / len(baseline)
    recent_mean = sum(item.value_numeric for item in recent) / len(recent)
    if baseline_mean <= 0 or recent_mean < baseline_mean * 1.2:
        return None
    evidence = [item.id for item in (*baseline, *recent)]
    return {
        "rule_version": RULE_VERSION,
        "title": "Synthetic trend flagged for review",
        "explanation": (
            "Demo-only rule: the mean of the final two synthetic heart-rate samples is "
            "more than 20% above the mean of the prior four samples. This is not a "
            "medical threshold, diagnosis, or validated prediction."
        ),
        "evidence_ids": evidence,
    }
