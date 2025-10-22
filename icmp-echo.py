import network

# Connect to WLAN first
wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect('Pycom', auth=(network.WLAN.WPA2, '12345678'))

while not wlan.isconnected():
    pass

print("Connected, IP:", wlan.ifconfig()[0])

# Send ICMP echo requests
response = wlan.ping("")  # replace with your target host
print("Ping response time (ms):", response)