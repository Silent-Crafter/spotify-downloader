from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from os import path

from functions import *

auth_manager = SpotifyClientCredentials(client_id='276dee1768a642e0ae15f34fc7fe6251',client_secret='f234a63aa0654f2b8304efe46275d6b1')
sp = Spotify(auth_manager=auth_manager)

url = input('URL: ')
folder = input('Path: ')

maxRetry = 3

failed = []

if 'open.spotify.com/playlist' in url:
    results = sp.playlist_tracks(playlist_id=url)

    urls = []

    tracks = results['items']
    
    mode = input('Select method (n/T/a): ')

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    for track in tracks:
        song = sp.track(track['track']['id'])
        title = create_title(song)
        if not path.isfile(f'{folder}/{title}.mp3'):
            print('\n-----------------------------------------------------------------------------------------------')
            print('\t\t\t\tSong:',song['name'])
            print('-----------------------------------------------------------------------------------------------\n')
            while True:
                try:
                    link = search(song, mode.strip())
                    download(folder, title, link)
                    set_meta(sp, song, title, folder)

                except (KeyboardInterrupt, SystemExit):
                    exit()

                except Exception as e:
                    if maxRetry < 1:
                        print('Retry limit reached. Breaking out of loop....')
                        failed.append(song['name'])
                        break
                    else:
                        print(e)
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
    mode = input('Select method (n/T/a): ')
    if not path.isfile(f'{folder}/{title}.mp3'):
        print('\n-----------------------------------------------------------------------------------------------')
        print('\t\t\t\tSong:',song['name'])
        print('-----------------------------------------------------------------------------------------------\n')
        try:
            link = search(song, mode.strip())
            download(folder, title, link)
            set_meta(sp, song, title, folder)

        except (KeyboardInterrupt, SystemExit):
            exit()

        except:
            print('FAILED')
        print('\n-----------------------------------------------------------------------------------------------')
    else:
        print(f'{title} Already Downloaded')

elif 'open.spotify.com/album' in url:
    album = sp.album_tracks(url)

    tracks = album['items']
    
    mode = input('Select method (n/T/a): ')

    while album['next']:
        album = sp.next(album)
        tracks.extend(album['items'])

    for track in tracks:
        song = sp.track(track['id'])
        title = create_title(song)
        if not path.isfile(f'{folder}/{title}.mp3'):
            print('\n-----------------------------------------------------------------------------------------------')
            print('\t\t\t\tSong:',song['name'])
            print('-----------------------------------------------------------------------------------------------\n')
            while True:
                try:
                    link = search(song, mode.strip())
                    download(folder, title, link)
                    set_meta(sp, song, title, folder)

                except (KeyboardInterrupt, SystemExit):
                    exit()

                except Exception as e:
                    if maxRetry < 1:
                        print('Retry limit reached. Breaking out of loop....')
                        failed.append(song['name'])
                        break
                    else:
                        print(e)
                        maxRetry -= 1
                        continue
                break
            print('\n-----------------------------------------------------------------------------------------------')
        else:
            print(title)

    print('songs downloaded')
    print('failed:',failed)

else:
    print('Given url is not of a song or playlist on spotify')
