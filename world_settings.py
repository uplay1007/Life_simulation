from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QFormLayout, QSlider, QColorDialog

from superqt import QLabeledSlider, QLabeledRangeSlider

from rlsider import QLDRSlider, QLRSlider


class CWorldSettings(QWidget):
    def __init__(self, world):
        super().__init__()
        self.world = world
        self.applied = False

        self.setWindowTitle(f"Settings for {world.name}")
        self.setGeometry(800, 200, 500, 700)

        self.anim_male_color = world.anim_male_color
        self.anim_female_color = world.anim_female_color

        self.gridLayout = QtWidgets.QFormLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        # Лэйбл и поле для ширины поля
        self.l_size_x = QLabel(self)
        self.l_size_x.setText('Width:')
        self.gridLayout.setWidget(0, QFormLayout.LabelRole, self.l_size_x)

        self.le_size_x = QLineEdit(self)
        self.le_size_x.setText(str(world.size_x))
        self.gridLayout.setWidget(0, QFormLayout.FieldRole, self.le_size_x)

        # Лэйбл и поле для высоты поля
        self.l_size_y = QLabel(self)
        self.l_size_y.setText('Height:')
        self.gridLayout.setWidget(1, QFormLayout.LabelRole, self.l_size_y)

        self.le_size_y = QLineEdit(self)
        self.le_size_y.setText(str(world.size_y))
        self.gridLayout.setWidget(1, QFormLayout.FieldRole, self.le_size_y)

        # Лэйбл и поле для размера ячейки
        self.l_cell_size = QLabel(self)
        self.l_cell_size.setText('Сell size:')
        self.gridLayout.setWidget(2, QFormLayout.LabelRole, self.l_cell_size)

        self.le_cell_size = QLineEdit(self)
        self.le_cell_size.setText(str(world.cell_size))
        self.gridLayout.setWidget(2, QFormLayout.FieldRole, self.le_cell_size)

        # Границы размеров животных
        self.l_anim_size = QLabel(self)
        self.l_anim_size.setText('Animal size:')
        self.gridLayout.setWidget(3, QFormLayout.LabelRole, self.l_anim_size)

        self.sl_anim_size = QLDRSlider(Qt.Horizontal)
        self.sl_anim_size.setRange(0.5, 1.5)
        self.sl_anim_size.setValue((world.anim_size_min, world.anim_size_max))
        self.sl_anim_size.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(3, QFormLayout.FieldRole, self.sl_anim_size)

        # Границы прямолинейность животных
        self.l_anim_straight = QLabel(self)
        self.l_anim_straight.setText('Animal straight, %:')
        self.gridLayout.setWidget(4, QFormLayout.LabelRole, self.l_anim_straight)

        self.sl_anim_straight = QLRSlider(Qt.Horizontal)
        self.sl_anim_straight.setRange(1, 100)
        self.sl_anim_straight.setValue((world.anim_straight_min, world.anim_straight_max))
        self.sl_anim_straight.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(4, QFormLayout.FieldRole, self.sl_anim_straight)

        # Границы мобильности животных
        self.l_anim_mobility = QLabel(self)
        self.l_anim_mobility.setText('Animal mobility, %:')
        self.gridLayout.setWidget(5, QFormLayout.LabelRole, self.l_anim_mobility)

        self.sl_anim_mobility = QLRSlider(Qt.Horizontal)
        self.sl_anim_mobility.setRange(1, 100)
        self.sl_anim_mobility.setValue((world.anim_mobility_min, world.anim_mobility_max))
        self.sl_anim_mobility.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(5, QFormLayout.FieldRole, self.sl_anim_mobility)

        # Границы дальнозоркости животных
        self.l_anim_vision = QLabel(self)
        self.l_anim_vision.setText('Vision:')
        self.gridLayout.setWidget(6, QFormLayout.LabelRole, self.l_anim_vision)

        self.sl_anim_vision = QLRSlider(Qt.Horizontal)
        self.sl_anim_vision.setRange(1, 15)
        self.sl_anim_vision.setValue((world.anim_vision_min, world.anim_vision_max))
        self.sl_anim_vision.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(6, QFormLayout.FieldRole, self.sl_anim_vision)

        # Границы возможного максимального возраста животных
        self.l_anim_maxage = QLabel(self)
        self.l_anim_maxage.setText('Max Age:')
        self.gridLayout.setWidget(7, QFormLayout.LabelRole, self.l_anim_maxage)

        self.sl_anim_maxage = QLRSlider(Qt.Horizontal)
        self.sl_anim_maxage.setRange(1, 1000)
        self.sl_anim_maxage.setValue((world.anim_min_age, world.anim_max_age))
        self.sl_anim_maxage.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(7, QFormLayout.FieldRole, self.sl_anim_maxage)

        # Границы здоровья, % от макс возраста
        self.l_anim_health = QLabel(self)
        self.l_anim_health.setText('Helth, % of max age:')
        self.gridLayout.setWidget(8, QFormLayout.LabelRole, self.l_anim_health)

        self.sl_anim_health = QLRSlider(Qt.Horizontal)
        self.sl_anim_health.setRange(1, 100)
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
        self.sl_anim_repl.setRange(1, 1000)
        self.sl_anim_repl.setValue((world.anim_repl_age_min, world.anim_repl_age_max))
        self.sl_anim_repl.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(10, QFormLayout.FieldRole, self.sl_anim_repl)

        # Кнопа выбора цвета для мужчин
        self.l_anim_male_color = QLabel(self)
        self.l_anim_male_color.setText('Male color:')
        self.gridLayout.setWidget(20, QFormLayout.LabelRole, self.l_anim_male_color)

        self.btn_m_color = QPushButton(self)
        self.gridLayout.setWidget(20, QFormLayout.FieldRole, self.btn_m_color)
        self.btn_m_color.setStyleSheet("background-color: {}".format(QColor(world.anim_male_color).name()))
        self.btn_m_color.setText('Color')
        self.btn_m_color.clicked.connect(self.select_m_color)

        # Кнопа выбора цвета для женщин
        self.l_anim_female_color = QLabel(self)
        self.l_anim_female_color.setText('Female color:')
        self.gridLayout.setWidget(21, QFormLayout.LabelRole, self.l_anim_female_color)

        self.btn_f_color = QPushButton(self)
        self.gridLayout.setWidget(21, QFormLayout.FieldRole, self.btn_f_color)
        self.btn_f_color.setStyleSheet("background-color: {}".format(QColor(world.anim_female_color).name()))
        self.btn_f_color.setText('Color')
        self.btn_f_color.clicked.connect(self.select_f_color)

        # Энергия в появляемой еде.
        self.l_energy = QLabel(self)
        self.l_energy.setText('Meal energy size:')
        self.gridLayout.setWidget(30, QFormLayout.LabelRole, self.l_energy)

        self.sl_energy = QLRSlider(Qt.Horizontal)
        self.sl_energy.setRange(1, 100)
        self.sl_energy.setValue((world.meal_energy_min, world.meal_energy_max))
        self.sl_energy.setHandleLabelPosition(QLabeledRangeSlider.LabelPosition.LabelsBelow)
        self.gridLayout.setWidget(30, QFormLayout.FieldRole, self.sl_energy)

        # Частота появления еды, 0 - значит не появляется
        self.l_meal_freq = QLabel(self)
        self.l_meal_freq.setText('Meal frequency:')
        self.gridLayout.setWidget(31, QFormLayout.LabelRole, self.l_meal_freq)

        self.sl_meal_freq = QLabeledSlider(Qt.Horizontal)
        self.sl_meal_freq.setRange(0, 300)
        self.sl_meal_freq.setValue(world.meal_freq)
        self.gridLayout.setWidget(31, QFormLayout.FieldRole, self.sl_meal_freq)

        self.l_error = QLabel(self)
        self.gridLayout.setWidget(100, QFormLayout.FieldRole, self.l_error)
        self.l_error.setStyleSheet('color: red')
        self.l_error.setVisible(False)

        self.apply = QPushButton(self)
        self.apply.setGeometry(125, 650, 50, 30)
        self.apply.setText('Apply')
        self.apply.clicked.connect(self.applypb)

        self.cancel = QPushButton(self)
        self.cancel.setGeometry(180, 650, 50, 30)
        self.cancel.setText('Cancel')
        self.cancel.clicked.connect(self.cancelpb)

    def applypb(self):
        if self.le_size_x.text().isdigit() and self.le_size_y.text().isdigit() and self.le_cell_size.text().isdigit():
            if int(self.le_size_x.text()) > 2 and int(self.le_size_y.text()) > 2 and int(self.le_cell_size.text()) > 2:

                self.world.resize(int(self.le_size_x.text()), int(self.le_size_y.text()), int(self.le_cell_size.text()))

                self.world.anim_size_min = self.sl_anim_size.value()[0]
                self.world.anim_size_max = self.sl_anim_size.value()[1]

                self.world.anim_straight_min = self.sl_anim_straight.value()[0]
                self.world.anim_straight_max = self.sl_anim_straight.value()[1]

                self.world.anim_mobility_min = self.sl_anim_mobility.value()[0]
                self.world.anim_mobility_max = self.sl_anim_mobility.value()[1]

                self.world.anim_vision_min = self.sl_anim_vision.value()[0]
                self.world.anim_vision_max = self.sl_anim_vision.value()[1]

                self.world.anim_min_age = self.sl_anim_maxage.value()[0]
                self.world.anim_max_age = self.sl_anim_maxage.value()[1]

                self.world.anim_health_min = self.sl_anim_health.value()[0]
                self.world.anim_health_max = self.sl_anim_health.value()[1]

                self.world.anim_male_color = self.anim_male_color
                self.world.anim_female_color = self.anim_female_color

                self.world.anim_gender_bal = self.sl_anim_gender_bal.value()

                self.world.anim_repl_age_min = self.sl_anim_repl.value()[0]
                self.world.anim_repl_age_max = self.sl_anim_repl.value()[1]

                self.world.meal_energy_min = self.sl_energy.value()[0]
                self.world.meal_energy_max = self.sl_energy.value()[1]

                self.world.meal_freq = self.sl_meal_freq.value()

                self.applied = True
                self.close()
            else:
                self.l_error.setText('Too low size: must be greater then 2')
                self.l_error.setVisible(True)
        else:
            self.l_error.setText('Invalid format: must be integers')
            self.l_error.setVisible(True)

    def cancelpb(self):
        self.applied = False
        self.close()

    def select_m_color(self):
        self.anim_male_color = QColorDialog().getColor()
        self.btn_m_color.setStyleSheet("background-color: {}".format(self.anim_male_color.name()))

    def select_f_color(self):
        self.anim_female_color = QColorDialog().getColor()
        self.btn_f_color.setStyleSheet("background-color: {}".format(self.anim_female_color.name()))
