#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time


pwm = PWM(0x70)

pwm.setPWMFreq(1000)                        # Set frequency to 60 Hz

for i in range(128):
	print i
	pwm.setAllPWM(i*16, 4095-i*16)
	time.sleep(.01)



