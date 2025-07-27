from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog
from collections import deque


class DrawingScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(DrawingScene, self).__init__(parent)
        self.pen = QPen(Qt.black, 5, Qt.SolidLine)
        self.brush = QBrush(Qt.NoBrush)
        self.drawing = False
        self.lastPoint = QPointF()
        self.currentTool = '笔'
        self.currentRect = None
        self.currentLine = None
        self.currentEllipse = None

        self.shapes_stack = deque()  # 用于保存绘制的图形

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.scenePos()

            if self.currentTool == '直线':
                self.currentLine = self.addLine(self.lastPoint.x(), self.lastPoint.y(),
                                                self.lastPoint.x(), self.lastPoint.y(), self.pen)
                self.shapes_stack.append(self.currentLine)  # 将图形加入栈中

            elif self.currentTool == '矩形':
                self.currentRect = self.addRect(self.lastPoint.x(), self.lastPoint.y(), 0, 0, self.pen)
                self.shapes_stack.append(self.currentRect)

            elif self.currentTool == '椭圆':
                self.currentEllipse = self.addEllipse(self.lastPoint.x(), self.lastPoint.y(), 0, 0, self.pen)
                self.shapes_stack.append(self.currentEllipse)

    def mouseMoveEvent(self, event):
        if self.drawing:
            if self.currentTool == '笔':
                self.addLine(self.lastPoint.x(), self.lastPoint.y(),
                             event.scenePos().x(), event.scenePos().y(), self.pen)
                self.lastPoint = event.scenePos()

            elif self.currentTool == '直线' and self.currentLine:
                self.currentLine.setLine(self.lastPoint.x(), self.lastPoint.y(),
                                         event.scenePos().x(), event.scenePos().y())

            elif self.currentTool == '矩形' and self.currentRect:
                self.currentRect.setRect(self.lastPoint.x(), self.lastPoint.y(),
                                         event.scenePos().x() - self.lastPoint.x(),
                                         event.scenePos().y() - self.lastPoint.y())

            elif self.currentTool == '椭圆' and self.currentEllipse:
                self.currentEllipse.setRect(self.lastPoint.x(), self.lastPoint.y(),
                                            event.scenePos().x() - self.lastPoint.x(),
                                            event.scenePos().y() - self.lastPoint.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            self.currentLine = None
            self.currentRect = None
            self.currentEllipse = None

    def undo(self):
        if self.shapes_stack:
            shape = self.shapes_stack.pop()  # 弹出栈顶图形
            self.removeItem(shape)  # 从场景中移除图形


    def setPenColor(self, color):
        self.pen.setColor(color)

    def getPenColor(self):
        return self.pen.color()

    def setPenWidth(self, width):
        self.pen.setWidth(width)

    def getPenWidth(self):
        return self.pen.width()

    def setCurrentTool(self, toolName):
        self.currentTool = toolName

    def saveImg(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(None, "保存图像", "",
                                                  "PNG Files (*.png);;JPEG Files (*.jpg; *.jpeg);;All Files (*)",
                                                  options=options)

        if fileName:
            pixmap = QPixmap(int(self.width()) + 1, int(self.height()) + 1)
            pixmap.fill(Qt.white)

            painter = QPainter(pixmap)
            self.render(painter)
            painter.end()

            pixmap.save(fileName)
