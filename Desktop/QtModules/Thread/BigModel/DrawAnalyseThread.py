from io import BytesIO

import PIL
from PIL import Image
from PyQt5.QtCore import QThread, pyqtSignal, QBuffer

from Modules.DrawAnalyse import predict as predict_picture
from Modules.TextEmoAnalyse import predict as predict_text


class DrawAnalyseThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(DrawAnalyseThread, self).__init__(parent)
        self.picture = PIL.Image.Image()
        self.isRemote = False
        self.remoteIP = None

    def updateImg(self, image):
        self.picture = self.QImage2PIL(image)

    def remoteRun(self, ip):
        self.isRemote = True
        self.remoteIP = ip

    def QImage2PIL(self, qimage):
        """将QImage转换为PIL图像"""
        buffer = QBuffer()
        buffer.open(QBuffer.ReadWrite)

        # 保存 QImage 到缓冲区并确认操作是否成功
        if not qimage.save(buffer, "PNG"):
            raise ValueError("QImage 保存到 QBuffer 失败")

        # 将缓冲区的数据转换为 BytesIO，以便 Pillow 识别
        byte_array = buffer.data()
        buffer.close()

        pil_image = Image.open(BytesIO(byte_array))
        return pil_image

    def run(self):
        if self.isRemote:
            pass
        else:
            output = predict_text(predict_picture(self.picture))

        self.finished.emit(output)
