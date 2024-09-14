#!/usr/bin/python3.10
# sudo update-desktop-database
# https://pystray.readthedocs.io/en/latest/index.html
import sys
import requests
import webbrowser
import time
import threading
from pystray import Icon, Menu, MenuItem


def on_exit_systray():
    sys.exit()


def is_24ksa01_available(url):
    response = requests.get(url)
    values = response.json()
    for v in values:
        datacenters = v["datacenters"]
        for d in datacenters:
            if "unavailable" not in d["availability"]:
                return True
    return False


JSON_URL = "https://ca.ovh.com/engine/apiv6/dedicated/server/datacenter/availabilities/?excludeDatacenters=false&planCode=24ska01&server=24ska01"
WEBSITE = "https://eco.ovhcloud.com/fr-ca/kimsufi/ks-a/"
DELAY = 60 * 5  # 5 min

if __name__ == "__main__":
    systray = Icon('kimsufi-checker', icon="kimsufi-logo.png", menu=Menu(
        MenuItem('Kimsufi-Checker', enabled=False, action=None),
        MenuItem('exit', on_exit_systray))).run()
    # Run the icon mainloop in a separate thread
    threading.Thread(target=systray.run).start()
    while True:
        if is_24ksa01_available(JSON_URL):
            webbrowser.open(WEBSITE)
            print("found !")
            break
        print("not found ...")
        time.sleep(DELAY)
