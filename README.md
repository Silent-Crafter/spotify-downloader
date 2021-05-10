# spotify downloader
 downloads songs from spotify through youtube along with adding meta

## Setup
Run the setup.py to install missing modules. After running main.py the program will install a chromium package if not present. it will do this only once. it won't downloader later when you run it. It is required by the requests_html package to simulate a html session, in simpler words, to browse the internet.

## Usage
run the main.py file
input the asked values
for path, specify the path for the directory in this fashion:

``` C:\Music\Spotify```
<br> OR
<br> ``` /home/Music ``` (for linux) (DONT USE ~ TO INDICATE HOME DIR)

NOTE : Do not add a slash at the end of the directory as shown in the example

### modes
the program will ask you for mode/method.

n : normal mode/method. searches song normally. <br>
t : topic mode/method. adds -Topic in the end. Very usefull to get plain audio tracks if there is unwanted audio from the music video or anothe random meme video. <br>
a : audio mode/method. add (Official Audio) to further enhance the search term for youtube. server the same purpose as t mode. <br>

For playlist the default mode will be 'n'. The program won't ask you.
Recommended is the normal mode. it works for must of the time. but in case if it dosen't use t or a. 

covers are less likely to get fetched for youtube reasons.
