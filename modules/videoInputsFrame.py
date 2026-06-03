from .utils import runwareUtils as rwUtils


class RunwareVideoInputsFrameImages:
    """Video Inputs Frame node for adapting frame images structure for video inference"""

    MAX_FRAMES = 4
    FRAME_POSITIONS = ["first", "last"]

    @classmethod
    def INPUT_TYPES(cls):
        optionalInputs = {}

        for i in range(1, cls.MAX_FRAMES + 1):
            optionalInputs[f"image{i}"] = ("IMAGE", {
                "tooltip": "Frame image to include in video inference inputs.frameImages.",
            })
            optionalInputs[f"useFrame{i}"] = ("BOOLEAN", {
                "tooltip": "Enable to set frame position (first/last).",
                "default": False,
            })
            optionalInputs[f"frame{i} position"] = (cls.FRAME_POSITIONS, {
                "default": "first",
                "tooltip": "Frame position: 'first' or 'last'. Only used when 'Use Frame' is enabled.",
            })
            optionalInputs[f"useTimestamp{i}"] = ("BOOLEAN", {
                "tooltip": "Enable to set a timestamp (seconds) within the input video.",
                "default": False,
            })
            optionalInputs[f"timestamp{i}"] = ("FLOAT", {
                "default": 0.0,
                "min": 0.0,
                "max": 9999.0,
                "step": 0.01,
                "tooltip": "Timestamp in seconds (hundredths supported, e.g. 3.44). Only used when 'Use Timestamp' is enabled.",
            })

        return {
            "required": {},
            "optional": optionalInputs,
        }

    DESCRIPTION = (
        "Build inputs.frameImages entries for video inference: "
        "{image: base64}, {image: base64, frame: first|last}, or "
        "{image: base64, timestamp: seconds}."
    )
    FUNCTION = "createFrameInputs"
    RETURN_TYPES = ("RUNWAREVIDEOINPUTSFRAMEIMAGES",)
    RETURN_NAMES = ("Video Inputs Frame Images",)
    CATEGORY = "Runware"

    def createFrameInputs(self, **kwargs):
        frameImages = []

        for i in range(1, self.MAX_FRAMES + 1):
            image = kwargs.get(f"image{i}")
            if image is None:
                continue

            use_frame = kwargs.get(f"useFrame{i}", False)
            frame_position = kwargs.get(f"frame{i} position", "first")
            use_timestamp = kwargs.get(f"useTimestamp{i}", False)
            timestamp = self._parse_timestamp(kwargs.get(f"timestamp{i}", 0.0))

            frameImages.append(
                self._createFrameEntry(
                    image,
                    use_frame=use_frame,
                    frame_position=frame_position,
                    use_timestamp=use_timestamp,
                    timestamp=timestamp,
                )
            )

        return (frameImages,)

    @staticmethod
    def _parse_timestamp(value, default=0.0):
        """Coerce timestamp input; ComfyUI may send '' when the widget is disabled."""
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return max(0.0, float(value))
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "":
                return default
            try:
                return max(0.0, float(stripped))
            except ValueError:
                return default
        return default

    def _createFrameEntry(self, image, use_frame, frame_position, use_timestamp, timestamp):
        imageData = rwUtils.convertTensor2IMGBase64Only(image)
        entry = {"image": imageData}

        if use_timestamp:
            entry["timestamp"] = round(timestamp, 2)
        elif use_frame:
            frame_value = frame_position
            if isinstance(frame_value, str):
                frame_value = frame_value.strip()
            if frame_value:
                entry["frame"] = frame_value

        return entry


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInputsFrameImages": RunwareVideoInputsFrameImages,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInputsFrameImages": "Runware Video Inputs Frame Images",
}
