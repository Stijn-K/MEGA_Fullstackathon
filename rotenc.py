from gpiozero import RotaryEncoder, Button
from threading import Event

# Pin numbers: GPIO <num>
rotor = RotaryEncoder(16, 20, wrap=True, max_steps=180)
rotor.steps = -180
btn = Button(27, pull_up=False)

done = Event()

def rotation():
    print(f"{rotor.steps=}")

def btn_pressed():
    print(f"button pressed")


def stop_script():
    print("exiting")
    done.set()

rotor.when_rotated = rotation
btn.when_released = btn_pressed
btn.when_held = stop_script


done.wait()