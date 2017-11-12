import sys
import multiprocessing
import speech_recognition as sr
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from Voice import Ui_Dialog
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
        
        
		self.PiButton.clicked.connect(self.piButtonOperation)
		self.VoiceCommandButton.clicked.connect(self.voiceCommandOperation)
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
       
        
	def voiceCommandOperation(self):
		print('In voiceCommandOperation')
		# Record Audio
		r = sr.Recognizer()
		r.energy_threshold = 3700
		
		# Speech recognition using Google Speech Recognition
		try:
			with sr.Microphone() as source:
				print("Adjusting ambient noise levels! Please wait")
				r.adjust_for_ambient_noise(source, duration=1);
				print("Speak now!")
				audio = r.listen(source, timeout=1.5)
			# for testing purposes, we're just using the default API key
			# to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
			# instead of `r.recognize_google(audio)`
			speech_to_text_output = r.recognize_google(audio, language="en-IN")
			print("You said: " + speech_to_text_output)
		
		except sr.WaitTimeoutError as e:
			print("Timeout; {0}".format(e))

		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")

		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
		
		#Check if text has valid keyword or not
		try:
			if "left" in speech_to_text_output:
				command = "left"
			elif "right" in speech_to_text_output:
				command = "right"
			elif "front" in speech_to_text_output:
				command = "front"
			elif "back" in speech_to_text_output:
				command = "back"
			elif "stop" in speech_to_text_output:
				command = "stop"
			print("Identified the command as  ---->  " + command)
			print("Transmitting to AWS Server")

		except NameError:
			print("Did not recognize a valid command")
			print("Terminating operation")
		self.mqttc.publish("Navigation", command)
        
        
	def piButtonOperation(self):
		print('In piButtonOperation')
		
    


		
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    prog = UIProgram(dialog)
    dialog.show()
    sys.exit(app.exec_())