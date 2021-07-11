import requests
import urllib.parse

class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist}{track}')
        url = "https://api.spotify.com/v1/search?q=" + query + "&type=track"
        response = requests.get(url,headers={"Content-type": "applicatoin/json", "Authorization": f"Bearer {self.api_token}"})
        results = response.json()['tracks']['items']

        if results:
            return results[0]['id']
        else:
            raise Exception("Nothing found", artist, "-", track)

    def add_song_to_library(self, song_id):
        url = "https:api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={"id": [song_id]},
            headers={"Content-type": "applicatoin/json","Authorization": f"Bearer {self.api_token}"}
        )

        return response.ok