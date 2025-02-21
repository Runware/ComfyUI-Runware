from comfy.model_management import InterruptProcessingException
from requests.adapters import HTTPAdapter
from server import PromptServer
from dotenv import load_dotenv
from pathlib import Path
from PIL import Image
import numpy as np
import requests
import random
import base64
import torch
import uuid
import os
import io

load_dotenv()

RUNWARE_REMBG_OUTPUT_FORMATS = {
    "outputFormat": (["WEBP", "PNG"], {
        "default": "WEBP", 
        "tooltip": "Choose the output image format."
    })
}

RUNWARE_API_BASE_URL = "https://api.runware.ai/v1"
session = requests.Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10)
session.mount("http://", adapter)
session.mount("https://", adapter)

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

SESSION_TIMEOUT = getTimeout()
RUNWARE_API_KEY = getAPIKey()
OUTPUT_FORMAT = getOutputFormat()
OUTPUT_QUALITY = getOutputQuality()

def setEnvKey(keyName, keyValue):
    comfyNodeRoot = Path(__file__).parent.parent.parent
    envFilePath = comfyNodeRoot / '.env'
    if not envFilePath.exists():
        envFilePath.touch()
    with open(envFilePath, 'r') as f:
        lines = f.readlines()
    key_exists = False
    new_lines = []
    for line in lines:
        if line.startswith(f'{keyName}='):
            key_exists = True
            new_lines.append(f'{keyName}={keyValue}\n')
        else:
            new_lines.append(line)
    if not key_exists:
        new_lines.append(f'{keyName}={keyValue}\n')
    with open(envFilePath, 'w') as f:
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

def genRandSeed(minSeed = 1000, maxSeed = 9223372036854776000):
    return random.randint(minSeed, maxSeed)

def genRandUUID():
    return str(uuid.uuid4())

def checkAPIKey(apiKey):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Accept-Encoding": "gzip, deflate, br, zstd",
    }

    genConfig = [{
            "taskType": "authentication",
            "apiKey": apiKey,
    }]

    try:
        genResult = session.post(RUNWARE_API_BASE_URL, headers=headers, json=genConfig, timeout=10, allow_redirects=False, stream=True)
        genResult = genResult.json()
        if("errors" in genResult):
            return str(genResult["errors"][0]["message"])
        else:
            return True
    except Exception as e:
        return False

def sendImageCaption(captionText, nodeID):
    PromptServer.instance.send_sync("runwareImageCaption", {
        "success": True,
        "captionText": captionText,
        "nodeID": nodeID,
})

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
        genResult = session.post(RUNWARE_API_BASE_URL, headers=headers, json=genConfig, timeout=SESSION_TIMEOUT, allow_redirects=False, stream=True)
        genResult = genResult.json()
        if("errors" in genResult):
            raise Exception(genResult["errors"][0]["message"])
        else:
            return genResult
    except requests.exceptions.Timeout:
        raise Exception(f"Error: Request Timed Out After {SESSION_TIMEOUT} Seconds - Please Try Again!")
    except requests.exceptions.RequestException:
        raise Exception("Error: Runware Request Failed!")
    except Exception as e:
        if "invalid api key" in str(e).lower():
            PromptServer.instance.send_sync("runwareError", {
                "success": False,
                "errorMessage": str(e),
                "errorCode": 401,
            })
            raise InterruptProcessingException()
        else:
            raise Exception(f"Error: {e}")
    return False

def convertTensor2IMG(tensorImage):
    imageNP = (tensorImage.squeeze().numpy() * 255).astype(np.uint8)
    image = Image.fromarray(imageNP)
    with io.BytesIO() as buffer:
        image.save(buffer, format="webp")
        imgb64 =  base64.b64encode(buffer.getvalue()).decode('utf-8')
    imgDataURI = f'data:image/webp;base64,{imgb64}'
    return imgDataURI

def convertIMG2Tensor(b64img):
    imgbytes = base64.b64decode(b64img)
    image = Image.open(io.BytesIO(imgbytes))
    imageNP = np.array(image).astype(np.float32) / 255.0
    tensorImage = torch.from_numpy(imageNP).squeeze()
    return tensorImage

def convertImageB64List(imageDataObject):
    images = ()
    for result in imageDataObject["data"]:
        generatedImage = result.get("imageBase64Data", result.get("maskImageBase64Data", result.get("guideImageBase64Data", False)))
        generatedImage = convertIMG2Tensor(generatedImage)
        images += (generatedImage,)
    images = torch.stack(images, dim=0)
    return (images,)