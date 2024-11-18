import machine
import time
import urequests
import network
import ujson

# Load WiFi configurations from config.json
with open('config.json') as f:
    config = ujson.load(f)

WIFI_CONFIGS = config['WIFI']
CURRENT_WIFI_INDEX = 0

def connect_wifi():
    global CURRENT_WIFI_INDEX
    # Initialize the WiFi interface in station mode
    station = network.WLAN(network.STA_IF)
    station.active(True)  # Activate the station

    # Try to connect to each WiFi network in the list
    index = 0
    for wifi in WIFI_CONFIGS:
        ssid = wifi['SSID']
        password = wifi['PASSWORD']
        if not station.isconnected():
            print(f"Connecting to network {ssid}...")
            station.connect(ssid, password)

            # Wait for the connection
            for _ in range(10):  # Try for 10 seconds
                if station.isconnected():
                    break
                time.sleep(1)
                print("Connecting...")

        if station.isconnected():
            print(f"Connected to network {ssid}! IP address:", station.ifconfig()[0])
            CURRENT_WIFI_INDEX = index
            return

    print("Unable to connect to any WiFi network.")

connect_wifi()

# Define the GPIO pin where the LED is connected
led = machine.Pin(2, machine.Pin.OUT)
switch = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

# Functions to send HTTP requests
def send_right_signal():
    global CURRENT_WIFI_INDEX
    try:
        response = urequests.get(f"{WIFI_CONFIGS[CURRENT_WIFI_INDEX]['IP']}/right")
        print("Single Click Request Sent, Status:", response.status_code)
        response.close()
    except Exception as e:
        print(f"Error sending single click request to {WIFI_CONFIGS[CURRENT_WIFI_INDEX]['IP']}:", e)
        
def send_left_signal():
    global CURRENT_WIFI_INDEX
    try:
        response = urequests.get(f"{WIFI_CONFIGS[CURRENT_WIFI_INDEX]['IP']}/left")
        print("Single Click Request Sent, Status:", response.status_code)
        response.close()
    except Exception as e:
        print(f"Error sending single click request to {WIFI_CONFIGS[CURRENT_WIFI_INDEX]['IP']}:", e)



while True:
    if switch.value() == 0:  # 0 means the button is pressed
        
        send_right_signal()
        time.sleep_ms(50)  # Debounce