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
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(1000, 720, 31, 22))
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(2)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(940, 710, 41, 41))
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setReadOnly(True)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit.setStyleSheet("background-color: rgb(235, 235, 235);")
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(1040, 710, 71, 41))
        self.textEdit_2.setAutoFillBackground(False)
        self.textEdit_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.textEdit_2.setStyleSheet("background-color: rgb(235, 235, 235);")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.DownButton.setText(_translate("Dialog", "DOWN"))
        self.LeftButton.setText(_translate("Dialog", "LEFT"))
        self.RightButton.setText(_translate("Dialog", "RIGHT"))
        self.UpButton.setText(_translate("Dialog", "UP"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">UI Pi </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Mode</p></body></html>"))
        self.textEdit_2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Gesture Pi </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Mode</p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

