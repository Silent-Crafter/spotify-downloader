from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from os import path

from functions import *

auth_manager = SpotifyClientCredentials(client_id='276dee1768a642e0ae15f34fc7fe6251',client_secret='f234a63aa0654f2b8304efe46275d6b1')
sp = Spotify(auth_manager=auth_manager)

url = input('URL: ')

maxRetry = 3

failed = []

if 'open.spotify.com/playlist' in url:
    results = sp.playlist_tracks(playlist_id=url)

    urls = []

    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:                                #TAKES A HELL LOT OF TIME
        song = sp.track(track['track']['id'])
        title = create_title(song)
        if not path.isfile(f'../{title}.mp3'):
            print('\n-----------------------------------------------------------------------------------------------')
            print('\t\t\t\tSong:',song['name'])
            print('-----------------------------------------------------------------------------------------------\n')
            while True:
                try:
                    link = search(song, 'n')
                    download(title, link)
                    set_meta(sp, song, title)
                except:
                    if maxRetry < 1:
                        print('Retry limit reached. Breaking out of loop....')
                        failed.append(song['name'])
                        break
                    else:
                        print('\nConnection Timed out. Trying again...\n')
                        maxRetry -= 1
                        continue
                break
            print('\n-----------------------------------------------------------------------------------------------')
        else:
            print(title)

    print('songs downloaded')
    print('failed:',failed)

elif 'open.spotify.com/track' in url:
    song = sp.track(url)
    mode = input('Select method (n/t/a): ')
    print('\n-----------------------------------------------------------------------------------------------')
    print('\t\t\t\tSong:',song['name'])
    print('-----------------------------------------------------------------------------------------------\n')
    try:
        title,link = search(song, mode)
        download(title, link)
        set_meta(sp, song, title)
    except:
        failed.append(song['name'])
        print('FAILED')
    print('\n-----------------------------------------------------------------------------------------------')

else:
    print('given url is not of a song on spotify')