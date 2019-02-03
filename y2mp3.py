import argparse
import requests
import re
from urllib.request import build_opener
from urllib.error import HTTPError
from urllib.parse import parse_qs


def build_url(video_id):
    youtube_watch_url = 'https://www.youtube.com/watch?v='
    return youtube_watch_url + video_id

def download_youtube_video_as_mp3(video_id):
    # get video info
    get_video_info(video_id)

urls = {
    'gdata': "https://www.googleapis.com/youtube/v3/",
    'watchv': "http://www.youtube.com/watch?v=%s",
    'playlist': ('http://www.youtube.com/list_ajax?'
                 'style=json&action_get_list=1&list=%s'),
    'thumb': "http://i.ytimg.com/vi/%s/default.jpg",
    'bigthumb': "http://i.ytimg.com/vi/%s/mqdefault.jpg",
    'bigthumbhd': "http://i.ytimg.com/vi/%s/hqdefault.jpg",

    'vidinfo': ('https://www.youtube.com/get_video_info?video_id=%s&'
                'eurl=https://youtube.googleapis.com/v/%s&sts=%s'),
    'embed': "https://youtube.com/embed/%s"
    }

def get_video_info(video_id):
    """ Return info for video_id.  Returns dict. """
    embed_webpage = fetch_decode(urls['embed'])
    sts = re.search(r'sts"\s*:\s*(\d+)', embed_webpage).group(1)

    url = urls['vidinfo'] % (video_id, video_id, sts)

    info_bytes = fetch_decode(url)  # bytes
    info_dict = parseqs(info_bytes)  # unicode dict

    import pdb; pdb.set_trace()

    if info_dict['status'][0] == "fail":
        reason = info_dict['reason'][0] or "Bad video argument"

    return info_dict

def parseqs(data):
    """ parse_qs, return unicode. """
    if type(data) == str:
        return parse_qs(data)
    else:
        data = data.decode("utf8")
        data = parse_qs(data)

    return data

def fetch_decode(url, encoding=None):
    """ Fetch url and decode. """
    try:
        req = build_opener().open(url)
    except HTTPError as e:
        if e.getcode() == 503:
            time.sleep(.5)
            return fetch_decode(url, encoding)
        else:
            raise

    print("Url: {0}".format(url))
    ct = req.headers['content-type']

    if encoding:
        return req.read().decode(encoding)
    elif "charset=" in ct:
        encoding = re.search(r"charset=([\w-]+)\s*(:?;|$)", ct).group(1)
        return req.read().decode(encoding)
    else:
        return req.read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_id',
            help='the video id given in the youtube watch url with the "v" parameter')
    args = parser.parse_args()

    download_youtube_video_as_mp3(args.video_id)

if __name__ == '__main__':
    main()
