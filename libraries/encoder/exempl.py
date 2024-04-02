from encoder import Encoder
import time
from machine import Pin

# GPIO Pins A и B, третий кнопка необязательный
enc = Encoder(14, 12, 13)
val = 0

def encoder_changed(change):
    global val
    if change == Encoder.ROT_CW:
        val = val + 1
        print(val)
    elif change == Encoder.ROT_CCW:
        val = val - 1
        print(val)
    elif change == Encoder.SW_PRESS:
        print('PRESS')
    elif change == Encoder.SW_RELEASE:
        print('RELEASE')

enc.add_handler(encoder_changed)

while True:
    time.sleep_ms(10)