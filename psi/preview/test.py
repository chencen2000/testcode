import logging
import sys
import picamera
import io
import threading
import time
from fractions import Fraction

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def take_image():
    logging.info("take_image: ++")
    with picamera.PiCamera() as c:
        c.resolution = (3280, 2464)
        c.ISO = 50
        c.capture("take_image_0.jpg")
        analog_gain = c.analog_gain
        iso = c.ISO
        awb_gains = c.awb_gains

    logging.info("take_image: --")

def take_image_1():
    logging.info("take_image_1: ++")
    with picamera.PiCamera() as c:
        c.resolution = (3280, 2464)
        c.ISO = 100
        c.awb_mode = 'off'
        c.exposure_mode = 'off'
        c.exposure_compensation = 0
        # c.exposure_speed = 33243
        # c.analog_gain = Fraction(737, 256)
        # c.digital_gain = Fraction(257, 256)
        c.shutter_speed = 75000
        c.awb_gains = (Fraction(155, 128), Fraction(367, 128))
        time.sleep(0.05)
        c.capture("take_image_1.jpg")
    logging.info("take_image_1: --")

logging.info("start: ++")
take_image()
take_image_1() 
logging.info("start: --")