import cv2
import numpy as np
from PIL import Image, ImageGrab, ImageFilter
import pyautogui
import keyboard
import time
import autoit

active = False
is_recording = False
click_array = []
delay = 0

pyautogui.PAUSE = 0

black_min = (0, 0, 0)
black_max = (70, 70, 70)

def is_within_threshold(pixel, threshold_min=(0, 0, 0), threshold_max=(20, 20, 20), max_diff=20):
    within_range = all(threshold_min[i] <= pixel[i] <= threshold_max[i] for i in range(3))
    balanced = abs(pixel[0] - pixel[1]) <= max_diff and abs(pixel[0] - pixel[2]) <= max_diff and abs(pixel[1] - pixel[2]) <= max_diff
    return within_range and balanced

def paint(location):
    autoit.mouse_click("left", location[0], location[1], 1, 0)

def record_click_location():
    global is_recording, click_array
    if is_recording:
        click_array.append(pyautogui.position())

def array_interlope(array_var):
    result = []
    mid = len(array_var) // 2
    for n in range(mid):
        result.append(array_var[n])
        result.append(array_var[-(n+1)])
    if len(array_var) % 2 != 0:
        result.append(array_var[mid])
    return result

def record_toggle(wipe):
    global is_recording, click_array
    is_recording = not is_recording
    if is_recording:
        if wipe:
            click_array = []
            print("RECORDING STARTED | Previous Recording Wiped")
        else:
            print("RECORDING STARTED | Adding On To Previous Recording")
    else:
        print("RECORDING STOPPED")
        click_array = array_interlope(click_array)

def main():
    global click_array, delay
    if not click_array:
        print("There is nothing in the array")
        return

    print("Loop Started")
    while True:
        for item in click_array:
            target_color = pyautogui.pixel(int(item[0]), int(item[1]))
            if not is_within_threshold(target_color, black_min, black_max):
                paint(item)
            if keyboard.is_pressed('q'):
                print("Loop Stopped")
                return
            time.sleep(delay/1000)

def set_delay():
    global delay
    delay = int(input("Millisecond Delay?\n"))

def record_wipe():
    record_toggle(True)

def record_add():
    record_toggle(False)

keyboard.add_hotkey('3', main)
keyboard.add_hotkey('-', set_delay)
keyboard.add_hotkey('+', record_click_location)
keyboard.add_hotkey('[', record_add)
keyboard.add_hotkey(']', record_wipe)
keyboard.wait()

print("done")