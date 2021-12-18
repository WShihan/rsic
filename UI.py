# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QMessageBox

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1062, 693)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color:black")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.window_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.window_layout.setContentsMargins(0, 0, 2, 0)
        self.window_layout.setSpacing(5)
        self.window_layout.setObjectName("window_layout")
        self.gv_img = QtWidgets.QGraphicsView(self.centralwidget)
        self.gv_img.setStyleSheet("background-color:white")
        self.gv_img.setObjectName("gv_img")
        self.window_layout.addWidget(self.gv_img)
        self.btn_layout = QtWidgets.QVBoxLayout()
        self.btn_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.btn_layout.setContentsMargins(5, 10, 5, -1)
        self.btn_layout.setSpacing(30)
        self.btn_layout.setObjectName("btn_layout")
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_open.sizePolicy().hasHeightForWidth())
        self.btn_open.setSizePolicy(sizePolicy)
        self.btn_open.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_open.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_open.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.btn_open.setStyleSheet("")
        self.btn_open.setText("")
        self.btn_open.setObjectName("btn_open")
        self.btn_open.setIcon(QIcon('asset/open.png'))
        self.btn_open.clicked.connect(lambda: self.get_file(MainWindow))

        self.btn_layout.addWidget(self.btn_open)
        self.btn_export = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_export.sizePolicy().hasHeightForWidth())
        self.btn_export.setSizePolicy(sizePolicy)
        self.btn_export.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_export.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_export.setText("")
        self.btn_export.setObjectName("btn_export")
        self.btn_export.setIcon(QIcon('asset/export.png'))
        self.btn_export.clicked.connect(lambda: self.test(MainWindow))

        self.btn_layout.addWidget(self.btn_export)
        self.btn_histogram = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_histogram.sizePolicy().hasHeightForWidth())
        self.btn_histogram.setSizePolicy(sizePolicy)
        self.btn_histogram.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_histogram.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_histogram.setText("")
        self.btn_histogram.setObjectName("btn_histogram")
        self.btn_histogram.setIcon(QIcon('asset/histogram.png'))

        self.btn_layout.addWidget(self.btn_histogram)
        self.btn_classify = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_classify.sizePolicy().hasHeightForWidth())
        self.btn_classify.setSizePolicy(sizePolicy)
        self.btn_classify.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_classify.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_classify.setText("")
        self.btn_classify.setObjectName("btn_classify")
        self.btn_classify.setIcon(QIcon('asset/classify.png'))

        self.btn_layout.addWidget(self.btn_classify)
        self.btn_help = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_help.sizePolicy().hasHeightForWidth())
        self.btn_help.setSizePolicy(sizePolicy)
        self.btn_help.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_help.setMaximumSize(QtCore.QSize(50, 50))
        self.btn_help.setText("")
        self.btn_help.setObjectName("btn_help")
        self.btn_help.setIcon(QIcon('asset/help.png'))

        self.btn_layout.addWidget(self.btn_help)
        spacerItem = QtWidgets.QSpacerItem(10, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.btn_layout.addItem(spacerItem)
        self.window_layout.addLayout(self.btn_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wsh遥感分类器"))
        self.btn_open.setToolTip(_translate("MainWindow", "打开文件"))
        self.btn_export.setToolTip(_translate("MainWindow", "结果另存为"))
        self.btn_histogram.setToolTip(_translate("MainWindow", "像元直方图"))
        self.btn_classify.setToolTip(_translate("MainWindow", "分类"))
        self.btn_help.setToolTip(_translate("MainWindow", "帮助"))

    def get_file(self, window):
        file_name, _ = QFileDialog.getOpenFileName(window, "选择影像", r'E:\Desktop', '*.tif')
        print(file_name)
        """
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle("选择影像")
        self.dialog.setFilter("Image files (*.tif)")
        #self.dialog.setFileMode(QFileDialog.AnyFile)  # 设置打开模式
        if self.dialog.exec():
            file_name = self.dialog.selectedFiles()[0]
            print(file_name)
        """

    def test(self, window):
        qmb = QMessageBox.critical(window, '错误', '这是一个错误对话框', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)

