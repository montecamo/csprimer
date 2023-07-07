import socket
import struct
import sys


def qname(url):
    labels = url.split(".")
    qname_bytes = b""

    for label in labels:
        qname_bytes += len(label).to_bytes(1, byteorder="big")
        qname_bytes += bytes(label, "ascii")

    return qname_bytes + b"\x00"


def request(url):
    id = b"\x88\x88"
    flags = b"\x01\x00"

    qdcount = b"\x00\x01"
    ancount = b"\x00\x00"
    nscount = b"\x00\x00"
    arcount = b"\x00\x00"

    qtype = b"\x00\x01"
    qclass = b"\x00\x01"

    question = qname(url) + qtype + qclass

    return id + flags + qdcount + ancount + nscount + arcount + question


def parse_answers(data, offset):
    id, flags, qdcount, ancount = struct.unpack(">HHHH", data[0:8])

    answers = data[offset:]

    return [answers[i * 16 : (i + 1) * 16] for i in range(ancount)]


def parse_answer(answer):
    offset, type, clas, ttl, rdlen, addr = struct.unpack(">HHHIHI", answer)

    return addr


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect(("1.1.1.1", 53))

req = request(sys.argv[1])

s.send(req)
data = s.recv(4096)

id, flags, qdcount, ancount = struct.unpack(">HHHH", data[0:8])

answers = parse_answers(data, len(req))

for address in [parse_answer(answer) for answer in answers]:
    ip = ".".join([str(x) for x in address.to_bytes(4, byteorder="big")])

    print(ip)

s.close()
