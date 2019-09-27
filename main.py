import network
import json

# Load wifi credentials from file
with open("wifi.json", "r") as credentials_json:
    try:
        credentials = json.load(credentials_json)
    except ValueError:
        print("ERROR: Could not parse wifi.json")
    try:
        wifi_ssid = credentials['ssid']
        wifi_pass = credentials['password']
    except KeyError:
        print("ERROR: Could not find keys in wifi.json")

# Configure wlan
wlan = network.WLAN()
wlan.active(True)
wlan.connect(wifi_ssid, wifi_pass)
while( not wlan.isconnected ):
    time.sleep(1)
print("Connected to {}".format(wifi_ssid))
