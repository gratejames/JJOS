from m5stack import *
from m5ui import *
import os
import re

x = 1
iconPos = []
while x <= 3:
	iconPos.append(((320/3)-13)*(x)-35)
	x += 1

del x

___currentDirDict = {}
___currentDirOptions = []

___placeInCDO = 0

___currentFolder = '/flash/Home'

def myExit():
	print("Exiting...")
	loadFolder(___currentFolder)
	buttonA.wasPressed(NavigateLeftInFolder)
	buttonB.wasPressed(SelectInFolder)
	buttonC.wasPressed(NavigateRightInFolder)
	if FACESmode == "GAMEBOY":
		buttonLeft.wasPressed(NavigateLeftInFolder)
		buttonSelect.wasPressed(SelectInFolder)
		buttonRight.wasPressed(NavigateRightInFolder)

try:
	os.mkdir(___currentFolder)
except OSError:
	pass

def WrapLine(nameOfFile):
	name1 = nameOfFile
	while lcd.textWidth(name1) >= 120:
		name1 = name1[:-1]

	name2 = nameOfFile[len(name1):]
	while lcd.textWidth(name2) >= 120:
		name2 = name2[:-1]

	name3 = nameOfFile[len(name1) + len(name2):]
	while lcd.textWidth(name3) >= 120:
		name3 = name3[:-1]


	try:
		name2 = name2[1:] if name2[0] == " " else name2
	except (IndexError):
		pass

	try:
		name3 = name3[1:] if name3[0] == " " else name3
	except (IndexError):
		pass

	return name1, name2, name3
def loadPlaceInCDO(place, redraw=False):
	if redraw:
		lcd.clear(lcd.WHITE)
		drawControlBar()
		lcd.setTextColor(color=lcd.BLACK, bcolor=lcd.WHITE)
		lcd.rect(30, 30, 260, 150)
		lcd.font(lcd.FONT_Default)
		lcd.text(5, 5, ___currentFolder)
	lcd.rect(48, 48, 120, 100, lcd.WHITE, lcd.WHITE)
	lcd.font(lcd.FONT_DejaVu18)

	nameOfFile = ___currentDirDict[___currentDirOptions[place]]["Name"]
	name1, name2, name3 = WrapLine(nameOfFile)
	print("Current Option: " + nameOfFile)

	lcd.image(175, 55, "/flash/res/" + ___currentDirDict[___currentDirOptions[place]]["Icon"] + ".jpg")

	lcd.print(name1, 50, 50)
	lcd.print(name2, 50, 80)
	lcd.print(name3, 50, 110)

	___placeInCDO = place

def loadFile(fileName):
	dicty = {}
	if "." in fileName:
		N = 3
		with open(fileName, 'r') as f:    
			for i in range(N):
				line = next(f).strip()
				dicty[line[3:7]] = line[8:]
		dicty["Path"] = fileName
	else:
		dicty["Path"] = fileName
		dicty["Name"] = fileName.replace(___currentFolder, "")
		dicty["Icon"] = "File"
		dicty["Main"] = True
	return dicty

def backPath(path):
	path = path.replace("\\", "/")
	pathList = path.split("/")
	newPath = "/".join(pathList[:-1])
	return newPath

def loadFolder(folderName):
	global ___currentFolder, ___currentDirDict, ___currentDirOptions
	___currentDirDict = {}
	___currentDirOptions = []
	___currentDirDict = {}
	for i in os.listdir(folderName):
		path = folderName + "/" + i
		metadata = loadFile(path)
		___currentDirDict[i] = metadata
		___currentDirOptions.append(i)

	if folderName != "/flash/Home":
		backDict = {
			"Name": "../",
			"Icon": "File",
			"Main": True,
			"Path": backPath(___currentFolder),
		}
		___currentDirDict["../"] = backDict
		___currentDirOptions.append("../")

	___currentDirOptions.sort()

	loadPlaceInCDO(0, True)
	
def NavigateLeftInFolder():
	global ___placeInCDO, ___currentDirOptions
	if ___placeInCDO <= 0:
		___placeInCDO = len(___currentDirOptions)-1
	else:
		___placeInCDO += -1
	loadPlaceInCDO(___placeInCDO)

def SelectInFolder():
	global ___currentFolder, ___currentDirDict, ___currentDirOptions
	if ___currentDirDict[___currentDirOptions[___placeInCDO]]["Name"] == "/":
		typeOfItem = "Current Working Directory"
	elif not "." in ___currentDirOptions[___placeInCDO] or ___currentDirOptions[___placeInCDO] == "../":
		typeOfItem = "Folder"
	else:
		typeOfItem = "File"


	print()
	print("===================CLICKED===================")
	print("Name:   " + ___currentDirDict[___currentDirOptions[___placeInCDO]]["Name"])
	print("Icon:   " + ___currentDirDict[___currentDirOptions[___placeInCDO]]["Icon"])
	print("File:   " + ___currentDirOptions[___placeInCDO])
	print("Path:   " + ___currentDirDict[___currentDirOptions[___placeInCDO]]["Path"])
	print("Type:   " + typeOfItem)
	print("In dir: " + str(___currentDirOptions[___placeInCDO] in os.listdir(___currentFolder)))
	print("=============================================")
	print()

	if typeOfItem == "Current Working Directory":
		print("Doing CWD (ie. NOTHING)")
		print("Did CWD Stuff")
	elif typeOfItem == "Folder":
		print("Doing Folder Stuff")
		print("Loading 2 Folder: " + ___currentDirDict[___currentDirOptions[___placeInCDO]]["Path"])
		___currentFolder = ___currentDirDict[___currentDirOptions[___placeInCDO]]["Path"]
		print("Loading 1 Folder: " + ___currentFolder)
		loadFolder(___currentFolder)
		print("Did Folder Stuff")
	else:
		print("Doing Program Stuff")
		file = ___currentDirOptions[___placeInCDO]
		path = ___currentDirDict[___currentDirOptions[___placeInCDO]]["Path"]
		modulePath = path.replace(".py", "")

		print("Executing " + path)


		with open(path, "r") as f:
			file = f.read()
			exec(file)

		print("Did File Stuff")

def dotPath(path):
	path = path.replace("\\", "/")
	pathList = path.split("/")
	if pathList[0] == '':
		pathList = pathList[1:]
	while 'flash' in pathList:
		pathList = pathList[1:]

	newPath = ".".join(pathList)
	return newPath

def NavigateRightInFolder():
	global ___placeInCDO, ___currentDirOptions
	if ___placeInCDO >= len(___currentDirOptions)-1:
		___placeInCDO = 0
	else:
		___placeInCDO += 1
	loadPlaceInCDO(___placeInCDO)

def findAll(find, text):
	li = []
	for m in re.finditer(find, text):
		li.append(m.group())
	return(li)

def drawControlBar():
	lcd.line(0, 200, 320, 200, 0x000000)
	lcd.image(int(iconPos[0]), 210, "res/left.jpg")
	lcd.image(int(iconPos[1]), 210, "res/center.jpg")
	lcd.image(int(iconPos[2]), 210, "res/right.jpg")

def main():
	global ___currentFolder, ___currentDirDict, ___currentDirOptions
	lcd.tft_writecmd(0x21)
	lcd.clear(lcd.WHITE)
	print("RUNNING MAIN v2.0")

	ScreenHeight = 240
	ScreenWidth  = 320

	lcd.setCursor(0, 0)

	loadFolder(___currentFolder)
	buttonA.wasPressed(NavigateLeftInFolder)
	buttonB.wasPressed(SelectInFolder)
	buttonC.wasPressed(NavigateRightInFolder)
	if FACESmode == "GAMEBOY":
		buttonLeft.wasPressed(NavigateLeftInFolder)
		buttonSelect.wasPressed(SelectInFolder)
		buttonRight.wasPressed(NavigateRightInFolder)

main()
#Icons by https://icons8.com