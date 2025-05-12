import asyncio
from bleak import BleakClient, BleakScanner
import RPi.GPIO as GPIO
from rpi_ws281x import PixelStrip, Color
import time 

# WS2812B Config
LED_COUNT = 25
LED_PIN = 18
strip = None

# Buzzer setup
BUZZER_PIN = 17
buzzer = None
buzzer_task = None 

current_level = 0 

def set_led_color(level):
    global strip
    if level == 0:
        color = Color(0, 255, 0)  # Green 
    elif level == 1:
        color = Color(128, 0, 128)  # Purple 
    elif level == 2:
        color = Color(255, 255, 0)  # Yellow 
    elif level == 3:
        color = Color(255, 0, 0)  # Red 

    try:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
        strip.show()
    except Exception as e:
        print(f"Error setting LED color: {e}")


async def buzzer_controller():
    global current_level, buzzer
    last_buzz_state = False
    
    while True:
        level = current_level
        
        if level == 0:
            # Level 0: Buzzer OFF
            if last_buzz_state:
                buzzer.stop()
                last_buzz_state = False
            await asyncio.sleep(0.1)  # Check level periodically
        
        elif level == 1:
            buzzer.start(50)  # 50% duty cycle
            last_buzz_state = True
            await asyncio.sleep(0.2)
            buzzer.stop()
            last_buzz_state = False
            await asyncio.sleep(0.8)
        
        elif level == 2:
            buzzer.start(75)
            last_buzz_state = True
            await asyncio.sleep(0.1)
            buzzer.stop()
            last_buzz_state = False
            await asyncio.sleep(0.2)
        
        elif level == 3:
            buzzer.start(100)
            last_buzz_state = True
            await asyncio.sleep(0.05)
            buzzer.stop()
            last_buzz_state = False
            await asyncio.sleep(0.1)
        
        else:
            if last_buzz_state:
                buzzer.stop()
                last_buzz_state = False
            await asyncio.sleep(0.1)


def notification_callback(sender, data):
    global current_level
    if data and len(data) == 1:
        try:
            # Corrected byte order to 'little' for single byte from ArduinoBLE
            received_level = int.from_bytes(data, byteorder='little')

            if received_level != current_level:
                print(f"Car at Level: {received_level}")
                current_level = received_level # Update the global level
                set_led_color(received_level) # Update LEDs 

        except Exception as e:
            print(f"Error processing received data: {e}, Data: {data}")


async def main():
    global strip, buzzer, buzzer_task, current_level

    # --- Setup ---
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Initialize Buzzer Pin 
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    buzzer = GPIO.PWM(BUZZER_PIN, 1000) 

    # Initialize LED strip
    strip = PixelStrip(LED_COUNT, LED_PIN)
    strip.begin()
    set_led_color(0) 
    print("Buzzer, and LED Strip initialized.")

    print("Scanning for BLE devices...")
    arduino_name = "Nano33" 
    device = await BleakScanner.find_device_by_name(arduino_name, timeout=10.0)

    if not device:
        print(f"Could not find device '{arduino_name}'. Make sure it's advertising.")
        GPIO.cleanup()
        return

    print(f"Found device: {device.name} - {device.address}")

    # --- BLE Connect and Listen ---
    async with BleakClient(device.address) as client:
        print(f"Connected to {device.address}")

        # Correct 128-bit UUID for standard Digital Output characteristic
        characteristic_uuid = "00002a56-0000-1000-8000-00805f9b34fb" 

        # Start the buzzer control task in the background
        buzzer_task = asyncio.create_task(buzzer_controller())

        print(f"Subscribing to characteristic: {characteristic_uuid}")
        await client.start_notify(characteristic_uuid, notification_callback)
        print("Listening for notifications...")

        while client.is_connected:
            await asyncio.sleep(1)  # Keep main thread alive, tasks run in background


if __name__ == '__main__':
    asyncio.run(main())
