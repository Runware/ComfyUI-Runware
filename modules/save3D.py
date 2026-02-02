from .utils import runwareUtils as rwUtils
import folder_paths
import os
import re
import requests
from datetime import datetime


class RunwareSave3D:
    """Runware Save 3D node for saving 3D model files from URL"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "3dObject": ("STRING", {
                    "tooltip": "3D file URL from Runware 3D Inference node."
                }),
                "filenamePrefix": ("STRING", {
                    "default": "ComfyUI",
                    "tooltip": "Prefix for the filename."
                }),
            },
            "optional": {
                "filepath": ("STRING", {
                    "placeholder": "Saved file path will appear here after execution.",
                    "tooltip": "This field is automatically populated with the saved file path after save.",
                }),
            },
            "hidden": {"node_id": "UNIQUE_ID"},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_3d"
    OUTPUT_NODE = True
    CATEGORY = "Runware"
    DESCRIPTION = "Save 3D model files (GLB/PLY) from Runware 3D Inference to the output folder."

    def save_3d(self, filenamePrefix="ComfyUI", **kwargs):
        """Save 3D file from URL"""
        file_url = kwargs.get("3dObject", "")

        if not file_url or not file_url.strip():
            raise Exception("No 3D URL provided. Please connect the '3dObject' output from Runware 3D Inference node.")

        file_url = file_url.strip()

        # Get output directory
        output_dir = folder_paths.get_output_directory()
        threed_output_dir = os.path.join(output_dir, "3d_models")
        os.makedirs(threed_output_dir, exist_ok=True)

        # Get extension from URL (handle query parameters)
        url_without_params = file_url.split('?')[0]
        extension = url_without_params.split('.')[-1].lower()

        if extension not in ["glb", "ply"]:
            raise Exception(f"Unsupported 3D file extension '{extension}' from URL. Expected .glb or .ply.")

        # Sanitize filenamePrefix to prevent path traversal or arbitrary subdir creation
        prefix_basename = os.path.basename(
            filenamePrefix.replace(os.sep, "_").replace(os.altsep or os.sep, "_")
        )
        safe_prefix = re.sub(r"[^\w\-]", "", prefix_basename) or "ComfyUI"

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_prefix}_{timestamp}.{extension}"
        filepath = os.path.join(threed_output_dir, filename)

        # Download with retry logic
        max_retries = 10
        retry_delays = [2, 5, 10, 15, 20]

        for attempt in range(max_retries):
            try:
                response = requests.get(file_url, stream=True, timeout=60)
                print(f"[Runware Save 3D] Download attempt {attempt + 1}: {response.status_code}")

                if response.status_code == 422:
                    print(f"[Runware Save 3D] Server still processing, waiting...")
                    rwUtils.time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue

                if response.status_code == 502:
                    print(f"[Runware Save 3D] Server error (502), retrying...")
                    rwUtils.time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue

                response.raise_for_status()

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"[Runware Save 3D] Successfully saved to: {filepath}")

                # Send filepath to UI (like media upload mediaUUID)
                rwUtils.sendSave3DFilepath(filepath, kwargs.get("node_id"))

                return {"result": (filepath,), "ui": {"text": (f"Saved: {filename}",)}}

            except requests.exceptions.RequestException as e:
                print(f"[Runware Save 3D] Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    rwUtils.time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue
                else:
                    raise Exception(f"Failed to download 3D file after {max_retries} attempts: {e}")
            except Exception as e:
                print(f"[Runware Save 3D] Unexpected error: {e}")
                raise Exception(f"Failed to save 3D file: {e}")

        raise Exception("Failed to download 3D file: max retries exceeded")


NODE_CLASS_MAPPINGS = {
    "RunwareSave3D": RunwareSave3D,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareSave3D": "Runware Save 3D",
}
