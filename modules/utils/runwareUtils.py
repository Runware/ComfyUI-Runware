from comfy.model_management import InterruptProcessingException
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta
from server import PromptServer
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import numpy as np
import requests
import hashlib
import asyncio
import random
import base64
import torch
import uuid
import time
import json
import os
import io
import threading
import re

load_dotenv()

BASEFOLDER = Path(__file__).parent.parent.parent
IMAGE_CACHE_FILE = BASEFOLDER / "imagesCache.json"

if not IMAGE_CACHE_FILE.exists():
    with open(IMAGE_CACHE_FILE, "w") as f:
        print("[Runware] Initializing images cache...")
        json.dump({}, f)

RUNWARE_REMBG_OUTPUT_FORMATS = {
    "outputFormat": (
        ["WEBP", "PNG"],
        {"default": "WEBP", "tooltip": "Choose the output image format."},
    )
}

MAX_RETRIES = 4
RETRY_COOLDOWNS = [1, 2, 5, 10]

session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
session.mount("http://", adapter)
session.mount("https://", adapter)

_BASE64_PATTERN = re.compile(r'^(?:data:[^;]+;base64,)?[A-Za-z0-9+/=\s]+$')

def _truncate_base64_string(value: str, preview_length: int = 20) -> str:
    """Return a short preview for base64/data URI strings."""
    if value is None:
        return value

    prefix = ""
    payload = value

    if value.startswith("data:") and "base64," in value:
        prefix, payload = value.split("base64,", 1)
        prefix += "base64,"

    payload = payload.replace("\n", "").replace("\r", "")
    if len(payload) > preview_length:
        return f"{prefix}{payload[:preview_length]}...(truncated)"
    return value

def sanitize_for_logging(data, preview_length: int = 20, max_string_length: int = 2048):
    """
    Sanitize data structures for debug logging by truncating base64 strings.
    """
    if isinstance(data, dict):
        return {key: sanitize_for_logging(value, preview_length, max_string_length) for key, value in data.items()}
    if isinstance(data, list):
        return [sanitize_for_logging(item, preview_length, max_string_length) for item in data]
    if isinstance(data, tuple):
        return tuple(sanitize_for_logging(item, preview_length, max_string_length) for item in data)
    if isinstance(data, str):
        stripped = data.strip()
        if (len(stripped) > preview_length and _BASE64_PATTERN.match(stripped)
                and not stripped.lower().startswith("http")):
            return _truncate_base64_string(stripped, preview_length)
        if len(data) > max_string_length:
            return f"{data[:max_string_length]}...(truncated)"
        return data
    return data

def safe_json_dumps(data, **kwargs) -> str:
    """Dump JSON after sanitizing potential base64 payloads."""
    sanitized = sanitize_for_logging(data)
    return json.dumps(sanitized, **kwargs)

def generalRequestWrapper(recaller, *args, **kwargs):
    for attempt in range(MAX_RETRIES + 1):
        try:
            return recaller(*args, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
            if attempt == MAX_RETRIES:
                raise
            else:
                cooldown = RETRY_COOLDOWNS[attempt]
                print(f"[Runware] Error API Request Failed! Retrying in {cooldown} seconds... (Attempt {attempt+1}/{MAX_RETRIES})")
                time.sleep(cooldown)
            continue
    return False

def getAPIKey():
    apiKey = os.getenv("RUNWARE_API_KEY")
    if apiKey and isinstance(apiKey, str) and len(apiKey) > 24:
        return apiKey
    return False

def getTimeout():
    timeout = os.getenv("RUNWARE_TIMEOUT")
    if timeout and timeout.isdigit():
        return int(timeout)
    else:
        timeout = 180
        os.environ["RUNWARE_TIMEOUT"] = str(timeout)
        return timeout

def getOutputQuality():
    output_quality = os.getenv("RUNWARE_OUTPUT_QUALITY")
    if output_quality and isinstance(output_quality, str) and output_quality.isdigit():
        return int(output_quality)
    else:
        output_quality = 95
        os.environ["RUNWARE_OUTPUT_QUALITY"] = str(output_quality)
        return output_quality

def getOutputFormat():
    output_format = os.getenv("RUNWARE_OUTPUT_FORMAT")
    if output_format and isinstance(output_format, str):
        return output_format
    else:
        output_format = "WEBP"
        os.environ["RUNWARE_OUTPUT_FORMAT"] = output_format
        return output_format

def getEnableImagesCaching():
    enable_images_caching = os.getenv("RUNWARE_ENABLE_IMAGES_CACHING")
    if enable_images_caching and enable_images_caching.lower() in ["true", "false"]:
        return enable_images_caching.lower() == "true"
    else:
        enable_images_caching = True
        os.environ["RUNWARE_ENABLE_IMAGES_CACHING"] = str(enable_images_caching)
        return enable_images_caching

def getMinImageCacheSize():
    min_image_cache_size = os.getenv("RUNWARE_MIN_IMAGE_CACHE_SIZE")
    if min_image_cache_size and min_image_cache_size.isdigit():
        return int(min_image_cache_size)
    else:
        min_image_cache_size = 150
        os.environ["RUNWARE_MIN_IMAGE_CACHE_SIZE"] = str(min_image_cache_size)
        return min_image_cache_size

def getCustomEndpoint():
    custom_endpoint = os.getenv("RUNWARE_CUSTOM_ENDPOINT")
    if custom_endpoint and isinstance(custom_endpoint, str):
        return custom_endpoint
    return "https://api.runware.ai/v1"

SESSION_TIMEOUT = getTimeout()
RUNWARE_API_KEY = getAPIKey()
OUTPUT_FORMAT = getOutputFormat()
OUTPUT_QUALITY = getOutputQuality()
ENABLE_IMAGES_CACHING = getEnableImagesCaching()
MIN_IMAGE_CACHE_SIZE = getMinImageCacheSize()
RUNWARE_API_BASE_URL = getCustomEndpoint()

def setEnvKey(keyName, keyValue):
    comfyNodeRoot = Path(__file__).parent.parent.parent
    envFilePath = comfyNodeRoot / ".env"
    if not envFilePath.exists():
        envFilePath.touch()
    with open(envFilePath, "r") as f:
        lines = f.readlines()
    key_exists = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{keyName}="):
            key_exists = True
            new_lines.append(f"{keyName}={keyValue}\n")
        else:
            new_lines.append(line)
    if not key_exists:
        new_lines.append(f"{keyName}={keyValue}\n")
    with open(envFilePath, "w") as f:
        f.writelines(new_lines)
    return True

def setAPIKey(apiKey: str):
    global RUNWARE_API_KEY
    envSetRes = setEnvKey("RUNWARE_API_KEY", apiKey)
    if envSetRes:
        RUNWARE_API_KEY = apiKey
        os.environ["RUNWARE_API_KEY"] = apiKey
        return True

def setTimeout(timeout: int):
    envSetRes = setEnvKey("RUNWARE_TIMEOUT", str(timeout))
    if envSetRes:
        global SESSION_TIMEOUT
        SESSION_TIMEOUT = timeout
        os.environ["RUNWARE_TIMEOUT"] = str(timeout)
        return True

def setOutputFormat(format: str):
    envSetRes = setEnvKey("RUNWARE_OUTPUT_FORMAT", format)
    if envSetRes:
        global OUTPUT_FORMAT
        OUTPUT_FORMAT = format
        os.environ["RUNWARE_OUTPUT_FORMAT"] = format
        return True

def setOutputQuality(quality: int):
    envSetRes = setEnvKey("RUNWARE_OUTPUT_QUALITY", str(quality))
    if envSetRes:
        global OUTPUT_QUALITY
        OUTPUT_QUALITY = quality
        os.environ["RUNWARE_OUTPUT_QUALITY"] = str(quality)
        return True

def setEnableImagesCaching(enabled: bool):
    envSetRes = setEnvKey("RUNWARE_ENABLE_IMAGES_CACHING", str(enabled))
    if envSetRes:
        global ENABLE_IMAGES_CACHING
        ENABLE_IMAGES_CACHING = enabled
        os.environ["RUNWARE_ENABLE_IMAGES_CACHING"] = str(enabled)
        return True

def setMinImageCacheSize(size: int):
    envSetRes = setEnvKey("RUNWARE_MIN_IMAGE_CACHE_SIZE", str(size))
    if envSetRes:
        global MIN_IMAGE_CACHE_SIZE
        MIN_IMAGE_CACHE_SIZE = size
        os.environ["RUNWARE_MIN_IMAGE_CACHE_SIZE"] = str(size)
        return True

def genRandSeed(minSeed=1, maxSeed=4294967295):
    """Generate a random seed value (32-bit unsigned integer range for compatibility)"""
    return random.randint(minSeed, maxSeed)

def genRandUUID():
    return str(uuid.uuid4())

def getOrdinal(num):
    """Get ordinal string for number (e.g., 1 -> 'first', 2 -> 'second')"""
    ordinals = {1: "first", 2: "second", 3: "third", 4: "fourth"}
    return ordinals.get(num, f"{num}th")

def checkAPIKey(apiKey):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }

    genConfig = [
        {
            "taskType": "authentication",
            "apiKey": apiKey,
        }
    ]

    try:

        def recaller():
            return session.post(
                RUNWARE_API_BASE_URL,
                headers=headers,
                json=genConfig,
                timeout=10,
                allow_redirects=False,
                stream=True,
            )

        genResult = generalRequestWrapper(recaller)
        genResult = genResult.json()
        if "errors" in genResult:
            return str(genResult["errors"][0]["message"])
        else:
            return True
    except Exception as e:
        return False

def sendMediaUUID(mediaUUID, nodeID):
    PromptServer.instance.send_sync(
        "runwareMediaUUID",
        {
            "success": True,
            "mediaUUID": mediaUUID,
            "nodeID": nodeID,
            "widgetName": "mediaUUID",  # Target the mediaUUID widget
        },
    )

def sendImageCaption(captionText, nodeID):
    PromptServer.instance.send_sync(
        "runwareImageCaption",
        {
            "success": True,
            "captionText": captionText,
            "nodeID": nodeID,
            "widgetName": "imageCaption",  # Target the new imageCaption widget
        },
    )

def sendVideoTranscription(transcriptionText, nodeID):
    PromptServer.instance.send_sync(
        "runwareVideoTranscription",
        {
            "success": True,
            "transcriptionText": transcriptionText,
            "nodeID": nodeID,
            "widgetName": "prompt",  # Target the prompt widget (matching imageCaptioning pattern)
        },
    )

def inferenecRequest(genConfig):
    global RUNWARE_API_KEY, RUNWARE_API_BASE_URL, SESSION_TIMEOUT
    RUNWARE_API_KEY = os.getenv("RUNWARE_API_KEY")
    SESSION_TIMEOUT = int(os.getenv("RUNWARE_TIMEOUT"))
    headers = {
        "Authorization": f"Bearer {RUNWARE_API_KEY}",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }

    try:
        def recaller():
            return session.post(
                RUNWARE_API_BASE_URL,
                headers=headers,
                json=genConfig,
                timeout=SESSION_TIMEOUT,
                allow_redirects=False,
                stream=True,
            )

        genResult = generalRequestWrapper(recaller)
        try:
            genResult = genResult.json()
        except json.JSONDecodeError as e:
            print(f"[Debugging] Runware JSON Decode Error: {str(e)}")
            print(f"[Debugging] Runware Response Status Code: {genResult.status_code}")
            print(f"[Debugging] Runware Response Headers: {genResult.headers}")
            print(f"[Debugging] Runware Raw Response Content: {genResult.content}")
            raise Exception("Error: Invalid JSON response from API!")
        if "errors" in genResult:
            print(f"[DEBUG] API Error Response: {safe_json_dumps(genResult, indent=2) if isinstance(genResult, dict) else genResult}")
            raise Exception(genResult["errors"][0]["message"])
        else:
            return genResult
    except requests.exceptions.Timeout:
        raise Exception(
            f"Error: Request Timed Out After {SESSION_TIMEOUT} Seconds - Please Try Again!"
        )
    except requests.exceptions.RequestException:
        raise Exception("Error: Runware Request Failed!")
    except Exception as e:
        if "invalid api key" in str(e).lower():
            PromptServer.instance.send_sync(
                "runwareError",
                {
                    "success": False,
                    "errorMessage": str(e),
                    "errorCode": 401,
                },
            )
            raise InterruptProcessingException()
        else:
            raise Exception(f"Error: {e}")
    return False


async def uploadImage(imageDataUri):
    uploadTaskConfig = [
        {"taskType": "imageUpload", "taskUUID": genRandUUID(), "image": imageDataUri}
    ]

    try:
        uploadResult = inferenecRequest(uploadTaskConfig)
        if (
            uploadResult
            and "data" in uploadResult
            and "imageUUID" in uploadResult["data"][0]
        ):
            imageUUID = uploadResult["data"][0]["imageUUID"]
            return imageUUID
    except Exception as e:
        return False

    return False

async def uploadAndCacheImage(imgSig: str, imgDataUri: str):
    try:
        imageUUID = await uploadImage(imgDataUri)
        if imageUUID:
            await imageStoreSet(imgSig, imageUUID)
    except Exception as e:
        return False

async def imageStoreSet(imgHash: str, imgUUID: str) -> bool:
    try:
        with open(IMAGE_CACHE_FILE, "r") as f:
            cache = json.load(f)
        expires = (datetime.now() + timedelta(days=30)).isoformat()
        cache[imgHash] = {"uuid": imgUUID, "expires": expires}
        with open(IMAGE_CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
        return True
    except Exception as e:
        return False

def imageStoreGet(imgHash: str) -> str | bool:
    try:
        with open(IMAGE_CACHE_FILE, "r") as f:
            cache = json.load(f)
        if imgHash not in cache:
            return False
        entry = cache[imgHash]
        expires = datetime.fromisoformat(entry["expires"])
        if datetime.now() > expires:
            del cache[imgHash]
            with open(IMAGE_CACHE_FILE, "w") as f:
                json.dump(cache, f, indent=2)
            return False
        return entry["uuid"]
    except Exception as e:
        return False

def convertTensor2IMG(tensorImage):
    global ENABLE_IMAGES_CACHING, MIN_IMAGE_CACHE_SIZE
    ENABLE_IMAGES_CACHING = getEnableImagesCaching()
    MIN_IMAGE_CACHE_SIZE = int(os.getenv("RUNWARE_MIN_IMAGE_CACHE_SIZE"))

    imageNP = (tensorImage.squeeze().numpy() * 255).astype(np.uint8)
    imgSig = hashlib.sha256(imageNP.tobytes()).hexdigest()

    if ENABLE_IMAGES_CACHING:
        imgUUID = imageStoreGet(imgSig)
        if imgUUID:
            return imgUUID

    image = Image.fromarray(imageNP)
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        imageRawData = buffer.getvalue()
        imgBytes = len(imageRawData)
        imgSize = int(imgBytes / 1024)
        imgb64 = base64.b64encode(imageRawData).decode("utf-8")
        imgDataUri = f"data:image/png;base64,{imgb64}"

        if ENABLE_IMAGES_CACHING and imgSize >= MIN_IMAGE_CACHE_SIZE:
            try:
                loop = asyncio.get_running_loop()
                loop.call_soon(lambda: asyncio.ensure_future(uploadAndCacheImage(imgSig, imgDataUri)))
            except RuntimeError:
                def run_coro():
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    new_loop.run_until_complete(uploadAndCacheImage(imgSig, imgDataUri))
                    new_loop.close()
                threading.Thread(target=run_coro).start()
        return imgDataUri



def convertTensor2IMGForVideo(tensorImage):
    """Convert tensor to image and force upload to get UUID for video frame images"""
    imageNP = (tensorImage.squeeze().numpy() * 255).astype(np.uint8)
    imgSig = hashlib.sha256(imageNP.tobytes()).hexdigest()

    # Check if already cached
    imgUUID = imageStoreGet(imgSig)
    if imgUUID:
        return imgUUID

    # Convert to data URI - use PNG for video frame images
    image = Image.fromarray(imageNP)
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        imageRawData = buffer.getvalue()
        imgb64 = base64.b64encode(imageRawData).decode("utf-8")
        imgDataUri = f"data:image/png;base64,{imgb64}"

    # Force upload to get UUID - use synchronous approach to avoid event loop conflicts
    try:
        # Use synchronous upload instead of async
        uploadTaskConfig = [
            {"taskType": "imageUpload", "taskUUID": genRandUUID(), "image": imgDataUri}
        ]
        
        uploadResult = inferenecRequest(uploadTaskConfig)
        if (
            uploadResult
            and "data" in uploadResult
            and "imageUUID" in uploadResult["data"][0]
        ):
            uploaded_uuid = uploadResult["data"][0]["imageUUID"]
            
            # Cache the UUID synchronously
            try:
                with open(IMAGE_CACHE_FILE, "r") as f:
                    cache = json.load(f)
                expires = (datetime.now() + timedelta(days=30)).isoformat()
                cache[imgSig] = {"uuid": uploaded_uuid, "expires": expires}
                with open(IMAGE_CACHE_FILE, "w") as f:
                    json.dump(cache, f, indent=2)
            except Exception as e:
                print(f"[Warning] Error caching image: {e}")
            
            return uploaded_uuid
        else:
            print("[Warning] Failed to upload image, returning data URI")
            return imgDataUri
    except Exception as e:
        print(f"[Warning] Error uploading image: {e}")
        return imgDataUri

def convertIMG2Tensor(b64img):
    imgbytes = base64.b64decode(b64img)
    image = Image.open(io.BytesIO(imgbytes))
    imageNP = np.array(image).astype(np.float32) / 255.0
    tensorImage = torch.from_numpy(imageNP).squeeze()
    return tensorImage

def convertImageB64List(imageDataObject):
    images = ()
    for result in imageDataObject["data"]:
        generatedImage = result.get(
            "imageBase64Data",
            result.get(
                "maskImageBase64Data", result.get("guideImageBase64Data", False)
            ),
        )
        generatedImage = convertIMG2Tensor(generatedImage)
        images += (generatedImage,)
    images = torch.stack(images, dim=0)
    return images

class VideoObject:
    def __init__(self, video_url, width=None, height=None):
        self.video_url = video_url
        # Use provided dimensions or default to 864x480 for Seedance Lite
        self.width = width if width is not None else 864
        self.height = height if height is not None else 480
    
    def get_dimensions(self):
        return (self.width, self.height)
    
    def save_to(self, filename, **kwargs):
        """Save video to file by downloading from URL with retry logic"""
        max_retries = 10
        retry_delays = [2, 5, 10, 15, 20]  # Longer delays for retries with larger videos
        
        for attempt in range(max_retries):
            try:
                response = requests.get(self.video_url, stream=True, timeout=30)
                print(f"[Video Download] Attempt {attempt + 1}: {response}")
               
                if response.status_code == 422:
                    print(f"[Video Download] Server still processing, waiting...")
                    time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue
                    
                if response.status_code == 502:
                    print(f"[Video Download] Server error (502), retrying in {retry_delays[min(attempt, len(retry_delays) - 1)]} seconds...")
                    time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue
                
                response.raise_for_status()
                
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"[Video Download] Successfully downloaded video to {filename}")
                return True
                
            except requests.exceptions.RequestException as e:
                print(f"[Video Download] Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[min(attempt, len(retry_delays) - 1)])
                    continue
                else:
                    print(f"[Video Download] All {max_retries} attempts failed. Video URL: {self.video_url}")
                    return False
            except Exception as e:
                print(f"[Video Download] Unexpected error: {e}")
                return False

        return False
    
    def __str__(self):
        return f"VideoObject(url={self.video_url}, dimensions={self.width}x{self.height})"

def convertVideoB64List(videoDataObject, width=None, height=None):
    videos = ()
    for result in videoDataObject["data"]:
        generatedVideo = result.get("videoBase64Data", False)
        if generatedVideo:
            # For base64 data, create a video object (would need proper decoding in full implementation)
            video_obj = VideoObject(f"data:video/mp4;base64,{generatedVideo}", width, height)
            videos += (video_obj,)
        else:
            # If no base64 data, try to get video URL
            videoURL = result.get("videoURL", False)
            if videoURL:
                # Create a proper video object that ComfyUI can handle
                video_obj = VideoObject(videoURL, width, height)
                videos += (video_obj,)
    return videos

def pollVideoResult(taskUUID):
    """Poll for video generation result using task UUID with getResponse"""
    global RUNWARE_API_KEY, RUNWARE_API_BASE_URL, SESSION_TIMEOUT
    
    pollConfig = [
        {
            "taskType": "getResponse",
            "taskUUID": taskUUID,
        }
    ]
    
    headers = {
        "Authorization": f"Bearer {RUNWARE_API_KEY}",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }
    
    try:
        def recaller():
            return session.post(
                RUNWARE_API_BASE_URL,
                headers=headers,
                json=pollConfig,
                timeout=30,  # Shorter timeout for polling
                allow_redirects=False,
                stream=True,
            )
        
        pollResult = generalRequestWrapper(recaller)
        try:
            pollResult = pollResult.json()
        except json.JSONDecodeError as e:
            print(f"[Debugging] Runware Poll JSON Decode Error: {str(e)}")
            return None
            
        if "errors" in pollResult:
            print(f"[Debugging] Poll error: {safe_json_dumps(pollResult, indent=2) if isinstance(pollResult, (dict, list)) else pollResult}")
            return pollResult
        else:
            return pollResult
    except Exception as e:
        print(f"[Debugging] Poll request failed: {str(e)}")
        return None
