from tkinter import *

import vlc

# from MediaPlayer import Player

def close(root, player):
    
    player.stop()
    root.destroy()


def play(player):

    player.play()

def main():
    root = Tk()
    root.title("Pi Player")
    root.geometry("400x300")

    # player = Player(root, video= 'D:\\OneDrive\\Imágenes\\Blade Runner -1982- Official Trailer - Ridley Scott- Harrison Ford Movie_Trim.mp4');
    # player = Player(root, video= 'D:\\OneDrive\\Imágenes\\01. The Number Of The Beast.mp3');

    player = vlc.MediaPlayer('D:\\OneDrive\\Imágenes\\01. The Number Of The Beast.mp3')
    # player.play()

    media = player.get_media()
    type = media.get_type()

    print(f"media type: {type} - media: {media}")

    songName = "fooSong"

    Label(root, text= songName).grid(row= 2, column= 1)

    Button(root, text = "Play", command=lambda: play(player), width=5, height=2).grid(row=4, column=1)

    root.protocol("WM_DELETE_WINDOW", func= lambda: close(root, player))
    root.mainloop()

if __name__ == '__main__':
    
    main()


