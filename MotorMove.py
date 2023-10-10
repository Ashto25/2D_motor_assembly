from time import sleep
import RPi.GPIO as GPIO
import math
import threading

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
# for r in range(1):
#     GPIO.output(DIR, CW)
#     GPIO.output(DIR2, CW)
#     for x in range(step_count*1):
#         GPIO.output(STEP, GPIO.HIGH)
#         GPIO.output(STEP2, GPIO.HIGH)
#         sleep(delay)
#         GPIO.output(STEP, GPIO.LOW)
#         GPIO.output(STEP2, GPIO.LOW)
#         sleep(delay)
#     GPIO.output(DIR, CCW)
#     GPIO.output(DIR2, CCW)
#     sleep(1)
#     for x in range(step_count*4):
#         GPIO.output(STEP, GPIO.HIGH)
#         GPIO.output(STEP2, GPIO.HIGH)
#         sleep(delay)
#         GPIO.output(STEP, GPIO.LOW)
#         GPIO.output(STEP2, GPIO.LOW)
#         sleep(delay)
#     sleep(1)

motor_speed = 50

actual_x = 0
actual_y = 0


def move_x(steps, time_between):
    steps = int(steps)
    for i in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(time_between)
        GPIO.output(STEP, GPIO.LOW)
        actual_x += 1/int(Selected)

def move_y(steps, time_between):
    steps = int(steps)
    for i in range(steps):
        GPIO.output(STEP2, GPIO.HIGH)
        sleep(time_between)
        GPIO.output(STEP2, GPIO.LOW)
        actual_y += 1/int(Selected)

def moveto(x, y):

    print(f"Moving from ({actual_x}, {actual_y}) to ({x}, {y})")

    sps = motor_speed #* int(Selected)
    c = math.sqrt((actual_x-x)**2 + (actual_y-y)**2)

    time_run_sec = c / motor_speed #sps

    time_between_x = time_run_sec / (abs(x - actual_x) * int(Selected))
    time_between_y = time_run_sec / (abs(y - actual_y) * int(Selected))


    x_offset = (x - actual_x) * int(Selected)
    y_offset = (y - actual_y) *int(Selected)

    #Calculate slope of movement
    #slope = math.floor(y/x)

    #Update motor movement direction
    if x_offset > 0:
        GPIO.output(DIR, CW)
    else:
        GPIO.output(DIR, CCW)
    
    if y_offset > 0:
        GPIO.output(DIR2, CCW)
    else:
        GPIO.output(DIR2, CW)


    threadX = threading.Thread(target=move_x, args=(abs(x_offset), time_between_x))
    threadY = threading.Thread(target=move_y, args=(abs(y_offset), time_between_y))

    threadX.start()
    threadY.start()

    threadX.join()
    threadY.join()
    #sleep(time_run_sec)
    #sleep(1)
    print(f"Done moving, new pos is ({actual_x}, {actual_y})")
    # while x_progress < abs(x_offset) or y_progress < abs(y_offset):




#def circle_x():


def new_circle(radius):
    N = 100 # num of steps for complete revolution
    angle_increment = (2 * math.pi)/ N

    #Temporary (relative movement only for now)
    actual_x = 0
    actual_y = 0


    x_center = actual_x
    y_center = actual_y

    for i in range(N):
        angle = i * angle_increment

        x_pos = x_center + radius * math.cos(angle)
        y_pos = y_center + radius * math.sin(angle)

        moveto(x_pos, y_pos)




#Current position is the bottom ( radian 3pi/2 [0,-1] coordinate) of the circle
def move_circle(radius):

    #sps = motor_speed * int(Selected)
    circumference = 2 * math.pi * radius #2pir
    time_run_sec = circumference / motor_speed # Calculate distance / speed ( = distance / (distance/time) = time * (distance/distance) = time)

    time_between = time_run_sec / (int(Selected) * 4 * radius)

    current_degree = -90
    current_pos_x = 0 # Starts at circle bottom (x middle)
    current_pos_y = -radius # Starts at circle bottom

    #radius_sqrd = radius*radius

    for d in range(int(360 * int(Selected))):
        #rcosx()
        radians = math.radians(current_degree + (d/int(Selected))) # Calculate next angle to go to

        x_offset = (radius * math.cos(radians)) - current_pos_x
        y_offset = (radius * math.sin(radians)) - current_pos_y

        #Update motor movement direction
        if x_offset > 0:
            GPIO.output(DIR, CW)
        else:
            GPIO.output(DIR, CCW)
        
        if y_offset > 0:
            GPIO.output(DIR2, CCW)
        else:
            GPIO.output(DIR2, CW)

        current_pos_x = x_offset
        current_pos_y = y_offset
        
        print(x_offset, y_offset)

        threadX = threading.Thread(target=move_x, args=(abs(x_offset), time_between))
        threadY = threading.Thread(target=move_y, args=(abs(y_offset), time_between))


        threadX.start()
        threadY.start()
        threadX.join()
        threadY.join()
        #sleep(1)


    #     GPIO.output(STEP, GPIO.HIGH)
    #     current_pos_x += (1 / int(Selected))
    #     x_progress += (1 / int(Selected))
    #     if y_progress < abs(y_offset):
    #         y_progress += (1 / int(Selected))
    #         current_pos_y += (1 / int(Selected))
    #         GPIO.output(STEP2, GPIO.HIGH)
    #     sleep(delay)
    #     GPIO.output(STEP, GPIO.LOW)
    #     GPIO.output(STEP2, GPIO.LOW)
    
    # while y_progress < abs(y_offset):
    #     y_progress += (1 / int(Selected))
    #     GPIO.output(STEP2, GPIO.HIGH)
    #     current_pos_y += (1 / int(Selected))
    #     sleep(delay)
    #     GPIO.output(STEP2, GPIO.LOW)


moveto(200,200)
new_circle(20)
moveto(-200,-200)