from .utils import runwareUtils as rwUtils

class RunwareViduProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                # BGM parameter
                "bgm": ("BOOLEAN", {
                    "tooltip": "Enable background music for video generation",
                    "default": False,
                }),
                
                # Style parameter
                "style": ("STRING", {
                    "tooltip": "Video style configuration for Vidu models",
                    "default": "",
                }),
                
                # Movement amplitude parameter
                "movementAmplitude": ("STRING", {
                    "tooltip": "Controls the amplitude/intensity of movement in the generated video",
                    "default": "",
                }),
                
                # Template parameters
                "templateName": ("STRING", {
                    "tooltip": "Template name for video generation",
                    "default": "",
                }),
                "templateArea": ("STRING", {
                    "tooltip": "Template area configuration",
                    "default": "",
                }),
                "templateBeast": ("STRING", {
                    "tooltip": "Template beast configuration",
                    "default": "",
                }),
            },
        }

    DESCRIPTION = "Configure Vidu-specific provider settings for video generation. Includes background music, style, movement amplitude, and template configurations."
    FUNCTION = "viduProviderSettings"
    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("Vidu Provider Settings",)
    CATEGORY = "Runware"

    def viduProviderSettings(self, **kwargs):
        # Get all optional parameters
        bgm = kwargs.get("bgm")
        style = kwargs.get("style", "")
        movementAmplitude = kwargs.get("movementAmplitude", "")
        templateName = kwargs.get("templateName", "")
        templateArea = kwargs.get("templateArea", "")
        templateBeast = kwargs.get("templateBeast", "")

        # Build provider settings dictionary
        providerSettings = {}
        
        # Add basic parameters if specified
        if bgm is not None:
            providerSettings["bgm"] = bgm
        if style:
            providerSettings["style"] = style
        if movementAmplitude:
            providerSettings["movementAmplitude"] = movementAmplitude
        
        # Build template object if any template parameters are provided
        template = {}
        if templateName:
            template["name"] = templateName
        if templateArea:
            template["area"] = templateArea
        if templateBeast:
            template["beast"] = templateBeast
        
        # Add template to provider settings if any template parameters were specified
        if template:
            providerSettings["template"] = template

        return (providerSettings,)
