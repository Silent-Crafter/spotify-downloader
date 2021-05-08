from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from os import path

from functions import *

auth_manager = SpotifyClientCredentials(client_id='',client_secret='')
sp = Spotify(auth_manager=auth_manager)

url = input('URL: ')
folder = input('Path: ')

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
        if not path.isfile(f'{folder}/{title}.mp3'):
            print('\n-----------------------------------------------------------------------------------------------')
            print('\t\t\t\tSong:',song['name'])
            print('-----------------------------------------------------------------------------------------------\n')
            while True:
                try:
                    link = search(song, 'n')
                    download(folder, title, link)
                    set_meta(sp, song, title, folder)

                except (KeyboardInterrupt, SystemExit):
                    exit()

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
    title = create_title(song)
    mode = input('Select method (n/t/a): ')
    if not path.isfile(f'{folder}/{title}.mp3'):
        print('\n-----------------------------------------------------------------------------------------------')
        print('\t\t\t\tSong:',song['name'])
        print('-----------------------------------------------------------------------------------------------\n')
        try:
            link = search(song, mode)
            download(folder, title, link)
            set_meta(sp, song, title, folder)
        except (KeyboardInterrupt, SystemExit):
            exit()
        except:
            print('FAILED')
        print('\n-----------------------------------------------------------------------------------------------')
    else:
        print(f'{title} Already Downloaded')

else:
    print('given url is not of a song on spotify')