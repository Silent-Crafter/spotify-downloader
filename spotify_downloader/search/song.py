from requests import get
from re import findall
from spotipy import Spotify
from sys import exit

class SongObject:

    def __init__(self, spobj, mode='t'):

        self.mode = mode

        if not spobj:
            raise Exception('No spotipy object created')

        self.spobj: Spotify = spobj

        self.track = None

    def get_tracks(self, url):

        if not findall(r'open.spotify.com/[a-z]*/.{22}', url):
            print('Not a valid spotify song url.. quiting..')
            exit(1)

        if 'track' in url:
            return [self.get_track(url)]
        elif 'playlist' in url:
            return self.get_playlist(url)
        elif 'artist' in url:
            return self.get_artist(url)
        elif 'album' in url:
            return self.get_album(url)
        elif 'show' or 'episode':
            print('Podcast urls aren\'t yet supported.. quiting...')
            exit(1)

    def get_track(self, url):
        return self.spobj.track(url)

    def get_playlist(self, url):
        results = self.spobj.playlist_items(playlist_id=url)

        _tracks = results['items']

        while results['next']:
            results = self.spobj.next(results)
            _tracks.extend(results['items'])

        # for some weird reason, spotify returns some addiotinal information if used the playlist_tracks method
        # whose dictionary structure is different if used Spotify.album_tracks() or Spotify.track() functions.
        # we need the 'track' key to get the actual track information

        tracks = []

        for i in range(len(_tracks)):
            tracks.append(_tracks[0]['track'])
            _tracks.pop(0)

        return tracks

    def get_album(self, url):
        results = self.spobj.album_tracks(album_id=url)

        tracks = results['items']

        while results['next']:
            results = self.spobj.next(results)
            tracks.extend(results['items'])

        return tracks

    def get_artist(self, url) -> list:

        artist_id = 'spotify:artist:' + findall(r'artist/([A-Za-z0-9]*)', url)[0]
        _tracks = []
        tracks = []

        artist_albums = self.spobj.artist_albums(artist_id=artist_id, album_type='single,album,appears_on')

        albums = artist_albums['items']

        while artist_albums['next']:
            artist_albums = self.spobj.next(artist_albums)
            albums.extend(artist_albums['items'])

        for artist_album in albums:
            album = self.spobj.album_tracks(artist_album['uri'])

            _tracks = album['items']

            while album['next']:
                album = self.spobj.next(album)
                _tracks.extend(album['items'])

            for track in _tracks:
                song = self.spobj.track(track['id'])
                # this is because we don't want to download all the songs of an album
                # of which only one or two are of artists
                artist_match = False
                for artist in song['artists']:
                    if artist['uri'] == artist_id:
                        artist_match = True
                        break

                if artist_match:
                    tracks.append(track)

        del _tracks
        return tracks

    @staticmethod
    def create_title(track):
        if len(track['artists']) > 1:
            title = track['name'] + ' - ' + track['artists'][0]['name'] + ', ' + track['artists'][1]['name']
        else:
            title = track['name'] + ' - ' + track['artists'][0]['name']

        for disallowedChar in ['/', '?', '\\', '*', '|', '<', '>', '\"', ':']:
            if disallowedChar in title:
                if '\"' in title:
                    title = title.replace('\"', '\'')
                elif ':' in title:
                    title = title.replace(':', '-')
                else:
                    title = title.replace(disallowedChar, '')

        return title

    def search(self, song: dict) -> str:

        special_chars = {
            '%21': '!',
            '%22': '\"',
            '%23': '#',
            '%24': '$',
            '%25': '%',
            '%26': '&',
            '%27': '\'',
            '%28': '(',
            '%29': ')',
            '%2A': '*',
            '%2B': '+',
            '%2C': ',',
            '%2D': '-',
            '%2E': '.'
        }

        if self.mode == 'n' or self.mode == 'N':
            if (len(song['artists']) > 1):
                query = str(
                        song['name'] + ' ' + song['artists'][0]['name'] + ' ' + song['artists'][1]['name']
                ).replace(' ', '+')

            else:
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name']
                ).replace(' ', '+')

        elif self.mode == 't' or self.mode == 'T':
            if (len(song['artists']) > 1):
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' ' + song['artists'][1]['name'] + ' \"Provided to YouTube\"'
                ).replace(' ', '+')

            else:
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' \"Provided to YouTube\"'
                ).replace(' ', '+')

        elif self.mode == 'a' or self.mode == 'A':
            if (len(song['artists']) > 1):
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' ' + song['artists'][1]['name'] + ' (Official Audio)'
                ).replace(' ', '+')
            else:
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' (Official Audio)'
                ).replace(' ', '+')

        else:
            if (len(song['artists']) > 1):
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' ' + song['artists'][1]['name'] + ' \"Provided to YouTube\"'
                ).replace(' ', '+')
            else:
                query = str(
                    song['name'] + ' ' + song['artists'][0]['name'] + ' \"Provided to YouTube\"'
                ).replace(' ', '+')

        print(f'Search query: {query}', '\n')

        # query = quote(query)

        for special_char in special_chars:
            if special_char in query:
                query = query.replace(special_char, special_chars[special_char])

        # print('converted query: ',query,'\n')

        yt_url = f'https://www.youtube.com/results?search_query={query}'
        yt_song_link = None

        try:
            yt_page = get(yt_url)
            video_ids = findall(r'watch\?v=(\S{11})', yt_page.text)
            yt_song_link = "https://www.youtube.com/watch?v=" + video_ids[0]

        except IndexError:
            print('\nTry with different mode\n')

        except Exception as e:
            print(e)

        return yt_song_link
