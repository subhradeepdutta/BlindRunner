"""

This file presents the geometry/gui elements of UI_Login Pi.

PyQt5 library is used for generating the GUI for UI_Login Pi.

Created by: PyQt5 UI code generator 5.4.1

"""

# Importing modules for Camera, PyQt5, time, boto3 etc.,
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PIL.ImageQt import ImageQt
from PIL import Image
import boto3
import UI_Logic
import picamera
import time
import io
import Images_rc


# Global variables section
BUCKET = "subrareko"
KEY = "login_image.jpg"
COLLECTION = "UI_Collection"
image = None

class ThreadClass(QtCore.QThread):
    """Utility which creates a thread to continously capture images from camera.

    This utility triggers a signal for 0.1 seconds to display the image on the
    Videographics window.
    """

    # Defining signal for triggering the main thread
    trigger = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self,parent = None):
        # Initializing the thread
        super(ThreadClass,self).__init__(parent)
        
    # Define run function to video streaming functionality    
    def run(self):
        print("\n In Video Capture ThreadClass \n")
        global image

        # Creating camera object
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        time.sleep(2)

        # Creating a byte stream to store the captured image
        image_stream = io.BytesIO()
        for foo in camera.capture_continuous(image_stream, 'jpeg'):
            image_stream.seek(0)
            image = Image.open(image_stream)
            
            qimage = ImageQt(image)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            print("Sending capture to main thread \n")
            self.trigger.emit(pixmap)
            # Giving delay of 0.1 seconds
            time.sleep(0.1)
            image_stream.seek(0)
            image_stream.truncate()

class Ui_Dialog(object):
    """Utility which displays the UI Login page for authentication from the user.

    This utility provides a login_button. When login_button is pressed,
    Image is sent to AWS rekognition, if the image taken is matched with the database
    then the page is navigated to control page, otherwise popup window is shown for
    unsuccessful authentication.
    """
    
    def loginCheck(self):
        # Saving the captured image from camera to local directory
        global image
        image.save('capture_image.jpg')

        # Creating client for AWS S3
        s3obj = boto3.client("s3",\
                               region_name = 'us-west-2',
                               aws_access_key_id='****************',
                               aws_secret_access_key='******************************************')
    
        s3obj.upload_file('capture_image.jpg', BUCKET, 'login_image.jpg')
        
        rekognition = boto3.client("rekognition",\
                                   region_name = 'us-west-2',
                                   aws_access_key_id='****************',
                                   aws_secret_access_key='******************************************')


        # Searching the image from AWS S3 in the AWS Collection
        try:
            response = rekognition.search_faces_by_image(
                    Image={
                            "S3Object": {
                                    "Bucket": BUCKET,
                                    "Name": KEY,
                            }
                    },
                    CollectionId=COLLECTION,
                    FaceMatchThreshold=80,
            )
            print("Checking for Authentication \n")
            # If condition if face doesn't matches
            if(response['FaceMatches'] == []):
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setWindowTitle("Warning")
                self.msgBox.setText("Authentication is Unsuccessful")
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.show()
            else:
                # Face matches from the AWS collection available
                self.loginWindow = QtWidgets.QDialog()
                self.prog = UI_Logic.UIProgram(self.loginWindow)
                self.loginWindow.show()
                self.obj.destroy()
        except ValueError:
            print("No faces found")
            
        
    def setupUi(self, Dialog):
        """Setting up the UI Login page for authentication from the user.

        Args:
            QtDialog window object

        Login button is provided to capture the image and to send the image to AWS Rekognition.
        """
        Dialog.setObjectName("Dialog")
        Dialog.resize(1163, 786)
        font = QtGui.QFont()
        font.setFamily("Comic Sans MS")
        font.setPointSize(18)
        Dialog.setFont(font)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        Dialog.setWhatsThis("")
        Dialog.setStyleSheet("QDialog {border-image: url(:/Images/f1.jpg)}")
        Dialog.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        Dialog.setModal(False)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.obj = Dialog
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.BlindRunnerText = QtWidgets.QLabel(Dialog)
        self.BlindRunnerText.setMinimumSize(QtCore.QSize(450, 100))
        self.BlindRunnerText.setMaximumSize(QtCore.QSize(750, 150))
        font = QtGui.QFont()
        font.setPointSize(50)
        self.msgBox = QtWidgets.QMessageBox()
        self.BlindRunnerText.setFont(font)
        self.BlindRunnerText.setStyleSheet("background-color: rgba(100, 100, 100, 120); color: rgba(255,255,255,200);")
        self.BlindRunnerText.setObjectName("BlindRunnerText")
        self.gridLayout.addWidget(self.BlindRunnerText, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.VideoGraphicsView = QtWidgets.QGraphicsView(Dialog)
        self.VideoGraphicsView.setMinimumSize(QtCore.QSize(640, 480))
        self.VideoGraphicsView.setMaximumSize(QtCore.QSize(640, 480))
        self.VideoGraphicsView.setStyleSheet("")
        self.VideoGraphicsView.setObjectName("VideoGraphicsView")
        self.scene = QtWidgets.QGraphicsScene()
        self.gridLayout.addWidget(self.VideoGraphicsView, 1, 1, 1, 1)
        self.SharatText = QtWidgets.QLabel(Dialog)
        self.SharatText.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SharatText.setFont(font)
        self.SharatText.setStyleSheet("color: rgba(255,255,255,200);")
        self.SharatText.setObjectName("SharatText")
        self.gridLayout.addWidget(self.SharatText, 2, 0, 2, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignBottom)
        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setMinimumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 100), stop:1 rgba(255,255,255, 100)); color: rgba(255,255,255,200);")
        self.login_button.setObjectName("login_button")
        self.gridLayout.addWidget(self.login_button, 2, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.SubhradeepText = QtWidgets.QLabel(Dialog)
        self.SubhradeepText.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SubhradeepText.setFont(font)
        self.SubhradeepText.setStyleSheet("color: rgba(255,255,255,200);")
        self.SubhradeepText.setObjectName("SubhradeepText")
        self.gridLayout.addWidget(self.SubhradeepText, 2, 2, 2, 1, QtCore.Qt.AlignRight|QtCore.Qt.AlignBottom)
        self.SridharText = QtWidgets.QLabel(Dialog)
        self.SridharText.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.SridharText.setFont(font)
        self.SridharText.setStyleSheet("color: rgba(255,255,255,200);")
        self.SridharText.setObjectName("SridharText")
        self.gridLayout.addWidget(self.SridharText, 3, 1, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        
        self.login_button.clicked.connect(self.loginCheck)
        self.threadclass = ThreadClass()
        self.threadclass.trigger.connect(self.updateImage)
        self.threadclass.start()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        
    # Define updateImage funtion to show the image on the Graphics view.   
    def updateImage(self,pixmap):
        print('In update_Image')
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.update()
        self.VideoGraphicsView.setScene(self.scene)

    # Define retranslateUi funtion to change the text to different language.
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.BlindRunnerText.setText(_translate("Dialog", "The Blind Runner"))
        self.SharatText.setText(_translate("Dialog", "Sharat RP"))
        self.login_button.setText(_translate("Dialog", "Login"))
        self.SubhradeepText.setText(_translate("Dialog", "Subhradeep Dutta"))
        self.SridharText.setText(_translate("Dialog", "Sridhar Pavithrapu"))


# The main function will create a QApplication for QDialog window for diaplaying UI Login page
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

