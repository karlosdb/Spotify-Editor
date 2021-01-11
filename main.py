from core import *

# Karlos Boehlke 2020

# this just runs some of the core functions of the core console app
# you want to run this file, alone with controller.py if you want to click buttons instad of using the hotkeys

# parse and store the user owned playlists
parseUserPlaylists()
# print the user owned playlists
printUserPlaylists()
# choose the 'focusable' playlists
choosePlaylists()

# print controls for showing hotkeys and exiting
print(f"PRESS {config.help_print_hotkey.upper()} TO SHOW HOTKEYS\nPRESS {config.exit_program_hotkey.upper()} TO EXIT\n")

# print the currently playing song
printCurrentlyPlayingSong()

# exit the program on press of the escape key
keyboard.wait(config.exit_program_hotkey)
