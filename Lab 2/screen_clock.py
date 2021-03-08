import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import requests, json 
import adafruit_rgb_display.st7789 as st7789

from time import strftime

from random import randint 

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

color = "#FFFFFF"

rand_color = lambda : (randint(50, 255), randint(50, 255), randint(50,255))

#https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/

api_key = "2b2d65a0c659df2209f94b23bc340e8c"
url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + api_key + "&id=5128581" 
response = requests.get(url) 
x = response.json() 

mess = ""

fill = (0,0,0)

if x["cod"] != "401": 
    y = x["main"]
    temp = y["temp"] 
    z = x["weather"] 
    desc = z[0]["description"] 

    mess = "The current temperateure is " + str(temp) + " and the weather is " + desc

    if temp < 65:
        fill = (0,200,255)
    else:
        fill = (255,200,200)


while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=fill)

    t = strftime("%I:%M %p")

    if buttonB.value and not buttonA.value:
        color = rand_color()
    
    y = top
    draw.text((x, y), t, font=font, fill=color)
    draw.text((x, y+10), mess , font=font, fill=color)

    # Display image.
    disp.image(image, rotation)
    time.sleep(1)