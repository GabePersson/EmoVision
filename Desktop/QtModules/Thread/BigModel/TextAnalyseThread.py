from PyQt5.QtCore import QThread, pyqtSignal
from Modules.TextEmoAnalyse import predict


class TextAnalyseThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(TextAnalyseThread, self).__init__(parent)
        self.text = str()
        self.isRemote = False
        self.remoteIP = None

    def updateText(self, text):
        self.text = text

    def remoteRun(self, ip):
        self.isRemote = True
        self.remoteIP = ip


    def run(self):
        if self.isRemote:
            pass
        else:
            output = predict(self.text)

        self.finished.emit(output)
