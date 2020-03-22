import logging
import sys
import picamera
import io
import threading
from flask import Flask, request, send_file, Response

app = Flask(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" />
</body>
</html>
"""
# <img src="stream.mjpg" width="640" height="480" />

image_frame=None
quit_event = threading.Event()
save_image_event = threading.Event()
save_complete_event = threading.Event()

def get_frame():
    save_complete_event.clear()
    save_image_event.set()
    save_complete_event.wait()
    logging.info("frame: gen.")
    return image_frame

def capture_image():
    global image_frame
    with picamera.PiCamera() as camera:
        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            # with open("foo.jpg", "wb") as f:
            #     f.write(stream.getvalue())
            # break
            if quit_event.is_set():
                break
            if save_image_event.is_set():
                image_frame = stream.getvalue()
                save_complete_event.set()
                save_image_event.clear()
            stream.seek(0)
            stream.truncate()

@app.route('/')
def index():
    return PAGE

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    logging.info("main: is terminating...")
    return 'Server shutting down...'

def gen():
    while True:
        frame = get_frame()
        m = io.BytesIO()
        m.write(b'--frame\r\n')
        m.write(b'Content-Type: image/jpeg\r\n')
        s = "Content-Length: %d\r\n\r\n" % len(frame)
        m.write(s.encode('utf-8'))
        m.write(frame)
        m.write(b'\r\n')
        yield (m.getvalue())
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream.mjpg')
def preview():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
    

if __name__ == '__main__':
    logging.info("start: ++")
    t = threading.Thread(target=capture_image, daemon=True)
    t.start()
    app.run(host="0.0.0.0")
    quit_event.set()
    t.join()
    logging.info("start: --")