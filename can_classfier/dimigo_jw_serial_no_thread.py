#-*- coding:utf-8 -*-
import serial 
import time
import cv2
import os
#from tensorflow.keras.models import load_model
import numpy as np
class_labes = ["can", "cup", "pet"]

#model = load_model("vgg_animals.h5")

def open_port():
    if seq.isOpen() == False:
        seq.open()

def close_port():
    if seq.isOpen() == True:
        seq.close()

def is_seq_open():
    if seq.isOpen() == True:
        return True
    else:
        return False


seq = serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        
seq.port = "COM3"
cap = cv2.VideoCapture(1)
cap.set(3, 320)
cap.set(4, 240)

open_port()

while True: 
    ret, img = cap.read()
    if ret:
        cv2.imshow("show", img)
        key = cv2.waitKey(1)
        if key&0xff == ord('q'):
            break
       
    if seq.isOpen() == True: 
        try:
            if seq.inWaiting()> 0:
                try:       
                    command = seq.readline()
                    cmd_dec = command.decode()
                    print(cmd_dec)
        
                            
                    time.sleep(0.5)
                    print("Classified result CAN!!")
                    seq.write("can".encode())
                    print("can".encode())
                    '''
                    data = cv2.resize(img, (64, 64), interpolation = cv2.INTER_AREA)
                    data = data.astype("float") / 255

                    X = np.asarray([data])
                    s = model(X, training = False) 

                    index = np.argmax(s)

                    object = class_labes[index]
                    print(object)
                    
                    if object == "can":
                        self.seq.write("can\r\n".encode())
                        print("dd")
                    elif object == "cup":
                        self.seq.write("cup\r\n".encode())
                        print("dd")
                    
                    else :
                        self.seq.write("pet\r\n".encode())
                        print("dd")
                    '''
                
                
                except ValueError:
                    print("value error")

        except IOError:
            print("IO error")