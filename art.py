from PIL import Image
import shutil, time, os, argparse
from colorama import init
import cv2

init()

ASCII_CHARS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def get_terminal_size():
    ts = shutil.get_terminal_size(fallback=(80, 24))
    return ts.columns, ts.lines


def get_pixel_colors(image):
    width, height = image.size
    pixels = list(image.getdata())
    return [pixels[i * width : (i + 1) * width] for i in range(height)]


def rgb_to_char(r, g, b):
    brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255
    index = int(brightness * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]


def print_colored_ascii(pixel_grid, char=""):
    RESET = "\033[0m"
    for row in pixel_grid:
        line = []
        for r, g, b in row:
            ch = char if char else rgb_to_char(r, g, b)
            line.append(f"\033[38;2;{r};{g};{b}m{ch}")
        print("".join(line) + RESET)


def render_frame(frame):
    term_w, term_h = get_terminal_size()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img = img.resize((term_w, int(term_h * 2 / 3)), Image.LANCZOS)
    colors = get_pixel_colors(img)
    os.system("cls" if os.name == "nt" else "clear")
    print_colored_ascii(colors, char="█")


def render_image(path):
    img = Image.open(path).convert("RGB")
    term_w, term_h = get_terminal_size()
    img = img.resize((term_w, int(term_h * 2 / 3)), Image.LANCZOS)
    colors = get_pixel_colors(img)
    print_colored_ascii(colors, char="")


def render_video(path, skip=1):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    delay = 1 / fps
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            render_frame(frame)
            time.sleep(delay)

            for _ in range(skip - 1):
                cap.read()
    except KeyboardInterrupt:
        print("\033[0m")
        cap.release()


def render_webcam(skip=1, max_fps=15):
    cap = cv2.VideoCapture(0)  # 0 = default webcam
    fps = cap.get(cv2.CAP_PROP_FPS) or max_fps
    delay = 1 / min(fps, max_fps)  # cap FPS for performance

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue  # keep trying if a frame fails

            render_frame(frame)
            time.sleep(delay)

            # Skip N-1 frames to improve speed
            for _ in range(skip - 1):
                cap.read()
    except KeyboardInterrupt:
        print("\033[0m")
        cap.release()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render an image or video as colored ASCII in the terminal"
    )
    parser.add_argument("file", nargs="?", help="Path to image or video file")
    parser.add_argument("--video", action="store_true", help="Render file as video")
    parser.add_argument("--webcam", action="store_true", help="Use webcam instead of a file")
    parser.add_argument(
        "--gradient",
        action="store_true",
        help="Use an ASCII gradient instead of block characters (█)",
    )
    args = parser.parse_args()

    if args.webcam:
        render_webcam(skip=2)  # adjust skip as needed
    elif args.video:
        render_video(args.file, skip=4)
    else:
        if not args.gradient:
            ASCII_CHARS = "█"
        render_image(args.file)
