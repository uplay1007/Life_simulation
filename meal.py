import random

from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem, QGraphicsRectItem
from PyQt5.QtCore import Qt

from object import CObject


class CMeal(CObject):
    def __init__(self, x, y, energy, world, kingdom='plant', parent=None):
        super().__init__(x, y, world, parent)
        self.kingdom = kingdom

        self.energy = energy
        self.pen = QPen(Qt.gray, 0.1, Qt.SolidLine)

        if self.kingdom == 'plant':
            self.brush = QBrush(Qt.green)
        else:
            self.brush = QBrush(Qt.darkGray)

        self.body = QGraphicsRectItem()
        self.addToGroup(self.body)
        self.body.setBrush(self.brush)
        self.body.setPen(self.pen)

        self.redraw()

    def redraw(self):
        s = self.world.cell_size
        self.body.setRect(-s / 2, -s / 2, s, s)
        self.setPos(self.x * s + s / 2, self.y * s + s / 2)
        self.setScale(0.5)

    def next_gen(self):
        # if self.age >= 10:
        #    self.kill()
        #    return
        self.age += 1
