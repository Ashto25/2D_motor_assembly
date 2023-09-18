from time import sleep
import RPi.GPIO as GPIO

DIR = 20
STEP = 21

DIR2 = 19
STEP2 = 26

CW = 1
CCW = 0
SPR = 200

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
GPIO.output(DIR, CW)
GPIO.output(DIR2, CW)

MODE = (14, 15, 18) #GPIO Microstepping Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'1':(0,0,0),
              '4':(0,1,0),
              '8':(1,1,0),
              '16':(0,0,1),
              '32':(1,0,1)}
Selected = '16'
GPIO.output(MODE, RESOLUTION[Selected])

step_count = SPR * int(Selected)
delay = 1 / step_count / 5
for r in range(10):
    GPIO.output(DIR, CW)
    GPIO.output(DIR2, CW)
    for x in range(step_count*4):
        GPIO.output(STEP, GPIO.HIGH)
        GPIO.output(STEP2, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        GPIO.output(STEP2, GPIO.LOW)
        sleep(delay)
    GPIO.output(DIR, CCW)
    GPIO.output(DIR2, CCW)
    sleep(1)
    for x in range(step_count*4):
        GPIO.output(STEP, GPIO.HIGH)
        GPIO.output(STEP2, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        GPIO.output(STEP2, GPIO.LOW)
        sleep(delay)
    sleep(1)

    
