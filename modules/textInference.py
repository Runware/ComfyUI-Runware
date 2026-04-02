import uuid
from typing import Any, Dict, List, Optional

from .utils import runwareUtils as rwUtils


class RunwareTextInference:
    """Runware textInference API: chat completion via selected text model and messages."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("RUNWARETEXTMODEL", {
                    "tooltip": "Connect Runware Text Model Search output.",
                }),
                "messages": ("RUNWARETEXTINFERENCEMESSAGES", {
                    "tooltip": "Connect Runware Text Inference Messages output.",
                }),
            },
            "optional": {
                "settings": ("RUNWARETEXTINFERENCESETTINGS", {
                    "tooltip": "Connect Runware Text Inference Settings (setting + thinking).",
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Optional provider-specific settings (wrapped by provider prefix from the model AIR).",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "infer_text"
    CATEGORY = "Runware/Text"
    DESCRIPTION = "Run text/chat inference using Runware textInference. Connect Text Model and Text Inference Messages."

    @staticmethod
    def _extract_text_from_data_item(item: Dict[str, Any]) -> Optional[str]:
        if not isinstance(item, dict):
            return None
        if "text" in item and item["text"] is not None:
            return str(item["text"])
        if "content" in item and isinstance(item["content"], str):
            return item["content"]
        choices = item.get("choices")
        if isinstance(choices, list) and len(choices) > 0:
            ch0 = choices[0]
            if isinstance(ch0, dict):
                msg = ch0.get("message")
                if isinstance(msg, dict) and "content" in msg:
                    return str(msg["content"])
                if "text" in ch0:
                    return str(ch0["text"])
        return None

    def _finalize_text(self, gen_result: Dict[str, Any]) -> str:
        if "data" not in gen_result or not gen_result["data"]:
            raise Exception("No data in text inference response.")
        item = gen_result["data"][0]
        text = self._extract_text_from_data_item(item)
        if text is None:
            raise Exception(
                "Could not read assistant text from response. "
                f"Keys on data[0]: {list(item.keys()) if isinstance(item, dict) else type(item)}"
            )
        return text

    def infer_text(self, **kwargs):
        model = (kwargs.get("model") or "").strip()
        messages: List[Dict[str, str]] = kwargs.get("messages") or []
        text_settings = kwargs.get("settings")
        provider_settings = kwargs.get("providerSettings")

        if not model:
            raise Exception("model is empty.")
        if not messages:
            raise Exception("messages are empty.")

        task_uuid = str(uuid.uuid4())
        task: Dict[str, Any] = {
            "taskType": "textInference",
            "taskUUID": task_uuid,
            "model": model,
            "deliveryMethod": "sync",
            "messages": messages,
            "includeCost": True,
            "includeUsage": True,
        }

        if text_settings is not None and isinstance(text_settings, dict) and len(text_settings) > 0:
            task["settings"] = text_settings

        if provider_settings is not None and isinstance(provider_settings, dict) and len(provider_settings) > 0:
            provider_name = model.split(":")[0] if ":" in model else model
            task["providerSettings"] = {provider_name: provider_settings}

        gen_config = [task]
        print(f"[Runware Text Inference] Request: {rwUtils.safe_json_dumps(gen_config, indent=2)}")

        gen_result = rwUtils.inferenecRequest(gen_config)
        print(f"[Runware Text Inference] Response: {rwUtils.safe_json_dumps(gen_result, indent=2)}")

        return (self._finalize_text(gen_result),)
