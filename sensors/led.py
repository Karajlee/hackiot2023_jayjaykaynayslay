import RPi.GPIO as GPIO
from enum import Enum
import Adafruit_CharLCD as LCD
import time

GPIO.setwarnings(False) 

GPIO.setup(13, GPIO.OUT)
pwm = GPIO.PWM(13, 100)

state=0
pwm.start(0)
curr = 5

while True:
    if(state==0):
        while(curr<=100):
            pwm.ChangeDutyCycle(curr)
            curr += 5
        state = 1
    if(state==1):
        while(curr>=0):
            pwm.ChangeDutyCycle(curr)
            curr -= 5
        state = 0
