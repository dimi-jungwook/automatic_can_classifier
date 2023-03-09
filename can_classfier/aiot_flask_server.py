from flask import Flask, render_template, Response
from aiot_arduino_serial_class_thread import AiotSerialManager
import random
from flask_socketio import SocketIO, emit
from cobit_opencv_cam import CobitOpenCVCam
from threading import Thread
from flask import Flask, render_template, Response

app = Flask(__name__)
socketio = SocketIO(app, async_mode=None)
def gen_frames():  # generate frame by frame from camera
   
    while True:
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + cam.get_jpeg() + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def hello():
    return("hello")

@app.route('/video_feed',methods = ['GET'])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/method', methods=['GET', 'POST'])
def method():
    temp = random.randint(20, 40)
    humid = random.randint(40, 100)
    light = random.randint(10, 50)
    distance = 0
    templateData = {
        'temp' : temp,
        'humid' : humid,
        'light' : light,
        'distance': distance
        }
    return render_template('index.html', **templateData)

if __name__ == '__main__':
    #ser_manager = AiotSerialManager("/dev/ttyACM0")
    #ser_manager.start()
    #ser_manager.open_port()
    cam = CobitOpenCVCam()
    t = Thread(target=cam.run, args=())
    t.daemon = True
    t.start()
    

    socketio.run(app, port=5000)

