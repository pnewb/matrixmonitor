# MatrixMonitor
Use the M5 Stack Atom Matrix as a tiny monitor for 3d printers using Klipper, Moonraker, and Mainsail.

micropython on the M5Stack Atom Matrix to monitor warmup and print status via [Mainsail](https://github.com/meteyou/mainsail) and [Moonraker](https://github.com/Arksine/klipper/tree/work-web_server-20200131/)

If there is no print in progress the device will show the current hotend temperature on the first two lines
as a percentage of the target temperature.  If you're at 80c, and the target temp is 105c, we'll display
8 lit pixels on the top two rows. (There's some arguments about if we should base this on 20c as a base temp)
The second two rows are the same, but for the bed temperature.
If the bed and the hotend are both up to temperature, the bottom row of 5 pixels is a binary representation of
how many minutes you've been up to temp.  At 30 minutes we'll just light the whole screen green.

During an active print we'll use the top 4 rows to display percentage completed, when there's an estimated 30
minutes remaining, the bottom row will be a countdown until the print is estimated to be done.


# Setup

Edit up the config.txt with your ssid and passphrase, along with the IP of the printer you'd like to monitor.

There should be a [WiFiManager-esque](https://github.com/tayfunulu/WiFiManager/) webpage to put these things in via a browser, and I'd like a long
hold on the screen/button during bootup to launch that, but first thing's first, let's make it function.


If you want to hack on this, I'd recommend VSCode with the PyMakr plugin. Once you've identified the
proper port, order of operations is:
1. Plug in the M5 Atom Matrix
2. Terminate the PyMakr console
3. Press the restart button on the side of the Matrix

Since the Matrix is such predictable hardware, I'm sure we can do an image flash at some point when we have
browser based configuration.  Until then you can follow the instructions
[here](https://m5stack.hackster.io/324677/fun-with-atom-matrix-323e3b) to get a basic micropython install.

After that you can use VSCode or the Adafruit [ampy tool](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) to upload the files onto the Matrix and you should be good to go.
