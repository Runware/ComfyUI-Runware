import re

from .utils import runwareUtils as rwUtils


class vectorize:
    """Vectorize node for converting images to vector format"""

    # Models grouped by architecture (provider), same pattern as video model search
    VECTORIZE_MODELS = {
        "Recraft": [
            "recraft:1@1 (Recraft 1)",
            "recraft:v4-pro@vector (Recraft V4 Pro Vector)",
            "recraft:v4@vector (Recraft V4 Vector)",
        ],
        "Picsart": [
            "picsart:1@1 (Picsart 1)",
        ],
    }

    MODEL_ARCHITECTURES = [
        "All",
        "Recraft",
        "Picsart",
    ]

    @classmethod
    def _getAllModels(cls):
        """Get all models from all architectures"""
        all_models = []
        for models in cls.VECTORIZE_MODELS.values():
            all_models.extend(models)
        return all_models

    @classmethod
    def INPUT_TYPES(cls):
        all_models = cls._getAllModels()
        default_model = all_models[0] if all_models else "recraft:1@1 (Recraft 1)"
        return {
            "required": {
                "Model Search": ("STRING", {
                    "tooltip": "Search for a vectorization model by name or AIR code (e.g. recraft, picsart).",
                }),
                "Model Architecture": (cls.MODEL_ARCHITECTURES, {
                    "tooltip": "Choose model architecture to filter the model list.",
                    "default": "Recraft",
                }),
                "Vector Model List": (all_models, {
                    "tooltip": "Select the vectorization model. Filter by Model Architecture above.",
                    "default": default_model,
                }),
                "Use Search Value": ("BOOLEAN", {
                    "tooltip": "When enabled, the value in Model Search is used as the model AIR code instead of the list selection.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
            },
            "optional": {
                "Image": ("IMAGE", {
                    "tooltip": "Optional input image to be vectorized."
                }),
                "dimensions": ([
                    "None", "Square HD (1024x1024)", "Custom"
                ], {
                    "default": "None",
                    "tooltip": "Output dimensions preset. Select 'None' for model default, or a preset to set width/height. Use 'Custom' with width/height inputs.",
                }),
                "width": ("INT", {
                    "tooltip": "Width in pixels. Used when dimensions is not 'None' (or with Custom).",
                    "default": 1024,
                    "min": 128,
                    "max": 6048,
                    "step": 1,
                }),
                "height": ("INT", {
                    "tooltip": "Height in pixels. Used when dimensions is not 'None' (or with Custom).",
                    "default": 1024,
                    "min": 128,
                    "max": 6048,
                    "step": 1,
                }),
                "Use positivePrompt": ("BOOLEAN", {
                    "tooltip": "When enabled, include positivePrompt in the vectorize request.",
                    "default": False,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "positivePrompt": ("STRING", {
                    "multiline": True,
                    "tooltip": "Optional text prompt for vectorization. Only sent when Use Positive Prompt is enabled.",
                }),
                "providerSettings": ("RUNWAREPROVIDERSETTINGS", {
                    "tooltip": "Connect a Runware Provider Settings Node to configure provider-specific parameters (e.g. Recraft, Picsart).",
                }),
            },
        }

    DESCRIPTION = "Convert images to vector format using Runware's vectorization service."
    FUNCTION = "vectorizeImage"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("IMAGE",)
    CATEGORY = "Runware"

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def vectorizeImage(self, **kwargs):
        """Vectorize image and return SVG URL"""
        image = kwargs.get("Image")
        use_search_value = kwargs.get("Use Search Value", False)
        search_input = kwargs.get("Model Search", "")
        current_model = kwargs.get("Vector Model List", "recraft:1@1 (Recraft 1)")

        if use_search_value and search_input and str(search_input).strip():
            model_air_code = str(search_input).strip()
        else:
            # Extract AIR code from "airId (Display Name)" format
            model_air_code = current_model.split(" (")[0].strip()

        image_uuid = rwUtils.convertTensor2IMG(image) if image is not None else None
        width = kwargs.get("width")
        height = kwargs.get("height")
        dimensions = kwargs.get("dimensions", "None")
        use_positive_prompt = kwargs.get("Use positivePrompt", False)
        positive_prompt = kwargs.get("positivePrompt")
        provider_settings = kwargs.get("providerSettings")
        gen_config = self._buildGenConfig(
            model_air_code, image_uuid,
            width=width, height=height, dimensions=dimensions,
            use_positive_prompt=use_positive_prompt, positive_prompt=positive_prompt,
            provider_settings=provider_settings,
        )

        print(f"[DEBUG] Sending Vectorize Request:")
        print(f"[DEBUG] Request Payload: {rwUtils.safe_json_dumps(gen_config, indent=2)}")

        gen_result = rwUtils.inferenecRequest(gen_config)
        print(f"[DEBUG] Received Vectorize Response:")
        print(f"[DEBUG] Response: {rwUtils.safe_json_dumps(gen_result, indent=2)}")

        self._validateResponse(gen_result)
        svg_url = rwUtils.extractImageURLs(gen_result)
        return (svg_url,)

    @staticmethod
    def _parseDimensionsPreset(dimensions):
        """Parse 'Label (WxH)' to (width, height) or None if not a preset."""
        if not dimensions or dimensions in ("None", "Custom"):
            return None, None
        m = re.search(r"\((\d+)x(\d+)\)", dimensions)
        if m:
            return int(m.group(1)), int(m.group(2))
        return None, None

    def _buildGenConfig(self, model, image_uuid, width=None, height=None, dimensions="None",
                        use_positive_prompt=False, positive_prompt=None, provider_settings=None):
        """Build generation configuration for API request. image_uuid, width, height, positivePrompt, providerSettings are optional."""
        inputs = {}
        if image_uuid is not None:
            inputs["image"] = image_uuid
        payload = {
            "taskType": "vectorize",
            "taskUUID": rwUtils.genRandUUID(),
            "model": model,
            "inputs": inputs,
            "outputType": "URL",
            "outputFormat": "svg",
        }
        if dimensions and dimensions != "None":
            w, h = width, height
            if w is None or h is None:
                pw, ph = self._parseDimensionsPreset(dimensions)
                if pw is not None and ph is not None:
                    w, h = pw, ph
            if w is not None and h is not None:
                payload["width"] = w
                payload["height"] = h
        if use_positive_prompt and positive_prompt is not None and str(positive_prompt).strip():
            payload["positivePrompt"] = str(positive_prompt).strip()
        # Handle providerSettings - extract provider name from model and merge (same as image inference)
        if provider_settings is not None:
            provider_name = model.split(":")[0] if ":" in model else model
            if isinstance(provider_settings, dict):
                if any(key in provider_settings for key in ["alibaba", "bytedance", "klingai", "openai", "pixverse",
                                                            "bria", "lightricks", "luma", "minimax", "runway", "vidu",
                                                            "elevenlabs", "bfl", "xai", "recraft", "picsart", "sourceful"]):
                    payload["providerSettings"] = provider_settings
                else:
                    payload["providerSettings"] = {provider_name: provider_settings}
            else:
                payload["providerSettings"] = provider_settings
        return [payload]

    def _validateResponse(self, gen_result):
        """Validate API response"""
        if "errors" in gen_result:
            error_message = gen_result["errors"][0]["message"]
            raise Exception(f"Vectorization failed: {error_message}")


NODE_CLASS_MAPPINGS = {
    "RunwareVectorize": vectorize,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVectorize": "Runware Vectorize",
}
