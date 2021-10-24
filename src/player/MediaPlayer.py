import vlc
import logging
import discid

from player.AudioDisc import AudioDisc
from player.Track import Track

logger = logging.getLogger(__name__)

class MediaPlayer:

    __mediaPath: str
    __player : vlc.MediaPlayer
    __mediaList : vlc.MediaList
    __mediaListPlayer : vlc.MediaListPlayer
    __eventManager: vlc.EventManager
    __media: vlc.Media

    audioDisc: AudioDisc

    def __init__(self, path = "cdda:///dev/sr0"):

        self.__mediaPath = path
        self.audioDisc = None

        self.__createMediaPlayer()

    def play(self):

        logger.info("Play track")
        self.__mediaListPlayer.play()
    
    def stop(self):

        logger.info("Stop track")

        if self.__mediaListPlayer.is_playing():
            self.__mediaListPlayer.stop()

    def pause(self):

        logger.info("Pause track")
        self.__mediaListPlayer.pause()

    def next(self):

        logger.info("Next track")
        self.__mediaListPlayer.next()

    def prev(self):

        logger.info("Previous track")
        self.__mediaListPlayer.previous()

    def loadDisk(self):

        logger.info("Load disc")
        self.__loadDisk(self.__mediaPath)

    # ----------------------------------------------------------------------

    def __loadDisk(self, path: str):

        logger.info(f"Load media player resource: {path}")


        self.__getDiscInformation(path)

        if (self.audioDisc != None):

            for track in self.audioDisc.tracks:
                
                self.__media = vlc.Media(path, (track.playerName))
                self.__mediaList.add_media(self.__media)

            self.__mediaListPlayer.set_media_list(self.__mediaList)

            self.__eventManager = self.__player.event_manager()
            # self.__eventManager__.event_attach(vlc.EventType.MediaParsedChanged, self.__getDiscInformation__)
            # self.__eventManager.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.__mediaPlayerTimeChanged)
            
    def __mediaPlayerTimeChanged(self, event):

        logger.info(f"time changed: {event}")

    def __getDiscInformation(self, path: str):

        try:
            discDevice = path[7:]
            disc : discid.Disc = discid.read(device = discDevice)

            logger.info(f"disc id: {disc.id}")

            tracks = [Track(name = track.number, duration = track.seconds) for track in disc.tracks]
            self.audioDisc = AudioDisc(id = disc.id, tracks =  tracks)
        
        except Exception as exception:

            logger.exception("Unable to load disc information", exception)

    def __createMediaPlayer(self): 

        vlcInstance = vlc.Instance()
        self.__player = vlcInstance.media_player_new()

        self.__mediaList = vlcInstance.media_list_new()

        self.__mediaListPlayer = vlcInstance.media_list_player_new()
        self.__mediaListPlayer.set_media_player(self.__player)


        
        