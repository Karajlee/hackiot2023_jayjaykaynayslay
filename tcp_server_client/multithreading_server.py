# Reference: https://pymotw.com/3/socket/tcp.html
# socket_echo_server.py

import sys
import socket
import threading
import RPi.GPIO as GPIO
from enum import Enum
import time

# Button State Machine
class State(Enum):
    OFF = 1
    ON = 2
    SEND_MSG = 3

# ----------------------------- THREADS -----------------------------
def read_from_client(socket, address):
    ## Receive the data from client
    while True:
        data = socket.recv(16)
        print('received {!r}'.format(data))
        if not data:
            print('no data from', address)
            break
    
    state = State.OFF

def write_to_client(socket):
    ## Read in inputs from sensors
    while True:
        # BUTTON
        if GPIO.input(10) == GPIO.HIGH:
            print("Button was pushed!")

            # update state
            if state == State.OFF:
                state = State.ON
                GPIO.output(12, GPIO.HIGH)
            elif state == State.ON:
                state = State.SEND_MSG
            elif state == State.SEND_MSG:
                state = State.OFF
                GPIO.output(12, GPIO.LOW)
            
            # debouncing    
            while(GPIO.input(10)==GPIO.HIGH):
                time.sleep(15/1000)

        # RIBBON & PRESSURE- TBD
        if (state == State.SEND_MSG):
            msg = "Send a message (reading ribbon and pressure sensor data)"


# ----------------------------- MAIN -----------------------------
def main():
    # Set initial pins and state
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(12, GPIO.OUT)  # LED
    GPIO.output(12, GPIO.LOW) # OFF
    state = State.OFF

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('172.20.10.7', 12345)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Initiate threads
        read_thread = threading.Thread(target=read_from_client, args=(connection,client_address,))
        write_thread = threading.Thread(target=write_to_client, args=(connection,))

        # Join threads when done
        read_thread.join()
        write_thread.join()

    finally:
        # Clean up the connection
        connection.close()

    print("Server done!")

if __name__ == "__main__":
    main()
