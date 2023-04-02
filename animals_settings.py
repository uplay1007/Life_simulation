from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QFormLayout, QSlider, QSpinBox
from superqt import QLabeledRangeSlider, QLabeledSlider

from rlsider import QLDRSlider, QLRSlider


class CAnimalSettings(QWidget):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.applied = False
        self.anim_num = 100
        self.anim_size_min = 0.5
        self.anim_size_max = 1.5
        self.anim_gender_bal = 50
        self.anim_mobility_min = 50
        self.anim_mobility_max = 100
        self.anim_straight_min = 1
        self.anim_straight_max = 100
        self.anim_min_age = 100
        self.anim_max_age = 300
        self.anim_male_color = Qt.blue
        self.anim_female_color = Qt.magenta

        self.setWindowTitle('Settings')
        self.setGeometry(800, 600, 380, 400)

        self.gridLayout = QtWidgets.QFormLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Кол-во животных
        self.l_num_anim = QLabel(self)
        self.l_num_anim.setText('Quantity of animals:')
        self.gridLayout.setWidget(0, QFormLayout.LabelRole, self.l_num_anim)

        self.sb_num_anim = QSpinBox(self)
        self.sb_num_anim.setMaximum(99999)
        self.sb_num_anim.setValue(100)
        self.gridLayout.setWidget(0, QFormLayout.FieldRole, self.sb_num_anim)

        # Границы прямолинейность животных
        self.l_anim_straight = QLabel(self)
        self.l_anim_straight.setText('Animal straight, %:')
        self.gridLayout.setWidget(4, QFormLayout.LabelRole, self.l_anim_straight)

        self.sl_anim_straight = QLRSlider(Qt.Horizontal)
        if world.anim_straight_min == world.anim_straight_max:
            self.sl_anim_straight.setRange(1, 100)
            self.sl_anim_straight.setValue((world.anim_straight_min, world.anim_straight_max))
            self.sl_anim_straight.setDisabled(True)
        else:
            self.sl_anim_straight.setRange(world.anim_straight_min, world.anim_straight_max)
            self.sl_anim_straight.setValue((world.anim_straight_min, world.anim_straight_max))
        self.sl_anim_straight.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(4, QFormLayout.FieldRole, self.sl_anim_straight)

        # Границы мобильности животных
        self.l_anim_mobility = QLabel(self)
        self.l_anim_mobility.setText('Animal mobility, %:')
        self.gridLayout.setWidget(5, QFormLayout.LabelRole, self.l_anim_mobility)

        self.sl_anim_mobility = QLRSlider(Qt.Horizontal)
        if world.anim_mobility_min == world.anim_mobility_max:
            self.sl_anim_mobility.setRange(1, 100)
            self.sl_anim_mobility.setValue((world.anim_mobility_min, world.anim_mobility_max))
            self.sl_anim_mobility.setDisabled(True)
        else:
            self.sl_anim_mobility.setRange(world.anim_mobility_min, world.anim_mobility_max)
            self.sl_anim_mobility.setValue((world.anim_mobility_min, world.anim_mobility_max))
        self.sl_anim_mobility.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(5, QFormLayout.FieldRole, self.sl_anim_mobility)

        # Границы дальнозоркости животных
        self.l_anim_vision = QLabel(self)
        self.l_anim_vision.setText('Vision:')
        self.gridLayout.setWidget(6, QFormLayout.LabelRole, self.l_anim_vision)

        self.sl_anim_vision = QLRSlider(Qt.Horizontal)
        if world.anim_vision_min == world.anim_vision_max:
            self.sl_anim_vision.setRange(1, 15)
            self.sl_anim_vision.setValue((world.anim_vision_min, world.anim_vision_max))
            self.sl_anim_vision.setDisabled(True)
        else:
            self.sl_anim_vision.setRange(world.anim_vision_min, world.anim_vision_max)
            self.sl_anim_vision.setValue((world.anim_vision_min, world.anim_vision_max))
        self.sl_anim_vision.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(6, QFormLayout.FieldRole, self.sl_anim_vision)

        # Границы возможного максимального возраста животных
        self.l_anim_maxage = QLabel(self)
        self.l_anim_maxage.setText('Max Age:')
        self.gridLayout.setWidget(7, QFormLayout.LabelRole, self.l_anim_maxage)

        self.sl_anim_maxage = QLRSlider(Qt.Horizontal)
        if world.anim_min_age == world.anim_max_age:
            self.sl_anim_maxage.setRange(1, 1000)
            self.sl_anim_maxage.setValue((world.anim_min_age, world.anim_max_age))
            self.sl_anim_maxage.setDisabled(True)
        else:
            self.sl_anim_maxage.setRange(world.anim_min_age, world.anim_max_age)
            self.sl_anim_maxage.setValue((world.anim_min_age, world.anim_max_age))
        self.sl_anim_maxage.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(7, QFormLayout.FieldRole, self.sl_anim_maxage)

        # Границы здоровья, % от макс возраста
        self.l_anim_health = QLabel(self)
        self.l_anim_health.setText('Helth, % of max age:')
        self.gridLayout.setWidget(8, QFormLayout.LabelRole, self.l_anim_health)

        self.sl_anim_health = QLRSlider(Qt.Horizontal)
        if world.anim_health_min == world.anim_health_max:
            self.sl_anim_health.setRange(1, 100)
            self.sl_anim_health.setValue((world.anim_health_min, world.anim_health_max))
            self.sl_anim_health.setDisabled(True)
        else:
            self.sl_anim_health.setRange(world.anim_health_min, world.anim_health_max)
            self.sl_anim_health.setValue((world.anim_health_min, world.anim_health_max))
        self.sl_anim_health.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(8, QFormLayout.FieldRole, self.sl_anim_health)

        # Гендерный баланс
        self.l_anim_gender_bal = QLabel(self)
        self.l_anim_gender_bal.setText('Gender balance:')
        self.gridLayout.setWidget(9, QFormLayout.LabelRole, self.l_anim_gender_bal)

        self.sl_anim_gender_bal = QLabeledSlider(Qt.Horizontal)
        self.sl_anim_gender_bal.setRange(0, 100)
        self.sl_anim_gender_bal.setValue(world.anim_gender_bal)
        self.gridLayout.setWidget(9, QFormLayout.FieldRole, self.sl_anim_gender_bal)

        # Возраст через который возможна следующая репликация
        self.l_anim_repl = QLabel(self)
        self.l_anim_repl.setText('Period of replication:')
        self.gridLayout.setWidget(10, QFormLayout.LabelRole, self.l_anim_repl)

        self.sl_anim_repl = QLRSlider(Qt.Horizontal)
        if world.anim_repl_age_min == world.anim_repl_age_max:
            self.sl_anim_repl.setRange(1, 1000)
            self.sl_anim_repl.setValue((world.anim_repl_age_min, world.anim_repl_age_max))
            self.sl_anim_repl.setDisabled(True)
        else:
            self.sl_anim_repl.setRange(world.anim_repl_age_min, world.anim_repl_age_max)
            self.sl_anim_repl.setValue((world.anim_repl_age_min, world.anim_repl_age_max))
        self.sl_anim_repl.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(10, QFormLayout.FieldRole, self.sl_anim_repl)

        self.apply = QPushButton(self)
        self.apply.setGeometry(175, 360, 50, 30)
        self.apply.setText('Apply')
        self.apply.clicked.connect(self.applypb)
        self.cancel = QPushButton(self)
        self.cancel.setGeometry(230, 360, 50, 30)
        self.cancel.setText('Cancel')
        self.cancel.clicked.connect(self.cancelpb)

    def applypb(self):
        self.world.generate_random_animals(int(self.sb_num_anim.text()),
                                           self.sl_anim_repl.value(),
                                           self.sl_anim_health.value(),
                                           self.sl_anim_maxage.value(),
                                           self.sl_anim_gender_bal.value(),
                                           self.sl_anim_mobility.value(),
                                           self.sl_anim_straight.value(),
                                           self.sl_anim_vision.value()
                                           )
        self.applied = True
        self.close()

    def cancelpb(self):
        self.applied = False
        self.close()
