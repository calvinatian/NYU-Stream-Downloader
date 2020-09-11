import json
import os
import shutil
import argparse
import re
import requests
from tqdm import tqdm
from pathlib import Path

def main(url, file_name, audio_only, video_only, download_directory):
    # Download all the available segments from the url.
    # Append /seg-x-v1-a1.ts, check for successful response, and save the file

    if download_directory != None:
        print("download directory provided")
        print(download_directory)
        download_dir = f"{download_directory}" # use user specified directory if provided
    else:
        print("no download directory provided")
        download_dir = f"{str(os.path.join(Path.home(), 'Downloads'))}/NYU-Stream" # Get path to user's download folder, hopefully works cross platform
        # download_dir = os.getcwd()
        print(download_dir)

    if not os.path.exists(f"{download_dir}/temp_dir"):
        os.makedirs(f"{download_dir}/temp_dir")
    if not os.path.exists(f"{download_dir}/output"):
        os.makedirs(f"{download_dir}/output")

    temp_dir = f"{download_dir}/temp_dir/"
    print(temp_dir)

    video, audio = 1, 1 # Set download mode, video + audio (default), video only, audio only
    if audio_only:
        video = 2
        file_name = f"{file_name}.m4a"
    elif video_only:
        audio = 2
        file_name = f"{file_name}.mp4"
    else: file_name = f"{file_name}.mp4"

    count = 1
    segment = f"seg-{count}-v{video}-a{audio}.ts"
    print(segment)

    base_url = re.search(r"(.*)seg.*ts\?", url).group(1) # e.g. https://cfvod.kaltura.com/scf/hls/p/1674401/sp/167440100/serveFlavor/entryId/0_qmi5nijw/v/2/ev/6/flavorId/0_sk10ecbm/name/a.mp4/
    print(base_url)

    security = re.search(r".*(\?.*)", url).group(1) #e.g. "?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTY3NDQwMS9zcC8xNjc0NDAxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX3FtaTVuaWp3L3YvMi9ldi82L2ZsYXZvcklkLzBfc2sxMGVjYm0vbmFtZS9hLm1wNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNTk5NDQ3MTkwfX19XX0_&Signature=ggJaUOJjyKjjVncLe71p3BECt2g2KKV53jhXAmUN3AvxgRT3pe9dxw4uMlASAf6nh7JEESn68Q2cPvCNgf4BOpFeh6itjNCKdTUGgk46nGay7JD7k79QFXSh6ict0JPEd92N5w6mo8C-UOdx8IZhIqF6LbNKSlOli6yf-vI75lHhknc~L6ULkEtw1d0kp8h435FNrYCqrWagVt6Cnq-jE4W~WU2YGIT~yArBbEh3n~BqdfZUDm0xlG8Y82oIdpGNgRqTpaHo2~YZkwmSJtmExEyTWs-wnRk0YxkC~k-qoPDQta-1~uU3PfjszFGTboWP-Om43FVvMjgUBIjL3qibuQ__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"
    # print(security)

    response = requests.get(f"{base_url}{segment}{security}")

    if response.status_code != 200:
        print("Invalid URL or video does not exist.")
        exit()

    fileList = []
    print("Downloading pieces...")
    while response.status_code == 200:
        segment = f"seg-{count}-v{video}-a{audio}.ts"
        response = requests.get(f"{base_url}{segment}{security}")
        with open(f"{temp_dir}{segment}", 'wb') as f:
            f.write(response.content)
        fileList.append(temp_dir + segment)
        count += 1

    # Edge case: Last piece seems to not contain any video or audio stream
    # If the file less less than 1KB, ignore and delete it
    # if os.path.getsize(fileList[-1]) < 1000:
    #     os.remove(fileList[-1])
    #     fileList = fileList[:-1]

    print("Stitching pieces...")
    with open(f"{download_dir}/output/{file_name}", 'wb') as stitched:
        for filename in fileList:
            with open(os.path.join("", filename), 'rb') as part:
                shutil.copyfileobj(part, stitched)

    # Cleanup downloaded files
    for filename in fileList:
        os.remove(filename)
    if len(os.listdir(temp_dir)) == 0:
        os.removedirs(temp_dir)

    print("Done")

if __name__ == "__main__":
    # Expected input URL format:
    # https://streaming.video.ubc.ca/ ........  a6rb/name/a.mp4
    parser = argparse.ArgumentParser(description="Download videos from NYU Stream")
    parser.add_argument("URL", default=None, help="See README for help on GitHub for help getting the correct URL")
    # parser.add_argument("-f", "--output-file-name", action="store", dest="file_name", default="output", help="output file name", metavar="file name")
    # parser.add_argument("-d", "--download-directory", action="store", dest="download_directory", help="directory to download files to", metavar="download directory")
    parser.add_argument("-f", action="store", dest="file_name", metavar="file name", default="output", help="output file name")
    parser.add_argument("-d", action="store", dest="download_directory", metavar="download directory", help="directory to download files to")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--audio-only", dest="audio", action="store_true", help="download audio only")
    group.add_argument("-v", "--video-only", dest="video", action="store_true", help="download video only")

    args = parser.parse_args()

    main(args.url, args.file_name, args.audio, args.video, args.download_directory)
