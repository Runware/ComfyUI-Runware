import base64
import os
import time
import requests
import torch
import soundfile as sf
import numpy as np
from io import BytesIO
from .utils.runwareUtils import (
    RUNWARE_API_KEY,
    RUNWARE_API_BASE_URL,
    generalRequestWrapper,
    genRandUUID,
    sanitize_for_logging,
    safe_json_dumps,
    sendMediaUUID,
)


class RunwareMediaUpload:
    """Runware Media Upload node for uploading audio/video to Runware storage"""
    
    # MIME type mapping for video files
    VIDEO_MIME_TYPES = {
        '.mp4': 'video/mp4',
        '.avi': 'video/avi',
        '.mov': 'video/quicktime',
        '.webm': 'video/webm',
    }
    
    DEFAULT_SAMPLE_RATE = 22050
    DEFAULT_VIDEO_MIME = 'video/mp4'
    MAX_POLL_ATTEMPTS = 100
    POLL_INTERVAL = 2
    REQUEST_TIMEOUT = 30

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "media": ("VIDEO,AUDIO", {
                    "tooltip": "Media tensor from ComfyUI load video or audio node",
                }),
                "mediaUUID": ("STRING", {
                    "placeholder": "Generated media UUID will appear here automatically.",
                    "tooltip": "This field will be automatically populated with the generated media UUID after upload.",
                }),
            },
            "hidden": {"node_id": "UNIQUE_ID"}
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mediaUUID",)
    FUNCTION = "uploadMedia"
    CATEGORY = "Runware"
    DESCRIPTION = "Upload audio media to Runware's media storage and get mediaUUID"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NAN")

    def uploadMedia(self, media=None, mediaUuid=None, **kwargs):
        """Main function to upload media and return mediaUUID"""
        if media is None:
            raise ValueError("Media input is required")
        
        print(f"[Debug] uploadMedia called with media: {type(media)}, mediaUuid: {mediaUuid}")
        
        try:
            mediaBase64 = self._convertMediaToBase64(media)
            print(f"[Debug] Media converted to base64, length: {len(mediaBase64)}")
            
            mediaUuid = self._uploadToRunware(mediaBase64)
            print(f"[Debug] Upload completed! MediaUUID: {mediaUuid}")
            print(f"[Debug] ===== RESULT: {mediaUuid} =====")
            
            sendMediaUUID(mediaUuid, kwargs.get("node_id"))
            return (mediaUuid,)
        except Exception as e:
            print(f"[Debug] Media upload failed: {str(e)}")
            raise e

    def _convertMediaToBase64(self, mediaTensor):
        """Convert media tensor to base64 data URI"""
        print(f"[Debug] Media type: {type(mediaTensor)}")
        
        if self._isVideoFile(mediaTensor):
            return self._convertVideoToBase64(mediaTensor)
        elif isinstance(mediaTensor, dict) and 'waveform' in mediaTensor:
            return self._convertAudioDictToBase64(mediaTensor)
        elif isinstance(mediaTensor, torch.Tensor):
            return self._convertTensorToBase64(mediaTensor)
        else:
            raise ValueError(f"Unsupported media type: {type(mediaTensor)}")

    def _isVideoFile(self, mediaTensor):
        """Check if media tensor is a VideoFromFile object"""
        return (hasattr(mediaTensor, 'video_path') or 
                str(type(mediaTensor)).find('VideoFromFile') != -1)

    def _convertVideoToBase64(self, videoTensor):
        """Convert video file to base64 data URI"""
        print(f"[Debug] VideoFromFile object detected")
        
        videoFile = self._getVideoFilePath(videoTensor)
        videoPath = self._extractVideoPath(videoFile)
        
        print(f"[Debug] Processing video file: {videoPath}")
        
        with open(videoPath, 'rb') as f:
            videoBytes = f.read()
        
        mimeType = self._getMimeType(videoPath)
        videoBase64 = base64.b64encode(videoBytes).decode('utf-8')
        
        return f"data:{mimeType};base64,{videoBase64}"

    def _getVideoFilePath(self, videoTensor):
        """Extract video file path from VideoFromFile object"""
        videoFile = getattr(videoTensor, '_VideoFromFile__file', None)
        
        if videoFile is None:
            for attr in ['video_path', 'path', 'file_path', 'filename', '_file']:
                if hasattr(videoTensor, attr):
                    videoFile = getattr(videoTensor, attr)
                    print(f"[Debug] Found video file via {attr}: {videoFile}")
                    break
        
        if videoFile is None:
            raise ValueError("Could not find video file in VideoFromFile object")
        
        return videoFile

    def _extractVideoPath(self, videoFile):
        """Extract file path from file object or string"""
        if hasattr(videoFile, 'name'):
            return videoFile.name
        elif isinstance(videoFile, str):
            return videoFile
        else:
            raise ValueError(f"Unexpected video file type: {type(videoFile)}")

    def _getMimeType(self, filePath):
        """Get MIME type based on file extension"""
        ext = os.path.splitext(filePath.lower())[1]
        return self.VIDEO_MIME_TYPES.get(ext, self.DEFAULT_VIDEO_MIME)

    def _convertAudioDictToBase64(self, audioDict):
        """Convert audio dictionary to base64 WAV data URI"""
        waveform = audioDict['waveform']
        sampleRate = audioDict.get('sample_rate', self.DEFAULT_SAMPLE_RATE)
        
        waveformNp = self._prepareWaveformNumpy(waveform)
        wavBytes = self._convertWaveformToWav(waveformNp, sampleRate)
        wavBase64 = base64.b64encode(wavBytes).decode('utf-8')
        
        return f"data:audio/wav;base64,{wavBase64}"

    def _convertTensorToBase64(self, mediaTensor):
        """Convert direct tensor input to base64 WAV data URI"""
        waveformNp = self._prepareWaveformNumpy(mediaTensor)
        wavBytes = self._convertWaveformToWav(waveformNp, self.DEFAULT_SAMPLE_RATE)
        wavBase64 = base64.b64encode(wavBytes).decode('utf-8')
        
        return f"data:audio/wav;base64,{wavBase64}"

    def _prepareWaveformNumpy(self, waveform):
        """Prepare waveform tensor/array for soundfile (returns [channels, samples])"""
        if isinstance(waveform, torch.Tensor):
            # Normalize dimensions: [batch, channels, samples] -> [channels, samples]
            if waveform.dim() == 3:
                waveform = waveform.squeeze(0)
            elif waveform.dim() == 1:
                waveform = waveform.unsqueeze(0)
            waveformNp = waveform.cpu().numpy()
        else:
            waveformNp = np.array(waveform)
            if waveformNp.ndim == 1:
                waveformNp = waveformNp.reshape(1, -1)
        
        return waveformNp

    def _convertWaveformToWav(self, waveformNp, sampleRate):
        """Convert numpy waveform to WAV bytes using soundfile"""
        # soundfile expects [samples, channels]
        waveformNp = waveformNp.T
        
        buffer = BytesIO()
        sf.write(buffer, waveformNp, sampleRate, format='WAV')
        buffer.seek(0)
        
        return buffer.getvalue()

    def _uploadToRunware(self, mediaDataUri):
        """Upload media to Runware and return mediaUUID"""
        taskUuid = genRandUUID()
        print(f"[Debug] Generated task UUID: {taskUuid}")
        
        mediaData = self._stripDataUriPrefix(mediaDataUri)
        uploadConfig = self._buildUploadConfig(taskUuid, mediaData)
        
        print(f"[Debug] Upload config: {sanitize_for_logging(uploadConfig[0])}")
        print(f"[Debug] API URL: {RUNWARE_API_BASE_URL}")
        
        uploadResult = self._makeUploadRequest(uploadConfig)
        self._validateUploadResponse(uploadResult)
        
        uploadData = uploadResult.get("data", [])
        if uploadData and len(uploadData) > 0:
            mediaUuid = uploadData[0].get("mediaUUID", "")
            if mediaUuid and mediaUuid != "1":
                print(f"[Debug] Got immediate mediaUUID: {mediaUuid}")
                return mediaUuid
        
        print(f"[Debug] Starting polling for result...")
        return self._pollForResult(taskUuid)

    def _stripDataUriPrefix(self, mediaDataUri):
        """Strip data URI prefix if present"""
        if mediaDataUri.startswith("data:"):
            mediaData = mediaDataUri.split(",", 1)[1]
            print(f"[Debug] Stripped data URI prefix, media data length: {len(mediaData)}")
            return mediaData
        return mediaDataUri

    def _buildUploadConfig(self, taskUuid, mediaData):
        """Build upload configuration for API request"""
        return [{
            "taskType": "mediaStorage",
            "taskUUID": taskUuid,
            "operation": "upload",
            "media": mediaData,
        }]

    def _getApiHeaders(self):
        """Get API request headers"""
        return {
            "Authorization": f"Bearer {RUNWARE_API_KEY}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }

    def _makeUploadRequest(self, uploadConfig):
        """Make upload request to Runware API"""
        def recaller():
            print(f"[Debug] Making POST request to Runware API...")
            return requests.post(
                RUNWARE_API_BASE_URL,
                headers=self._getApiHeaders(),
                json=uploadConfig,
                timeout=self.REQUEST_TIMEOUT,
                allow_redirects=False,
                stream=True,
            )
        
        response = generalRequestWrapper(recaller)
        return self._parseJsonResponse(response)

    def _parseJsonResponse(self, response):
        """Parse JSON response from API"""
        if response.status_code != 200:
            errorText = response.text[:500]
            print(f"[Debug] Request failed with status {response.status_code}")
            print(f"[Debug] Response text: {errorText}")
            raise Exception(f"Request failed with status {response.status_code}: {response.text[:200]}")
        
        if not response.text or not response.text.strip():
            raise Exception("Request failed: Empty response from server")
        
        try:
            return response.json()
        except ValueError as e:
            print(f"[Debug] Failed to parse JSON response: {str(e)}")
            print(f"[Debug] Response text: {response.text[:500]}")
            raise Exception(f"Request failed: Invalid JSON response from server: {str(e)}")

    def _validateUploadResponse(self, uploadResult):
        """Validate upload response"""
        print(f"[Debug] Upload response: {safe_json_dumps(uploadResult, indent=2) if isinstance(uploadResult, (dict, list)) else uploadResult}")
        
        if "errors" in uploadResult:
            print(f"[Debug] Upload error: {safe_json_dumps(uploadResult, indent=2) if isinstance(uploadResult, (dict, list)) else uploadResult}")
            raise Exception(f"Upload failed: {uploadResult}")

    def _pollForResult(self, taskUuid):
        """Poll for media upload result"""
        pollConfig = [{
            "taskType": "getResponse",
            "taskUUID": taskUuid,
        }]
        
        for attempt in range(self.MAX_POLL_ATTEMPTS):
            try:
                print(f"[Debug] Poll attempt {attempt + 1}/{self.MAX_POLL_ATTEMPTS}")
                
                def recaller():
                    return requests.post(
                        RUNWARE_API_BASE_URL,
                        headers=self._getApiHeaders(),
                        json=pollConfig,
                        timeout=self.REQUEST_TIMEOUT,
                        allow_redirects=False,
                        stream=True,
                    )
                
                pollResult = generalRequestWrapper(recaller)
                pollData = self._parsePollResponse(pollResult)
                
                if pollData:
                    mediaUuid = pollData.get("mediaUUID", "")
                    if mediaUuid == "1":
                        print(f"[Debug] Still processing... attempt {attempt + 1}")
                        time.sleep(self.POLL_INTERVAL)
                        continue
                    elif mediaUuid and mediaUuid != "1":
                        print(f"[Debug] Upload completed! MediaUUID: {mediaUuid}")
                        return mediaUuid
                
                print(f"[Debug] Attempt {attempt + 1}: No data in response, continuing...")
                time.sleep(self.POLL_INTERVAL)
            except Exception as e:
                print(f"[Debug] Poll attempt {attempt + 1} failed: {str(e)}")
                time.sleep(self.POLL_INTERVAL)
                continue
        
        raise Exception("Polling timeout - upload did not complete")

    def _parsePollResponse(self, pollResult):
        """Parse polling response"""
        if pollResult.status_code != 200:
            print(f"[Debug] Poll failed with status {pollResult.status_code}")
            return None
        
        if not pollResult.text or not pollResult.text.strip():
            print(f"[Debug] Poll returned empty response")
            return None
        
        try:
            pollResultJson = pollResult.json()
        except ValueError as e:
            print(f"[Debug] Failed to parse JSON in poll: {str(e)}")
            return None
        
        print(f"[Debug] Poll response: {safe_json_dumps(pollResultJson, indent=2) if isinstance(pollResultJson, (dict, list)) else pollResultJson}")
        
        if "errors" in pollResultJson:
            print(f"[Debug] Poll error: {safe_json_dumps(pollResultJson, indent=2) if isinstance(pollResultJson, (dict, list)) else pollResultJson}")
            return None
        
        if "data" in pollResultJson and len(pollResultJson["data"]) > 0:
            print(f"[Debug] Poll data: {sanitize_for_logging(pollResultJson['data'][0])}")
            return pollResultJson["data"][0]
        
        return None


# Export the class directly
runwareMediaUpload = RunwareMediaUpload
