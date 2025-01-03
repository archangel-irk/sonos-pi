#!/usr/bin/env python3
import signal
import colorsys
import time
import RPi.GPIO as GPIO
import ioexpander as io
import atexit
atexit.register(GPIO.cleanup)

# https://github.com/pimoroni/ioe-python/blob/master/examples/rotary.py

# print("""rotary.py
#
# Change the I2C_ADDR to:
#  - 0x0F to use with the Rotary Encoder breakout.
#  - 0x18 to use with IO Expander.
#
# Press Ctrl+C to exit.
#
# """)

I2C_ADDR = 0x0F  # 0x18 for IO Expander, 0x0F for the encoder breakout

PIN_RED = 1
PIN_GREEN = 7
PIN_BLUE = 2

POT_ENC_A = 12
POT_ENC_B = 3
POT_ENC_C = 11

BRIGHTNESS = 1                  # Effectively the maximum fraction of the period that the LED will be on
PERIOD = int(255 / BRIGHTNESS)  # Add a period large enough to get 0-255 steps at the desired brightness

ioe = io.IOE(i2c_addr=I2C_ADDR, interrupt_pin=4)

# Swap the interrupt pin for the Rotary Encoder breakout
if I2C_ADDR == 0x0F:
    ioe.enable_interrupt_out(pin_swap=True)

ioe.setup_rotary_encoder(1, POT_ENC_A, POT_ENC_B, pin_c=POT_ENC_C)

ioe.set_pwm_period(PERIOD)
ioe.set_pwm_control(divider=2)  # PWM as fast as we can to avoid LED flicker

ioe.set_mode(PIN_RED, io.PWM, invert=True)
ioe.set_mode(PIN_GREEN, io.PWM, invert=True)
ioe.set_mode(PIN_BLUE, io.PWM, invert=True)

print("Running LED with {} brightness steps.".format(int(PERIOD * BRIGHTNESS)))

count = 0
r, g, b, = 0, 0, 0

# while True:
#     if ioe.get_interrupt():
#         count = ioe.read_rotary_encoder(1)
#         ioe.clear_interrupt()
#
#     h = (count % 360) / 360.0
#     r, g, b = [int(c * PERIOD * BRIGHTNESS) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
#     ioe.output(PIN_RED, r)
#     ioe.output(PIN_GREEN, g)
#     ioe.output(PIN_BLUE, b)
#
#     print(count, r, g, b)
#
#     time.sleep(1.0 / 30)


def volume_changed(channel, callback=None):
    global count, r, g, b

    delta = ioe.read_rotary_encoder(1)
    ioe.clear_interrupt()
    ioe.clear_rotary_encoder(1)

    if callback is not None:
        callback(delta)

    count += delta

    # was 360
    h = (count % 50) / 50.0
    r, g, b = [int(c * PERIOD * BRIGHTNESS) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    ioe.output(PIN_RED, r)
    ioe.output(PIN_GREEN, g)
    ioe.output(PIN_BLUE, b)

    # print(delta, r, g, b)


def listen_volume_change(callback=None):
    # Clear before listen to interrupt.
    # Seems like "RGB Encoder Breakout" stores the interrupt flag in some of "Nuvoton microcontroller" registers.
    # Probably sometimes when program exits the interrupt flag is not cleared.
    # Then when new program starts it will not get new interrupts because the flag is not changing, it's already set and
    # was not cleared.
    # Fixes "Stop reacting on volume change".
    ioe.clear_interrupt()
    ioe.clear_rotary_encoder(1)

    ioe.on_interrupt(lambda channel: volume_changed(channel, callback))
    # ioe._gpio.add_event_detect(self._interrupt_pin, self._gpio.FALLING, callback=callback, bouncetime=1)
    print("Init volume knob")


if __name__ == '__main__':
    listen_volume_change()
    signal.pause()
