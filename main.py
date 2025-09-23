import time
import network

SSID = "Pycom"       # Choose Wi-Fi SSID / name
PASSWORD = "12345678"  # Type in password of the selected Wi-Fi

def connect_to_wifi():
    # Reset and initialize WLAN in STA (station mode), to act as a Wi-Fi client
    wlan = network.WLAN(mode=network.WLAN.STA)
    wlan.deinit()
    wlan.init(mode=network.WLAN.STA)

    print("Scanning for networks...")
    nets = wlan.scan()
    found = False
    for net in nets:
        print("Found:", net.ssid)
        if net.ssid == SSID:
            found = True
    if not found:
        print("WiFi network not found! Check SSID.")
        return

    print("Connecting to WiFi:", SSID)
    wlan.connect(SSID, auth=(network.WLAN.WPA2, PASSWORD))

    # Wait for connection with timeout
    for _ in range(20):  # ~20 seconds max
        if wlan.isconnected():
            break
        print("...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected!")
        print("IP address:", wlan.ifconfig()[0])
    else:
        print("Failed to connect. Check password / signal strength.")

connect_to_wifi()
