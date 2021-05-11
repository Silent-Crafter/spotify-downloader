import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package,'--upgrade'])

print('Checking Modules..')

modules = ['spotipy', 're', 'youtube_dl', 'urllib', 'mutagen']

for module in modules:
    try:
        __import__(module)
    except:
        install(module)
