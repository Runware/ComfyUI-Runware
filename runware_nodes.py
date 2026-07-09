"""
ComfyUI runtime for Runware nodes.

One node per curated model, generated from the schema bundle (`build_node`),
every node running through the Python SDK over REST. Node logic lives once in
the base class; generated classes are thin data. Plus a generic untyped node
for models newer than the installed pack.

Coverage: image (IMAGE tensor in/out), video/audio/3D (saved file → path),
text (STRING). Nested params (lora, controlNet, providerSettings) ride in via an
`advanced_json` input.

torch / numpy / PIL / folder_paths come from the ComfyUI runtime; `runware` and
`pillow` from requirements.txt. API key from RUNWARE_API_KEY.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import base64
import importlib.util
import io
import json
import os
import urllib.request
import uuid
from typing import Any


# ComfyUI capability probes (resolved once at import). Audio/video outputs use the
# richer native types when available and degrade to a saved file path otherwise. Audio
# decodes via soundfile (libsndfile, no FFmpeg) or torchaudio, whichever is installed.
_HAS_AUDIO = any(importlib.util.find_spec(m) is not None for m in ("soundfile", "torchaudio"))
_VideoFromFile: Any = None
if importlib.util.find_spec("comfy_api") is not None:
    # `comfy_api.input` is a back-compat shim that no longer re-exports VideoFromFile; the class
    # lives in `comfy_api.latest` on current ComfyUI. Try both so video keeps its native VIDEO type
    # across versions instead of silently degrading to a file path.
    for _mod in ("comfy_api.latest", "comfy_api.input"):
        try:
            _VideoFromFile = importlib.import_module(_mod).VideoFromFile  # type: ignore[attr-defined]
            break
        except Exception:  # noqa: BLE001
            _VideoFromFile = None
_HAS_VIDEO = _VideoFromFile is not None


# ----------------------------------------------------------------------- client identity


def _package_version() -> str:
    """Version from the shipped pyproject.toml (no tomllib import needed)."""
    pyproject = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyproject.toml")
    try:
        with open(pyproject, encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if stripped.startswith("version") and "=" in stripped:
                    return stripped.split("=", 1)[1].strip().strip("'\"")
    except OSError:
        pass
    return "0.0.0"


# Passed to the SDK as its User-Agent prefix so Runware can attribute ComfyUI
# traffic: `runware-comfyui/<ver> runware-python/<sdk> (python/…) schemas/…`.
USER_AGENT_PREFIX = f"runware-comfyui/{_package_version()}"


# ----------------------------------------------------------------------- async bridge


def run_blocking(coro: Any) -> Any:
    """Drive an async coroutine from sync node code, even inside ComfyUI's loop."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


_UI_API_KEY: str | None = None  # set from the ComfyUI Settings panel via /runware/set_key


def resolve_api_key() -> str | None:
    """RUNWARE_API_KEY env var, else the ComfyUI Settings key, else `runware auth login`."""
    key = os.environ.get("RUNWARE_API_KEY")
    if key:
        return key.strip()
    if _UI_API_KEY:
        return _UI_API_KEY
    try:
        with open(os.path.expanduser("~/.runware/config.yaml")) as fh:
            for line in fh:
                lower = line.strip().lower()
                if ":" in line and any(lower.startswith(k) for k in ("api_key", "apikey", "key", "token")):
                    return line.split(":", 1)[1].strip().strip("'\"")
    except OSError:
        pass
    return None


async def run_request(request: dict[str, Any]) -> list[dict[str, Any]]:
    from runware import Runware  # noqa: PLC0415

    api_key = resolve_api_key()
    if not api_key:
        raise RuntimeError("No Runware API key. Set RUNWARE_API_KEY or run `runware auth login`.")
    async with Runware(api_key=api_key, transport="rest", user_agent_prefix=USER_AGENT_PREFIX) as client:
        return await client.run(request)


def _clean_error(exc: BaseException) -> str:
    """A short, readable one-liner for a failed request, hiding the SDK/asyncio stack. Surfaces
    the Runware error's parameter / code / HTTP status when present so the message is actionable."""
    msg = str(getattr(exc, "message", None) or exc).strip() or exc.__class__.__name__
    tail: list[str] = []
    param = getattr(exc, "parameter", None)
    code = getattr(exc, "code", None)
    status = getattr(exc, "status_code", None)
    if param:
        tail.append(f"parameter '{param}'")
    if code and str(code).lower() not in msg.lower():
        tail.append(f"code {code}")
    if status:
        tail.append(f"HTTP {status}")
    return "Runware: " + msg + (f"  [{', '.join(tail)}]" if tail else "")


def run_request_blocking(request: dict[str, Any]) -> list[dict[str, Any]]:
    """Run a request synchronously, but on failure raise a clean single-line error instead of the
    deep SDK/asyncio traceback ComfyUI would otherwise dump. Set RUNWARE_DEBUG for the full stack."""
    try:
        return run_blocking(run_request(request))
    except Exception as exc:  # noqa: BLE001
        if os.environ.get("RUNWARE_DEBUG"):
            import traceback  # noqa: PLC0415
            traceback.print_exc()
        raise RuntimeError(_clean_error(exc)) from None


# ---------------------------------------------------------------------------- imaging


def _imaging() -> tuple[Any, Any, Any]:
    import numpy as np  # noqa: PLC0415
    import torch  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415
    return torch, np, Image


def tensor_to_data_uris(image: Any) -> list[str]:
    """ComfyUI IMAGE tensor [B,H,W,C] float 0-1 → list of PNG data URIs."""
    _, np, Image = _imaging()
    arr = (image.clamp(0, 1).cpu().numpy() * 255.0).round().astype("uint8")
    uris: list[str] = []
    for frame in arr:
        buf = io.BytesIO()
        Image.fromarray(frame).save(buf, format="PNG")
        uris.append("data:image/png;base64," + base64.b64encode(buf.getvalue()).decode())
    return uris


def urls_to_image(urls: list[str]) -> Any:
    torch, np, Image = _imaging()
    if not urls:
        return torch.zeros((1, 512, 512, 3))
    frames = []
    for url in urls:
        data = urllib.request.urlopen(url).read()  # noqa: S310
        pil = Image.open(io.BytesIO(data)).convert("RGB")
        frames.append(np.asarray(pil).astype("float32") / 255.0)
    return torch.from_numpy(np.stack(frames))


def mask_to_data_uri(mask: Any) -> str:
    """ComfyUI MASK [B,H,W] (or [H,W]) float 0-1 → grayscale PNG data URI."""
    _, np, Image = _imaging()
    arr = mask.clamp(0, 1).cpu().numpy()
    if arr.ndim == 3:
        arr = arr[0]
    arr = (arr * 255.0).round().astype("uint8")
    buf = io.BytesIO()
    Image.fromarray(arr, mode="L").save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


# ------------------------------------------------------------------------- file saving


def _output_dir() -> str:
    try:
        import folder_paths  # noqa: PLC0415  (provided by ComfyUI)
        return folder_paths.get_output_directory()
    except Exception:  # noqa: BLE001
        import tempfile  # noqa: PLC0415
        return tempfile.gettempdir()


def _download(url: str, suffix: str) -> str:
    path = os.path.join(_output_dir(), f"runware_{uuid.uuid4().hex[:8]}{suffix}")
    with open(path, "wb") as fh:
        fh.write(urllib.request.urlopen(url).read())  # noqa: S310
    return path


def _media_url(result: dict[str, Any]) -> str | None:
    for key in ("videoURL", "audioURL", "imageURL", "URL", "url"):
        if result.get(key):
            return result[key]
    outs = result.get("outputs")
    if isinstance(outs, dict):
        files = outs.get("files")
        if isinstance(files, list) and files and isinstance(files[0], dict):
            return files[0].get("url")
    return None


def _audio_output(url: str) -> Any:
    """Decode a returned audio file into a ComfyUI AUDIO dict {waveform, sample_rate}.
    Prefers soundfile (libsndfile, no FFmpeg dependency) and falls back to torchaudio."""
    import torch  # noqa: PLC0415
    path = _download(url, _SUFFIX.get("audioInference", ".mp3"))
    try:  # soundfile: self-contained libsndfile, decodes WAV/FLAC/OGG (and MP3 on libsndfile >= 1.1)
        import numpy as np  # noqa: PLC0415
        import soundfile as sf  # noqa: PLC0415
        data, sample_rate = sf.read(path, dtype="float32", always_2d=True)  # (frames, channels)
        return {"waveform": torch.from_numpy(np.ascontiguousarray(data.T)).unsqueeze(0),
                "sample_rate": int(sample_rate)}
    except Exception:  # noqa: BLE001
        pass
    try:
        import torchaudio  # noqa: PLC0415
        waveform, sample_rate = torchaudio.load(path)
        return {"waveform": waveform.unsqueeze(0), "sample_rate": int(sample_rate)}
    except Exception as exc:  # noqa: BLE001
        print(f"[Runware] audio decode failed ({exc}); install `soundfile`. File saved at {path}")
        return {"waveform": torch.zeros(1, 2, 1), "sample_rate": 44100}


def _video_output(url: str) -> Any:
    """Wrap a returned video file as a ComfyUI VIDEO object, or fall back to its path."""
    path = _download(url, _SUFFIX.get("videoInference", ".mp4"))
    if _VideoFromFile is not None:
        try:
            return _VideoFromFile(path)
        except Exception as exc:  # noqa: BLE001
            print(f"[Runware] video wrap failed ({exc}); file saved at {path}")
    return path


def _set_path(obj: dict[str, Any], path: list[str], value: Any) -> None:
    cur = obj
    for key in path[:-1]:
        cur = cur.setdefault(key, {})
    cur[path[-1]] = value


def _total_cost(results: list[dict[str, Any]]) -> float:
    """Sum the API cost across results (present when includeCost was requested)."""
    try:
        return sum(float(r.get("cost") or 0) for r in results if isinstance(r, dict))
    except (TypeError, ValueError):
        return 0.0


def _socket_fields_from_inputs(input_types: dict[str, Any]) -> dict[str, set[str]]:
    """Per array-feature socket, the item fields this model accepts, read from the `rw_socket_fields`
    the generator placed on the socket in INPUT_TYPES."""
    out: dict[str, set[str]] = {}
    for scope in ("required", "optional"):
        for name, spec in (input_types.get(scope) or {}).items():
            if isinstance(spec, (list, tuple)) and len(spec) == 2 and isinstance(spec[1], dict):
                fields = spec[1].get("rw_socket_fields")
                if fields:
                    out[name] = set(fields)
    return out


def _strip_unsupported_fields(request: dict[str, Any], socket_fields: dict[str, set[str]]) -> None:
    """Drop fields a model does not declare from its feature values. A shared builder is the union
    of every model's fields, so it can produce more than a given model accepts: array features
    (ControlNet/IP-Adapter/LoRA) strip per item, single-object features (Speech) strip the object."""
    for slot, allowed in socket_fields.items():
        value = request.get(slot)
        if isinstance(value, list):
            request[slot] = [
                {k: v for k, v in item.items() if k in allowed} if isinstance(item, dict) else item
                for item in value
            ]
        elif isinstance(value, dict):
            request[slot] = {k: v for k, v in value.items() if k in allowed}


def _run_info(results: list[dict[str, Any]]) -> str:
    """A short on-node summary of a run: total cost and whether the safety check flagged
    anything. Each field appears only when the response carried it (cost needs includeCost;
    NSFWContent is present only when the model ran a content check)."""
    parts: list[str] = []
    cost = _total_cost(results)
    if cost:
        parts.append("$" + f"{cost:.6f}".rstrip("0").rstrip("."))
    flags = [r.get("NSFWContent") for r in results if isinstance(r, dict) and "NSFWContent" in r]
    if flags:
        parts.append("NSFW: " + ("yes" if any(flags) else "no"))
    return "  ·  ".join(parts)  # middot separates cost from the NSFW flag


_SIZE_TRIAD = ("width", "height", "resolution")


def _apply_param_plan(target: dict[str, Any], kwargs: dict[str, Any], plan: dict[str, dict[str, Any]]) -> None:
    """Map widget inputs onto a request/item dict per the generated param plan."""
    size_choices: list[tuple[Any, dict[str, Any]]] = []
    for name, value in kwargs.items():
        if value is None:
            continue
        p = plan.get(name, {"path": [name], "kind": "scalar"})
        path, kind = p["path"], p["kind"]
        if p.get("gated_by") and not kwargs.get(p["gated_by"]):
            continue  # its group gate (e.g. `safety`) is off → leave the field to the model
        if kind in ("skip", "group_gate"):  # a gate's value widget, or a group toggle: never sent
            continue
        if kind == "size_choice":  # applied last: authoritative over the size triad
            size_choices.append((value, p))
            continue
        if kind == "scalar":
            if p.get("omit_empty") and isinstance(value, str) and not value.strip():
                continue  # empty optional string → let the model default
            if "omit_value" in p and value == p["omit_value"]:
                continue  # the "(default)" sentinel → omit
            _set_path(target, path, value)
        elif kind == "gate":  # a reveal toggle: send the paired value only when on
            if value:
                paired = kwargs.get(p["value_key"])
                if paired is not None:
                    _set_path(target, path, paired)
        elif kind == "bool_tri":  # (default) / enabled / disabled
            if value == "enabled":
                _set_path(target, path, True)
            elif value == "disabled":
                _set_path(target, path, False)
        elif kind == "feature":  # a builder's typed output (a list or object), placed as-is
            _set_path(target, path, value)
        elif kind == "media_string":
            if isinstance(value, str) and value.strip():
                _set_path(target, path, value.strip())
        elif kind == "media_array":
            if isinstance(value, str) and value.strip():
                _set_path(target, path, [line.strip() for line in value.splitlines() if line.strip()])
        elif kind == "image_scalar":
            _set_path(target, path, tensor_to_data_uris(value)[0])
        elif kind == "mask_scalar":
            _set_path(target, path, mask_to_data_uri(value))
        elif kind == "image_array":
            _set_path(target, path, tensor_to_data_uris(value))
        elif kind == "image_objects":
            type_value = p.get("type")
            _set_path(target, path, [
                {"image": u, **({"type": type_value} if type_value else {})}
                for u in tensor_to_data_uris(value)
            ])

    # A `size` dropdown folds the mutually-exclusive resolution/width/height into one
    # choice. Apply it after everything else and let it own the whole triad: a concrete
    # size clears the others so we never send a conflicting pair. An empty choice ("use
    # width and height") leaves the width/height widgets that were set above untouched.
    for value, p in size_choices:
        chosen = (p.get("options") or {}).get(value)
        if not isinstance(chosen, dict):
            continue
        concrete = {k: v for k, v in chosen.items() if not k.startswith("__")}
        if chosen.get("__none__") or concrete:  # explicit "None", or a concrete size: own the triad
            for k in _SIZE_TRIAD:
                target.pop(k, None)
            target.update(concrete)
        # an empty choice ("Custom") leaves the width/height widgets set above untouched


# --------------------------------------------------------------------------- base node


# Output classification by taskType (the `inference` list spans more than the 5
# modalities: it also carries image-producing operations and caption/vectorize).
_IMAGE_TASKS = {"imageInference", "upscale", "removeBackground", "imageMasking", "controlNetPreprocess"}
_TEXT_TASKS = {"textInference", "caption", "promptEnhance"}
_AUDIO_TASKS = {"audioInference"}
_VIDEO_TASKS = {"videoInference"}
_SUFFIX = {"videoInference": ".mp4", "audioInference": ".mp3", "3dInference": ".glb", "vectorize": ".svg"}
_LABEL = {
    "imageInference": "Image", "upscale": "Image", "removeBackground": "Image",
    "imageMasking": "Image", "controlNetPreprocess": "Image",
    "videoInference": "Video", "audioInference": "Audio", "3dInference": "3D",
    "textInference": "Text", "caption": "Text", "promptEnhance": "Text",
    "vectorize": "Vector", "training": "Training",
}
_FILE_RET = (("STRING",), ("file_path",))
_RET = {
    "image": (("IMAGE",), ("image",)),
    "text": (("STRING",), ("text",)),
    "audio": (("AUDIO",), ("audio",)) if _HAS_AUDIO else _FILE_RET,
    "video": (("VIDEO",), ("video",)) if _HAS_VIDEO else _FILE_RET,
    "file": _FILE_RET,
}


def _output_kind(task_type: str) -> str:
    if task_type in _IMAGE_TASKS:
        return "image"
    if task_type in _TEXT_TASKS:
        return "text"
    if task_type in _AUDIO_TASKS:
        return "audio"
    if task_type in _VIDEO_TASKS:
        return "video"
    return "file"


class _RunwareNode:
    MODEL = ""
    TASK_TYPE = ""
    PARAM_PLAN: dict[str, dict[str, Any]] = {}
    _INPUT_TYPES: dict[str, Any] = {}
    _SOCKET_FIELDS: dict[str, set[str]] = {}  # per array-feature socket, item fields this model accepts

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "execute"
    CATEGORY = "Runware"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return cls._INPUT_TYPES

    def execute(self, **kwargs: Any) -> Any:
        request: dict[str, Any] = {"model": self.MODEL, "taskType": self.TASK_TYPE, "includeCost": True}
        advanced = kwargs.pop("advanced_json", "") or ""

        # Widgets, media, images, and connected feature sockets all flow through the plan.
        # Params governed by a validation rule are off-by-default toggles in the node, so a
        # default request never breaks a rule and nothing is dropped silently.
        _apply_param_plan(request, kwargs, self.PARAM_PLAN)

        # A ControlNet/IP-Adapter builder is shared across models, so it can carry item fields
        # this model does not accept (architectures expand the base object). Drop those, so a
        # builder wired into a model that only has the base fields sends a request it accepts.
        _strip_unsupported_fields(request, self._SOCKET_FIELDS)

        # Raw advanced JSON is the user's escape hatch and wins on conflict.
        if advanced.strip():
            try:
                data = json.loads(advanced)
                if isinstance(data, dict):
                    request.update(data)
            except json.JSONDecodeError:
                pass

        results = run_request_blocking(request)
        if os.environ.get("RUNWARE_DEBUG"):
            keys = sorted({k for r in results if isinstance(r, dict) for k in r})
            nsfw = [r.get("NSFWContent") for r in results if isinstance(r, dict)]
            print(f"[Runware] {self.TASK_TYPE} sent safety={request.get('safety')} | "
                  f"result keys={keys} | NSFWContent={nsfw}")
        outputs = self._outputs(results)
        info = _run_info(results)  # cost + NSFW flag, shown on the node
        if info:
            print(f"[Runware] {self.TASK_TYPE}: {info}")
            return {"ui": {"runware_info": [info]}, "result": outputs}
        keys = sorted({k for r in results if isinstance(r, dict) for k in r})
        print(f"[Runware] {self.TASK_TYPE}: no cost/NSFW in response; result keys = {keys}")
        return outputs

    def _outputs(self, results: list[dict[str, Any]]) -> tuple[Any]:
        results = [r for r in results if isinstance(r, dict)]
        kind = _output_kind(self.TASK_TYPE)
        if kind == "image":
            return (urls_to_image([r["imageURL"] for r in results if r.get("imageURL")]),)
        if kind == "text":
            return ("\n".join(r.get("text", "") for r in results if r.get("text")),)
        if kind == "audio" and _HAS_AUDIO:
            for r in results:
                url = _media_url(r)
                if url:
                    return (_audio_output(url),)
        if kind == "video" and _HAS_VIDEO:
            for r in results:
                url = _media_url(r)
                if url:
                    return (_video_output(url),)
        for r in results:  # 3d / vector / other, and audio/video without the native type
            url = _media_url(r)
            if url:
                return (_download(url, _SUFFIX.get(self.TASK_TYPE, ".bin")),)
        return ("",)

    async def _run(self, request: dict[str, Any]) -> list[dict[str, Any]]:  # kept for symmetry
        return await run_request(request)


# ----------------------------------------------------------------------- generic node


class RunwareCustom:
    # Generic escape hatch: any model + taskType, any modality. It makes no assumption about what the
    # model takes or returns; it sends a raw request and hands back the raw response as JSON. Feed
    # media in as UUIDs/URLs in the JSON (see Runware Upload Image), and pull results out of the JSON
    # with Runware Get, then wire those to a loader / Preview / Save node.
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("result_json",)
    FUNCTION = "execute"
    CATEGORY = "Runware/Custom"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "model": ("STRING", {"default": "runware:100@1", "tooltip": "Model AIR"}),
                "taskType": ("STRING", {"default": "imageInference"}),
            },
            "optional": {
                "request_json": ("STRING", {"multiline": True, "default": "{}",
                                            "tooltip": "The full request body as JSON, merged over model/taskType. "
                                                       "Put any media inputs here as UUIDs/URLs (see Runware Upload Image)."}),
            },
        }

    def execute(self, model: str, taskType: str, request_json: str = "{}") -> Any:
        request: dict[str, Any] = {"model": model, "taskType": taskType, "includeCost": True}
        try:
            data = json.loads(request_json or "{}")
            if isinstance(data, dict):
                request.update(data)
        except json.JSONDecodeError:
            pass

        results = run_request_blocking(request)
        results = [r for r in results if isinstance(r, dict)]
        outputs = (json.dumps(results),)
        info = _run_info(results)
        return {"ui": {"runware_info": [info]}, "result": outputs} if info else outputs


# ----------------------------------------------------------- generated param builders


class _RunwareBuilder:
    """Builds one feature (LoRA, ControlNet, PuLID, ...) and outputs its own typed
    value: a list for stackable features (chained), an object for single ones.
    Generated from the feature's schema; wired into the model node's typed socket."""

    SLOT = ""  # the feature's socket name; for arrays, also the chain input
    IS_ARRAY = False
    REQUIRED: list[str] = []  # fields the feature can't be built without
    PARAM_PLAN: dict[str, dict[str, Any]] = {}
    _INPUT_TYPES: dict[str, Any] = {}

    RETURN_TYPES = ("RUNWARE_PARAMS",)
    RETURN_NAMES = ("params",)
    FUNCTION = "build"
    CATEGORY = "Runware/Params"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return cls._INPUT_TYPES

    def build(self, **kwargs: Any) -> tuple[Any]:
        chain = kwargs.pop(self.SLOT, None) if self.IS_ARRAY else None
        advanced = kwargs.pop("advanced_json", "") or ""
        item: dict[str, Any] = {}
        _apply_param_plan(item, kwargs, self.PARAM_PLAN)
        if advanced.strip():
            try:
                data = json.loads(advanced)
                if isinstance(data, dict):
                    item.update(data)
            except json.JSONDecodeError:
                pass
        # An unfilled required field (unconnected image, empty model, ...) would make the
        # API reject the whole request. Drop the incomplete feature instead of sending it.
        complete = all(item.get(f) not in (None, "", [], {}) for f in self.REQUIRED)
        if self.IS_ARRAY:
            items = list(chain) if isinstance(chain, list) else []
            if complete:
                items.append(item)
            return (items or None,)
        return (item if complete else None,)


# ----------------------------------------------------------------------- upload utility


async def run_upload(image_uri: str) -> str:
    from runware import Runware  # noqa: PLC0415

    api_key = resolve_api_key()
    if not api_key:
        raise RuntimeError("No Runware API key. Set RUNWARE_API_KEY or run `runware auth login`.")
    async with Runware(api_key=api_key, transport="rest", user_agent_prefix=USER_AGENT_PREFIX) as client:
        for r in await client.media_storage({"operation": "upload", "media": image_uri}):
            if isinstance(r, dict) and r.get("mediaUUID"):
                return str(r["mediaUUID"])
    return ""


class RunwareUploadImage:
    """Upload an image once -> reusable UUID (for media inputs or the custom node)."""

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_uuid",)
    FUNCTION = "execute"
    CATEGORY = "Runware/Params"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": {"image": ("IMAGE",)}}

    def execute(self, image: Any) -> tuple[str]:
        return (run_blocking(run_upload(tensor_to_data_uris(image)[0])),)


class RunwareLoadImage:
    """Download an image URL (or a Runware result URL) into an IMAGE tensor."""

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "execute"
    CATEGORY = "Runware/Params"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {"required": {"url": ("STRING", {"default": "", "tooltip": "Image URL"})}}

    def execute(self, url: str) -> tuple[Any]:
        url = (url or "").strip()
        return (urls_to_image([url] if url else []),)


def _first_url(data: Any) -> str | None:
    """First URL/data-URI string found anywhere in a decoded response (depth-first)."""
    if isinstance(data, str):
        return data if data.startswith(("http://", "https://", "data:")) else None
    if isinstance(data, dict):
        data = list(data.values())
    if isinstance(data, list):
        for v in data:
            found = _first_url(v)
            if found:
                return found
    return None


def _json_get(data: Any, path: str) -> Any:
    """Walk a dot-path into decoded JSON; numeric segments index into lists. An empty path returns
    the first URL found (the common single-output case)."""
    segs = [p for p in (path or "").split(".") if p]
    if not segs:
        return _first_url(data)
    cur = data
    for seg in segs:
        if isinstance(cur, list):
            try:
                cur = cur[int(seg)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            cur = cur.get(seg)
        else:
            return None
    return cur


class RunwareGet:
    """Pull a field out of a Runware result_json by dot-path, e.g. `0.imageURL`, `0.videoURL`, or
    `0.outputs.files.0.url` (the leading index picks the task in the result list; numeric segments
    index lists). Leave path empty to grab the first URL found. Output is a STRING you feed to a
    loader such as Runware Load Image (URL), or to a Save/Preview node."""

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    FUNCTION = "execute"
    CATEGORY = "Runware/Params"

    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {"result_json": ("STRING", {"forceInput": True})},
            "optional": {
                "path": ("STRING", {"default": "", "tooltip": "Dot-path into the response, e.g. "
                                    "0.imageURL or 0.outputs.files.0.url. Empty = first URL found."}),
            },
        }

    def execute(self, result_json: str, path: str = "") -> tuple[str]:
        try:
            data = json.loads(result_json or "null")
        except json.JSONDecodeError:
            return ("",)
        value = _json_get(data, path)
        if value is None:
            return ("",)
        return (value if isinstance(value, str) else json.dumps(value),)


# ----------------------------------------------------------------------------- factory


_SPECS_PATH = os.path.join(os.path.dirname(__file__), "nodes.json")


_EXTRA_NODES = {
    "RunwareCustom": (RunwareCustom, "Runware (custom)"),
    "RunwareGet": (RunwareGet, "Runware Get"),
    "RunwareUploadImage": (RunwareUploadImage, "Runware Upload Image"),
    "RunwareLoadImage": (RunwareLoadImage, "Runware Load Image (URL)"),
}


def _build() -> tuple[dict[str, Any], dict[str, str]]:
    classes: dict[str, Any] = {k: v[0] for k, v in _EXTRA_NODES.items()}
    names: dict[str, str] = {k: v[1] for k, v in _EXTRA_NODES.items()}

    with open(_SPECS_PATH) as fh:
        data = json.load(fh)

    for spec in data["models"]:
        task_type = spec["task_type"]
        rtypes, rnames = _RET[_output_kind(task_type)]
        key = spec["key"]
        classes[key] = type(key, (_RunwareNode,), {
            "MODEL": spec["model"],
            "TASK_TYPE": task_type,
            "PARAM_PLAN": spec["param_plan"],
            "_INPUT_TYPES": spec["input_types"],
            "_SOCKET_FIELDS": _socket_fields_from_inputs(spec["input_types"]),
            "RETURN_TYPES": rtypes,
            "RETURN_NAMES": rnames,
            "CATEGORY": f"Runware/{_LABEL.get(task_type, 'Other')}/{spec['creator']}",
        })
        names[key] = spec["name"]

    for spec in data.get("architectures", []):
        task_type = spec["task_type"]
        rtypes, rnames = _RET[_output_kind(task_type)]
        key = spec["key"]
        classes[key] = type(key, (_RunwareNode,), {
            "MODEL": spec.get("default_model", ""),  # the model widget overrides this per run
            "TASK_TYPE": task_type,
            "PARAM_PLAN": spec["param_plan"],
            "_INPUT_TYPES": spec["input_types"],
            "_SOCKET_FIELDS": _socket_fields_from_inputs(spec["input_types"]),
            "RETURN_TYPES": rtypes,
            "RETURN_NAMES": rnames,
            "CATEGORY": "Runware/Custom models",
        })
        names[key] = spec["name"]

    for b in data.get("builders", []):
        input_types = b["input_types"]
        slot, typ = b["slot"], b["type"]
        if b["is_array"]:  # stackable features chain through a same-typed input
            input_types.setdefault("optional", {})[slot] = (typ,)
        key = b["key"]
        classes[key] = type(key, (_RunwareBuilder,), {
            "SLOT": slot,
            "IS_ARRAY": b["is_array"],
            "REQUIRED": b.get("required", []),
            "PARAM_PLAN": b["param_plan"],
            "_INPUT_TYPES": input_types,
            "RETURN_TYPES": (typ,),
            "RETURN_NAMES": (slot,),
        })
        names[key] = b["name"]

    # Two different models can share a display name (e.g. Vidu Q1 ships as both a video and an image
    # model). They register fine under distinct keys, but the identical label is confusing on search,
    # so disambiguate a collision by the node's modality: "Vidu Q1 (Video)" / "Vidu Q1 (Image)".
    by_label: dict[str, list[str]] = {}
    for key, label in names.items():
        by_label.setdefault(label, []).append(key)
    for label, keys in by_label.items():
        if len(keys) < 2:
            continue
        for key in keys:
            mod = _LABEL.get(getattr(classes[key], "TASK_TYPE", ""))
            if mod:
                names[key] = f"{label} ({mod})"

    return classes, names


NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS = _build()


# ------------------------------------------------------------- frontend search route


async def search_models(params: dict[str, Any]) -> list[dict[str, str]]:
    """Run a catalog model search, flattened to [{air, name}] for the picker."""
    from runware import Runware  # noqa: PLC0415

    api_key = resolve_api_key()
    if not api_key:
        raise RuntimeError("No Runware API key. Set RUNWARE_API_KEY or run `runware auth login`.")
    async with Runware(api_key=api_key, transport="rest", user_agent_prefix=USER_AGENT_PREFIX) as client:
        results = await client.model_search(params)
    models: list[dict[str, str]] = []
    for r in results:
        if not isinstance(r, dict):
            continue
        for m in r.get("results") or []:
            if isinstance(m, dict):
                air = m.get("air") or m.get("model") or m.get("id")
                if air:
                    models.append({"air": str(air), "name": str(m.get("name") or air)})
    return models


_ROUTES_REGISTERED = False


def _register_routes() -> None:
    """Register the /runware/model_search HTTP route (no-op outside ComfyUI)."""
    global _ROUTES_REGISTERED
    if _ROUTES_REGISTERED:
        return
    try:
        from server import PromptServer  # noqa: PLC0415
        from aiohttp import web  # noqa: PLC0415
    except Exception:  # noqa: BLE001
        return

    @PromptServer.instance.routes.post("/runware/model_search")  # type: ignore[misc]
    async def _model_search_route(request: Any) -> Any:
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            body = {}
        params: dict[str, Any] = {"search": str(body.get("search") or ""), "limit": int(body.get("limit") or 40)}
        for key in ("category", "type", "conditioning", "architecture"):
            if body.get(key):
                params[key] = body[key]
        try:
            models = await search_models(params)
        except Exception as exc:  # noqa: BLE001
            return web.json_response({"error": str(exc)}, status=500)
        return web.json_response({"models": models})

    @PromptServer.instance.routes.post("/runware/set_key")  # type: ignore[misc]
    async def _set_key_route(request: Any) -> Any:
        global _UI_API_KEY
        try:
            body = await request.json()
        except Exception:  # noqa: BLE001
            body = {}
        key = str(body.get("key") or "").strip()
        _UI_API_KEY = key or None
        return web.json_response({"ok": True})

    _ROUTES_REGISTERED = True


_register_routes()
