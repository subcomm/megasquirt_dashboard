import board
import busio
import time
import digitalio
import canio
import struct
import neopixel

# Main VARS
rpm = 0
SHIFT_RPM = 7600

# Nextion Displays UART interfaces
uart = busio.UART(board.A2, board.A3, baudrate=115200, timeout=1) # DASH RIGHT
uart2 = busio.UART(board.TX, board.RX, baudrate=115200, timeout=1) # DASH LEFT


# NEOPIXEL STUFF
pixel_pin_onboard = board.NEOPIXEL # ON-BOARD NEOPIXEL
pixel_pin = board.A5
num_pixels = 16
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
OFF = (0, 0, 0)

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.05, auto_write=False)
pixels_board = neopixel.NeoPixel(pixel_pin_onboard, 1, brightness=0.05, auto_write=False)

# n0.val=bauds // places bauds value in n0.val component

def pixels_on(clr0, clr1, clr2, clr3, clr4, clr5, clr6, clr7):
    pixels[0] = clr0
    pixels[1] = clr1
    pixels[2] = clr2
    pixels[3] = clr3
    pixels[4] = clr4
    pixels[5] = clr5
    pixels[6] = clr6
    pixels[7] = clr7
    pixels.show()

def pixels_on_2(clr0, clr1, clr2, clr3, clr4, clr5, clr6, clr7):
    pixels[8] = clr0
    pixels[9] = clr1
    pixels[10] = clr2
    pixels[11] = clr3
    pixels[12] = clr4
    pixels[13] = clr5
    pixels[14] = clr6
    pixels[15] = clr7
    pixels.show()

def leds_off():
    pixels.fill((0, 0, 0))

def cycle_pixels(color1, color2):        
    pixels.fill(color1)
    pixels.show()
    time.sleep(0.1)
    pixels.fill(color2)
    pixels.show()
    

def pixels_onboard(color):
    pixels_board[0] = color
    pixels_board.show()
    time.sleep(0.1)
    pixels_board[0] = OFF
    pixels_board.show()

def shift_light():
    if rpm in range(100,1000):
        pixels_on(GREEN, OFF, OFF, OFF, OFF, OFF, OFF, OFF)
        pixels_on_2(GREEN, OFF, OFF, OFF, OFF, OFF, OFF, OFF)
    elif rpm in range(1001,2000):
        pixels_on(GREEN, GREEN, OFF, OFF, OFF, OFF, OFF, OFF)
        pixels_on_2(GREEN, GREEN, OFF, OFF, OFF, OFF, OFF, OFF)
    elif rpm in range(2001,3000):
        pixels_on(GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF, OFF)
        pixels_on_2(GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF, OFF)
    elif rpm in range(3001,4000):
        pixels_on(GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF)
        pixels_on_2(GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF)
    elif rpm in range(4001,5000):
        pixels_on(GREEN, GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF)
        pixels_on_2(GREEN, GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF)
    elif rpm in range(5500,5799):
        pixels_on(GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED)
        pixels_on_2(GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED)
    elif rpm in range(5800,6500):
        pixels_on(RED, RED, RED, RED, RED, RED, RED, RED)
        pixels_on_2(CYAN, RED, CYAN, RED, CYAN, RED, CYAN, RED)
    elif rpm >= SHIFT_RPM:
        cycle_pixels(PURPLE,RED)
        pixels_onboard(CYAN)


# Message sending to Nextion
def message_send(message):
    ending = 0xFF, 0xFF, 0xFF
    # print(message)
    uart.write(message.encode('ascii'))
    uart.write(bytes(ending))
    uart2.write(message.encode('ascii'))
    uart2.write(bytes(ending))
    


# CAN BUS
# The CAN transceiver has a standby pin, bring it out of standby mode
if hasattr(board, 'CAN_STANDBY'):
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)

# The CAN transceiver is powered by a boost converter, turn on its supply
if hasattr(board, 'BOOST_ENABLE'):
   boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
   boost_enable.switch_to_output(True)

# Can Bus pins
can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=500_000, auto_restart=True)

# CAN listener 0x600 - 0x607
listener = can.listen(matches=[canio.Match(1512, mask=1516)], timeout=2.0)

old_bus_state = None


while True:
    # Debug
    # counter += 1
    # if counter > 1000:
    #    break
    # rpm -= 1
    # print(rpm)

    # Uart message receiving
    receiving_data = False
    buffer = uart.in_waiting
    if buffer != 0:
        data_r = uart.read(1)
        receiving_data = True
        received = []
        received.append(data_r)

    while receiving_data is True:
        data_r = uart.read(1)
        # print("Receiving")
        if data_r == b'\xff':
            data_r = uart.read(1)
            if data_r == b'\xff':
                data_r = uart.read(1)
                if data_r == b'\xff':
                    # Message ended
                    receiving_data = False
                    if received == [b'\x00', b'\x00', b'\x00']:
                        print("Nextion Startup")
                    elif received == [b'\x88']:
                        print("Nextion Ready")
                    elif received == [b'\x1a']:
                        print("Nextion: Invalid variable")
                    elif received == [b'\0x11']:
                        print("Nextion: Invalid Baud")
                    elif received == [b'\0x24']:
                        print("Nextion: Serial Buffer Overflow")
                    else:
                        print('Message: ', received)
        else:
            received.append(data_r)
    

    # CAN BUS
    # Bus state information
    bus_state = can.state
    if bus_state != old_bus_state:
        print(f"Bus state changed to {bus_state}")
        old_bus_state = bus_state
    
    message = listener.receive()

    # Message handling
    if message is None:
        print("No message received within timeout")
        # time.sleep(1)
        continue

    data = message.data
    if len(data) != 8:
        print(f"Unusual message length {len(data)}")
        # time.sleep(1)
        continue

    id = message.id


    if id == 1512: # RPM
        # Unpack message
        message = struct.unpack(">BBBBBBBB", data) # >HBbHH
        # size = struct.calcsize(">BBBBBBBB")
        # print("Size:", size)
        # print("Raw_Data:", data)
        # print(message)
        rpm = int(message[2] * 100)
        print("RPM:", rpm)

        data_s = 'n0.val='+str(rpm)
        message_send(data_s)
        shift_light()
        
    elif id == 1513:
        message = struct.unpack("<bBBBHH", data)
        # Oil pressure
        oil_p = int(message[2])
        data_s = 'n2.val='+str(oil_p)
        message_send(data_s)    
    elif id == 1514: # AFR
        message = struct.unpack("<bBBBHH", data)
        # Lambda
        lambda_value = int(message[1])
        # print(lambda_value)
        data_s = 'x0.val='+str(lambda_value)
        data_p = 'j0.val='+str((lambda_value) * 0.10)
        message_send(data_s)
        message_send(data_p)
        
    elif id == 1515:
        message = struct.unpack("<BbHHBB", data)
        # Battery voltage
        battery_v = int(message[0])
        data_s = 'ba.val='+str(battery_v)
        message_send(data_s)
    
    elif id == 1516:
        message = struct.unpack(">BBBBBBBB", data)
        # Battery voltage
        clt = int(message[4])
        data_s = 'n2.val='+str(clt)
        message_send(data_s)
        
        print("Raw_Data:", data)
        print(message)

