"""

This file presents the logic of controlling car pi using AWS MQTT commands.

It also shows if Car Pi is in UI mode or Gesture mode.

"""

# Importing modules for PyQt5, time, PIL, Paho  etc.,
import sys
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


# Global variables section
connflag = False
# By default both the pi's are set in UI mode
piMode = 1
udp_sock = 0
udp_server_address = 0
dialogBoxSide = ""
mqttc = None
ip_addr = '192.168.141.146'

class MQTT_ThreadClass(QtCore.QThread):
    """Utility which creates a thread to continously subscribe for notifications from AWS.

    This utility triggers a signal to main thread whenever a notification is received.
    """

    # Defining signal for triggering the main thread
    trigger = QtCore.pyqtSignal(['QString'])
    def __init__(self,parent = None):
        # Initializing the thread
        super(MQTT_ThreadClass,self).__init__(parent)
        
    # Define run function to listen to notifications
    def run(self):
        print("\nIn MQTT_ThreadClass\n")
        # Configuration settings for AWS
        awshost = "data.iot.us-west-2.amazonaws.com"
        awsport = 8883
        clientId = "UiPi"
        thingName = "UiPi"
        caPath = "aws-iot-rootCA.crt"
        certPath = "cert.pem"
        keyPath = "privkey.pem"

        # Define on_connect function to subscribe to different topics like "PiMode" and "Lambda/notify"
        def on_connect(client, userdata, flags, rc):
            global connflag
            connflag = True
            print("Connection returned result: " + str(rc) )
            client.subscribe([("Lambda/Notify",1),("PiMode",1)])

        # Define on_message function to listen to notifications from AWS
        def on_message(client, userdata, msg):
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))
            print("\n")

            # Trigger for "Lambda/Notify" notifications
            if(msg.topic == "Lambda/Notify") and (piMode == 1):
                message = str(msg.payload.decode("utf-8"))
                self.trigger.emit(message)

            # Trigger for "PiMode" notifications 
            elif(msg.topic == "PiMode"):
                if(str(msg.payload.decode("utf-8")) == "UI"):
                    self.trigger.emit('UI')
                    
                elif(str(msg.payload.decode("utf-8")) == "Gesture"):
                    self.trigger.emit('Gesture')
                    
                else:
                    print("Invalid mode")
            else:
                print("Invalid notification received\n")
                    
                    
        # Declaring MQTT interfaces
        global mqttc
        mqttc = paho.Client()
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message


        # Starting the MQTT connection
        mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        mqttc.connect(awshost, awsport, keepalive=60)

        mqttc.loop_start()
      

class VideoStreaming_ThreadClass(QtCore.QThread):
    """Utility which creates a thread to continously stream video from car pi.

    This utility triggers a signal to main thread whenever a image is received from Car Pi
    through TCP connection.
    """

    # Defining signal for triggering the main thread
    trigger = QtCore.pyqtSignal(QtGui.QPixmap)
    def __init__(self,parent = None):
        # Initializing the thread
        super(VideoStreaming_ThreadClass,self).__init__(parent)
        
    # Define run function to stream video from Car Pi   
    def run(self):
        global ip_addr
        print("\n In VideoStreaming_ThreadClass \n")
        # Connect a server socket to car pi server:8008
        self.client_socket = socket.socket()
        self.client_socket.connect((ip_addr, 8008))

        # Accept a single connection and make a file-like object out of it
        self.connection = self.client_socket.makefile('rb')
        # While loop for receiving images 
        while 1:
            self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
            # Check for valid image length is received
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
            # Send the image to main thread
            self.trigger.emit(pixmap)
            time.sleep(0.1)
            

class UIProgram(Ui_Dialog):
    """Utility which displays the UI Contrl page to control the car.

    This utility provides a control buttons like Left, Right, Up, Down. Depending on
    the control buttons, commands are sent to car pi through AWS. Video is also streamed
    car pi using TCP sockets.
    """

    # Define showWarningBox function to show popup window on error
    def showWarningBox(self,arg):
        
        global piMode
        global dialogBoxSide

        # Check for PiMode arguments from AWS
        if(arg == 'UI'):
            piMode = 1
            self.horizontalSlider.setValue(piMode)
           
        elif(arg == 'Gesture'):
            piMode = 2
            self.horizontalSlider.setValue(piMode)
        # Showing notification on error  
        else:
            Notification = "Possible collision on " + arg+ " side"
            dialogBoxSide = arg
            self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.msgBox.setWindowTitle("Warning")
            self.msgBox.setText(Notification)
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msgBox.show()

    # Initializing the UI control window
    def __init__(self, dialog):
        global ip_addr
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.msgBox = QtWidgets.QMessageBox()
        self.DownButton.pressed.connect(self.downButtonOperation)
        self.LeftButton.pressed.connect(self.leftButtonOperation)
        self.RightButton.pressed.connect(self.rightButtonOperation)
        self.UpButton.pressed.connect(self.upButtonOperation)
        self.SignOutButton.clicked.connect(self.ExitOperation)
        self.horizontalSlider.valueChanged[int].connect(self.piButtonOperation)
        self.DownButton.released.connect(self.releaseOperation)
        self.LeftButton.released.connect(self.releaseOperation)
        self.RightButton.released.connect(self.releaseOperation)
        self.UpButton.released.connect(self.releaseOperation)
        
        global udp_sock
        global udp_server_address
        # Creating a UDP socket for transmitting car control command
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect a server socket to car pi server:9200
        udp_server_address = (ip_addr, 9200)
        # Sending UI control command to car pi
        message = "UI"
        sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
        print("Message sent to server:" + message)
        print("\n")

        # Creating thread for video streaming
        self.threadclass = VideoStreaming_ThreadClass()
        self.threadclass.trigger.connect(self.updateImage)
        self.threadclass.start()

        # Creating thread for MQTT connection and notifications
        self.threadclass1 = MQTT_ThreadClass()
        self.threadclass1.trigger.connect(self.showWarningBox)
        self.threadclass1.start()
        
    
    # Define updateImage funtion to show the image on the Graphics view.    
    def updateImage(self,pixmap):
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.update()
        self.VideoGraphicsView.setScene(self.scene)
       
    # Define releaseOperation funtion to send 'stop' command to car pi.    
    def releaseOperation(self):
        global piMode
        global mqttc
        print('In releaseOperation')
        if piMode == 1:
            mqttc.publish("Gesture-Pi/Commands", "Stop",qos=1)
        else:
            print('Invalid PiMode \n')

    # Define downButtonOperation funtion to send 'back' command to car pi.             
    def downButtonOperation(self):
        global piMode
        global dialogBoxSide
        global mqttc
        print('In downButtonOperation \n')
        if (piMode == 1) and (dialogBoxSide != "Back"):
            mqttc.publish("Gesture-Pi/Commands", "Back",qos=1)
            dialogBoxSide = ""
        else:
            print('Invalid PiMode \n')
            
    # Define leftButtonOperation funtion to send 'left' command to car pi.    
    def leftButtonOperation(self):
        global piMode
        global dialogBoxSide
        global mqttc
        print('In leftButtonOperation')
        if (piMode == 1)  and (dialogBoxSide != "Left"):
            mqttc.publish("Gesture-Pi/Commands", "Left",qos=1)
            dialogBoxSide = ""
        else:
            print('Invalid PiMode \n')

    # Define rightButtonOperation funtion to send 'right' command to car pi.    
    def rightButtonOperation(self):
        global piMode
        global dialogBoxSide
        global mqttc
        print('In rightButtonOperation')
        if (piMode == 1) and (dialogBoxSide != "Right"):
            mqttc.publish("Gesture-Pi/Commands", "Right",qos=1)
            dialogBoxSide = ""
        else:
            print('Invalid PiMode \n')

    # Define upButtonOperation funtion to send 'front' command to car pi.    
    def upButtonOperation(self):
        global piMode
        global dialogBoxSide
        global mqttc
        print('In upButtonOperation')
        if (piMode == 1) and (dialogBoxSide != "Front"):
            mqttc.publish("Gesture-Pi/Commands", "Front",qos=1)
            dialogBoxSide = ""
        else:
            print('Invalid PiMode \n')

    # Define piButtonOperation funtion to change the Pi Mode.    
    def piButtonOperation(self, value):
        global piMode
        global udp_sock
        global udp_server_address
        global mqttc
            
        print('In piButtonOperation \n')
        if value == 1:
            print('In Ui Pi mode')
            
            message = "UI"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            print("\n")
            
            piMode = value
            mqttc.publish("PiMode", "UI",qos=1)
            
        elif value == 2:
            print('In Gesture Pi mode')
            
            message = "Gesture"
            sent = udp_sock.sendto(message.encode('utf-8'), udp_server_address)
            print("Message sent to server:" + message)
            print("\n")
            
            piMode = value
            mqttc.publish("PiMode", "Gesture",qos=1)
            
        else:
            print('Invalid slider value received \n')   

    # Define ExitOperation to close the application
    def ExitOperation(self):
        print('In Exit Operation')
        sys.exit()
    


# The main function will create a QApplication for QDialog window for UI control page		
if __name__ == '__main__':
 
    # Calling the GUI function
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = UIProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())
