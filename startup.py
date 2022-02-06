# -*- coding: utf-8 -*-
"""
@Date: 2022/2/6
@Author:Wang Shihan
"""
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from RSIC.utils import Chart, PhotoViewer, Tiff2array, Exporter
from RSIC.UI import Ui_MainWindow

class RSIC_Win(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(RSIC_Win, self).__init__()
        self.file_name = None
        self.setUI()
    def setUI(self):
        self.setupUi(self)
        # 窗体初始化大小
        self.resize(1600, 900)
        self.setStyleSheet("background-color:#212220")
        # 设置图标
        self.setWindowIcon(QIcon(r'asset/icon/sticker.png'))
        self.btn_open.setIcon(QIcon('asset/icon/open.png'))
        self.btn_export.setIcon(QIcon('asset/icon/export.png'))
        self.btn_histogram.setIcon(QIcon('asset/icon/histogram.png'))
        self.btn_classify.setIcon(QIcon('asset/icon/classify.png'))
        self.btn_help.setIcon(QIcon('asset/icon/help.png'))

        self.add_slot()

    def add_slot(self):
        self.btn_open.clicked.connect(lambda: self.get_file())
        self.btn_export.clicked.connect(self.export_img)
        self.btn_histogram.clicked.connect(self.func_stastic)
        self.btn_help.clicked.connect(self.help)

    def get_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "选择影像", r'E:\Desktop\GisFile\DEM',
                                                       '*.tif;;*.jpg;;*.jpeg;;*.png')
            if file_name:
                self.file_name = file_name
                self.tif_thread = Tiff2array(self.file_name)
                self.tif_thread.singal.connect(self.show_chart)
                self.gv_img.setPhoto(QPixmap(self.file_name))
        except Exception as e:
            print("Select file failed!" + str(e))
        """
        # 添加图片到QGraphicsView
        pix = QPixmap(self.file_name)
        item = QGraphicsPixmapItem(pix)
        scene = QGraphicsScene()
        scene.addItem(item)
        self.gv_img.setScene(scene)

        # 打开影像的另外一种方法
        self.dialog = QFileDialog()
        self.dialog.setWindowTitle("选择影像")
        self.dialog.setFilter("Image files (*.tif)")
        #self.dialog.setFileMode(QFileDialog.AnyFile)  # 设置打开模式
        if self.dialog.exec():
            file_name = self.dialog.selectedFiles()[0]
            print(file_name)
        """
    def func_stastic(self):
        try:
            if self.file_name:
                self.tif_thread.start()
            else:
                QMessageBox.information(self.centralwidget, '消息', '未选择影像!', QMessageBox.Yes)
        except Exception as e:
            print("read tiff failed!" + str(e))

    def show_chart(self,n):
        chart = Chart(n)
        chart.show()
    def export_img(self):
        try:
            if self.file_name:
                fname, ftype = QFileDialog.getSaveFileName(self.centralwidget, '导出为', 'E:/Desktop',
                                                           "*.png;;*.tif;;*.jpg")
                if fname:
                    exporter = Exporter(self.gv_img.scene(), fname)
                    exporter.start()
                    QMessageBox.information(self.centralwidget, '消息', '导出成功！', QMessageBox.Yes)
                else:
                    pass
            else:
                raise ValueError("未选择影像")
        except Exception as e:
            QMessageBox.information(self.centralwidget, '消息', '未选择影像!', QMessageBox.Yes)

    def help(self):
        self.help_win = QMainWindow()
        self.help_win.setWindowTitle("帮助文档")
        self.help_win.setWindowIcon((QIcon('asset/icon/help.png')))
        self.help_win.resize(600,800)
        self.wv = QWebEngineView()
        self.wv.load(QUrl.fromLocalFile("E:/Desktop/mypython/PyQt5\RSIC/asset/help.html"))
        self.help_win.setCentralWidget(self.wv)
        self.help_win.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    rsic_win = RSIC_Win()
    rsic_win.show()
    sys.exit(app.exec_())
