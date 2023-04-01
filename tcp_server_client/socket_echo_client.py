# Reference: https://pymotw.com/3/socket/tcp.html
# socket_echo_client.py
import RPi.GPIO as GPIO
from enum import Enum
import socket
import sys

#Will change this
def readMessage(message, sock):
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received ')

def main():# Create a TCP/IP socket
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    # initialize state
    class State(Enum):
        OFF = 1
        ON = 2
        STATE_1 = 3
        STATE_2 = 4
    state = State.OFF

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.20.10.7', 12345)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # # Send data
        # message = b'This is the message.  It will be repeated.'
        # print('sending {!r}'.format(message))
        # sock.sendall(message)

        while True: 
            if GPIO.input(10) == GPIO.HIGH:
                # print("Button was pushed!")
                message = b'Button was pushed!'
                sock.sendall(message)

                # update state
                if state == State.OFF:
                    state = State.ON
                elif state == State.ON:
                    state = State.STATE_1
                elif state == State.STATE_1:
                    state = State.STATE_2
                elif state == State.STATE_2:
                    state = State.OFF
                
                # temp = 'State:'+ str(state.value)
                # message = bytes(temp, "utf-8")
                sock.sendall(b'State: ')
                sock.sendall(state.value)

                while(GPIO.input(10)==GPIO.HIGH):
                    time.sleep(15/1000)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(16)
                    amount_received += len(data)
                    print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()

if __name__=="__main__":
    main()
