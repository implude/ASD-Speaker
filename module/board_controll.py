def change_led_bright(bright):
    pass

import serial
import time

py_serial = serial.Serial(
    
    port='/dev/ttyUSB0',
    
    baudrate=9600,
)