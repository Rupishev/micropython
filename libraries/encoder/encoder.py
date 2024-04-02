from machine import Pin
import micropython

class Encoder:
    ROT_CW = 1     #по часовой
    ROT_CCW = 2    #против часовой
    SW_PRESS = 4   #нажата
    SW_RELEASE = 8 #отжата
    
    def __init__(self,dt,clk,sw=None):
        # фаза А, фаза В, кнопка
        self.dt_pin = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.clk_pin = Pin(clk, Pin.IN, Pin.PULL_UP)
        
        self.last_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        self.dt_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        self.clk_pin.irq(handler=self.rotary_change, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
        
        if sw:
            self.sw_pin = Pin(sw, Pin.IN, Pin.PULL_UP)
            self.sw_pin.irq(handler=self.switch_detect, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING )
            self.last_button_status = self.sw_pin.value()
        
        self.handlers = []
        

    def rotary_change(self, pin):
        new_status = (self.dt_pin.value() << 1) | self.clk_pin.value()
        if new_status == self.last_status:
            return
        transition = (self.last_status << 2) | new_status
        try:
            if transition in [0b0001, 0b0111, 0b1110, 0b1000]:
                micropython.schedule(self.call_handlers, Encoder.ROT_CW) #по часовой
            elif transition in [0b1011, 0b1101, 0b0100, 0b0010]:
                micropython.schedule(self.call_handlers, Encoder.ROT_CCW) #против часовой
        except RuntimeError:
            pass
        self.last_status = new_status

    def switch_detect(self,pin):
        if self.last_button_status == self.sw_pin.value():
            return
        self.last_button_status = self.sw_pin.value()
        try:
            if self.sw_pin.value():
                micropython.schedule(self.call_handlers, Encoder.SW_RELEASE) #отжата
            else:
                micropython.schedule(self.call_handlers, Encoder.SW_PRESS) #нажата
        except RuntimeError:
            pass

    def add_handler(self, handler):
        #передаём функцию из вне, которая потом будет обработана в прерывании
        self.handlers.append(handler)

    def call_handlers(self, type):
        for handler in self.handlers:
            handler(type) # выполняется внешняя функция с аргументом из прерывания
