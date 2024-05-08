#!/usr/bin/env python3
import signal
from queue import Empty
from pprint import pprint

# Import variables which also set current working directory
import variables
import logger

from soco.events import event_listener
import sonos
import volume_knob
import display
import atexit
#atexit.register(display.turn_off_display)

def change_volume(delta):
    display.turn_on_display()
    new_volume = sonos.set_relative_volume(delta)
    #print('Volume: ', new_volume)
    logger.info("Volume: %s", new_volume)


#print('Volume: ', sonos.get_volume())
logger.info("Volume: %s", sonos.get_volume())

# here you put your main loop or block of code
volume_knob.listen_volume_change(change_volume)
sonos.display_current_album_art()

# signal.pause()

# Subscribe to AV events
sub = sonos.device.avTransport.subscribe()

# print out the events as they arise
while True:
    try:
        event = sub.events.get(timeout=0.5)
        # pprint(event.variables)
        if event.variables['transport_state'] == 'PLAYING':
            sonos.display_current_album_art()

    except Empty:
        pass
    except KeyboardInterrupt:
        sub.unsubscribe()
        event_listener.stop()
        break

