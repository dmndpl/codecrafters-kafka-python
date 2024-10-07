import socket  # noqa: F401
from typing import List

class ApiVersionRequestV4():

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

class ApiKey():

    def __init__(self, api_key, min_version=0, max_version=4):
        self.api_key = api_key
        self.min_version = 0 
        self.max_version = 4

    def to_bytes(self):
        return self.api_key.to_bytes(2, byteorder="big") + self.min_version.to_bytes(2, byteorder="big") + self.max_version.to_bytes(2, byteorder="big")


class ApiVersionsResponseV4():
    
    TAG_BUFFER = int(0).to_bytes(1, byteorder="big")
    MIN_VERSION = 0
    MAX_VERSION = 4

    def __init__(self, correlation_id=int, error_code=0, api_keys:List[ApiKey] = [], throttle_time_ms=0):
        self.correlation_id = correlation_id
        self.error_code = error_code
        self.api_keys = api_keys
        self.throttle_time_ms = throttle_time_ms

    @classmethod
    def from_requestV4(cls, req: ApiVersionRequestV4):
        error_code = 0 if cls.MIN_VERSION <= req.api_version <= cls.MAX_VERSION else 35
        api_keys = [ApiKey(req.api_key, cls.MIN_VERSION, cls.MAX_VERSION)]
        correlation_id = req.correlation_id
        return cls(correlation_id, error_code, api_keys)

    def to_bytes(self):
        header = self.correlation_id.to_bytes(4, byteorder="big")

        body = (
            self.error_code.to_bytes(2, byteorder="big")
            + int(len(self.api_keys) + 1).to_bytes(1, byteorder="big")
            + b"".join([api_key.to_bytes() for api_key in self.api_keys])
            + self.TAG_BUFFER
            + self.throttle_time_ms.to_bytes(4, byteorder="big")
            + self.TAG_BUFFER
        )

        return (len(header) + len(body)).to_bytes(4, byteorder="big") + header + body

    def __str__(self):
       return str(self.to_bytes())

def create_api_version_response(request: ApiVersionRequestV4):
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
            req = ApiVersionRequestV4(data)
            print(req)
            response = ApiVersionsResponseV4.from_requestV4(req)
            conn.sendall(response.to_bytes())

def test_main():
    input = b'\x00\x00\x00#\x00\x12\x00\x04p\xdf\x9f\xbc\x00\tkafka-cli\x00\nkafka-cli\x040.1\x00'
    req = ApiVersionRequestV4(input)
    print(req)
    print(ApiVersionsResponseV4.from_requestV4(req))

if __name__ == "__main__":
    main()
