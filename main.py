# Reference: https://pymotw.com/3/socket/tcp.html
# socket_echo_server.py

import sys
import socket
import threading
# import RPi.GPIO as GPIO
from enum import Enum
import time

# Button State Machine
class State(Enum):
    OFF = 1
    ON = 2
    SEND_MSG = 3
state = State.SEND_MSG

# ----------------------------- INITIALIZE -----------------------------
def init_rpi0():
    SERVER_PORT = 12340
    CLIENT_PORT = 12341

    ## Setup a TCP/IP server socket
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    # server_address = ('172.20.10.7', SERVER_PORT)
    server_address = ('localhost', SERVER_PORT)   # *FOR LOCAL TESTING*
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
        # server_address = ('172.20.10.7', CLIENT_PORT)
        server_address = ('localhost', CLIENT_PORT)   # *FOR LOCAL TESTING*
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
    # server_address = ('172.20.10.7', CLIENT_PORT)
    server_address = ('localhost', CLIENT_PORT)   # *FOR LOCAL TESTING*
    print('1\tconnecting to {} port {}'.format(*server_address))
    client_sock.connect(server_address)

    try:
        # Initiate read thread
        read_thread = threading.Thread(target=read_from_client, args=(client_sock,server_address))
        read_thread.start()

        ## Setup a TCP/IP server socket
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        # server_address = ('172.20.10.7', SERVER_PORT)
        server_address = ('localhost', SERVER_PORT)   # *FOR LOCAL TESTING*
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

    ## Receive the data from client
    while True:
        data = socket.recv(16)
        print('received {!r}'.format(data))
        if not data:
            print('no data from', address)
            break
    
    state = State.OFF

def write_to_client(socket):
    print("Preparing to write...")

    ## Read in inputs from sensors
    # while True:
        # BUTTON
        # if GPIO.input(10) == GPIO.HIGH:
            # print("Button was pushed!")

            # # update state
            # if state == State.OFF:
            #     state = State.ON
            #     GPIO.output(12, GPIO.HIGH)
            # elif state == State.ON:
            #     state = State.SEND_MSG
            # elif state == State.SEND_MSG:
            #     state = State.OFF
            #     GPIO.output(12, GPIO.LOW)
            
            # # debouncing    
            # while(GPIO.input(10)==GPIO.HIGH):
            #     time.sleep(15/1000)

        # RIBBON & PRESSURE- TBD
    if (state == State.SEND_MSG):
        msg = b'Send a message (reading ribbon and pressure sensor data)'
        socket.sendall(msg)

# ----------------------------- MAIN -----------------------------
def main():
    # # Set initial pins and state
    # GPIO.setwarnings(False) 
    # GPIO.setmode(GPIO.BOARD) 
    # GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # GPIO.setup(12, GPIO.OUT)  # LED
    # GPIO.output(12, GPIO.LOW) # OFF

    # Check for valid num of args
    if len(sys.argv) != 2:
        print('Invalid number of parameters.')
        print('python main.py [SERVER=0/CLIENT=1]')
        sys.exit()

    # Determine if rpi 0 or 1
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
