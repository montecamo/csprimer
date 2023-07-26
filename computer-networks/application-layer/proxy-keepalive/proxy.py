import socket
import signal
import sys


OWN_ADDR = ("0.0.0.0", 8000)
UPSTREAM_ADDR = ("127.0.0.1", 9000)


def log(s):
    print(s, file=sys.stderr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(OWN_ADDR)
s.listen(10)
log(f"Accepting new connections on {OWN_ADDR}")


def handler(_, __):
    print("close")
    s.close()
    sys.exit(0)


signal.signal(signal.SIGINT, handler)


def make_http_parser():
    state = "PARSE_METHOD"
    data = {}
    data["headers"] = {}
    data["content"] = b""

    body_separator_length = 0

    content_length = 0

    key = b""
    value = b""

    def clock(byte):
        nonlocal state
        nonlocal value
        nonlocal key
        nonlocal content_length
        nonlocal body_separator_length

        match state:
            case "PARSE_METHOD":
                if byte == b" ":
                    data["method"] = value.decode("utf-8")
                    state = "PARSE_URL"
                    value = b""
                    return

                value += byte

            case "PARSE_URL":
                if byte == b" ":
                    data["url"] = value.decode("utf-8")
                    state = "PARSE_HTTP_VERSION"
                    value = b""
                    return

                value += byte

            case "PARSE_HTTP_VERSION":
                if byte == b"\r":
                    state = "PARSE_NEWLINE"
                    data["version"] = value.decode("utf-8")

                    value = b""
                    return

                value += byte

            case "PARSE_NEWLINE":
                if byte == b"\n":
                    state = "PARSE_HEADER_KEY"

            case "PARSE_HEADER_SPACE":
                state = "PARSE_HEADER_VALUE"

            case "PARSE_BODY_SEPARATOR":
                if body_separator_length == 1:
                    state = "PARSE_BODY"

                body_separator_length -= 1

            case "PARSE_BODY":
                if content_length == 1:
                    data["content"] += byte
                    return data

                data["content"] += byte
                content_length -= 1

            case "PARSE_HEADER_KEY":
                if byte == b"\r":
                    if (
                        data["method"] == "GET"
                        or not "content-length" in data["headers"]
                    ):
                        state = "FINISH"
                        return data

                    content_length = int(data["headers"]["content-length"])
                    body_separator_length = 1

                    state = "PARSE_BODY_SEPARATOR"

                if byte == b":":
                    state = "PARSE_HEADER_SPACE"
                    return

                key += byte

            case "PARSE_HEADER_VALUE":
                if byte == b"\r":
                    data["headers"][key.decode("utf-8").lower()] = value.decode("utf-8")
                    key = b""
                    value = b""

                    state = "PARSE_NEWLINE"
                    return

                value += byte

    return clock


def parse_request(connection):
    parser = make_http_parser()

    while True:
        bytes = connection.recv(4096)

        if not bytes:
            print("Connection closed")
            break

        yield ("BYTES", bytes)

        for byte in bytes:
            state = parser(byte.to_bytes(1, byteorder="big"))

            if state != None:
                parser = make_http_parser()
                yield ("DATA", state)
                break


while True:
    try:
        client_sock, client_addr = s.accept()
        log(f"New connection from {client_addr}")
        request_data = None
        upstream_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        upstream_sock.connect(UPSTREAM_ADDR)
        log(f"Connected to {UPSTREAM_ADDR}")

        for data in parse_request(client_sock):
            match data:
                case ("BYTES", bytes):
                    log(f"-> *    {len(bytes)}B")
                    upstream_sock.send(bytes)
                    log(f"   * -> {len(bytes)}B")

                case ("DATA", request):
                    print("req", request)

                    for data in parse_request(upstream_sock):
                        match data:
                            case ("BYTES", bytes):
                                log(f"   * <- {len(bytes)}B")
                                client_sock.send(bytes)
                                log(f"<- *    {len(bytes)}B")

                            case ("DATA", request):
                                break

                    if (
                        request["method"] == "HTTP/1.0"
                        and not "connection" in request["headers"]
                    ) or (request["headers"]["connection"] == "close"):
                        client_sock.close()
                        upstream_sock.close()

    except ConnectionRefusedError:
        client_sock.send(b"HTTP/1.1 502 Bad Gateway\r\n\r\n")
        log("<- *    BAD GATEWAY")
    except OSError as msg:
        log(msg)
    finally:
        upstream_sock.close()
        client_sock.close()

s.close()
