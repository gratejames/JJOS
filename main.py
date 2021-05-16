from m5stack import *
from m5ui import *
import os
import re



keys = {
	"K_X":		0x20,
	"K_DOWN":	0x02,
	"K_LEFT":	0x04,
	"K_RIGHT":	0x08,
	"K_UP":		0x01,
	"K_O":		0x10,
	"K_SELECT":	0x40,
	"K_START":	0x80,
}

def getGameBoyPressed(key):
	if key in keys:
		return (i2c.readfrom(8, 1)[0] ^ 0xff) & key

x = 1
iconPos = []
while x <= 3:
	iconPos.append(((320/3)-13)*(x)-35)
	x += 1


currentDirDict = {}
currentDirOptions = []

placeInCDO = 0

currentFolder = '/flash/Home'

def myExit():
	print("Exiting...")
	loadFolder(currentFolder)
	buttonA.wasPressed(NavigateLeftInFolder)
	buttonB.wasPressed(SelectInFolder)
	buttonC.wasPressed(NavigateRightInFolder)
	buttonLeft.wasPressed(NavigateLeftInFolder)
	buttonSelect.wasPressed(SelectInFolder)
	buttonRight.wasPressed(NavigateRightInFolder)

try:
	os.mkdir(currentFolder)
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
		lcd.text(5, 5, currentFolder)
	lcd.rect(48, 48, 120, 100, lcd.WHITE, lcd.WHITE)
	lcd.font(lcd.FONT_DejaVu18)

	nameOfFile = currentDirDict[currentDirOptions[place]]["Name"]
	name1, name2, name3 = WrapLine(nameOfFile)
	print("Current Option: " + nameOfFile)

	lcd.image(175, 55, "/flash/res/" + currentDirDict[currentDirOptions[place]]["Icon"] + ".jpg")

	lcd.print(name1, 50, 50)
	lcd.print(name2, 50, 80)
	lcd.print(name3, 50, 110)

	placeInCDO = place

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
		dicty["Name"] = fileName.replace(currentFolder, "")
		dicty["Icon"] = "File"
		dicty["Main"] = True
	return dicty

def backPath(path):
	path = path.replace("\\", "/")
	pathList = path.split("/")
	newPath = "/".join(pathList[:-1])
	return newPath

def loadFolder(folderName):
	global currentFolder, currentDirDict, currentDirOptions
	currentDirDict = {}
	currentDirOptions = []
	currentDirDict = {}
	for i in os.listdir(folderName):
		path = folderName + "/" + i
		metadata = loadFile(path)
		currentDirDict[i] = metadata
		currentDirOptions.append(i)

	if folderName != "/flash/Home":
		backDict = {
			"Name": "../",
			"Icon": "File",
			"Main": True,
			"Path": backPath(currentFolder),
		}
		currentDirDict["../"] = backDict
		currentDirOptions.append("../")

	currentDirOptions.sort()

	loadPlaceInCDO(0, True)
	
def NavigateLeftInFolder():
	global placeInCDO, currentDirOptions
	if placeInCDO <= 0:
		placeInCDO = len(currentDirOptions)-1
	else:
		placeInCDO += -1
	loadPlaceInCDO(placeInCDO)

def SelectInFolder():
	global currentFolder, currentDirDict, currentDirOptions
	if currentDirDict[currentDirOptions[placeInCDO]]["Name"] == "/":
		typeOfItem = "Current Working Directory"
	elif not "." in currentDirOptions[placeInCDO] or currentDirOptions[placeInCDO] == "../":
		typeOfItem = "Folder"
	else:
		typeOfItem = "File"


	print()
	print("===================CLICKED===================")
	print("Name:   " + currentDirDict[currentDirOptions[placeInCDO]]["Name"])
	print("Icon:   " + currentDirDict[currentDirOptions[placeInCDO]]["Icon"])
	print("File:   " + currentDirOptions[placeInCDO])
	print("Path:   " + currentDirDict[currentDirOptions[placeInCDO]]["Path"])
	print("Type:   " + typeOfItem)
	print("In dir: " + str(currentDirOptions[placeInCDO] in os.listdir(currentFolder)))
	print("=============================================")
	print()

	if typeOfItem == "Current Working Directory":
		print("Doing CWD (ie. NOTHING)")
		print("Did CWD Stuff")
	elif typeOfItem == "Folder":
		print("Doing Folder Stuff")
		print("Loading 2 Folder: " + currentDirDict[currentDirOptions[placeInCDO]]["Path"])
		currentFolder = currentDirDict[currentDirOptions[placeInCDO]]["Path"]
		print("Loading 1 Folder: " + currentFolder)
		loadFolder(currentFolder)
		print("Did Folder Stuff")
	else:
		print("Doing Program Stuff")
		file = currentDirOptions[placeInCDO]
		path = currentDirDict[currentDirOptions[placeInCDO]]["Path"]
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
	global placeInCDO, currentDirOptions
	if placeInCDO >= len(currentDirOptions)-1:
		placeInCDO = 0
	else:
		placeInCDO += 1
	loadPlaceInCDO(placeInCDO)

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
	global currentFolder, currentDirDict, currentDirOptions
	lcd.tft_writecmd(0x21)
	lcd.clear(lcd.WHITE)
	print("RUNNING MAIN v2.0")

	ScreenHeight = 240
	ScreenWidth  = 320

	lcd.setCursor(0, 0)

	loadFolder(currentFolder)
	buttonA.wasPressed(NavigateLeftInFolder)
	buttonB.wasPressed(SelectInFolder)
	buttonC.wasPressed(NavigateRightInFolder)
	buttonLeft.wasPressed(NavigateLeftInFolder)
	buttonSelect.wasPressed(SelectInFolder)
	buttonRight.wasPressed(NavigateRightInFolder)

main()
#Icons by https://icons8.com