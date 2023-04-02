from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsItemGroup
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt


class CGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

    def wheelEvent(self, event):
        super(CGraphicsView, self).wheelEvent(event)
        if event.angleDelta().y() > 0:
            self.scale(1.25, 1.25)
        else:
            self.scale(0.75, 0.75)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.__prevMousePos = event.pos()
        else:
            super(CGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            offset = self.__prevMousePos - event.pos()
            self.__prevMousePos = event.pos()

            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
            self.scene().update()
        else:
            super(CGraphicsView, self).mouseMoveEvent(event)



class CGraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qpen = QPen(Qt.black, 0.3, Qt.SolidLine)
        self.grid = None

    def create_grid(self, size_x, size_y, cell_size):
        if not self.grid:
            self.grid = QGraphicsItemGroup()
            self.addItem(self.grid)
        else:
            for item in self.grid.childItems():
                self.grid.removeFromGroup(item)
        for i in range(size_x + 1):
            line = QGraphicsLineItem(i * cell_size, 0, i * cell_size, size_y * cell_size, self.grid)
            line.setPen(self.qpen)
        for i in range(size_y + 1):
            line = QGraphicsLineItem(0, i * cell_size, size_x * cell_size, i * cell_size, self.grid)
            line.setPen(self.qpen)
