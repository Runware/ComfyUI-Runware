from typing import Dict, Any, Tuple


class RunwareRegionalPromptingAdvancedFeature:
    """
    Runware Regional Prompting Advanced Feature Node

    Builds the advancedFeatures.regionalPrompting configuration object:
      - injectSteps
      - backgroundPrompt
      - baseRatio
      - regions (connected from the Regions node)
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "injectSteps": ("INT", {
                    "tooltip": "Steps to inject regional masks (1-100).",
                    "default": 15,
                    "min": 1,
                    "max": 100,
                }),
                "backgroundPrompt": ("STRING", {
                    "tooltip": "Background prompt applied to uncovered areas.",
                    "default": "",
                }),
                "baseRatio": ("FLOAT", {
                    "tooltip": "Base prompt attention weight (0.0 - 1.0).",
                    "default": 0.2,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                }),
                "regions": ("RUNWAREREGIONALPROMPTINGREGIONS", {
                    "tooltip": "Connect Runware Regional Prompting Advanced Feature Regions node to define regional prompts and masks.",
                }),
            },
        }

    RETURN_TYPES: Tuple[str] = ("RUNWAREREGIONALPROMPTINGADVFEATURE",)
    RETURN_NAMES = ("regionalPrompting",)
    FUNCTION = "createRegionalPrompting"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure regional prompting advanced feature (injectSteps, backgroundPrompt, "
        "baseRatio, and regions). Connect output to Runware Image  Advanced Feature Input "
        "regionalPrompting input."
    )

    def createRegionalPrompting(self, regions=None, **kwargs) -> tuple:
        """Build regionalPrompting dict for advancedFeatures.regionalPrompting."""
        inject_steps = int(kwargs.get("injectSteps", 15))
        base_ratio = float(kwargs.get("baseRatio", 0.2))
        background_prompt = (kwargs.get("backgroundPrompt", "") or "").strip()

        config: Dict[str, Any] = {
            "injectSteps": inject_steps,
            "baseRatio": base_ratio,
        }

        if background_prompt:
            config["backgroundPrompt"] = background_prompt

        if isinstance(regions, list) and regions:
            config["regions"] = regions

        return (config,)


NODE_CLASS_MAPPINGS = {
    "RunwareRegionalPromptingAdvancedFeature": RunwareRegionalPromptingAdvancedFeature,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareRegionalPromptingAdvancedFeature": "Runware Regional Prompting Advanced Feature",
}

