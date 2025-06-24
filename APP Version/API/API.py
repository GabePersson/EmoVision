import json
import os
import shutil
import time
from copy import deepcopy
import subprocess

import PIL.Image
from Modules.TextEmoAnalyse import predict as predict_text
from Modules.EmoAnalyse import predict as predict_face
from Modules.GenerateSimpleDraw import generate
from Modules.VoiceRecognition import voice_input
from Modules.GenerateImg import generate_image_from_text
from fastapi import FastAPI, UploadFile, File, Request, Form
from pydantic import BaseModel
import uvicorn

app = FastAPI()
data_save_dir = 'data'


class TextModel(BaseModel):
    text: str


Faceen2cn = {
    'angry': '怒',
    'disgusted': '忧',
    'fearful': '恐',
    'happy': '喜',
    'neutral': '思',
    # 'sad': '悲', 这里归类为忧
    'surprised': '惊'
}
Texten2cn = {
    'angry': '怒',
    'sad': '忧',
    'fear': '恐',
    'happy': '喜',
    'neutral': '思',
    # 'sad': '悲', 这里归类为忧
    'surprise': '惊'
}


### uniapp端的情绪处理模块 ###

@app.post('/picture_predict')
async def process_picture_info(request: Request):
    result = await request.json()
    if len(drawData['data']) >= 100:
        drawData['data'].pop(0)
        drawData['time'].pop(0)
    drawData['data'].append(result)
    drawData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


@app.post('/process_text_info')
def process_text_info(text: TextModel):
    result = predict_text(text.text)
    result = {
        Texten2cn[key]: value for key, value in result.items()
    }
    if len(textData['data']) >= 100:
        textData['data'].pop(0)
        textData['time'].pop(0)
    textData['data'].append(result)
    textData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


face_save_path = os.path.join(data_save_dir, 'tempface.jpg')


@app.post('/face_predict')
def face_predict(file: UploadFile = File(...)):
    try:
        img_file = file.file
        with open(face_save_path, 'wb') as buffer:
            shutil.copyfileobj(img_file, buffer)

    except Exception as e:
        print(e)

    result = predict_face(PIL.Image.open(face_save_path))
    result['disgusted'] += result['sad']
    result.pop('sad')
    result = {
        Faceen2cn[key]: value for key, value in result.items()
    }
    if len(faceData['data']) >= 100:
        faceData['data'].pop(0)
        faceData['time'].pop(0)
    faceData['data'].append(result)
    faceData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


@app.post('/text_predict')
def generate_image(data: TextModel):
    input_text = data.text
    process_text_info(input_text)
    image_url = generate_image_from_text(input_text)
    if image_url is not None:
        return {'image_url': image_url}
    else:
        return None


audio_save_path = os.path.join(data_save_dir, 'tempaudio.mp3')
wav_save_path = os.path.join(data_save_dir, 'temp.wav')
VOICE_TRANSFORM = ['ffmpeg', '-i', audio_save_path, wav_save_path]


@app.post('/voice_recognition')
def voice_recog(file: UploadFile = File(...)):
    result = ""
    try:
        audio_file = file.file

        with open(audio_save_path, 'wb') as buffer:
            shutil.copyfileobj(audio_file, buffer)
        subprocess.run(VOICE_TRANSFORM, input=b'y\n', check=True)
        result = voice_input(wav_save_path)
    except Exception as e:
        print(e)
    return {
        'result': result
    }


@app.post('/generate_ref_img')
def generate_ref_img(text: TextModel):
    content = text.text
    img_url = generate_image_from_text(content)
    if img_url is None:
        return {
            "image_url": ""
        }
    else:
        return {
            "image_url": img_url
        }


img_save_path = 'temp.png'


@app.post('/generate_next_img')
def generate_next_img(file: UploadFile = File(...), prompt: str = Form(...)):
    try:
        img_file = file.file

        with open(img_save_path, 'wb') as buffer:
            shutil.copyfileobj(img_file, buffer)
    except Exception as e:
        print(e)

    img_url = generate(img_save_path, prompt)
    if img_url is None:
        return {
            "image_url": None
        }
    else:
        return {
            "image_url": img_url
        }



### uniapp独有API模块结束 ###


emoLabels = ["喜", "怒", "思", "惊", "恐", "忧"]

originData = {
    "time": [],
    "data": []
}

faceData = deepcopy(originData)
drawData = deepcopy(originData)
textData = deepcopy(originData)

comprehensiveData = deepcopy(originData)

nextStage = False


### SugarBI模块 ###

@app.get("/ranking_api")
async def get_ranking_api():
    sumEmo()
    if len(comprehensiveData['time']) != 0:
        rows = [
            {
                "mental": emo,
                "ratio": comprehensiveData["data"][-1][emo]
            } for emo in emoLabels
        ]
    else:
        rows = []
    data = {
        "status": 0,
        "msg": "",
        "data": {
            "columns": [
                {
                    "id": "mental",
                    "name": "情绪"
                },
                {
                    "id": "ratio",
                    "name": "情绪占比"
                }
            ],
            "rows": rows
        }
    }
    return data


@app.get("/river_api")
async def get_river_api():
    sumEmo()
    goal_data = []
    if len(comprehensiveData['time']) != 0:
        for emo in emoLabels:
            for idx, theTime in enumerate(comprehensiveData['time']):
                goal_data.append([theTime, comprehensiveData['data'][idx][emo], emo])

    data = {
        "status": 0,
        "msg": "",
        "data":
            {
                "legend": emoLabels,
                "data": goal_data
            }
    }
    return data


def sumEmo():
    if len(faceData['data']) != 0:
        theFaceData = faceData['data'][-1]
    else:
        theFaceData = None
    if len(textData['data']) != 0:
        theTextData = textData['data'][-1]
    else:
        theTextData = None
    global comprehensiveData
    comprehensiveData = deepcopy(drawData)
    for idx, data in enumerate(comprehensiveData['data']):
        if theTextData is None:
            if theFaceData is None:
                break
            else:
                comprehensiveData['data'][idx] = {
                    key: data[key] * 0.8 + theFaceData[key] * 0.2 for key in data.keys()
                }
        else:
            if theFaceData is None:
                comprehensiveData['data'][idx] = {
                    key: data[key] * 0.5 + theTextData[key] * 0.5 for key in data.keys()
                }
            else:
                comprehensiveData['data'][idx] = {
                    key: data[key] * 0.4 + theFaceData[key] * 0.2 + theTextData[key] * 0.4 for key in data.keys()
                }


@app.post("/enterNextStage")
async def enterNextStage():
    global nextStage
    nextStage = True


@app.post("/stopNextStage")
async def enterNextStage():
    global nextStage
    nextStage = False


@app.get("/clear")
async def clear():
    global comprehensiveData
    global faceData
    global drawData
    global textData

    faceData = deepcopy(originData)
    drawData = deepcopy(originData)
    textData = deepcopy(originData)
    comprehensiveData = deepcopy(originData)


@app.get('/music')
async def getMusic():
    sumEmo()
    emoRatio = comprehensiveData['data'][-1]
    sorted_data = sorted(emoRatio.items(), key=lambda x: x[1], reverse=True)
    bigEmoRation = sorted_data[:2]
    if bigEmoRation[0][1] >= 0.5 or bigEmoRation[0][1] >= 3 * bigEmoRation[1][1]:
        return bigEmoRation[0][0]
    else:
        return bigEmoRation[0][0] + bigEmoRation[1][0]


@app.get('/most_emo')
async def getMostEmo():
    sumEmo()
    emoRatio = comprehensiveData['data'][-1]
    sorted_data = sorted(emoRatio.items(), key=lambda x: x[1], reverse=True)
    bigEmoRation = sorted_data[:2]
    if bigEmoRation[0][1] >= 0.5 or bigEmoRation[0][1] >= 3 * bigEmoRation[1][1]:
        return bigEmoRation[0][0]
    else:
        return bigEmoRation[0][0] + bigEmoRation[1][0]


### SugarBI模块结束 ###

### Qt模块 ###

@app.post("/faceData")
async def get_faceData(request: Request):
    binary_data = await request.body()
    json_data = json.loads(binary_data)
    if len(faceData['data']) >= 100:
        faceData['data'].pop(0)
        faceData['time'].pop(0)
    faceData['data'].append(json_data)
    faceData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


@app.post("/textData")
async def get_textData(request: Request):
    binary_data = await request.body()
    json_data = json.loads(binary_data)
    if len(textData['data']) >= 100:
        textData['data'].pop(0)
        textData['time'].pop(0)
    textData['data'].append(json_data)
    textData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


@app.post("/drawData")
async def get_drawData(request: Request):
    binary_data = await request.body()
    json_data = json.loads(binary_data)
    if len(drawData['data']) >= 100:
        drawData['data'].pop(0)
        drawData['time'].pop(0)
    drawData['data'].append(json_data)
    drawData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


### Qt模块结束 ###

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=25565)
