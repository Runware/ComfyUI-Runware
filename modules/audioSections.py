class RunwareAudioSections:
    """Audio Sections node for creating audio composition sections"""
    
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
                    "tooltip": "Styles that should be present in this section (comma-separated)"
                }),
                "negativeLocalStyles": ("STRING", {
                    "default": "vocals",
                    "tooltip": "Styles that should not be present in this section (comma-separated)"
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
    FUNCTION = "createSections"
    CATEGORY = "Runware/Audio"

    def createSections(self, **kwargs):
        """Create audio section object from provided parameters"""
        sectionName = kwargs.get("sectionName", "")
        positiveLocalStyles = kwargs.get("positiveLocalStyles", "")
        negativeLocalStyles = kwargs.get("negativeLocalStyles", "")
        duration = kwargs.get("duration", 0)
        lines = kwargs.get("lines", "")
        
        section = {
            "sectionName": sectionName,
            "positiveLocalStyles": self._parseCommaSeparated(positiveLocalStyles),
            "negativeLocalStyles": self._parseCommaSeparated(negativeLocalStyles),
            "duration": duration,
            "lines": self._parseLines(lines)
        }
        
        return (section,)

    def _parseCommaSeparated(self, text):
        """Parse comma-separated string into list"""
        return [item.strip() for item in text.split(",") if item.strip()]

    def _parseLines(self, text):
        """Parse multiline text into list"""
        return [line.strip() for line in text.split("\n") if line.strip()]
