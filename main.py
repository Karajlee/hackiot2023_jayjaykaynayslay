# Reference: https://pymotw.com/3/socket/tcp.html
# socket_echo_server.py

import spidev
import sys
import socket
import threading
import RPi.GPIO as GPIO
from enum import Enum
import time

# ----------------------------- ADC -----------------------------
spi = spidev.SpiDev()
spi.open(0, 0)  # open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # set SPI clock speed

channel = 0

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
def read_from_client(socket, address):
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

        if(sensor_data[0]=="P"):
            pwm.ChangeDutyCycle(int(sensor_data[1])/2)

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

        value_str = str(value)
        while(len(value_str)<3):
            value_str = "0"+value_str

        if state == State.SEND_MSG:
            msg = b'R 001'
            socket.sendall(msg)
            # state = State.SEND_PRESSURE
        elif state == State.SEND_PRESSURE:
            # msg = b'P 001'
            msg_str = "P "+value_str
            print(msg_str)

            socket.sendall(msg_str.encode())
            # state = State.OFF

# ----------------------------- MAIN -----------------------------
def main():
    # # Set initial pins and state
    # GPIO.setwarnings(False) 
    # GPIO.setmode(GPIO.BOARD) 
    # GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(12, GPIO.OUT)  # LED
    # GPIO.output(12, GPIO.LOW) # OFF
    button_pin = 26
    led_pin = 13
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(led_pin, GPIO.OUT)

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