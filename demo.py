# this demo takes input from the rotary encoder, and drives the LED strip.
# when the rotary encoder is rotated, it moves the LED along the LED strip, each LED gets a random color, wrapping around at the ends.
# when the rotary encoder is pressed, it flashes the entire LED strip with random colors.

# REQUIREMENTS
# sudo pip install adafruit-circuitpython-neopixel
# change `dtparam=audio=on` to `dparam=audio=off` in `/boot/firmware/config.txt`

# Connections
# Rotary encoder
# CLK   ->  GPIO 17     (11)
# DT    ->  GPIO 18     (12)
# SW    ->  GPIO 27     (13)
# +     ->  3.3v        (1)
# GND   ->  GND         (6)
#
# LED strip
# V+    -> NOTHING      (X) (aangesloten aan adapter)
# V-    -> GND          (6)
# DI    -> GPIO 21      (40)

# RUNNING
# sudo python ./demo.py

import time
import random
import board
import neopixel
from gpiozero import RotaryEncoder, Button
from signal import pause

# === CONFIG ===
NUM_PIXELS = 30
PIXEL_PIN = board.D21  # GPIO21
BRIGHTNESS = 0.5

# Rotary encoder pins
CLK = 17
DT = 18
SW = 27

# === INIT ===
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

encoder = RotaryEncoder(CLK, DT, max_steps=1000)
button = Button(SW, pull_up=True, bounce_time=0.05)

position = 0

# === FUNCTIONS ===
def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def clear_strip():
    pixels.fill((0, 0, 0))
    pixels.show()

def update_led():
    clear_strip()
    index = position % NUM_PIXELS
    pixels[index] = random_color()
    pixels.show()

def flash_random_color():
    for i in range(NUM_PIXELS):
        pixels[i] = random_color()
    pixels.show()
    time.sleep(0.3)
    clear_strip()
    update_led()

def rotated():
    global position
    position = encoder.steps
    update_led()

def pressed():
    flash_random_color()

# === SETUP ===
encoder.when_rotated = rotated
button.when_pressed = pressed

update_led()
print("Running... Rotate or press the encoder. Ctrl+C to exit.")

# === LOOP ===
try:
    pause()
except KeyboardInterrupt:
    clear_strip()
    print("\nExiting...")
