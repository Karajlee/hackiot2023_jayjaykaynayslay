import spidev
import RPi.GPIO as GPIO
from enum import Enum
import time

spi = spidev.SpiDev()
spi.open(0, 0)  # open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # set SPI clock speed

channel = 0

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def read_adc(channel):
    # MCP3008 expects 3 bytes: start bit, single-ended/differential bit, and channel selection bits
    # We can send 3 bytes at once using spi.xfer2()
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # The ADC returns 10 bits of data, but the first 2 bits are meaningless. We can discard them by taking the last 8 bits.
    adc = ((r[1] & 3) << 8) + r[2]
    return adc

while True:
    if GPIO.input(26) == GPIO.HIGH:
        print("Button was pushed!")

        # update state
        if channel == 0:
            channel = 1
        else:
            channel = 0
        
        print("Channel:", channel)

        while(GPIO.input(26)==GPIO.HIGH):
            time.sleep(15/1000)
    
    value = read_adc(channel)  # read from channel 0
    print("ADC value:", value)
    time.sleep(.5)