# EinkPicoCalendar

An eInk calendar with Raspberry Pi Pico and Waveshare ePaper-4.2, allowing to mark holidays and display temperature.

# Usage

A simple calendar, displays the current temperature by the Pico's internal thermal sensor and a calendar. Use the 
two buttons on the display to move to the previous and next month. There's a file to mark holidays and special
dates that you can update. 

# Installation

1. Flash micropython in your Raspberry Pico.
2. Edit the `main.py` to adjust texts to your language.
3. Edit the `holidays.txt`: Each line should have day number and month number, comma separated.
4. Get the python files and the txt file into the Pico, be it using Thonny, rshell or any other means.
5. Plug your Pico to the WaveShare ePaper 4.2

# Related projects

This project uses code from https://github.com/peterhinch/micropython-font-to-py for generating the font files here 
and https://github.com/mcauser/micropython-waveshare-epaper as the driver for the WaveShare ePaper 4.2.
