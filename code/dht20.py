from machine import Pin, I2C
import time

cmd = bytearray(b'\xAC\x33\x00') # Measurement Commands
i2c_address = 0x38 # I2C Address
humidity_data = 0.00 # Humidity Data
temperature_data = 0.00 # Temperature Data
json_data = " " # JSON type temperature and humidity data

# DHT20 initialization of temperature and humidity sensor
def init(SCL = Pin(21), SDA = Pin(20), FREQ = 10000):
    global i2c
    
    buff = bytearray(7) # Received Data
    
    # I2C Settings
    i2c = I2C(0, scl = SCL, sda = SDA, freq = FREQ)
       
    i2c.writeto(i2c_address, cmd,  True)
    time.sleep_ms(100)
    
    i2c.readfrom_into(i2c_address, buff, True)
    time.sleep_ms(100)
    
    # Init Check
    if (buff[0] & 0x18) == 0x18:
        print('DTH20 INIT SUCCESS')
    else:
        print('DTH20 INIT FAILED')
        
# Data receiving and analyzing
def get_data():
    global humidity_data
    global temperature_data
    
    buff = bytearray(7) # Received Data
    
    # Measurement command transmission and data reception
    while True:
        i2c.writeto(i2c_address, cmd, True)
        time.sleep_ms(100)
        
        i2c.readfrom_into(i2c_address, buff, True)
        time.sleep_ms(100)
        
        # Check the data transfer
        if not (buff[0] | 0x7F) != 0x7F or buff[0] == 0x00:
            break
    
    # Data analyzing
    humidity_data_temp = (buff[1] << 12) | (buff[2] << 4) | ((buff[3] >> 4) & 0x0f)
    temperature_data_temp = ((buff[3] & 0x0f) << 16) | (buff[4] << 8) | (buff[5])
    humidity_data = humidity_data_temp / 1048576 * 100
    temperature_data = temperature_data_temp / 1048576 * 200 - 50
    
    # Display data with two decimal points
    humidity_data = round(humidity_data, 2)
    temperature_data = round(temperature_data, 2)
    
# Convert temperature and humidity data to JSON format
def to_json():
    global json_data
    json_data = "{\"temperature\": " + ('%.2f' % temperature_data) + \
                ", \"humidity\": " + ('%.2f' % humidity_data) + \
                "}"
    return json_data