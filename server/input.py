from evdev import UInput, ecodes as e

KEY_MAP = {
    "up": e.KEY_UP,
    "down": e.KEY_DOWN,
    "left": e.KEY_LEFT,
    "right": e.KEY_RIGHT,
    "enter": e.KEY_ENTER,
    "back": e.KEY_ESC,
    "space": e.KEY_SPACE,
    "left_click": e.BTN_LEFT,
    "right_click": e.BTN_RIGHT,
}

capabilities = {
    e.EV_KEY: list(KEY_MAP.values()),
    e.EV_REL: [e.REL_X, e.REL_Y],
}

remote = UInput(events=capabilities, name="pi-smart-remote", version=0x3)


def press(key_name):
    if key_name not in KEY_MAP:
        print("How did you do that?")
        return False
    code = KEY_MAP[key_name]
    remote.write(e.EV_KEY, code, 1)
    remote.syn()
    remote.write(e.EV_KEY, code, 0)
    remote.syn()
    return True


def move_mouse(x, y):
    remote.write(e.EV_REL, e.REL_X, int(x))
    remote.write(e.EV_REL, e.REL_Y, int(y))
    remote.syn()
