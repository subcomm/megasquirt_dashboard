# Megasquirt Can - 
# 11bit CAN headers are used at 500kbps with sequential addressing. Big-endian. 
# The default base identifier is 1512 decimal (0x5e8).

import board
import busio
import displayio
import i2cdisplaybus
import time
import digitalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label

# on-board led test
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# NEXTION DISPLAY UART/SERIAL settings
# uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1)
uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=1)

# Nextion message receiving
def receive_uart():
    receiving_data = False
    buffer = uart.in_waiting    
    if buffer != 0:
        data_r = uart.read(3)
        receiving_data = True
        received = []
        received.append(data_r)
        print(f"###### UART RECV'D:", data_r)

# Message sending to Nextion
def message_send(message):
    ending = bytearray([0xff,0xff,0xff])
    uart.write(bytes(message,'ascii'))
    # uart.write(message.encode('ascii'))
    uart.write(ending)
    print("Message Sent:", message)

# Nextion baudrate change
if False:
    # To make sure Nextion is ready
    time.sleep(1)
    message_send('bauds=115200')

while True:
    afr = "7788"
    # data_s = 'x0.val='+str(afr)
    data_s = 'x0.val='+afr
    # data_s = 'ot.val='+str(oil_t)
    #data_s = str.encode(x0.val=2222)
    message_send(data_s)
    receive_uart()
    time.sleep(1.0)


# Monochrome 0.96" 128x64 OLED ###########
WIDTH = 128
HEIGHT = 64
BORDER = 5
i2c = board.I2C()
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
# Monochrome 0.96" 128x64 OLED END ###########



