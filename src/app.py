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