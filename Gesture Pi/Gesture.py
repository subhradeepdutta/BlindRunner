"""

This file presents the geometry/gui elements of Gesture Pi.

PyQt5 library is used for generating the GUI for Gesture Pi.

Created by: PyQt5 UI code generator 5.4.1

"""

# Importing PyQT5 modules
from PyQt5 import QtCore, QtGui, QtWidgets
import Images_rc

class Ui_Dialog(object):
    """Utility which maintains a gui elements of Gesture Pi.

    Utility which facilitates gesture movement to control the car,and
    Graphics view to display the video received from car pi.
    """

    # Define setupUi function to initalize the gui elements
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(18)
        Dialog.setFont(font)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Dialog.setWhatsThis("")
        Dialog.setStyleSheet("QDialog {border-image: url(:/Images/f1.jpg)}")
        Dialog.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        Dialog.setModal(False)
        self.GestureCommandButton = QtWidgets.QPushButton(Dialog)
        self.GestureCommandButton.setGeometry(QtCore.QRect(380, 590, 331, 91))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.GestureCommandButton.setFont(font)
        self.GestureCommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.GestureCommandButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.GestureCommandButton.setObjectName("GestureCommandButton")
        self.SignOutButton = QtWidgets.QPushButton(Dialog)
        self.SignOutButton.setGeometry(QtCore.QRect(950, 10, 201, 91))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SignOutButton.setFont(font)
        self.SignOutButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SignOutButton.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.SignOutButton.setObjectName("SignOutButton")
        self.VideoGraphicsView = QtWidgets.QGraphicsView(Dialog)
        self.VideoGraphicsView.setGeometry(QtCore.QRect(250, 60, 640, 480))
        self.VideoGraphicsView.setStyleSheet("")
        self.VideoGraphicsView.setObjectName("VideoGraphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.horizontalSlider = QtWidgets.QSlider(Dialog)
        self.horizontalSlider.setGeometry(QtCore.QRect(920, 710, 81, 71))
        self.horizontalSlider.setStyleSheet("QSlider::handle:horizontal {background-color: rgba(200,200,200,200);}\n"
"QSlider {background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(205,0,0, 100), stop:1 rgba(0, 0, 0, 100))};")
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(2)
        self.horizontalSlider.setPageStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.UiPiMode = QtWidgets.QTextEdit(Dialog)
        self.UiPiMode.setGeometry(QtCore.QRect(810, 710, 101, 71))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.UiPiMode.setFont(font)
        self.UiPiMode.setAutoFillBackground(True)
        self.UiPiMode.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgba(255,255,255, 100), stop:1 rgba(0, 0, 0, 100)); color: rgba(200,200,200,255);")
        self.UiPiMode.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.UiPiMode.setReadOnly(True)
        self.UiPiMode.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.UiPiMode.setObjectName("UiPiMode")
        self.GesturePiMode = QtWidgets.QTextEdit(Dialog)
        self.GesturePiMode.setGeometry(QtCore.QRect(1010, 710, 131, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.GesturePiMode.setFont(font)
        self.GesturePiMode.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.BlankCursor))
        self.GesturePiMode.setFocusPolicy(QtCore.Qt.NoFocus)
        self.GesturePiMode.setAutoFillBackground(False)
        self.GesturePiMode.setStyleSheet("background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(255,255,255, 100), stop:1 rgba(0, 0, 0, 100)); color: rgba(200,200,200,255);")
        self.GesturePiMode.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.GesturePiMode.setReadOnly(True)
        self.GesturePiMode.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.GesturePiMode.setObjectName("GesturePiMode")
        self.CommandDisplay = QtWidgets.QTextEdit(Dialog)
        self.CommandDisplay.setGeometry(QtCore.QRect(300, 700, 491, 61))
        self.CommandDisplay.setObjectName("CommandDisplay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    # Define retranslateUi function is used to retranslate the text of push buttons in different language
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.GestureCommandButton.setText(_translate("Dialog", "GESTURE COMMAND"))
        self.SignOutButton.setText(_translate("Dialog", "SIGN OUT"))
        self.UiPiMode.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">UI Pi </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Mode</span></p></body></html>"))
        self.GesturePiMode.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:18pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Gesture Pi </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Mode</span></p></body></html>"))


# The main function will create a QApplication for QDialog window for Gesture Pi page

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

