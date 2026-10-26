from socket import socket
from argparse import ArgumentParser

def main():
    """Connect to a TCP Server and display its response."""
    parser = ArgumentParser(description="Connect to a TCP Server, send a message and display the result.")

    # Add command line arguments
    parser.add_argument("ip_address")
    parser.add_argument("port", type=int)
    parser.add_argument("message")

    args = parser.parse_args()
    ip_address, port, message = args.ip_address, args.port, args.message

    # Establish a socket connection
    with socket() as client_socket:
        address = (ip_address, port)

        client_socket.connect(address)

        client_socket.sendall(message.encode())

        response = client_socket.recv(1024).decode()

        print(response)


if __name__ == "__main__":
    main()