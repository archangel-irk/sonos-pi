#!/usr/bin/env python3
import os
import urllib.request
import soco
import display

# print(device.set_relative_volume(-5))
# print(device.get_current_track_info())

device = soco.discovery.by_name("Sonos TV")
last_album_art_url = None

# album_art.display_current_playing_art(device)

# Examples of art URLs through sonos
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3VpxEo6vMpi4rQ6t2WVVkK%3fsid%3d9%26flags%3d8232%26sn%3d1
# http://10.0.1.4:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a3DjBDQs8ebkxMBo2V8V3SH%3fsid%3d9%26flags%3d32

# print(device.get_current_transport_info())
# print('Volume: ', device.volume)

# Decrease volume by
# device.set_relative_volume(-3)
# Increase volume by
# device.set_relative_volume(3)

# Play / Pause button
# playback = device.get_current_transport_info()
# playback_state = playback.get('current_transport_state')
# if playback_state == 'PAUSED_PLAYBACK':
#    device.play()
# elif playback_state == 'PLAYING':
#    device.pause()
# print(device.get_current_track_info())


def subscribe():
    # Subscribe to AV events
    # http://docs.python-soco.com/en/latest/api/soco.events.html
    return [
        device.renderingControl.subscribe(auto_renew=True),
        device.avTransport.subscribe(auto_renew=True)
    ]


def get_volume():
    return device.volume


def set_relative_volume(delta):
    # Unmute the device first.
    # The device can be playing the music but being muted
    # changing the volume doesn't unmute the device,
    # so we need to do it manually.
    device.mute = False
    new_volume = device.set_relative_volume(delta)
    return new_volume


def display_current_album_art():
    global last_album_art_url
    # Get Art URL from SONOS current track playing.
    # example: https://i.scdn.co/image/ab67616d0000b2731d31a4969ceaaaa91c52e025
    url = device.get_current_track_info()['album_art']
    if url == '' or url == last_album_art_url:
        return
    print("COVER_URL: ", url)
    filepath = download_art(url)
    display.display_local_image_file(filepath)
    last_album_art_url = url


COVERS_DIR = "/tmp/sonosd/covers/"

def download_art(url):
    # Make sure the temp covers folder exists. Create if doesn't exist.
    os.makedirs(COVERS_DIR, exist_ok=True)

    # url example: https://i.scdn.co/image/ab67616d0000b2731d31a4969ceaaaa91c52e025
    # Get the last "hash" as a name
    filehash = url.split('/')[-1]
    filename = filehash + ".jpg"
    # Construct a file path
    filepath = COVERS_DIR + filename

    print("filepath: ", filepath)

    # Download the image
    urllib.request.urlretrieve(url, filepath)
    return filepath
