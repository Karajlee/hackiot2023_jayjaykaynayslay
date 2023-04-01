import sys
import socket

# ----------------------------- SERVER -----------------------------
def init_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('172.20.10.7', 12345)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection')
        connection, client_address = sock.accept()
        try:
            print('connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print('received {!r}'.format(data))
                if data:
                    print('sending data back to the client')
                    connection.sendall(data)
                else:
                    print('no data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()

# ----------------------------- CLIENT -----------------------------
def init_client():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('172.20.10.7', 12345)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)

    try:

        # Send data
        message = b'This is the message.  It will be repeated.'
        print('sending {!r}'.format(message))
        sock.sendall(message)

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

# ----------------------------- MAIN -----------------------------
def main():
    # Check for valid num of args
    if len(sys.argv) != 2:
        print('Invalid number of parameters.')
        print('python main.py [SERVER=0/CLIENT=1]')
        sys.exit()

    # Determine if server or client
    server_client = int(sys.argv[1])
    if server_client == 0:
        # Server
        init_server()
    elif server_client == 1:
        # Client
        init_client()

if __name__ == '__main__':
    main()