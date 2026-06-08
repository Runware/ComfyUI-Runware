"""
Runware Image Inference Settings Scoring Rubric
Builds settings.scoringRubric[] for Riverflow 2.5 (1–8 dimensions).
"""

from typing import Any, Dict, List, Tuple

_MAX_SCORE_GUIDANCE = 5
_MAX_RUBRIC_COMBINE = 4


def _build_score_guidance(kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
    guidance: List[Dict[str, Any]] = []

    for i in range(1, _MAX_SCORE_GUIDANCE + 1):
        if not kwargs.get(f"useScoreGuidance{i}", False):
            continue

        score = kwargs.get(f"score{i}")
        description = (kwargs.get(f"guidanceDescription{i}") or "").strip()
        if score is None or not description:
            continue

        guidance.append({
            "score": float(score),
            "description": description,
        })

    return guidance


def _build_rubric_entry(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    entry: Dict[str, Any] = {
        "key": (kwargs.get("key") or "").strip(),
        "label": (kwargs.get("label") or "").strip(),
        "description": (kwargs.get("description") or "").strip(),
        "weight": float(kwargs.get("weight", 1.0)),
    }

    if kwargs.get("usePassingScore", False):
        entry["passingScore"] = float(kwargs.get("passingScore", 0.0))

    guidance = _build_score_guidance(kwargs)
    if guidance:
        entry["scoreGuidance"] = guidance

    return entry


class RunwareImageInferenceSettingsScoringRubric:
    """Build one scoringRubric dimension for settings.scoringRubric."""

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {
            "usePassingScore": ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": "Include passingScore for this scoring dimension.",
            }),
            "passingScore": ("FLOAT", {
                "default": 0.5,
                "min": 0.0,
                "max": 1.0,
                "step": 0.01,
                "tooltip": "Optional dimension floor from 0 to 1. Only used when usePassingScore is enabled.",
            }),
        }

        for i in range(1, _MAX_SCORE_GUIDANCE + 1):
            optional[f"useScoreGuidance{i}"] = ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": f"Include scoreGuidance anchor {i} (up to {_MAX_SCORE_GUIDANCE} per dimension).",
            })
            optional[f"score{i}"] = ("FLOAT", {
                "default": 0.0,
                "min": 0.0,
                "max": 1.0,
                "step": 0.01,
                "tooltip": f"Normalized score anchor (0–1) for scoreGuidance entry {i}.",
            })
            optional[f"guidanceDescription{i}"] = ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": f"What score anchor {i} means for the judge.",
            })

        return {
            "required": {
                "key": ("STRING", {
                    "default": "",
                    "tooltip": "Unique machine-readable dimension key (e.g. composition, lighting).",
                }),
                "label": ("STRING", {
                    "default": "",
                    "tooltip": "Short human-readable dimension label.",
                }),
                "description": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Judging criteria for this score dimension.",
                }),
                "weight": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 100.0,
                    "step": 0.01,
                    "tooltip": "Positive scoring weight. Weights are normalized internally.",
                }),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCESCORINGRUBRIC",)
    RETURN_NAMES = ("scoringRubric",)
    FUNCTION = "build_scoring_rubric"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Define one settings.scoringRubric[] dimension for Riverflow 2.5 (key, label, description, weight, "
        "optional passingScore and up to 5 scoreGuidance anchors). Connect to Runware Image Inference Settings, "
        "or use Runware Image Inference Settings Scoring Rubric Combine for up to 4 dimensions."
    )

    def build_scoring_rubric(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        return ([_build_rubric_entry(kwargs)],)


class RunwareImageInferenceSettingsScoringRubricCombine:
    """Combine up to 4 Scoring Rubric node outputs into settings.scoringRubric."""

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {}
        for i in range(2, _MAX_RUBRIC_COMBINE + 1):
            optional[f"Scoring Rubric {i}"] = ("RUNWAREIMAGEINFERENCESCORINGRUBRIC", {
                "tooltip": f"Optional scoring rubric dimension {i} (connect Runware Image Inference Settings Scoring Rubric).",
            })

        return {
            "required": {
                "Scoring Rubric 1": ("RUNWAREIMAGEINFERENCESCORINGRUBRIC", {
                    "tooltip": "First scoring rubric dimension (connect Runware Image Inference Settings Scoring Rubric).",
                }),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCESCORINGRUBRIC",)
    RETURN_NAMES = ("scoringRubric",)
    FUNCTION = "combine_scoring_rubric"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Combine up to 4 Runware Image Inference Settings Scoring Rubric outputs into settings.scoringRubric. "
        "Connect scoringRubric to Runware Image Inference Settings."
    )

    def combine_scoring_rubric(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        combined: List[Dict[str, Any]] = []

        for i in range(1, _MAX_RUBRIC_COMBINE + 1):
            chunk = kwargs.get(f"Scoring Rubric {i}")
            if chunk is not None and isinstance(chunk, list):
                combined.extend(
                    entry for entry in chunk
                    if isinstance(entry, dict) and len(entry) > 0
                )

        return (combined,)
