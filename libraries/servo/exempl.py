from servo import Servo
import time

#цикличная прокрутка
def cycl(pin):
    motor=Servo(pin) # A changer selon la broche utilisée
    motor.move(0) # tourne le servo à 0°
    time.sleep(0.3)
    motor.move(90) # tourne le servo à 90°
    time.sleep(0.3)
    motor.move(180) # tourne le servo à 180°
    time.sleep(0.3)
    motor.move(90) # tourne le servo à 90°
    time.sleep(0.3)
    motor.move(0) # tourne le servo à 0°
    time.sleep(0.3)

#перемещение от и до с регулировкой скорости

def moveTime(pin, start_angle, finish_angle, pause_ms):
    motor=Servo(pin)
    #необходимые установки
    motor.update_settings(50, 26, 123, 0, 180, pin)
    it=start_angle
    while it <= finish_angle:
        motor.move(it)
        it+=1
        time.sleep_ms(pause_ms)
    motor.stop()
    
#пример
pin = 2

moveTime(pin, 80, 100, 10) #плавный

#ручной режим
mo1 = Servo(2)
mo1.move(80)
mo1.stop()

