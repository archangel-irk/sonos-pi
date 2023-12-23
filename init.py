#!/usr/bin/env python3

import signal
import sonos
import volume_knob
import display


def change_volume(delta):
    display.turn_on_display()
    new_volume = sonos.set_relative_volume(delta)
    print('Volume: ', new_volume)


print('Volume: ', sonos.get_volume())

# here you put your main loop or block of code
volume_knob.listen_volume_change(change_volume)
sonos.display_current_album_art()

signal.pause()
