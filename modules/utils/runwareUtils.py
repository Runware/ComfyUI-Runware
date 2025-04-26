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
        timeout = 90
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

def genRandSeed(minSeed=1000, maxSeed=9223372036854776000):
    return random.randint(minSeed, maxSeed)

def genRandUUID():
    return str(uuid.uuid4())

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

def sendImageCaption(captionText, nodeID):
    PromptServer.instance.send_sync(
        "runwareImageCaption",
        {
            "success": True,
            "captionText": captionText,
            "nodeID": nodeID,
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
        image.save(
            buffer, format="webp", quality=100, subsampling=0, method=6, exact=True
        )
        imageRawData = buffer.getvalue()
        imgBytes = len(imageRawData)
        imgSize = int(imgBytes / 1024)
        imgb64 = base64.b64encode(imageRawData).decode("utf-8")
        imgDataUri = f"data:image/webp;base64,{imgb64}"

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
