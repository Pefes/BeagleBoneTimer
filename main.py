import Adafruit_BBIO.GPIO as GPIO
from time import sleep
import datetime
import os
import threading
import lcddriver
import i2c_lib

import Adafruit_BBIO.ADC as ADC
ADC.setup()

analogPin="P9_33"

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
    lcd.lcd_clear()
    lcd.lcd_display_string(str(subtitle), 0)  # 2 LINIA 3 zamienione z 2
    return


def clock():
    while (changeMode == 0):
        print(datetime.datetime.now().time())
        lcdPrint(datetime.datetime.now().time())
        wait(1)


def readPotencjometers():
    pot1 = int(round(ADC.read(analogPin) * 60))
    return pot1


def timer():
    while (True and changeMode == 1):
        print("wybor czasu")
        pickedTime = readPotencjometers()
        potVal = readPotencjometers()
        lcdPrint(potVal)
        wait(0.1)
        if (isPushed(b2)):
            #saveTimeToCountDown()
            break

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

    #if (newTimer):
    #   timer()

def addSecond(time):
    wait(0.01)
    return time + 0.01


def chronometer():
    time = 0
    saved = []
    lcdPrint(time)
    countUp = True

    while (True and changeMode == 2):
        print("stoper")
        if (isPushed(b2)):
            break

    wait(0.5)
    while (countUp and changeMode == 2):
        if (isPushed(b2)):
            countUp = not countUp
        if (countUp):
            time = addSecond(time)
        if (isPushed(b3)):
            saved.append(time)
        lcdPrint(time)
        print(time)
        print(saved)

    i = 0
    while (True and changeMode == 2):
        if (isPushed(b2)):
            #i = pickHigher(i)
            i = 0
        if (isPushed(b3)):
            #i = pickLower(i)
            i = 0
        #lcdPrint(saved[i])
        wait(0.1)


def thread_function(name):
    while (True):
        clock()
        chronometer()
        timer()


x = threading.Thread(target = thread_function, args = (1, ))
x.setDaemon(True)
x.start()

while(True):
    if (isPushed(b1)):
        changeMode += 1
        if (changeMode > 2):
            changeMode = 0
        wait(1)