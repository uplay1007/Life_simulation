import random

from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsEllipseItem
from PyQt5.QtCore import Qt


class CObject(QGraphicsItemGroup):
    def __init__(self, x, y, world, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y
        self.age = 0
        self.world = world
        self.world.addItem(self)
        self.world.animals.append(self)
        self.world.animals_cache[self.x][self.y].append(self)

    def kill(self):
        del self.world.animals[self.world.animals.index(self)]
        del self.world.animals_cache[self.x][self.y][self.world.animals_cache[self.x][self.y].index(self)]
        self.world.removeItem(self)
        for item in self.childItems():
            self.removeFromGroup(item)
        del self

    def next_gen(self):
        self.age += 1

    def redraw(self):
        pass

    def move(self, x, y):
        del self.world.animals_cache[self.x][self.y][self.world.animals_cache[self.x][self.y].index(self)]
        self.x = x
        self.y = y
        self.world.animals_cache[self.x][self.y].append(self)
        # self.redraw()
