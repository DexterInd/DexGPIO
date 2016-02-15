import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
b1_pin=11
b2_pin=12

GPIO.setup(b1_pin,GPIO.IN)
GPIO.setup(b2_pin,GPIO.IN)
while True:
	print "B1: %d B2: %d" %(GPIO.input(b1_pin),GPIO.input(b2_pin))
	