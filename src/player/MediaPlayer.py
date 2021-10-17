import vlc
import logging

logger = logging.getLogger(__name__)

class MediaPlayer:

    __player__ : vlc.MediaPlayer
    __mediaList__ : vlc.MediaList
    __mediaListPlayer__ : vlc.MediaListPlayer
    __eventManager__: vlc.EventManager
    __media__: vlc.Media

    def __init__(self, path = "cdda:///dev/sr0"):

        self.__loadDisk__(path)

    def play(self):

        logger.info("Play track")
        self.__mediaListPlayer__.play()
        # self.__getDiscInformation__()
    
    def stop(self):

        logger.info("Stop track")
        self.__mediaListPlayer__.stop()

    def pause(self):

        logger.info("Pause track")
        self.__mediaListPlayer__.pause()

    def next(self):

        logger.info("Next track")
        self.__mediaListPlayer__.next()

    def prev(self):

        logger.info("Previous track")
        self.__mediaListPlayer__.previous()

    # ----------------------------------------------------------------------

    def __loadDisk__(self, path: str):

        logger.info(f"Load media player resource: {path}")

        vlcInstance = vlc.Instance()

        self.__player__ = vlcInstance.media_player_new()

        self.__mediaList__ = vlcInstance.media_list_new()

        self.__mediaListPlayer__ = vlcInstance.media_list_player_new()
        self.__mediaListPlayer__.set_media_player(self.__player__)

        self.__media__ = vlc.Media(path)
        self.__media__.parse_with_options(vlc.MediaParseFlag.do_interact, 0)

        self.__mediaList__.add_media(self.__media__)

        self.__mediaListPlayer__.set_media_list(self.__mediaList__)

        self.__eventManager__ = self.__player__.event_manager()
        self.__eventManager__.event_attach(vlc.EventType.MediaParsedChanged, self.__getDiscInformation__)


    def __getDiscInformation__(self):

        logger.info("Media information retrieved")

        media = self.__player__.get_media()

        logger.info(f"media: {media.tracks_get()}")

        
        