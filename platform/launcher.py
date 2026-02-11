import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXT_PATH = os.path.join(BASE_DIR, "extensions", "navigator")
# FLAGS = "--kiosk --noerrdialogs --disable-infobars --check-for-update-interval=31536000 --user-agent='Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) AppleWebkit/538.1 (KHTML, like Gecko) SamsungBrowser/1.0 TV Safari/538.1' --ozone-platform-hint=auto"
FLAGS = "--kiosk --noerrdialogs --disable-infobars --check-for-update-interval=31536000"

ENV = os.environ.copy()
ENV["DISPLAY"] = ":0"

Apps = {
    "netflix": f"chromium {FLAGS} --load-extension={EXT_PATH} --app=https://www.netflix.com/browse",
    "youtube": f"chromium {FLAGS} --user-agent='Mozilla/5.0 (SMART-TV; Linux; Tizen 2.4.0) AppleWebkit/538.1 (KHTML, like Gecko) SamsungBrowser/1.0 TV Safari/538.1' --app=https://www.youtube.com/tv",
    "prime": f"chromium {FLAGS} --app=https://www.primevideo.com",
    "jellyfin": f"chromium {FLAGS} --app=https://jellyfin.pmarigo.ovh",
    "moonlight": "flatpak run com.moonlight_stream.Moonlight",
    "home": "chromium --kiosk --app=http://localhost:8002/select/",
}


def select_app(app_name: str):
    if app_name not in Apps:
        return False
    cmd = Apps[app_name]
    open_app(cmd)
    return True


def open_app(command):
    close_apps()
    print(f"Launching: {command}")
    subprocess.Popen(f"{command}", shell=True)


def close_apps():
    subprocess.run("pkill chromium", shell=True)
    subprocess.run("pkill moonlight", shell=True)
