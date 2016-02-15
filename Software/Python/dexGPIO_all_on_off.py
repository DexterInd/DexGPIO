#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time


pwm = PWM(0x70)

pwm.setPWMFreq(1000)                        # Set frequency to 60 Hz
while (True):
	# Change speed of continuous servo on channel O
	print "On"
	pwm.setAllPWM(0, 4095)
	time.sleep(1)

	print "Off"
	pwm.setAllPWM(4095, 0)
	time.sleep(1)


