import argparse

def build_url(video_id):
    youtube_watch_url = 'https://www.youtube.com/watch?v='
    return youtube_watch_url + video_id

def download_youtube_video_as_mp3(video_id):
    url = build_url(args.video_id)
    print(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id', help='the video id given in the youtube watch url with the "v" parameter')
    args = parser.parse_args()
