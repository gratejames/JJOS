#--Name=TheFirst FileName
#--Icon=Qwer
#--Main=True

ExitCounter = 0

def main():
	print("Name: TheFirst FileName")
	print("Icon: Qwer")
	print("Main: True")

	lcd.clear(lcd.WHITE)
	lcd.print("C-Dummy", int(iconPos[2]), 210)

	buttonA.wasPressed(AButton)
	buttonB.wasPressed(BButton)
	buttonC.wasPressed(CButton)

def AButton():
	lcd.font(lcd.FONT_Default)
	lcd.print("A-Print", int(iconPos[0]), 210)
	lcd.print("B-Exit 0", int(iconPos[1]), 210)

def BButton():
	global ExitCounter
	ExitCounter += 1
	if ExitCounter >= 3:
		myExit()
	else:
		lcd.print(("B-Exit " + str(ExitCounter)), int(iconPos[1]), 210)


def CButton():
	print("Dummy Button")

main()