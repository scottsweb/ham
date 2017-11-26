#!/usr/bin/python

import picamera
import os
import shutil
from blinkt import set_clear_on_exit, set_pixel, set_all, show, clear, set_brightness
from time import sleep

set_clear_on_exit()

def forceCopyFile (sfile, dfile):
	if os.path.isfile(sfile):
		shutil.copy2(sfile, dfile)

# wait network etc
sleep(10)

# boot notification
set_pixel(0, 0, 255, 0, 0.1)
show()
sleep(0.5)
clear()
sleep(0.5)

# turn on all the lights
set_all(255, 255, 255, 0.8)
show()
sleep(1)

# take photo
camera = picamera.PiCamera()
camera.brightness = 55
camera.sharpness = 30
camera.contrast = 65
camera.rotation = 270
camera.led = False
camera.iso = 400
camera.color_effects = (128, 128)
camera.capture('/tmp/gas-meter.jpg')
sleep(0.2)

# lights off
clear()

# copy image to network
forceCopyFile( '/tmp/gas-meter.jpg', '/media/ham/homeassistant/gas-meter.jpg')

# stop notification
set_pixel(0, 255, 0, 0, 0.1)
show()
sleep(0.5)
clear()
sleep(0.5)
