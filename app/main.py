import socket  # noqa: F401


def create_api_version_response(correlation_id: int, status_code=None):
    correlation_id_bytes = correlation_id.to_bytes(4, byteorder="big")
    message = correlation_id_bytes
    if status_code:
        message += status_code.to_bytes(2, byteorder="big")
    message_length = len(message).to_bytes(4, byteorder="big")
    return message_length + message

def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        conn, addr = server.accept() # wait for client

        with conn:
            print(f"Connected from {addr}")
            data = conn.recv(1024)
            print(data, 'EOF')
            request_length = int.from_bytes(data[0:4], byteorder="big")
            data = data[4:]
            req_api_key_bytes = data[0:2]
            req_api_key = int.from_bytes(req_api_key_bytes, byteorder="big")
            req_api_version_bytes = data[2:4]
            req_api_version = int.from_bytes(req_api_version_bytes, byteorder="big")
            correlation_id_bytes = data[4:8]
            correlation_id = int.from_bytes(correlation_id_bytes, byteorder="big")
            if req_api_version > 4 or req_api_version < 0:
                conn.sendall(create_api_version_response(correlation_id, 35))
            else:
                conn.sendall(create_api_version_response(correlation_id))

if __name__ == "__main__":
    main()
