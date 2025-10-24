import time
import network

SSID = "Pycom"       # Choose Wi-Fi SSID / name
PASSWORD = "12345678"  # Type in password of the selected Wi-Fi

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.deinit()
wlan.init(mode=network.WLAN.STA)

def send_probe_request(target_ssid):

    print("Scanning for networks...")
    nets = wlan.scan(ssid=target_ssid, type=wlan.SCAN_ACTIVE)

    if nets:
        net = nets[0]
        print("Found:", net.ssid)
        if net.ssid == target_ssid:
            print("WiFi found - sent probe.")
            return
    else:
        print("No networks found.")



for i in range(100):
    send_probe_request(SSID)