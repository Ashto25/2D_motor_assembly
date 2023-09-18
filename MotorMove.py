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
# Motor Num.1
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
#Motor Num.2
GPIO.setup(DIR2, GPIO.OUT)
GPIO.setup(STEP2, GPIO.OUT)
#Motor Num1,2 set to clockwise motion
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
#Setup microstepping
GPIO.output(MODE, RESOLUTION[Selected])

#Steps per rotation after microstepping selection
step_count = SPR * int(Selected)
#Delay between steps
delay = 1 / step_count / 5


#Move in test motion back and forth
for r in range(1):
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

    
