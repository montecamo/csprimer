def serialize(type, req):
    match type:
        case "RES":
            return b"\r\n".join(
                [
                    b" ".join([req["version"], req["url"], req["http_text"]]),
                    *[
                        b": ".join([key, value])
                        for key, value in req["headers"].items()
                    ],
                    b"\r\n" + req["content"],
                ]
            )

        case "REQ":
            return b"\r\n".join(
                [
                    b" ".join([req["method"], req["url"], req["version"]]),
                    *[
                        b": ".join([key, value])
                        for key, value in req["headers"].items()
                    ],
                    b"\r\n" + req["content"],
                ]
            )

    return b""
