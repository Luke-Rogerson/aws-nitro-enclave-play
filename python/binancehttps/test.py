import socket
import json

ENCLAVE_CID = 26
ENCLAVE_PORT = 5000


def send_request_to_enclave():
    with socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM) as sock:
        sock.connect((ENCLAVE_CID, ENCLAVE_PORT))

        sock.sendall(b"price")

        response = sock.recv(4096).decode("utf-8")
        price_data = json.loads(response)
        print("BTC/USDT Price:", price_data)


if __name__ == "__main__":
    send_request_to_enclave()
