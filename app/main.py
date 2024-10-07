import socket  # noqa: F401

class ApiVersionRequest():

    def __init__(self, byte_stream):
        self.message_length = int.from_bytes(byte_stream[0:4], byteorder="big")
        self.api_key = int.from_bytes(byte_stream[4:6], byteorder="big")
        self.api_version = int.from_bytes(byte_stream[6:8], byteorder="big")
        self.correlation_id = int.from_bytes(byte_stream[8:12], byteorder="big")

    def __str__(self):
        return f'''
            Message Length: {self.message_length}
            API Key: {self.api_key}
            API Version: {self.api_version}
            Correlation ID: {self.correlation_id}
            '''

def create_api_version_response(request: ApiVersionRequest):
    header = request.correlation_id.to_bytes(4)

    min_version, max_version = 0, 4

    status_code = 0 if min_version <= request.api_version <= max_version else 35

    THROTTLE_TIME_MS = 0
    NUM_API_KEYS = 2
    TAG_BUFFER = int(0).to_bytes(1, byteorder="big")

    body = status_code.to_bytes(2) + NUM_API_KEYS.to_bytes(1) + request.api_key.to_bytes(2) + min_version.to_bytes(2) + max_version.to_bytes(2) + TAG_BUFFER + THROTTLE_TIME_MS.to_bytes(4) + TAG_BUFFER

    message_length = (len(header) + len(body)).to_bytes(4)
    return message_length + header + body

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        conn, addr = server.accept()

        with conn:
            print(f"Connected from {addr}")
            data = conn.recv(2048)
            print(data, 'EOF')
            req = ApiVersionRequest(data)
            print(req)
            conn.sendall(create_api_version_response(req))

def test_main():
    input = b'\x00\x00\x00#\x00\x12\x00\x04p\xdf\x9f\xbc\x00\tkafka-cli\x00\nkafka-cli\x040.1\x00'
    req = ApiVersionRequest(input)
    print(req)

if __name__ == "__main__":
    main()
