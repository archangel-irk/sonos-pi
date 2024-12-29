#!/usr/bin/env python3
import os
import urllib.request
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import unquote
from pprint import pprint
import soco
import display

# print(device.set_relative_volume(-5))
# print(device.get_current_track_info())

device = soco.discovery.by_name("Sonos TV")
last_album_art_url = None
cached_volume = None
last_evented_volume = None
ignore_volume_events = False

# album_art.display_current_playing_art(device)

# url can be:
# 1. If a song played from spotify app the url will be like
#    https://i.scdn.co/image/ab67616d0000b2731d31a4969ceaaaa91c52e025
# 2. If a song played from sonos app the url will be like
#    http://10.0.1.9:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a2GR2ljPQLtDfQsYd14Uxrm%3fsid%3d9%26flags%3d8232%26sn%3d1

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


def subscribe_volume():
    return device.renderingControl.subscribe(auto_renew=True)


def subscribe_current_track():
    # Subscribe to AV events
    # http://docs.python-soco.com/en/latest/api/soco.events.html
    return device.avTransport.subscribe(auto_renew=True)


def get_volume():
    return device.volume


def set_relative_volume(delta):
    global cached_volume
    # Unmute the device first.
    # The device can be playing the music but being muted
    # changing the volume doesn't unmute the device,
    # so we need to do it manually.
    device.mute = False
    new_volume = device.set_relative_volume(delta)
    cached_volume = new_volume


def display_current_album_art():
    global last_album_art_url
    # Get Art URL from device current track playing.
    track_info = device.get_current_track_info()
    url = track_info['album_art']
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

    filename = get_track_filename(url)
    # Construct a file path
    filepath = COVERS_DIR + filename

    print("filepath: ", filepath)

    # Download the image
    urllib.request.urlretrieve(url, filepath)
    return filepath


def get_track_filename(url):
    # process sonos type url
    # http://10.0.1.9:1400/getaa?s=1&u=x-sonos-spotify%3aspotify%253atrack%253a2GR2ljPQLtDfQsYd14Uxrm%3fsid%3d9%26flags%3d8232%26sn%3d1
    if 'x-sonos-spotify' in url:
        parsed_url = urlparse(url)
        # https://github.com/jishi/node-sonos-http-api/blob/1fa4cdc998d6cf7b0448a2c622b51d352dd05a0b/lib/actions/spotify.js#L20
        # sonos uri looks like "x-sonos-spotify:${encodedSpotifyUri}?sid=${sid}&flags=32&sn=1"
        sonos_uri = parse_qs(parsed_url.query)['u'][0]
        # take the encodedSpotifyUri part from sonos uri
        spotify_uri_encoded = sonos_uri.removeprefix('x-sonos-spotify:').split('?')[0]
        # https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids
        # get "spotify:track:4YxrU1KNuhskMAQztkACrA"
        spotify_uri = unquote(spotify_uri_encoded)
        # The base-62 identifier found at the end of the Spotify URI (see above) for an artist, track, album, playlist, etc.
        spotify_id = spotify_uri.split(':')[2]
        filehash = spotify_id

    else:
        # url example: https://i.scdn.co/image/ab67616d0000b2731d31a4969ceaaaa91c52e025
        # Get the last "hash" as a name
        filehash = url.split('/')[-1]

    return filehash + ".jpg"
