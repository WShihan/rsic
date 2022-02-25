# -*- coding: utf-8 -*-
"""
@Date: 2022/2/6
@Author:Wang Shihan
"""
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from RSIC.utils import Chart, Tiff2array, Exporter, Classify_Diaglog
from RSIC.UI import Ui_MainWindow


class RSIC_Win(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RSIC_Win, self).__init__()
        self.file_name = None
        self.set_ui()

    def set_ui(self):
        self.setupUi(self)
        # 窗体初始化
        self.resize(1600, 900)
        self.setWindowTitle("RSIC")
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
        self.btn_classify.clicked.connect(self.classify)

    def get_file(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "选择影像", r'E:/Desktop/GisFile/',
                                                       '*.tif;;*.jpg;;*.jpeg;;*.png;;*.img')
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

    @staticmethod
    def show_chart(data):
        """
        :param data: 影像矩阵数据
        :return:
        """
        chart = Chart(data)
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
            QMessageBox.information(self.centralwidget, '消息', '选择影响错误：' + str(e), QMessageBox.Yes)

    def help(self):
        self.help_win = QMainWindow()
        self.help_win.setWindowTitle("帮助文档")
        self.help_win.setWindowIcon((QIcon('asset/icon/help.png')))
        self.help_win.resize(600, 800)
        self.wv = QWebEngineView()
        self.wv.load(
            QUrl.fromLocalFile(r"E:/Desktop/mypython/PyQt5\RSIC/asset/help.html")
        )
        self.help_win.setCentralWidget(self.wv)
        self.help_win.show()

    def classify(self):
        if self.file_name:
            self.dilog = Classify_Diaglog(self.file_name)
        else:
            self.dilog = Classify_Diaglog()
        self.dilog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rsic_win = RSIC_Win()
    rsic_win.show()
    sys.exit(app.exec_())
