import folder_paths
import os
import io
import requests
import torch
import numpy as np
from PIL import Image
from datetime import datetime


def _bytes_to_image_tensor(img_data: bytes):
    """Decode image bytes to ComfyUI IMAGE tensor [1, H, W, C] float32 0-1."""
    pil = Image.open(io.BytesIO(img_data)).convert("RGB")
    arr = np.array(pil).astype(np.float32) / 255.0
    return torch.from_numpy(arr).unsqueeze(0)


class RunwareSaveImage:
    """Runware Save Image: download from URL(s), save/preview to disk, and forward as IMAGE for chaining."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Images": ("STRING", {
                    "tooltip": "Image URL(s) from Runware Image Inference node. For multiple images, URLs should be comma-separated."
                }),
                "filenamePrefix": ("STRING", {
                    "default": "ComfyUI",
                    "tooltip": "Prefix for the filename."
                }),
                "saveImage": ("BOOLEAN", {
                    "default": True,
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                    "tooltip": "If true, save to output folder. If false, download and preview only (purged when ComfyUI restarts)."
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Runware"

    def save_images(self, Images, filenamePrefix="ComfyUI", saveImage=True):
        """Download image(s) from URL(s), save/preview to disk, update gallery, and return IMAGE for downstream nodes."""

        image_urls = [url.strip() for url in Images.split(",") if url.strip()]

        if not image_urls:
            raise Exception("No images provided. Connect the 'IMAGE' output from Runware Image Inference node.")

        if saveImage:
            output_dir = folder_paths.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            file_type = "output"
        else:
            output_dir = folder_paths.get_temp_directory()
            file_type = "temp"

        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tensors = []

        for i, image_url in enumerate(image_urls):
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            img_data = response.content

            tensors.append(_bytes_to_image_tensor(img_data))

            url_without_params = image_url.split("?")[0]
            ext = url_without_params.split(".")[-1].lstrip(".") or "png"
            extension = "." + ext
            if len(image_urls) > 1:
                filename = f"{filenamePrefix}_{timestamp}_{i+1:03}{extension}"
            else:
                filename = f"{filenamePrefix}_{timestamp}{extension}"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"[Runware] {'Saved' if saveImage else 'Preview'}: {filepath}")

            saved_files.append({
                "filename": filename,
                "subfolder": "",
                "type": file_type
            })

        image_batch = torch.cat(tensors, dim=0)
        return {"result": (image_batch,), "ui": {"images": saved_files}}
