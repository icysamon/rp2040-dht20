from machine import Pin
import time, dht20

led = Pin("LED", Pin.OUT)

dht20.init()
time.sleep_ms(100)


while True:
    led.toggle()
    dht20.get_data()
    print(dht20.to_json())
    print(dht20.temperature_data)
    print(dht20.humidity_data)
    time.sleep(3)