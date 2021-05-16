import gc
from sys import modules
import sys
from machine import I2C
import machine

import micropython
micropython.alloc_emergency_exception_buf(100)

class TimerThing(object):
	def __init__(self):
		self.callbackList = []

	def AddCallback(self, callback):
		self.callbackList.append(callback)

	def Update(self, Arg):
		for i in self.callbackList:
			i()

class ButtonHandler(object):
	def __init__(self, key):
		self.key = key
		self.PreviousState = False

		TimerThing.AddCallback(self.cb)

	def wasPressed(self, callback):
		self.callback = callback

	def cb(self):
		if (i2c.readfrom(8, 1)[0] ^ 0xff) & self.key and not self.PreviousState:
			self.callback()
			self.PreviousState = True
		elif not (i2c.readfrom(8, 1)[0] ^ 0xff) & self.key:
			self.PreviousState = False


i2c = I2C(sda=21, scl=22)

if not 8 in i2c.scan():
	print("Gameboy Not Connected")

TimerThing = TimerThing()

interruptTimer = machine.Timer(1)
interruptTimer.init(period=50)
interruptTimer.callback(TimerThing.Update)

buttonLeft 		= ButtonHandler(0x04)
buttonRight 	= ButtonHandler(0x08)
buttonUp 		= ButtonHandler(0x01)
buttonDown		= ButtonHandler(0x02)
buttonA			= ButtonHandler(0x20)
buttonB			= ButtonHandler(0x20)
buttonStart		= ButtonHandler(0x80)
buttonSelect	= ButtonHandler(0x40)


# interruptTimer.init(None)
# f = open("boot.py", "w+")
# f.read()
