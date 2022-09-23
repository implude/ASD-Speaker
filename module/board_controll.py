import serial,time

py_serial = serial.Serial(
    
    port='/dev/ttyUSB0',
    
    baudrate=9600,
)


def change_led_color(hex_code):
    print(hex_code)
    plain = "X" + hex_code
    py_serial.write(plain.encode())

def change_led_bright(amount):
    print(amount)
    plain = "B" + '{0:03d}'.format(amount)
    py_serial.write(plain.encode())

change_led_color('ffffff')
print("LED start")

