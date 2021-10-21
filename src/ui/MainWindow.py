from tkinter import *
from player.MediaPlayer import MediaPlayer

import logging

class MainWindow:

    __window__: Tk
    __player__: MediaPlayer
    logger = logging.getLogger(__name__)

    def __init__(self, player: MediaPlayer, title = "Application", geometry = "400x300"):
        
        self.__window__ = Tk()
        self.__window__.title(title)
        self.__window__.geometry(geometry)

        self.__player__ = player

    def show(self):

        self.__window__.protocol("WM_DELETE_WINDOW", func = lambda: self.__onClose__())
        self.__buildControls__()
        self.__window__.mainloop()

    # ----------------------------------------------------------------------

    def __onClose__(self):

        self.logger.info("Close window instance")

        self.__player__.stop()
        self.__window__.destroy()

    def __play__(self):

        self.__player__.play()

    def __stop__(self):

        self.__player__.stop()

    def __pause__(self):

        self.__player__.pause()

    def __next__(self):

        self.__player__.next()

    def __previous__(self):

        self.__player__.prev()

    # ----------------------------------------------------------------------

    def __buildInformation__(self, frame: Frame):

        self.logger.info("Start building Information controls")
        Label(frame, text = f"Current track:").grid(row = 1, column = 2)


    def __buildDisplay__(self, frame: Frame):

        self.logger.info("Start building display controls")

    def __buildControls__(self):

        self.logger.info("Start building UI")

        topFrame = Frame(self.__window__, height = 30)
        topFrame.pack(fill = BOTH, side = TOP, expand = True)

        self.__buildInformation__(topFrame)

        middleFrame = Frame(self.__window__, height = 200, bg = "blue")
        middleFrame.pack(fill = BOTH, side = TOP, expand = True)

        self.__buildDisplay__(middleFrame)

        controlsFrame = Frame(self.__window__, height = 30)
        controlsFrame.pack(fill = BOTH, side = TOP, expand = True)

        Button(controlsFrame, text = "▶", width = 7, command = self.__play__) \
            .grid(row = 1, column = 1, columnspan = 2)

        Label(controlsFrame, text = " ").grid(row = 1, column = 3)

        Button(controlsFrame, text = "||", width = 7, command = self.__pause__) \
            .grid(row = 1, column = 4, columnspan = 2)
        Label(controlsFrame, text = " ").grid(row = 1, column = 7)

        Button(controlsFrame, text = "Stop", width = 7, command = self.__stop__) \
            .grid(row = 1, column = 8, columnspan = 2)
        Label(controlsFrame, text = " ").grid(row = 1, column = 10)

        Button(controlsFrame, text = "|<<", width = 7, command = self.__previous__) \
            .grid(row = 1, column = 14, columnspan = 2)
        Label(controlsFrame, text = " ").grid(row = 1, column = 13)

        Button(controlsFrame, text = ">>|", width = 7, command = self.__next__) \
            .grid(row = 1, column = 11, columnspan = 2)
        Label(controlsFrame, text = " ").grid(row = 1, column = 16)

        Button(controlsFrame, text = "Repeat", width = 7) \
            .grid(row = 1, column = 17, columnspan = 2)

        bottomFrame = Frame(self.__window__, height = 40)
        bottomFrame.pack(fill = BOTH, side = TOP, expand = True)

        Label(bottomFrame, text = "Pi Player v 1.0").place(x = 10, y = 10)

        self.logger.info("UI built")
