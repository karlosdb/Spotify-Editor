import tkinter as tk
import tkinter.ttk as ttk
import keyboard
import config


# Karlos Boehlke 2020

# this is a simple GUI controller for the core console app
# it only sends virtual keypresses for the purpose of not having to remember the
# console app hotkeys. This is meant to just be run alongside the console app
# if you want to have a GUI controller
# This has to be launched separately and alongside the main.py file

# object for the gui
class GUI:
    # root for the tkinter object
    master = None

    def __init__(self, master=None):
        self.master = master
        # build ui
        self.mainwindow = ttk.Frame(self.master)
        self.title = ttk.Label(self.mainwindow)
        self.title.config(padding='15', text='Spotify Editor')
        self.title.pack(side='top')
        self.buttons = ttk.Frame(self.mainwindow)
        self.add = ttk.Frame(self.buttons)
        self.add_track = ttk.Button(self.add)
        self.add_track.config(text='ADD')
        self.add_track.pack(side='top')
        self.add_track.configure(command=self.add_track_click)
        self.add_and_skip = ttk.Button(self.add)
        self.add_and_skip.config(text='ADD+SKIP')
        self.add_and_skip.pack(side='top')
        self.add_and_skip.configure(command=self.add_and_skip_click)
        self.add.config(height='30', padding='5', width='100')
        self.add.pack(side='left')
        self.skip_delete = ttk.Frame(self.buttons)
        self.skip_track = ttk.Button(self.skip_delete)
        self.skip_track.config(text='SKIP')
        self.skip_track.pack(ipady='3', side='top')
        self.skip_track.configure(command=self.skip_track_click)
        self.delete_track = ttk.Button(self.skip_delete)
        self.delete_track.config(text='DELETE')
        self.delete_track.pack(side='top')
        self.delete_track.configure(command=self.delete_track_click)
        self.skip_delete.config(height='30', width='100')
        self.skip_delete.pack(side='left')
        self.move = ttk.Frame(self.buttons)
        self.move_track = ttk.Button(self.move)
        self.move_track.config(text='MOVE')
        self.move_track.pack(side='top')
        self.move_track.configure(command=self.move_track_click)
        self.move_and_skip = ttk.Button(self.move)
        self.move_and_skip.config(text='MOVE+SKIP')
        self.move_and_skip.pack(side='top')
        self.move_and_skip.configure(command=self.move_and_skip_click)
        self.move.config(height='30', padding='5', width='100')
        self.move.pack(side='right')
        self.buttons.config(height='200', width='200')
        self.buttons.pack(side='top')
        self.frame_17 = ttk.Frame(self.mainwindow)
        self.exit = ttk.Button(self.frame_17)
        self.exit.config(text='exit')
        self.exit.pack(pady='5', side='top')
        self.exit.configure(command=self.exit_click)
        self.frame_17.config(height='30', width='200')
        self.frame_17.pack(side='bottom')
        self.mainwindow.config(height='200', width='200')
        self.mainwindow.pack(side='top')

        # Main widget
        self.mainwindow = self.mainwindow

    # all definitions for the button presses -- sends the keypress corresponding to the function in the console app
    def add_track_click(self):
        keyboard.press_and_release(config.add_track_hotkey)

    def add_and_skip_click(self):
        keyboard.press_and_release(config.add_and_skip_track_hotkey)

    def skip_track_click(self):
        keyboard.press_and_release(config.skip_track_hotkey)

    def delete_track_click(self):
        keyboard.press_and_release(config.delete_track_hotkey)

    def move_track_click(self):
        keyboard.press_and_release(config.move_track_hotkey)

    def move_and_skip_click(self):
        keyboard.press_and_release(config.move_and_skip_track_hotkey)

    def exit_click(self):
        keyboard.press_and_release(config.exit_program_hotkey)
        self.master.quit()

    # run the GUI applicatoin
    def run(self):
        self.mainwindow.mainloop()


# initialize the tkinter object and start the app
root = tk.Tk()
# set title of app
root.title("Controller")
app = GUI(root)
app.run()
