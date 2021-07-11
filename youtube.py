import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl
import os


class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track


class YouTubeClient(object):
    def __init__(self, credentials_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
        self.YouTubeClient = youtube

    
    def get_playlist(self):
        request = youtube.playlists().list(part="id, snippet", maxResults=10, mine=True)
        response = request.execute()

        return [Playlist(item['id'], item['snippet']['title']) for item in response['items']]


    def get_vid_from_playlist(self, playlist_id):
        songs = []
        request = youtube.playlistItems().list(playlist_id = playlist_id, part = "id, snippet")
        response = request.execute()

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            artist, track = self.get_title(video_id)

            if(artist and track):
                songs.append(Song(artist, track))

        return songs

    def get_title(self, video_id):
        youtube_url = "https://www.youtube.com/watch?v=" + video_id

        video = youtube_dl.YoutubeDL({'quiet':True}).extract_info(youtube_url, download = False)

        artist = video['artist']
        track = video['track']

        return artist, track
