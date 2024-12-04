from requests.adapters import HTTPAdapter
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

SESSION_TIMEOUT = 60
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

RUNWARE_API_KEY = getAPIKey()

def setAPIKey(apiKey: str):
    global RUNWARE_API_KEY
    comfyNodeRoot = Path(__file__).parent.parent.parent
    envFilePath = comfyNodeRoot / '.env'
    if not envFilePath.exists():
        envFilePath.touch()
    with open(envFilePath, 'r') as f:
        lines = f.readlines()
    key_exists = False
    new_lines = []
    for line in lines:
        if line.startswith('RUNWARE_API_KEY='):
            key_exists = True
            new_lines.append(f'RUNWARE_API_KEY={apiKey}\n')
        else:
            new_lines.append(line)
    if not key_exists:
        new_lines.append(f'RUNWARE_API_KEY={apiKey}\n')
    with open(envFilePath, 'w') as f:
        f.writelines(new_lines)
    RUNWARE_API_KEY = apiKey
    os.environ["RUNWARE_API_KEY"] = apiKey
    return True

def genRandSeed(minSeed = 1000, maxSeed = 9223372036854776000):
    return random.randint(minSeed, maxSeed)

def genRandUUID():
    return str(uuid.uuid4())

def inferenecRequest(genConfig):
    global RUNWARE_API_KEY
    RUNWARE_API_KEY = os.getenv("RUNWARE_API_KEY")
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
            raise Exception("Invalid API Key - Please Make Sure you set your correctly API Key Either in the env file or through the API Manager Node!\n\nIf you don't have an API Key, you can get it from: https://my.runware.ai/keys")
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