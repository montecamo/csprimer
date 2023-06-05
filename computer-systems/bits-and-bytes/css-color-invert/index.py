import re
import sys


def normalize(str):
    if len(str[1:]) <= 4:
        return "#" + "".join([x + x for x in str[1:]])

    return str


def rgb(s):
    return f"rgb({int(s[1:3], 16)} {int(s[3:5], 16)} {int(s[5:], 16)})"


def rgba(s):
    return f"rgba({int(s[1:3], 16)} {int(s[3:5], 16)} {int(s[5:7], 16)} / {round(int(s[7:], 16) / 255, 5)})"


def hex_to_rgb(str):
    normalized = normalize(str)

    return rgb(normalized) if len(normalized) == 7 else rgba(normalized)


with open(sys.argv[1], "r") as file:
    data = file.read()

    replaced = re.sub(r"#\w{3,8}(?=;)", lambda match: hex_to_rgb(match.group(0)), data)

    print(replaced, end="")
