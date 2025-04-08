# REQUIREMENTS
# sudo pip install adafruit-circuitpython-pn532
# sudo pip intall adafruit-blinka

# sudo raspi-config -> enable I2C in Interface Options -> reboot

import board
import busio
from adafruit_pn532.i2c import PN532_I2C

# Initialize I2C connection
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Get firmware version from PN532
ic, ver, rev, support = pn532.firmware_version
print(f"Found PN532 with firmware version: {ver}.{rev}")

# Configure PN532 to communicate with tags
pn532.SAM_configuration()

print("Waiting for an NFC card...")

while True:
    uid = pn532.read_passive_target(timeout=0.5)
    if uid is not None:
        print(f"Found NFC card with UID: {uid.hex()}")