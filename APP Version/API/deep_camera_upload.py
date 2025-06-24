import time
import requests
import pyrealsense2 as rs
import numpy as np
import cv2

# TODO: 修改为本地API地址
SERVER_IP = 'http://xxx.xx.xx.xx:25565/face_predict'

# 检查是否连接了深度相机
context = rs.context()
assert len(context.devices) > 0, "没有检测到深度相机"

# 配置相机
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

# 启动pipeline
profile = pipeline.start(config)

# 创建对齐对象（用于对齐彩色和深度帧）
align_to = rs.stream.color
align = rs.align(align_to)

# 主循环
try:
    while True:
        # 获取帧
        frames = pipeline.wait_for_frames()

        # 对齐深度帧到彩色帧
        aligned_frames = align.process(frames)
        color_frame = aligned_frames.get_color_frame()

        if color_frame:
            # 将彩色帧转换为numpy数组
            color_image = np.asanyarray(color_frame.get_data())

            # 缩小图像尺寸到640x480
            resized_image = cv2.resize(color_image, (640, 480))

            # 编码图像为JPEG格式
            _, img_encoded = cv2.imencode('.jpg', resized_image)

            # 将图像上传到服务器
            try:
                response = requests.post(SERVER_IP, files={'file': ('frame.jpg', img_encoded.tobytes(), 'image/jpeg')})
                print(f"上传状态: {response.status_code}, 返回信息: {response.text}")
            except Exception as e:
                print(f"Error sending data: {e}")

        time.sleep(10)  # 控制帧率
except KeyboardInterrupt:
    print("程序停止")
finally:
    # 停止相机
    pipeline.stop()
