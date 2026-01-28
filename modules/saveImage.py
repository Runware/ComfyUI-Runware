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
                "filename_prefix": ("STRING", {
                    "default": "ComfyUI",
                    "tooltip": "Prefix for the filename."
                }),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "save_images"
    OUTPUT_NODE = True
    CATEGORY = "Runware"
    
    def save_images(self, Images, filename_prefix="ComfyUI"):
        """Save images using URL directly"""
        
        # Get output directory
        output_dir = folder_paths.get_output_directory()
        os.makedirs(output_dir, exist_ok=True)
        
        # Split URLs if comma-separated (for batch processing)
        image_urls = [url.strip() for url in Images.split(",") if url.strip()]
        
        if not image_urls:
            raise Exception("No image added provided. Please connect the 'Image' from Runware Image Inference node.")
        
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Process each image
        for i, image_url in enumerate(image_urls):
            # Download original file directly from URL to preserve quality
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            img_data = response.content
            
            # Get extension from URL (handle query parameters)
            url_without_params = image_url.split('?')[0]
            extension = "." + url_without_params.split('.')[-1]
            
            # Generate filename with timestamp
            if len(image_urls) > 1:
                filename = f"{filename_prefix}_{timestamp}_{i+1:03}.{extension.lstrip('.')}"
            else:
                filename = f"{filename_prefix}_{timestamp}.{extension.lstrip('.')}"
            filepath = os.path.join(output_dir, filename)
            
            # Write the downloaded file
            with open(filepath, 'wb') as f:
                f.write(img_data)
            print(f"[Runware] Saved original file: {filepath}")
            
            # Add preview data for ComfyUI
            saved_files.append({
                "filename": filename,
                "subfolder": "",
                "type": "output"
            })
        
        return {"ui": {"images": saved_files}}
