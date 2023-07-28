import socket
from log import log
from parser import Parser
from serializer import serialize

UPSTREAM_ADDR = ("127.0.0.1", 9000)


class Proxy:
    def __init__(self, client):
        upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream.connect(UPSTREAM_ADDR)

        log(f"Connected to {UPSTREAM_ADDR}")

        self.state = "OPEN"
        self.client = client
        self.upstream = upstream
        self.parser = Parser("REQ")

    def reset_parser(self):
        self.parser = Parser("REQ")

    def handle_upstream(self):
        parser = Parser("RES")

        while True:
            data = self.upstream.recv(4096)

            if not data:
                break

            log(f"   * <- {len(data)}B")

            for byte in data:
                parser.parse(byte.to_bytes(1, byteorder="big"))

            if parser.state == "FINISH":
                parser.data["headers"][b"Foo"] = b"bar"
                serialized = serialize("RES", parser.data)

                self.client.send(serialized)

                log(f"<- *    {len(serialized)}B")

                break

    def close(self):
        self.upstream.close()
        self.client.close()

        self.state = "CLOSE"

    def handle(self):
        data = self.client.recv(4096)

        if not data:
            self.close()
            return

        log(f"-> *    {len(data)}B")

        self.upstream.send(data)

        log(f"   * -> {len(data)}B")

        for byte in data:
            self.parser.parse(byte.to_bytes(1, byteorder="big"))

        if self.parser.state == "FINISH":
            self.handle_upstream()
            self.reset_parser()
