from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit, QWidget, QLabel, QFormLayout, QColorDialog


class CVirusSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.applied = False

        self.setWindowTitle('Settings')
        self.setGeometry(800, 600, 320, 240)

        self.gridLayout = QtWidgets.QFormLayout(self)
        self.gridLayout.setObjectName("gridLayout")

        self.v_lname = QLabel(self)
        self.v_lname.setText('Virus name:')
        self.gridLayout.setWidget(0, QFormLayout.LabelRole, self.v_lname)
        self.v_iname = QLineEdit()
        self.gridLayout.setWidget(0, QFormLayout.FieldRole, self.v_iname)

        self.v_ldur = QLabel(self)
        self.v_ldur.setText('Virus duration:')
        self.gridLayout.setWidget(1, QFormLayout.LabelRole, self.v_ldur)
        self.v_idur = QLineEdit()
        self.gridLayout.setWidget(1, QFormLayout.FieldRole, self.v_idur)

        self.v_limun = QLabel(self)
        self.v_limun.setText('Virus immunity period:')
        self.gridLayout.setWidget(2, QFormLayout.LabelRole, self.v_limun)
        self.v_iimun = QLineEdit()
        self.gridLayout.setWidget(2, QFormLayout.FieldRole, self.v_iimun)

        self.v_limp = QLabel(self)
        self.v_limp.setText('Virus impact:')
        self.gridLayout.setWidget(3, QFormLayout.LabelRole, self.v_limp)
        self.v_iimp = QLineEdit()
        self.gridLayout.setWidget(3, QFormLayout.FieldRole, self.v_iimp)

        self.l_error = QLabel(self)
        self.gridLayout.setWidget(4, QFormLayout.FieldRole, self.l_error)
        self.l_error.setStyleSheet('color: red')
        self.l_error.setVisible(False)

        self.btn_color = QPushButton(self)
        self.gridLayout.setWidget(5, QFormLayout.FieldRole, self.btn_color)
        self.btn_color.setText('Color')
        self.btn_color.clicked.connect(self.select_color)
        self.btn_immun_color = QPushButton(self)
        self.gridLayout.setWidget(6, QFormLayout.FieldRole, self.btn_immun_color)
        self.btn_immun_color.setText('Immunity color')
        self.btn_immun_color.clicked.connect(self.select_immun_color)

        self.apply = QPushButton(self)
        self.apply.setGeometry(125, 200, 50, 30)
        self.apply.setText('Apply')
        self.apply.clicked.connect(self.applypb)
        self.cancel = QPushButton(self)
        self.cancel.setGeometry(180, 200, 50, 30)
        self.cancel.setText('Cancel')
        self.cancel.clicked.connect(self.cancelpb)

    def applypb(self):
        if self.v_idur.text().isdigit() and self.v_iimun.text().isdigit() and self.v_iimp.text().isdigit():
            if int(self.v_idur.text()) >= 0 and int(self.v_iimun.text()) >= 0 and int(self.v_iimp.text()) >= 0:
                self.name = self.v_iname.text()
                self.duration = int(self.v_idur.text())
                self.immunity = int(self.v_iimun.text())
                self.impact = int(self.v_iimp.text())
                self.applied = True
                self.close()
            else:
                self.l_error.setText('Incorrect parameters: must be greater then 0')
                self.l_error.setVisible(True)
        else:
            self.l_error.setText('Invalid format: must be integers')
            self.l_error.setVisible(True)

    def cancelpb(self):
        self.applied = False
        self.close()

    def select_color(self):
        self.color = QColorDialog().getColor()
        self.btn_color.setStyleSheet("background-color: {}".format(self.color.name()))

    def select_immun_color(self):
        self.color_imun = QColorDialog().getColor()
        self.btn_immun_color.setStyleSheet("background-color: {}".format(self.color_imun.name()))
