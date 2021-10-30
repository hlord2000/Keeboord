# Keeboord
## Created for the Mechanical Keyboard Club at Georgia Tech

This is a mechanical keyboard for Kaihl and Cherry switches.  It utilizes no diodes, instead registering button presses by using I2C I/O expanders.  These give interrupts to the microcontroller, an Adafruit QT Py RP2040, which then read from each I/O expander.