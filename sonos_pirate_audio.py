#!/usr/bin/env python3

import signal
import RPi.GPIO as GPIO
import soco
import album_art

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# print(device.set_relative_volume(-5))
# print(device.get_current_track_info())

device = soco.discovery.by_name("Sonos TV")

print(device.get_current_track_info()['album_art'])

album_art.display_current_playing_art(device)

# Examples of art URLs through sonos
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3VpxEo6vMpi4rQ6t2WVVkK%3fsid%3d9%26flags%3d8232%26sn%3d1
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3DjBDQs8ebkxMBo2V8V3SH%3fsid%3d9%26flags%3d32

# print(device.get_current_transport_info())

print("""buttons.py - Detect which button has been pressed

This example should demonstrate how to:
1. set up RPi.GPIO to read buttons,
2. determine which button has been pressed

Press Ctrl+C to exit!

""")

# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
# Boards prior to 23 January 2020 used 5, 6, 16 and 20 
# try changing 24 to 20 if your Y button doesn't work.
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, X and Y respectively
LABELS = ['A', 'B', 'X', 'Y']

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if label == 'B':
        # Decrease volume by
        device.set_relative_volume(-3)
    elif label == 'Y':
        # Increase volume by
        device.set_relative_volume(3)
    elif label == 'A':
        # Play / Pause button
        playback = device.get_current_transport_info()
        playback_state = playback.get('current_transport_state')
        if playback_state == 'PAUSED_PLAYBACK':
            device.play()
        elif playback_state == 'PLAYING':
            device.pause()


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 100ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()
