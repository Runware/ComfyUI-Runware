from typing import Dict, Any, List, Tuple


class RunwareRegionalPromptingAdvancedFeatureRegions:
    """
    Runware Regional Prompting Advanced Feature Regions Node

    Builds the advancedFeatures.regionalPrompting.regions array, with up to 4 regions.
    Each region has a prompt and a rectangular mask [x0, y0, x1, y1].
    """

    @classmethod
    def INPUT_TYPES(cls):
        coords_tooltip = "Mask rectangle as [x0, y0, x1, y1] in image pixel coordinates."
        return {
            "required": {},
            "optional": {
                # Region 1
                "useRegion1": ("BOOLEAN", {
                    "tooltip": "Enable first regional prompt mask.",
                    "default": False,
                }),
                "region1Prompt": ("STRING", {
                    "tooltip": "Prompt for region 1.",
                    "default": "",
                }),
                "region1_x0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                }),
                "region1_y0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                }),
                "region1_x1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region1_y1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                # Region 2
                "useRegion2": ("BOOLEAN", {
                    "tooltip": "Enable second regional prompt mask.",
                    "default": False,
                }),
                "region2Prompt": ("STRING", {
                    "tooltip": "Prompt for region 2.",
                    "default": "",
                }),
                "region2_x0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region2_y0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                }),
                "region2_x1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 1024,
                    "min": 0,
                    "max": 8192,
                }),
                "region2_y1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                # Region 3
                "useRegion3": ("BOOLEAN", {
                    "tooltip": "Enable third regional prompt mask.",
                    "default": False,
                }),
                "region3Prompt": ("STRING", {
                    "tooltip": "Prompt for region 3.",
                    "default": "",
                }),
                "region3_x0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 0,
                    "min": 0,
                    "max": 8192,
                }),
                "region3_y0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region3_x1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region3_y1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 1024,
                    "min": 0,
                    "max": 8192,
                }),
                # Region 4
                "useRegion4": ("BOOLEAN", {
                    "tooltip": "Enable fourth regional prompt mask.",
                    "default": False,
                }),
                "region4Prompt": ("STRING", {
                    "tooltip": "Prompt for region 4.",
                    "default": "",
                }),
                "region4_x0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region4_y0": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 512,
                    "min": 0,
                    "max": 8192,
                }),
                "region4_x1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 1024,
                    "min": 0,
                    "max": 8192,
                }),
                "region4_y1": ("INT", {
                    "tooltip": coords_tooltip,
                    "default": 1024,
                    "min": 0,
                    "max": 8192,
                }),
            },
        }

    RETURN_TYPES: Tuple[str] = ("RUNWAREREGIONALPROMPTINGREGIONS",)
    RETURN_NAMES = ("regions",)
    FUNCTION = "createRegions"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Configure regions array for regional prompting. Each enabled region provides "
        "a prompt and a rectangular mask [x0, y0, x1, y1]. Connect to Runware Regional "
        "Prompting Advanced Feature regions input."
    )

    def createRegions(self, **kwargs) -> tuple:
        """Build list of regional prompting regions."""
        regions: List[Dict[str, Any]] = []

        for idx in range(1, 5):
            use_region = kwargs.get(f"useRegion{idx}", False)
            prompt = (kwargs.get(f"region{idx}Prompt", "") or "").strip()
            if not use_region or not prompt:
                continue

            x0 = int(kwargs.get(f"region{idx}_x0", 0))
            y0 = int(kwargs.get(f"region{idx}_y0", 0))
            x1 = int(kwargs.get(f"region{idx}_x1", 0))
            y1 = int(kwargs.get(f"region{idx}_y1", 0))

            mask = [x0, y0, x1, y1]
            regions.append(
                {
                    "prompt": prompt,
                    "mask": mask,
                }
            )

        return (regions,)


NODE_CLASS_MAPPINGS = {
    "RunwareRegionalPromptingAdvancedFeatureRegions": RunwareRegionalPromptingAdvancedFeatureRegions,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareRegionalPromptingAdvancedFeatureRegions": "Runware Regional Prompting Advanced Feature Regions",
}

