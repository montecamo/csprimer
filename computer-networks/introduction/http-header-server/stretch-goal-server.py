import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 8888))
s.listen(1)


def parse_headers(connection):
    state = "PARSE_NEWLINE"
    headers = {}
    key = b""
    value = b""

    while True:
        byte = connection.recv(1)

        match state:
            case "PARSE_NEWLINE":
                if byte == b"\n":
                    state = "PARSE_HEADER_KEY"

            case "PARSE_HEADER_KEY":
                if byte == b"\r":
                    break
                if byte == b":":
                    connection.recv(1)
                    state = "PARSE_HEADER_VALUE"
                    continue

                key += byte

            case "PARSE_HEADER_VALUE":
                if byte == b"\r":
                    headers[key.decode("utf-8")] = value.decode("utf-8")
                    key = b""
                    value = b""

                    state = "PARSE_NEWLINE"
                    continue

                value += byte

    return headers


def json_response(jsn):
    return "\r\n".join(
        [
            "HTTP/1.1 200 OK",
            "Content-Type: application/json",
            f"Content-Length: {len(jsn)}\r\n",
            jsn,
        ]
    )


while True:
    connection, _ = s.accept()

    headers = parse_headers(connection)
    response = json_response(json.dumps(headers, indent=2))

    connection.send(bytes(response, "utf-8"))
    connection.close()
