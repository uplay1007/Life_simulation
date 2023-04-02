from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem


class CVirus:
    def __init__(self, name, duration, immunity, impact, color, color_immunity, parent=None):
        self.name = name
        self.duration = duration
        self.immunity = immunity
        self.impact = impact
        self.color = color
        self.color_immunity = color_immunity
        self.age = 0
        self.inf_gen = -1
        self.max_age = self.duration + self.immunity
        self.parent = parent

        self.brush = QBrush(self.color)
        self.immunity_brush = QBrush(self.color_immunity)
        self.pen = QPen(Qt.gray, 0.1, Qt.SolidLine)

        self.body = QGraphicsEllipseItem()
        self.body.setBrush(self.brush)
        self.body.setPen(self.pen)

        if self.parent:
            self.body.setParentItem(self.parent)
            self.parent.viruses.append(self)
            if self.parent.world.generation == 0:
                self.inf_gen = -1
            else:
                self.inf_gen = self.parent.world.generation

    def next_gen(self):
        if self.age >= self.max_age:
            self.kill()
        elif self.age <= self.duration:
            self.parent.damage(self.impact)
        else:
            self.body.setBrush(self.immunity_brush)
        self.age += 1

    def kill(self):
        if self.parent:
            self.parent.removeFromGroup(self.body)
            del self.parent.viruses[self.parent.viruses.index(self)]
        # self.parent.redraw()
        del self

    def attack(self, target):
        if not target.has_virus(self.name):
            CVirus(self.name, self.duration, self.immunity, self.impact, self.color, self.color_immunity, target)
            # target.redraw()
