import spotipy
from spotipy.oauth2 import SpotifyOAuth
import keyboard
from collections import namedtuple
import time
import re
import pickle
import config

# Karlos Boehlke 2020

# get information for the spotify api
# scope of api, meaning what permissions are needed for the app to work
scope = "user-read-playback-state user-modify-playback-state playlist-modify-private playlist-modify-public"
# create api object using application client IDs and scope, allows user to log in in the browser
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                               client_secret=config.client_secret,
                                               redirect_uri="https://www.google.com/",
                                               scope=scope))

# simple tuple object for a playlist name and id
PlaylistNameAndId = namedtuple('PlaylistNameAndId', ['name', 'id'])

# simple tuple object to hold a current track info that is relevant to this app
CurrentTrackInfo = namedtuple('CurrentTrackInfo',
                              ['artist', 'trackName', 'trackId', 'contextPlaylistId', 'contextPlaylistName'])

# playlists that are owned by the user, to be added to in parseUserPlaylists
userOwnedPlaylists = []

# all playlists that the user has saved
userPlaylists = sp.current_user_playlists(limit=50)


# look through all playlists that the user has saved and add ones that the user owns to userOwnedPlaylists
def parseUserPlaylists():
    # loop through the userPlaylists objects
    for i, playlist in enumerate(userPlaylists['items']):
        # check if the owner of the playlist is the same as the current user
        if (playlist['owner']['id'] == sp.current_user()['id']):
            # add the name and id of playlist to userOwnedPlaylists
            userOwnedPlaylists.append(PlaylistNameAndId(playlist['name'], userPlaylists['items'][i]['id']))


# print out the user owned playlists in a numbered fashion
def printUserPlaylists():
    for i in range(len(userOwnedPlaylists)):
        print("%d %s" % (i, userOwnedPlaylists[i].name))


# retrieve and print out the user's currently playing song
def printCurrentlyPlayingSong():
    # retrieve current track info
    currentTrack = getCurrentTrackInfo()
    # if current track could be recieved, print artist and name
    if currentTrack != None:
        print("Currently playing: " + currentTrack.artist + " - " + currentTrack.trackName)


# retrieve current track info from api and parse it into the current track tuple object
def getCurrentTrackInfo():
    try:
        # get the current track object from the api
        track = sp.current_user_playing_track()
        # get artist name
        artist = track['item']['artists'][0]['name']
        # get track name
        trackName = track['item']['name']
        # get track id
        trackId = [track['item']['uri']]

        # get uri for the 'context' of the track, meaning who's playing it and from what playlist it's being played
        contextUri = track['context']['uri']
        # parse out just the current playlist's id
        contextPlaylistId = re.sub(r'spotify:.*playlist:', '', contextUri)
        # retrieve the playlist object corresponding to the playlist id
        contextPlaylist = sp.playlist(playlist_id=contextPlaylistId)
        # take the name from the playlist object
        contextPlaylistName = contextPlaylist['name']

        # return all relevant found info as a currenttrackinfo tuple
        return CurrentTrackInfo(artist, trackName, trackId, contextPlaylistId, contextPlaylistName)

    # if the track cannot be found, return None
    except:
        return None


# add the currently playing song to a playlist determined by an inputted playlist number
# optional param to skip current song after adding
def addSong(playlistNum=0, next=False):
    # get current track info
    currentTrack = getCurrentTrackInfo()

    # print what is being added and where to
    print(f'\nAdding {currentTrack.trackName} by {currentTrack.artist} to {userOwnedPlaylists[playlistNum].name}')

    # add the currently playing song to the specified playlist
    sp.playlist_add_items(userOwnedPlaylists[playlistNum].id, currentTrack.trackId)

    # if the next param is True, skip to next track
    if (next): sp.next_track()

    # wait one second then display the currently playing song
    time.sleep(1)
    printCurrentlyPlayingSong()


# 'move' the currently playing song, either to the specified playlist, or straight to the trash with the 'delete' param
# optional 'next' param skips song after moving
def moveSong(playlistNum=0, next=False, delete=False):
    # get current track info
    currentTrack = getCurrentTrackInfo()

    # if the action is not to just delete the song, add the song to the specified playlist
    if (delete == False):
        print(
            f'\nMoving {currentTrack.trackName} to {userOwnedPlaylists[playlistNum].name} from {currentTrack.contextPlaylistName}')
        sp.playlist_add_items(userOwnedPlaylists[playlistNum].id, currentTrack.trackId)

    # try to remove the currently playing song from the playlist that it is playing from
    try:
        sp.playlist_remove_all_occurrences_of_items(currentTrack.contextPlaylistId, currentTrack.trackId)
        if (delete): print(
            f'removing all occurences of {currentTrack.trackName} from {currentTrack.contextPlaylistName}')
    # if the song can't be removed, it's because it's from a playlist that the user does not own
    except:
        print("can't move song from playlist that you don't own, song was only added instead")

    # if the next param is true, skip to next track
    if (next): sp.next_track()

    # wait one second then print currently playing song
    time.sleep(1)
    printCurrentlyPlayingSong()


# create a hotkey to 'focus' on a playlist, meaning that this playlist will be the one being added to
# with the move/add functions.
def createFocusHotkey(hotkey, playlistNum):
    keyboard.add_hotkey(hotkey, lambda: focusPlaylist(playlistNum))
    print(f'Added hotkey "{hotkey}" to focus playlist {userOwnedPlaylists[int(playlistNum)].name}')


# retrieve saved playlist numbers and put them into a list and return that list, if possible
def retrievePlaylistNums():
    try:
        with open("playlistNums.dump", "rb") as input:  # open data file

            # parse the data file into the playlistNums list
            playlistNums = pickle.load(input)

            # return the list
            return playlistNums

        # if there isn't a file just print that there isn't a file and return an empty list
    except FileNotFoundError:
        print("no file found, please just input selection")
        return None


# have the user select playlists to be in the pool for being 'focused'/edited
def choosePlaylists():
    while True:
        try:
            # ask the user for input
            playlistNums = input(
                "input the playlists you would like to focus on by typing their numbers separated by a space\n"
                "if you want to use the same playlists as last time, just press enter.\n").split()

            # if the user just presses enter without typing anything, get playlistNums from the saved file
            if (playlistNums == []):
                # retrieve playlist numbers from file
                playlistNums = retrievePlaylistNums()
                print("retrieving saved playlist selections...")

            # check to make sure numbers are within range
            for i in range(len(playlistNums)):
                playlistNum = playlistNums[i]
                if (int(playlistNum) < 0 or int(playlistNum) > len(userOwnedPlaylists) - 1):
                    print("playlist numbers are not in the range of possible playlists")
                    raise Exception()

            if (len(playlistNums) > 10):
                print("cannot have more than 10 focus options!")
                raise Exception()

            # create hotkeys for each playlist
            for i in range(len(playlistNums)):
                playlistNum = playlistNums[i]
                createFocusHotkey(str(i + 1), playlistNum)

                # save selection to file for retrieval next open
            with open("playlistNums.dump", "wb") as output:
                pickle.dump(playlistNums, output, pickle.HIGHEST_PROTOCOL)

            break
        # if there are any errors in getting the playlist numbers, restart the process
        except:

            print("playlist numbers were not parsable, please try again.\n")


# "focus" on a playlist, make this playlist the playlist that gets editied from the functions of the program
def focusPlaylist(playlistNum):
    focusedPlaylist = int(playlistNum)

    # print what playlist is being focused
    print(f'\nfocusing playlist {playlistNum} - {userOwnedPlaylists[focusedPlaylist].name}')

    # reassign all the hotkeys for adding, adding + skip, moving, moving + skip to the focused playlist
    keyboard.clear_hotkey(config.add_track_hotkey)
    keyboard.add_hotkey(config.add_track_hotkey, lambda: addSong(focusedPlaylist))

    keyboard.clear_hotkey(config.add_and_skip_track_hotkey)
    keyboard.add_hotkey(config.add_and_skip_track_hotkey, lambda: addSong(focusedPlaylist, next=True))

    keyboard.clear_hotkey(config.move_track_hotkey)
    keyboard.add_hotkey(config.move_track_hotkey, lambda: moveSong(focusedPlaylist))

    keyboard.clear_hotkey(config.move_and_skip_track_hotkey)
    keyboard.add_hotkey(config.move_and_skip_track_hotkey, lambda: moveSong(focusedPlaylist, next=True))


# skip track and display next song
def skipTrack():
    sp.next_track()
    time.sleep(1)
    # print('\n')
    printCurrentlyPlayingSong()


# prints out the guide for hotkey controls
def printHelp():
    print(
        f'''
    {config.add_track_hotkey}: add song to focused playlist
    {config.add_and_skip_track_hotkey}: add song to focused playlist and skip to next song
    {config.skip_track_hotkey}: skip track
    {config.move_track_hotkey}: move song to focused playlist
    {config.move_and_skip_track_hotkey}: move song to focuesd playlist and skip
    {config.delete_track_hotkey}: DELETE song from current playlist
    {config.exit_program_hotkey.upper()}: EXIT program
    
    Change Focus by pressing the numbers assigned to each playlist when choosing playlists! 
    Numbers start from 1
''')
    printCurrentlyPlayingSong()


# set default keybinds, which all act with the first playlist as the focus, these get reassigned when the user chooses focus
keyboard.add_hotkey(config.add_track_hotkey, lambda: addSong())  # add song
keyboard.add_hotkey(config.add_and_skip_track_hotkey, lambda: addSong())  # add song + skip
keyboard.add_hotkey(config.skip_track_hotkey, lambda: skipTrack())  # skip track
keyboard.add_hotkey(config.move_track_hotkey, lambda: moveSong())  # move song to focused playlist
keyboard.add_hotkey(config.move_and_skip_track_hotkey, lambda: moveSong(next=True))  # move song and skip

keyboard.add_hotkey(config.delete_track_hotkey,
                    lambda: moveSong(next=True, delete=True))  # DELETE SONG FROM CURRENT PLAYLIST
keyboard.add_hotkey('ctrl+h', lambda: printHelp())  # print out the guide for the hotkeys
