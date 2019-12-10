import Adafruit_BBIO.GPIO as GPIO
from time import sleep
import datetime
import os
import threading
import lcddriver
import i2c_lib
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM


changeMode = 0
chronoTime = datetime.datetime(2019, 11, 9, 0, 0, 0, 0)
chronoCount = True

b1="P9_11"
b2="P9_13"
b3="P9_15"
analogPin1="P9_33"
analogPin2="P9_35"

GPIO.setup(b1, GPIO.IN)
GPIO.setup(b2, GPIO.IN)
GPIO.setup(b3, GPIO.IN)


ADC.setup()
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
        lcdPrint(str(datetime.datetime.now().time()).split(".")[0])
        wait(1)


def readPotencjometers():
    pot1 = int(round(ADC.read(analogPin1) * 59))
    pot2 = int(round(ADC.read(analogPin2) * 59))

    return pot1, pot2

def secondLess(pickedTime):
    if pickedTime > datetime.datetime(2019, 11, 9, 0, 0, 0, 0):
        wait(1)
        pickedTime -= datetime.timedelta(seconds = 1)
    return pickedTime

def ringStart():
    PWM.start("P9_21", 25, 1000)

def ringStop():
    PWM.stop("P9_21")


def timer():
    while (True and changeMode == 1):
        print("wybor czasu")
        pickedMinutes, pickedSeconds = readPotencjometers()
        pickedTime = datetime.datetime(2019, 11, 9, 0, pickedMinutes, pickedSeconds, 0)
        lcdPrint(str(pickedTime.time())[3:])

        wait(0.1)
        if (isPushed(b2)):
            break

    stopped = False
    countDown = True
    wait(0.5)

    while (changeMode == 1):
        if countDown:
            pickedTime = secondLess(pickedTime)
            lcdPrint(str(pickedTime.time())[3:])

        wait(1)

        if pickedTime == datetime.datetime(2019, 11, 9, 0, 0, 0, 0):
            if (not stopped):
                ringStart()
            if (isPushed(b2)):
                stopped = True
                ringStop()
                #break


        if isPushed(b2):
            countDown = not(countDown)
            print(countDown)
            wait(0.5)


def addSecond(time):
    wait(0.01)
    return time + 0.01

def chronoCounter():
    chronoTime = datetime.datetime(2019, 11, 9, 0, 0, 0, 0)
    while(changeMode == 2):
        if(chronoCount):
            wait(0.01)
            chronoTime += datetime.timedelta(microseconds = 100000)



def chronometer():
    saved = []
    countUp = True
    count = threading.Thread(target=chronoCounter, args=(1,))
    count.setDaemon(True)
    count.start()

    while (True and changeMode == 2):
        print("stoper")
        if (isPushed(b2)):
            break

    wait(0.5)
    while (changeMode == 2):
        if (isPushed(b2)):
            countUp = not countUp
        if (isPushed(b3)):
            saved.append(chronoTime)
        lcdPrint(str(chronoTime.time())[3:])
        wait(0.5)

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

PWM.cleanup()


while(True):
    if (isPushed(b1)):
        changeMode += 1
        if (changeMode > 2):
            changeMode = 0
        wait(1)







