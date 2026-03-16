# Using-TFT-display-T-dongle-S3-
Using the Display and Button on T-Dongle S3 (with CircuitPython)

The T-Dongle S3 is a compact ESP32‑S3 board with a built‑in color display and a single programmable button. With CircuitPython you can quickly build interactive projects – show graphics, read button presses, and more. This article explains the basics using ready‑to‑run code examples.

Contents

· Requirements
· Quick Start: Powering the Display
· Working with the Display
  · Displaying Text
  · Displaying a BMP Image
· Working with the Button
  · Simple Button Reading
  · Example: Morse Code Input
· Code Examples
· Notes

---

Requirements

· T‑Dongle S3 with CircuitPython firmware (version 8.x or later recommended).
· Required CircuitPython libraries (place them in the lib folder on the device):
  · adafruit_display_text – for text handling.
  · (For images, no extra library is needed – displayio is built in.)
· Example files:
  · code_text_display.py
  · code_image_display.py
  · code_button_use.py

Important: The display on T‑Dongle S3 is powered through a separate pin IO39. You must turn it on before using it.

Quick Start: Powering the Display

Enable the display power supply first:

```python
import board
import digitalio

lcd_power = digitalio.DigitalInOut(board.IO39)
lcd_power.direction = digitalio.Direction.OUTPUT
lcd_power.value = True   # turn display power on
```

After that you can access the board.DISPLAY object and adjust its settings:

```python
display = board.DISPLAY
display.brightness = 0.0   # see the note about brightness below
display.rotation = 0       # 0, 90, 180, 270
```

Note on brightness: On some T‑Dongle S3 units the backlight control is inverted – setting brightness = 0.0 gives maximum brightness, while 1.0 turns the backlight off. This is a known “Chinese logic” quirk. If your display stays dark, try brightness = 1.0 instead. The examples use 0.0 because that works on many devices; adjust according to your hardware.

Working with the Display

Displaying Text

Use the adafruit_display_text library to create text labels. Create a displayio.Group, add a label.Label to it, and assign the group as the root group of the display.

Example (from code_text_display.py):

```python
import board
import displayio
import terminalio
from adafruit_display_text import label

# (power‑on code omitted for brevity – see above)

display = board.DISPLAY
display.brightness = 0.0   # or 1.0 if needed

main_group = displayio.Group()
display.root_group = main_group

text_label = label.Label(
    terminalio.FONT,
    text="HELLO!",
    color=0x00FF00,      # green in hex
    x=15,                # X coordinate
    y=40                 # Y coordinate
)
main_group.append(text_label)

while True:
    pass
```

You can change the displayed text dynamically by assigning a new string to text_label.text.

Displaying a BMP Image

The display can show uncompressed BMP files (indexed colour, 16‑bit, or 24‑bit). Use displayio.OnDiskBitmap to load a file from the device’s file system.

Example (from code_image_display.py):

```python
import board
import displayio

# (power‑on code omitted)

display = board.DISPLAY
display.brightness = 0.0
display.rotation = 90   # rotate if needed

with open("image.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    group = displayio.Group()
    group.append(tile_grid)
    display.root_group = group

while True:
    pass
```

Tip: Copy your BMP file to the device’s root folder. Make sure the image dimensions and colour format are compatible with the display.

Working with the Button

The button on T‑Dongle S3 is connected to pin IO0. It is pulled up externally, so the pin reads False (low) when pressed. Use the internal pull‑up to be safe.

Simple Button Reading

```python
import board
import digitalio
import time

button = digitalio.DigitalInOut(board.IO0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP   # enable internal pull‑up

while True:
    if not button.value:           # button pressed (False)
        print("Button pressed")
        time.sleep(0.2)            # simple debounce
```

Example: Morse Code Input

A more interesting use is to interpret press duration as dots and dashes, enabling simple command input. This is implemented in code_button_use.py.

How it works:

· The button is polled in a loop.
· The duration of each press is measured.
· A short press (≤ 0.3 s) is recorded as a dot.
· A long press (≥ 0.6 s) is recorded as a dash.
· After a pause longer than 2 seconds the sequence is evaluated.
· If the sequence is dotdash (dot‑dash), the text on the display changes to "Goodbye".

Key parts:

```python
# Button setup
button = digitalio.DigitalInOut(board.IO0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Timing constants
DOT_MAX = 0.3           # max duration for a dot
DASH_MIN = 0.6          # min duration for a dash
END_TIMEOUT = 2.0       # pause after which sequence is considered complete
DEBOUNCE = 0.05         # debounce delay

# Main loop
while True:
    now = time.monotonic()
    if not button.value and (now - last_event_time) > DEBOUNCE:
        press_start = now
        while not button.value:
            pass
        press_duration = time.monotonic() - press_start

        if press_duration <= DOT_MAX:
            symbols.append('dot')
        elif press_duration >= DASH_MIN:
            symbols.append('dash')
        last_event_time = time.monotonic()

    # If symbols exist and a long pause has passed
    if symbols and (now - last_event_time) > END_TIMEOUT:
        sequence = ''.join(symbols)
        if sequence == "dotdash":    # expected command
            text_label.text = "Goodbye"
        symbols.clear()
```

Code Examples

All three examples are available in the repository. You can copy them to your T‑Dongle S3 and test them:

· code_text_display.py – simple text output.
· code_image_display.py – displays a BMP image.
· code_button_use.py – button input using Morse‑like sequences.

To run an example, rename it to code.py (or main.py) and copy it to the device. It will start automatically on the next reset or power‑up.

Notes

· If the display stays dark, check that IO39 is set as an output and pulled high. Also try brightness = 1.0 in case your unit uses inverted backlight control.
· Brightness can be adjusted, but at brightness = 0.0 the backlight may be off on some devices (see note above).
· For images, use uncompressed BMP files. Convert them online or with a graphics editor if needed.
· The examples use an infinite loop while True: pass to keep the program alive. In real projects you would place your main logic inside that loop (reading sensors, updating the screen, etc.).
· Debouncing is implemented with simple time checks. For more robust handling, consider using the adafruit_debouncer library.

---

If you have questions or suggestions, feel free to open an issue or pull request. Happy hacking with your T‑Dongle S3!
