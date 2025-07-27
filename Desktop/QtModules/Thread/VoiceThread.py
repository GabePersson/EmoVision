from PyQt5.QtCore import QThread, pyqtSignal, qDebug
from Modules.VoiceRecognition import voice_input


class VoiceThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        qDebug("Loading the voice module")
        text = ""
        try:
            text = voice_input()
        except Exception as e:
            raise e
        finally:
            self.finished.emit(text)
