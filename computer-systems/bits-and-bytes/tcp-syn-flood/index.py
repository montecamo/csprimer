def parse_tcp(frame):
    flags = frame[13]

    return {
        "ack": (flags & 0b00010000) >> 4,
    }


def parse_ipv4(frame):
    header_length = (frame[4] & 0x0F) * 4

    return parse_tcp(frame[header_length + 4 :])


with open("synflood.pcap", "rb") as file:
    syn = 0
    ack = 0

    file.read(24)
    while file.read(8):
        size = int.from_bytes(file.read(4), "little")
        file.read(4)

        parsed = parse_ipv4(file.read(size))

        if parsed["ack"]:
            ack += 1
        else:
            syn += 1

    print(f"{round(ack / syn * 100)}%")
