from .utils import runwareUtils as rwUtils


class RunwareVideoInferenceOutputs:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Output": (
                    "RUNWARETASK",
                    {
                        "tooltip": "Connect the OUTPUT from Runware Video Inference.",
                    },
                ),
            },
            "optional": {
                "draftId": ("STRING", {
                    "placeholder": "Draft ID will appear here after generation.",
                    "tooltip": "This field will be automatically populated with the draft ID from the video inference output.",
                }),
                "videoId": ("STRING", {
                    "placeholder": "Video ID will appear here after generation.",
                    "tooltip": "This field will be automatically populated with the video ID from the video inference output.",
                }),
            },
            "hidden": {"node_id": "UNIQUE_ID"},
        }

    DESCRIPTION = "Extracts Runware video inference outputs such as draftId and videoId."
    FUNCTION = "get_outputs"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("draftID", "videoID")
    CATEGORY = "Runware"
    OUTPUT_NODE = True  # Ensure node executes even if outputs aren't used

    def get_outputs(self, Output, draftId=None, videoId=None, **kwargs):
        draft_id = ""
        video_id = ""

        try:
            data_list = None

            # Handle different possible response shapes defensively
            if isinstance(Output, dict):
                if "data" in Output:
                    data_list = Output.get("data", [])
                elif "response" in Output and isinstance(Output["response"], dict):
                    data_list = Output["response"].get("data", [])

            if data_list and len(data_list) > 0:
                first = data_list[0]
                outputs = first.get("outputs") or {}
                if isinstance(outputs, dict):
                    # draftId is used by some providers
                    draft_id = outputs.get("draftId", "") or outputs.get("draftID", "")
                    # videoId / videoID used by other providers
                    video_id = outputs.get("videoId", "") or outputs.get("videoID", "")

            # Send to frontend so values appear in textboxes (like Media Upload)
            rwUtils.sendVideoOutputs(draft_id, video_id, kwargs.get("node_id"))

        except Exception as e:
            print(f"[Runware Video Outputs] Failed to parse outputs: {e}")

        return (draft_id, video_id)


NODE_CLASS_MAPPINGS = {
    "RunwareVideoInferenceOutputs": RunwareVideoInferenceOutputs,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareVideoInferenceOutputs": "Runware Video Inference Outputs",
}

