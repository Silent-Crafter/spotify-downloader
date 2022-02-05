#!/usr/bin/python3
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from os import path
from sys import argv,exit

from spotify_downloader.search.song import SongObject
from spotify_downloader.download.downloader import download
from spotify_downloader.download.embed_meta import set_meta


def console():
    auth_manager = SpotifyClientCredentials(client_id='276dee1768a642e0ae15f34fc7fe6251',
                                            client_secret='f234a63aa0654f2b8304efe46275d6b1')
    sp = Spotify(auth_manager=auth_manager)

    if len(argv) > 1:
        url = argv[1]
    else:
        url = input('URL: ')

    folder = input('Path: ').strip()
    mode = input('mode(T/n/a): ').strip()
    
    if not folder:
        folder = '.'

    songobj = SongObject(sp, mode)

    try:
        tracks = songobj.get_tracks(url)
    # every exception sir? EVERYONE
    except Exception:
        print('\nError 404: Not Found')
        exit(1)

    failed = []
    max_retry = 3

    for track in tracks:
        try:
            song = songobj.get_track(track["external_urls"]["spotify"])
        except TypeError:
            continue

        title = songobj.create_title(track)
        if not path.isfile(f'{folder}/{title}.mp3'):
            print('\n-----------------------------------------------------------------------------------------------')
            print('\t\t\t\tSong:', song['name'])
            print('-----------------------------------------------------------------------------------------------\n')
            while True:
                try:
                    link = songobj.search(song)
                    download(folder, title, link)
                    set_meta(sp, song, title, folder)

                except (KeyboardInterrupt, SystemExit):
                    exit()

                except Exception as e:
                    if max_retry < 1:
                        print('Retry limit reached. Breaking out of loop....')
                        failed.append(song['name']+': '+song['external_urls']['spotify'])
                        break
                    else:
                        print(e)
                        max_retry -= 1
                        continue
                break
            print('\n-----------------------------------------------------------------------------------------------')
        else:
            print(f'{title} Already Downloaded')

    print('songs downloaded')
    if failed:
        print('failed = [')
        for failure in failed:
            print('\t'+failure)
        print(']')
