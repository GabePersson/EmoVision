import sys

from PyQt5.QtWidgets import QApplication

from QtModules.UI.MainWindow import MainWindow

app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec())
