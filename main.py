# Reference: https://pymotw.com/3/socket/tcp.html
# socket_echo_server.py

import spidev
import sys
import socket
import threading
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from enum import Enum
import time

# ----------------------------- ADC -----------------------------
spi = spidev.SpiDev()
spi.open(0, 0)  # open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # set SPI clock speed

channel = 0

GPIO.setup(13, GPIO.OUT)
pwm = GPIO.PWM(13, 100)
pwm.start(0)

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
pwm_backlight = GPIO.PWM(lcd_backlight, 100)

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Button State Machine
class State(Enum):
    OFF = 1
    ON = 2
    SEND_MSG = 3
    SEND_PRESSURE = 4

state = State.SEND_MSG
rpi_num = 0



def read_adc(channel):
    # MCP3008 expects 3 bytes: start bit, single-ended/differential bit, and channel selection bits
    # We can send 3 bytes at once using spi.xfer2()
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    # The ADC returns 10 bits of data, but the first 2 bits are meaningless. We can discard them by taking the last 8 bits.
    adc = ((r[1] & 3) << 8) + r[2]
    return adc


# ----------------------------- INITIALIZE -----------------------------
def init_rpi0():
    SERVER_PORT = 12340
    CLIENT_PORT = 12341

    ## Setup a TCP/IP server socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('172.20.10.7', SERVER_PORT)
    # server_address = ('localhost', SERVER_PORT)   # *FOR LOCAL TESTING*
    print('0\tstarting up on {} port {}'.format(*server_address))
    server_sock.bind(server_address)

    # Listen for incoming connections
    server_sock.listen(1)

    # Wait for a connection
    print('0\twaiting for a connection')
    connection, client_address = server_sock.accept()
    try:
        print('0\tconnection from', client_address)

        # Initiate and start server writing thread
        write_thread = threading.Thread(target=write_to_client, args=(connection,))
        write_thread.start()

        ## Setup a TCP/IP client socket
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('172.20.10.5', CLIENT_PORT)
        # server_address = ('localhost', CLIENT_PORT)   # *FOR LOCAL TESTING*
        print('0\tconnecting to {} port {}'.format(*server_address))
        client_sock.connect(server_address)

        try:
            # Initiate read thread
            read_thread = threading.Thread(target=read_from_client, args=(client_sock,server_address))
            read_thread.start()
            read_thread.join()
            
        finally:
            print('0\tclosing socket')
            client_sock.close()

        write_thread.join()

    finally:
        print('0\tclosing connection')
        connection.close()


def init_rpi1():
    SERVER_PORT = 12341
    CLIENT_PORT = 12340

    ## Setup a TCP/IP client socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.20.10.7', CLIENT_PORT)
    # server_address = ('localhost', CLIENT_PORT)   # *FOR LOCAL TESTING*
    print('1\tconnecting to {} port {}'.format(*server_address))
    client_sock.connect(server_address)

    try:
        # Initiate read thread
        read_thread = threading.Thread(target=read_from_client, args=(client_sock,server_address))
        read_thread.start()

        ## Setup a TCP/IP server socket
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('172.20.10.5', SERVER_PORT)
        # server_address = ('localhost', SERVER_PORT)   # *FOR LOCAL TESTING*
        print('1\tstarting up on {} port {}'.format(*server_address))
        server_sock.bind(server_address)

        # Listen for incoming connections
        server_sock.listen(1)

        # Wait for a connection
        print('1\twaiting for a connection')
        connection, client_address = server_sock.accept()
        try:
            print('1\tconnection from', client_address)

            # Initiate and start server writing thread
            write_thread = threading.Thread(target=write_to_client, args=(connection,))
            write_thread.start()
            write_thread.join()
        finally:
            print('1\tclosing socket')
            client_sock.close()

        read_thread.join()
            
    finally:
        print('1\tclosing socket')
        client_sock.close()

# ----------------------------- THREADS -----------------------------
# m = threading.Lock()
def read_from_client(socket, address):
    global pwm
    global lcd
    # global m

    print("Preparing to read...")

    # state = 0 #Reading whether to process ribbon or pressure

    ## Receive the data from client
    while True:
        data = socket.recv(5)
        print('received {!r}'.format(data))

        if not data:
            print('no data from', address)
            break
        
        # Process data
        sensor_data = data.decode('ascii').split(" ")
        if (len(sensor_data) != 2 or sensor_data[1] == ''):
            continue

        if(sensor_data[0]=="P"):
            pwm.ChangeDutyCycle(int(sensor_data[1])/2)
        if(sensor_data[0]=="R"):
            total_cols = int(sensor_data[1])
            print(total_cols)
            # m.acquire()
            if total_cols != 96:
                blocks_filled = total_cols * 2 / 96 * 7
                blocks_empty = 16 - int(blocks_filled)

                # block_line=""
                # for i in range(int(blocks_filled)):
                #     block_line += 'X'
                
                # for i in range(blocks_empty):
                #     block_line +=' '

                # block_line = ('X' * blocks_filled) + (' ' * blocks_empty)
                print(block_line)
                # lcd.set_cursor(0, 0)
                # lcd.message(block_line)
                # lcd.set_cursor(0, 1)
                # lcd.message(block_line)

                # # Filled square
                # fill = [
                #     0b11111,
                #     0b11111,
                #     0b11111,
                #     0b11111,
                #     0b11111,
                #     0b11111,
                #     0b11111,
                #     0b11111,
                # ]
                # # Empty square
                # empty = [
                #     0b00000,
                #     0b00000,
                #     0b00000,
                #     0b00000,
                #     0b00000,
                #     0b00000,
                #     0b00000,
                #     0b00000,
                # ]
                # lcd.create_char(0, fill)
                # lcd.create_char(7, empty)


                # max_col = 2 * total_cols
                # col = 0
                # while (col < max_col):
                #     # Load custom characters into LCD memory
                #     # Display custom characters using message()
                #     lcd.message('\n')
                #     lcd.set_cursor(col, 0)
                #     lcd.message('\x00')
                #     lcd.set_cursor(col+1, 0)
                #     lcd.message('\x00')
                #     lcd.set_cursor(col, 1)
                #     lcd.message('\x00')
                #     lcd.set_cursor(col+1, 1)
                #     lcd.message('\x00')

                #     col += 2
                #     # time.sleep(0.3)

                # col = max_col
                # while (col < 16):
                #     # Load custom characters into LCD memory
                #     # Display custom characters using message()
                #     lcd.message('\n')
                #     lcd.set_cursor(col, 0)
                #     lcd.message('\x07')
                #     lcd.set_cursor(col, 1)
                #     lcd.message('\x07')

                #     col += 1
                #     # time.sleep(0.15)

            else:
                lcd.clear()
                print("Total cols = 7")
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
                print("lcd done print")
            # m.release()
            time.sleep(0.5)

    # global state
    # state = State.OFF

def write_to_client(socket):
    print("Preparing to write...")
    global state
    global channel

    ## Read in inputs from sensors
    while True:
        # BUTTON
        # if GPIO.input(26) == GPIO.HIGH:
            # print("Button was pushed!")

            # # update state
            # if state == State.OFF:
            #     state = State.ON
            #     GPIO.output(12, GPIO.HIGH)
            # elif state == State.ON:
            #     state = State.SEND_MSG
            # elif state == State.SEND_MSG:
            #     state = State.SEND_PRESSURE
            # elif state == State.SEND_PRESSURE:
            #     state = State.OFF
            #     GPIO.output(12, GPIO.LOW)
            
            # # debouncing    
            # while(GPIO.input(10)==GPIO.HIGH):
            #     time.sleep(15/1000)

        # RIBBON - TBD
        if GPIO.input(26) == GPIO.HIGH:
            print("Button was pushed!")

            # update state
            if channel == 0:
                channel = 1
                state = State.SEND_PRESSURE
            else:
                channel = 0
                state = State.SEND_MSG
            
            print("Channel:", channel)

            while(GPIO.input(26)==GPIO.HIGH):
                time.sleep(15/1000)
    
        value = int(read_adc(channel))  # read from channel 0
        # print("ADC value:", value)
        # time.sleep(.5)
        if(value>200 and channel==1):
            value=200

        if(value>96 and channel==0):
            value=96

        # if (channel == 0):
        #     value=int(value * 7 / 96)

        # if (channel == 1):
        #     value/=2

        value_str = str(value)
        while(len(value_str)<3):
            value_str = "0"+value_str

        if state == State.SEND_MSG:
            msg_str = "R "+value_str
            socket.sendall(msg_str.encode())
            # state = State.SEND_PRESSURE
        elif state == State.SEND_PRESSURE:
            # msg = b'P 001'
            msg_str = "P "+value_str

            socket.sendall(msg_str.encode())
            # state = State.OFF

# ----------------------------- MAIN -----------------------------
def main():
    # # Set initial pins and state
    # GPIO.setwarnings(False) 
    # GPIO.setmode(GPIO.BOARD) 
    # GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    button_pin = 26
    led_pin = 13
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.OUT)  # LED
    GPIO.output(12, GPIO.LOW) # OFF

    # Check for valid num of args
    if len(sys.argv) != 2:
        print('Invalid number of parameters.')
        print('python main.py [SERVER=0/CLIENT=1]')
        sys.exit()

    # Determine if rpi 0 or 1
    global rpi_num
    rpi_num = int(sys.argv[1])
    if rpi_num == 0:
        init_rpi0()
    if rpi_num == 1:
        init_rpi1()
    else:
        print('Invalid parameter passed.')
        print('python main.py [0 or 1]')
        sys.exit()

if __name__ == "__main__":
    main()