"""Display a custom character"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

snooze = 0.5  # number of seconds to sleep

# modified/semi-working
lcd_rs = digitalio.DigitalInOut(board.D6)
lcd_en = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D9)
lcd_d6 = digitalio.DigitalInOut(board.D10)
lcd_d5 = digitalio.DigitalInOut(board.D11)
lcd_d4 = digitalio.DigitalInOut(board.D12)
lcd_backlight = digitalio.DigitalInOut(board.D13)

# Initialise the LCD class
lcd = characterlcd.Character_LCD_Mono(
    lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight
)


n = 0
while n <= 10:
    for i in range(0, 10000000000, 125000000):
        time.sleep(snooze)
        lcd.text_direction = lcd.LEFT_TO_RIGHT
        mssg = str(i)
        lcd.message = "Number: \n" + mssg
        print("Number: ", mssg)
