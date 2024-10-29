import socket
from web3 import Web3
from eth_account.messages import encode_defunct
import argparse
import sys

PRIVATE_KEY = "0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


class VsockListener:
    """Server"""

    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog
        self.web3 = Web3()

    def bind(self, port):
        """Bind and listen for connections on the specified port"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    # def bind(self, port): # local
    #     """Bind and listen for TCP connections on localhost"""
    #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     self.sock.bind(('0.0.0.0', port))
    #     self.sock.listen(self.conn_backlog)

    def recv_data(self):
        """Receive data from a remote endpoint and process it (sign or verify)"""
        while True:
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            data = from_client.recv(1024).decode()

            if data:
                # Split the request data (format: "<operation>:<message>:<signature>")
                request = data.split(":")
                operation = request[0]
                message = request[1]

                if operation == "sign":
                    # Sign the message
                    signed_message = self.sign_message(message)
                    print(f"Signed message: {signed_message}")
                    from_client.sendall(signed_message.encode("utf-8"))

                elif operation == "verify" and len(request) > 2:
                    signature = request[2]
                    verification_result = self.verify_message(message, signature)
                    result_msg = f"Signature valid: {verification_result}"
                    print(result_msg)
                    from_client.sendall(result_msg.encode("utf-8"))

            from_client.close()

    def sign_message(self, message):
        """Sign the message using the Ethereum private key with web3.py"""
        encoded_msg = encode_defunct(text=message)
        signed_message = self.web3.eth.account.sign_message(
            encoded_msg, private_key=PRIVATE_KEY
        )
        return signed_message.signature.hex()

    def verify_message(self, message, signature):
        """Verify the message's signature"""
        print("signature:", signature)
        encoded_msg = encode_defunct(text=message)
        recovered_address = self.web3.eth.account.recover_message(
            encoded_msg, signature=signature
        )
        print("recovered_address:", recovered_address)
        account = self.web3.eth.account.from_key(PRIVATE_KEY)
        print("signer_address:", account.address)
        is_valid = recovered_address == account.address
        print("Signature valid:", is_valid)
        return is_valid


def server_handler(args):
    server = VsockListener()
    server.bind(args.port)
    server.recv_data()


def main():
    parser = argparse.ArgumentParser(prog="vsock-server")
    parser.add_argument(
        "--version",
        action="version",
        help="Prints version information.",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(
        title="options", description="Available subcommands"
    )

    server_parser = subparsers.add_parser(
        "server", description="Server", help="Listen on a given port."
    )
    server_parser.add_argument("port", type=int, help="The local port to listen on.")
    server_parser.set_defaults(func=server_handler)

    if len(sys.argv) < 2:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    print("Starting server...")
    main()
