from machine import Pin
from neopixel import NeoPixel
from utime import sleep


#Too many LEDs in a tiny box, we should limit ourselves to
# a max of %20 power, 255 is the max intensity for each sub-pixel
# so don't go over 51 in any RGB value

colors = {'red': (50,0,0),
          'green': (0,50,0),
          'blue': (0,0,50),
          'white': (50,50,50),
          'orange': (50,25,0),
          'off': (0,0,0),
          }



np = NeoPixel(Pin(27), 25)

def print_matrix(grid, color):
    pxl_idx = 0
    for pxl in grid:
        if pxl:
            np[pxl_idx] = colors[color]
        else:
            np[pxl_idx] = colors['off']
        pxl_idx+=1
    np.write()
    
def clear_screen():
    for pxl in range(25):
        np[pxl] = colors['off']
    np.write()
        
numbers = {
           'zero':
             [0,1,1,1,0,
              0,1,0,1,0,
              0,1,0,1,0,
              0,1,0,1,0,
              0,1,1,1,0],
           'one':
             [0,0,1,0,0,
              0,0,1,0,0,
              0,0,1,0,0,
              0,0,1,0,0,
              0,0,1,0,0],
           'two':
             [0,1,1,1,0,
              0,0,0,1,0,
              0,1,1,1,0,
              0,1,0,0,0,
              0,1,1,1,0],
           'three':
             [0,1,1,1,0,
              0,0,0,1,0,
              0,1,1,1,0,
              0,0,0,1,0,
              0,1,1,1,0],
           'four':
             [0,1,0,1,0,
              0,1,0,1,0,
              0,1,1,1,0,
              0,0,0,1,0,
              0,0,0,1,0],
           'five':
             [0,1,1,1,0,
              0,1,0,0,0,
              0,1,1,1,0,
              0,0,0,1,0,
              0,1,1,1,0],
           'six':
             [0,1,1,1,0,
              0,1,0,0,0,
              0,1,1,1,0,
              0,1,0,1,0,
              0,1,1,1,0],
           'seven':
             [0,1,1,1,0,
              0,0,0,1,0,
              0,0,0,1,0,
              0,0,0,1,0,
              0,0,0,1,0],
           'eight':
             [0,1,1,1,0,
              0,1,0,1,0,
              0,1,1,1,0,
              0,1,0,1,0,
              0,1,1,1,0],
           'nine':
             [0,1,1,1,0,
              0,1,0,1,0,
              0,1,1,1,0,
              0,0,0,1,0,
              0,0,0,1,0],
           }

#This was the best I could come up with, but it's trash.
# I want some kind of "everything is good" or "waiting"
# image.
voron = [0,0,1,0,1,
         0,1,0,1,0,
         1,0,1,0,1,
         0,1,0,1,0,
         1,0,1,0,0]

wifi  = [0,1,1,0,0,
         0,0,0,1,0,
         1,1,0,0,1,
         0,0,1,0,1,
         1,0,1,0,0]

def countdown():
    print_matrix(numbers['nine'], 'green')
    sleep(1)
    print_matrix(numbers['eight'], 'green')
    sleep(1)
    print_matrix(numbers['seven'], 'green')
    sleep(1)
    print_matrix(numbers['six'], 'green')
    sleep(1)
    print_matrix(numbers['five'], 'green')
    sleep(1)
    print_matrix(numbers['four'], 'green')
    sleep(1)
    print_matrix(numbers['three'], 'green')
    sleep(1)
    print_matrix(numbers['two'], 'blue')
    sleep(1)
    print_matrix(numbers['one'], 'red')
    sleep(1)
    print_matrix(numbers['zero'], 'red')
    sleep(1)
    clear_screen()

clear_screen()