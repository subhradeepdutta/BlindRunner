import sys
import multiprocessing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from UI import Ui_Dialog
import socket
import struct
import time
from PIL.ImageQt import ImageQt
from PIL import Image
import io
import paho.mqtt.client as paho
import os
import ssl
from time import sleep
from random import uniform

connflag = False


      

class ThreadClass(QtCore.QThread):
    
    trigger = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self,parent = None):
        super(ThreadClass,self).__init__(parent)
        
        
    def run(self):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', 8006))
        self.server_socket.listen(0)
        self.connection = self.server_socket.accept()[0].makefile('rb')
        while 1:
            
            # Accept a single connection and make a file-like object out of it
            
            self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            if not self.image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(self.connection.read(self.image_len))
            # Rewind the stream, open it as an image with PIL and do some
            # processing on it
            image_stream.seek(0)
            image = Image.open(image_stream)
            
            qimage = ImageQt(image)
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.trigger.emit(pixmap)
            time.sleep(0.1)
            
def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )
    
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
        

class UIProgram(Ui_Dialog):
        
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.DownButton.pressed.connect(self.downButtonOperation)
        self.LeftButton.pressed.connect(self.leftButtonOperation)
        self.RightButton.pressed.connect(self.rightButtonOperation)
        self.UpButton.pressed.connect(self.upButtonOperation)
        self.PiButton.pressed.connect(self.piButtonOperation)
        self.DownButton.released.connect(self.releaseOperation)
        self.LeftButton.released.connect(self.releaseOperation)
        self.RightButton.released.connect(self.releaseOperation)
        self.UpButton.released.connect(self.releaseOperation)
        self.PiButton.released.connect(self.releaseOperation)
        self.threadclass = ThreadClass()
        self.threadclass.trigger.connect(self.updateImage)
        self.threadclass.start()
        
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "UiPi"
        thingName = "UiPi"
        caPath = "VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
        certPath = "cert.pem"
        keyPath = "privkey.pem"
        
        
            
        
		
        self.mqttc = paho.Client()
        self.mqttc.on_connect = on_connect
        self.mqttc.on_message = on_message

        

        self.mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        self.mqttc.connect(awshost, awsport, keepalive=60)

        self.mqttc.loop_start()
        
    
        
    def updateImage(self,pixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.update()
        self.VideoGraphicsView.setScene(self.scene)
       
        
    def releaseOperation(self):
        print('In releaseOperation')
        self.mqttc.publish("temperature", "Stop")
        
    def downButtonOperation(self):
        print('In downButtonOperation')
        self.mqttc.publish("temperature", "Back")
        
    def leftButtonOperation(self):
        print('In leftButtonOperation')
        self.mqttc.publish("temperature", "Left")
        
    def rightButtonOperation(self):
        print('In rightButtonOperation')
        self.mqttc.publish("temperature", "Right")
        
    def upButtonOperation(self):
        print('In upButtonOperation')
        self.mqttc.publish("temperature", "Front")
        
    def piButtonOperation(self):
        print('In piButtonOperation')
        
    


		
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = UIProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())