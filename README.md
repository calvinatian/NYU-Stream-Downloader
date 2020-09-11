# NYU Stream Downloader

This is a fork of [UBC Kultura Downloader](https://github.com/DonneyF/ubc-kaltura-video-downloader) modified to work with NYU Stream. Some functionality has been changed or added.

This script is used to download videos from [NYU Stream](https://stream.nyu.edu). You must first login to NYU Stream using the default authentication on NYU.

## Requirements
* Python 3
  * requests module
* Web browser

Install the `requests` module with pip as shown:

Windows
```python
pip install requests
```
Mac/Linux
```python
pip3 install requests
```

## Usage
### Getting the correct URL
First, the correct URL must be copied. Steps to copy the correct URL can be seen below. The URL should follow the format of this [example URL](https://cfvod.kaltura.com/scf/hls/p/1674401/sp/167440100/serveFlavor/entryId/1_sgq36ht8/v/1/flavorId/1_9r05c6s9/name/a.mp4/seg-1-v1-a1.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTY3NDQwMS9zcC8xNjc0NDAxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8xX3NncTM2aHQ4L3YvMS9mbGF2b3JJZC8xXzlyMDVjNnM5L25hbWUvYS5tcDQvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU5OTkxNjU0M319fV19&Signature=Wjq~Q3GwS8OtebeuWmxslRlHVPwtbwCVjXn0NaQy80s1OzY0O98-Rona2F6-g2RNY6Ewz9U8zfN04~l-QfpmqZhe1g3ocd-wvmEXjUvK~jhQ7juMqaIm1bJPccQiuqEfWXh4OKqX7RdaBvr8zhoWQ0mznw8QnwpVTORZZJwIFd~prlyQooLnxAOCKJJQGnGvABSkusOiEvMnah4q3znilJKkN-XVrw~pl3la0iy6Bagu-yv56HWDW88ri6nFy9fKt4I62O2-eGoGxeLoGvsezSynJwG4W93Nxm15gFF0ehfUzk~N6ROC4oCXYv7yjsUJvuJ-xmI2b4r5Jx0tjQUsfA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A).

<details>
<summary>
Firefox Instructions
</summary>

1. Open the Firefox menu and click on "Web Developer"<br> <img src="documentation/images/firefox/1%20firefox_menu.png" alt="firefox menu" height="400"> 
2. Click the "Network" button<br> <img src="documentation/images/firefox/2%20firefox_network.png" alt="network button in firefox menu" height="400"> 
3. Open the video on NYU stream<br> <img src="documentation/images/firefox/3%20video_page.png" alt="NYU Stream video page" height="200">
4. Click the media tab filter<br> <img src="documentation/images/firefox/4%20network_tab.png" alt="network tab" height="400">
5. Click the link with `seg` in the name, the type should be `mp2t`. You may need to start the video playback for results to show up in the network tab.<br><img src="documentation/images/firefox/5%20click_seg.png" alt="clicking segment" height="400">
6. Finally, copy the link as shown<br> <img src="documentation/images/firefox/6%20copy_url.png" alt="copy link" height="400">
</details>

### Script Usage
```
python downloader.py [-h] [-f file name] [-d download directory] [-a | -v] "URL"

Download videos from NYU Stream

positional arguments:
  URL                   See README for help on GitHub for help getting the correct URL

optional arguments:
  -h, --help             show this help message and exit
  -f file name           output file name
  -d download directory  directory to download files to
  -a, --audio-only       download audio only
  -v, --video-only       download video only
```
* The URL should be surrounded in quotes.
* If a download directory is not specified the default download directory is a folder called `NYU-Stream/output` under the user's download folder.
  * The default filename is `output.mp4` or `output.m4a` depending on if its a video or audio only.
    * The file extension `mp4` or `m4a` will be automatically added
  * By default the file downloaded will contain both audio and video. Use the `-a` or `-v` options if you only want the video or audio

#### Example usage
```python
python downloader.py -f FileName "https://cfvod.kaltura.com/scf/hls/p/1674401/sp/167440100/serveFlavor/entryId/1_sgq36ht8/v/1/flavorId/1_9r05c6s9/name/a.mp4/seg-1-v1-a1.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTY3NDQwMS9zcC8xNjc0NDAxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8xX3NncTM2aHQ4L3YvMS9mbGF2b3JJZC8xXzlyMDVjNnM5L25hbWUvYS5tcDQvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTU5OTkxNjU0M319fV19&Signature=Wjq~Q3GwS8OtebeuWmxslRlHVPwtbwCVjXn0NaQy80s1OzY0O98-Rona2F6-g2RNY6Ewz9U8zfN04~l-QfpmqZhe1g3ocd-wvmEXjUvK~jhQ7juMqaIm1bJPccQiuqEfWXh4OKqX7RdaBvr8zhoWQ0mznw8QnwpVTORZZJwIFd~prlyQooLnxAOCKJJQGnGvABSkusOiEvMnah4q3znilJKkN-XVrw~pl3la0iy6Bagu-yv56HWDW88ri6nFy9fKt4I62O2-eGoGxeLoGvsezSynJwG4W93Nxm15gFF0ehfUzk~N6ROC4oCXYv7yjsUJvuJ-xmI2b4r5Jx0tjQUsfA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"
```

## Legal Notice
Videos may be copyrighted by the uploader. Do not redistribute video/audio without permission.
