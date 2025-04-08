# REQUIREMENTS
# sudo pip install adafruit-circuitpython-neopixel
# change `dtparam=audio=on` to `dparam=audio=off` in `/boot/firmware/config.txt`

import board
import neopixel
import time

LED_PIN = board.D18 # GPIO 18
LED_COUNT = 30

strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.1, auto_write=False)

strip.fill((50, 0, 0))  # Set all LEDs to Red
strip.show()


# Wipe LED strip with Green
for i in range(LED_COUNT):
    strip[i] = (0, 50, 0) # Green
    strip.show()
    time.sleep(0.1)
