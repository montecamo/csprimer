import struct


def chunks(lst, n):
    return [lst[i : i + n] for i in range(0, len(lst), n)]


def rotate_90(pixels):
    rotated = [[None] * len(row) for row in pixels]
    h = len(pixels)
    w = len(pixels[0])

    for i in range(h):
        for j in range(w):
            rotated[j][w - i - 1] = pixels[i][j]

    return rotated


def pack_pixels(pixels, row_size):
    return [chunks(row, 3) for row in chunks(pixels, row_size)]


def unpack_pixels(pixels):
    return bytes([byte for row in pixels for pixel in row for byte in pixel])


with open("teapot.bmp", "rb") as f:
    data = f.read()
    offset, _, w, h = struct.unpack("<IIii", data[10:26])
    row_size = 3 * w

    pixels = data[offset : offset + row_size * h]

    rotated_pixels = unpack_pixels(rotate_90(pack_pixels(pixels, row_size)[::-1])[::-1])

    with open("output.bmp", "wb") as file:
        file.write(data.replace(pixels, rotated_pixels))
