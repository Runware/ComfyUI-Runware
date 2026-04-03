"""
Runware Video Inference Elements — builds inputs.elements[] for videoInference (Kling elements, etc.).
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from .utils import runwareUtils as rwUtils

_REF_IMAGE_SLOTS = 3
_REF_VIDEO_SLOTS = 4

_ALLOWED_TAGS = frozenset(
    {
        "Hottest",
        "Character",
        "Animal",
        "Item",
        "Costume",
        "Scene",
        "Effect",
        "Others",
    }
)


def _split_lines_or_csv(value: Optional[str]) -> List[str]:
    if value is None:
        return []
    s = str(value).strip()
    if not s:
        return []
    parts = re.split(r"[\n,]+", s)
    return [p.strip() for p in parts if p.strip()]


def _parse_tags(value: Optional[str]) -> List[str]:
    raw = _split_lines_or_csv(value)
    if not raw:
        return []
    out: List[str] = []
    for t in raw:
        if t in _ALLOWED_TAGS:
            if t not in out:
                out.append(t)
    return out


def _build_element_dict(
    id_: str,
    description: str,
    frontalImage: Any,
    refer_images: List[Any],
    refer_videos: List[Any],
    voice: str,
    tags: str,
) -> Dict[str, Any]:
    el: Dict[str, Any] = {}
    id_s = (id_ or "").strip()
    if id_s:
        el["id"] = id_s
    desc = (description or "").strip()
    if desc:
        el["description"] = desc
    if isinstance(frontalImage, str):
        front = frontalImage.strip()
        if front:
            el["frontalImage"] = front
    elif frontalImage is not None:
        el["frontalImage"] = frontalImage
    imgs = [x for x in refer_images if x is not None]
    if imgs:
        el["images"] = imgs
    vids = [x for x in refer_videos if x is not None]
    if vids:
        el["videos"] = vids
    voices = _split_lines_or_csv(voice)
    if voices:
        el["voice"] = voices
    tag_list = _parse_tags(tags)
    if tag_list:
        el["tags"] = tag_list
    return el


class RunwareVideoInferenceElements:
    """One Kling / video inference element for inputs.elements."""

    @classmethod
    def INPUT_TYPES(cls):
        optional: Dict[str, tuple] = {
                "id": ("STRING", {
                    "default": "",
                    "tooltip": "User-facing element id (max 20 chars on API). For reuse, set only id with no reference media.",
                }),
                "description": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Optional element description (e.g. for image_refer / new elements).",
                }),
                "frontalImage": ("IMAGE", {
                    "tooltip": "Frontal reference image for the element.",
                }),
                "voice": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Voice file URLs (mp3/wav/mp4/mov), one per line or comma-separated.",
                }),
                "tags": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Comma or newline-separated tags: Hottest, Character, Animal, Item, Costume, Scene, Effect, Others.",
                }),
        }
        for i in range(1, _REF_IMAGE_SLOTS + 1):
            optional[f"images_{i}"] = ("IMAGE", {
                "tooltip": f"Optional reference image {i} for image_refer (up to {_REF_IMAGE_SLOTS}).",
            })
        for i in range(1, _REF_VIDEO_SLOTS + 1):
            optional[f"videos_{i}"] = ("VIDEO", {
                "tooltip": f"Optional reference video {i} for video_refer (file-backed VIDEO, e.g. Load Video).",
            })
        return {"required": {}, "optional": optional}

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCEELEMENTS",)
    RETURN_NAMES = ("Elements",)
    FUNCTION = "build_element"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Define a single video inference element (id, description, frontalImage, images_1…images_3, videos_1…videos_4, voice, tags) "
        "for inputs.elements on Kling and compatible models. Connect to Runware Video Inference Inputs → Elements, "
        "or use Runware Video Inference Elements Combine for multiple elements."
    )

    def build_element(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        frontal_image = kwargs.get("frontalImage", None)
        frontal_image_value = None
        if frontal_image is not None:
            frontal_image_value = rwUtils.convertTensor2IMG(frontal_image)

        refer_images: List[Any] = []
        for i in range(1, _REF_IMAGE_SLOTS + 1):
            slot = kwargs.get(f"images_{i}")
            if slot is not None:
                refer_images.append(rwUtils.convertTensor2IMG(slot))

        refer_videos: List[Any] = []
        for i in range(1, _REF_VIDEO_SLOTS + 1):
            slot = kwargs.get(f"videos_{i}")
            if slot is not None:
                refer_videos.append(rwUtils.convertVideoInputToDataUri(slot))

        el = _build_element_dict(
            str(kwargs.get("id") or ""),
            str(kwargs.get("description") or ""),
            frontal_image_value,
            refer_images,
            refer_videos,
            str(kwargs.get("voice") or ""),
            str(kwargs.get("tags") or ""),
        )
        if not el:
            raise ValueError(
                "Runware Video Inference Elements: provide at least id, description, frontalImage, "
                "images_1…images_3, videos_1…videos_4, voice, or tags."
            )
        return ([el],)


class RunwareVideoInferenceElementsCombine:
    """Combine multiple Runware Video Inference Elements (each output is a list) into one list."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Elements 1": ("RUNWAREVIDEOINFERENCEELEMENTS", {
                    "tooltip": "Connect a Runware Video Inference Elements node (single-element list).",
                }),
            },
            "optional": {
                "Elements 2": ("RUNWAREVIDEOINFERENCEELEMENTS", {
                    "tooltip": "Optional second Runware Video Inference Elements node.",
                }),
                "Elements 3": ("RUNWAREVIDEOINFERENCEELEMENTS", {
                    "tooltip": "Optional third Runware Video Inference Elements node.",
                }),
                "Elements 4": ("RUNWAREVIDEOINFERENCEELEMENTS", {
                    "tooltip": "Optional fourth Runware Video Inference Elements node.",
                }),
            },
        }

    RETURN_TYPES = ("RUNWAREVIDEOINFERENCEELEMENTS",)
    RETURN_NAMES = ("Elements",)
    FUNCTION = "combine"
    CATEGORY = "Runware"
    DESCRIPTION = (
        "Combine up to four Runware Video Inference Elements outputs into inputs.elements. "
        "Connect the result to Runware Video Inference Inputs → Elements."
    )

    def combine(self, **kwargs) -> Tuple[List[Dict[str, Any]]]:
        out: List[Dict[str, Any]] = []
        for i in range(1, 5):
            key = f"Elements {i}"
            chunk = kwargs.get(key)
            if chunk is not None and isinstance(chunk, list):
                out.extend(
                    e for e in chunk
                    if isinstance(e, dict) and len(e) > 0
                )
        if not out:
            raise ValueError(
                "Runware Video Inference Elements Combine: connect at least one non-empty Elements input."
            )
        return (out,)
