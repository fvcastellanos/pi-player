
from player.Track import Track


class AudioDisc:

    id: str
    tracks = []

    def __init__(self, id: str):

        self.id = id

    def __init__(self, id: str, tracks):

        self.id = id
        self.tracks = tracks

    def getTrackCount(self) -> int:

        return self.tracks.count()

    def addTrack(self, track: Track):

        self.tracks.append(track)

    def getCurrentTrack(self) -> Track:

        for track in self.tracks:
            if (track.current):
                return track

        return None