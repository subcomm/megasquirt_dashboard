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
import canio
import struct
import terminalio
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
        data_r = uart.read(2)
        receiving_data = True
        received = []
        received.append(data_r)
        print(f"###### UART RECV'D:", data_r)

# Nextion Message sending
def message_send(message):
    ending = 0xFF, 0xFF, 0xFF
    uart.write(message.encode('ascii'))
    uart.write(bytes(ending))
    print("Message Sent:", message)

# Nextion baudrate change
if False:
    # To make sure Nextion is ready
    time.sleep(1)
    message_send('bauds=115200')



# Monochrome 0.96" 128x64 OLED ###########
WIDTH = 128
HEIGHT = 64
BORDER = 5
i2c = board.I2C()
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)
# Monochrome 0.96" 128x64 OLED END ###########


# If the CAN transceiver has a standby pin, bring it out of standby mode
if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)

# If the CAN transceiver is powered by a boost converter, turn on its supply
if hasattr(board, 'BOOST_ENABLE'):
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)

# Use this line if your board has dedicated CAN pins. (Feather M4 CAN and Feather STM32F405)
can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=500_000, auto_restart=True)

# canio.Match(id: int, *, mask: Optional[int] = None, extended: bool = False)
listener = can.listen(matches=[canio.Match(1512, mask=1516)], timeout=1.0)
# listener = can.listen(timeout=1.0) # Listen for all message IDs


old_bus_state = None
old_count = -1
count = 0


while True:
    bus_state = can.state
    if bus_state != old_bus_state:
        print(f"Bus state changed to {bus_state}")
        old_bus_state = bus_state

    message = listener.receive()
    if message is None:
        print("No messsage received within timeout!")
        print("Continuing...")
        receive_uart()
        continue

    data = message.data
    id = message.id
    if len(data) != 8:
        print(f"Unusual message length {len(data)}")
        print(f"message_id:", id)
        print(f"message_data:", message.data)

    # MAP, RPM, CLT, TPS
    elif id == 1512:
        # count += 1
        # print(f"message_count:", count)
        # print(f"message_id:", id)
        # print(f"message_data:", message.data)
        message_struct = struct.unpack('>HBbHH', data)
        map = float(message_struct[0] * 0.10)
        rpm = message_struct[1]
        clt = float(message_struct[3] * 0.10)
        tps = float(message_struct[4] * 0.10)
        # print(f"message unpacked:", message_struct)
        print(f"MAP:", map, "RPM", rpm)
        print(f"RPM:", rpm)
        data_s = 'n0.val='+str(rpm)
        message_send(data_s)
        print(f"Temp:", clt, "TPS", tps)
        
    
    # MAT - MASS AIR TEMPERATURE
    elif id == 1513:
        message_struct = struct.unpack('>bBBBHH', data)
        mat = float(message_struct[4] * 0.10)
        # print(f"MAT:", mat)
        # time.sleep(1.0)

    # AFR (AIR/FULE RATIO)
    elif id == 1514:
        message_struct = struct.unpack('>bBBBHH', data)
        afr = int(message_struct[1] * 10)
        print(f"AFR:", afr)
        data_s = 'x0.val='+str(afr)
        message_send(data_s)
        receive_uart()

    # BAT VOLTAGE
    elif id == 1515:
        message_struct = struct.unpack('>HBbHH', data)
        bat = float(message_struct[0] * 0.10)
        # print(f"message_id:", id)
        # print(f"message_data:", message.data)
        print(f"BAT:", bat)
        data_s = 'x1.val='+str(bat)
        message_send(data_s)
        

    elif id == 1516:
        message_struct = struct.unpack('>HBbHH', data)
        msg0 = message_struct[0]
        print(f"msg0:", msg0)

    else:
        message_struct = struct.unpack('>HBbHH', data)
        print(f"message_id:", id)
        print(f"unrecognized message:", message_struct)


