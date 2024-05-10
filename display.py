import time
import threading
import RPi.GPIO as GPIO
from PIL import Image
import ST7789 as ST7789

# GPIO.setmode(GPIO.BCM)

# We must set the backlight pin up as an output first
# GPIO.setup(13, GPIO.OUT)

# Set up our pin as a PWM output at 500Hz
# backlight = GPIO.PWM(13, 500)
# backlight.stop()

# Create ST7789 LCD display class.
disp = ST7789.ST7789(
    width=240,
    height=240,
    rotation=90,
    port=0,  # SPI port
    cs=ST7789.BG_SPI_CS_FRONT,  # SPI port Chip-select channel # BG_SPI_CS_BACK or BG_SPI_CS_FRONT
    dc=9,  # BCM pin used for data/command
    backlight=19,   # 18 for back BG slot, 19 for front BG slot.
    spi_speed_hz=80 * 1000 * 1000,
    offset_left=40
)

WIDTH = disp.width
HEIGHT = disp.height

# Initialize display.
disp.begin()

def display_local_image_file(image_file):
    # Load an image from file.
    print('Loading image: {}...'.format(image_file))
    image = Image.open(image_file)

    # Resize the image
    image = image.resize((WIDTH, HEIGHT))

    # Draw the image on the display hardware.
    print('Drawing image')
    disp.display(image)
    turn_on_display()


def turn_off_display():
    disp.set_backlight(0)
    disp.command(ST7789.ST7789_DISPOFF)


display_off_timer = None


def turn_on_display():
    global display_off_timer
    disp.set_backlight(1)
    disp.command(ST7789.ST7789_DISPON)

    if display_off_timer is not None:
        display_off_timer.cancel()

    # Turn off the display after 5 min
    display_off_timer = threading.Timer(60 * 5, turn_off_display)
    display_off_timer.start()
