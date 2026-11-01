# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# esp32 micropython access point
# save to boot.py if esp32 should be an independant access point with own dhcp

import network

# Define network name and password (password must be at least 8 characters)
SSID = "ESP32-MicroPython-AP"
PASSWORD = "mysecretpassword"

# Create a WLAN object in Access Point mode
ap = network.WLAN(network.AP_IF)

# Activate the access point interface
ap.active(True)

# Configure the network SSID and password
ap.config(essid=SSID, password=PASSWORD)

# Print the assigned IP address (defaults to 192.168.4.1)
print("Access Point started!")
print("IP Address:", ap.ifconfig()[0])
