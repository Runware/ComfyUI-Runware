"""
Runware Kling Provider Settings MultiPrompt Node
Adds multiPrompt to Kling provider settings. Connects to Runware Kling Provider Settings
and outputs merged provider settings for Video Inference.
"""

from typing import Dict, Any, List


class RunwareKlingProviderSettingsMultiPrompt:
    """Runware Kling Provider Settings MultiPrompt Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Connect Runware KlingAI Provider Settings to merge with multiPrompt",
                }),
            },
            "optional": {
                "MultiPrompt Segment 1": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
                "MultiPrompt Segment 2": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
                "MultiPrompt Segment 3": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
                "MultiPrompt Segment 4": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
                "MultiPrompt Segment 5": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
                "MultiPrompt Segment 6": ("RUNWAREKLINGMULTIPROMPTSEGMENT", {
                    "tooltip": "Connect a Runware Kling MultiPrompt Segment",
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    FUNCTION = "mergeProviderSettings"
    CATEGORY = "Runware/Provider Settings"
    DESCRIPTION = "Add multiPrompt to Kling provider settings. Connect Runware KlingAI Provider Settings and one or more Runware Kling MultiPrompt Segment nodes. Output connects to Runware Video Inference."

    def mergeProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Merge Kling provider settings with multiPrompt segments"""

        provider_settings = kwargs.get("providerSettings")
        segments: List[Dict[str, Any]] = []

        for i in range(1, 7):
            segment = kwargs.get(f"MultiPrompt Segment {i}")
            if segment is not None and isinstance(segment, dict):
                prompt = segment.get("prompt", "").strip()
                if prompt:
                    segments.append({
                        "prompt": prompt,
                        "duration": int(segment.get("duration", 4)),
                    })

        # Start with existing provider settings or empty dict
        if isinstance(provider_settings, dict):
            # May be flat (from Kling) or wrapped {"klingai": {...}}
            if "klingai" in provider_settings:
                kling_settings = dict(provider_settings["klingai"])
            else:
                kling_settings = dict(provider_settings)
        else:
            kling_settings = {}

        if segments:
            kling_settings["multiPrompt"] = segments

        if not kling_settings:
            return ({},)

        # Output format expected by video inference: wrap with klingai if flat
        return ({"klingai": kling_settings},)


NODE_CLASS_MAPPINGS = {
    "RunwareKlingProviderSettingsMultiPrompt": RunwareKlingProviderSettingsMultiPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareKlingProviderSettingsMultiPrompt": "Runware Kling Provider Settings MultiPrompt",
}
