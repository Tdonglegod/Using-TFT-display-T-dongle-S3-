import board
import displayio
import terminalio
import digitalio
import time
from adafruit_display_text import label

# 1. On
lcd_power = digitalio.DigitalInOut(board.IO39)
lcd_power.direction = digitalio.Direction.OUTPUT
lcd_power.value = True

# 2. Initialisation system display 
display = board.DISPLAY
display.brightness = 0.0  

# 3. СОЗДАЁМ ТЕКСТ
main_group = displayio.Group()
display.root_group = main_group

text_label = label.Label(
    terminalio.FONT,
    text="HELLO!",
    color=0x00FF00,
    x=15,
    y=40
)
main_group.append(text_label)

# 4. Button settings
button = digitalio.DigitalInOut(board.IO0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP          

# 5. Morze 
DOT_MAX = 0.3           
DASH_MIN = 0.6           
END_TIMEOUT = 2.0        
DEBOUNCE = 0.05          


last_event_time = time.monotonic()   
symbols = []                        
sos_detected = False                  

print("System started")

while True:
    now = time.monotonic()

    
    if not sos_detected:
        
        if not button.value and (now - last_event_time) > DEBOUNCE:
            press_start = now
            
            while not button.value:
                
                pass
            press_duration = time.monotonic() - press_start

            
            if press_duration <= DOT_MAX:
                symbols.append('dot')
                print(".")  
            elif press_duration >= DASH_MIN:
                symbols.append('dash')
                print("-")  
            else:
                
                pass

            
            last_event_time = time.monotonic()

        
        if symbols and (now - last_event_time) > END_TIMEOUT:
           
            seq = ''.join(symbols)
            print("Введено:", seq)

           
            if seq == "dotdash":
                text_label.text = "Goodbye"
                sos_detected = True
                print("Goodbye")
            else:
                print("clear boofer.")
            symbols.clear()   