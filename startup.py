# -*- coding: utf-8 -*-
"""
@Date: 2021/12/18
@Author:Wang Shihan
"""
from PyQt5.QtWidgets import QApplication, QMainWindow
from RSIC.UI import Ui_MainWindow
from PyQt5.QtGui import QIcon
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowIcon(QIcon(r'asset/winIcon.png'))
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())
