import os
# import sys

print(f"User: {os.getlogin()}")
print(f"Groups: {os.getgroups()}")

try:
    from evdev import UInput, ecodes as e
    print("Library found. Attempting to create device...")

    cap = {e.EV_KEY: [e.BTN_LEFT]}
    ui = UInput(cap, name="test-mouse")
    ui.write(e.EV_KEY, e.BTN_LEFT, 1)
    ui.syn()
    ui.write(e.EV_KEY, e.BTN_LEFT, 0)
    ui.syn()

    print("SUCCESS! Virtual device created at /dev/uinput")
    ui.close()

except ImportError:
    print("ERROR: evdev library not installed in this environment.")
except PermissionError:
    print("CRITICAL ERROR: Permission Denied! Your user cannot write to /dev/uinput.")
    print("Fix: You need to set up udev rules and add your user to the input group.")
except OSError as err:
    print(f"ERROR: OS Error: {err}")
