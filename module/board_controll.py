import serial

py_serial = serial.Serial(
    
    port='/dev/ttyUSB0',
    
    baudrate=9600,
)

s = "ffffff"
py_serial.write(s.encode())


def change_led_bright(bright):
    pass
def change_led_color(hex_code):
    py_serial.write(hex_code.encode())



