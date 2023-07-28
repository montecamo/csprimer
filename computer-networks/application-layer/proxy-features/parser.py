class Parser:
    def __init__(self, type):
        self.type = type

        self.state = "PARSE_METHOD" if type == "REQ" else "PARSE_HTTP_VERSION"
        self.headers = {}
        self.data = {"headers": {}, "content": b"", "method": b"", "version": b""}

        self.body_separator_length = 0

        self.content_length = 0

        self.key = b""
        self.value = b""

    def parse(self, byte):
        match self.state:
            case "PARSE_METHOD":
                if byte == b" ":
                    self.data["method"] = self.value
                    self.state = "PARSE_URL"
                    self.value = b""
                    return

                self.value += byte

            case "PARSE_HTTP_TEXT":
                if byte == b"\r":
                    self.state = "PARSE_NEWLINE"
                    self.data["http_text"] = self.value
                    self.value = b""

                    return

                self.value += byte

            case "PARSE_URL":
                if byte == b" ":
                    self.data["url"] = self.value
                    self.state = (
                        "PARSE_HTTP_VERSION"
                        if self.type == "REQ"
                        else "PARSE_HTTP_TEXT"
                    )
                    self.value = b""
                    return

                self.value += byte

            case "PARSE_HTTP_VERSION":
                if byte == b"\r":
                    self.state = "PARSE_NEWLINE" if self.type == "REQ" else "PARSE_URL"
                    self.data["version"] = self.value

                    self.value = b""
                    return

                self.value += byte

            case "PARSE_NEWLINE":
                if byte == b"\n":
                    self.state = "PARSE_HEADER_KEY"

            case "PARSE_HEADER_SPACE":
                self.state = "PARSE_HEADER_VALUE"

            case "PARSE_BODY_SEPARATOR":
                if self.body_separator_length == 1:
                    self.state = "PARSE_BODY"

                self.body_separator_length -= 1

            case "PARSE_BODY":
                if self.content_length == 1:
                    self.data["content"] += byte
                    self.state = "FINISH"

                    return self.data

                self.data["content"] += byte
                self.content_length -= 1

            case "PARSE_HEADER_KEY":
                if byte == b"\r":
                    if (
                        self.data["method"] == "GET"
                        or not "content-length" in self.headers
                    ):
                        self.state = "FINISH"
                        return self.data

                    self.content_length = int(self.headers["content-length"])
                    self.body_separator_length = 1

                    self.state = "PARSE_BODY_SEPARATOR"

                if byte == b":":
                    self.state = "PARSE_HEADER_SPACE"
                    return

                self.key += byte

            case "PARSE_HEADER_VALUE":
                if byte == b"\r":
                    self.data["headers"][self.key] = self.value
                    self.headers[self.key.decode("utf-8").lower()] = self.value.decode(
                        "utf-8"
                    )
                    self.key = b""
                    self.value = b""

                    self.state = "PARSE_NEWLINE"
                    return

                self.value += byte
