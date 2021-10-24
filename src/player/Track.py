
class Track:

    name: str
    label: str
    playerName: str

    duration: int
    current: bool

    def __init__(self, name: str):

        self.__init__(name, 0)
    
    def __init__(self, name: str, duration: int):

        self.name = self.label = self.__buildName(name)
        self.playerName = self.__buildPlayerName(name)
        self.duration = duration
        self.current = False

    def __buildPlayerName(self, id: str) -> str:

        return f":cdda-track={id}"

    def __buildName(self, id: str) -> str:

        return f"Track {id}"

    