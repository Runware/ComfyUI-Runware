from .utils import runwareUtils as rwUtils


class imageMasking:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Image": ("IMAGE", {
                    "tooltip": "Specifies the input image to be processed for mask generation."
                }),
                "Detection Model": ([
                    "face_yolov8n", "face_yolov8s", "mediapipe_face_full", "mediapipe_face_short", "mediapipe_face_mesh",
                    "mediapipe_face_mesh_eyes_only", "eyes_mesh_mediapipe", "nose_mesh_mediapipe", "lips_mesh_mediapipe",
                    "eyes_lips_mesh", "nose_eyes_mesh", "nose_lips_mesh", "hand_yolov8n", "person_yolov8n-seg", "person_yolov8s-seg"
                ], {
                    "tooltip": "Specifies the specialized detection model to use for mask generation.",
                    "default": "face_yolov8n",
                }),
                "Confidence": ("FLOAT", {
                    "tooltip": "Confidence threshold for detections. Only detections with confidence scores above this threshold will be included in the mask.",
                    "default": 0.25,
                    "min": 0,
                    "max": 1,
                    "step": 0.01,
                }),
                "Max Detections": ("INT", {
                    "tooltip": "Limits the maximum number of elements (faces, hands, or people) that will be detected and masked in the image. If there are more elements than this value, only the ones with highest confidence scores will be included.",
                    "default": 6,
                    "min": 1,
                    "max": 20,
                }),
                "Mask Padding": ("INT", {
                    "tooltip": "Extends or reduces the detected mask area by the specified number of pixels. Positive values create a larger masked region (useful when you want to ensure complete coverage of the element), while negative values shrink the mask (useful for tighter, more focused areas).",
                    "default": 4,
                    "min": -40,
                    "max": 40,
                }),
                "Mask Blur": ("INT", {
                    "tooltip": "Extends the mask by the specified number of pixels with a gradual fade-out effect, creating smooth transitions between masked and unmasked regions in the final result.",
                    "default": 4,
                    "min": 0,
                    "max": 20,
                }),
            },
        }

    DESCRIPTION = "Image Masking provides intelligent detection and mask generation for specific elements in images, particularly optimized for faces, hands, and people. Built on advanced detection models, this feature enhances the inpainting workflow by automatically creating precise masks around detected elements, enabling targeted enhancement and detailing."

    FUNCTION = "imageMasking"
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("Image", "Mask Preview", "Mask")
    CATEGORY = "Runware"

    def imageMasking(self, **kwargs):
        image = kwargs.get("Image")
        detectionModel = kwargs.get("Detection Model")
        confidence = kwargs.get("Confidence")
        maxDetections = kwargs.get("Max Detections")
        maskPadding = kwargs.get("Mask Padding")
        maskBlur = kwargs.get("Mask Blur")

        model_mapping = {
            "face_yolov8n": "runware:35@1",
            "face_yolov8s": "runware:35@2",
            "mediapipe_face_full": "runware:35@6",
            "mediapipe_face_short": "runware:35@7",
            "mediapipe_face_mesh": "runware:35@8",
            "mediapipe_face_mesh_eyes_only": "runware:35@9",
            "eyes_mesh_mediapipe": "runware:35@15",
            "nose_mesh_mediapipe": "runware:35@13",
            "lips_mesh_mediapipe": "runware:35@14",
            "eyes_lips_mesh": "runware:35@10",
            "nose_eyes_mesh": "runware:35@11",
            "nose_lips_mesh": "runware:35@12",
            "hand_yolov8n": "runware:35@3",
            "person_yolov8n-seg": "runware:35@4",
            "person_yolov8s-seg": "runware:35@5"
        }
        detectionModel = model_mapping.get(detectionModel, detectionModel)

        genConfig = [
            {
                "taskType": "imageMasking",
                "taskUUID": rwUtils.genRandUUID(),
                "inputImage": rwUtils.convertTensor2IMG(image),
                "model": detectionModel,
                "confidence": confidence,
                "maxDetections": maxDetections,
                "outputType": "URL",
                "outputFormat": rwUtils.OUTPUT_FORMAT,
                "outputQuality": rwUtils.OUTPUT_QUALITY,
            }
        ]

        genConfig[0]["maskPadding"] = maskPadding
        genConfig[0]["maskBlur"] = maskBlur

        genResult = rwUtils.inferenecRequest(genConfig)
        image_url = rwUtils.extractImageURLs(genResult)
        return (image, image_url, image_url)
