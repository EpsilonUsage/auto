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

pyautogui.PAUSE = 0

mouse = pynput.mouse.Controller()

black_min = (0, 0, 0)
black_max = (75, 75, 75)

def is_within_threshold(pixel, threshold_min=(0, 0, 0), threshold_max=(20, 20, 20), max_diff=20):
	within_range = all(threshold_min[i] <= pixel[i] <= threshold_max[i] for i in range(3))

	balanced = (
		abs(pixel[0] - pixel[1]) <= max_diff and
		abs(pixel[0] - pixel[2]) <= max_diff and
		abs(pixel[1] - pixel[2]) <= max_diff
	)

	return within_range and balanced

def killSwitch():
	exit()

def paint(location):
	autoit.mouse_click("left", location[0], location[1], 1, 0)
#	mouse.move(location[0], location[1])
	pyautogui.click()

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
			target_color = pyautogui.pixel(item[0], item[1])
			
			if not is_within_threshold(target_color, black_min, black_max):
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