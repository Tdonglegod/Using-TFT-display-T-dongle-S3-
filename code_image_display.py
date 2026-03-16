import board
import displayio
import digitalio

# 1. On (IO39)
lcd_power = digitalio.DigitalInOut(board.IO39)
lcd_power.direction = digitalio.Direction.OUTPUT
lcd_power.value = True 

# 2. Settings
display = board.DISPLAY
display.brightness = 0.0  
display.rotation = 90    

# 3. Loading image.bmp
with open("image.bmp", "rb") as bitmap_file:
    bitmap = displayio.OnDiskBitmap(bitmap_file)
    
    
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

    
    

    group = displayio.Group()
    group.append(tile_grid)
    display.root_group = group

    print("Image displayed!")

    while True:
        pass

