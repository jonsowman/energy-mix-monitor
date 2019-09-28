import network
import json
import energy
import ssd1306
import time
from machine import Pin, I2C

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
    return wlan

def configure_oled():
    # Configure oled
    i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    return oled

def update_display(oled, wlan, since_last, mix, ci):
    oled.fill(0)
    # Write time
    oled.text("Last  : {:.0f} secs".format(since_last), 0, 0)
    if wlan.isconnected():
        oled.text("Wifi  : OK", 0, 9)
    else:
        oled.text("Wifi  : disconn", 0, 9)
    # Write energy fractions
    oled.text("Wind  : {:.1f}%".format(mix.percent("wind")), 0, 17)
    oled.text("Solar : {:.1f}%".format(mix.percent("solar")), 0, 26)
    oled.text("Bio   : {:.1f}%".format(mix.percent("biomass")), 0, 35)
    oled.text("Import: {:.1f}%".format(mix.percent("imports")), 0, 44)
    oled.hline(0, 54, 128, 1)
    oled.text("Intens: {:.0f}g/kWh".format(ci.current), 0, 56)
    oled.show()

def run():
    # Run init
    wlan = connect_wifi()
    oled = configure_oled()
    first_run = True

    # Track the last update time
    last_update = time.ticks_ms()

    # Run forever
    while True:
        time_now = time.ticks_ms()
        time_since_last = time.ticks_diff(time_now, last_update) / 1000
        if time_since_last > 30 or first_run:
            last_update = time_now
            mix = energy.mix()
            ci = energy.intensity()
            first_run = False
        update_display(oled, wlan, time_since_last, mix, ci)
        time.sleep(1)

if __name__ == '__main__':
    run()
