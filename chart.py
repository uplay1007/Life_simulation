from pyqtgraph import PlotWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen


class CChart(PlotWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.window_x = 200
        self.setBackground('w')
        self.pen = QPen(Qt.darkBlue, 1, Qt.SolidLine)
        self.x = [0]
        self.y = [0]

        self.data_line = self.plot(self.x, self.y, pen=self.pen)

        self.setXRange(max(min(self.x), max(max(self.x), 100) - self.window_x), max(max(self.x), 100), update=True)
        self.setYRange(0, max(max(self.y), 30))

    def clear_chart(self):
        # self.x.clear()
        # self.y.clear()
        self.x = [0]
        self.y = [0]

        # self.data_line = self.plot(self.x, self.y, pen=self.pen)
        self.data_line.setData(self.x, self.y)
        self.setXRange(max(min(self.x), max(max(self.x), 100) - self.window_x), max(max(self.x), 100), update=True)
        self.setYRange(0, max(max(self.y), 30))

    def append(self, dot):
        if len(self.x) <= self.window_x * 3:
            pass
        else:
            del self.x[0]
            del self.y[0]

        self.x.append(self.x[-1] + 1)
        self.y.append(dot)

        self.data_line.setData(self.x, self.y)
        self.setXRange(max(min(self.x), max(max(self.x), 100) - self.window_x), max(max(self.x), 100), update=True)
        self.setYRange(0, max(max(self.y), 30))
