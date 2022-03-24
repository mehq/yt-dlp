# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..compat import compat_urllib_parse_urlparse
from ..utils import smuggle_url


class CraftsyIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?craftsy.com/class/(?P<id>[\w-]+)'
    _TESTS = [{
        'url': 'https://www.craftsy.com/class/all-access-estes-park-wool-market/',
        'info_dict': {
            'id': '278194',
            'title': 'All Access: Estes Park Wool Market',
        },
        'playlist_count': 6,
    }, {
        'url': 'https://www.craftsy.com/class/all-access-estes-park-wool-market/#6172661053001',
        'md5': 'd7e883a839b4b4c4d153e1ca78b776a6',
        'info_dict': {
            'id': '6172661053001',
            'ext': 'mp4',
            'title': 'Ivy Sipes',
            'duration': 431.573,
            'timestamp': 1595016833,
            'upload_date': '20200717',
            'uploader_id': '6168786647001',
            'formats': 'count:46',
            'thumbnail': r're:https?://.*\.jpg',
            'tags': 'count:8',
        },
        'params': {
            'noplaylist': True,
        },
    }]

    def _brightcove_result(self, account_id, player_id, video_id):
        return self.url_result(
            smuggle_url(
                f'https://players.brightcove.net/{account_id}/{player_id}_default/index.html?videoId={video_id}',
                data={'referrer': 'https://www.craftsy.com/'}
            ), video_id=video_id)

    def _real_extract(self, url):
        class_id = self._match_id(url)
        video_id = compat_urllib_parse_urlparse(url).fragment
        webpage = self._download_webpage(url, class_id)
        data = self._parse_json(
            self._search_regex(r'class_video_player_vars\s*=\s*({.+?}});', webpage, 'class data'), class_id)
        class_id = data.get('class_id') or class_id
        player_data = data['video_player']
        player_id = (
                player_data.get('preview_player_id')
                or player_data.get('lesson_player_id')
                or player_data.get('free_player_id'))
        account_id = player_data['bc_account_id']

        if not self._yes_playlist(class_id, video_id):
            return self._brightcove_result(account_id, player_id, video_id)

        entries = [
            self._brightcove_result(account_id, player_id, lesson['video_id'])
            for lesson in data['lessons']
        ]

        if player_data.get('class_preview'):
            entries.insert(0, self._brightcove_result(account_id, player_id,
                                                      player_data['class_preview']['video_id']))

        return self.playlist_result(entries, class_id, data.get('class_title'))
