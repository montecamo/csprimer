import socket
import sys
import signal


upstream_port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


s.bind(("127.0.0.1", 9999))

s.listen()


def handler(_, __):
    print("close")
    s.close()
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


while True:
    conn, addr = s.accept()

    print(f"New connection from {addr}")
    a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    a.connect(("127.0.0.1", upstream_port))

    data = conn.recv(4096)

    if not data:
        break

    print(f"-> *    {len(data)}B")
    print(f"   * -> {len(data)}B")

    a.send(data)

    while True:
        data = a.recv(4096)
        print(f"   * <- {len(data)}B")

        if not data:
            break

        print(f"<- *    {len(data)}B")
        conn.send(data)

    conn.close()
    a.close()
