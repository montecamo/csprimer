import math

def encode(num):
    bytes = b''
    bytes_len = math.ceil(num.bit_length() / 7)

    for index in range(bytes_len):
        part = (num >> 7 * index) & 127

        if index < bytes_len - 1:
            part |= 128

        bytes += part.to_bytes(1, 'big')

    return bytes

def decode(bytes):
    result = 0

    for index, byte in enumerate(bytes):
        result |= (byte & 127) << 7 * index

    return result
