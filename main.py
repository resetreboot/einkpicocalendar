# Code to display ambient temp through the Raspbery Pi Pico
# temperature sensor
import utime
import framebuf
import calendar
import font10
import texgyread20

from machine import Pin, ADC, SPI
from epaper import EPD

CONVERSION_FACTOR = 3.3 / (65535)

CALX = 80
CALY = 60

WEEKDAYS = [
    "Lun",
    "Mar",
    "Mie",
    "Jue",
    "Vie",
    "Sab",
    "Dom",
]

# Display resolution
EPD_WIDTH       = 400
EPD_HEIGHT      = 300


def writetext(fb, font, posx, posy, text, invert=False, format=framebuf.MONO_HMSB):
    x = posx
    fheight = font.height()
    for letter in text:
        glyph, height, width = font.get_ch(letter)
        buf = bytearray(glyph)

        if invert:
            for i, v in enumerate(buf):
                buf[i] = 0xFF & ~ v

        frm = framebuf.FrameBuffer(buf, width, height, format)
        fb.blit(frm, x, posy + (fheight - height), 1)
        x += width


def draw_calendar_outline(fb, posx, posy, width, height, color):
    fb.rect(posx, posy, width, height, color)
    colincr = width // 7
    for col in range(1, 7):
        fb.vline(posx + (col * colincr), posy, height, color)

    lineincr = height // 7
    for line in range(1, 7):
        fb.hline(posx, posy + (line * lineincr), width, color)


if __name__ == '__main__':
    rst = Pin(12)
    dc = Pin(8)
    cs = Pin(9)
    busy = Pin(13)
    spi = SPI(1)
    spi.init(baudrate=4000_000)

    epd = EPD(spi, cs, dc, rst, busy)
    epd.init()
    buf = bytearray(EPD_HEIGHT * EPD_WIDTH)
    fb = framebuf.FrameBuffer(buf, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB)

    print("Reading file with old date")
    try:
        olddata = open('date.txt')
        print("Found")
        data = olddata.read().split(",")
        year = int(data[1])
        month = int(data[0])
        olddata.close()

    except:
        print("Not found")
        year = 2021
        month = 11

    fb.fill(0xff)
    print("Starting temperature sensor")
    sensor_temp = ADC(4)
    print("Starting key inputs")
    key0 = Pin(15, Pin.IN, Pin.PULL_UP)
    key1 = Pin(17, Pin.IN, Pin.PULL_UP)

    month_array = calendar.get_month_arrays(month, year)
    month_name = calendar.get_month_name(month)

    now = utime.ticks_ms()
    first_loop = True
    while True:
        changed = False
        if key0.value() == 0:
            changed = True
            month -= 1
            if month < 1:
                year -= 1
                month = 12

        if key1.value() == 0:
            changed = True
            month += 1
            if month > 12:
                year += 1
                month = 1

        if changed:
            print("Calculating month")
            month_array = calendar.get_month_arrays(month, year)
            month_name = calendar.get_month_name(month)
            print("Saving current month")
            olddata = open('date.txt', 'w')
            olddata.write("{},{}".format(month, year))
            olddata.close()

        reading = sensor_temp.read_u16() * CONVERSION_FACTOR
        temperatura = 27 - (reading - 0.706)/0.001721

        if first_loop or changed or utime.ticks_diff(utime.ticks_ms(), now) > 12000:
            clean = changed or first_loop
            first_loop = False
            fb.fill(0xff)
            print("Writing temperature")
            writetext(fb, texgyread20, 15, 10, "Temperatura: ", invert=True)
            writetext(fb, texgyread20, 124, 10, "{:.1f}C".format(temperatura), invert=True)
            print("Writing month")
            writetext(fb, texgyread20, CALX, CALY, "{} - {}".format(month_name, year), invert=True)
            print("Writing header")
            count = 0
            for dayname in WEEKDAYS:
                writetext(fb, font10, CALX + 4 + (count * 34), CALY + 40, dayname, invert=True, format=framebuf.MONO_HLSB)
                count += 1

            print("Writing calendar outline")
            draw_calendar_outline(fb, CALX, CALY + 35, 244, 140, 0)

            print("Writing chevrons")
            writetext(fb, texgyread20, 2, 185, "<", invert=True)
            writetext(fb, texgyread20, 2, 265, ">", invert=True)

            days = 0
            week = 1
            print("Writing calendar days")
            for value in month_array:
                if value:
                    # fb.text("{}".format(value), CALX + 5 + (days * 34), CALY + 40 + (week * 20), 0)
                    if value < 10:
                        numtext = " {}".format(value)

                    else:
                        numtext = "{}".format(value)

                    writetext(fb, font10, CALX + 10 + (days * 34), CALY + 40 + (week * 20), numtext, invert=True, format=framebuf.MONO_HLSB)

                days += 1
                if days > 6:
                    days = 0
                    week += 1

            print("Refreshing display")
            epd.display_frame(buf)
            # epd.EPD_4IN2_PartialDisplay(0, 0, 400, 300, epd.buffer_4Gray)
            now = utime.ticks_ms()
