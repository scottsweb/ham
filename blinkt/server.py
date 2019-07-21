import paho.mqtt.client as mqtt
import time, colorsys, thread
import simplejson as json
import random
from random import randint
from time import sleep
import sys
import blinkt

blinkt.set_clear_on_exit(True)

def show(r, g, b):
	blinkt.set_brightness(0.05)
	blinkt.set_all(255,0,0)
	blinkt.show()
	time.sleep(2)
	blinkt.clear()
	blinkt.show()

def flash(pulse, r, g, b):
	i = 1
	blinkt.set_brightness(0.05)
	while i <= pulse:
		blinkt.set_all(r,g,b)
		blinkt.show()
		time.sleep(0.2)
		blinkt.clear()
		blinkt.show()
		time.sleep(0.2)
		i += 1

def show_graph(v, r, g, b):
	blinkt.set_brightness(0.05)
	v *= blinkt.NUM_PIXELS
	for x in range(blinkt.NUM_PIXELS):
		if v < 0:
			r, g, b = 0, 0, 0
		else:
			r, g, b = [int(min(v, 1.0) * c) for c in [r, g, b]]
		pixel = blinkt.NUM_PIXELS -1 - x
		blinkt.set_pixel(pixel, r, g, b)
		v -= 1
	blinkt.show()
	time.sleep(2)
	blinkt.clear()
	blinkt.show()

def larson():
	blinkt.set_brightness(0.15)
	REDS = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]
	end = time.time() + 2 # 2 seconds
	start = time.time()
	while time.time() <= end:
		delta = (time.time() - start) * 16
		offset = int(abs((delta % len(REDS)) - blinkt.NUM_PIXELS))

		for i in range(blinkt.NUM_PIXELS):
			pixel = blinkt.NUM_PIXELS -1 - i
			blinkt.set_pixel(pixel, REDS[offset + i], 0, 0)

		blinkt.show()
		time.sleep(0.1)
	blinkt.clear()
	blinkt.show()

def guage(target):
	blinkt.set_brightness(0.05)
	LEDS = [
		[0,255,0],
		[120,255,0],
		[255,180,0],
		[255,120,0],
		[255,60,0],
		[255,20,0],
		[255,0,0],
		[255,0,0]
	]

	for i in range(blinkt.NUM_PIXELS):
		pixel = blinkt.NUM_PIXELS -1 - i
		blinkt.set_pixel(pixel, LEDS[i][0], LEDS[i][1], LEDS[i][2])
		blinkt.show()
		time.sleep(0.1)

	while i >= target:
		pixel = blinkt.NUM_PIXELS -1 - i
		blinkt.set_pixel(pixel, 0, 0, 0)
		blinkt.show()
		time.sleep(0.1)
		i -= 1

	time.sleep(4)
	blinkt.clear()
	blinkt.show()

def rdom(r,g,b,speed,density):
	end = time.time() + 2 # 2 seconds
	while time.time() <= end:
		pixels = random.sample(range(blinkt.NUM_PIXELS), random.randint(1, density))
		for i in range(blinkt.NUM_PIXELS):
			if i in pixels:
				blinkt.set_pixel(i, r, g, b)
			else:
				blinkt.set_pixel(i, 0, 0, 0)
		blinkt.show()
		time.sleep(speed)
	blinkt.clear()
	blinkt.show()

# Handle command
def handleRequest(req):

	if 'opcode' in req:
		print ("OpCode: " + req['opcode'])

		if (req['opcode'] == '0'):
			blinkt.clear()
			blinkt.show()
		elif (req['opcode'] == '2'):
			show(255,0,0)
		elif (req['opcode'] == '3'):
			show(255,153,0)
		elif (req['opcode'] == '4'):
			show(0,255,0)
		elif (req['opcode'] == '7'):
			rdom(0,0,255,0.3,4) # Rain
		elif (req['opcode'] == '10'):
			flash(5,255,0,0) # away
		elif (req['opcode'] == '11'):
			flash(5,0,255,0) # home
		elif (req['opcode'] == '12'):
			guage(8) # high power
		elif (req['opcode'] == '13'):
			guage(2) # low power
		elif (req['opcode'] == '14'):
			guage(5) # medium power
		elif (req['opcode'] == '15'):
			rdom(245,245,255,0.8,2) # Snow
		elif (req['opcode'] == '99'):
			blinkt.clear()
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

client.connect("192.168.11.3", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
