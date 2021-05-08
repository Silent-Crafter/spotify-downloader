import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print('Checking Modules..')

modules = ['spotipy', 'bs4', 'requests', 'requests_html', 'youtube_dl', 'urllib', 'mutagen', 'pyppeteer']

for module in modules:
    try:
        __import__(module)
    except:
        install(module)