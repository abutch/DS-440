from flask import Flask, render_template, Response, request
import cv2
import mediapipe as mp
import time
import math as m


app = Flask(__name__, template_folder='.')

cap = cv2.VideoCapture(0)

fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (width, height)


def gen_frames():
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def run_script():
    file = open(r'/Users/alexb/Desktop/DS 440/human_posture_analysis_video.py', 'r').read() #replace with user file path
    return exec(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype= 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()
