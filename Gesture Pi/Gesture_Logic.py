import sys
import skywriter
import signal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QThread
from Gesture import Ui_Dialog
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
from pymsgbox import *


connflag = False
some_value = 5000
# By default both the pi's are set in UI mode
dialogBoxSide = ""
piMode = 1

udp_sock = 0
udp_server_address = 0
dialogBoxSide = ""
ip_addr = '192.168.141.146'

mqttc = None

class ThreadClass1(QtCore.QThread):
    
    trigger = QtCore.pyqtSignal(['QString'])
    def __init__(self,parent = None):
        super(ThreadClass1,self).__init__(parent)
        
        
    def run(self):
        print("In ThreadClass1")
        ########################### MQTT Connection##########################
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "UiPi"
        thingName = "UiPi"
        caPath = "aws-iot-rootCA.crt"
        certPath = "cert.pem"
        keyPath = "privkey.pem"

        def on_connect(client, userdata, flags, rc):
            global connflag
            connflag = True
            print("Connection returned result: " + str(rc) )
            client.subscribe([("Lambda/Notify",1),("PiMode",1)])
        def on_message(client, userdata, msg):
            
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
            if(msg.topic == "Lambda/Notify") and (piMode == 2):
                message = str(msg.payload.decode("utf-8"))
                self.trigger.emit(message)
                
            elif(msg.topic == "PiMode"):
                if(str(msg.payload.decode("utf-8")) == "UI"):
                    self.trigger.emit('UI')
                    
                elif(str(msg.payload.decode("utf-8")) == "Gesture"):
                    self.trigger.emit('Gesture')
                    
                else:
                    print("Invalid mode")
                    
                    

        global mqttc
        mqttc = paho.Client()
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message



        mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        mqttc.connect(awshost, awsport, keepalive=60)

        mqttc.loop_start()
        #####################################################################
      

class ThreadClass(QtCore.QThread):
    
    trigger = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self,parent = None):
        super(ThreadClass,self).__init__(parent)
        
        
    def run(self):
        print("In ThreadClass")
        global ip_addr
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        self.client_socket = socket.socket()
        self.client_socket.connect((ip_addr, 8009))

        # Make a file-like object out of the connection
        self.connection = self.client_socket.makefile('rb')
        print("Connection established")
        while 1:
            
            # Accept a single connection and make a file-like object out of it
            #print("In while")
            self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            #print("self.image_len %d" %self.image_len)
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
            

	
        

class UIProgram(Ui_Dialog):
    
    def showWarningBox(self,arg):
        
        global piMode
        global dialogBoxSide
        print("showWarningBox with piMode:%d" %piMode)
        if(arg == 'UI'):
            piMode = 1
            self.horizontalSlider.setValue(piMode)
            
        elif(arg == 'Gesture'):
            piMode = 2
            self.horizontalSlider.setValue(piMode)
            
        else:
            if(piMode == 2):
                
                Notification = "Possible collision on " + arg+ " side"
                dialogBoxSide = arg
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setWindowTitle("Warning")
                self.msgBox.setText(Notification)
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.show()
        
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)

        self.horizontalSlider.valueChanged[int].connect(self.piButtonOperation)
        self.GestureCommandButton.clicked.connect(self.gestureCommand)
        self.SignOutButton.clicked.connect(self.ExitOperation)
        self.msgBox = QtWidgets.QMessageBox()
        
        # Create a UDP socket
        global udp_sock
        global udp_server_address
        global ip_addr
        
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        udp_server_address = (ip_addr, 9200)
        
        message = "UI"
        sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
        print("Message sent to server:" + message)
        self.threadclass = ThreadClass()
        self.threadclass.trigger.connect(self.updateImage)
        self.threadclass.start()
        
        self.threadclass1 = ThreadClass1()
        self.threadclass1.trigger.connect(self.showWarningBox)
        self.threadclass1.start()

        
    def updateImage(self,pixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.update()
        self.VideoGraphicsView.setScene(self.scene)
        
      
        
    def gestureCommand(self):
        print('In Gesture Command Operation')
        command =None
        
        
        
        @skywriter.flick()
        def flick(start,finish):
            global piMode
            global dialogBoxSide
            global mqttc
            print('Got a flick!', start, finish)

            if start == "east" and finish == "west":
                command = "Left"

            elif start == "west" and finish == "east":
                command = "Right"

            elif start == "north" and finish == "south":
                command = "Back"

            elif start == "south" and finish == "north":
                command = "Front"
            else:
                print("Invalid command")
                
            print("Pi is in %d" %piMode)
                
            if (piMode == 2) and (dialogBoxSide != command):
                # self.CommandDisplay.setText(command)
                mqttc.publish("Gesture-Pi/Commands", command, qos = 1)
                print("Transmitted successfully")
                dialogBoxSide = ""
            else:
                print("Invalid PiMode")
            
        
        @skywriter.touch()
        def touch(position):
            global piMode
            global mqttc
            print('Touch!', position)
            command = "Stop"

            # self.CommandDisplay.setText(command)
            if piMode == 2:
                mqttc.publish("Gesture-Pi/Commands", command,qos=1)
                print("Transmitted successfully")
            else:
                text="Pi is in Invalid mode"
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setWindowTitle("Warning")
                self.msgBox.setText(text)
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.show()
                    
        
     
    def piButtonOperation(self, value):
        global piMode
        global udp_sock
        global udp_server_address
        global mqttc
            
        print('In piButtonOperation')
        if value == 1:
            print('In Ui Pi mode')
            
            message = "UI"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            
            piMode = value
            
            mqttc.publish("PiMode", "UI",qos=1)
        elif value == 2:
            print('In Gesture Pi mode')
            
            message = "Gesture"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            
            piMode = value
    
            mqttc.publish("PiMode", "Gesture",qos=1)
        else:
            print('Invalid slider value received')
			
    def ExitOperation(self):
                print('In ExitOperation')
                sys.exit()

        
if __name__ == '__main__':

    
    
    # Calling the GUI function
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = UIProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())
