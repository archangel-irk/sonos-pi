#!/usr/bin/env python3
import signal
from queue import Empty
from pprint import pprint
import os
from soco.events import event_listener
import sonos
import volume_knob
import display
import atexit
#atexit.register(display.turn_off_display)

# NOTE! Do not rely on the working directory.
# systemd sets "/" root folder as cwd for the process.
# Using absolute path fixes permission denied problem when running in systemd.
# /home/konstantin/sonos-pi/covers/
# WORKING_DIR = os.path.dirname(os.path.realpath(__file__)) + "/"

print('------------START SONOSC------------')
print('cwd: ', os.getcwd())


def change_volume_handler(delta):
    display.turn_on_display()
    new_volume = sonos.set_relative_volume(delta)
    print("Volume: ", new_volume)


print("Volume: ", sonos.get_volume())

# here you put your main loop or block of code
volume_knob.listen_volume_change(change_volume_handler)
sonos.display_current_album_art()

# signal.pause()

# Subscribe to sonos events
renderingControl, avTransport = sonos.subscribe()

# print out the events as they arise
while True:
    try:
        event = renderingControl.events.get(timeout=0.5)
        # pprint(event.variables)
        if 'volume' in event.variables:
            print(event.variables['volume']['Master'])
    except Empty:
        pass

    try:
        event = avTransport.events.get(timeout=0.5)
        # pprint(event.variables)
        if 'transport_state' in event.variables:
            if event.variables['transport_state'] == 'PLAYING':
                sonos.display_current_album_art()
    except Empty:
        pass

    except KeyboardInterrupt:
        renderingControl.unsubscribe()
        avTransport.unsubscribe()
        event_listener.stop()
        break

