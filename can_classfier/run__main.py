from dimigo_jw_serial_control import SerialManager
from flask import Flask, render_template, Response

import random
from flask_socketio import SocketIO, emit
from cobit_opencv_cam import CobitOpenCVCam
#from threading import Thread
from flask import Flask, render_template, Response
import serial
import time
import json


app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)

def gen_frames():  # generate frame by frame from camera
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + at.get_jpeg() + b'\r\n')  # concat frame one by one and show result



@app.route('/', methods=['GET', 'POST'])
def method():
    result = at.get_inference()
    templateData = {
        'result' : result,
        }
    return render_template('index.html', **templateData)

@socketio.event
def my_event(message):
    data = json.loads(message)
    if int(data['CONTROL']) == 0:
        at.stop_motor()
    else:
        at.run_motor()

@app.route('/video_feed',methods = ['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

at = SerialManager("COM4") 
at.daemon = True                                                                                                                 
at.open_port()  
at.start()
socketio.run(app, port=5000)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          