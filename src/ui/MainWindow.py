from tkinter import *

class MainWindow:

    __window__: Tk

    def __init__(self, title = "Application", geometry = "400x300"):
        
        self.__window__ = Tk()
        self.__window__.title(title)
        self.__window__.geometry(geometry)

    def show(self):

        self.__window__.protocol("WM_DELETE_WINDOW", func = lambda: self.onClose())
        self.__buildControls__()
        self.__window__.mainloop()

    def onClose(self):

        self.__window__.destroy()

    def __buildControls__(self):

        topFrame = Frame(self.__window__)
        topFrame.pack(side= TOP)

        middleFrame = Frame(self.__window__)
        middleFrame.pack(side= TOP)

        bottomFrame = Frame(self.__window__)
        bottomFrame.pack(side = BOTTOM)

