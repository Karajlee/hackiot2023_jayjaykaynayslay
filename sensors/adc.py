import spidev

spi = spidev.SpiDev()
spi.open(0, 0)  # open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # set SPI clock speed

def read_adc(channel):
    # MCP3008 expects 3 bytes: start bit, single-ended/differential bit, and channel selection bits
    # We can send 3 bytes at once using spi.xfer2()
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # The ADC returns 10 bits of data, but the first 2 bits are meaningless. We can discard them by taking the last 8 bits.
    adc = ((r[1] & 3) << 8) + r[2]
    return adc

while True:
    value = read_adc(0)  # read from channel 0
    print("ADC value:", value)