import socket  # noqa: F401


def create_api_version_response(correlation_id: int):
    correlation_id_bytes = correlation_id.to_bytes(4, byteorder="big")
    message_length = len(correlation_id_bytes).to_bytes(4, byteorder="big")
    return message_length + correlation_id_bytes

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
            
            conn.sendall(create_api_version_response(7))

if __name__ == "__main__":
    main()
