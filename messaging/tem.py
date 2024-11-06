import ctypes
import time
from pynput import mouse

# Function to block user input (keyboard and mouse)
def block_input(block):
    ctypes.windll.user32.BlockInput(block)

def on_click(x, y, button, pressed):
    if block_clicks:
        print(f"Blocked click at ({x}, {y}) with {button}")
        return False  # Block clicks by returning False
    else:
        return True  # Allow normal mouse functionality

# Start the mouse listener
def block_for_duration(duration):
    global block_clicks
    with mouse.Listener(on_click=on_click) as listener:
        print(f"Blocking clicks for {duration} seconds...")
        block_clicks = True  # Enable blocking
        time.sleep(duration)  # Block clicks for the given duration
        block_clicks = False  # Disable blocking
        print("Mouse clicks unblocked.")

def bloc(ti):
    # Block input (1 to block, 0 to unblock)
    print("Blocking input for 5 seconds...")
    block_input(True)  # Block input
    block_for_duration(20)
    # time.sleep(ti)  # Keep input blocked for 5 seconds

    block_input(False)  # Unblock input
    print("Input unblocked.")

bloc(20)