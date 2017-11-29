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
		
        self.CommandDisplay = QtWidgets.QLabel(Dialog)
        self.CommandDisplay.setGeometry(QtCore.QRect(490, 660, 191, 51))
        self.CommandDisplay.setAutoFillBackground(False)
        self.CommandDisplay.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CommandDisplay.setLineWidth(30)
        self.CommandDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.CommandDisplay.setObjectName("CommandDisplay")
        self.ExitButton = QtWidgets.QPushButton(Dialog)
        self.ExitButton.setGeometry(QtCore.QRect(50, 690, 75, 23))
        self.ExitButton.setObjectName("ExitButton")

        self.retranslateUi(Dialog)
        #self.VoiceCommandButton.clicked.connect(self.CommandDisplay.clear)
        #self.ExitButton.clicked.connect(self.PushButton.click)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.VoiceCommandButton.setText(_translate("Dialog", "Gesture Command"))
        self.CommandDisplay.setText(_translate("Dialog", "<html><head/><body><p><br/></p></body></html>"))
        self.ExitButton.setText(_translate("Dialog", "Exit"))
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

