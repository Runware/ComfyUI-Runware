"""
Runware Text Inference Settings Cache Node
Builds the cache object for Runware Text Inference (settings.cache.{scope, ttl}).

Maps cache_control placement (Anthropic):
  - scope: where cache_control is attached
      * system          -> system block only
      * system+history  -> system block + last user message block (default)
  - ttl: cache lifetime (5m or 1h)
"""

from typing import Dict, Any


class RunwareTextInferenceSettingsCache:
    """Runware Text Inference Settings Cache node."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "scope": (["system", "system+history"], {
                    "default": "system+history",
                    "tooltip": (
                        "Where cache_control is attached.\n"
                        "- system: cache the system block only.\n"
                        "- system+history: cache the system block and the last user message block."
                    ),
                }),
                "ttl": (["5m", "1h"], {
                    "default": "5m",
                    "tooltip": "Cache lifetime: 5m (5 minutes) or 1h (1 hour).",
                }),
            }
        }

    RETURN_TYPES = ("RUNWARETEXTINFERENCESETTINGSCACHE",)
    RETURN_NAMES = ("cache",)
    FUNCTION = "createCache"
    CATEGORY = "Runware/Text"
    DESCRIPTION = (
        "Build a settings.cache object (scope + ttl) and connect it to Runware Text Inference. "
        "Merged into the request as settings.cache.{scope, ttl}."
    )

    def createCache(self, **kwargs) -> tuple[Dict[str, Any]]:
        scope = (kwargs.get("scope") or "system+history").strip().lower()
        if scope not in ("system", "system+history"):
            scope = "system+history"

        ttl = (kwargs.get("ttl") or "5m").strip().lower()
        if ttl not in ("5m", "1h"):
            ttl = "5m"

        return ({"scope": scope, "ttl": ttl},)


NODE_CLASS_MAPPINGS = {
    "RunwareTextInferenceSettingsCache": RunwareTextInferenceSettingsCache,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareTextInferenceSettingsCache": "Runware Text Inference Settings Cache",
}
