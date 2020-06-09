#main.py is called on startup after boot.py executes
import printer_monitor
from utime import sleep

while true:
    printer_monitor.run()
    sleep(30)
