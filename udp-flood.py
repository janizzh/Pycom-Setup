import network
import socket
import time

SSID = "Pycom"
PASSWORD = "12345678"
UDP_IP = "192.168.4.1"
UDP_PORT = 12345
MESSAGE = "Hello AP!"
COUNT = 10
INTERVAL = 0

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.deinit()
wlan.init(mode=network.WLAN.STA)
wlan.connect(SSID, auth=(network.WLAN.WPA2, PASSWORD))
while not wlan.isconnected():
    time.sleep(0.5)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(COUNT):
    sock.sendto((f"{MESSAGE} #{i+1}").encode(), (UDP_IP, UDP_PORT))
    time.sleep(INTERVAL)
sock.close()
