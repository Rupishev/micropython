from uModBusSerial import uModBusSerial as ModBusRTU
import time

pins = [0,1] #TX,RX
master = ModBusRTU(1, 9600, 8, 1, None, pins)

i = 0
response = False

# 01 06 F0 08 03E8 - частота 10hz в EEPROM параметр P0-08 = 0

while not response or i > 10:
    i += 1
    try:
        response = master.write_single_register(1, 0xF008, 0x03E8)
        time.sleep_ms(10)
        
    except: 
        print(i)
        if i > 10:
            print('Прошло больше 10 итераций без ответа')
            break
        
else:
        print('изменение частота 10hz')
        response = False

# 01 06 20 00 00 01 - Вращение в прямом направлении

while not response or i > 10:
    i += 1
    try:
        response = master.write_single_register(1, 0x2000, 0x0001)
        time.sleep_ms(10)
        
    except: 
        print(i)
        if i > 10:
            print('Прошло больше 10 итераций без ответа')
            break 
        
else:
        print('Вперед')
        response = False
    
time.sleep(3)

# 01 06 20 00 00 06 - стоп

while not response or i > 10:
    i += 1
    try:
        response = master.write_single_register(1, 0x2000, 0x0006)
        time.sleep_ms(10)
        
    except: 
        print(i)
        if i > 10:
            print('Прошло больше 10 итераций без ответа')
            break 
   
else:
        print('Стоп')
        response = False
        
time.sleep(2)


        #master.read_holding_registers(1, 0x00, 0x000A) # 01 03 0000 000A C5CD
        #time.sleep_ms(10)