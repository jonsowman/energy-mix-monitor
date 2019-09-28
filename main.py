import network
import json
import energy
import ssd1306
import time
import ntptime
from machine import Pin, I2C, RTC

def connect_wifi():
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
    while( not wlan.isconnected() ):
        time.sleep(1)
    print("Connected to {}".format(wifi_ssid))

    # Set NTP
    ntptime.settime()

def configure_oled():
    # Configure oled
    i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    return oled

if __name__ == '__main__':
    # Run init
    connect_wifi()
    oled = configure_oled()
    rtc = RTC()

    # Run forever
    while True:
        mix = energy.mix()
        oled.fill(0)
        # Write time
        time_now = rtc.datetime()
        oled.text("Last: {:02d}:{:02d}:{:02d}".format(time_now[4],
            time_now[5], time_now[6]), 0, 0)
        # Write energy fractions
        oled.text("Wind: {}%".format(mix.percent("wind")), 0, 20)
        oled.text("Solar: {}%".format(mix.percent("solar")), 0, 30)
        oled.text("Hydro: {}%".format(mix.percent("hydro")), 0, 40)
        oled.text("Imports: {}%".format(mix.percent("imports")), 0, 50)
        oled.show()
        time.sleep(30)

