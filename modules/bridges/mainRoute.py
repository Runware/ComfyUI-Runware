from ..utils import runwareUtils as rwUtils
from server import PromptServer
from aiohttp import web

routes = PromptServer.instance.routes

@routes.post('/setAPIKey')
async def setAPIKey(reqPayload):
    reqData = await reqPayload.json()
    apiKey = reqData.get('apiKey', None)
    if(apiKey is None or apiKey == "" or len(apiKey) < 30):
        return web.json_response({'success': False, 'error': 'Invalid API Key!'})
    try:
        apiKey = apiKey.strip()
        apiCheckResult = rwUtils.checkAPIKey(apiKey)
        if(apiCheckResult == False):
            return web.json_response({'success': False, 'error': 'Failed To Set Your API Key, Please Try Again!'})
        elif(apiCheckResult != True):
            return web.json_response({'success': False, 'error': apiCheckResult})
        rwUtils.setAPIKey(apiKey)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    return web.json_response({'success': True})

@routes.post('/setMaxTimeout')
async def setMaxTimeout(reqPayload):
    reqData = await reqPayload.json()
    maxTimeout = reqData.get('maxTimeout', 90)
    if(maxTimeout < 5 or maxTimeout > 99):
        return web.json_response({'success': False, 'error': 'Invalid Timeout Value!'})
    try:
        rwUtils.setTimeout(maxTimeout)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    return web.json_response({'success': True})

@routes.post('/setOutputFormat')
async def setOutputFormat(reqPayload):
    reqData = await reqPayload.json()
    outputFormat = reqData.get('outputFormat', 'WEBP')
    if outputFormat not in ['WEBP', 'PNG', 'JPEG']:
        return web.json_response({'success': False, 'error': 'Invalid Output Format!'})
    try:
        rwUtils.setOutputFormat(outputFormat)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    return web.json_response({'success': True})

@routes.post('/setOutputQuality')
async def setOutputQuality(reqPayload):
    reqData = await reqPayload.json()
    outputQuality = reqData.get('outputQuality', 95)
    if not isinstance(outputQuality, int) or outputQuality < 20 or outputQuality > 99:
        return web.json_response({'success': False, 'error': 'Invalid Output Quality!'})
    try:
        rwUtils.setOutputQuality(outputQuality)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    return web.json_response({'success': True})

@routes.post('/promptEnhance')
async def promptEnhance(reqPayload):
    reqData = await reqPayload.json()
    userPrompt = reqData.get('userPrompt')
    utilityConfig = [{
        "taskType": "promptEnhance",
        "taskUUID": rwUtils.genRandUUID(),
        "prompt": userPrompt,
        "promptMaxLength": 300,
        "promptVersions": 1,
    }]

    try:
        utilityResults = rwUtils.inferenecRequest(utilityConfig)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    enhancedPrompt = utilityResults["data"][0]["text"]
    return web.json_response({'success': True, 'enhancedPrompt': enhancedPrompt})

@routes.post('/modelSearch')
async def modelSearch(reqPayload):
    reqData = await reqPayload.json()
    modelQuery = reqData.get('modelQuery', "")
    modelArch = reqData.get('modelArch', "all")
    modelCategory = reqData.get('modelCat', "checkpoint")
    modelType = reqData.get('modelType', "base")
    controlNetConditioning = reqData.get('condtioning', "all")

    utilityConfig = [{
        "taskType": "modelSearch",
        "taskUUID": rwUtils.genRandUUID(),
        "category": modelCategory,
        "limit": 25,
        "sort": "-downloadCount",
    }]

    aclTypes = ["controlnet", "lora", "lycoris", "embeddings", "vae"]

    if(modelCategory not in aclTypes):
        utilityConfig[0]["type"] = modelType
    elif(modelCategory == "controlnet" and controlNetConditioning != "all"):
        utilityConfig[0]["conditioning"] = controlNetConditioning
    if(modelArch != "all"):
        utilityConfig[0]["architecture"] = modelArch
    if(modelQuery != ""):
        utilityConfig[0]["search"] = modelQuery

    try:
        utilityResults = rwUtils.inferenecRequest(utilityConfig)
    except Exception as e:
        return web.json_response({'success': False, 'error': str(e)})
    totalResults = utilityResults["data"][0]["totalResults"]
    if(totalResults < 1):
        return web.json_response({'success': False, 'error': 'No Results Found!'})
    results = utilityResults["data"][0].get("results", [])
    if not results:
        return web.json_response({'success': False, 'error': 'No Results Found!'})
    modelList = results
    return web.json_response({'success': True, 'modelList': modelList})