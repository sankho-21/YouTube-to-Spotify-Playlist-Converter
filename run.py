from youtube import YouTubeClient
from spotify import SpotifyClient
import os

def run():
    youtube_client = YouTubeClient('JSON FILE ADDRESS')
    spotify_client = SpotifyClient(os.getenv('SPOTIFY OATH TOKEN'))
    playlists = youtube_client.get_playlist()
    print(playlists)

    for index, playlist in enumerate(playlists):
        print(index, ":" , playlist.title)
    
    choice = int(input("Enter your playlist number: "))

    chosen_playlist = playlists[choice]

    print("Your Selected playlist:", chosen_playlist.title)

    songs = youtube_client.get_vid_from_playlist(chosen_playlist.id)
    print("Attempting to add", len(songs))

    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_song_to_library(spotify_song_id)
            if added_song:
                print("Added", added_song, "to your library")


run()