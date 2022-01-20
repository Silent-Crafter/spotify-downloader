from sys import exc_info
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC
from mutagen.id3 import ID3
from requests import get


def set_meta(sp, song, filename, folder):

    exit_flag = False

    for disallowedChar in ['/', '?', '\\', '*', '|', '<', '>', '\"', ':']:
        if disallowedChar in filename:
            if '\"' in filename:
                filename = filename.replace('\"', '\'')
            elif ':' in filename:
                filename = filename.replace(':', '-')
            else:
                filename = filename.replace(disallowedChar, '')

    file = f'{folder}/{filename}.mp3'
    print('\nFilename:', filename)
    print('File exists:', os.path.isfile(file))

    max_retry = 3

    while True:
        try:
            print('\nGetting metadata.....')
            primary_artist_id = song['artists'][0]['id']
            raw_artist_meta = sp.artist(primary_artist_id)

            album_id = song['album']['id']
            raw_album_meta = sp.album(album_id)

            song_name = song['name']

            album_name = song['album']['name']

            contributing_artists = []
            for artist in song['artists']:
                contributing_artists.append(artist['name'])

            track_number = song['track_number']

            genre = raw_album_meta['genres'] + raw_artist_meta['genres']

            print('embedding meta')
            # embed song details
            # we save tags as both ID3 v2.3 and v2.4
            # The simple ID3 tags
            try:
                audio_file = EasyID3(file)

            except Exception:
                audio_file = EasyID3()

            # song name
            audio_file['title'] = song_name
            audio_file['titlesort'] = song_name

            # track number
            audio_file['tracknumber'] = str(track_number)

            # disc number
            audio_file['discnumber'] = str(song['disc_number'])

            # genres (pretty pointless if you ask me)
            # we only apply the first available genre as ID3 v2.3 doesn't support multiple
            # genres and ~80% of the world PC's run Windows - an OS with no ID3 v2.4 support
            genres = genre
            if len(genres) > 0:
                audio_file['genre'] = genres[0]

            # all involved artists
            audio_file['artist'] = contributing_artists

            # album name
            audio_file['album'] = album_name

            # album artist (all of 'em)
            album_artists = []

            for artist in song['album']['artists']:
                album_artists.append(artist['name'])

            audio_file['albumartist'] = album_artists

            # album release date (to what ever precision available)
            audio_file['date'] = song['album']['release_date']
            audio_file['originaldate'] = song['album']['release_date']

            # save as both ID3 v2.3 & v2.4 as v2.3 isn't fully features and
            # windows doesn't support v2.4 until later versions of Win10
            audio_file.save(file, v2_version=3)

            # setting the album art
            audio_file = ID3(file)
            raw_album_art = get(song['album']['images'][0]['url']).content
            audio_file['APIC'] = APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=raw_album_art
            )

            audio_file.save(v2_version=3)

        except KeyboardInterrupt:
            print('quiting...')
            exit_flag = True
            raise Exception

        except Exception:
            if exit_flag:
                exit()
            elif max_retry < 1:
                print('Retry limit reached. Breaking out of loop....')
                print(exc_info())
                break
            else:
                print('\nAn error occurred. Trying again...\n')
                max_retry -= 1
                continue

        break

    print('done')
