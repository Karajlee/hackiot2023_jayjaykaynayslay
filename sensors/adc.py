import spidev
from gpiozero import MCP3008

spi = spidev.SpiDev()
spi.open(0,0)

adc = MCP3008(channel=0)

while True:

    analog_value=adc.value

    print(analog_value)