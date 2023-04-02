import sys
import sqlite3
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QEventLoop, QRectF

from Gist import CGist
from custom_view import CGraphicsView
from world_settings import CWorldSettings
from world import CWorld
from virus import CVirus
from chart import CChart
from virus_table import CVirusTable
from virus_settings import CVirusSettings
from animals_settings import CAnimalSettings
from PyQt5.QtWidgets import QGraphicsView

from itertools import groupby


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dbname = 'sim.db'

        self.current_speed = 100

        self.animals_wind = None

        self.setObjectName("MainWindow")
        self.resize(1280, 920)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setMinimumSize(QtCore.QSize(1024, 600))
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(300, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")

        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.graphicsView = CGraphicsView(self.frame_2)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setViewportUpdateMode(QGraphicsView.NoViewportUpdate)
        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.horizontalLayout.addWidget(self.frame_2)

        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 1, 1, 1)

        self.setCentralWidget(self.centralwidget)

        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.actionNewWorld = QtWidgets.QAction(self)
        self.actionNewWorld.setObjectName("actionNewWorld")

        self.actionStart = QtWidgets.QAction(self)
        self.actionStart.setObjectName("actionStart")

        self.actionStop = QtWidgets.QAction(self)
        self.actionStop.setObjectName("actionStop")

        self.actionOne_step = QtWidgets.QAction(self)
        self.actionOne_step.setObjectName("actionOne_step")

        self.actionGenerate = QtWidgets.QAction(self)
        self.actionGenerate.setObjectName("actionGenerate")

        self.actionClear = QtWidgets.QAction(self)
        self.actionClear.setObjectName("actionClear")

        self.actionFit = QtWidgets.QAction(self)
        self.actionFit.setObjectName("actionFit")

        self.actionSize_in = QtWidgets.QAction(self)
        self.actionSize_in.setObjectName("actionSize_in")

        self.actionSize_out = QtWidgets.QAction(self)
        self.actionSize_out.setObjectName("actionSize_out")

        self.actionDrop = QtWidgets.QComboBox(self)
        self.actionDrop.setObjectName('actionDrop')
        self.actionDrop.addItems(['Fastest', 'Fast', 'Medium', 'Slow'])
        self.actionDrop.setCurrentIndex(1)
        self.actionDrop.currentTextChanged.connect(self.change_spped)

        self.actionVirus = QtWidgets.QAction(self)
        self.actionVirus.setObjectName("actionVirus")

        self.actionAnimals = QtWidgets.QAction(self)
        self.actionAnimals.setObjectName("actionAnimals")

        self.actionWorldDefault = QtWidgets.QAction(self)
        self.actionWorldDefault.setObjectName("Default")
        self.actionWorldDefault.setText("Default")

        self.actionWorldSmall = QtWidgets.QAction(self)
        self.actionWorldSmall.setObjectName("Default")
        self.actionWorldSmall.setText("Small")

        self.actionWorldMedium = QtWidgets.QAction(self)
        self.actionWorldMedium.setObjectName("Default")
        self.actionWorldMedium.setText("Medium")

        self.actionWorldLarge = QtWidgets.QAction(self)
        self.actionWorldLarge.setObjectName("Default")
        self.actionWorldLarge.setText("Large")


        self.toolBar.addAction(self.actionNewWorld)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionGenerate)
        self.toolBar.addAction(self.actionAnimals)
        self.toolBar.addAction(self.actionClear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionOne_step)
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addWidget(self.actionDrop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionFit)
        self.toolBar.addAction(self.actionSize_in)
        self.toolBar.addAction(self.actionSize_out)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionVirus)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionWorldDefault)
        self.toolBar.addAction(self.actionWorldSmall)
        self.toolBar.addAction(self.actionWorldMedium)
        self.toolBar.addAction(self.actionWorldLarge)

        self.setWindowTitle("LIFE SIMULATION")
        self.toolBar.setWindowTitle("toolBar")
        self.actionNewWorld.setToolTip("parameters of world")
        self.actionStart.setToolTip("start simulation")
        self.actionStop.setToolTip("stop simulation")
        self.actionOne_step.setToolTip("one step of simulation")
        self.actionGenerate.setToolTip("Generate animals (quick 100)")
        self.actionAnimals.setToolTip("Generate animals (custom)...")
        self.actionClear.setToolTip("clear the world")
        self.actionFit.setToolTip("fit world to the screen")
        self.actionVirus.setToolTip("Add virus strain")
        self.actionSize_in.setToolTip("zoom in")
        self.actionSize_out.setToolTip("zoom out")
        self.actionNewWorld.setIcon(QIcon('resources\\gear-fill.svg'))
        self.actionStart.setIcon(QIcon('resources\\play-circle-fill.svg'))
        self.actionStop.setIcon(QIcon('resources\\pause-circle-fill.svg'))
        self.actionOne_step.setIcon(QIcon('resources\\skip-end-circle-fill.svg'))
        self.actionGenerate.setIcon(QIcon('resources\\recycle.svg'))
        self.actionClear.setIcon(QIcon('resources\\trash (2).svg'))
        self.actionFit.setIcon(QIcon('resources\\arrows-fullscreen.svg'))
        self.actionSize_in.setIcon(QIcon('resources\\plus-square.svg'))
        self.actionSize_out.setIcon(QIcon('resources\\dash-square.svg'))
        self.actionVirus.setIcon(QIcon('resources\\virus.svg'))
        self.actionAnimals.setIcon(QIcon('resources\\piggy-bank-fill.svg'))

        self.actionNewWorld.triggered.connect(self.settings)
        self.actionFit.triggered.connect(self.fit_world)
        self.actionOne_step.triggered.connect(self.next_gen)
        self.actionStart.triggered.connect(self.start_play)
        self.actionStop.triggered.connect(self.stop_play)
        self.actionSize_in.triggered.connect(self.size_in)
        self.actionSize_out.triggered.connect(self.size_out)
        self.actionGenerate.triggered.connect(self.generate_world)
        self.actionClear.triggered.connect(self.clear_world)
        self.actionVirus.triggered.connect(self.virus_settings)
        self.actionAnimals.triggered.connect(self.animals_settings)

        self.world = CWorld(self.dbname)
        self.graphicsView.setScene(self.world)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.next_gen)

        self.statusbar = self.statusBar()
        self.num_cells = QLabel(self)
        self.num_cells.setText('Quantity of animals: ')
        self.statusbar.addPermanentWidget(self.num_cells)
        self.num_animals = QLineEdit(self)
        self.statusbar.addPermanentWidget(self.num_animals)
        self.num_animals.setEnabled(False)

        self.num_males = QLabel(self)
        self.num_males.setText('Quantity of males: ')
        self.statusbar.addPermanentWidget(self.num_males)
        self.num_males1 = QLineEdit(self)
        self.statusbar.addPermanentWidget(self.num_males1)
        self.num_males1.setEnabled(False)

        self.num_females = QLabel(self)
        self.num_females.setText('Quantity of females: ')
        self.statusbar.addPermanentWidget(self.num_females)
        self.num_females1 = QLineEdit(self)
        self.statusbar.addPermanentWidget(self.num_females1)
        self.num_females1.setEnabled(False)

        self.num_gener = QLabel(self)
        self.num_gener.setText('Generation: ')
        self.statusbar.addPermanentWidget(self.num_gener)
        self.num_gener1 = QLineEdit(self)
        self.statusbar.addPermanentWidget(self.num_gener1)
        self.num_gener1.setEnabled(False)

        self.num_ill = QLabel(self)
        self.num_ill.setText('Num of sick: ')
        self.statusbar.addPermanentWidget(self.num_ill)
        self.num_ill1 = QLineEdit(self)
        self.statusbar.addPermanentWidget(self.num_ill1)
        self.num_ill1.setEnabled(False)

        self.table_of_viruses = QLabel(self.frame)
        self.table_of_viruses.setText('Avaible viruses')
        self.table_of_viruses.move(10, 5)

        self.virus_table = CVirusTable(self.frame, self.world)
        self.virus_table.setGeometry(0, 20, 300, 200)
        self.load_viruses()

        self.total_anim = QLabel(self.frame)
        self.total_anim.setText('Total number of animals')
        self.total_anim.move(10, 225)

        self.chart1 = CChart(self.frame)
        self.chart1.setGeometry(0, 240, 300, 200)

        self.total_virused = QLabel(self.frame)
        self.total_virused.setText('Total number of infected animals')
        self.total_virused.move(10, 445)

        self.chart2 = CChart(self.frame)
        self.chart2.setGeometry(0, 460, 300, 200)

        self.l_stat = QLabel(self.frame)
        self.l_stat.setText('Distribution')
        self.l_stat.move(10, 665)

        self.gist = CGist(self.frame)
        self.gist.setGeometry(0, 685, 300, 200)

        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(180, 665, 120, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(('Mobility', 'Straightness', 'Vision', 'Max Age', 'Age', 'Health'))
        self.comboBox.currentTextChanged.connect(self.onGistSelect)

        self.nums()

        self.actionWorldDefault.triggered.connect(lambda: self.load_world_settings("Default"))
        self.actionWorldSmall.triggered.connect(lambda: self.load_world_settings("Small"))
        self.actionWorldMedium.triggered.connect(lambda: self.load_world_settings("Medium"))
        self.actionWorldLarge.triggered.connect(lambda: self.load_world_settings("Large"))

    def load_world_settings(self, name="Default"):
        self.world.load_world(name)
        self.world.resize(self.world.size_x, self.world.size_y, self.world.cell_size)
        self.world.create_grid(self.world.size_x, self.world.size_y, self.world.cell_size)
        self.fit_world()

        self.world.meal_calc = []
        self.world.resize_cache()
        self.world.update()

    def settings(self):
        self.par = CWorldSettings(self.world)
        self.par.setAttribute(Qt.WA_DeleteOnClose)
        self.par.show()

        loop = QEventLoop()
        self.par.destroyed.connect(loop.quit)
        loop.exec()
        if self.par.applied:
            self.world.save_world()
            self.world.create_grid(self.world.size_x, self.world.size_y, self.world.cell_size)
            self.fit_world()
            self.world.meal_calc = []
        del self.par

    def fit_world(self):
        if self.world:
            rect = QRectF(-self.world.cell_size / 2, -self.world.cell_size / 2,
                          self.world.size_x * self.world.cell_size + self.world.cell_size,
                          self.world.size_y * self.world.cell_size + self.world.cell_size)
            self.graphicsView.setSceneRect(rect)
            self.graphicsView.fitInView(rect, Qt.KeepAspectRatio)

    def next_gen(self):
        self.world.next_gen()
        if self.world.generation % 1 == 0:
            self.world.redraw()
            self.world.update()
        self.nums()

        QtWidgets.QApplication.processEvents()

    def start_play(self):
        self.timer.start(self.current_speed)

    def stop_play(self):
        self.timer.stop()

    def size_in(self):
        self.graphicsView.scale(1.25, 1.25)

    def size_out(self):
        self.graphicsView.scale(0.75, 0.75)

    def change_spped(self, s):
        if s == 'Fastest':
            self.current_speed = 0
            self.timer.setInterval(0)
        elif s == 'Fast':
            self.current_speed = 100
            self.timer.setInterval(100)
        elif s == 'Medium':
            self.current_speed = 500
            self.timer.setInterval(500)
        elif s == 'Slow':
            self.current_speed = 1000
            self.timer.setInterval(1000)

    def generate_world(self):
        self.world.generate_random_animals(100,
                                           (self.world.anim_repl_age_min, self.world.anim_repl_age_max),
                                           (self.world.anim_health_min, self.world.anim_health_max),
                                           (self.world.anim_min_age, self.world.anim_max_age),
                                           self.world.anim_gender_bal,
                                           (self.world.anim_mobility_min, self.world.anim_mobility_max),
                                           (self.world.anim_straight_min, self.world.anim_straight_max),
                                           (self.world.anim_vision_min, self.world.anim_vision_max),
                                           )
        self.nums()
        self.world.redraw()
        self.world.update()

    def clear_world(self):
        self.world.clear_all()
        self.chart1.clear_chart()
        self.chart2.clear_chart()
        self.nums()
        self.world.redraw()
        self.world.update()

    def virusing(self):
        self.virus_table.add_virus(CVirus('COVID19', 40, 100, 6, Qt.red, Qt.green))
        self.virus_table.add_virus(CVirus('грипп', 30, 40, 2, Qt.black, Qt.darkGreen))
        self.virus_table.add_virus(CVirus('эбола', 50, 10, 10, Qt.red, Qt.green))
        self.virus_table.add_virus(CVirus('орви', 20, 7, 4, Qt.black, Qt.darkGreen))
        self.virus_table.add_virus(CVirus('чума', 10, 300, 15, Qt.red, Qt.green))
        self.virus_table.add_virus(CVirus('корь', 25, 10, 3, Qt.black, Qt.darkGreen))

    def virus_settings(self):
        self.virus_wind = CVirusSettings()
        self.virus_wind.setAttribute(Qt.WA_DeleteOnClose)
        self.virus_wind.show()
        loop = QEventLoop()
        self.virus_wind.destroyed.connect(loop.quit)
        loop.exec()
        if self.virus_wind.applied:
            v = CVirus(self.virus_wind.name, self.virus_wind.duration,
                       self.virus_wind.immunity, self.virus_wind.impact,
                       self.virus_wind.color, self.virus_wind.color_imun)
            self.virus_table.add_virus(v)
            self.insert_virus(v)
        del self.virus_wind

    def animals_settings(self):

        self.animals_wind = CAnimalSettings(self.world)
        self.animals_wind.setAttribute(Qt.WA_DeleteOnClose)
        self.animals_wind.show()
        loop = QEventLoop()
        self.animals_wind.destroyed.connect(loop.quit)
        loop.exec()
        if self.animals_wind.applied:
            self.nums()
            self.world.redraw()
            self.world.update()

    def nums(self):
        self.virus_num = len(list(filter(lambda a: a.kingdom == 'animal' and a.is_ill(), self.world.animals)))

        self.chart2.append(self.virus_num)

        males = list(filter(lambda a: a.kingdom == 'animal' and a.gender == 'm', self.world.animals))
        females = list(filter(lambda a: a.kingdom == 'animal' and a.gender == 'f', self.world.animals))
        self.chart1.append(len(males) + len(females))
        self.num_animals.setText(str(len(males) + len(females)))
        self.num_males1.setText(str(len(males)))
        self.num_females1.setText(str(len(females)))
        self.num_ill1.setText(str(self.virus_num))
        self.num_gener1.setText(str(self.world.generation))

        self.onGistSelect()

    def onGistSelect(self):
        v = self.comboBox.currentText()
        if v == 'Straightness':
            _arr = list(map(lambda a: a.straight, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 5
        elif v == 'Mobility':
            _arr = list(map(lambda a: a.mobility, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 5
        elif v == 'Vision':
            _arr = list(map(lambda a: a.vision, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 1
        elif v == 'Max Age':
            _arr = list(map(lambda a: a.max_age, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 10
        elif v == 'Age':
            _arr = list(map(lambda a: a.age, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 10
        elif v == 'Health':
            _arr = list(map(lambda a: a.health, filter(lambda a: a.kingdom == 'animal', self.world.animals)))
            _scale = 10
        else:
            _arr = ([0], [0])
            _scale = 10

        _res = self.getgrouped(_arr, _scale)
        self.gist.setdata(_res[0], _res[1], _scale)

    def getgrouped(self, arr, n):
        x = []
        y = []
        for key, group in groupby(sorted(arr), lambda a: round(a // n * n, 0)):
            x.append(key)
            y.append(len(list(group)))
        return ((x, y))

    def rounddown(self, x, n):
        return round(5 ** (-n) + x, -n)
        pass

    def load_viruses(self):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        rez = cur.execute("""SELECT name, duration, immunity, impact, color, icolor FROM viruses""").fetchall()
        for vir in rez:
            self.virus_table.add_virus(CVirus(vir[0], vir[1], vir[2], vir[3], QColor(vir[4]), QColor(vir[5])))
        cur.close()
        con.close()

    def insert_virus(self, v):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute("""INSERT into viruses (name, duration, immunity, impact, color, icolor) 
VALUES (?, ?, ?, ?, ?, ?)""", (v.name, v.duration, v.immunity, v.impact, v.color.name(), v.color_immunity.name()))
        con.commit()
        cur.close()
        con.close()

    def remove_virus(self, name):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        cur.execute("""DELETE FROM viruses WHERE name = '%s'""" % name)
        con.commit()
        cur.close()
        con.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec_())
