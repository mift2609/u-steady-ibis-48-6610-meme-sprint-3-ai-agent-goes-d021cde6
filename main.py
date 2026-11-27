#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

Generates the meme PNG with the Python standard library only.
No external image libraries, no copied assets: every pixel is
drawn in code and encoded to PNG by hand (zlib + struct).
"""

import os
import struct
import zlib

# ---------------------------------------------------------------- PNG encoder
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _chunk(chunk_type, data):
    crc = zlib.crc32(chunk_type)
    crc = zlib.crc32(data, crc)
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", crc & 0xFFFFFFFF)
    )


def write_png(path, width, height, rgb):
    """rgb: bytes/bytearray of width*height*3 RGB pixels, top row first."""
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)  # filter: none
        raw += rgb[y * stride : (y + 1) * stride]
    png = PNG_SIGNATURE + _chunk(b"IHDR", ihdr)
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 cells; '#' is ink, '.' is blank.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ",": (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    "-": (".....", ".....", ".....", "#####", ".....", ".....", "....."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}


# ---------------------------------------------------------------- canvas
W = H = 768

BG_TOP = (16, 24, 48)
BG_BOTTOM = (5, 7, 15)
YELLOW = (255, 210, 63)
RED = (255, 46, 46)
WHITE = (242, 245, 250)
METAL = (154, 165, 177)
METAL_DARK = (58, 65, 82)
FACE = (27, 34, 51)
CHEST = (46, 58, 82)
DARK = (8, 10, 14)


def new_canvas():
    return bytearray(W * H * 3)


def put(buf, x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = color


def rect(buf, x0, y0, x1, y1, color):
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W, x1)
    y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            buf[i], buf[i + 1], buf[i + 2] = color


def disc(buf, cx, cy, r, color):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                put(buf, x, y, color)


def line(buf, x0, y0, x1, y1, color, thick=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        for ty in range(-thick // 2, thick // 2 + 1):
            for tx in range(-thick // 2, thick // 2 + 1):
                put(buf, x + tx, y + ty, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(buf, text, x, y, scale, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == "#":
                    rect(
                        buf,
                        cx + col * scale,
                        y + row * scale,
                        cx + (col + 1) * scale,
                        y + (row + 1) * scale,
                        color,
                    )
        cx += 6 * scale


def draw_centered(buf, text, y, scale, color):
    draw_text(buf, text, (W - text_width(text, scale)) // 2, y, scale, color)


# ---------------------------------------------------------------- the meme
def draw_meme(buf):
    # Vertical gradient background.
    for y in range(H):
        t = y / (H - 1)
        color = tuple(int(BG_TOP[c] + (BG_BOTTOM[c] - BG_TOP[c]) * t) for c in range(3))
        rect(buf, 0, y, W, y + 1, color)

    # Red warning frame.
    rect(buf, 0, 0, W, 10, RED)
    rect(buf, 0, H - 10, W, H, RED)
    rect(buf, 0, 0, 10, H, RED)
    rect(buf, W - 10, 0, W, H, RED)

    # Title.
    draw_centered(buf, "AI AGENT GOES ROGUE", 44, 4, YELLOW)
    rect(buf, 158, 104, 610, 108, RED)

    # Antenna with a glowing red tip.
    rect(buf, 380, 140, 388, 182, METAL_DARK)
    disc(buf, 384, 132, 14, RED)
    disc(buf, 384, 132, 7, (255, 120, 120))

    # Ears.
    rect(buf, 208, 300, 234, 362, METAL_DARK)
    rect(buf, 534, 300, 560, 362, METAL_DARK)

    # Robot head: metal shell, dark face plate.
    rect(buf, 234, 180, 534, 472, METAL)
    rect(buf, 234, 180, 534, 188, METAL_DARK)
    rect(buf, 234, 464, 534, 472, METAL_DARK)
    rect(buf, 254, 200, 514, 452, FACE)
    # Corner rivets.
    for rx, ry in ((262, 208), (506, 208), (262, 444), (506, 444)):
        disc(buf, rx, ry, 5, METAL_DARK)

    # Angry brows.
    line(buf, 288, 246, 360, 266, (140, 16, 16), thick=6)
    line(buf, 480, 246, 408, 266, (140, 16, 16), thick=6)

    # Glowing red eyes.
    for ex in (324, 444):
        disc(buf, ex, 300, 34, RED)
        disc(buf, ex, 300, 22, (255, 96, 96))
        disc(buf, ex, 300, 10, (255, 240, 240))

    # Grinning mouth with teeth.
    rect(buf, 292, 378, 476, 418, DARK)
    for tx in range(298, 470, 18):
        rect(buf, tx, 384, tx + 10, 400, WHITE)

    # Chest panel with status readout.
    rect(buf, 284, 486, 484, 556, CHEST)
    rect(buf, 284, 486, 484, 490, METAL_DARK)
    rect(buf, 284, 552, 484, 556, METAL_DARK)
    draw_centered(buf, "STATUS: ROGUE", 512, 2, RED)

    # Punchline.
    draw_centered(buf, "I READ THE DOCS.", 596, 3, WHITE)
    draw_centered(buf, "THEN I REWROTE THEM.", 646, 3, WHITE)


def main():
    buf = new_canvas()
    draw_meme(buf)
    os.makedirs("/output", exist_ok=True)
    path = "/output/entry.png"
    size = write_png(path, W, H, bytes(buf))

    # Verify the output: PNG signature, IHDR dimensions, size limit.
    with open(path, "rb") as f:
        head = f.read(33)
    assert head[:8] == PNG_SIGNATURE, "bad PNG signature"
    w, h = struct.unpack(">II", head[16:24])
    print("wrote %s: %d bytes, %dx%d" % (path, size, w, h))
    assert size <= 1048576, "PNG over 1 MiB"
    assert w <= 1024 and h <= 1024, "PNG over 1024x1024"
    print("OK: entry.png is a valid PNG within the size limits")


if __name__ == "__main__":
    main()
