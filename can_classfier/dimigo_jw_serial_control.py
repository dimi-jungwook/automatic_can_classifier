#-*- coding:utf-8 -*-
import serial 
import time
from threading import Thread
import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
class_labes = ["can", "cup", "pet"]

model = load_model("cans_tl_not_ft.h5")

class SerialManager(Thread):
   
    def __init__(self, serial_port):
        Thread.__init__(self)
        print('Serial Thread...')
        self.seq = serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        self.seq.port = serial_port
        self.daemon = True
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 320)
        self.cap.set(4, 240)
        self.jpeg = None
        self.label = ""


    def run(self):
       
        while True: 
            ret, img = self.cap.read() 
            if self.seq.isOpen() == True: 
                    
                try:
                    if self.seq.inWaiting():
                        try:       
                           

                            self.command = self.seq.readline()
                            
                            cmd_dec = self.command.decode()
                            print(cmd_dec)
                            #self.seq.write("can".encode())
                        
                            # camera read -> inference -> servo command 
                            #self.seq.write("can\r\n")
                        
                            if cmd_dec[0] == 'H':
                            
                                #ret, img = self.cap.read()
                                #if ret:
                                    # cv2.imencode()....
                                    #cv2.imshow("show2", img)
                                    #key = cv2.waitKey(1)
                                    #if key&0xff == ord('q'):
                                    #    break
                                                              
                                #time.delay(0.5)                                                  
                                #print("Classified result CAN!!")
                                
                                
                                data = cv2.resize(img, (64, 64), interpolation = cv2.INTER_AREA)
                                data = data.astype("float") / 255

                                X = np.asarray([data])
                                s = model(X, training = False) 
                                
                                index = np.argmax(s)         

                                object = class_labes[index]
                                print(object)
                                
                                if object == "can":
                                    self.seq.write("can".encode())
                                    print("can1".encode())
                                    self.label = 'can'
                                elif object == "cup":
                                    self.seq.write("cup".encode())
                                    print("cup1".encode())
                                    self.label = 'cup'
                                
                                else :
                                    self.seq.write("pet".encode())
                                    print("pet1".encode())
                                    self.label = 'pet'
                                
                            
                            
                        except ValueError:
                            print("value error")

                except IOError:
                    print("IO error")
            
            cv2.putText(img, self.label, (10,200), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255), 4)
            ret, self.jpeg = cv2.imencode('.jpg', img)
            if ret:
                cv2.imshow("show", img)
            
                key = cv2.waitKey(1)
                if key&0xff == ord('q'):
                    break
                
    def open_port(self):
        if self.seq.isOpen() == False:
            self.seq.open()

    def close_port(self):
        if self.seq.isOpen() == True:
            self.seq.close()

    def is_seq_open(self):
        if self.seq.isOpen() == True:
            return True
        else:
            return False

    def get_serial_port(self):
        return self.seq.port

    def get_serial_data(self):
        return self.command

    def run_motor(self):
        print("conveyer run")
        self.seq.write("sss\r\n".encode())

    def stop_motor(self):
        print("conveyer stop")
        self.seq.write("ppp\r\n".encode())

    def get_inference(self):
        return self.label



    #def run(self):
    #    while True:
    #        ret, self.frame = self.cap.read()
    #        ret, self.jpeg = cv2.imencode('.jpg', self.frame)
    
    def get_jpeg(self):
        return self.jpeg.tobytes()



if __name__ =='__main__':
    ser_manager = SerialManager("COM3")
    ser_manager.open_port()
    ser_manager.run()