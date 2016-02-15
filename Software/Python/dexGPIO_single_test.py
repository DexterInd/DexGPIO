#!/usr/bin/env python
import dexGPIO_lib
import time

d= dexGPIO_lib.dexGPIO()
while True:
	for i in range(128):
		print i*32
		# d.setLED(0,i*32)	#Set 1 led
		d.setAllLED(i*32)	#Set all LED's 
		time.sleep(.01)

	for i in range(129):
		print 4095-i*32
		# d.setLED(0,i*32)
		d.setAllLED(4095-i*32)
		time.sleep(.01)