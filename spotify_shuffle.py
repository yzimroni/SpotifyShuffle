import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public ' \
        'user-read-recently-played user-top-read'

token = util.prompt_for_user_token("spotify_user", scope)

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


library_songs = get_all_items(lambda o: sp.current_user_saved_tracks(limit=50, offset=o), 50)
