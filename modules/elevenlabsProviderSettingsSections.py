class RunwareElevenLabsProviderSettingsSections:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "sectionName": ("STRING", {
                    "default": "intro",
                    "tooltip": "Name of the section"
                }),
                "positiveLocalStyles": ("STRING", {
                    "default": "guitar, buildup",
                    "tooltip": "Local positive styles for this section (comma-separated): positiveLocalStyles"
                }),
                "negativeLocalStyles": ("STRING", {
                    "default": "vocals",
                    "tooltip": "Local negative styles for this section (comma-separated): negativeLocalStyles"
                }),
                "duration": ("INT", {
                    "default": 15,
                    "min": 3,
                    "max": 120,
                    "tooltip": "Duration of the section in seconds (3-120)"
                }),
                "lines": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "Lyrics for the section (one line per line)"
                }),
            }
        }

    RETURN_TYPES = ("RUNWAREAUDIOSECTIONS",)
    RETURN_NAMES = ("sections",)
    FUNCTION = "create_sections"
    CATEGORY = "Runware/Audio"

    def create_sections(self, **kwargs):
        sectionName = kwargs.get("sectionName", "")
        positiveLocalStyles = kwargs.get("positiveLocalStyles", "")
        negativeLocalStyles = kwargs.get("negativeLocalStyles", "")
        duration = kwargs.get("duration", 0)
        lines = kwargs.get("lines", "")
        
        # Create section object
        section = {
            "sectionName": sectionName,
            "positiveLocalStyles": [style.strip() for style in positiveLocalStyles.split(",") if style.strip()],
            "negativeLocalStyles": [style.strip() for style in negativeLocalStyles.split(",") if style.strip()],
            "duration": duration,
            "lines": [line.strip() for line in lines.split("\n") if line.strip()]
        }
        
        return (section,)
