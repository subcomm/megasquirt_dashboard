import board
import busio
import time
import digitalio
import canio
import struct

# UART settings
# uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1)
uart = busio.UART(board.A2, board.A3, baudrate=9600, timeout=1)

# Message sending to Nextion
def message_send(message):
    ending = 0xFF, 0xFF, 0xFF
    uart.write(message.encode('ascii'))
    uart.write(bytes(ending))

# Nextion baudrate change
if False:
    # To make sure Nextion is ready
    time.sleep(1)
    message_send('bauds=115200')

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
                        print("Invalid variable")
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
        message = struct.unpack(">bBBBHH", data)
        rpm = int(message[1] *10)
        rpm_p = int(message[1] * 0.625)
        clt = int(message[3])
        data_s = 'n0.val='+str(rpm)
        data_p = 'j1.val='+str(rpm_p)
        data_clt = 'n1.val='+str(clt)
        message_send(data_s)
        message_send(data_p)
        message_send(data_clt)
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
       