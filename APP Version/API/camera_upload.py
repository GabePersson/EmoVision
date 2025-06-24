import time
import cv2
import requests

# TODO: 修改为本地API地址
SERVER_IP = 'http://xxx.xx.xx.xx:25565/face_predict'

# 打开摄像头（0表示第一个摄像头，如果有多个摄像头可以尝试 1, 2 等）
cap = cv2.VideoCapture(0)

# 检查摄像头是否打开成功
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

try:
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            print("无法读取帧")
            break

        # 缩小图像尺寸到640x480
        resized_frame = cv2.resize(frame, (640, 480))

        # 编码图像为JPEG格式
        _, img_encoded = cv2.imencode('.jpg', resized_frame)

        # 上传图像到服务器
        try:
            response = requests.post(SERVER_IP, files={'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')})
            print(f"上传状态: {response.status_code}, 返回信息: {response.text}")
        except Exception as e:
            print(f"上传失败: {e}")

        # 控制帧率
        time.sleep(10)
finally:
    # 释放摄像头并关闭窗口
    cap.release()
