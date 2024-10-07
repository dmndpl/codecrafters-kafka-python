import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging,
    # they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    conn, addr = server.accept() # wait for client

    with conn:
        print(f"Connected from {addr}")
        while True:
            data = sock.recv(4)
            print(data, 'EOF')
        

        hardcoded_message_id = byte_var = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x07])
        conn.send(hardcoded_message_id)

if __name__ == "__main__":
    main()
