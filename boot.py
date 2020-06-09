# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()


### Join wifi network

import config
import network
import blinky
from utime import sleep

#Activate the WiFi interface
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        blinky.print_matrix(blinky.wifi, 'orange')
        sta_if.active(True)
        sta_if.connect(config.ssid, config.passphrase)
        while not sta_if.isconnected():
            pass
            blinky.print_matrix(blinky.wifi, 'red')
            sleep(2)
            blinky.print_matrix(blinky.wifi, 'orange')
            sleep(2)
    print('network config:', sta_if.ifconfig())
    blinky.print_matrix(blinky.wifi, 'green')
    sleep(3)
    blinky.clear_screen()
    #there's definitely some little glitches, double write should fix it for clearing.
    blinky.clear_screen()

do_connect()