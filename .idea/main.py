import datetime
import time
import pywinctl as win
"""
import FreeSimpleGUI as sg


layout = [[sg.Text("Welcome to our game tracker!")],
          [sg.Text("The point is to track your gameplay to make sure you aren't playing games for too long, and to make sure you aren't engaging in any toxic behavior.")]
]

window = sg.Window('Game Tracker', layout)

event, values = window.read()

window.close()
"""

window = ""
lastChange = time.time()

while True:
    time.sleep(1)
    if (win.getActiveWindow().getAppName() != window):    # Checks if the window is the same for an hour
        lastChange = time.time()
        window = win.getActiveWindow().getAppName()
    else:
        if time.time() - lastChange > 10 * 1 * 1:
            print("You have been using " + window + " for too long")            