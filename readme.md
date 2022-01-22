# Keeboord
## Created for the Mechanical Keyboard Club at Georgia Tech
![image](https://github.com/hlord2000/Keeboord/blob/5662409076e690ab5b0b350bf3bddc92285a627e/image.png)

This is a mechanical keyboard for Kaihl and Cherry switches.  It utilizes no diodes, instead registering button presses by using I2C I/O expanders.  These give interrupts to the microcontroller, an Adafruit QT Py RP2040, which then read from each I/O expander.
