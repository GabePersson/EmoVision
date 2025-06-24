import cv2
import socket
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage
#TODO:修改为API地址
SERVER_IP = 'localhost'

class CameraThread(QThread):
    def __init__(self, parent=None):
        super(CameraThread, self).__init__(parent)
        self.cap = None
        self.running = False
        self.img = QImage()
        self.server_address = (SERVER_IP, 8002)  # 替换为服务器IP和端口
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.cap = cv2.VideoCapture(0)  # 打开摄像头
        self.running = True

        while self.running:
            ret, frame = self.cap.read()  # 读取帧
            if ret:
                # 缩小图像尺寸到640x480
                frame = cv2.resize(frame, (640, 480))

                # 转换为QImage以显示
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                self.img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()

                # 编码帧为JPEG格式
                _, img_encoded = cv2.imencode('.jpg', frame)

                # 发送帧数据到服务器（通过UDP）
                try:
                    self.sock.sendto(img_encoded.tobytes(), self.server_address)
                except Exception as e:
                    print(e)

            self.msleep(33)  # 控制帧率

    def stop(self):
        self.running = False
        self.msleep(100)
        if self.cap is not None:
            self.cap.release()
        self.sock.close()  # 关闭UDP socket
