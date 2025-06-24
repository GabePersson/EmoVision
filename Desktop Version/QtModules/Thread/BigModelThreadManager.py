import json
import time
import urllib.request
from PyQt5.QtGui import QImage
from QtModules.Thread.BigModel.FaceAnalyseThread import FaceAnalyseThread

from QtModules.Thread.BigModel.TextAnalyseThread import TextAnalyseThread

from QtModules.Thread.BigModel.DrawAnalyseThread import DrawAnalyseThread

# TODO:此处改为分析服务器IP
SERVER_IP = 'http://localhost:8001'


class BigModelThreadManager:
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

    def __init__(self):
        # 标记每种分析的运行状态
        # self.runFaceAnalyse = False
        # self.runTextAnalyse = False
        # self.runRemote = False  # 用于远程分析选项

        # 初始化分析线程
        self.faceAnalyseThread = FaceAnalyseThread()
        self.textAnalyseThread = TextAnalyseThread()
        self.drawAnalyseThread = DrawAnalyseThread()

        # 连接线程的 finished 信号到槽函数
        self.faceAnalyseThread.finished.connect(self.onFaceAnalyseFinished)
        self.textAnalyseThread.finished.connect(self.onTextAnalyseFinished)
        self.drawAnalyseThread.finished.connect(self.onDrawAnalyseFinished)

    def runFace(self, image: QImage):
        self.faceAnalyseThread.updateImg(image)
        if not self.faceAnalyseThread.isRunning():
            self.faceAnalyseThread.start()  # 启动线程进行人脸分析

    def runText(self, text: str):
        self.textAnalyseThread.updateText(text)
        if not self.textAnalyseThread.isRunning():
            self.textAnalyseThread.start()  # 启动线程进行文本分析

    def runDraw(self, image: QImage):
        self.drawAnalyseThread.updateImg(image)
        if not self.drawAnalyseThread.isRunning():
            self.drawAnalyseThread.start()  # 启动线程进行人脸分析

    def onFaceAnalyseFinished(self, theDict):
        url = SERVER_IP + '/faceData'
        # 将数据编码为URL格式，并转换为字节流
        theDict['disgusted'] += theDict['sad']
        theDict.pop('sad')
        theDict = {
            self.Faceen2cn[key]: value for key, value in theDict.items()
        }
        print(theDict)
        data = json.dumps(theDict).encode('utf-8')
        try:
            response = urllib.request.urlopen(url, data=data)
        except Exception as e:
            print(f"Face Analyse:{e}")

    def onTextAnalyseFinished(self, theDict):
        url = SERVER_IP + '/textData'
        # 将数据编码为URL格式，并转换为字节流
        theDict = {
            self.Texten2cn[key]: value for key, value in theDict.items()
        }
        print(theDict)
        data = json.dumps(theDict).encode('utf-8')
        try:
            response = urllib.request.urlopen(url, data=data)
        except Exception as e:
            print(f"Face Analyse:{e}")

    def onDrawAnalyseFinished(self, theDict):
        url = SERVER_IP + '/drawData'
        # 将数据编码为URL格式，并转换为字节流
        theDict = {
            self.Texten2cn[key]: value for key, value in theDict.items()
        }
        print(theDict)
        data = json.dumps(theDict).encode('utf-8')
        try:
            response = urllib.request.urlopen(url, data=data)
        except Exception as e:
            print(f"Face Analyse:{e}")

    # def setRemoteRun(self, remote: bool):
    #     self.runRemote = remote  # 设置是否启用远程分析
