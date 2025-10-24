import base64
import os
import uuid
import time
import requests
import torch
import torchaudio
import numpy as np
from io import BytesIO
from .utils.runwareUtils import (
    RUNWARE_API_KEY,
    RUNWARE_API_BASE_URL,
    generalRequestWrapper,
    genRandUUID,
    genRandSeed,
    sendMediaUUID,
)

class RunwareMediaUpload:
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
            "hidden": { "node_id": "UNIQUE_ID" }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("mediaUUID",)
    FUNCTION = "uploadMedia"
    CATEGORY = "Runware"
    DESCRIPTION = "Upload audio media to Runware's media storage and get mediaUUID"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(s, **kwargs):
        return float("NAN")

    def uploadMedia(self, media=None, mediaUUID=None, **kwargs):
        print(f"[Debug] uploadMedia called with media: {type(media)}, mediaUUID: {mediaUUID}")
        if media is None:
            raise ValueError("Media input is required")
        
        try:
            # Convert media tensor to base64
            print(f"[Debug] Converting media to base64...")
            media_base64 = self._convert_media_to_base64(media)
            print(f"[Debug] Media converted to base64, length: {len(media_base64)}")
            
            # Upload to Runware
            print(f"[Debug] Starting upload to Runware...")
            media_uuid = self._upload_to_runware(media_base64)
            print(f"[Debug] Upload completed! MediaUUID: {media_uuid}")
            print(f"[Debug] ===== RESULT: {media_uuid} =====")
            
            # Send the mediaUUID back to the UI
            sendMediaUUID(media_uuid, kwargs.get("node_id"))
            
            return (media_uuid,)
            
        except Exception as e:
            print(f"[Debug] Media upload failed: {str(e)}")
            raise e

    def _convert_media_to_base64(self, media_tensor):
        """Convert media tensor to base64 data URI"""
        try:
            # Handle ComfyUI VIDEO objects (VideoFromFile)
            print(f"[Debug] Media type: {type(media_tensor)}")
            print(f"[Debug] Media attributes: {dir(media_tensor)}")
            
            # Check if this is a ComfyUI VideoFromFile object
            if hasattr(media_tensor, 'video_path') or str(type(media_tensor)).find('VideoFromFile') != -1:
                # This is a ComfyUI VideoFromFile object
                print(f"[Debug] VideoFromFile object detected")
                
                # Try to get the file path from the private attribute
                video_file = getattr(media_tensor, '_VideoFromFile__file', None)
                if video_file is None:
                    # Try other possible attributes
                    for attr in ['video_path', 'path', 'file_path', 'filename', '_file']:
                        if hasattr(media_tensor, attr):
                            video_file = getattr(media_tensor, attr)
                            print(f"[Debug] Found video file via {attr}: {video_file}")
                            break
                
                if video_file is None:
                    raise ValueError("Could not find video file in VideoFromFile object")
                
                # If it's a file object, get the path
                if hasattr(video_file, 'name'):
                    video_path = video_file.name
                elif isinstance(video_file, str):
                    video_path = video_file
                else:
                    raise ValueError(f"Unexpected video file type: {type(video_file)}")
                
                print(f"[Debug] Processing video file: {video_path}")
                
                # Read the video file and convert to base64
                with open(video_path, 'rb') as f:
                    video_bytes = f.read()
                
                # Detect MIME type based on file extension
                if video_path.lower().endswith('.mp4'):
                    mime_type = 'video/mp4'
                elif video_path.lower().endswith('.avi'):
                    mime_type = 'video/avi'
                elif video_path.lower().endswith('.mov'):
                    mime_type = 'video/quicktime'
                elif video_path.lower().endswith('.webm'):
                    mime_type = 'video/webm'
                else:
                    mime_type = 'video/mp4'  # Default
                
                # Encode to base64
                video_base64 = base64.b64encode(video_bytes).decode('utf-8')
                
                # Return as data URI
                return f"data:{mime_type};base64,{video_base64}"
            
            # ComfyUI AUDIO objects are dictionaries with 'waveform' and 'sample_rate'
            elif isinstance(media_tensor, dict):
                if 'waveform' in media_tensor:
                    waveform = media_tensor['waveform']
                    sample_rate = media_tensor.get('sample_rate', 22050)
                    
                    # Convert tensor to proper format for torchaudio
                    if isinstance(waveform, torch.Tensor):
                        # Ensure waveform is in the correct format [channels, samples]
                        if waveform.dim() == 3:
                            waveform = waveform.squeeze(0)  # Remove batch dimension
                        elif waveform.dim() == 1:
                            waveform = waveform.unsqueeze(0)  # Add channel dimension
                    else:
                        waveform = torch.tensor(waveform)
                        if waveform.dim() == 1:
                            waveform = waveform.unsqueeze(0)
                    
                    # Create WAV file in memory
                    buffer = BytesIO()
                    torchaudio.save(buffer, waveform, sample_rate, format="wav")
                    buffer.seek(0)
                    
                    # Get the WAV file bytes
                    wav_bytes = buffer.getvalue()
                    
                    # Encode to base64
                    wav_base64 = base64.b64encode(wav_bytes).decode('utf-8')
                    
                    # Return as data URI
                    return f"data:audio/wav;base64,{wav_base64}"
                else:
                    raise ValueError("Invalid audio object: missing 'waveform' key")
            else:
                # Fallback for direct tensor input
                if isinstance(media_tensor, torch.Tensor):
                    waveform = media_tensor
                    sample_rate = 22050  # Default sample rate
                    
                    # Ensure waveform is in the correct format [channels, samples]
                    if waveform.dim() == 3:
                        waveform = waveform.squeeze(0)  # Remove batch dimension
                    elif waveform.dim() == 1:
                        waveform = waveform.unsqueeze(0)  # Add channel dimension
                else:
                    waveform = torch.tensor(media_tensor)
                    sample_rate = 22050
                    if waveform.dim() == 1:
                        waveform = waveform.unsqueeze(0)
                
                # Create WAV file in memory
                buffer = BytesIO()
                torchaudio.save(buffer, waveform, sample_rate, format="wav")
                buffer.seek(0)
                
                # Get the WAV file bytes
                wav_bytes = buffer.getvalue()
                
                # Encode to base64
                wav_base64 = base64.b64encode(wav_bytes).decode('utf-8')
                
                # Return as data URI
                return f"data:audio/wav;base64,{wav_base64}"
            
        except Exception as e:
            print(f"[Debug] Error converting media to base64: {str(e)}")
            raise e

    def _upload_to_runware(self, media_data_uri):
        """Upload media to Runware and return mediaUUID"""
        global RUNWARE_API_KEY, RUNWARE_API_BASE_URL
        
        task_uuid = genRandUUID()
        print(f"[Debug] Generated task UUID: {task_uuid}")
        
        # Strip data URI prefix for media storage API
        if media_data_uri.startswith("data:"):
            media_data = media_data_uri.split(",", 1)[1]
            print(f"[Debug] Stripped data URI prefix, media data length: {len(media_data)}")
        else:
            media_data = media_data_uri
        
        upload_config = [
            {
                "taskType": "mediaStorage",
                "taskUUID": task_uuid,
                "operation": "upload",
                "media": media_data,
            }
        ]
        
        print(f"[Debug] Upload config: {upload_config[0]}")
        print(f"[Debug] API URL: {RUNWARE_API_BASE_URL}")
        
        headers = {
            "Authorization": f"Bearer {RUNWARE_API_KEY}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }
        
        try:
            def recaller():
                print(f"[Debug] Making POST request to Runware API...")
                return requests.post(
                    RUNWARE_API_BASE_URL,
                    headers=headers,
                    json=upload_config,
                    timeout=30,
                    allow_redirects=False,
                    stream=True,
                )
            
            upload_result = generalRequestWrapper(recaller)
            upload_result = upload_result.json()
            print(f"[Debug] Upload response: {upload_result}")
            
            if "errors" in upload_result:
                print(f"[Debug] Upload error: {upload_result}")
                raise Exception(f"Upload failed: {upload_result}")
            
            # Check if we got immediate result or need to poll
            if upload_result.get("data") and len(upload_result["data"]) > 0:
                data = upload_result["data"][0]
                print(f"[Debug] Upload data: {data}")
                if "mediaUUID" in data and data["mediaUUID"] != "1":
                    print(f"[Debug] Got immediate mediaUUID: {data['mediaUUID']}")
                    return data["mediaUUID"]
            
            # Poll for result
            print(f"[Debug] Starting polling for result...")
            return self._poll_for_result(task_uuid)
            
        except Exception as e:
            print(f"[Debug] Upload request failed: {str(e)}")
            raise e

    def _poll_for_result(self, task_uuid):
        """Poll for media upload result"""
        global RUNWARE_API_KEY, RUNWARE_API_BASE_URL
        
        poll_config = [
            {
                "taskType": "getResponse",
                "taskUUID": task_uuid,
            }
        ]
        
        headers = {
            "Authorization": f"Bearer {RUNWARE_API_KEY}",
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip, deflate, br, zstd",
        }
        
        max_attempts = 100
        for attempt in range(max_attempts):
            try:
                print(f"[Debug] Poll attempt {attempt + 1}/{max_attempts}")
                def recaller():
                    return requests.post(
                        RUNWARE_API_BASE_URL,
                        headers=headers,
                        json=poll_config,
                        timeout=30,
                        allow_redirects=False,
                        stream=True,
                    )
                
                poll_result = generalRequestWrapper(recaller)
                poll_result = poll_result.json()
                print(f"[Debug] Poll response: {poll_result}")
                
                if "errors" in poll_result:
                    print(f"[Debug] Poll error: {poll_result}")
                    continue
                
                if "data" in poll_result and len(poll_result["data"]) > 0:
                    data = poll_result["data"][0]
                    print(f"[Debug] Poll data: {data}")
                    
                    # Check if mediaUUID is still "1" (still processing)
                    if "mediaUUID" in data and data["mediaUUID"] == "1":
                        print(f"[Debug] Still processing... attempt {attempt + 1}")
                        time.sleep(2)
                        continue
                    
                    # Check for completion - look for mediaUUID
                    if "mediaUUID" in data and data["mediaUUID"] != "1":
                        print(f"[Debug] Upload completed! MediaUUID: {data['mediaUUID']}")
                        return data["mediaUUID"]
                
                print(f"[Debug] Attempt {attempt + 1}: No data in response, continuing...")
                time.sleep(2)
                
            except Exception as e:
                print(f"[Debug] Poll attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)
                continue
        
        raise Exception("Polling timeout - upload did not complete")


# Export the class directly
runwareMediaUpload = RunwareMediaUpload
