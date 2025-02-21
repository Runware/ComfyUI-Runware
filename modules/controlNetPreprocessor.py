from .utils import runwareUtils as rwUtils

class controlNetPreprocessor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                        "tooltip": "Specifies the input image to be preprocessed to generate a guide image. This guide image will be used as a reference for image generation processes, guiding the AI to generate images that are more aligned with the input image."
                }),
                "PreProcessor Type": ([
                        "Canny",
                        "Depth",
                        "MLSD",
                        "NormalBAE",
                        "OpenPose",
                        "Tile",
                        "Seg",
                        "LineArt",
                        "LineArtAnime",
                        "Shuffle",
                        "Scribble",
                        "SoftEdge",
                    ], {
                    "tooltip": "Choose Preprocessor Type To Generate The Guide Image.",
                    "default": "Canny",
                }),
                "Include Hands And Faces [ OpenPose ]": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include the hands and face in the pose outline when using the OpenPose preprocessor.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "Canny Low Threshold": ("INT", {
                        "tooltip": "Defines the lower threshold when using the Canny edge detection preprocessor.",
                        "default": 100,
                        "min": 0,
                        "max": 255,
                }),
                "Canny High Threshold": ("INT", {
                        "tooltip": "Defines the high threshold when using the Canny edge detection preprocessor.",
                        "default": 200,
                        "min": 0,
                        "max": 255,
                }),
                "Image Resizing": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "It Allows Image Resizing if the dimension of the image is higher than a specific value it will be resized.",
                    "label_on": "Enabled",
                    "label_off": "Disabled",
                }),
                "dimensions": ([
                    "Square (512x512)", "Square HD (1024x1024)", "Portrait 3:4 (768x1024)",
                    "Portrait 9:16 (576x1024)", "Landscape 4:3 (1024x768)",
                    "Landscape 16:9 (1024x576)", "Custom"
                ], {
                    "default": "Square HD (1024x1024)",
                    "tooltip": "Resize the dimensions of the generated Guide image by specifying its width and height in pixels, or select from the predefined options. Image dimensions must be multiples of 64 (e.g., 512x512, 1024x768).",
                }),
                "width": ("INT", {
                        "tooltip": "If the Image height dimension is larger than this value, the output image will be resized to the specified height.",
                        "default": 1024,
                        "min": 512,
                        "max": 2048,
                        "step": 64,
                }),
                "height": ("INT", {
                        "tooltip": "If the Image width dimension is larger than this value, the output image will be resized to the specified width.",
                        "default": 1024,
                        "min": 512,
                        "max": 2048,
                        "step": 64,
                    }),
            },
        }

    DESCRIPTION = "ControlNet offers advanced capabilities for precise image processing through the use of guide images in specific formats, known as preprocessed images. This powerful tool enhances the control and customization of image generation, enabling users to achieve desired artistic styles and detailed adjustments effectively."
    FUNCTION = "controlNetPreProcess"
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("GUIDE IMAGE",)
    CATEGORY = "Runware"

    def controlNetPreProcess(self, **kwargs):
        image = kwargs.get("Image")
        preProcessorType = kwargs.get("PreProcessor Type")
        includeHandsAndFaces = kwargs.get("Include Hands And Faces [ OpenPose ]")
        cannyLowThreshold = kwargs.get("Canny Low Threshold")
        cannyHighThreshold = kwargs.get("Canny High Threshold")
        imageResizing = kwargs.get("Image Resizing")
        width = kwargs.get("width")
        height = kwargs.get("height")

        genConfig = [
            {
                "taskType": "imageControlNetPreProcess",
                "taskUUID": rwUtils.genRandUUID(),
                "inputImage": rwUtils.convertTensor2IMG(image),
                "preProcessorType": preProcessorType,
                "outputFormat": rwUtils.OUTPUT_FORMAT,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
                "outputType": "base64Data",
            }
        ]

        # For Debugging Purposes Only
        print(f"[Debugging] Task UUID: {genConfig[0]['taskUUID']}")

        if(imageResizing):
            genConfig[0]["width"] = width
            genConfig[0]["height"] = height
        if(preProcessorType == "OpenPose" and includeHandsAndFaces):
            genConfig[0]["includeHandsAndFaceOpenPose"] = includeHandsAndFaces
        elif(preProcessorType == "Canny"):
            genConfig[0]["lowThresholdCanny"] = cannyLowThreshold
            genConfig[0]["highThresholdCanny"] = cannyHighThreshold

        genResult = rwUtils.inferenecRequest(genConfig)
        images = rwUtils.convertImageB64List(genResult)
        return images