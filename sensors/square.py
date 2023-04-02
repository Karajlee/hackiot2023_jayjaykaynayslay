import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN)

while True:
    adc_value = GPIO.input(26)
    print("ADC value: {}".format(adc_value))
    time.sleep(0.1)
