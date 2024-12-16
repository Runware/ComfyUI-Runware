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
        "limit": 15,
        "sort": "-downloadCount",
    }]

    if(modelCategory != "controlnet" and modelCategory != "lora"):
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
    modelList = utilityResults["data"][0]["results"]
    return web.json_response({'success': True, 'modelList': modelList})