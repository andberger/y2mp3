import argparse
import requests
import re
from urllib.request import build_opener, urlopen
from urllib.error import HTTPError
from urllib.parse import parse_qs, parse_qsl, unquote


def download_youtube_video_as_mp3(video_id):
    # get video info
    info_dict = get_video_info(video_id)

    # extract stream map
    stream_maps = info_dict['url_encoded_fmt_stream_map']

    import pdb; pdb.set_trace()

    # descramble stream data
    for fmt in stream_maps:
        apply_descrambler(info_dict, fmt)


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

def apply_descrambler(stream_data, key):
    stream_data[key] = [
        {k: unquote(v) for k, v in parse_qsl(i)}
        for i in stream_data[key].split(',')
    ]

def apply_mixin(dct, key, func, *args, **kwargs):
    dct[key] = func(dct[key], *args, **kwargs)

def get_video_info(video_id):
    """ Return info for video_id.  Returns dict. """
    embed_webpage = fetch_decode(urls['embed'])
    sts = re.search(r'sts"\s*:\s*(\d+)', embed_webpage).group(1)

    url = urls['vidinfo'] % (video_id, video_id, sts)

    import pdb; pdb.set_trace()
    video_info = urlopen(url).read().decode('utf-8')
    info_dict = {k: v for k, v in parse_qsl(video_info)}

    return info_dict

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
