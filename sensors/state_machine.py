import RPI.GPIO as GPIO
from enum import Enum, auto

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# initialize state
class State(Enum):
    OFF = auto()
    ON = auto()
    STATE_1 = auto()
    STATE_2 = auto()
state = State.OFF

while True: 
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")

        # update state
        if state == State.OFF:
            state = State.ON
        elif state == State.ON:
            state = State.STATE_1
        elif state == State.STATE_1:
            state = State.STATE_2
        elif state == State.STATE_2:
            state = State.OFF
        
        print("State:", state)


        