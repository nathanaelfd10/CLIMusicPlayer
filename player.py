import os
from pygame import mixer
from color import color_blue, color_yellow, color_green, color_green2, color_red, color_red2, color_end, color_header, font_bold
import csv
import pandas as pd
import ast


class Player(object):

    def __init__(self):
        self.playlist_path = "playlist/playlist.csv"
        self.song_list = self.scan_for_songs()
        self.playing_state = None
        self.current_song = ""
        self.previous_list = []
        self.playlist = []
        self.playlist_name = "None loaded"
        self.volumeVal = 0.7
        self.initMixer()
        self.playerMain()

    def playerMain(self):
        self.next()
        mixer.music.set_volume(self.volumeVal)
        self.play()

        while True:
            self.clear()
            print(color_red + '\n\n\nNow Playing:' + color_end, color_header + self.current_song + color_end)
            print("Current volume:" + color_green, int(self.volumeVal*100), color_end + "\n")
            if self.playing_state == True:
                print('Type',  color_red + 'P', color_end + 'to', color_red + 'pause' + color_end)
            elif self.playing_state == False:
                print('Type', color_green + 'P', color_end + 'to', color_green + 'resume' + color_end)

            print("\nType the following keywords to perform an action: ")
            print("'Next' to play the next song")
            print("'Open' to play a select song")
            print("'Playlist' to open the playlist menu")
            print("'Volume' to adjust the volume.")
            print("'Reload' to rescan all songs in directory")
            print("'Stop' to stop")

            x = input("  ")
            if self.playing_state == True:
                if x.upper() == 'P':
                    mixer.music.pause()
                    self.playing_state = False
                    
            elif self.playing_state == False:
                if x.upper() == 'P':
                    mixer.music.unpause()
                    self.playing_state = True 

            if x.upper() == 'S' or x.upper() == 'STOP':
                self.stop()
                break
            elif x.upper() == 'NEXT':
                self.next()
            elif x.upper() == 'OPEN':
                self.open()
            elif x.upper() == 'PLAYLIST':
                self.playlistMain()
            elif x.upper() == 'R' or x.upper() == 'RELOAD':
                self.reloadSongs()
            elif x.upper() == 'VOL' or x.upper() == 'VOLUME':
                self.volumeControl()

    def initMixer(self):
        mixer.pre_init()
        mixer.init(192000, -16, 2, 2042)            

    def volumeControl(self):
        while True:
            try:
                volInput = int(input("Enter volume (1-100): "))
                break
            except:
                print("Please enter a valid number.")
                
        self.volumeVal = volInput / 100
        mixer.music.set_volume(self.volumeVal)
        print("Volume has been set to", self.volumeVal)
    
    def reloadSongs(self):
        self.song_list = self.scan_for_songs()
        self.playlist = {}
        self.playlist_name = "None loaded"

    def playlistMain(self):
         self.load_playlist() 
         while True:
            self.clear()
            print("\n\n\n\n\nYou're currently inside the playlist menu.")
            print("Current playlist: " + color_header + self.playlist_name + color_end)
            print(color_red + 'Now Playing:' + color_end, color_header + self.current_song + color_end + "\n")
            print("Type 'new' to create a playlist.")
            print("Type 'open' to open a playlist.")
            print("Type 'open song' to play a select song")
            print("Type 'next' to play the next song.")
            print("Type 'quit' to return to main menu.")

            x = input("  ")
            if x.upper() == 'NEW':
                self.create_playlist()
            elif x.upper() == 'QUIT':
                break
            elif x.upper() == 'OPEN':
                self.open_playlist()
            elif x.upper() == 'OPEN SONG':
                self.open()
            elif x.upper() == 'NEXT':
                self.next()

    def create_playlist(self):
        song_found = self.scan_for_songs()
        playlist_name = input("Enter a playlist name: ")
        playlist_content = []
        self.clear()

        # self.clear()
        while True:
            try:
                print("======== AVAILABLE SONGS ========")
                for x, song in enumerate(song_found):
                    print(str(x+1)+'.', song)
                select_song = int(input("Enter " + color_red + "0" + color_end + " to save.\nSelect a song to add (1-" + str(x+1) + "): "))
                self.clear()

            except:
                print("Please enter a valid number.")

            if select_song == 0:
                    print(self.playlist)
                    self.playlist[playlist_name] = playlist_content
                    print(self.playlist)
                    self.save_to_playlist()
                    print('Playlist ' + playlist_name +  ' saved')
                    self.load_playlist()
                    # self.load_playlist()
                    # self.playerMain()
                    break

            elif select_song in range(1, x+2):
                print('Song added:')
                for y, song in enumerate(song_found):
                    if int(select_song) == int(y+1):
                        playlist_content.append(song)
                        for z, song in enumerate(playlist_content):
                            print(str(z+1)+'.' + str(song))

    def open_playlist(self):
            self.clear()
            print("\n\n\n\n\n====== Playlist ======")
            for x, playlist in enumerate(self.playlist):
                print(str(x+1)+".", playlist)

            while True:
                try:
                    playlist_chosen = int(input("Enter " + color_red + "0" + color_end + " to cancel.\nSelect a playlist to open (1-" + str(x+1) + "): "))
                except:
                    print("Please enter a valid number.")
                if playlist_chosen == 0:
                    break
                elif playlist_chosen in range(1, x+2):
                    for y, playlist in enumerate(self.playlist):
                        if int(playlist_chosen) == int(y+1):
                            self.playlist_name = playlist
                            load_playlist_str = self.playlist.get(playlist)
                            self.song_list = self.eval(load_playlist_str)
                            self.current_song = self.song_list[0]
                            mixer.music.load(str(self.current_song))
                            self.play()
                    break
    
    def load_playlist(self):
        try:
            self.playlist = pd.read_csv(self.playlist_path, header=None, index_col=0, squeeze=True).to_dict()
        except:
            self.playlist = {}
            try:
                os.mkdir('playlist')
            except FileExistsError:
                pass
            with open(self.playlist_path, 'w') as playlist_file:
                pass
            # file = 
            # file.close()
            print("You haven't created a playlist yet, please create a new one.")
            self.create_playlist()

    def save_to_playlist(self):
        with open(self.playlist_path, "w") as playlist_file:
            writer = csv.writer(playlist_file)
            for key, value in self.playlist.items():
                writer.writerow([key, value])

    def open(self):
        self.clear()
        print("\n\n")
        print("========== Select a song to play ==========")
        for x, song in enumerate(self.song_list):
            print(str(x+1)+'.', song)

        while True:
            try:
                select_song = int(input("Enter " + color_red + "0" + color_end + " to cancel.\nSelect a song (1-" + str(x+1) + "): "))
                break
            except:
                print("Please enter a valid number.")

        if select_song == 0:
            pass
        else:
            for x, song in enumerate(self.song_list):
                if x+1 == int(select_song):
                    print(song)
                    self.current_song = song
                    mixer.music.load(self.current_song)
                    self.play()
    
    def clear(self):
        clear = lambda: os.system('cls')
        clear()

    def scan_for_songs(self):
        songs_found = []
        for file in os.listdir("music"):
            if file.endswith(".mp3"):
                songs_found.append(os.path.join("music/"+file))
        return songs_found

    def play(self):
        mixer.music.play()
        self.playing_state = True

    def stop(self):
        mixer.music.stop()
    
    def next(self):
        self.song_list.append(self.song_list[0])
        self.current_song = self.song_list.pop(0)
        mixer.music.load(self.current_song)
        mixer.music.play()

    def eval(self, anon):
        try:
            ev = ast.literal_eval(anon)
            return ev
        except ValueError:
            corrected = "\'" + anon + "\'"
            ev = ast.literal_eval(corrected)
            return ev

    def show_playlist(self):
        for x, playlist in enumerate(self.playlist):
            print(str(x+1)+".", playlist)