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
import json

sensor_side_option = "Stop"

mqttc = paho.Client()


def distance(GPIO_TRIGGER, GPIO_ECHO):
    
    # set Trigger to HIGH
     
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


def video_streaming():
    
    host  = '0.0.0.0'
    port1 = 8008
    port2 = 8009
    

    server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket1.bind((host, port1))
    server_socket1.listen(0)
    connection1 = server_socket1.accept()[0].makefile('wb')
    
    server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket2.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket2.bind((host, port2))
    server_socket2.listen(0)
    connection2 = server_socket2.accept()[0].makefile('wb')
    
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.vflip = True
            camera.hflip = True
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
                connection1.write(struct.pack('<L', stream.tell()))
                connection1.flush()
                connection2.write(struct.pack('<L', stream.tell()))
                connection2.flush()
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                connection1.write(stream.read())
                stream.seek(0)
                connection2.write(stream.read())
                # If we've been capturing for more than 30 seconds, quit
                #if time.time() - start > 30:
                #    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
        # Write a length of zero to the stream to signal we're done
        connection1.write(struct.pack('<L', 0))
        connection2.write(struct.pack('<L', 0))
    finally:       
        connection1.close()
        connection2.close()
        server_socket1.close()
        server_socket2.close()


def sensor_streaming():
    while 1:
        global sensor_side_option
        if(sensor_side_option != "Stop"):
            print("Calculating proximity distance:")
            if(sensor_side_option == "Front"):    
                dist = distance(16,15)
            elif(sensor_side_option == "Back"):
                dist = distance(37,35)
            elif(sensor_side_option == "Left"):
                dist = distance(31,33)
            elif(sensor_side_option == "Right"):
                dist = distance(24,26)
            else:
                printf("Invalid sensor side")
            print ("Measured Distance = %.1f cm" % dist)
            send_msg = {
                'sensor_value': dist,
                'sensor_side': sensor_side_option
            }
            msg = json.dumps(send_msg)
            mqttc.publish("Car-Pi/Distance", msg,qos=1)
            time.sleep(1)
        

		
		
def motor_driving():
   

    RP=3
    RN=5
    LP=7
    LN=11
    sleeptime=1

    GPIO.setup(RP, GPIO.OUT)
    GPIO.setup(RN, GPIO.OUT)
    GPIO.setup(LP, GPIO.OUT)
    GPIO.setup(LN, GPIO.OUT)
    
    
    
    def forward():
        print("Moving Forward")
        global sensor_side_option
        sensor_side_option = "Front"
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)
        

    def backward():
        print("Moving Backward")
        global sensor_side_option
        sensor_side_option = "Back"
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)
        


    def right():
        print("Moving Right")
        global sensor_side_option
        sensor_side_option = "Right"
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)
        
            
            
    def left():
        print("Moving Left")
        global sensor_side_option
        sensor_side_option = "Left"
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)
        
                    
                    
    def stop():
        print("Moving Stop")
        global sensor_side_option
        sensor_side_option = "Stop"
        GPIO.output(RP, GPIO.LOW)
        GPIO.output(LN, GPIO.LOW)
        GPIO.output(RN, GPIO.LOW)
        GPIO.output(LP, GPIO.LOW)
        
    
    awshost = "data.iot.us-west-2.amazonaws.com"
    awsport = 8883
    clientId = "Car-Pi"
    thingName = "Car-Pi"
    caPath = "VeriSign-Class 3-Public-Primary-Certification-Authority-G5.pem"
    certPath = "cert.pem"
    keyPath = "privkey.pem"

    def on_connect(client, userdata, flags, rc):
        global connflag
        connflag = True
        print("Connection returned result: " + str(rc) )
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("Gesture-Pi/Commands" , 1 )

    def on_message(client, userdata, msg):
        print("topic: "+msg.topic)
        print("payload: "+str(msg.payload.decode("utf-8")))
        
        received_message = str(msg.payload.decode("utf-8"))
        if received_message == "Front":
            forward()
        elif received_message == "Back":
            backward()
        elif received_message == "Right":
            right()
        elif received_message == "Left":
            left()
        elif received_message == "Stop":
            stop()
        
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message


    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    mqttc.connect(awshost, awsport, keepalive=60)

    mqttc.loop_forever()

	
def udp_data():
	# Create a TCP/IP socket
	udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
	# Bind the socket to the port
	udp_server_address = ('', 9200)
	print("Starting up server at address: " + str(udp_server_address) )
	udp_sock.bind(udp_server_address)
	
	while True:
		print("waiting to receive message ")
		data, address = udp_sock.recvfrom(4096)
		
		print("Received data:" + data.decode("utf-8"))
		

if __name__ == "__main__":

    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)

    first_thread = threading.Thread(name='video_streaming', target=video_streaming)

    second_thread = threading.Thread(name='motor_driving', target=motor_driving)
    
    third_thread = threading.Thread(name='sensor_data', target=sensor_streaming)
	
    fourth_thread = threading.Thread(name='udp_data', target=udp_data)

    first_thread.start()
    second_thread.start()
    third_thread.start()
    fourth_thread.start()

    first_thread.join()
    second_thread.join()
    third_thread.join()
    fourth_thread.join()
			
