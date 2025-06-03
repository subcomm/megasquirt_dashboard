# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Display a custom character"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# modified/semi-working
lcd_rs = digitalio.DigitalInOut(board.D5)
lcd_en = digitalio.DigitalInOut(board.D6)
lcd_d7 = digitalio.DigitalInOut(board.D9)
lcd_d6 = digitalio.DigitalInOut(board.D10)
lcd_d5 = digitalio.DigitalInOut(board.D11)
lcd_d4 = digitalio.DigitalInOut(board.D12)
lcd_backlight = digitalio.DigitalInOut(board.D13)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)

i = 0
while i <= 10:
    lcd.backlight = True
    print("Hello\nCircuitPython")
    lcd.message = "Hello\nCircuitPython"
# Wait 5s
    time.sleep(0.5)
    lcd.clear()
# Print two line message right to left
    lcd.text_direction = lcd.RIGHT_TO_LEFT
    print("Hello\nCircuitPython")
    lcd.message = "Hello\nCircuitPython"
# Wait 5s
    time.sleep(0.5)
# Return text direction to left to right
    lcd.text_direction = lcd.LEFT_TO_RIGHT
# Display cursor
    lcd.clear()
    lcd.cursor = True
    print("Cursor! ")
    lcd.message = "Cursor! "
# Wait 5s
    time.sleep(0.5)
# Display blinking cursor
    lcd.clear()
    lcd.blink = True
    lcd.message = "Blinky Cursor!"
    print("Blinky Cursor! ")
# Wait 5s
    time.sleep(0.5)
    lcd.blink = False
    lcd.clear()
# Create message to scroll
    scroll_msg = "<-- Scroll"
    lcd.message = scroll_msg

# Scroll message to the left
    for i in range(len(scroll_msg)):
        time.sleep(0.5)
        lcd.move_left()
        lcd.clear()
        lcd.message = "Going to sleep\nCya later!"
        print("Going to sleep\nCya later!")
        time.sleep(3)
# Turn backlight off
#lcd.backlight = False
    time.sleep(2)
