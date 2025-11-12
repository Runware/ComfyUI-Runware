from typing import Any, Dict, List


class RunwareLumaProviderSettings:
    """Provider settings node for LumaAI video generation parameters."""

    CONCEPT_OPTIONS = [
        "",
        "aerial",
        "aerial_drone",
        "bolt_cam",
        "crane_down",
        "crane_up",
        "dolly_zoom",
        "elevator_doors",
        "eye_level",
        "ground_level",
        "handheld",
        "high_angle",
        "low_angle",
        "orbit_left",
        "orbit_right",
        "over_the_shoulder",
        "overhead",
        "pan_left",
        "pan_right",
        "pedestal_down",
        "pedestal_up",
        "pov",
        "pull_out",
        "push_in",
        "roll_left",
        "roll_right",
        "selfie",
        "static",
        "tilt_down",
        "tilt_up",
        "tiny_planet",
        "truck_left",
        "truck_right",
        "zoom_in",
        "zoom_out",
    ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "useLoop": ("BOOLEAN", {
                    "tooltip": "Enable to include the loop parameter in provider settings.",
                    "default": False,
                }),
                "loop": ("BOOLEAN", {
                    "tooltip": "When enabled, generated video will loop seamlessly.",
                    "default": False,
                }),
                "useConcept1": ("BOOLEAN", {
                    "tooltip": "Enable to include Concept 1 in the concepts list.",
                    "default": False,
                }),
                "concept1": (cls.CONCEPT_OPTIONS, {
                    "tooltip": "Concept key to guide the video generation (e.g., aerial, bolt_cam).",
                    "default": "",
                }),
                "useConcept2": ("BOOLEAN", {
                    "tooltip": "Enable to include Concept 2 in the concepts list.",
                    "default": False,
                }),
                "concept2": (cls.CONCEPT_OPTIONS, {
                    "tooltip": "Concept key to guide the video generation.",
                    "default": "",
                }),
                "useConcept3": ("BOOLEAN", {
                    "tooltip": "Enable to include Concept 3 in the concepts list.",
                    "default": False,
                }),
                "concept3": (cls.CONCEPT_OPTIONS, {
                    "tooltip": "Concept key to guide the video generation.",
                    "default": "",
                }),
                "useConcept4": ("BOOLEAN", {
                    "tooltip": "Enable to include Concept 4 in the concepts list.",
                    "default": False,
                }),
                "concept4": (cls.CONCEPT_OPTIONS, {
                    "tooltip": "Concept key to guide the video generation.",
                    "default": "",
                }),
            }
        }

    DESCRIPTION = "Configure LumaAI provider settings including loop and concept guidance."
    FUNCTION = "createProviderSettings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Provider Settings",)
    CATEGORY = "Runware/Provider Settings"

    def createProviderSettings(self, **kwargs) -> tuple[Dict[str, Any]]:
        """Build LumaAI provider settings payload."""

        useLoop = kwargs.get("useLoop", False)
        loop = kwargs.get("loop", False)

        concepts = self._collectConcepts(**kwargs)

        lumaSettings: Dict[str, Any] = {}

        if useLoop:
            lumaSettings["loop"] = bool(loop)

        if concepts:
            lumaSettings["concepts"] = concepts

        result = {}
        if lumaSettings:
            result["lumaai"] = lumaSettings

        return (result if result else None,)

    def _collectConcepts(self, **kwargs) -> List[Dict[str, str]]:
        """Collect concept entries from kwargs respecting use toggles."""

        concepts: List[Dict[str, str]] = []

        for index in range(1, 5):
            use_key = f"useConcept{index}"
            concept_key = f"concept{index}"

            if kwargs.get(use_key, False):
                concept_value = kwargs.get(concept_key, "")
                if isinstance(concept_value, str):
                    normalized = concept_value.strip().lower()
                    if normalized != "":
                        concepts.append({"key": normalized})

        return concepts


NODE_CLASS_MAPPINGS = {
    "RunwareLumaProviderSettings": RunwareLumaProviderSettings,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareLumaProviderSettings": "Runware Luma Provider Settings",
}
