import socket
import struct


HOST = "127.0.0.1"
PORT = 1234

SER_NIL = 0
SER_ERR = 1
SER_STR = 2
SER_INT = 3
SER_DBL = 4
SER_ARR = 5


def encode_request(*args):
    payload = struct.pack("<I", len(args))

    for arg in args:
        data = arg.encode("utf-8")
        payload += struct.pack("<I", len(data))
        payload += data

    return struct.pack("<I", len(payload)) + payload


def recv_exact(sock, size):
    data = b""

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            raise ConnectionError("server closed the connection")

        data += chunk

    return data


def decode_response(sock):
    header = recv_exact(sock, 4)
    size = struct.unpack("<I", header)[0]

    data = recv_exact(sock, size)

    if not data:
        return None

    response_type = data[0]
    payload = data[1:]

    if response_type == SER_NIL:
        return None

    if response_type == SER_STR:
        length = struct.unpack("<I", payload[:4])[0]
        return payload[4:4 + length].decode("utf-8")

    if response_type == SER_INT:
        return struct.unpack("<q", payload[:8])[0]

    if response_type == SER_ERR:
        code = struct.unpack("<i", payload[:4])[0]
        length = struct.unpack("<I", payload[4:8])[0]
        message = payload[8:8 + length].decode("utf-8")
        return f"ERROR {code}: {message}"

    return f"UNKNOWN RESPONSE TYPE: {response_type}"


def send_command(sock, *args):
    print(f"> {' '.join(args)}")

    sock.sendall(encode_request(*args))

    response = decode_response(sock)

    print(f"< {response}")

    return response


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        print(f"Connected to Redis server at {HOST}:{PORT}\n")

        assert send_command(sock, "set", "key", "hello") is None
        assert send_command(sock, "get", "key") == "hello"
        assert send_command(sock, "del", "key") == 1
        assert send_command(sock, "get", "key") is None

        print("\nAll tests passed.")


if __name__ == "__main__":
    main()  