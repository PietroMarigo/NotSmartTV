from evdev import UInput, ecodes as e


global remote
capabilities = {
    e.EV_KEY: [e.KEY_LEFT, e.KEY_RIGHT, e.KEY_UP, e.KEY_DOWN]
}
remote = UInput(events=capabilities, name="virtual buttons", version=0x3)


def up():
    remote.write(e.EV_KEY, e.KEY_UP, 1)
    remote.syn()
    remote.write(e.EV_KEY, e.KEY_UP, 0)
    remote.syn()


def down():
    remote.write(e.EV_KEY, e.KEY_DOWN, 1)
    remote.syn()
    remote.write(e.EV_KEY, e.KEY_DOWN, 0)
    remote.syn()


def left():
    remote.write(e.EV_KEY, e.KEY_LEFT, 1)
    remote.syn()
    remote.write(e.EV_KEY, e.KEY_LEFT, 0)
    remote.syn()


def right():
    remote.write(e.EV_KEY, e.KEY_RIGHT, 1)
    remote.syn()
    remote.write(e.EV_KEY, e.KEY_RIGHT, 0)
    remote.syn()
