"""

This file presents the logic of controlling car pi using AWS MQTT commands.


"""

# Importing modules for PyQt5, time, boto3, Paho  etc.,
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
import boto3
import signal


# Global variables section
sensor_side_option = "Stop"
mqttc = paho.Client()


# Define distance function to capture the distance of any obstacle on
# all the four directions of the car.
def distance(GPIO_TRIGGER, GPIO_ECHO):

    # Set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # Set Trigger after to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # Set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # Storing the start and stop time
    StartTime = time.time()
    StopTime = time.time()
 
    # Save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # Save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # Calculating time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # Multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    # Returning distance calculated
    return distance


# Define video_streaming function to capture video from camera connected
# and send it to other Pi's using TCP connection
def video_streaming():

    # Creating ports for both Gesture Pi and UI Pi
    host  = '0.0.0.0'
    port1 = 8008
    port2 = 8009
    
    print("Receiving connection UI Pi and Gesture Pi \n")
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
            # Start a camera capture and let the camera warm up for 2 seconds
            time.sleep(2)

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
                
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
                
        # Write a length of zero to the stream to signal we're done
        connection1.write(struct.pack('<L', 0))
        connection2.write(struct.pack('<L', 0))
        
    finally:
        # Closing all the connections created
        connection1.close()
        connection2.close()
        server_socket1.close()
        server_socket2.close()


# Define sensor_streaming function to publish distance of the proximity sensors to AWS
def sensor_streaming():
    print("In sensor_Streaming \n")
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
            # Publishing distance to AWS
            mqttc.publish("Car-Pi/Distance", msg,qos=1)
            time.sleep(1)
        

# Define motor_driving function to control the motors of the car				
def motor_driving():
    print("In motor_driving function \n")
   
    # Setting GPIO pins for different direction
    RP=3
    RN=5
    LP=13
    LN=11
    sleeptime=1

    # Setting all the GPIO pins to out
    GPIO.setup(RP, GPIO.OUT)
    GPIO.setup(RN, GPIO.OUT)
    GPIO.setup(LP, GPIO.OUT)
    GPIO.setup(LN, GPIO.OUT)
    
    # Define forward function to move the car forward
    def forward():
        print("Moving Forward \n")
        global sensor_side_option
        sensor_side_option = "Front"
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)
        
    # Define backward function to move the car backwards
    def backward():
        print("Moving Backward \n")
        global sensor_side_option
        sensor_side_option = "Back"
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)
        
    # Define right function to move the car right
    def right():
        print("Moving Right \n")
        global sensor_side_option
        sensor_side_option = "Right"
        GPIO.output(RN, GPIO.HIGH)
        GPIO.output(LP, GPIO.HIGH)
               
    # Define left function to move the car left        
    def left():
        print("Moving Left \n")
        global sensor_side_option
        sensor_side_option = "Left"
        GPIO.output(RP, GPIO.HIGH)
        GPIO.output(LN, GPIO.HIGH)
        
    # Define stop function to stop the car                 
    def stop():
        print("Moving Stop \n")
        global sensor_side_option
        sensor_side_option = "Stop"
        GPIO.output(RP, GPIO.LOW)
        GPIO.output(LN, GPIO.LOW)
        GPIO.output(RN, GPIO.LOW)
        GPIO.output(LP, GPIO.LOW)
        
    # AWS configuration settings
    awshost = "data.iot.us-west-2.amazonaws.com"
    awsport = 8883
    clientId = "Car-Pi"
    thingName = "Car-Pi"
    caPath = "aws-iot-rootCA.crt"
    certPath = "cert.pem"
    keyPath = "privkey.pem"

    # Define on_connect function to subscribe to "Gesture-Pi/Commands" topic
    def on_connect(client, userdata, flags, rc):
        global connflag
        connflag = True
        print("Connection returned result: " + str(rc) )
        print("\n")
        client.subscribe("Gesture-Pi/Commands" , 1 )

    # Define on_message function to receive notifications from AWS
    def on_message(client, userdata, msg):
        print("topic: "+msg.topic)
        print("payload: "+str(msg.payload.decode("utf-8")))
        print("\n")
        
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
        else:
            print("Invalid command received\n")

    # Starting the MQTT connection   
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    mqttc.connect(awshost, awsport, keepalive=60)
    mqttc.loop_forever()

	
def udp_data():
    
    global sns
    # Create a UDP socket
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind the socket to the port
    udp_server_address = ('', 9200)
    print("Starting up server at address: " + str(udp_server_address) )
    print("\n")
    udp_sock.bind(udp_server_address)
    
    while True:
            print("waiting to receive message \n")
            data, address = udp_sock.recvfrom(4096)
            
            print("Received data:" + data.decode("utf-8"))
            print("\n")
            
            msg = "Car is controlled by " + data.decode("utf-8")
            # Sending the SNS notification
            sns.publish(Message=msg, TopicArn='arn:aws:sns:us-west-2:783367766210:carControl')
		
		
# Main function for having functionality for car pi
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)

if __name__ == "__main__":

    # Handling exceptions
    signal.signal(signal.SIGINT, signal_handler)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    # Creating the session for AWS SNS
    session = boto3.Session(profile_name='default')
    sns = session.client('sns')

    # Creating threads
    first_thread = threading.Thread(name='video_streaming', target=video_streaming)
    second_thread = threading.Thread(name='motor_driving', target=motor_driving)
    third_thread = threading.Thread(name='sensor_data', target=sensor_streaming)
    fourth_thread = threading.Thread(name='udp_data', target=udp_data)
    
    # Making setDaemon true for all threads for clean exit
    first_thread.setDaemon(True)
    second_thread.setDaemon(True)
    third_thread.setDaemon(True)
    fourth_thread.setDaemon(True)

    # Starting threads
    first_thread.start()
    second_thread.start()
    third_thread.start()
    fourth_thread.start()

    # Blocking the main thread till all the threads completed their execution
    first_thread.join()
    second_thread.join()
    third_thread.join()
    fourth_thread.join()
			
