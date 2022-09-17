def change_led_bright(bright):
    pass

import serial
import time

py_serial = serial.Serial(
    
    port='COM3',
    
    baudrate=9600,
)

while True:
      
    commend = input('Order: ')
    py_serial.write(commend.encode())
    time.sleep(0.1)
    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())