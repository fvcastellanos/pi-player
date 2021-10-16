
import vlc
import logging

logger = logging.getLogger(__name__)

class MediaPlayer:

    __player__ : vlc.MediaPlayer

    def __init__(self, path = "cdda:///E:/"):

        logger.info(f"Load media player resource: {path}")
        # self.__player__ = vlc.MediaPlayer(path)
        self.__player__ = vlc.MediaPlayer()

        flag = vlc.MediaParseFlag(0) # local

        media = vlc.Media(path)

        media.parse_with_options(flag, 2000)

        self.__player__.set_media(media)

    def play(self):

        logger.info("Play track")
        self.__player__.play()
    
    def stop(self):

        logger.info("Stop track")
        self.__player__.stop()