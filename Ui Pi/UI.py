# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI Pi.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        self.DownButton = QtWidgets.QPushButton(Dialog)
        self.DownButton.setGeometry(QtCore.QRect(480, 660, 201, 91))
        self.DownButton.setObjectName("DownButton")
        self.LeftButton = QtWidgets.QPushButton(Dialog)
        self.LeftButton.setGeometry(QtCore.QRect(30, 330, 201, 91))
        self.LeftButton.setObjectName("LeftButton")
        self.RightButton = QtWidgets.QPushButton(Dialog)
        self.RightButton.setGeometry(QtCore.QRect(930, 310, 201, 91))
        self.RightButton.setObjectName("RightButton")
        self.UpButton = QtWidgets.QPushButton(Dialog)
        self.UpButton.setGeometry(QtCore.QRect(470, 30, 201, 91))
        self.UpButton.setObjectName("UpButton")
        self.VideoGraphicsView = QtWidgets.QGraphicsView(Dialog)
        self.VideoGraphicsView.setGeometry(QtCore.QRect(260, 150, 640, 480))
        self.VideoGraphicsView.setObjectName("VideoGraphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.PiButton = QtWidgets.QPushButton(Dialog)
        self.PiButton.setGeometry(QtCore.QRect(990, 720, 93, 28))
        self.PiButton.setObjectName("PiButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.DownButton.setText(_translate("Dialog", "DOWN"))
        self.LeftButton.setText(_translate("Dialog", "LEFT"))
        self.RightButton.setText(_translate("Dialog", "RIGHT"))
        self.UpButton.setText(_translate("Dialog", "UP"))
        self.PiButton.setText(_translate("Dialog", "UI PI"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

