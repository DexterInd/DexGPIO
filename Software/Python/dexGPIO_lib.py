#!/usr/bin/env python
import time,sys
import RPi.GPIO as GPIO
import smbus
import math

# use the bus that matches your raspi version
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class dexGPIO:
	address				 = 0x70
	debug				 = 0
	__MODE1              = 0x00
	__MODE2              = 0x01
	__SUBADR1            = 0x02
	__SUBADR2            = 0x03
	__SUBADR3            = 0x04
	__PRESCALE           = 0xFE
	__LED0_ON_L          = 0x06
	__LED0_ON_H          = 0x07
	__LED0_OFF_L         = 0x08
	__LED0_OFF_H         = 0x09
	__ALL_LED_ON_L       = 0xFA
	__ALL_LED_ON_H       = 0xFB
	__ALL_LED_OFF_L      = 0xFC
	__ALL_LED_OFF_H      = 0xFD

	# Bits
	__RESTART            = 0x80
	__SLEEP              = 0x10
	__ALLCALL            = 0x01
	__INVRT              = 0x10
	__OUTDRV             = 0x04

	def write8(self, reg, value):
		try:
			bus.write_byte_data(self.address, reg, value)
		except IOError:
			return -1
		
	def readU8(self, reg):
		"Read an unsigned byte from the I2C device"
		try:
			result = bus.read_byte_data(self.address, reg)
			return result
		except IOError:
			return -1
	  
	def __init__(self):
		if (self.debug):
			print "Reseting PCA9685 MODE1 (without SLEEP) and MODE2"
		self.setAllPWM(0, 0)							#Turn off everything
		# self.write8(self.__MODE2, self.__OUTDRV)
		self.write8(self.__MODE2, self.__INVRT)			#Used to turn on LED, Fig 15 Pg 29	PCA9685 datasheet
		# self.write8(self.__MODE1, self.__ALLCALL)
		time.sleep(0.005)                                       # wait for oscillator

		mode1 = self.readU8(self.__MODE1)
		mode1 = mode1 & ~self.__SLEEP                 # wake up (reset sleep)
		self.write8(self.__MODE1, mode1)
		time.sleep(0.005)                             # wait for oscillator
		self.setPWMFreq();
		
	def setPWMFreq(self):
		prescale=5 			#For 1000Hz
		oldmode = self.readU8(self.__MODE1);
		newmode = (oldmode & 0x7F) | 0x10             # sleep
		self.write8(self.__MODE1, newmode)        # go to sleep
		self.write8(self.__PRESCALE, int(math.floor(prescale)))
		self.write8(self.__MODE1, oldmode)
		time.sleep(0.005)
		self.write8(self.__MODE1, oldmode | 0x80)

	def setPWM(self, channel, on, off):
		"Sets a single PWM channel"
		self.write8(self.__LED0_ON_L+4*channel, on & 0xFF)
		self.write8(self.__LED0_ON_H+4*channel, on >> 8)
		self.write8(self.__LED0_OFF_L+4*channel, off & 0xFF)
		self.write8(self.__LED0_OFF_H+4*channel, off >> 8)

	def setAllPWM(self, on, off):
		"Sets a all PWM channels"
		self.write8(self.__ALL_LED_ON_L, on & 0xFF)
		self.write8(self.__ALL_LED_ON_H, on >> 8)
		self.write8(self.__ALL_LED_OFF_L, off & 0xFF)
		self.write8(self.__ALL_LED_OFF_H, off >> 8)

	def setLED(self,led,pwm_value):
		"Sets the led (0-15) to PWM value (0-4095)"
		self.setPWM(led,0,pwm_value)
		
	def setAllLED(self, pwm_value):
		"Sets all led's (0-15) to PWM value (0-4095)"
		self.setAllPWM(0,pwm_value)
		
if __name__ == "__main__":		
	d= dexGPIO()
	for i in range(128):
		print i*32
		# d.setLED(0,i*32)
		d.setAllLED(i*32)
		time.sleep(.01)
