# Submission for the 1 hour hack at WHACK 2025

Sometimes programs on your PC just don't work. It's always good to have a CLI backup.
Broken photo viewer? Check it out in the terminal!
Broken video viewer? Just watch it in the terminal!
Broken webcam viewer? Terminal too!

# ASCII Art Terminal Renderer

`art.py` renders images, videos, or live webcam feeds as colored ASCII art directly in your terminal.

## Usage

```bash
python art.py [file] [options]
```

## Arguments

file – Path to an image or video file. Required for image or video mode. Not used for webcam mode.

## Options

--gradient – For photos/images: use a full ASCII gradient for brightness mapping. If not provided, block characters (█) are used.

--video – Treat the provided file as a video and play it in the terminal.

--webcam – Use the default webcam as a live video source.

Examples

Render an image using block characters (default):

python art.py example.jpg

Render an image using an ASCII gradient:

python art.py example.jpg --gradient

Play a video file in the terminal:

python art.py example.mp4 --video

Display a live webcam feed in the terminal:

python art.py --webcam
