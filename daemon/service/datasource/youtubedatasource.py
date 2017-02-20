import logging
import sys

from decorator.datasource import datasource
from provider.musicvideo.youtubeprovider import YoutubeProvider


@datasource('youtube')
class YoutubeDatasource(object):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self._youtubeProvider = YoutubeProvider()

    def _process(self, datasource, tracks):
        for track in tracks:
            try:
                self.logger.info(
                    'fetching datasource for artist=%s, album=%s, track=%s',
                    track.album.artist.name, track.album.name, track.name)

                repo = self._youtubeProvider.getMusicVideo(
                    track.album.artist.name, track.album.name, track.name)

                self.logger.info('done. repo=%s', repo)

                # set relationship
                repo.track = track
                datasource.repositories.append(repo)
            except:
                e = sys.exc_info()[1]
                self.logger.error(e)
