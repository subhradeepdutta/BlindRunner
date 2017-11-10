import io
import socket
import struct
import time
import picamera
import threading
import sys
import RPi.GPIO as GPIO
import paho.mqtt.client as paho
import os
import ssl

def video_streaming():
	
    # Connect a client socket to my_server:8000 (change my_server to the
    # hostname of your server)
    client_socket = socket.socket()
    client_socket.connect(('raspberrypi', 8006))

    # Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            # Start a preview and let the camera warm up for 2 seconds
            #camera.start_preview()
            time.sleep(2)

            # Note the start time and construct a stream to hold image data
            # temporarily (we could write it directly to connection but in this
            # case we want to find out the size of each capture first to keep
            # our protocol simple)
            start = time.time()
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg'):
                    
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                #if time.time() - start > 30:
                #    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection.write(struct.pack('<L', 0))
    finally:       
        connection.close()
        client_socket.close()
		

		
		
def motor_driving():
    mode=GPIO.getmode()

    GPIO.cleanup()

    RP=37
    RN=35
    LP=38
    LN=36
    sleeptime=1

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(RP, GPIO.OUT)
    GPIO.setup(RN, GPIO.OUT)
    GPIO.setup(LP, GPIO.OUT)
    GPIO.setup(LN, GPIO.OUT)
    
    def forward():
        print("Moving Forward")
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)

    def backward():
        print("Moving Backward")
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)


    def right():
        print("Moving Right")
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)
            
            
    def left():
        print("Moving Left")
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)
                    
                    
    def stop():
        print("Moving Stop")
        GPIO.output(RP, GPIO.LOW)
        GPIO.output(LN, GPIO.LOW)
        GPIO.output(RN, GPIO.LOW)
        GPIO.output(LP, GPIO.LOW)
    
    def on_connect(client, userdata, flags, rc):
        print("Connection returned result: " + str(rc) )
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("#" , 1 )

    def on_message(client, userdata, msg):
        print("topic: "+msg.topic)
        print("payload: "+str(msg.payload))
        
        if msg.payload == "Front":
            forward()
        elif msg.payload == "Back":
            backward()
        elif msg.payload == "Right":
            right()
        elif msg.payload == "Left":
            left()
        elif msg.payload == "Stop":
            stop()


    mqttc = paho.Client()
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    awshost = "data.iot.us-west-2.amazonaws.com"
    awsport = 8883
    clientId = "UiPi"
    thingName = "UiPi"
    caPath = "VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
    certPath = "cert.pem"
    keyPath = "privkey.pem"

    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    mqttc.connect(awshost, awsport, keepalive=60)

    mqttc.loop_forever()
			
if __name__ == "__main__":

    first_thread = threading.Thread(name='video_streaming', target=video_streaming)

    second_thread = threading.Thread(name='motor_driving', target=motor_driving)

    first_thread.start()
    second_thread.start()

    first_thread.join()
    second_thread.join()
			
