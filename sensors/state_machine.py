import RPi.GPIO as GPIO
from enum import Enum
import time

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.OUT)  # LED
GPIO.output(12, GPIO.LOW) # OFF

# initialize state
class State(Enum):
    OFF = 1
    ON = 2
    STATE_1 = 3
    STATE_2 = 4
state = State.OFF

while True: 
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")

        # update state
        if state == State.OFF:
            state = State.ON
            GPIO.output(12, GPIO.HIGH)
        elif state == State.ON:
            state = State.STATE_1
            GPIO.output(12, GPIO.HIGH)
        elif state == State.STATE_1:
            state = State.STATE_2
            GPIO.output(12, GPIO.HIGH)
        elif state == State.STATE_2:
            state = State.OFF
            GPIO.output(12, GPIO.LOW)
        
        print("State:", state)

        while(GPIO.input(10)==GPIO.HIGH):
            time.sleep(15/1000)


        