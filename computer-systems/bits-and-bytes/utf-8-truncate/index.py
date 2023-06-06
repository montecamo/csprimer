def truncate(text, length):
    truncated = text[:length]

    if len(truncated) == 0 or len(truncated) == len(text) or text[length] >> 6 != 0x02:
        return truncated

    while truncated[-1] >> 6 == 0x02:
        truncated = truncated[:-1]

    return truncated[:-1]


with open("cases", "rb") as file:
    lines = file.readlines()

    for line in lines:
        bytes = truncate(line[1:].strip(), line[0])
        print(bytes.decode("utf8"))
