import pyqtgraph as pg
from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor


class CGist(PlotWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_x = 200
        self.setBackground('w')
        self.pen = QPen(Qt.darkBlue, 1, Qt.SolidLine)
        self.x = []
        self.y = []

        self.bargraph = pg.BarGraphItem(x=self.x, height=self.y, width=10, brush=QBrush(QColor(Qt.blue)))
        self.addItem(self.bargraph)

        self.y = [3, 1, 2]
        # self.bargraph.setOpts(x=self.x,height=self.y)

    def clear_chart(self):
        self.x = [0]
        self.y = [0]
        self.bargraph.setOpts(x=self.x, height=self.y, width=10)

        # self.bargraph = pg.BarGraphItem(x=self.x, height=self.y, width=10, brush=QBrush(QColor(Qt.blue)))

        # self.data_line = self.plot(self.x, self.y, pen=self.pen)

    def setdata(self, x, y, w):
        self.x = x
        self.y = y
        self.bargraph.setOpts(x=self.x, height=self.y, width=w)
