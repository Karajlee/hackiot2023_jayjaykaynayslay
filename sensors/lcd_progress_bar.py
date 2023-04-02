import RPi.GPIO as GPIO
from enum import Enum
import Adafruit_CharLCD as LCD
import time
import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # set SPI clock speed

channel = 0

def read_adc(channel):
    # MCP3008 expects 3 bytes: start bit, single-ended/differential bit, and channel selection bits
    # We can send 3 bytes at once using spi.xfer2()
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # The ADC returns 10 bits of data, but the first 2 bits are meaningless. We can discard them by taking the last 8 bits.
    adc = ((r[1] & 3) << 8) + r[2]
    return adc

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
# GPIO.setmode(GPIO.BOARD) 
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(11, GPIO.OUT)  # Backlight
# GPIO.output(11, GPIO.LOW)
GPIO.setup(12, GPIO.OUT)  # LED
GPIO.output(12, GPIO.LOW) # OFF
# GPIO Pins for LCD and Backlight

GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

# Initialize squares
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

# Fill squares
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
    time.sleep(0.3)

# Empty squares
col = 14
lcd.create_char(7, empty)
while (col >= 0):
    # Load custom characters into LCD memory
    # Display custom characters using message()
    lcd.message('\n')
    lcd.set_cursor(col, 0)
    lcd.message('\x07')
    lcd.set_cursor(col+1, 0)
    lcd.message('\x07')
    lcd.set_cursor(col, 1)
    lcd.message('\x07')
    lcd.set_cursor(col+1, 1)
    lcd.message('\x07')

    col -= 2
    time.sleep(0.15)

# PEACE
peaceL = [
    0b00000,
    0b00000,
    0b00001,
    0b00001,
    0b00001,
    0b00001,
    0b00000,
    0b00000,
]
peaceM = [
    0b01110,
    0b10101,
    0b00100,
    0b00100,
    0b00100,
    0b01010,
    0b10001,
    0b01110,
]
peaceR = [
    0b00000,
    0b00000,
    0b10000,
    0b10000,
    0b10000,
    0b10000,
    0b00000,
    0b00000,
]
# Load custom characters into LCD memory
lcd.create_char(0, peaceL)
lcd.create_char(1, peaceM)
lcd.create_char(2, peaceR)
# Display custom characters using message()
lcd.message('\n')
lcd.set_cursor(1, 0)
lcd.message('\x00')  # Display heart character
lcd.message('\x01')  # Display smiley character
lcd.message('\x02')  # Display smiley character


# HEART
heartL = (
    0b00110,
    0b01111,
    0b11111,
    0b11111,
    0b01111,
    0b00111,
    0b00011,
    0b00001,
)
heartR = (
    0b01100,
    0b11110,
    0b11111,
    0b11111,
    0b11110,
    0b11100,
    0b11000,
    0b10000,
)
# Load custom characters into LCD memory
lcd.create_char(3, heartL)
lcd.create_char(4, heartR)
# Display custom characters using message()
lcd.message('\n')
lcd.set_cursor(7, 0)
lcd.message('\x03')  # Display heart character
lcd.message('\x04')  # Display smiley character


# CODE
codeL = (
    0b00010,
    0b00100,
    0b01000,
    0b10000,
    0b01000,
    0b00100,
    0b00010,
    0b00000,
)
codeR = (
    0b01000,
    0b00100,
    0b00010,
    0b00001,
    0b00010,
    0b00100,
    0b01000,
    0b00000,
)
# Load custom characters into LCD memory
lcd.create_char(5, codeL)
lcd.create_char(6, codeR)
# Display custom characters using message()
lcd.message('\n')
lcd.set_cursor(12, 0)
lcd.message('\x05')  # Display heart character
lcd.message('\x06')  # Display smiley character


# PEACE LOVE CODE
lcd.set_cursor(0, 1)
lcd.message('Peace Love Code')