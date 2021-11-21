# Keeboord
## Created for the Mechanical Keyboard Club at Georgia Tech
![image](https://user-images.githubusercontent.com/36466317/142748067-17710f67-7b27-449e-8bc0-62e4a7e345fe.png)

This is a mechanical keyboard for Kaihl and Cherry switches.  It utilizes no diodes, instead registering button presses by using I2C I/O expanders.  These give interrupts to the microcontroller, an Adafruit QT Py RP2040, which then read from each I/O expander.
