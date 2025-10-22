import network
import socket
import pycom
import _thread
import time

pycom.heartbeat(False)

ap = network.WLAN(mode=network.WLAN.AP, ssid="Pycom", auth=(network.WLAN.WPA2, "12345678"))
time.sleep(2)
print("AP started. Connect to SSID 'Pycom'")