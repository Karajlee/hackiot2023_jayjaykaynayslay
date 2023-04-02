import RPi.GPIO as GPIO
from enum import Enum
import Adafruit_CharLCD as LCD
import time

GPIO.setwarnings(False) 
# GPIO.setmode(GPIO.BOARD) 
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(11, GPIO.OUT)  # Backlight
# GPIO.output(11, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)  # LED
GPIO.output(12, GPIO.LOW) # OFF
# GPIO Pins for LCD and Backlight

lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 12

GPIO.setup(lcd_rs, GPIO.OUT)
GPIO.output(lcd_rs, GPIO.HIGH)

GPIO.setup(lcd_en, GPIO.OUT)
GPIO.output(lcd_en, GPIO.HIGH)

GPIO.setup(lcd_d4, GPIO.OUT)
GPIO.output(lcd_d4, GPIO.HIGH)

GPIO.setup(lcd_d5, GPIO.OUT)
GPIO.output(lcd_d5, GPIO.HIGH)

GPIO.setup(lcd_d6, GPIO.OUT)
GPIO.output(lcd_d6, GPIO.HIGH)

GPIO.setup(lcd_d7, GPIO.OUT)
GPIO.output(lcd_d7, GPIO.HIGH)

GPIO.setup(lcd_backlight, GPIO.OUT)
# GPIO.output(lcd_backlight, GPIO.HIGH)

# GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(lcd_backlight, 100)

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Filled square
fill = (
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
)

col = 0
lcd.create_char(0, fill)
while (col != 16):
    # Load custom characters into LCD memory
    # Display custom characters using message()
    lcd.message('\n')
    lcd.set_cursor(col, 0)
    lcd.message('\x00')
    lcd.set_cursor(col+1, 0)
    lcd.message('\x00')
    lcd.set_cursor(col, 1)
    lcd.message('\x00')
    lcd.set_cursor(col+1, 1)
    lcd.message('\x00')

    col += 2
    time.sleep(1)

# Empty square
empty = (
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
)
col = 14
lcd.create_char(0, empty)
while (col != 0):
    # Load custom characters into LCD memory
    # Display custom characters using message()
    lcd.message('\n')
    lcd.set_cursor(col, 0)
    lcd.message('\x00')
    lcd.set_cursor(col+1, 0)
    lcd.message('\x00')
    lcd.set_cursor(col, 1)
    lcd.message('\x00')
    lcd.set_cursor(col+1, 1)
    lcd.message('\x00')

    col -= 2
    time.sleep(2)