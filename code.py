import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)

key_mappings = [
    (Keycode.ONE, "1"),
    (Keycode.TWO, "2"),
    (Keycode.THREE, "3"),
    (Keycode.FOUR, "4"),
    (Keycode.FIVE, "5"),
    (Keycode.SIX, "6"),
    (Keycode.SEVEN, "7"),
    (Keycode.EIGHT, "8"),
    (Keycode.NINE, "9"),
    (Keycode.ZERO, "0"),
]

try:
    pin_names = []
    pins = []
    
    for pin_num in range(len(key_mappings)):
        try:
            pin_attr = f"D{pin_num}"
            if hasattr(board, pin_attr):
                pin = digitalio.DigitalInOut(getattr(board, pin_attr))
                pin.direction = digitalio.Direction.INPUT
                pin.pull = digitalio.Pull.UP
                pins.append(pin)
                pin_names.append(pin_attr)
        except:
            pass

        previous_states = [True] * len(pins)
        
    while True:
        for i, pin in enumerate(pins):
            current_state = pin.value
            
            if previous_states[i] and not current_state:
                keycode, key_name = key_mappings[i]
                keyboard.send(keycode)
            
            previous_states[i] = current_state
        
        time.sleep(0.01)
    
except Exception as e:
    print(f"Error setting up keyboard: {e}")
