import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("127.0.0.1", 8888))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(1)


def parse_headers(data):
    headers = data.decode("utf-8").split("\r\n")[1:-2]
    headers = [x.split(" ") for x in headers]
    headers = {header[0][:-1]: header[1] for header in headers}

    return json.dumps(headers, indent=2)


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
    data = b""

    while True:
        next = connection.recv(10)
        print(next)
        if not next:
            break

        data += next

    headers = parse_headers(data)

    connection.send(bytes(json_response(headers), "utf-8"))
    connection.close()
