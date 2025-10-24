# ICMP Echo (Ping) for Pycom ESP32
# Works with firmware missing random/urandom modules
import time
import network
import socket
import struct
import select
import uctypes

# --- Wi-Fi connect ---
SSID = 'Pycom'
PASSWORD = '12345678'

wlan = network.WLAN(mode=network.WLAN.STA)
wlan.connect(SSID, auth=(network.WLAN.WPA2, PASSWORD))
print("Connecting to Wi-Fi...")

ip, netmask, gateway, dns = wlan.ifconfig()
print("Connected. IP:", ip, "Gateway:", gateway)

# --- Internet checksum ---
def checksum(data):
    if len(data) & 1:
        data += b'\x00'
    s = 0
    for i in range(0, len(data), 2):
        s += (data[i] << 8) + data[i + 1]
        s = (s & 0xffffffff)
    while s >> 16:
        s = (s & 0xffff) + (s >> 16)
    return (~s) & 0xffff

# --- Simple pseudo-random ID (no random module) ---
def get_packet_id():
    # Just use the lower 16 bits of current microsecond timer
    return time.ticks_us() & 0xFFFF

# --- Ping implementation ---
def simple_ping(host, count=4, timeout_ms=3000, size=32):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)  # 1 = ICMP
    except Exception as e:
        print("Raw socket failed:", e)
        return (0, 0)

    sock.settimeout(timeout_ms / 1000.0)
    addr = socket.getaddrinfo(host, 1)[0][-1][0]
    print("PING %s (%s): %d data bytes" % (host, addr, size))

    packet_id = get_packet_id()
    sent = 0
    received = 0

    for seq in range(1, count + 1):
        # Build ICMP header
        header = struct.pack('!BBHHH', 8, 0, 0, packet_id, seq)
        payload = struct.pack('!d', time.ticks_us()) + b'Q' * (size - 8)
        chksum = checksum(header + payload)
        header = struct.pack('!BBHHH', 8, 0, chksum, packet_id, seq)
        packet = header + payload

        try:
            sock.sendto(packet, (addr, 1))
            sent += 1
        except Exception as e:
            print("Send failed:", e)
            continue

        start_time = time.ticks_us()
        while True:
            ready, _, _ = select.select([sock], [], [], timeout_ms / 1000.0)
            if ready:
                recv_packet, addr_info = sock.recvfrom(1024)
                icmp_header = recv_packet[20:28]
                r_type, r_code, r_chksum, r_id, r_seq = struct.unpack('!BBHHH', icmp_header)
                if r_type == 0 and r_id == packet_id and r_seq == seq:
                    rtt = (time.ticks_us() - start_time) / 1000.0
                    print("%d bytes from %s: icmp_seq=%d time=%.2f ms" %
                          (len(recv_packet), addr_info[0], seq, rtt))
                    received += 1
                    break
            else:
                print("Request timeout for icmp_seq=%d" % seq)
                break

        time.sleep_ms(1000)

    sock.close()
    print("%d packets transmitted, %d packets received" % (sent, received))
    return (sent, received)

# --- Run ping to gateway (or any IP) ---
target = gateway  # e.g. "192.168.4.1"
simple_ping(target, count=4)
