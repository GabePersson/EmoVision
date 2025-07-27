from fastapi import FastAPI

from fastapi.responses import FileResponse
import uvicorn
import os

app = FastAPI()
video_dir = 'video'

@app.get('/video_{index}')
async def process_picture_info(index:int):
    video_path = os.path.join(video_dir,str(index)+'.mp4')
    return FileResponse(video_path)







if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=25563)
