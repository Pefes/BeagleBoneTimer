import Adafruit_BBIO.GPIO as GPIO
from time import sleep
import datetime
import os
import threading
import lcddriver
import i2c_lib

changeMode = 0


b1="P9_11"
b2="P9_13"
b3="P9_15"
GPIO.setup(b1, GPIO.IN)
GPIO.setup(b2, GPIO.IN)
GPIO.setup(b3, GPIO.IN)

lcd = lcddriver.lcd()

def wait(t):
    sleep(t)

def isPushed(button):
    if GPIO.input(button):
        return True
    else:
        return False


def lcdPrint(subtitle):
    lcd.lcd_display_string(subtitle, 3)  # 2 LINIA 3 zamienione z 2
    return


def clock():
    wait(1)

    while (changeMode == 0):
        print(datetime.datetime.now().time())
        lcdPrint(str(datetime.datetime.now().time()))
        wait(1)



def readPotencjometers():
    return 1
def timer():
    while (True):
        print("wybor czasu")
        pickedTime = readPotencjometers()
        lcdPrint(pickedTime)
        if (isPushed(b2)):
            saveTimeToCountDown()
            break
        if (changeMode != 1):
            return

    stopped = False
    countDown = True
    while (changeMode == 1):
        lcdPrint(pickedTime)
        if countDown:
            secondLess(pickedTime)
        if pickedTime < 0:
            pickedTime = 0
            if (not stopped):
                ring()
            if (isPushed(b2)):
                stopped = True

        if isPushed(b2):
            countDown = not countDown
        if isPushed(b3):
            newTimer = True
            break


    if (newTimer):
        timer()


def chronometer():
    time = 0
    saved = []
    lcdPrint(time)

    while (True):
        print("stoper")
        if (changeMode != 2):
            return
        if (isPushed(b2)):
            break
    while (True):
        if (changeMode != 2):
            break
        if (isPushed(b2)):
            countUp = not countUp
        if (countUp):
            time = addSecond(time)
        if (isPushed(b3)):
            saved.append(time)
        lcdPrint(time)
        #wait(1)

    i = 0
    while (True):

        if (changeMode != 2):
            return
        if (isPushed(b2)):
            i = pickHigher(i)
        if (isPushed(b3)):
            i = pickLower(i)
        lcdPrint(saved[i])
        wait(0.1)


def thread_function(name):
    while (True):
        clock()
        chronometer()
        timer()


x = threading.Thread(target=thread_function, args=(1,))
x.start()

while(True):
    if (isPushed(b1)):
        changeMode += 1
        if (changeMode > 2):
            changeMode = 0
        wait(1)
    #print(changeMode)