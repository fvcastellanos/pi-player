import tkinter as Tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
from TkMenu import _Tk_Menu

import time
import vlc
import sys

_isLinux   = sys.platform.startswith('linux')
_isMacOS   = sys.platform.startswith('darwin')
_isWindows = sys.platform.startswith('win')

class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    _geometry = ''
    _stopped  = None

    def __init__(self, parent, title=None, video=''):
        Tk.Frame.__init__(self, parent)

        self.parent = parent  # == root
        self.parent.title(title or "tkVLCplayer")
        self.video = expanduser(video)

        # Menu Bar
        #   File Menu
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = _Tk_Menu(menubar)
        fileMenu.bind_shortcuts_to(parent)  # XXX must be root?

        fileMenu.add_shortcut("Open...", 'o', self.OnOpen)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Play", 'p', self.OnPlay)  # Play/Pause
        fileMenu.add_command(label="Stop", command=self.OnStop)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Mute", 'm', self.OnMute)
        fileMenu.add_separator()
        fileMenu.add_shortcut("Close", 'c', self.OnClose)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.fileMenu = fileMenu
        self.playIndex = fileMenu.index("Play")
        self.muteIndex = fileMenu.index("Mute")

        # first, top panel shows video

        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel)
        self.canvas.pack(fill=Tk.BOTH, expand=1)
        self.videopanel.pack(fill=Tk.BOTH, expand=1)

        # panel to hold buttons
        self.buttons_panel = Tk.Toplevel(self.parent)
        self.buttons_panel.title("")
        self.is_buttons_panel_anchor_active = False

        buttons = ttk.Frame(self.buttons_panel)
        self.playButton = ttk.Button(buttons, text="Play", command=self.OnPlay)
        stop            = ttk.Button(buttons, text="Stop", command=self.OnStop)
        self.muteButton = ttk.Button(buttons, text="Mute", command=self.OnMute)
        self.playButton.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        self.muteButton.pack(side=Tk.LEFT)

        self.volMuted = False
        self.volVar = Tk.IntVar()
        self.volSlider = Tk.Scale(buttons, variable=self.volVar, command=self.OnVolume,
                                  from_=0, to=100, orient=Tk.HORIZONTAL, length=200,
                                  showvalue=0, label='Volume')
        self.volSlider.pack(side=Tk.RIGHT)
        buttons.pack(side=Tk.BOTTOM, fill=Tk.X)


        # panel to hold player time slider
        timers = ttk.Frame(self.buttons_panel)
        self.timeVar = Tk.DoubleVar()
        self.timeSliderLast = 0
        self.timeSlider = Tk.Scale(timers, variable=self.timeVar, command=self.OnTime,
                                   from_=0, to=1000, orient=Tk.HORIZONTAL, length=500,
                                   showvalue=0)  # label='Time',
        self.timeSlider.pack(side=Tk.BOTTOM, fill=Tk.X, expand=1)
        self.timeSliderUpdate = time.time()
        timers.pack(side=Tk.BOTTOM, fill=Tk.X)


        # VLC player
        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        self.parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        self.parent.update()

        # After parent.update() otherwise panel is ignored.
        self.buttons_panel.overrideredirect(True)

        # Estetic, to keep our video panel at least as wide as our buttons panel.
        self.parent.minsize(width=502, height=0)

        self.is_buttons_panel_anchor_active = False

        self._AnchorButtonsPanel()

        self.OnTick()  # set the timer up

    def OnClose(self, *unused):
        """Closes the window and quit.
        """
        # print("_quit: bye")
        self.parent.quit()  # stops mainloop
        self.parent.destroy()  # this is necessary on Windows to avoid
        # ... Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def _DetectButtonsPanelDragging(self, _):
        """If our last click was on the boarder
           we disable the anchor.
        """
        if self.has_clicked_on_buttons_panel:
            self.is_buttons_panel_anchor_active = False
            self.buttons_panel.unbind("<Button-1>")
            self.buttons_panel.unbind("<B1-Motion>")
            self.buttons_panel.unbind("<ButtonRelease-1>")

    def _AnchorButtonsPanel(self):
        video_height = self.parent.winfo_height()
        panel_x = self.parent.winfo_x()
        panel_y = self.parent.winfo_y() + video_height + 23 # 23 seems to put the panel just below our video.
        panel_height = self.buttons_panel.winfo_height()
        panel_width = self.parent.winfo_width()
        self.buttons_panel.geometry("%sx%s+%s+%s" % (panel_width, panel_height, panel_x, panel_y))

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?

        if self.is_buttons_panel_anchor_active:
            self._AnchorButtonsPanel()

    def OnFullScreen(self, *unused):
        """Toggle full screen, macOS only.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/wm.htm#M10>
        f = not self.parent.attributes("-fullscreen")  # or .wm_attributes
        if f:
            self._previouscreen = self.parent.geometry()
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.bind("<Escape>", self.OnFullScreen)
        else:
            self.parent.attributes("-fullscreen", f)  # or .wm_attributes
            self.parent.geometry(self._previouscreen)
            self.parent.unbind("<Escape>")

    def OnMute(self, *unused):
        """Mute/Unmute audio.
        """
        # audio un/mute may be unreliable, see vlc.py docs.
        self.volMuted = m = not self.volMuted  # self.player.audio_get_mute()
        self.player.audio_set_mute(m)
        u = "Unmute" if m else "Mute"
        self.fileMenu.entryconfig(self.muteIndex, label=u)
        self.muteButton.config(text=u)
        # update the volume slider text
        self.OnVolume()

    def OnOpen(self, *unused):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop()
        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a video".
        video = askopenfilename(initialdir = Path(expanduser("~")),
                                title = "Choose a video",
                                filetypes = (("all files", "*.*"),
                                             ("mp4 files", "*.mp4"),
                                             ("mov files", "*.mov")))
        self._Play(video)

    def _Pause_Play(self, playing):
        # re-label menu item and button, adjust callbacks
        p = 'Pause' if playing else 'Play'
        c = self.OnPlay if playing is None else self.OnPause
        self.fileMenu.entryconfig(self.playIndex, label=p, command=c)
        # self.fileMenu.bind_shortcut('p', c)  # XXX handled
        self.playButton.config(text=p, command=c)
        self._stopped = False

    def _Play(self, video):
        # helper for OnOpen and OnPlay
        if isfile(video):  # Creation
            m = self.Instance.media_new(str(video))  # Path, unicode
            self.player.set_media(m)
            self.parent.title("tkVLCplayer - %s" % (basename(video),))

            # set the window id where to render VLC's video output
            h = self.videopanel.winfo_id()  # .winfo_visualid()?
            if _isWindows:
                self.player.set_hwnd(h)
            else:
                self.player.set_xwindow(h)  # fails on Windows
            # FIXME: this should be made cross-platform
            self.OnPlay()

    def OnPause(self, *unused):
        """Toggle between Pause and Play.
        """
        if self.player.get_media():
            self._Pause_Play(not self.player.is_playing())
            self.player.pause()  # toggles

    def OnPlay(self, *unused):
        """Play video, if none is loaded, open the dialog window.
        """
        # if there's no video to play or playing,
        # open a Tk.FileDialog to select a file
        if not self.player.get_media():
            if self.video:
                self._Play(expanduser(self.video))
                self.video = ''
            else:
                self.OnOpen()
        # Try to play, if this fails display an error message
        elif self.player.play():  # == -1
            self.showError("Unable to play the video.")
        else:
            self._Pause_Play(True)
            # set volume slider to audio level
            vol = self.player.audio_get_volume()
            if vol > 0:
                self.volVar.set(vol)
                self.volSlider.set(vol)

    def OnResize(self, *unused):
        """Adjust the window/frame to the video aspect ratio.
        """
        g = self.parent.geometry()
        if g != self._geometry and self.player:
            u, v = self.player.video_get_size()  # often (0, 0)
            if v > 0 and u > 0:
                # get window size and position
                g, x, y = g.split('+')
                w, h = g.split('x')
                # alternatively, use .winfo_...
                # w = self.parent.winfo_width()
                # h = self.parent.winfo_height()
                # x = self.parent.winfo_x()
                # y = self.parent.winfo_y()
                # use the video aspect ratio ...
                if u > v:  # ... for landscape
                    # adjust the window height
                    h = round(float(w) * v / u)
                else:  # ... for portrait
                    # adjust the window width
                    w = round(float(h) * u / v)
                self.parent.geometry("%sx%s+%s+%s" % (w, h, x, y))
                self._geometry = self.parent.geometry()  # actual

    def OnStop(self, *unused):
        """Stop the player, resets media.
        """
        if self.player:
            self.player.stop()
            self._Pause_Play(None)
            # reset the time slider
            self.timeSlider.set(0)
            self._stopped = True
        # XXX on macOS libVLC prints these error messages:
        # [h264 @ 0x7f84fb061200] get_buffer() failed
        # [h264 @ 0x7f84fb061200] thread_get_buffer() failed
        # [h264 @ 0x7f84fb061200] decode_slice_header error
        # [h264 @ 0x7f84fb061200] no frame!

    def OnTick(self):
        """Timer tick, update the time slider to the video time.
        """
        if self.player:
            # since the self.player.get_length may change while
            # playing, re-set the timeSlider to the correct range
            t = self.player.get_length() * 1e-3  # to seconds
            if t > 0:
                self.timeSlider.config(to=t)

                t = self.player.get_time() * 1e-3  # to seconds
                # don't change slider while user is messing with it
                if t > 0 and time.time() > (self.timeSliderUpdate + 2):
                    self.timeSlider.set(t)
                    self.timeSliderLast = int(self.timeVar.get())
        # start the 1 second timer again
        self.parent.after(1000, self.OnTick)
        # adjust window to video aspect ratio, done periodically
        # on purpose since the player.video_get_size() only
        # returns non-zero sizes after playing for a while
        if not self._geometry:
            self.OnResize()

    def OnTime(self, *unused):
        if self.player:
            t = self.timeVar.get()
            if self.timeSliderLast != int(t):
                # this is a hack. The timer updates the time slider.
                # This change causes this rtn (the 'slider has changed' rtn)
                # to be invoked.  I can't tell the difference between when
                # the user has manually moved the slider and when the timer
                # changed the slider.  But when the user moves the slider
                # tkinter only notifies this rtn about once per second and
                # when the slider has quit moving.
                # Also, the tkinter notification value has no fractional
                # seconds.  The timer update rtn saves off the last update
                # value (rounded to integer seconds) in timeSliderLast if
                # the notification time (sval) is the same as the last saved
                # time timeSliderLast then we know that this notification is
                # due to the timer changing the slider.  Otherwise the
                # notification is due to the user changing the slider.  If
                # the user is changing the slider then I have the timer
                # routine wait for at least 2 seconds before it starts
                # updating the slider again (so the timer doesn't start
                # fighting with the user).
                self.player.set_time(int(t * 1e3))  # milliseconds
                self.timeSliderUpdate = time.time()

    def OnVolume(self, *unused):
        """Volume slider changed, adjust the audio volume.
        """
        vol = min(self.volVar.get(), 100)
        v_M = "%d%s" % (vol, " (Muted)" if self.volMuted else '')
        self.volSlider.config(label="Volume " + v_M)
        if self.player and not self._stopped:
            # .audio_set_volume returns 0 if success, -1 otherwise,
            # e.g. if the player is stopped or doesn't have media
            if self.player.audio_set_volume(vol):  # and self.player.get_media():
                self.showError("Failed to set the volume: %s." % (v_M,))

    def showError(self, message):
        """Display a simple error dialog.
        """
        self.OnStop()
        showerror(self.parent.title(), message)
