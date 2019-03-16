import sys
import spotipy
import spotipy.util as util
import random
import os
import datetime

scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public ' \
        'user-read-recently-played user-top-read'

token = util.prompt_for_user_token("spotify_user", scope)

PLAYLIST_SIZE = 100

if not token:
    sys.exit()

sp = spotipy.Spotify(auth=token)


def get_all_items(source, per_page):
    items = []
    offset = 0
    while True:
        result = source(offset)
        if result and "items" in result:
            items.extend(result["items"])
        if offset >= result["total"]:
            break
        offset += per_page
    return {"items": items}


def run():
    print("Running SpotifyShuffle")
    user_id = sp.me()["id"]
    playlist_id = os.getenv('SHUFFLE_PLAYLIST_ID')
    print("Spotify user ID: %s" % user_id)
    print("Spotify playlist ID: %s" % playlist_id)

    print("Loading library")
    library_songs = get_all_items(lambda o: sp.current_user_saved_tracks(limit=50, offset=o), 50)["items"]
    print("Library loaded, %s songs found" % len(library_songs))
    random.shuffle(library_songs)
    track_ids = [s["track"]["id"] for s in library_songs[:PLAYLIST_SIZE]]

    sp.user_playlist_replace_tracks(user_id, playlist_id, track_ids)
    sp.user_playlist_change_details(user_id, sp._get_id("playlist", playlist_id), description="""Automatically shuffled by SpotifyShuffle
Last shuffle date: %s
Playlist size: %s (%s)""" % (datetime.date.today().strftime("%H:%M:%S %d.%m.%Y"), len(track_ids), PLAYLIST_SIZE))
    print("Updated playlist id %s with %s randomized songs" % (playlist_id, len(track_ids)))


if __name__ == "__main__":
    run()
