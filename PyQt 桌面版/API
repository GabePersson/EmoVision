from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from copy import deepcopy
import uvicorn
import time
import json

app = FastAPI()

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


@app.get("/getVideo")
async def get_video():
    return FileResponse("演示.mp4")


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
    if len(faceData['data']) >= 100:
        faceData['data'].pop(0)
        faceData['time'].pop(0)
    faceData['data'].append(json_data)
    faceData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


@app.post("/drawData")
async def get_drawData(request: Request):
    binary_data = await request.body()
    json_data = json.loads(binary_data)
    if len(faceData['data']) >= 100:
        drawData['data'].pop(0)
        drawData['time'].pop(0)
    drawData['data'].append(json_data)
    drawData['time'].append(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))


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
                    key: data[key]*0.8+theFaceData[key]*0.2 for key in data.keys()
                }
        else:
            if theFaceData is None:
                comprehensiveData['data'][idx] = {
                    key: data[key]*0.5+theTextData[key]*0.5 for key in data.keys()
                }
            else:
                comprehensiveData['data'][idx] = {
                    key: data[key]*0.4+theFaceData[key]*0.2+theTextData[key]*0.4 for key in data.keys()
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
    sorted_data = sorted(emoRatio.items(),key=lambda x:x[1], reverse=True)
    bigEmoRation = sorted_data[:2]
    if bigEmoRation[0][1]>=0.5 or bigEmoRation[0][1]>=3*bigEmoRation[1][1]:
        return bigEmoRation[0][0]
    else:
        return bigEmoRation[0][0]+bigEmoRation[1][0]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
