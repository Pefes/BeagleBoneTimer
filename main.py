def isPushed(button):
    return


def lcdPrint(subtitle):
    return


def clock():
    while (!isPushed(b1)):
        lcdPrint(systime)
        wait(1)


def timer():
    while (True):
        pickedTime = readPotencjometrs
        lcdPrint(pickedTime)
        if (isPushed(b2)):
            saveTimeToCountDown()
            break
        if (isPushed(b1)):
            return
        wait(0.1)

    while (!isPushed(b1)):
        lcdPrint(pickedTime)
        if countDown:
            secondLess(pickedTime)
        if pickedTime < 0:
            pickedTime = 0
            if (!stopped)
            ring()
    if isPushed(b2):
        countDown = not countDown
    if isPushed(b3):
        newTimer = true
        break


if (newTimer):
    timer()


def chronometer():
    time = 0
    saved = []
    lcdPrint(time)
    while (True):
        if (isPushed(b1)):
            return
        if (isPushed(b2))
            break
    while (True):
        if (isPushed(b1)):
            break
        if (isPushed(b2)):
            countUp = not countUp
        if (countUp):
            time = addSecond(time)
        if (isPushed(b3)):
            saved.append(time)
        lcdPrint(time)
        wait(1)

    i = 0
    while (True):

        if (isPushed(b1)):
            return
        if (isPushed(b2)):
            i = pickHigher(i)
        if (isPushed(b3)):
            i = pickLower(i)
        lcdPrint(saved[i])
        wait(0.1)


while (True):
    clock()
    timer()
    chronometer()