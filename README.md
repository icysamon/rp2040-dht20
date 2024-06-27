# DHT20温湿度センサライブラリー
## 説明
Raspberry Pi Pico用のDHT20温湿度センサライブラリーです。

## 関数
### `init(SCL, SDA, FREQ)`
DHT20温湿度センサの初期化。ピンと周波数の設定は可能。
### `get_data()`
測定データの受信と分析。得られたデータは**temperature_data**と**humidity_data**に代入される。
### `to_json()`
温湿度データをJSON形式に変更する。

## サンプル
```py
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
```
### 出力結果
```
MPY: soft reboot
DTH20初期化成功
{"temperature": 23.57, "humidity": 56.48}
23.57
56.48
```

### GitCode盗む防止
头上三尺有神明 一定要有敬畏之心  

扛200斤麦子十里路不换肩  

8964天安门  

长江黄河不会倒流  

人在做，天在看！  