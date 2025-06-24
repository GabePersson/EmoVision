import urllib.request
from PyQt5 import QtWidgets
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QDesktopServices, QPainter
from PyQt5.QtWidgets import QColorDialog, QFileDialog, QProgressBar, QLabel, QMessageBox
from QtModules.Thread.MusicPlayerThread import MusicPlayerThread
from QtModules.UI.Ui_MainWindow import Ui_MainWindow
from QtModules.Thread.GenerateImageThread import GenerateImageThread
from QtModules.Thread.CameraThread import CameraThread
from QtModules.UI.DrawingScene import DrawingScene
from QtModules.Thread.VoiceThread import VoiceThread
from QtModules.Thread.DepthCameraThread import DepthCameraThread
from QtModules.Thread.BigModelThreadManager import BigModelThreadManager

#TODO:将此处改为本地API
SERVER_IP = 'http://<IP_ADDRESS:PORT>'

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.useUserImg = True
        self.refImg = QImage()

        ## 摄像头模块
        # 创建摄像头线程
        self.camera_thread = CameraThread()
        # 启用摄像头
        self.ckbox_camera.stateChanged.connect(self.onChkboxCamera)
        ## End

        self.graphScene = DrawingScene(self)
        self.graphScene.setSceneRect(0, 0, 800, 600)
        self.graphicsView.setScene(self.graphScene)

        ## 编辑颜色按钮
        self.btn_editColor.clicked.connect(self.onBtnColorEdit)
        ## End

        ## 编辑笔刷类型
        self.penType = self.cbox_penType.currentText()
        self.cbox_penType.currentTextChanged.connect(self.onCboxPenTypeChanged)
        ## End

        ## 编辑笔刷大小
        self.sbox_size.setValue(self.graphScene.getPenWidth())
        self.sbox_size.valueChanged.connect(self.onSboxSizeChanged)

        self.btn_back.clicked.connect(self.graphScene.undo)
        self.btn_clear.clicked.connect(self.onBtnClear)
        self.btn_endDrawing.clicked.connect(self.onBtnEndDrawing)

        self.btn_saveDraw.clicked.connect(self.graphScene.saveImg)

        self.btn_voice.clicked.connect(self.onBtnVoice)

        # 生成参考图像
        self.btn_saveRefImg.setEnabled(False)
        self.btn_genImg.clicked.connect(self.onBtnGenerateImg)

        # 保存参考图像
        self.btn_saveRefImg.clicked.connect(self.onBtnSaveRefImg)

        # 设置状态栏
        self.drawingProressBar = QProgressBar()
        self.drawingProressBar.setMinimum(0)
        self.drawingProressBar.setMaximum(3)
        self.drawingProressBar.setTextVisible(False)
        self.drawingProressBar.setFixedWidth(100)  # 设置进度条的宽度为100像素
        self.drawingProressBar.setValue(1)

        self.drawingProressText = QLabel()
        self.drawingProressText.setText("目前为第一阶段：绘画")

        # 创建一个占位符标签来模拟空隙
        self.drawingSpacer = QLabel()
        self.drawingSpacer.setFixedWidth(20)  # 设置空隙宽度

        # 将小部件直接添加到状态栏
        self.statusBar.addWidget(self.drawingSpacer)
        self.statusBar.addWidget(self.drawingProressBar)
        self.statusBar.addWidget(self.drawingProressText)

        # 大模型后台处理
        self.timer = QTimer()
        self.timer.timeout.connect(self.runBigModel)
        self.timer.start(5000)  # 每5秒运行一次

        # 初始化大模型管理器
        self.BigModelThreadManager = BigModelThreadManager()

        # 音乐播放器
        self.musicPlayerThread = MusicPlayerThread()
        self.ckbox_music.stateChanged.connect(self.onCkboxMusic)

        # 清理数据
        self.clearData()

        # 深度相机
        self.depth_camera_thread = DepthCameraThread()

    def confirmAction(self, title="确认操作", text="你确定要执行该操作吗"):
        reply = QMessageBox.question(
            self,
            title,
            text,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def onChkboxCamera(self, checked: bool):
        if checked:
            self.start_camera()
        else:
            self.stop_camera()

    def onBtnColorEdit(self):
        self.graphScene.setPenColor(QColorDialog.getColor(self.graphScene.getPenColor(), self, "选择颜色"))

    def onSboxSizeChanged(self):
        self.graphScene.setPenWidth(self.sbox_size.value())

    def onCboxPenTypeChanged(self):
        self.graphScene.setCurrentTool(self.cbox_penType.currentText())

    def onBtnVoice(self):
        self.btn_voice.setEnabled(False)

        self.voiceThread = VoiceThread()
        self.voiceThread.finished.connect(self.VoiceRecognitionFinished)
        self.voiceThread.start()

    def VoiceRecognitionFinished(self, text):
        self.btn_voice.setEnabled(True)
        self.ledit_prompt.setText(text)

    def onBtnGenerateImg(self):
        self.btn_genImg.setEnabled(False)

        self.generateImageThread = GenerateImageThread(self.ledit_prompt.text())
        self.generateImageThread.finished.connect(self.GenerateImageFinished)
        self.generateImageThread.start()

        # prompt情感分类
        self.BigModelThreadManager.runText(self.ledit_prompt.text())

    def GenerateImageFinished(self, qimage: QImage):
        self.rbtn_refImgAnalyse.setEnabled(True)
        self.btn_genImg.setEnabled(True)
        self.btn_saveRefImg.setEnabled(True)
        if qimage.isNull():
            # TODO:因为额度问题，因此此处采用之前生成的图片
            with open("Srcs/sample_generation.jpg", 'rb') as f:
                data = f.read()
            qimage.loadFromData(data)
        self.refImg = qimage
        qimage = qimage.scaled(self.label_refImg.size())
        self.label_refImg.setPixmap(QPixmap.fromImage(qimage))

    def onBtnSaveRefImg(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(None, "保存图像", "",
                                                  "PNG Files (*.png);;JPEG Files (*.jpg; *.jpeg);;All Files (*)",
                                                  options=options)

        if fileName:
            self.refImg.save(fileName)

    def onBtnClear(self):
        if self.confirmAction(text="你确定清空画布吗"):
            self.graphScene.clear()

    def onBtnEndDrawing(self):
        if self.confirmAction(title="结束绘画", text="你确认结束绘画吗?"):
            if self.drawingProressBar.value() == 1:
                self.toSecondStage()
            elif self.drawingProressBar.value() == 3:
                self.endStage()

    def toSecondStage(self):
        self.musicPlayerThread.updateMusicList(self.getBigEmo())
        if self.ckbox_music.isChecked():
            self.musicPlayerThread.run()
        self.graphScene.clear()
        self.drawingProressBar.setValue(2)
        self.drawingProressText.setText("第二阶段：听音乐")
        self.open_website()

        while not self.confirmAction(title="结束音乐疗愈", text="你确认结束音乐部分吗？"):
            pass
        self.toThirdStage()

    def open_website(self):
        # 设置要打开的URL
        url = QUrl("http://sugar.bce.baidu.com/group/first/preview/dashboard/d_1013e-ipngz4p-kwjx63?hideReturnButton=1&__scp__=scp_1013e-6f3hfbrw-k4z7rg")
        # 在默认浏览器中打开链接
        QDesktopServices.openUrl(url)

    def toThirdStage(self):
        self.stopMusic()
        self.drawingProressBar.setValue(3)
        self.drawingProressText.setText("第三阶段：绘画")

    def endStage(self):
        QMessageBox.information(
            self,
            "结束疗愈",
            "感谢您的使用。",
            QMessageBox.Ok,
            QMessageBox.Ok
        )
        self.close()

    def start_camera(self):
        if self.depth_camera_thread.checkCamera():
            self.depth_camera_thread.start()
        else:
            print("无深度相机，不进行深度相机分析")
            self.camera_thread.start()


    def stop_camera(self):
        if self.depth_camera_thread.isRunning():
            self.depth_camera_thread.stop()
            self.depth_camera_thread.wait()
        elif self.camera_thread.isRunning():
            self.camera_thread.stop()
            self.camera_thread.wait()


    def runBigModel(self):
        # 运行大模型的例子，传入图片和文本数据
        if self.camera_thread.isRunning():
            img = self.camera_thread.img
            if not img.isNull():
                self.BigModelThreadManager.runFace(img)
        elif self.depth_camera_thread.isRunning():
            img = self.depth_camera_thread.img
            if not img.isNull():
                self.BigModelThreadManager.runFace(img)
        # 将场景渲染到一个QImage中

        if self.rbtn_selfDrawAnalyse.isChecked():
            draw_img = QImage(self.graphScene.sceneRect().size().toSize(), QImage.Format_RGB32)
            draw_img.fill(Qt.white)
            # 使用QPainter将场景绘制到QImage上
            painter = QPainter(draw_img)
            self.graphScene.render(painter)
            painter.end()
        else:
            draw_img = self.refImg
        self.BigModelThreadManager.runDraw(draw_img)

    def clearData(self):
        url = SERVER_IP + '/clear'
        urllib.request.urlopen(url)

    def getBigEmo(self):
        url = SERVER_IP + '/music'
        response = urllib.request.urlopen(url).read().decode('utf-8')
        return response

    def onCkboxMusic(self, checked):
        if self.musicPlayerThread.init:
            if checked:
                self.musicPlayerThread.player.play()
            else:
                self.musicPlayerThread.player.stop()
    def stopMusic(self):
        self.musicPlayerThread.stop()
