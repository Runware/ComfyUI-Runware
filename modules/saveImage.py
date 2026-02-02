from .utils import runwareUtils as rwUtils
import folder_paths
import os
import requests
from datetime import datetime

class RunwareSaveImage:
    """Runware Save Image node that respects format from imageURL"""
    
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
    
    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Runware"
    
    def save_images(self, Images, filenamePrefix="ComfyUI", saveImage=True):
        """Save images using URL directly"""
        
        # Split URLs if comma-separated (for batch processing)
        image_urls = [url.strip() for url in Images.split(",") if url.strip()]
        
        if not image_urls:
            raise Exception("No image added provided. Please connect the 'Image' from Runware Image Inference node.")
        
        # Use output dir when saving, temp dir for preview only (purged on restart)
        if saveImage:
            output_dir = folder_paths.get_output_directory()
            os.makedirs(output_dir, exist_ok=True)
            file_type = "output"
        else:
            output_dir = folder_paths.get_temp_directory()
            file_type = "temp"
        
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, image_url in enumerate(image_urls):
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            img_data = response.content
            
            url_without_params = image_url.split('?')[0]
            extension = "." + url_without_params.split('.')[-1]
            
            if len(image_urls) > 1:
                filename = f"{filenamePrefix}_{timestamp}_{i+1:03}.{extension.lstrip('.')}"
            else:
                filename = f"{filenamePrefix}_{timestamp}.{extension.lstrip('.')}"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(img_data)
            print(f"[Runware] {'Saved' if saveImage else 'Preview'}: {filepath}")
            
            saved_files.append({
                "filename": filename,
                "subfolder": "",
                "type": file_type
            })
        
        return {"ui": {"images": saved_files}}
