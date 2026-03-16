import board
import displayio
import terminalio
import digitalio
from adafruit_display_text import label

# 1. On
lcd_power = digitalio.DigitalInOut(board.IO39)
lcd_power.direction = digitalio.Direction.OUTPUT
lcd_power.value = True 

# 2. initialization system display
display = board.DISPLAY

# 3. 

display.brightness = 0.0  # or 1.0 if not work.
# 4.Display text
main_group = displayio.Group()
display.root_group = main_group

text_label = label.Label(
    terminalio.FONT, 
    text="HELLO!", 
    color=0x00FF00, # HEX
    x=15, 
    y=40
)
main_group.append(text_label)

print("System started")

while True:
    pass
