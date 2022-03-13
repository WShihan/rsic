# -*- coding: utf-8 -*-
"""
@Date: 2021/12/25
@Author:Wang Shihan
"""
import matplotlib as mpl
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from osgeo import gdal
import numpy as np
from PIL import Image
from RSIC.My_dialog import Ui_MainWindow as Mydialog
from RSIC.classify import K_Means, RfC



# ============================类=============================
mpl.rcParams['font.family'] = "SimHei"
# matplotlib 画布类
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=16, height=9, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(fig)


# ==========在PyQt中展示Mpl的基类==============
class QtMpl(QWidget):
    def __init__(self):
        super(QtMpl, self).__init__()
        self.setGeometry(500, 100,1000, 750)
        self.set_ui()

    def set_ui(self):
        self.canvas = MplCanvas()
        self.tool_bar = NavigationToolbar(self.canvas, self)
        self.frame = QVBoxLayout()
        self.frame.addWidget(self.tool_bar)
        self.frame.addWidget(self.canvas)
        self.setLayout(self.frame)

    def plot(self, **kwargs):
        pass

# ===================统计表类===========================
class Chart(QtMpl):
    def __init__(self, data):
        super(Chart, self).__init__()
        self.setWindowTitle("统计分析")
        self.setWindowIcon(QIcon('asset/icon/histogram.png'))
        self.setGeometry(500, 100,1000, 750)
        self.setup_ui()
        self.data = data

    def setup_ui(self):
        self.plot(flag="init")
        self.btn_hist = QPushButton('DN直方图')
        self.btn_hist.clicked.connect(
            lambda: self.plot(data=self.data, flag="hist", bins=256, rwidth=0.8, density=True))
        self.btn_line = QPushButton("散点图")
        self.btn_line.clicked.connect(lambda: self.plot(data=self.data, flag="scatter"))
        self.btn_line.setMaximumSize(80, 50)
        self.btn_hist.setMaximumSize(80, 50)

        # 添加按钮
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_hist)
        btn_layout.addWidget(self.btn_line)

        self.frame.addLayout(btn_layout)

    def plot(self, data=None, flag=None, **kwargs):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        try:
            if flag == "hist":
                ax.hist(data, bins=kwargs['bins'], rwidth=kwargs['rwidth'])
                ax.set_title("像元分布直方图", fontsize=20, pad=15)
                ax.set_xlabel("DN", fontsize=15, labelpad=10)
                ax.set_ylabel("频率", fontsize=15, labelpad=10)
            elif flag == "scatter":
                ax.plot(data, ".k", markersize=0.1)
                max_v = max(data)
                ax.set_ylim(0, max_v + max_v * 0.3)
            elif flag == "line":
                ax.plot(data, "-.k", label="line")
                max_v = max(data)
                ax.set_ylim(0, max_v + max_v * 0.3)
            elif flag == "init":
                img = Image.open(r'E:\Desktop\mypython\PyQt5\RSIC\asset\image\LUCC_Asia.jpeg')
                ax.imshow(img)
                # 隐藏刻度线和标签
                ax.set_yticks([])
                ax.set_xticks([])
                # 隐藏坐标轴
                ax.axis('off')
            self.canvas.draw()
        except Exception as e:
            print(e)

# 图片展示类
class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0
    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)

# 获取影像数组
class Tiff2array(QThread):
    singal = QtCore.pyqtSignal(np.ndarray)
    def __init__(self, file):
        super(Tiff2array, self).__init__()
        self.file = file
    def run(self):
        img = gdal.Open(self.file, gdal.GA_ReadOnly)
        arr = img.GetRasterBand(1).ReadAsArray()
        del img
        self.singal.emit(arr.flatten())

class Exporter(QThread):
    def __init__(self,scene, fname):
        super(Exporter, self).__init__()
        self.fname = fname
        self.scene = scene
    def run(self):
        try:
            rect = self.scene.sceneRect()
            pixmap = QImage(rect.height(), rect.width(), QImage.Format_ARGB32_Premultiplied)
            painter = QPainter(pixmap)
            rectf = QRectF(0, 0, pixmap.rect().height(), pixmap.rect().width())
            self.scene.render(painter, rectf, rect)
            pixmap.save(self.fname)
            painter.end()
        except Exception as e:
            print(e)

# ====================分类窗口======================
class Classify_Diaglog(QMainWindow, Mydialog):
    def __init__(self, origin_file=None):
        self.origin_file = origin_file
        super(Classify_Diaglog, self).__init__()
        self.setWindowIcon(QIcon('asset/icon/classify.png'))
        self.setupUi(self)
        self.setWindowTitle("地物分类")
        self.new_tab = QTabWidget(self.tw)

        self.set_func()

    def set_func(self):
        if self.origin_file:
            self.le_input.setText(self.origin_file)
        self.btn_input.clicked.connect(lambda :self.fill_form("btn_input"))
        self.btn_out.clicked.connect(lambda :self.fill_form("btn_out"))
        self.btn_input_rfc.clicked.connect(lambda :self.fill_form("btn_input_rfc"))
        self.btn_train.clicked.connect(lambda :self.fill_form("btn_train"))
        self.btn_out_rfc.clicked.connect(lambda :self.fill_form("btn_out_rfc"))
        self.btn_ok_rfc.clicked.connect(lambda : self.start(which=0))
        self.btn_ok.clicked.connect(lambda :self.start(which=1))
        self.tb_km.setText("k均值聚类算法是一种迭代求解的聚类分析算法，其步骤是，预将数据分为K组，则随机"
                           "选取K个对象作为初始的聚类中心，然后计算每个对象与各个种子聚类中心之间的距离，把每个对象分配给距离它最近的聚类中心。聚"
                           "类中心以及分配给它们的对象就代表一个聚类。每分配一个样本，聚类的聚类中心会根据聚类中现有的对象被重新计算。这个过程将不断"
                           "重复直到满足某个终止条件。终止条件可以是没有（或最小数目）对象被重新分配给不同的聚类，没有（或最小数目）聚类中心再发生变化"
                           "，误差平方和局部最小。"
                           )
        self.tb_rfc.setText("""随机森林分类器是一种由很多决策树分类模型组成的集成分类器模型.该分类器对参数不敏感，不易过拟合，训练速度快，比较适合多分类问题""")

    def fill_form(self, which):
        if which == "btn_input":
            file_name = file_getter(self)
            if file_name:
                self.le_input.setText(file_name)
            else:
                pass
        elif which == "btn_out":
            file_name = file_saver(self)
            if file_name:
                self.le_out.setText(file_name)
            else:
                pass
        elif which == "btn_input_rfc":
            file_name = file_getter(self)
            if file_name:
                self.le_input_rfc.setText(file_name)
            else:
                pass
        elif which == "btn_train":
            file_name = file_getter(self)
            if file_name:
                self.le_train.setText(file_name)
            else:
                pass
        elif which == "btn_out_rfc":
            file_name = file_saver(self)
            if file_name:
                self.le_out_rfc.setText(file_name)
            else:
                pass


    def start(self, which):
        try:
            if which:
                if self.origin_file:
                    out_file = self.origin_file
                else:
                    out_file = self.le_out.text()
                file_name = self.le_input.text()
                iter_n = self.le_iter.text()
                count = self.le_count.text()
                if file_name and out_file:
                    self.km = K_Means(img_file=file_name, count_n=int(count), iter_n=int(iter_n), out_file=out_file)
                    self.km.sig_cluster.connect(self.draw)
                    self.km.start()
                else:
                    raise ValueError("文件错误！")
            else:
                file_input = self.le_input_rfc.text()
                file_train = self.le_train.text()
                file_out = self.le_out_rfc.text()
                #print(file_train, file_out, file_input)
                self.r_tree = RfC(file_input, file_out, file_train)
                self.r_tree.signal.connect(self.collect_msg)
                self.r_tree.sig_cls.connect(self.draw)
                self.r_tree.start()

        except Exception as e:
            print(str(e))
    def collect_msg(self, s):
        self.tb_res_rfc.append(s)

    def draw(self, cls):
        self.post_win = PostClassification()
        self.post_win.plot(cls)
        self.post_win.show()

# =================打开文件和保存文件函数====================
def file_getter(self):
    try:
        file_name, _ = QFileDialog.getOpenFileName(self, "选择影像", r'E:\Desktop\mypython\PyQt5\RSIC\asset\res',
                                                   '*.tif;;*.jpg;;*.jpeg;;*.png;;*.img;;*.shp')
        if file_name:
            self.file_name = file_name
            return file_name
    except Exception as e:
        print("Select file failed!" + str(e))

def file_saver(self):
    try:
        save_name, ftype = QFileDialog.getSaveFileName(self.centralwidget, '导出为', 'E:/Desktop',
                                                   "*.tif;;*.png;;*.jpg")
        if save_name:
            return save_name
        else:
            pass
    except Exception as e:
        QMessageBox.information(self.centralwidget, '消息', '选择影响错误：' + str(e), QMessageBox.Yes)

#======================遥感分类后处理=========================
class PostClassification(QtMpl):
    def __init__(self):
        super(PostClassification, self).__init__()
        self.setWindowTitle("分类结果")
        self.setWindowIcon(QIcon('asset/icon/classify.png'))

    def plot(self, data):
        self.canvas.figure.clear()
        ax  = self.canvas.figure.add_subplot(111)
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.imshow(data)
        self.canvas.draw()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    c = Chart(list(range(10)))
    c.plot()
    c.show()
    sys.exit(app.exec_())
