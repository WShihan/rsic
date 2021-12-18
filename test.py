import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import (QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()

    scene.addLine(20, 20, 200, 200)
    scene.addText('Hello Graphics View')
    scene.addRect(0, 0, 320, 240)
    scene.addEllipse(100, 100, 100, 100)

    rect = QGraphicsRectItem(99, 99, 102, 102)
    rect.setPen(QPen(Qt.red))
    scene.addItem(rect)

    view = QGraphicsView(scene)
    view.setWindowTitle('实战PyQt5: 图形视图 演示!')
    view.resize(480, 320)
    view.show()

    sys.exit(app.exec())
