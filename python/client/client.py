import socket
import argparse
import sys
import time


class VsockStream:
    """Client"""

    def __init__(self, conn_tmo=5):
        self.conn_tmo = conn_tmo

    # def connect(self, address): # local
    #     """Connect to the server using TCP"""
    #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.sock.settimeout(self.conn_tmo)
    #     self.sock.connect(address)
    #     print("CONNECTED LOCALLY")

    def connect(self, endpoint):
        """Connect to the remote endpoint"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.settimeout(self.conn_tmo)
        self.sock.connect(endpoint)

    def send_data(self, data):
        """Send data to the TCP server"""
        self.sock.sendall(data.encode())

    def recv_data(self):
        """Receive signed data from the server"""
        response = self.sock.recv(1024).decode()
        return response

    def disconnect(self):
        """Close the client socket"""
        self.sock.close()


def client_handler(args):
    client = VsockStream()
    endpoint = (args.cid, args.port)

    total_start = time.time()
    connect_start = time.time()
    client.connect(endpoint)
    connect_end = time.time()
    print(f"🕒 Connection time: {connect_end - connect_start:.6f} seconds")

    operation = args.operation  # either 'sign' or 'verify'
    msg = args.message
    signature = args.signature  # Only used in 'verify' operation

    if operation == "sign":
        request_data = f"sign:{msg}"
    elif operation == "verify":
        request_data = f"verify:{msg}:{signature}"

    # Send the request (sign or verify)
    send_start = time.time()
    client.send_data(request_data)
    send_end = time.time()
    print(f"🕒 Send message time: {send_end - send_start:.6f} seconds")

    recv_start = time.time()
    response = client.recv_data()
    recv_end = time.time()
    print(f"🕒 Receive response time: {recv_end - recv_start:.6f} seconds")

    print(f"Response: {response}")

    client.disconnect()

    total_end = time.time()
    print(f"🕒 Total process time: {total_end - total_start:.6f} seconds")


def main():
    parser = argparse.ArgumentParser(prog="vsock-client")
    parser.add_argument(
        "--version",
        action="version",
        help="Prints version information.",
        version="%(prog)s 0.1.0",
    )
    subparsers = parser.add_subparsers(title="options")

    client_parser = subparsers.add_parser(
        "client", description="Client", help="Connect to a given cid and port."
    )
    client_parser.add_argument("cid", type=int, help="The remote endpoint CID.")
    client_parser.add_argument("port", type=int, help="The remote endpoint port.")
    client_parser.add_argument(
        "--message", type=str, help="The message to be signed/verified."
    )
    client_parser.add_argument(
        "--operation",
        type=str,
        choices=["sign", "verify"],
        help="Choose to sign or verify.",
    )
    client_parser.add_argument(
        "--signature", type=str, help="Signature for verification."
    )
    client_parser.set_defaults(func=client_handler)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
