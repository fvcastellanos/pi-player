from ctypes import alignment
from tkinter import *
from player.MediaPlayer import MediaPlayer

import logging

class MainWindow:

    __window: Tk
    __player: MediaPlayer
    __trackList = Listbox

    __currentTrack: StringVar
    __tracksCount: StringVar

    logger = logging.getLogger(__name__)

    def __init__(self, player: MediaPlayer, title = "Application", geometry = "480x320"):
        
        self.__window = Tk()
        self.__window.title(title)
        self.__window.geometry(geometry)

        self.__player = player

        self.__tracksCount = IntVar(0)
        self.__currentTrack = StringVar("")

    def show(self):

        self.__window.protocol("WM_DELETE_WINDOW", func = lambda: self.__onClose())
        self.__buildControls()
        self.__window.mainloop()

    # ----------------------------------------------------------------------

    def __onClose(self):

        self.logger.info("Close window instance")

        self.__player.stop()
        self.__window.destroy()

    def __play(self):

        self.__player.play()

    def __stop(self):

        self.__player.stop()

    def __pause(self):

        self.__player.pause()

    def __next(self):

        self.__player.next()

    def __previous(self):

        self.__player.prev()

    def __loadDiskInformation(self):

        self.logger.info("Load Disc information")

        self.__player.loadDisk()

        info = self.__player.audioDisc

        self.__trackList.delete(0, END)

        if info != None:

            labels = [track.label for track in info.tracks]

            self.__trackList.insert(END, *labels)
            self.__tracksCount.set(len(labels))

    # ----------------------------------------------------------------------

    def __buildInformation(self, frame: Frame):

        self.logger.info("Start building Information controls")
        Label(frame, text = "Current track:").grid(row = 1, column = 1)
        Label(frame, text = "Tracks:").grid(row = 2, column = 1)

        Label(frame, textvariable = self.__currentTrack).grid(row = 1, column = 2)
        Label(frame, textvariable = self.__tracksCount).grid(row = 2, column = 2)

    def __buildControls(self):

        self.logger.info("Start building UI")

        topFrame = Frame(self.__window, height = 30)
        topFrame.pack(fill = BOTH, side = TOP, expand = True, anchor = "w")

        middleFrame = Frame(self.__window, height = 200, bg = "blue")
        middleFrame.pack(fill = BOTH, side = TOP, expand = True)

        controlsFrame = Frame(self.__window, height = 30)
        controlsFrame.pack(fill = BOTH, side = TOP, expand = True)

        bottomFrame = Frame(self.__window, height = 40)
        bottomFrame.pack(fill = BOTH, side = TOP, expand = True)

        self.__buildInformation(topFrame)

        self.__buildDisplay(middleFrame)

        self.__buildMediaButtons(controlsFrame)


        Label(bottomFrame, text = "Pi Player v 1.0").place(x = 10, y = 10)

        self.logger.info("UI built")

    def __buildDisplay(self, frame: Frame):

        self.logger.info("Start building display controls")

        self.__trackList = Listbox(frame)
        self.__trackList.grid(row = 1, column = 1, columnspan = 3)


    def __buildMediaButtons(self, frame: Frame):

        Button(frame, text = u"\u23F5", width = 3, command = self.__play) \
            .grid(row = 1, column = 1, columnspan = 2)

        Label(frame, text = " ").grid(row = 1, column = 3)

        Button(frame, text = u"\u23F8", width = 3, command = self.__pause) \
            .grid(row = 1, column = 4, columnspan = 2)
        Label(frame, text = " ").grid(row = 1, column = 7)

        Button(frame, text = u"\u23F9", width = 3, command = self.__stop) \
            .grid(row = 1, column = 8, columnspan = 2)
        Label(frame, text = " ").grid(row = 1, column = 10)

        Button(frame, text = u"\u23EE", width = 3, command = self.__previous) \
            .grid(row = 1, column = 11, columnspan = 2)
        Label(frame, text = " ").grid(row = 1, column = 13)

        Button(frame, text = u"\u23ED", width = 3, command = self.__next) \
            .grid(row = 1, column = 14, columnspan = 2)
        Label(frame, text = " ").grid(row = 1, column = 16)

        Button(frame, text = u"\u21BB", width = 3) \
            .grid(row = 1, column = 17, columnspan = 2)

        Button(frame, text = u"\u21C4", width = 3, command = self.__loadDiskInformation) \
            .grid(row = 1, column = 20, columnspan = 2)


