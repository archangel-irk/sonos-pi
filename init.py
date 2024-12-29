#!/usr/bin/env python3
import signal
from queue import Empty
from pprint import pprint
import os
import threading
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
print("Volume: ", sonos.get_volume())

volume_events_timer = None


# https://docs.sonos.com/docs/volume
def knob_volume_handler(delta):
    global volume_events_timer
    sonos.set_relative_volume(delta)
    display.display_volume(sonos.cached_volume)

    sonos.ignore_volume_events = True
    if volume_events_timer is not None:
        volume_events_timer.cancel()

    def resume_event_handling():
        sonos.ignore_volume_events = False

    # event volume changes can be slow, keep ignoring events for two more seconds
    volume_events_timer = threading.Timer(2, resume_event_handling)
    volume_events_timer.start()


def event_volume_handler(new_volume):
    sonos.cached_volume = new_volume
    display.display_volume(sonos.cached_volume)


volume_knob.listen_volume_change(knob_volume_handler)
sonos.display_current_album_art()

# signal.pause()

# Subscribe to sonos events
renderingControl = sonos.subscribe_volume()
avTransport = sonos.subscribe_current_track()


# print out the events as they arise
while True:
    try:
        event = renderingControl.events.get(timeout=0.5)
        # pprint(event.variables)
        if 'volume' in event.variables:
            sonos.last_evented_volume = event.variables['volume']['Master']
            if not sonos.ignore_volume_events:
                event_volume_handler(event.variables['volume']['Master'])
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

