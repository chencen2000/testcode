import picamera
from flask import Flask, request, send_file
import time
import io
from PIL import Image
import threading
import logging
import sys

app = Flask(__name__)
quit_event = threading.Event()
save_image_event = threading.Event()
save_complete_event = threading.Event()
image_ready = io.BytesIO()
image_buffer = None
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def preview2():
    global image_buffer
    logging.info("preview: thread is starting...")
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.ISO = 50
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            if save_image_event.is_set():
                image_buffer = stream.getvalue()
                save_complete_event.set()
                save_image_event.clear
            stream.seek(0)
            stream.truncate()
            if quit_event.is_set():
                break
    logging.info("preview: thread is terminated")


def preview():
    global image_ready
    logging.info("preview: thread is starting...")
    stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.ISO = 50
        camera.start_preview()
        time.sleep(2)
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            image = Image.open(stream)
            if save_image_event.is_set():
                # with open("foo.jpg", "w") as f:                
                #     image.save(f)
                if image_ready is None or image_ready.closed:
                    image_ready = io.BytesIO()
                else:
                    image_ready.seek(0)
                    image_ready.truncate()
                image.save(image_ready, format='JPEG')
                save_complete_event.set()
                save_image_event.clear()
            stream.seek(0)
            stream.truncate()
            if quit_event.is_set():
                break
    logging.info("preview: thread is terminated")

@app.route('/')
def hello_world():
    # return 'post data to http://10.1.1.154:5000/sga'
    #return render_template('home.html')
    return "Hello, World!"

@app.route('/preview2')
def preview_getimage2():
    save_image_event.set()
    save_complete_event.wait()
    save_complete_event.clear()
    # image_ready.seek(0)
    img = io.BytesIO(image_buffer)
    return send_file(img, mimetype='image/jpeg')

@app.route('/preview')
def preview_getimage():
    save_image_event.set()
    save_complete_event.wait()
    save_complete_event.clear()
    image_ready.seek(0)
    return send_file(image_ready, mimetype='image/jpeg')

@app.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    logging.info("main: is terminating...")
    return 'Server shutting down...'

if __name__ == '__main__':
    logging.info("main: is starting.")
    # t = threading.Thread(target=preview, daemon=True)
    t = threading.Thread(target=preview2, daemon=True)
    t.start()
    app.run(host='0.0.0.0')
    logging.info("main: shutdown preview thread.")
    quit_event.set()
    t.join()
    logging.info("main: is terminated.")