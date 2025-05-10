import cv2
import numpy as np
from PIL import Image, ImageGrab, ImageFilter
import pyautogui
import keyboard
import math
import pynput
import autoit
import time

active = False
isRecording = False
clickArray = []
delay = 0

pyautogui.PAUSE = 0.0005

mouse = pynput.mouse.Controller()

def killSwitch():
	exit()

def paint(location):
	autoit.mouse_click("left", location[0], location[1], 1, 0)
#	mouse.move(location[0], location[1])
#	pyautogui.click(location)

def recordClickLocation():
	global isRecording, clickArray

	if isRecording:
		currentMouseX, currentMouseY = pyautogui.position()
		clickArray.append([currentMouseX, currentMouseY])
		print([currentMouseX, currentMouseY])

def arrayInterlope(arrayVar):
	result = []
	mid = len(arrayVar) // 2

	for n in range(mid):
		result.append(arrayVar[n])
		result.append(arrayVar[-(n+1)])

	if len(arrayVar) % 2 != 0:
		result.append(arrayVar[mid])

	return result

def recordToggle(Wipe):
	global isRecording, clickArray

	isRecording = not isRecording

	if isRecording == True:
		try:
			if Wipe == True:
				print("RECORDING STARTED | Previous Recording Wiped")
				clickArray = []
			elif Wipe == False:
				print("RECORDING STARTED | Adding On To Previous Recording")
		except:
			print("Your lazy ass forgot to assign a variable to \"Wipe\".")
	else:
		print("RECORDING STOPPED")

		clickArray = arrayInterlope(clickArray)

def main():
	global active, clickArray, delay

	if len(clickArray) == 0:
		print("There is nothing in the array silly bill")
		return

	print("Loop Started")

	while True:
		for item in clickArray:
			paint(item)
			if keyboard.is_pressed('q'):
				print("Loop Stopped")
				return
			time.sleep(delay/1000)

def minusFunction():
	global delay
	delay = int(input("Millisecond Delay?\n"))

def recordWipe():
	recordToggle(True)

def recordAdd():
	recordToggle(False)

keyboard.add_hotkey('3', main)
keyboard.add_hotkey('-', minusFunction)
keyboard.add_hotkey('+', recordClickLocation)
keyboard.add_hotkey('[', recordAdd)
keyboard.add_hotkey(']', recordWipe)
keyboard.wait()

#while ks == True:
#	main()
#	ks = False


#
#keyboard.add_hotkey('4', killLoop)


print("done")