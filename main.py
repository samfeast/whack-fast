import argparse
from PIL import Image
import shutil
from colorama import init
import cv2

init()

ASCII_CHARS = " .:-=+*#%@"
# ASCII_CHARS = " .'`^,:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_terminal_size():
    ts = shutil.get_terminal_size(fallback=(80, 24))
    return ts.columns, ts.lines


def load_and_resize_image(path):
    img = Image.open(path).convert("RGB")
    term_w, term_h = get_terminal_size()
    target_w = term_w
    target_h = int(term_h * 2 / 3)
    resized = img.resize((target_w, target_h), Image.LANCZOS)
    return resized


def get_pixel_colors(image):
    """
    Returns a 2D list of (R, G, B) tuples for each pixel in the image.
    """
    width, height = image.size
    pixels = list(image.getdata())
    pixel_grid = [pixels[i * width : (i + 1) * width] for i in range(height)]
    return pixel_grid


def print_colored_ascii(pixel_grid, char=""):
    RESET = "\033[0m"
    for row in pixel_grid:
        line = []
        for r, g, b in row:
            if char == "":
                ch = rgb_to_char(r, g, b)
            else:
                ch = char
            line.append(f"\033[38;2;{r};{g};{b}m{ch}")
        print("".join(line) + RESET)


def rgb_to_char(r, g, b):
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    index = int(brightness * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render an image as colored ASCII in the terminal")
    parser.add_argument("image_file", help="Path to the image file to render")
    args = parser.parse_args()

    img_path = args.image_file
    img = load_and_resize_image(img_path)
    # Optional: save resized image for debugging
    img.save("resized_example.jpg")
    colors = get_pixel_colors(img)
    print_colored_ascii(colors, char="")
