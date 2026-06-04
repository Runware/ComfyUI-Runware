"""
Runware Image Inference Settings Structured Prompt
Builds settings.structuredPrompt for Ideogram 4.0 and compatible models.
Connect the output to Runware Image Inference Settings → structuredPrompt.
Mutually exclusive with positivePrompt at the API level.
"""

import json
from typing import Any, Dict, List, Tuple


class RunwareImageInferenceSettingsStructuredPrompt:
    """Ideogram-style structured JSON prompt for image inference settings."""

    _ELEMENT_SLOTS = 8

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {
            "high_level_description": ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": "Global scene summary (required).",
            }),
            "background": ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": "compositional_deconstruction.background — setting/surface/atmosphere, not discrete subjects.",
            }),
            "useStyleDescription": ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": "Include style_description from JSON below.",
            }),
            "style_description": ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": "style_description object as JSON (aesthetics, lighting, photo OR art_style, medium, color_palette). Only when 'Use Style Description' is enabled.",
            }),
            "useElementsJson": ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": "Set elements from a JSON array instead of element slots 1–8.",
            }),
            "elementsJson": ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": "JSON array of element objects ({type, desc, text?, bbox?, color_palette?}). Only when 'Use Elements JSON' is enabled.",
            }),
        }

        for i in range(1, cls._ELEMENT_SLOTS + 1):
            optional[f"use_element_{i}"] = ("BOOLEAN", {
                "default": False,
                "label_on": "Enabled",
                "label_off": "Disabled",
                "tooltip": f"Include element slot {i} in compositional_deconstruction.elements.",
            })
            optional[f"element_type_{i}"] = (["obj", "text"], {
                "default": "obj",
                "tooltip": f"Element {i} type: obj (desc interpreted) or text (text rendered literally).",
            })
            optional[f"element_desc_{i}"] = ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": f"Element {i} desc — natural language treatment/position notes.",
            })
            optional[f"element_text_{i}"] = ("STRING", {
                "multiline": True,
                "default": "",
                "tooltip": f"Element {i} text — literal copy for type text only.",
            })
            optional[f"element_bbox_{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Element {i} optional bbox JSON: [y_min, x_min, y_max, x_max] in 0–1000 coords.",
            })
            optional[f"element_color_palette_{i}"] = ("STRING", {
                "default": "",
                "tooltip": f"Element {i} optional hex colours, comma-separated (e.g. #1F3B26,#7A5A2F).",
            })

        return {"required": {}, "optional": optional}

    RETURN_TYPES = ("RUNWAREIMAGEINFERENCESTRUCTUREDPROMPT",)
    RETURN_NAMES = ("structuredPrompt",)
    FUNCTION = "build_structured_prompt"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Build settings.structuredPrompt for Ideogram 4.0 (snake_case schema) from "
        "high_level_description, background, style_description, and elements. "
        "Connect to Runware Image Inference Settings. Do not send positivePrompt in the same request."
    )

    @staticmethod
    def _parse_json_object(raw: str, field_name: str) -> Dict[str, Any]:
        text = (raw or "").strip()
        if not text:
            raise ValueError(f"{field_name} is empty.")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"{field_name} must be valid JSON: {e}") from e
        if not isinstance(parsed, dict):
            raise ValueError(f"{field_name} must be a JSON object.")
        return parsed

    @staticmethod
    def _parse_json_array(raw: str, field_name: str) -> List[Any]:
        text = (raw or "").strip()
        if not text:
            raise ValueError(f"{field_name} is empty.")
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"{field_name} must be valid JSON: {e}") from e
        if not isinstance(parsed, list):
            raise ValueError(f"{field_name} must be a JSON array.")
        return parsed

    @classmethod
    def _build_element_from_slot(cls, kwargs: Dict[str, Any], index: int) -> Dict[str, Any]:
        el_type = str(kwargs.get(f"element_type_{index}", "obj")).strip() or "obj"
        if el_type not in ("obj", "text"):
            raise ValueError(f"element_type_{index} must be obj or text.")

        element: Dict[str, Any] = {"type": el_type}

        desc = str(kwargs.get(f"element_desc_{index}") or "").strip()
        if desc:
            element["desc"] = desc

        if el_type == "text":
            text = str(kwargs.get(f"element_text_{index}") or "").strip()
            if text:
                element["text"] = text

        bbox_raw = str(kwargs.get(f"element_bbox_{index}") or "").strip()
        if bbox_raw:
            try:
                bbox = json.loads(bbox_raw)
            except json.JSONDecodeError as e:
                raise ValueError(f"element_bbox_{index} must be valid JSON: {e}") from e
            if not isinstance(bbox, list):
                raise ValueError(f"element_bbox_{index} must be a JSON array.")
            element["bbox"] = bbox

        palette_raw = str(kwargs.get(f"element_color_palette_{index}") or "").strip()
        if palette_raw:
            palette = [h.strip() for h in palette_raw.split(",") if h.strip()]
            if palette:
                element["color_palette"] = palette

        if el_type == "text" and "text" not in element and not desc:
            raise ValueError(
                f"Element slot {index}: type text requires element_text_{index} or element_desc_{index}."
            )
        if el_type == "obj" and not desc:
            raise ValueError(f"Element slot {index}: type obj requires element_desc_{index}.")

        return element

    @classmethod
    def _collect_elements(cls, kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        if kwargs.get("useElementsJson", False):
            return cls._parse_json_array(
                kwargs.get("elementsJson", ""),
                "elementsJson",
            )

        elements: List[Dict[str, Any]] = []
        for i in range(1, cls._ELEMENT_SLOTS + 1):
            if not kwargs.get(f"use_element_{i}", False):
                continue
            elements.append(cls._build_element_from_slot(kwargs, i))
        return elements

    def build_structured_prompt(self, **kwargs) -> Tuple[Dict[str, Any]]:
        hld = str(kwargs.get("high_level_description") or "").strip()
        if not hld:
            raise ValueError("high_level_description is required.")

        structured: Dict[str, Any] = {"high_level_description": hld}

        if kwargs.get("useStyleDescription", False):
            style_raw = kwargs.get("style_description", "")
            structured["style_description"] = self._parse_json_object(
                style_raw,
                "style_description",
            )

        comp: Dict[str, Any] = {}
        background = str(kwargs.get("background") or "").strip()
        if background:
            comp["background"] = background

        elements = self._collect_elements(kwargs)
        if elements:
            comp["elements"] = elements

        if comp:
            structured["compositional_deconstruction"] = comp

        return (structured,)


NODE_CLASS_MAPPINGS = {
    "RunwareImageInferenceSettingsStructuredPrompt": RunwareImageInferenceSettingsStructuredPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareImageInferenceSettingsStructuredPrompt": "Runware Image Inference Settings Structured Prompt",
}
