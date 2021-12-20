import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 2
GPIO_ECHO = 3
PUMP_OUT = 4

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(PUMP_OUT, GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    counter1 = 0
    counter2 = 0

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        counter1 += 1
        if counter1 > 5000:
            print("Lost Echo Low")
            return 0

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        counter2 += 1
        if counter2 > 5000:
            print("Lost Echo High")
            return 0

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(0.5)
            if dist > 6:
                GPIO.output(PUMP_OUT, True)
                print("Pump is ON")
                time.sleep(3)
            else:
                GPIO.output(PUMP_OUT, False)
                time.sleep(1)
    except Exception as e:
            print(str(e))