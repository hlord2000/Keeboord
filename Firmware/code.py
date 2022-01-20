import time
import board
import busio
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_mcp230xx.mcp23017 import MCP23017

# To use default I2C bus (most boards)
i2c = busio.I2C(board.A2,board.A3,frequency=400000)

mcp = [MCP23017(i2c, address = expander) for expander in [0x22, 0x20, 0x21]]

mcp_pins = []

for expander in mcp:
    for pin in range(0,16):
        mcp_pins.append(expander.get_pin(pin))
        
for i in mcp_pins:
    i.pull = digitalio.Pull.UP
    
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)
layers = [
[
Keycode.ESCAPE, Keycode.Q, Keycode.W, Keycode.E, Keycode.R, Keycode.T, Keycode.Y, Keycode.U, Keycode.I, Keycode.O, Keycode.P, Keycode.BACKSPACE,
Keycode.TAB, Keycode.A, Keycode.S, Keycode.D, Keycode.F, Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L, Keycode.SEMICOLON, Keycode.ENTER,
Keycode.SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.QUOTE,
Keycode.LEFT_CONTROL, Keycode.LEFT_GUI, Keycode.LEFT_ALT, Keycode.F20, "DOWN", Keycode.SPACE, "UP", Keycode.APPLICATION, Keycode.RIGHT_GUI, Keycode.RIGHT_ALT, Keycode.RIGHT_CONTROL
],

[
Keycode.ESCAPE, Keycode.ONE, Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO, Keycode.BACKSPACE,
Keycode.TAB, Keycode.MINUS, Keycode.EQUALS, Keycode.LEFT_BRACKET, Keycode.RIGHT_BRACKET, Keycode.G, Keycode.LEFT_ARROW, Keycode.DOWN_ARROW, Keycode.UP_ARROW, Keycode.RIGHT_ARROW, Keycode.SEMICOLON, Keycode.QUOTE,
Keycode.SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.SHIFT,
Keycode.LEFT_CONTROL, Keycode.LEFT_GUI, Keycode.LEFT_ALT, Keycode.F20, "DOWN", Keycode.SPACE, "UP", Keycode.APPLICATION, Keycode.RIGHT_GUI, Keycode.RIGHT_ALT, Keycode.RIGHT_CONTROL
],

[
Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5, Keycode.F6, Keycode.F7, Keycode.F8, Keycode.F9, Keycode.F10, Keycode.F11, Keycode.F12,
Keycode.TAB, Keycode.A, Keycode.S, Keycode.D, Keycode.F, Keycode.G, Keycode.H, Keycode.J, Keycode.K, Keycode.L, Keycode.SEMICOLON, Keycode.ENTER,
Keycode.SHIFT, Keycode.Z, Keycode.X, Keycode.C, Keycode.V, Keycode.B, Keycode.N, Keycode.M, Keycode.COMMA, Keycode.PERIOD, Keycode.FORWARD_SLASH, Keycode.QUOTE,
Keycode.LEFT_CONTROL, Keycode.LEFT_GUI, Keycode.LEFT_ALT, Keycode.F20, "DOWN", Keycode.SPACE, "UP", Keycode.APPLICATION, Keycode.RIGHT_GUI, Keycode.RIGHT_ALT, Keycode.RIGHT_CONTROL
]

]
layer_index = 0
keeboord_matrix = layers[layer_index]



matrix_converted = [
{
    0:44,
    1:21,
    2:45,
    3:22,
    4:46,
    5:23,
    6:47,
    7:24,
    8:12,
    9:36,
    10:11,
    11:35,
    12:10,
    13:34,
    14:9,
    15:33
},
{
    0:41,
    1:17,
    2:42,
    3:18,
    4:31,
    5:7,
    6:43,
    7:20,
    8:8,
    9:32,
    10:-1,
    11:19,
    12:6,
    13:30,
    14:5,
    15:29
},
{
    0:1,
    1:25,
    2:38,
    3:14,
    4:39,
    5:15,
    6:40,
    7:16,
    8:4,
    9:28,
    10:3,
    11:27,
    12:2,
    13:26,
    14:37,
    15:13
}
]
        
key_state = [0,0,0]
prev_state = [0,0,0]
held = []
layer_index = 0

while True:
    try:
        for i, expander in enumerate(mcp):    
            key_state[i-1] = 65535 - (((expander.gpiob) << 8) | (expander.gpioa))
        
        for i in range(0,3):
            for j in range(0,16):
                key_code = keeboord_matrix[matrix_converted[i][j]-1]
                key_pressed = int((key_state[i]) >> (j)) & 1
                
                if all([key_pressed, key_code == "UP", key_code not in held]):
                    if layer_index + 1 > 2:
                        layer_index = 0
                    else:
                        layer_index = layer_index + 1
                    keeboord_matrix = layers[layer_index]
                    held.append(key_code)
                    continue
                elif all([key_pressed, key_code == "DOWN", key_code not in held]):
                    if layer_index - 1 < 0:
                        layer_index = 2
                    else:
                        layer_index = layer_index - 1
                    keeboord_matrix = layers[layer_index]
                    held.append(key_code)
                    continue

                if all([key_pressed, key_code not in held]):
                    keyboard.press(key_code)
                    held.append(key_code)
                elif all([not key_pressed, key_code in held]):
                    held.remove(key_code)
                    if any([key_code == "UP", key_code == "DOWN"]):
                        continue
                    keyboard.release(key_code)
    except ValueError:
        pass