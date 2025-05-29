### Library Imports ###
from PIL import ImageGrab
import pyautogui
import keyboard
import time
import autoit
import asyncio

### Variables ###
is_recording = False
click_array = []
delay = 0

using_color = (0, 0, 0) # default
color_min = [x - 20 for x in using_color]
color_max = [x + 20 for x in using_color]

### Program Functionality Variables ###
pyautogui.PAUSE = 0
tasks = []

### Emergency Use
kill_flag = False

### Functions ###
def switchColor():
    global color_min, color_max
    temp_position = pyautogui.position()
    using_color = pyautogui.pixel(temp_position[0], temp_position[1])
    color_min = [x - 20 for x in using_color]
    color_max = [x + 20 for x in using_color]
    print("Color Switched")
#    print(using_color)
#    print(color_min)
#    print(color_max)

def is_within_threshold(pixel, threshold_min=(0, 0, 0), threshold_max=(20, 20, 20), max_diff=256):
    within_range = all(threshold_min[i] <= pixel[i] <= threshold_max[i] for i in range(3))
    balanced = abs(pixel[0] - pixel[1]) <= max_diff and abs(pixel[0] - pixel[2]) <= max_diff and abs(pixel[1] - pixel[2]) <= max_diff
#   print(within_range)
#   print(balanced)
    return within_range and balanced

def paint(location):
    autoit.mouse_click("left", location[0], location[1], 1, 0)

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

def set_delay():
    global delay
    delay = int(input("Millisecond Delay?\n"))

def record_wipe():
    record_toggle(True)

def record_add():
    record_toggle(False)

def record_click_location():
    global is_recording, click_array
    if is_recording:
        click_array.append(pyautogui.position())

### Main Code ###
async def trackLocation(task_id, coordinate): # This will be running for each member of a table
    try:
        while not kill_flag:
            await asyncio.sleep(0)
            
            target_color = pyautogui.pixel(int(coordinate[0]), int(coordinate[1]))
#            print('2')
            if not is_within_threshold(target_color, color_min, color_max):
                paint(coordinate)
                await asyncio.sleep(delay/1000)
#            print('3')
    except asyncio.CancelledError:
        print(f"Task {task_id} killed.")




async def cancelTasks():
    global kill_flag
    kill_flag = True

    for task in tasks:
        task.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    print("All coroutines killed")

async def monitor_killSwitch():
    global kill_flag

    while not kill_flag:
        await asyncio.sleep(0.1)
        if keyboard.is_pressed("q"):
            kill_flag = True

            for task in tasks:
                task.cancel()

            await asyncio.gather(*tasks, return_exceptions=True)

            print("All coroutines killed")

async def createTasks(items):
    global tasks
    item_count = len(items)
    tasks = [asyncio.create_task(trackLocation(task_id, item)) for task_id, item in enumerate(items)]
    killSwitchListener = asyncio.create_task(monitor_killSwitch())

    print(f"Tracking {item_count} tasks.")

    await asyncio.gather(*tasks, killSwitchListener, return_exceptions=True)

def cancel_middle_function():
    asyncio.run(cancelTasks())

#async def createCoroutines(items):
#    await createTasks(items)

def main():
    global click_array, delay, kill_flag
    if not click_array:
        print("There is nothing in the array")
        return

    kill_flag = False
    asyncio.run(createTasks(click_array))

keyboard.add_hotkey('3', main)
keyboard.add_hotkey('-', set_delay)
keyboard.add_hotkey('+', record_click_location)
keyboard.add_hotkey('[', record_add)
keyboard.add_hotkey(']', record_wipe)
keyboard.add_hotkey(';', switchColor)
keyboard.add_hotkey('q', cancel_middle_function)
keyboard.wait()

print("done")