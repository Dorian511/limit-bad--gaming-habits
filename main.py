import keyboard
import pywinctl

badWords = ["shucks", "darn", "job", "jonathan"]

def wordSaid():
    print("You cussed while playing " + pywinctl.getActiveWindowTitle())


for word in badWords:
    keyboard.add_word_listener(word, wordSaid, triggers=["enter", "space"])

keyboard.wait()
