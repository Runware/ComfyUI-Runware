class RunwareElevenLabsProviderSettings:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "positiveGlobalStyles": ("STRING", {
                    "multiline": True,
                    "default": "rock, energetic",
                    "tooltip": "Global positive styles for the entire song (comma-separated): positiveGlobalStyles"
                }),
                "negativeGlobalStyles": ("STRING", {
                    "multiline": True,
                    "default": "slow, quiet",
                    "tooltip": "Global negative styles for the entire song (comma-separated): negativeGlobalStyles"
                }),
            },
            "optional": {
                "sections": ("RUNWAREAUDIOSECTIONS", {
                    "tooltip": "Connect multiple Runware Audio Sections nodes to define song structure"
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREPROVIDERSETTINGS",)
    RETURN_NAMES = ("providerSettings",)
    FUNCTION = "create_provider_settings"
    CATEGORY = "Runware/Audio"

    def create_provider_settings(self, **kwargs):
        positiveGlobalStyles = kwargs.get("positiveGlobalStyles", "")
        negativeGlobalStyles = kwargs.get("negativeGlobalStyles", "")
        sections = kwargs.get("sections", [])
        
        # Parse styles from comma-separated strings
        positiveStyles = [style.strip() for style in positiveGlobalStyles.split(",") if style.strip()]
        negativeStyles = [style.strip() for style in negativeGlobalStyles.split(",") if style.strip()]
        
        # Handle sections - can be single section or list of sections
        sections_list = []
        if sections:
            if isinstance(sections, list):
                sections_list = sections
            else:
                sections_list = [sections]
        
        # Build the music composition plan
        

        music = {
            "compositionPlan": {
                "positiveGlobalStyles": positiveStyles,
                "negativeGlobalStyles": negativeStyles,
                "sections": sections_list
            }
        }
        
        # Create provider settings
        providerSettings = {
            "elevenlabs": {
                "music": music
            }
        }
        
        return (providerSettings,)
