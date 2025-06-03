import board
import time
import neopixel

# NEOPIXEL TEST STUFF
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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False)
pixels_board = neopixel.NeoPixel(pixel_pin_onboard, 1, brightness=0.5, auto_write=False)

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
    time.sleep(0.5)
    pixels.fill(color2)
    pixels.show()
    time.sleep(0.5)
    pixels_on_2(YELLOW, GREEN, YELLOW, GREEN, YELLOW, BLUE, YELLOW, BLUE)
    pixels.show()
    time.sleep(0.5)

def cycle_pixels_2():
    pixels_on_2(YELLOW, GREEN, YELLOW, GREEN, YELLOW, BLUE, YELLOW, BLUE)
    pixels.show()
    time.sleep(0.5)
    leds_off()
    pixels_on(YELLOW, GREEN, YELLOW, GREEN, YELLOW, BLUE, YELLOW, BLUE)
    pixels.show()
    time.sleep(0.5)
    leds_off()


def pixels_onboard(color):
    pixels_board[0] = color
    pixels_board.show()
    time.sleep(0.1)
    pixels_board[0] = OFF
    pixels_board.show()

# def shift_light():
#     if rpm in range(100,1000):
#         pixels_on(GREEN, OFF, OFF, OFF, OFF, OFF, OFF, OFF)
#     elif rpm in range(1001,2000):
#         pixels_on(GREEN, GREEN, OFF, OFF, OFF, OFF, OFF, OFF)
#     elif rpm in range(2001,3000):
#         pixels_on(GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF, OFF)
#     elif rpm in range(3001,4000):
#         pixels_on(GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF, OFF)
#     elif rpm in range(4001,5000):
#         pixels_on(GREEN, GREEN, GREEN, GREEN, GREEN, OFF, OFF, OFF)
#     elif rpm in range(5500,5799):
#         pixels_on(GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED)
#         pixels_on_2(GREEN, GREEN, GREEN, GREEN, GREEN, RED, RED, RED)
#     elif rpm in range(5800,6500):
#         pixels_on(RED, RED, RED, RED, RED, RED, RED, RED)
    # elif rpm >= SHIFT_RPM:
    #     cycle_pixels(PURPLE,RED)
    #     pixels_onboard(CYAN)
        

while True:
    cycle_pixels_2()
    print("test")