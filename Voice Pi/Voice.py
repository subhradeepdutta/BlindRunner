# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI Pi.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        self.VoiceCommandButton = QtWidgets.QPushButton(Dialog)
        self.VoiceCommandButton.setGeometry(QtCore.QRect(480, 540, 201, 91))
        self.VoiceCommandButton.setObjectName("VoiceCommandButton")
        self.VideoGraphicsView = QtWidgets.QGraphicsView(Dialog)
        self.VideoGraphicsView.setGeometry(QtCore.QRect(250, 40, 640, 480))
        self.VideoGraphicsView.setObjectName("VideoGraphicsView")
		self.scene = QtWidgets.QGraphicsScene()
        self.PiButton = QtWidgets.QPushButton(Dialog)
        self.PiButton.setGeometry(QtCore.QRect(990, 680, 93, 28))
        self.PiButton.setObjectName("PiButton")
        self.CommandDisplay = QtWidgets.QLabel(Dialog)
        self.CommandDisplay.setGeometry(QtCore.QRect(490, 670, 191, 51))
        self.CommandDisplay.setAutoFillBackground(False)
        self.CommandDisplay.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CommandDisplay.setLineWidth(10)
        self.CommandDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.CommandDisplay.setObjectName("CommandDisplay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.VoiceCommandButton.setText(_translate("Dialog", "Voice Command"))
        self.PiButton.setText(_translate("Dialog", "Voice Pi"))
        self.CommandDisplay.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))

