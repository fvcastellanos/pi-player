from ui.MainWindow import MainWindow
from player.MediaPlayer import MediaPlayer

import logging
import os

def main():

    logging.basicConfig(level= logging.INFO, format='%(asctime)s - %(levelname)s:%(module)s:%(funcName)s:%(lineno)s: %(message)s')

    path = os.environ["MEDIA_PATH"]

    player = MediaPlayer(path = path)
    mainWindow = MainWindow(player, title = "Pi Player")
    mainWindow.show()

if __name__ == '__main__':

    main()
    