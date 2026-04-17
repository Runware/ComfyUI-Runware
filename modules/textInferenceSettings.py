import json
from typing import Any, Dict, List, Tuple


class RunwareTextInferenceSettings:
    """Optional generation controls for Runware Text Inference (flat task.settings per API)."""

    _MAX_SYSTEM_CHARS = 200000
    _MAX_TOKENS_CAP = 131072
    _MAX_TOP_K = 100647
    _MAX_STOP_ITEMS = 5
    _MAX_STOP_ITEM_CHARS = 50

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useSystemPrompt": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include systemPrompt in settings.",
                }),
                "systemPrompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "System instruction (max 200,000 chars).",
                }),
                "useMaxTokens": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include maxTokens in settings.",
                }),
                "maxTokens": ("INT", {
                    "default": 4096,
                    "min": 1,
                    "max": cls._MAX_TOKENS_CAP,
                    "step": 1,
                    "tooltip": f"maxTokens (1–{cls._MAX_TOKENS_CAP}).",
                }),
                "useTemperature": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include temperature in settings.",
                }),
                "temperature": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Sampling temperature (0.0–1.0).",
                }),
                "useTopP": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include topP in settings.",
                }),
                "topP": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Nucleus sampling (0.01–1.0).",
                }),
                "useTopK": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include topK in settings.",
                }),
                "topK": ("INT", {
                    "default": 40,
                    "min": 1,
                    "max": cls._MAX_TOP_K,
                    "step": 1,
                    "tooltip": f"Top-k sampling (1–{cls._MAX_TOP_K}).",
                }),
                # Keep this in the original slot to avoid shifting legacy widgets_values.
                "thinkingLevel": (["none", "low", "medium", "high"], {
                    "default": "none",
                    "tooltip": "Extended reasoning level: none, low, medium, high.",
                }),
                "useStopSequences": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include stopSequences in settings.",
                }),
                "stopSequences": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Stop sequences: one per line (max 5 items, 50 chars each).",
                }),
                "usePresencePenalty": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include presencePenalty in settings.",
                }),
                "presencePenalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Presence penalty (-2.0 to 2.0).",
                }),
                "useFrequencyPenalty": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include frequencyPenalty in settings.",
                }),
                "frequencyPenalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Frequency penalty (-2.0 to 2.0).",
                }),
                "useTools": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include tools in settings.",
                }),
                "tools": ("STRING", {
                    "multiline": True,
                    "default": "[]",
                    "tooltip": "JSON array for tools.",
                }),
                "useToolChoice": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include toolChoice in settings.",
                }),
                "toolChoice": ("STRING", {
                    "multiline": True,
                    "default": "{}",
                    "tooltip": "JSON object for toolChoice.",
                }),
            },
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCESETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "create_settings"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Optional text inference settings (systemPrompt, maxTokens, temperature, topP, topK, "
        "stopSequences, presencePenalty, frequencyPenalty, tools, toolChoice, thinkingLevel). "
        "Connect to Runware Text Inference."
    )

    @staticmethod
    def _parse_json_setting(raw: Any, expected_type: type, field_name: str) -> Any:
        if isinstance(raw, expected_type):
            return raw
        if raw is None:
            return expected_type()

        text = str(raw).strip()
        if not text:
            return expected_type()

        try:
            parsed = json.loads(text)
        except Exception as exc:
            raise Exception(f"{field_name} must be valid JSON.") from exc

        if not isinstance(parsed, expected_type):
            expected = "array" if expected_type is list else "object"
            raise Exception(f"{field_name} must be a JSON {expected}.")
        return parsed

    def _parse_stop_sequences(self, raw: Any) -> List[str]:
        if raw is None:
            return []

        items: List[str] = []
        if isinstance(raw, (list, tuple)):
            for item in raw:
                text = str(item).strip()
                if text:
                    items.append(text)
        else:
            text = str(raw).strip()
            if text:
                normalized = text.replace("\r\n", "\n").replace(",", "\n")
                items = [segment.strip() for segment in normalized.split("\n") if segment.strip()]

        if len(items) > self._MAX_STOP_ITEMS:
            raise Exception(f"stopSequences supports up to {self._MAX_STOP_ITEMS} items.")
        for idx, item in enumerate(items, start=1):
            if len(item) > self._MAX_STOP_ITEM_CHARS:
                raise Exception(
                    f"stopSequences item {idx} exceeds {self._MAX_STOP_ITEM_CHARS} characters."
                )
        return items

    @staticmethod
    def _normalize_thinking_level(raw: Any) -> str:
        value = str(raw or "none").strip().lower()
        # Backward compatibility with older workflows.
        aliases = {
            "off": "none",
            "minimal": "low",
        }
        value = aliases.get(value, value)
        if value not in ("none", "low", "medium", "high"):
            return "none"
        return value

    def create_settings(self, **kwargs) -> Tuple[Dict[str, Any], ...]:
        out: Dict[str, Any] = {}

        if kwargs.get("useSystemPrompt", False):
            sys_text = (kwargs.get("systemPrompt") or kwargs.get("system") or "").strip()
            if sys_text:
                if len(sys_text) > self._MAX_SYSTEM_CHARS:
                    sys_text = sys_text[: self._MAX_SYSTEM_CHARS]
                out["systemPrompt"] = sys_text

        if kwargs.get("useMaxTokens", False):
            out["maxTokens"] = int(kwargs.get("maxTokens", 4096))

        if kwargs.get("useTemperature", False):
            out["temperature"] = float(kwargs.get("temperature", 1.0))

        if kwargs.get("useTopP", False):
            out["topP"] = float(kwargs.get("topP", 1.0))

        if kwargs.get("useTopK", False):
            out["topK"] = int(kwargs.get("topK", 40))

        if kwargs.get("useStopSequences", False):
            parsed_stop = self._parse_stop_sequences(kwargs.get("stopSequences", ""))
            if parsed_stop:
                out["stopSequences"] = parsed_stop

        if kwargs.get("usePresencePenalty", False):
            out["presencePenalty"] = float(kwargs.get("presencePenalty", 0.0))

        if kwargs.get("useFrequencyPenalty", False):
            out["frequencyPenalty"] = float(kwargs.get("frequencyPenalty", 0.0))

        if kwargs.get("useTools", False):
            parsed_tools = self._parse_json_setting(kwargs.get("tools"), list, "tools")
            if parsed_tools:
                out["tools"] = parsed_tools

        if kwargs.get("useToolChoice", False):
            parsed_choice = self._parse_json_setting(kwargs.get("toolChoice"), dict, "toolChoice")
            if parsed_choice:
                out["toolChoice"] = parsed_choice

        tl = self._normalize_thinking_level(kwargs.get("thinkingLevel", "none"))
        if tl != "none":
            out["thinkingLevel"] = tl

        if not out:
            return ({},)

        return (out,)
