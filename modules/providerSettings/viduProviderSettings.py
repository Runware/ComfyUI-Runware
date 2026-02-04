from ..utils import runwareUtils as rwUtils

class RunwareViduProviderSettings:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                # Audio parameter
                "useAudio": ("BOOLEAN", {
                    "tooltip": "Enable to include audio parameter in API request",
                    "default": False,
                }),
                "audio": ("BOOLEAN", {
                    "tooltip": "Enable audio for video generation. Only used when 'Use Audio' is enabled.",
                    "default": True,
                }),
                # BGM parameter
                "useBgm": ("BOOLEAN", {
                    "tooltip": "Enable to include bgm parameter in API request",
                    "default": False,
                }),
                "bgm": ("BOOLEAN", {
                    "tooltip": "Enable background music for video generation. Only used when 'Use BGM' is enabled.",
                    "default": False,
                }),
                # Style parameter
                "useStyle": ("BOOLEAN", {
                    "tooltip": "Enable to include style parameter in API request",
                    "default": False,
                }),
                "style": ("STRING", {
                    "tooltip": "Video style configuration for Vidu models. Only used when 'Use Style' is enabled.",
                    "default": "",
                }),
                # Movement amplitude parameter
                "useMovementAmplitude": ("BOOLEAN", {
                    "tooltip": "Enable to include movementAmplitude parameter in API request",
                    "default": False,
                }),
                "movementAmplitude": ("STRING", {
                    "tooltip": "Controls the amplitude/intensity of movement in the generated video. Only used when 'Use Movement Amplitude' is enabled.",
                    "default": "",
                }),
                # Template parameters
                "useTemplateName": ("BOOLEAN", {
                    "tooltip": "Enable to include template name in API request",
                    "default": False,
                }),
                "templateName": ("STRING", {
                    "tooltip": "Template name for video generation. Only used when 'Use Template Name' is enabled.",
                    "default": "",
                }),
                "useTemplateArea": ("BOOLEAN", {
                    "tooltip": "Enable to include template area in API request",
                    "default": False,
                }),
                "templateArea": ("STRING", {
                    "tooltip": "Template area configuration. Only used when 'Use Template Area' is enabled.",
                    "default": "",
                }),
                "useTemplateBeast": ("BOOLEAN", {
                    "tooltip": "Enable to include template beast in API request",
                    "default": False,
                }),
                "templateBeast": ("STRING", {
                    "tooltip": "Template beast configuration. Only used when 'Use Template Beast' is enabled.",
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
        useAudio = kwargs.get("useAudio", False)
        audio = kwargs.get("audio", True)
        useBgm = kwargs.get("useBgm", False)
        bgm = kwargs.get("bgm", False)
        useStyle = kwargs.get("useStyle", False)
        style = kwargs.get("style", "")
        useMovementAmplitude = kwargs.get("useMovementAmplitude", False)
        movementAmplitude = kwargs.get("movementAmplitude", "")
        useTemplateName = kwargs.get("useTemplateName", False)
        templateName = kwargs.get("templateName", "")
        useTemplateArea = kwargs.get("useTemplateArea", False)
        templateArea = kwargs.get("templateArea", "")
        useTemplateBeast = kwargs.get("useTemplateBeast", False)
        templateBeast = kwargs.get("templateBeast", "")

        # Build provider settings dictionary
        providerSettings = {}
        
        if useAudio:
            providerSettings["audio"] = audio
        if useBgm:
            providerSettings["bgm"] = bgm
        if useStyle and style and style.strip():
            providerSettings["style"] = style.strip()
        if useMovementAmplitude and movementAmplitude and movementAmplitude.strip():
            providerSettings["movementAmplitude"] = movementAmplitude.strip()
        
        # Build template object if any template parameters are enabled and provided
        template = {}
        if useTemplateName and templateName and templateName.strip():
            template["name"] = templateName.strip()
        if useTemplateArea and templateArea and templateArea.strip():
            template["area"] = templateArea.strip()
        if useTemplateBeast and templateBeast and templateBeast.strip():
            template["beast"] = templateBeast.strip()
        if template:
            providerSettings["template"] = template

        return (providerSettings,)
