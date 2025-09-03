from .utils import runwareUtils as rwUtils


class RunwareFrameImages:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "image1": ("IMAGE", {
                    "tooltip": "Frame image that will constrain video content at a specific timeline position. Used for keyframe control.",
                }),
                "frame1_position": (["auto", "first", "last", "0", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120"], {
                    "default": "auto",
                    "tooltip": "Frame position: 'auto' (automatic distribution), 'first' (beginning), 'last' (end), or specific frame number (0-120).",
                }),
                "image2": ("IMAGE", {
                    "tooltip": "Frame image that will constrain video content at a specific timeline position. Used for keyframe control.",
                }),
                "frame2_position": (["auto", "first", "last", "0", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120"], {
                    "default": "auto", 
                    "tooltip": "Frame position: 'auto' (automatic distribution), 'first' (beginning), 'last' (end), or specific frame number (0-120).",
                }),
                "image3": ("IMAGE", {
                    "tooltip": "Frame image that will constrain video content at a specific timeline position. Used for keyframe control.",
                }),
                "frame3_position": (["auto", "first", "last", "0", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120"], {
                    "default": "auto",
                    "tooltip": "Frame position: 'auto' (automatic distribution), 'first' (beginning), 'last' (end), or specific frame number (0-120).",
                }),
                "image4": ("IMAGE", {
                    "tooltip": "Frame image that will constrain video content at a specific timeline position. Used for keyframe control.",
                }),
                "frame4_position": (["auto", "first", "last", "0", "12", "24", "36", "48", "60", "72", "84", "96", "108", "120"], {
                    "default": "auto",
                    "tooltip": "Frame position: 'auto' (automatic distribution), 'first' (beginning), 'last' (end), or specific frame number (0-120).",
                }),
            }
        }
    
    DESCRIPTION = "Define keyframes that constrain specific frames within the video timeline. Different from reference images - these control WHEN specific visual content appears, not overall style consistency."
    FUNCTION = "create_frame_images"
    RETURN_TYPES = ("RUNWAREFRAMEIMAGES",)
    RETURN_NAMES = ("Frame Images",)
    CATEGORY = "Runware"
    
    def create_frame_images(self, **kwargs):
        frame_images = []
        
        # Process each image input
        for i in range(1, 5):  # Support up to 4 images
            image_key = f"image{i}"
            position_key = f"frame{i}_position"
            
            image = kwargs.get(image_key)
            position = kwargs.get(position_key, "auto")
            
            if image is not None:
                # Upload image and get UUID
                image_uuid = rwUtils.convertTensor2IMGForVideo(image)
                image_url = f"https://im.runware.ai/image/ii/{image_uuid}.webp"
                
                frame_data = {
                    "inputImage": image_url
                }
                
                # Only add frame position if not auto
                if position != "auto":
                    # Convert string numbers to integers for API
                    if position.isdigit():
                        frame_data["frame"] = int(position)
                    else:
                        frame_data["frame"] = position  # "first" or "last"
                
                frame_images.append(frame_data)
        
        return (frame_images,)


# Node class mappings for ComfyUI registration
NODE_CLASS_MAPPINGS = {
    "RunwareFrameImages": RunwareFrameImages,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RunwareFrameImages": "Runware Frame Images",
}
