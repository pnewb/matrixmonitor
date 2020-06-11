import config

# Use fetch for testing, use urequests for actually checking a running printer
#import fetch as requests
import urequests as requests

from machine import Pin
from neopixel import NeoPixel
from utime import sleep
from utime import time

#These are notes on what URLS return what kind of data, the {"result"}
# sections are all pulled direct from the printer during actual prints

#http://192.168.3.4:7125/printer/status?virtual_sdcard
# printing: {"result": {"virtual_sdcard": {"print_duration": 1516.7326718700006, "total_duration": 1516.7326718700006, "filament_used": 1393.625989999889, "is_active": true, "current_file": "Buck_Holder_-_buck_base.gcode", "file_position": 1149701, "progress": 0.9590440098798881}}}
# not printing: {"result": {"virtual_sdcard": {"print_duration": 0.0, "total_duration": 0.0, "filament_used": 0.0, "is_active": false, "current_file": "", "file_position": 0, "progress": 0.0}}}
#http://192.168.3.4:7125/printer/status?display_status
#{"result": {"display_status": {"progress": 0.68, "message": null}}}
#http://192.168.3.4:7125/printer/status?heater_bed
#{"result": {"heater_bed": {"temperature": 99.96510699366026, "target": 100.0}}}
#printer/status?extruder
#{"result": {"extruder": {"pressure_advance": 0.788, "target": 235.0, "temperature": 234.
#meteyou V2.167.347Today at 12:00 AM
#@pnewb V2.042 | V2.142 i think this is only the status for the display (M73). i use virtual_sdcard percent -> http://192.168.3.4:7125/printer/status?virtual_sdcard=progress
#this command is only for progress. if you need also the estimation time, remove "=progress" and you get more data.
#
#Arksine V2.179Today at 3:24 AM
#That is correct.  If what you want is M73 status then display_status.progress is what you want.  Keep in mind that there is a timeout with that variable, if it doesn't receive an update after 5 seconds it resets to zero.  File progress can be found the way meteyou mentioned.
#The remaining time calculations need to be done by the client, they are fairly simple.  You can get the total estimated time via the request to the file list (it shows up in metadata).  A simple calculation for remaining time can be done something like this
#remaining = est_time - (est_time * progress)
#The virtual_sdcard object also has two attributes, "print_duration" and "total_duration".  The "total_duration" is the number of seconds that have elapsed since the print started.  The "print_duration" is generally the same, but it excludes any time spent paused.   They can be used to estimated remaining times if you have no metadata
#remaining = print_duration / progress - print_duration

status_url = 'http://{}:{}/printer/status?'.format(config.printer_ip, config.printer_port)
temperatures_reached_time = False
np = NeoPixel(Pin(27), 25)

colors = {'red': (50,0,0),
          'green': (0,50,0),
          'blue': (0,0,50),
          'white': (50,50,50),
          'orange': (50,25,0),
          'off': (0,0,0),
          }



def percentage_complete_if_printing():

    status = requests.get(status_url + 'virtual_sdcard').json()

    if status['result']['virtual_sdcard']['is_active']:
        return status['result']['virtual_sdcard']['progress']

    return False

def display_percentage_complete(pct_complete):
    pixel_count = round(int(pct_complete * 10)) * 2

    for pxl in range(pixel_count):
        np[pxl] = colors['blue']

    np.write()


def display_temperatures(temps):
    temps_reached = 0
    print(temps)
    for key,value in temps.items():
        item = key
        number = value

        if number:
            pixel_count = int(number/10)
        else:
            pixel_count = 0
        print('{} temp: {}'.format(item, number))

        #we need a little wiggle room for rounding
        if number > 98:
            temps_reached += 1
            pixel_count = 10

        if item == 'heater_bed':
            pixel_start = 10
            print_color = 'orange'
        else:
            pixel_start = 0
            print_color = 'red'

        pixel_count += pixel_start

        for pxl in range(pixel_start, pixel_count):
            np[pxl] = colors[print_color]

    if temps_reached == 2:
        display_time(time_at_temp())
    else:
        temperatures_reached_time = False

    np.write()


def display_time(time):
    if time > 20:
        pass
        #do something to indicate printer is ready to go
    else:
        binary_time = "{:05b}".format(int(time))
        print('binary_time: {}'.format(binary_time))
        pixel_count = 20
        for pxl in str(binary_time):
            if int(pxl):
                np[pixel_count] = colors['green']
                print('lighting pixel {}'.format(pixel_count))
            else:
                np[pixel_count] = colors['off']
                print('blanking pixel {}'.format(pixel_count))

            pixel_count += 1

    np.write()


def get_current_temperatures():
    temps = {}
    for item in ['extruder', 'heater_bed']:
        temperatures = requests.get(status_url + item).json()
        target = temperatures['result'][item]['target']
        current_temp = temperatures['result'][item]['temperature']

        if target == 0:
            temps[item] = 0
        else:
            percentage = current_temp / target
            temps[item] = int(percentage * 100)
    return temps

def time_at_temp():
    #This is not 100% accurate.  The prior code to check the temperature_store worked great, except
    # that it overflowed the memory limits on this tiny little device.
    global temperatures_reached_time

    if not temperatures_reached_time:
        temperatures_reached_time = time()

    max_time_at_target = 20 * 60

    time_at_target = time() - temperatures_reached_time
    print('Minutes at target temperature: {}'.format(time_at_target/60))

    if time_at_target < max_time_at_target:
        return time_at_target/60

    return max_time_at_target/60

    


def run():
    percentage_complete = percentage_complete_if_printing()

    if percentage_complete:
        print('displaying percentage complete...')
        display_percentage_complete(percentage_complete)
        #Still need to deal with finding the remaining time and printing that out at the bottom once we're sub 30m
    else:
        display_temperatures(get_current_temperatures())
