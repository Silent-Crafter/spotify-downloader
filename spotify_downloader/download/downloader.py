from yt_dlp import YoutubeDL
import os


def download(folder, title, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': '{}/{}.%(ext)s'.format(folder, title)
    }

    print('Output file:', ydl_opts['outtmpl'])

    with YoutubeDL(ydl_opts) as ydl:

        if not os.path.isfile(f'{folder}/{title}.mp3'):
            ydl.download([url])

        else:
            print('File already exists not downloading')
