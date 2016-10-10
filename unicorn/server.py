import paho.mqtt.client as mqtt
import unicornhat as UH
import time, colorsys, thread
import simplejson as json
import random
import numpy as np
from time import sleep
from random import randint
from UHScroll import *
import sys

working = False
contWorking = False

# Set the UH to full white
def uh_setFullColour(r, g, b, brightness = 0.5):
	UH.off()
	UH.brightness(brightness)
	for y in range(8):
		for x in range(8):
			UH.set_pixel(x,y,r,g,b)
	UH.show()

# F1 Style Start
def uh_f1start(b = 0.5):
	UH.off()
	UH.brightness(b)
	UH.rotation(180)
	for x in range(2):
		for y in range(8):
			UH.set_pixel(x,y,255,0,0)
	UH.show()
	sleep(1)
	for x in range(2,4):
		for y in range(8):
			UH.set_pixel(x,y,255,0,0)
	UH.show()
	sleep(1)
	for x in range(4,6):
		for y in range(8):
			UH.set_pixel(x,y,255,0,0)
	UH.show()
	sleep(1)
	for x in range(6,8):
		for y in range(8):
			UH.set_pixel(x,y,255,0,0)
	UH.show()
	delayswitch =  random.random()
	delay = random.random()
	if delayswitch > 0.66:
		sleep(6 + delay)
	elif delayswitch > 0.33:
		sleep(5 + delay)
	else:
		sleep(4 + delay)
	UH.off()

def make_gaussian(fwhm, x0, y0):
	x = np.arange(0, 8, 1, float)
	y = x[:, np.newaxis]
	fwhm = fwhm
	gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
	return gauss

def uh_pulse():
	UH.off()
	global working
	working = True
	global contWorking
	contWorking = True
	while contWorking == True:
		x0, y0 = 3.5, 3.5
		for z in range(1, 5)[::-1] + range(1, 10):
			fwhm = 5/z
			gauss = make_gaussian(fwhm, x0, y0)
			for y in range(8):
				for x in range(8):
					h = 0.8
					s = 0.8
					v = gauss[x,y]
					rgb = colorsys.hsv_to_rgb(h, s, v)
					r = int(rgb[0] * 255.0)
					g = int(rgb[1] * 255.0)
					b = int(rgb[2] * 255.0)
					UH.set_pixel(x, y, r, g, b)
			UH.show()
			time.sleep(0.025)
	UH.off()
	working = False

def light(r,g,b):
	UH.off()
	UH.rotation(180)
	UH.brightness(0.5)
	global working
	working = True
	UH.set_pixel(2,1,r,g,b)
	UH.set_pixel(3,1,r,g,b)
	UH.set_pixel(4,1,r,g,b)
	UH.set_pixel(5,1,r,g,b)
	UH.set_pixel(1,2,r,g,b)
	UH.set_pixel(6,2,r,g,b)
	UH.set_pixel(1,3,r,g,b)
	UH.set_pixel(3,3,r,g,b)
	UH.set_pixel(4,3,r,g,b)
	UH.set_pixel(6,3,r,g,b)
	UH.set_pixel(2,4,r,g,b)
	UH.set_pixel(5,4,r,g,b)
	UH.set_pixel(2,5,r,g,b)
	UH.set_pixel(5,5,r,g,b)
	UH.set_pixel(3,6,r,g,b)
	UH.set_pixel(4,6,r,g,b)
	UH.show()
	time.sleep(2)
	UH.off()
	working = False

def rain():
	UH.off()
	UH.brightness(0.5)
	UH.rotation(0)

	wrd_rgb = [[115, 115, 255], [0, 0, 255], [0, 0, 200], [0, 0, 162], [0, 0, 145], [0, 0, 96], [0, 0, 74], [0, 0, 0,]]

	clock = 0

	blue_pilled_population = [[randint(0,7), 7]]
	while clock <= 60:
		for person in blue_pilled_population:
			y = person[1]
			for rgb in wrd_rgb:
				if (y <= 7) and (y >= 0):
					UH.set_pixel(person[0], y, rgb[0], rgb[1], rgb[2])
				y += 1
			person[1] -= 1
		UH.show()
		time.sleep(0.1)
		clock += 1
		if clock % 5 == 0 and clock <= 50:
			blue_pilled_population.append([randint(0,7), 7])
	UH.off()

def back(r,g,b):
	UH.off()
	UH.rotation(180)
	UH.brightness(0.5)
	global working
	working = True
	UH.set_pixel(3,1,r,g,b)
	UH.set_pixel(2,2,r,g,b)
	UH.set_pixel(1,3,r,g,b)
	UH.set_pixel(1,4,r,g,b)
	UH.set_pixel(2,5,r,g,b)
	UH.set_pixel(3,6,r,g,b)
	UH.show()
	time.sleep(2)
	UH.off()
	working = False

def front(r,g,b):
	UH.off()
	UH.rotation(180)
	UH.brightness(0.5)
	global working
	working = True
	UH.set_pixel(4,1,r,g,b)
	UH.set_pixel(5,2,r,g,b)
	UH.set_pixel(6,3,r,g,b)
	UH.set_pixel(6,4,r,g,b)
	UH.set_pixel(5,5,r,g,b)
	UH.set_pixel(4,6,r,g,b)
	UH.show()
	time.sleep(2)
	UH.off()
	working = False

def house(r,g,b):
	UH.off()
	UH.rotation(180)
	UH.brightness(0.5)
	global working
	working = True
	UH.set_pixel(4,0,r,g,b)
	UH.set_pixel(3,1,r,g,b)
	UH.set_pixel(4,1,r,g,b)
	UH.set_pixel(2,2,r,g,b)
	UH.set_pixel(3,2,r,g,b)
	UH.set_pixel(4,2,r,g,b)
	UH.set_pixel(5,2,r,g,b)
	UH.set_pixel(1,3,r,g,b)
	UH.set_pixel(2,3,r,g,b)
	UH.set_pixel(3,3,r,g,b)
	UH.set_pixel(4,3,r,g,b)
	UH.set_pixel(5,3,r,g,b)
	UH.set_pixel(6,3,r,g,b)
	UH.set_pixel(0,4,r,g,b)
	UH.set_pixel(1,4,r,g,b)
	UH.set_pixel(6,4,r,g,b)
	UH.set_pixel(7,4,r,g,b)
	UH.set_pixel(1,5,r,g,b)
	UH.set_pixel(6,5,r,g,b)
	UH.set_pixel(1,6,r,g,b)
	UH.set_pixel(4,6,r,g,b)
	UH.set_pixel(6,6,r,g,b)
	UH.set_pixel(1,7,r,g,b)
	UH.set_pixel(2,7,r,g,b)
	UH.set_pixel(3,7,r,g,b)
	UH.set_pixel(4,7,r,g,b)
	UH.set_pixel(5,7,r,g,b)
	UH.set_pixel(6,7,r,g,b)
	UH.show()
	time.sleep(2)
	UH.off()
	working = False

def battery(r,g,b):
	UH.off()
	UH.rotation(180)
	UH.brightness(0.5)
	global working
	working = True
	UH.set_pixel(1,2,r,g,b)
	UH.set_pixel(2,2,r,g,b)
	UH.set_pixel(3,2,r,g,b)
	UH.set_pixel(4,2,r,g,b)
	UH.set_pixel(5,2,r,g,b)
	UH.set_pixel(1,3,r,g,b)
	UH.set_pixel(2,3,r,g,b)
	UH.set_pixel(3,3,r,g,b)
	UH.set_pixel(6,3,r,g,b)
	UH.set_pixel(1,4,r,g,b)
	UH.set_pixel(2,4,r,g,b)
	UH.set_pixel(3,4,r,g,b)
	UH.set_pixel(6,4,r,g,b)
	UH.set_pixel(1,5,r,g,b)
	UH.set_pixel(2,5,r,g,b)
	UH.set_pixel(3,5,r,g,b)
	UH.set_pixel(4,5,r,g,b)
	UH.set_pixel(5,5,r,g,b)
	UH.show()
	time.sleep(2)
	UH.off()
	working = False

# Handle command
def handleRequest(req):
	print ("OpCode: " + req['opcode'])
	if (req['opcode'] == '0'):
		UH.off()
	elif (req['opcode'] == '1'):
		if (req['text'] != ''):
			unicorn_scroll(req['text'],'white',150,0.15)
			UH.off()
	elif (req['opcode'] == '2'):
		uh_setFullColour(255,0,0)
	elif (req['opcode'] == '3'):
		uh_setFullColour(255,153,0)
	elif (req['opcode'] == '4'):
		uh_setFullColour(0,255,0)
	elif (req['opcode'] == '5'):
		light(255,255,0)
	elif (req['opcode'] == '6'):
		light(255,255,255)
	elif (req['opcode'] == '7'):
		rain()
	elif (req['opcode'] == '8'):
		back(255,0,0)
	elif (req['opcode'] == '9'):
		front(255,0,0)
	elif (req['opcode'] == '10'):
		house(255,0,0)
	elif (req['opcode'] == '11'):
		house(0,255,0)
	elif (req['opcode'] == '12'):
		battery(255,0,0)
	elif (req['opcode'] == '13'):
		battery(0,255,0)
	elif (req['opcode'] == '14'):
		battery(255,255,0)
	elif (req['opcode'] == '40'):
		try:
			thread.start_new_thread(uh_pulse, ())
		except:
			print "Error: unable to start thread"
	elif (req['opcode'] == '41'):
		global contWorking
		contWorking = False
	elif (req['opcode'] == '50'):
		uh_f1start()
	elif (req['opcode'] == '99'):
		UH.off()
		print ("Exit request received")
		sys.exit(0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
	#print("Connected with result code "+str(rc))

	# Subscribing in on_connect() means that if we lose the connection and
	# reconnect then subscriptions will be renewed.
	client.subscribe("sycamore/unicorn")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print("Request received: " + str(msg.payload))
	req = json.loads(msg.payload)
	handleRequest(req)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.11.2", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

