import io
import json
import os
import shutil
import time
from copy import deepcopy
import subprocess
import requests
import PIL.Image
from Modules.DrawAnalyse import predict as predict_picture
from Modules.TextEmoAnalyse import predict as predict_text
from fastapi import FastAPI, Body, UploadFile, File, Request, Form
import uvicorn

app = FastAPI()

Texten2cn = {
    'angry': '怒',
    'sad': '忧',
    'fear': '恐',
    'happy': '喜',
    'neutral': '思',
    # 'sad': '悲', 这里归类为忧
    'surprise': '惊'
}

@app.post('/picture_predict')
async def process_picture_info(file: UploadFile = File(...)):
    content = await file.read()
    image = PIL.Image.open(io.BytesIO(content)).convert("RGB")
    result = predict_picture(image)
    if result is None:
        print("没额度了")
        return
    result = predict_text(result)
    result = {
        Texten2cn[key]: value for key, value in result.items()
    }
    requests.post(url='http://localhost:25565/picture_predict',json=result)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=25564)
