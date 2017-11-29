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

      

class ThreadClass(QtCore.QThread):
    
    trigger = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self,parent = None):
        super(ThreadClass,self).__init__(parent)
        
        
    def run(self):
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        self.client_socket = socket.socket()
        self.client_socket.connect(('192.168.141.147', 8009))

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
           
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)

        self.horizontalSlider.valueChanged[int].connect(self.piButtonOperation)
        self.VoiceCommandButton.clicked.connect(self.gestureCommand)
        self.ExitButton.clicked.connect(self.ExitOperation)
        self.threadclass = ThreadClass()
        self.threadclass.trigger.connect(self.updateImage)
        self.threadclass.start()
        
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "Gesture-Pi"
        thingName = "Gesture-Pi"
        caPath = "aws-iot-rootCA.crt"
        certPath = "cert.pem"
        keyPath = "privkey.pem"

        
        
        def on_connect(client, userdata, flags, rc):
            global connflag
            connflag = True
            print("Connection returned result: " + str(rc) )
            client.subscribe([("Lambda/Notify",1),("PiMode",1)])

        def on_message(client, userdata, msg):
            global piMode
            global dialogBoxSide
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
            if(msg.topic == "Lambda/Notify") and (piMode == 2):
                Notification = "Possible collision on " + str(msg.payload.decode("utf-8")) + " side"
                dialogBoxSide = str(msg.payload.decode("utf-8"))
                alert(text=Notification, title='Warning', button='OK')
            elif(msg.topic == "PiMode"):
                if(str(msg.payload.decode("utf-8")) == "UI"):
                    piMode = 1
                    print("Changed piMode variable to UI mode")
                    self.horizontalSlider.setValue(piMode)
                elif(str(msg.payload.decode("utf-8")) == "Gesture"):
                    piMode = 2
                    print("Changed piMode variable to Gesture mode")
                    self.horizontalSlider.setValue(piMode)
                else:
                    print("Invalid mode")
				

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
        
      
        
    def gestureCommand(self):
        print('In Gesture Command Operation')
        command =None
        
        
        
        @skywriter.flick()
        def flick(start,finish):
            global piMode
            global dialogBoxSide
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
                self.CommandDisplay.setText(command)
                self.mqttc.publish("Gesture-Pi/Commands", command, qos = 1)
                print("Transmitted successfully")
                dialogBoxSide = ""
            else:
                print("Invalid PiMode")
            
        
        @skywriter.touch()
        def touch(position):
            global piMode
            print('Touch!', position)
            command = "Stop"

            self.CommandDisplay.setText(command)
            if piMode == 2:
                self.mqttc.publish("Gesture-Pi/Commands", command,qos=1)
                print("Transmitted successfully")
            else:
                alert(text="Pi is in Invalid mode", title='Warning', button='OK')
                    
        
     
    def piButtonOperation(self, value):
        global piMode
        print('In piButtonOperation where %d' %value)
        if value == 1:
            print('In Ui Pi mode')
            
            message = "UI"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            
            piMode = value
            self.mqttc.publish("PiMode", "UI",qos=1)
        elif value == 2:
            print('In Gesture Pi mode')
            
            message = "Gesture"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            
            piMode = value
            self.mqttc.publish("PiMode", "Gesture",qos=1)
        else:
            print('Invalid slider value received')
			
    def ExitOperation(self):
                print('In ExitOperation')
                sys.exit()

        
if __name__ == '__main__':
     # Create a UDP socket
    
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    udp_server_address = ('192.168.141.147', 9200)
    
    message = "Hi"
    sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
    print("Message sent to server:" + message)
    
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = UIProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())
