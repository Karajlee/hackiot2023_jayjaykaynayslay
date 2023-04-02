import RPi.GPIO as GPIO
from enum import Enum
import Adafruit_CharLCD as LCD

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(11, GPIO.OUT)  # Backlight
GPIO.output(11, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)  # LED
GPIO.output(12, GPIO.LOW) # OFF
# GPIO Pins for LCD and Backlight
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


# initialize state
class State(Enum):
    OFF = 1
    ON = 2
    STATE_1 = 3
    STATE_2 = 4
state = State.OFF

def state_2_lcd_messages():
    lcd.clear()
    lcd.message("Message sent to Client")
    print("Message sent to Client")

while True: 
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")

        # update state
        if state == State.OFF:
            state = State.ON
            GPIO.output(12, GPIO.HIGH)
        elif state == State.ON:
            state = State.STATE_1
        elif state == State.STATE_1:
            state = State.STATE_2
            GPIO.output(11, GPIO.HIGH)
            state_2_lcd_messages()
        elif state == State.STATE_2:
            state = State.OFF
            GPIO.output(12, GPIO.LOW)
            GPIO.output(11, GPIO.LOW)
        
        print("State:", state)

        while(GPIO.input(10)==GPIO.HIGH):
            time.sleep(15/1000)


        