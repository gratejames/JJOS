import gc
from sys import modules
import sys
from machine import I2C
import machine

import micropython
micropython.alloc_emergency_exception_buf(100)
FACESmode = None

interruptTimer = machine.Timer(1)
interruptTimer.init(period=50)

if FACESmode == "GAMEBOY":
	class ___TimerCaller(object):
		def __init__(self):
			self.callbackList = []

		def AddCallback(self, callback):
			self.callbackList.append(callback)

		def Update(self, Arg):
			for i in self.callbackList:
				try:
					i()
				except (AttributeError):
					print("AttributeError")
					interruptTimer.deinit()


	class ___ButtonHandler(object):
		def __init__(self, key):
			self.key = key
			self.PreviousState = False

			___TimerCaller.AddCallback(self.cb)

		def wasPressed(self, callback):
			self.callback = callback

		def cb(self):
			try:
				if (i2c.readfrom(8, 1)[0] ^ 0xff) & self.key and not self.PreviousState:
					self.callback()
					self.PreviousState = True
				elif not (i2c.readfrom(8, 1)[0] ^ 0xff) & self.key:
					self.PreviousState = False
			except (OSError):
				print("GAMEBOY NOT ATTACHED")
				interruptTimer.deinit()

	def ___DummyHandler():
		pass

	i2c = I2C(sda=21, scl=22)

	___TimerCaller = ___TimerCaller()

	interruptTimer.callback(___TimerCaller.Update)

	buttonLeft 		= ___ButtonHandler(0x04)
	buttonRight 	= ___ButtonHandler(0x08)
	buttonUp 		= ___ButtonHandler(0x01)
	buttonDown		= ___ButtonHandler(0x02)
	buttonO			= ___ButtonHandler(0x20)
	buttonX			= ___ButtonHandler(0x20)
	buttonStart		= ___ButtonHandler(0x80)
	buttonSelect	= ___ButtonHandler(0x40)

	buttonLeft.wasPressed(___DummyHandler)
	buttonRight.wasPressed(___DummyHandler)
	buttonUp.wasPressed(___DummyHandler)
	buttonDown.wasPressed(___DummyHandler)
	buttonO.wasPressed(___DummyHandler)
	buttonX.wasPressed(___DummyHandler)
	buttonStart.wasPressed(___DummyHandler)
	buttonSelect.wasPressed(___DummyHandler)
else:
	interruptTimer.deinit()



# interruptTimer.deinit()
# f = open("boot.py", "w+")
# f.read()
# f.close()