#--Name=Smiley
#--Icon=Card
#--Main=True

from machine import I2C

i = 0

def main():
	lcd.clear(lcd.WHITE)
	lcd.font(lcd.FONT_Default)
	lcd.print("Left", int(iconPos[0]), 210)
	lcd.print("Exit", int(iconPos[1]), 210)
	lcd.print("Right", int(iconPos[2]), 210)

	buttonA.wasPressed(AButton)
	buttonB.wasPressed(BButton)
	buttonC.wasPressed(CButton)
	Running = True

def AButton():
	global i
	i = i-1
	DisplaySmiley(i)

def BButton():
	myExit()


def CButton():
	global i
	i = i+1
	DisplaySmiley(i)

def DisplaySmiley(num):
	print(num)
	if num == 0
		lcd.image(35, -10, "/flash/res/Happy.jpg")
	elif num == 1:
		lcd.image(35, -10, "/flash/res/Sad.jpg")
	elif num == 2:
		lcd.image(35, -10, "/flash/res/Mad.jpg")


	lcd.print("Left", int(iconPos[0]), 210)
	lcd.print("Exit", int(iconPos[1]), 210)
	lcd.print("Right", int(iconPos[2]), 210)


main()