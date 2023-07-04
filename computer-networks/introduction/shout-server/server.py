import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(("127.0.0.1", 8888))

while True:
    data, address = s.recvfrom(1024)

    s.sendto(bytes([x & ~0x20 for x in data[:-1]]) + b"\n", address)
