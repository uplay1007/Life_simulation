import random

from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QFont, QBrush, QIcon, QPixmap, QColor, QPen, QPainter
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton


class CVirusTable(QTableWidget):
    def __init__(self, parent, world):
        super().__init__(parent)
        self.world = world
        self.viruses = []

        self.setColumnCount(8)
        self.setHorizontalHeaderLabels(['Name', 'Dur', 'Imm', 'Imp', 'Clr', 'CI', '', ''])
        self.horizontalHeaderItem(0).setToolTip('Name of virus')
        self.horizontalHeaderItem(1).setToolTip('Duration of illness')
        self.horizontalHeaderItem(2).setToolTip('Duration of immunity')
        self.horizontalHeaderItem(3).setToolTip('Impact from virus')
        self.horizontalHeaderItem(4).setToolTip('Color of virus')
        self.horizontalHeaderItem(5).setToolTip('Color of virus immunity')
        font = QFont()
        font.setPointSize(8)
        self.setFont(font)
        self.horizontalHeader().setMinimumSectionSize(0)
        self.horizontalHeader().setStyleSheet("""QHeaderView::section {padding: 0px; margin: 0px; border: 8px;}""")

        self.resizeColumnsToContents()
        self.setRowCount(0)

    def add_virus(self, virus):
        self.viruses.append(virus)
        ind = len(self.viruses) - 1
        self.setRowCount(ind + 1)

        self.setItem(ind, 0, QTableWidgetItem(virus.name))
        self.setItem(ind, 1, QTableWidgetItem(str(virus.duration)))
        self.setItem(ind, 2, QTableWidgetItem(str(virus.immunity)))
        self.setItem(ind, 3, QTableWidgetItem(str(virus.impact)))

        """item = QTableWidgetItem()
        item.setBackground(QBrush(virus.color))
        self.setItem(ind, 4, item)
        item1 = QTableWidgetItem()
        item1.setBackground(QBrush(virus.color_immunity))
        self.setItem(ind, 5, item1)"""

        item = QTableWidgetItem()
        item.setIcon(QIcon(self.createRectPixmap(virus.color)))
        self.setItem(ind, 4, item)
        item1 = QTableWidgetItem()
        item1.setIcon(QIcon(self.createRectPixmap(virus.color_immunity)))
        self.setItem(ind, 5, item1)

        pb1 = QPushButton()
        pb1.clicked.connect(self.attack)
        pb1.setIcon(QIcon(QPixmap('resources\\virus.svg').scaled(QSize(16, 16))))

        pb2 = QPushButton()
        pb2.clicked.connect(self.remove)
        pb2.setIcon(QIcon(QPixmap('resources\\trash (2).svg').scaled(QSize(16, 16))))

        self.setCellWidget(ind, 6, pb1)
        self.setCellWidget(ind, 7, pb2)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def createRectPixmap(self, col):
        px = QPixmap(16, 16)
        px.fill(Qt.transparent)
        pxSize = px.rect().adjusted(1, 1, -1, -1)
        painter = QPainter(px)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(col)
        painter.setPen(QPen(col, 1))
        painter.drawRect(pxSize)
        painter.end()
        return px

    def attack(self):
        vir = self.viruses[self.currentRow()]
        animals = list(filter(lambda x: x.kingdom == 'animal' and not x.has_virus(vir.name), self.world.animals))
        if len(animals) > 0:
            vir.attack(animals[random.randint(0, len(animals) - 1)])
        self.world.redraw()
        self.world.update()

    def remove(self):
        self.parent().parent().parent().remove_virus(self.viruses[self.currentRow()].name)
        del self.viruses[self.currentRow()]
        self.removeRow(self.currentRow())
