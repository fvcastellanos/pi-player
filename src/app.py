# from tkinter import *

# from MediaPlayer import Player

# root = Tk()
# root.title("Pi Player")

# # player = Player(root, video= 'D:\\OneDrive\\Imágenes\\Blade Runner -1982- Official Trailer - Ridley Scott- Harrison Ford Movie_Trim.mp4');
# player = Player(root, video= 'D:\\OneDrive\\Imágenes\\01. The Number Of The Beast.mp3');
# root.protocol("WM_DELETE_WINDOW", player.OnClose)
# root.mainloop()

from ui.MainWindow import MainWindow

def main():

    mainWindow = MainWindow(title = "Pi Player")
    mainWindow.show()

if __name__ == '__main__':

    main()