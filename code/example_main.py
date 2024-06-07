from machine import Pin
import time, dht20

led = Pin("LED", Pin.OUT)

dht20.dht20_init()
time.sleep_ms(100)


while True:
    led.toggle()
    dht20.dht20_get_data()
    print(dht20.dht20_to_json())
    time.sleep(3)