# from tkinter import *

# from MediaPlayer import Player

# root = Tk()
# root.title("Pi Player")

# # player = Player(root, video= 'D:\\OneDrive\\Imágenes\\Blade Runner -1982- Official Trailer - Ridley Scott- Harrison Ford Movie_Trim.mp4');
# player = Player(root, video= 'D:\\OneDrive\\Imágenes\\01. The Number Of The Beast.mp3');
# root.protocol("WM_DELETE_WINDOW", player.OnClose)
# root.mainloop()

from ui.MainWindow import MainWindow
from player.MediaPlayer import MediaPlayer

import logging

def main():

    logging.basicConfig(level= logging.INFO, format='%(asctime)s - %(levelname)s:%(module)s:%(funcName)s:%(lineno)s: %(message)s')
    # logging.basicConfig(level= logging.INFO)

    player = MediaPlayer()
    mainWindow = MainWindow(player, title = "Pi Player")
    mainWindow.show()

if __name__ == '__main__':

    main()