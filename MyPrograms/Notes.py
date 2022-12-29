#--Name=Notes
#--Icon=Qwer
#--Main=True

import time
from machine import I2C
i2c = I2C(sda=21, scl=22)

ExitCounter = 0

def main():
	print("Name: TheFirst FileName")
	print("Icon: Qwer")
	print("Main: True")

	lcd.clear(lcd.WHITE)
	lcd.font(lcd.FONT_Default)
	lcd.print("Save", int(iconPos[0]), 210)
	lcd.print("Undo", int(iconPos[1]), 210)
	lcd.print("Redo", int(iconPos[2]), 210)

	lcd.font(lcd.FONT_DefaultSmall)
	lcd.print("", 0, 20)

	buttonA.wasPressed(AButton)
	buttonB.wasPressed(BButton)
	buttonC.wasPressed(CButton)
	Running = True

def AButton():
	Running = not Running

def BButton():
	global ExitCounter
	ExitCounter += 1
	if ExitCounter >= 5:
		myExit()
	else:
		lcd.print(("Undo " + str(ExitCounter)), int(iconPos[1]), 210)


def CButton():
	print("Dummy Button")

def KeyRead():
	if Running:
		KeyboardData = str(i2c.readfrom(8, 1).decode('cp1252'))
		if KeyboardData != '\x00':
			lcd.print(KeyboardData, color=lcd.BLACK, wrap=True)
		i2c.readfrom(8, 1)


keyboardTimer = machine.Timer(2)
keyboardTimer.init(period=100)
keyboardTimer.callback(KeyRead)

main()