# Keeboord
## Created for the Mechanical Keyboard Club at Georgia Tech
![alt text](https://github.com/hlord2000/Keeboord/blob/main/image.png?raw=true)
This is a mechanical keyboard for Kaihl and Cherry switches.  It utilizes no diodes, instead registering button presses by using I2C I/O expanders.  These give interrupts to the microcontroller, an Adafruit QT Py RP2040, which then read from each I/O expander.
