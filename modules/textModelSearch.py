class RunwareTextModelSearch:
    """Text model search node: pick or type a text/chat AIR model for Runware Text Inference."""

    TEXT_MODELS = {
        "MiniMax": [
            "minimax:m2.7@0 (MiniMax-M2.7)",
            "minimax:m2.7@highspeed (MiniMax-M2.7 Highspeed)",
            "minimax:m2.5@0 (MiniMax-M2.5)",
        ],
    }

    MODEL_PROVIDERS = [
        "All",
        "MiniMax",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        all_models = cls._get_all_models()
        default_model = "minimax:m2.7@0 (MiniMax-M2.7)"

        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search or type a text model AIR code (e.g. minimax:m2.7@0). Used when 'Use Search Value' is enabled.",
                }),
                "Model Provider": (cls.MODEL_PROVIDERS, {
                    "tooltip": "Filter the model list by provider.",
                    "default": "MiniMax",
                }),
                "TextList": (all_models, {
                    "tooltip": "Choose a model from the filtered list (AIR code is taken before the first space).",
                    "default": default_model,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When enabled, 'Model Search' is used as the model AIR instead of the selection in TextList.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            }
        }

    @classmethod
    def _get_all_models(cls):
        all_models = []
        for models in cls.TEXT_MODELS.values():
            all_models.extend(models)
        return all_models

    RETURN_TYPES = ("RUNWARETEXTMODEL",)
    RETURN_NAMES = ("model",)
    FUNCTION = "searchModels"
    CATEGORY = "Runware"
    DESCRIPTION = "Search and select text/chat models for Runware Text Inference."

    @classmethod
    def VALIDATE_INPUTS(cls, TextList):
        return True

    def searchModels(self, **kwargs):
        use_search = kwargs.get("Use Search Value", False)
        search_input = (kwargs.get("Model Search") or "").strip()

        if use_search:
            if not search_input:
                raise Exception("Use Search Value is enabled but Model Search is empty.")
            model_air = search_input
        else:
            current = kwargs.get("TextList")
            model_air = current.split(" (")[0] if current else ""

        return (model_air,)
