import hashlib
import socket
import ssl
import json
import argparse
import sys


BINANCE_API_PATH = "/api/v3/ticker/price?symbol=BTCUSDT"
PROXY_VSOCK_CID = 3  # CID 3 is reserved for the host in AWS Nitro Enclaves
PROXY_VSOCK_PORT = 8000  # Port the vsock proxy is listening on
BINANCE_SSL_CERT_PUBLIC_KEY = "a26834e9071cbf6a00fc6936c9955f4fe345fc83c03960cc289e3642041ce512"  # Expires Monday 10 February 2025 at 23:59:59


class VsockListener:
    """
    Server for receiving requests and responding with Binance API data over vsock
    Enforces SSL certificate public key pinning
    Requires the vsock proxy to be running on the host - https://github.com/aws/aws-nitro-enclaves-cli/tree/main/vsock_proxy
    """

    def __init__(self, conn_backlog=128):
        self.conn_backlog = conn_backlog

    def bind(self, port):
        """Bind and listen for connections on the specified port"""
        self.sock = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        self.sock.bind((socket.VMADDR_CID_ANY, port))
        self.sock.listen(self.conn_backlog)

    def recv_data(self):
        """Receive data from a client, make a request to Binance, and send back the response"""
        while True:
            (from_client, (remote_cid, remote_port)) = self.sock.accept()
            data = from_client.recv(1024).decode()

            if data:
                request = data.strip().lower()
                if request == "price":
                    # Fetch BTCUSDT price from Binance via the vsock proxy
                    price_data = self.get_binance_price()
                    from_client.sendall(price_data.encode("utf-8"))

            from_client.close()

    def get_binance_price(self):
        """
        Fetch the BTC/USDT price from Binance through the vsock proxy with TLS
        Error out if the SSL certificate public key does not match the expected value
        """
        vsock_conn = socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM)
        vsock_conn.connect((PROXY_VSOCK_CID, PROXY_VSOCK_PORT))

        context = ssl.create_default_context()
        with context.wrap_socket(
            vsock_conn, server_hostname="api.binance.com"
        ) as tls_conn:
            # Check the certificate pin
            der_cert = tls_conn.getpeercert(binary_form=True)
            cert_sha256 = hashlib.sha256(der_cert).hexdigest()
            if cert_sha256 != BINANCE_SSL_CERT_PUBLIC_KEY:
                raise ssl.SSLError(
                    f"Binance SSL public key mismatch: {cert_sha256} != {BINANCE_SSL_CERT_PUBLIC_KEY}"
                )

            request = f"GET {BINANCE_API_PATH} HTTP/1.1\r\nHost: api.binance.com\r\nConnection: close\r\n\r\n"
            tls_conn.sendall(request.encode("utf-8"))
            response = tls_conn.recv(4096).decode("utf-8")
            json_data = response.split("\r\n\r\n", 1)[1]
            print(f"Response: {json_data}")
            price_json = json.loads(json_data)
            return json.dumps(price_json)


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
