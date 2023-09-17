import os
import urllib.request
import soco
import display

def display_current_playing_art(device):
    filepath = download_current_playing_art(device)
    display.display_local_image_file(filepath)


def download_current_playing_art(device):
    # Get Art URL from SONOS current track playing.
    # example: https://i.scdn.co/image/ab67616d0000b2731d31a4969ceaaaa91c52e025
    url = device.get_current_track_info()['album_art']
    # Get the last "hash" as a name
    filehash = url.split('/')[-1]
    filename = filehash + ".jpg"
    # Construct a file path
    filepath = "./covers/" + filename
    # Make sure the "./covers/" folder exists. Create if doesn't exist.
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    # Download the image
    urllib.request.urlretrieve(url, filepath)
    return filepath