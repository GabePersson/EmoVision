from PyQt5.QtCore import QThread, pyqtSignal, qDebug
from PyQt5.QtGui import QImage
from Modules.GenerateImg import generate_image_from_text
import urllib.request


class GenerateImageThread(QThread):
    finished = pyqtSignal(QImage)

    def __init__(self, text, parent=None):
        super(GenerateImageThread, self).__init__(parent)
        self.text = text

    def run(self):
        qDebug("Loading the image generate module")
        qimage = QImage()
        try:
            image_url = generate_image_from_text(self.text)
            with urllib.request.urlopen(image_url) as f:
                image_data = f.read()
            qimage.loadFromData(image_data)
        except Exception as e:
            qDebug(str(e))
        finally:
            self.finished.emit(qimage)
