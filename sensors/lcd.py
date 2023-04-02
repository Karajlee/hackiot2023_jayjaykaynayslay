# import RPi.GPIO as GPIO
# from enum import Enum
# import Adafruit_CharLCD as LCD
# import time

# GPIO.setwarnings(False) 
# # GPIO.setmode(GPIO.BOARD) 
# GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# # GPIO.setup(11, GPIO.OUT)  # Backlight
# # GPIO.output(11, GPIO.LOW)
# GPIO.setup(12, GPIO.OUT)  # LED
# GPIO.output(12, GPIO.LOW) # OFF
# # GPIO Pins for LCD and Backlight

# lcd_rs = 25
# lcd_en = 24
# lcd_d4 = 23
# lcd_d5 = 17
# lcd_d6 = 18
# lcd_d7 = 22
# lcd_backlight = 4

# GPIO.setup(lcd_rs, GPIO.OUT)
# GPIO.output(lcd_rs, GPIO.HIGH)

# GPIO.setup(lcd_en, GPIO.OUT)
# GPIO.output(lcd_en, GPIO.HIGH)

# GPIO.setup(lcd_d4, GPIO.OUT)
# GPIO.output(lcd_d4, GPIO.HIGH)

# GPIO.setup(lcd_d5, GPIO.OUT)
# GPIO.output(lcd_d5, GPIO.HIGH)

# GPIO.setup(lcd_d6, GPIO.OUT)
# GPIO.output(lcd_d6, GPIO.HIGH)

# GPIO.setup(lcd_d7, GPIO.OUT)
# GPIO.output(lcd_d7, GPIO.HIGH)


# lcd_columns = 16
# lcd_rows = 2

# lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
#                            lcd_columns, lcd_rows, lcd_backlight)



# while True:
#     # lcd.clear()
#     lcd.message("Message sent to Client")
#     print("Message sent to Client")

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Define LCD pins
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Initialize the LCD object
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Clear the LCD screen
lcd.clear()

# Print a message on the LCD screen
lcd.message = "Hello, world!"