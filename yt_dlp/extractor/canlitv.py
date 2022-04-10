# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_urllib_parse_urlparse


class CanliTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?canlitv\.(?:com|fun)/(?P<id>[\w\d-]+)'
    _TESTS = [{
        'url': 'https://canlitv.com/canli-tv8',
        'info_dict': {
            'id': 'canli-tv8',
            'live_status': 'is_live',
            'ext': 'mp4',
            'title': r're:^Tv8 Canlı izle \d{4}-\d{2}-\d{2} \d{2}:\d{2}$',
            'description': 'md5:1ddd9b9c25fbffdd934fe05b94b0e39d',
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://canlitv.com/muz-tv',
        'info_dict': {
            'id': 'L4_vc5hKW2U',
            'ext': 'mp4',
            'uploader_url': 'http://www.youtube.com/user/muzTV',
            'release_timestamp': 1649019268,
            'thumbnail': 'https://i.ytimg.com/vi/L4_vc5hKW2U/maxresdefault_live.jpg',
            'live_status': 'is_live',
            'channel_follower_count': int,
            'playable_in_embed': True,
            'categories': list,
            'view_count': int,
            'tags': list,
            'channel_url': 'https://www.youtube.com/channel/UC2eH4vw5JuVpzLDrCkxW2pQ',
            'availability': 'unlisted',
            'description': 'md5:62c2be1023cf79b75e76e6ba7ff068e0',
            'like_count': int,
            'release_date': '20220403',
            'upload_date': '20220403',
            'channel': 'МУЗ-ТВ',
            'uploader': 'МУЗ-ТВ',
            'age_limit': 0,
            'channel_id': 'UC2eH4vw5JuVpzLDrCkxW2pQ',
            'title': r're:^Онлайн трансляция телеканала МУЗ-ТВ \d{4}-\d{2}-\d{2} \d{2}:\d{2}$',
            'uploader_id': 'muzTV',
        },
        'add_ie': ['Youtube'],
        'params': {
            'skip_download': True,
        },
    }, {
        'url': ' https://canlitv.fun/canli-tv8',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        player_page_path = self._search_regex(r'(/player/index.php\?id=\d+)', webpage, 'player_page_path')
        parsed_url_obj = compat_urllib_parse_urlparse(url)
        player_page_url = f'{parsed_url_obj.scheme}://{parsed_url_obj.netloc}{player_page_path}'
        player_page = self._download_webpage(player_page_url, video_id, headers={
            'Referer': url,
        })

        hls_url = self._search_regex(r'file:\s*"([^"]+)"', player_page, 'hls_url', default=None)
        if not hls_url:
            return self.url_result(self._search_regex(r'"(https://www.youtube.com/embed[^"]+)"', player_page,
                                                      'yt_embed_url'), 'Youtube')

        formats = self._extract_m3u8_formats(hls_url, video_id, 'mp4', m3u8_id='hls')
        self._sort_formats(formats)

        return {
            'id': video_id,
            'is_live': True,
            'title': self._og_search_title(webpage),
            'description': self._og_search_description(webpage, default=''),
            'formats': formats,
        }
