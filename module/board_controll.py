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
    plain = "B" + str(amount)
    py_serial.write(plain.encode())

change_led_color('Xffffff')
print("LED start")


def bright_down_hex(hex_code):
    R = int(hex_code[0:2], 16)
    G = int(hex_code[2:4], 16)
    B = int(hex_code[4:6], 16)
    R = R - 100
    G = G - 100
    B = B - 100
    if R < 0:
        R = 0
    if G < 0:
        G = 0
    if B < 0:
        B = 0
    hex_R = format(R, '2x')
    hex_G = format(G, '2x')
    hex_B = format(B, '2x')
    print(hex_R + hex_G + hex_B)
    return hex_R + hex_G + hex_B

def bright_up_hex(hex_code):
    R = int(hex_code[0:2], 16)
    G = int(hex_code[2:4], 16)
    B = int(hex_code[4:6], 16)
    R = R + 100
    G = G + 100
    B = B + 100
    if R > 255:
        R = 255
    if G > 255:
        G = 255
    if B > 255:
        B = 255
    hex_R = format(R, '2x')
    hex_G = format(G, '2x')
    hex_B = format(B, '2x')
    return hex_R + hex_G + hex_B

