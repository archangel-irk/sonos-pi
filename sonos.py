#!/usr/bin/env python3

import signal
#import RPi.GPIO as GPIO
import soco
import album_art

# Set up RPi.GPIO with the "BCM" numbering scheme
#GPIO.setmode(GPIO.BCM)

# print(device.set_relative_volume(-5))
# print(device.get_current_track_info())

device = soco.discovery.by_name("Sonos TV")

print(device.get_current_track_info()['album_art'])

album_art.display_current_playing_art(device)

# Examples of art URLs through sonos
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3VpxEo6vMpi4rQ6t2WVVkK%3fsid%3d9%26flags%3d8232%26sn%3d1
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3DjBDQs8ebkxMBo2V8V3SH%3fsid%3d9%26flags%3d32

# print(device.get_current_transport_info())

# Decrease volume by
#device.set_relative_volume(-3)
# Increase volume by
#device.set_relative_volume(3)
# Play / Pause button
#playback = device.get_current_transport_info()
#playback_state = playback.get('current_transport_state')
#if playback_state == 'PAUSED_PLAYBACK':
#    device.play()
#elif playback_state == 'PLAYING':
#    device.pause()
