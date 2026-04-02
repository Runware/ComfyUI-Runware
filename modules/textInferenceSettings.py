from typing import Any, Dict, Tuple


class RunwareTextInferenceSettings:
    """Optional generation controls for Runware Text Inference (flat task.settings per API)."""

    _MAX_SYSTEM_CHARS = 200000
    _MAX_TOKENS_CAP = 196608

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useSystemPrompt": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include systemPrompt in settings.",
                }),
                "system": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "System instruction (max 200,000 characters). Sent as systemPrompt.",
                }),
                "useMaxTokens": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include maxTokens in settings.",
                }),
                "maxTokens": ("INT", {
                    "default": 32768,
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
                    "min": 0.01,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Sampling temperature on (0, 1].",
                }),
                "useTopP": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include topP in settings.",
                }),
                "topP": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Nucleus sampling (0.0–1.0).",
                }),
                "useTopK": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include topK in settings.",
                }),
                "topK": ("INT", {
                    "default": 40,
                    "min": 1,
                    "max": 128,
                    "step": 1,
                    "tooltip": "Top-k sampling (1–128).",
                }),
                "thinkingLevel": (["off", "minimal", "low", "medium", "high"], {
                    "default": "off",
                    "tooltip": "thinkingLevel in settings (omit when off).",
                }),
            },
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCESETTINGS",)
    RETURN_NAMES = ("settings",)
    FUNCTION = "create_settings"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Optional text inference settings (flat: systemPrompt, maxTokens, temperature, topP, topK, thinkingLevel). "
        "Connect to Runware Text Inference."
    )

    def create_settings(self, **kwargs) -> Tuple[Dict[str, Any], ...]:
        out: Dict[str, Any] = {}

        if kwargs.get("useSystemPrompt", False):
            sys_text = (kwargs.get("system") or "").strip()
            if sys_text:
                if len(sys_text) > self._MAX_SYSTEM_CHARS:
                    sys_text = sys_text[: self._MAX_SYSTEM_CHARS]
                out["systemPrompt"] = sys_text

        if kwargs.get("useMaxTokens", False):
            out["maxTokens"] = int(kwargs.get("maxTokens", 32768))

        if kwargs.get("useTemperature", False):
            out["temperature"] = float(kwargs.get("temperature", 1.0))

        if kwargs.get("useTopP", False):
            out["topP"] = float(kwargs.get("topP", 0.95))

        if kwargs.get("useTopK", False):
            out["topK"] = int(kwargs.get("topK", 40))

        tl = kwargs.get("thinkingLevel", "off")
        if tl != "off":
            out["thinkingLevel"] = tl

        if not out:
            return ({},)

        return (out,)
