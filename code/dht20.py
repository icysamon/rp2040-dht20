from machine import Pin, I2C
import time


cmd = bytearray(b'\xAC\x33\x00') # 測定コマンド
i2c_address = 0x38 # I2Cアドレス
humidity_data = 0.00 # 湿度データ
temperature_data = 0.00 # 温度データ
json_data = " " # JSON型温湿度データ


# DHT20温湿度センサの初期化
def dht20_init(scl = Pin(21), sda = Pin(20), freq = 10000):
    global i2c
    
    buff = bytearray(7) # 受信データ
    
    # I2C通信の設定
    i2c = I2C(0, scl = scl, sda = sda, freq = freq)
       
    i2c.writeto(i2c_address, cmd,  True)
    time.sleep_ms(100)
    
    i2c.readfrom_into(i2c_address, buff, True)
    time.sleep_ms(100)
    
    # 出荷検査
    if (buff[0] & 0x18) == 0x18:
        print('DTH20初期化成功')
    else:
        print('DTH20初期化失敗')
        

# 測定データの受信と分析
def dht20_get_data():
    global humidity_data
    global temperature_data
    
    buff = bytearray(7) # 受信データ
    
    # 測定命令発信とデータ受信
    while True:
        i2c.writeto(i2c_address, cmd, True)
        time.sleep_ms(100)
        
        i2c.readfrom_into(i2c_address, buff, True)
        time.sleep_ms(100)
        
        # データの転送を確認する
        if not (buff[0] | 0x7F) != 0x7F or buff[0] == 0x00:
            break
    
    # データの分析
    humidity_data_temp = (buff[1] << 12) | (buff[2] << 4) | ((buff[3] >> 4) & 0x0f)
    temperature_data_temp = ((buff[3] & 0x0f) << 16) | (buff[4] << 8) | (buff[5])
    humidity_data = humidity_data_temp / 1048576 * 100;
    temperature_data = temperature_data_temp / 1048576 * 200 - 50;
    
    # 小数点以下２桁のデータを表示する
    humidity_data = round(humidity_data, 2)
    temperature_data = round(temperature_data, 2)
    

# 温湿度データをJSON形式に変更する
def dht20_to_json():
    global json_data
    json_data = "{\"temperature\": " + ('%.2f' % temperature_data) + \
                ", \"humidity\": " + ('%.2f' % humidity_data) + \
                "}"
    return json_data