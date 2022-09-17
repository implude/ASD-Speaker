import serial

py_serial = serial.Serial(
    
    port='/dev/ttyUSB0',
    
    baudrate=9600,
)

s = "ffffff"
py_serial.write(s.encode())
print("LED start")

def change_led_color(hex_code):
    py_serial.write(hex_code.encode())


def bright_down_hex(hex_code):
    R = int(hex_code[0:2], 16)
    G = int(hex_code[2:4], 16)
    B = int(hex_code[4:6], 16)
    R = R - 50
    G = G - 50
    B = B - 50
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
    R = R + 50
    G = G + 50
    B = B + 50
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

