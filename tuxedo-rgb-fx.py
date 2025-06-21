#!/usr/bin/env python3

import sys, os, time, random, atexit, signal
from pathlib import Path
import math

# --- SETTINGS ---
# You can tweak these values to change the speed and feel of the effect.

# Number of steps in the transition from one color to the next.
# Higher values make the transition longer and smoother.
TRANSITION_STEPS = 60

# Time (in seconds) to wait between each step.
# Lower values result in a smoother, higher-FPS animation. e.g., 0.016 is ~60 FPS.
SLEEP_DURATION = 0.02

# Minimum "distance" between the current and the next target color in the RGB space.
# This ensures transitions are visually distinct and not between two very similar colors.
MIN_COLOR_DIFFERENCE = 300
# -----------------

# --- SCRIPT INTERNALS ---
CONTROL_FILE = None

def find_control_file():
    """Auto-detects the keyboard's `multi_intensity` control file."""
    global CONTROL_FILE
    try:
        base_path = Path("/sys/class/leds/")
        kbd_dirs = list(base_path.glob("*kbd_backlight*"))
        if not kbd_dirs:
            raise FileNotFoundError("Could not find a compatible keyboard backlight device.")
        CONTROL_FILE = kbd_dirs[0] / "multi_intensity"
        if not os.access(CONTROL_FILE, os.W_OK):
            raise PermissionError(f"Control file '{CONTROL_FILE}' is not writable.")
    except Exception as e:
        print(f"Error finding control file: {e}", file=sys.stderr)
        sys.exit(1)

def write_color(r, g, b):
    """Writes the RGB color values to the system control file."""
    if not CONTROL_FILE: return
    try:
        with open(CONTROL_FILE, "w") as f:
            f.write(f"{r} {g} {b}")
    except IOError:
        # This can happen if the script is stopped during a write. It's safe to ignore.
        pass

def cleanup():
    """Sets the keyboard to a default white color on script exit."""
    if CONTROL_FILE and CONTROL_FILE.exists():
        write_color(255, 255, 255)

# --- COLOR CONVERSION AND GENERATION ---

def rgb_to_hsl(r, g, b):
    """Converts an RGB color to HSL."""
    r /= 255.0; g /= 255.0; b /= 255.0
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2.0
    if max_c == min_c:
        h = s = 0.0
    else:
        d = max_c - min_c
        s = d / (2.0 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
        if max_c == r: h = (g - b) / d + (6.0 if g < b else 0.0)
        elif max_c == g: h = (b - r) / d + 2.0
        else: h = (r - g) / d + 4.0
        h /= 6.0
    return h, s, l

def hsl_to_rgb(h, s, l):
    """Converts an HSL color to RGB."""
    def hue_to_rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q - p) * 6 * t
        if t < 1/2: return q
        if t < 2/3: return p + (q - p) * (2/3 - t) * 6
        return p
    if s == 0:
        r, g, b = l, l, l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    return int(r * 255), int(g * 255), int(b * 255)

def generate_vibrant_color():
    """Generates a random, aesthetically-pleasing color in HSL space."""
    # We generate colors in HSL for better visual results.
    h = random.random()              # Random Hue (the color itself, e.g., red, green, blue)
    s = random.uniform(0.8, 1.0)     # High Saturation (vivid, not grayish)
    l = random.uniform(0.5, 0.6)     # Medium Lightness (bright, but not washed out white)
    return hsl_to_rgb(h, s, l)

# --- MAIN EFFECT LOGIC ---

def run_effect_loop():
    """The main loop that creates and displays the color transitions."""
    current_r, current_g, current_b = generate_vibrant_color()
    while True:
        target_r, target_g, target_b = generate_vibrant_color()

        # Convert start and end colors to HSL for a smooth transition.
        h1, s1, l1 = rgb_to_hsl(current_r, current_g, current_b)
        h2, s2, l2 = rgb_to_hsl(target_r, target_g, target_b)

        # Calculate the change per step in HSL space.
        step_h = (h2 - h1) / TRANSITION_STEPS
        step_s = (s2 - s1) / TRANSITION_STEPS
        step_l = (l2 - l1) / TRANSITION_STEPS

        for i in range(1, TRANSITION_STEPS + 1):
            # Calculate the next intermediate HSL value.
            new_h, new_s, new_l = h1 + step_h * i, s1 + step_s * i, l1 + step_l * i

            # Convert the intermediate HSL color back to RGB.
            final_r, final_g, final_b = hsl_to_rgb(new_h, new_s, new_l)

            write_color(final_r, final_g, final_b)
            time.sleep(SLEEP_DURATION)

        # The target color becomes the new starting color for the next cycle.
        current_r, current_g, current_b = target_r, target_g, target_b

# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Ensure the script is run with root privileges.
    if os.geteuid() != 0:
        print("This script must be run as root.", file=sys.stderr)
        sys.exit(1)

    # Find the necessary system files to control the keyboard.
    find_control_file()

    # Register the cleanup function to run on exit.
    atexit.register(cleanup)

    # Handle termination signals gracefully to run the cleanup function.
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))

    # Start the main effect loop.
    run_effect_loop()
