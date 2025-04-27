import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, Listbox, END
import pygame

# Initiera pygame mixer
pygame.mixer.init()

class SimpleSpotify:
    def __init__(self, root):
        self.root = root
        self.root.title('Väldigt Enkel Musikspelare')
        self.music_folder = ''
        self.songs = []
        self.filtered_songs = []
        self.playlists = {}
        self.current_playlist = None
        self.current_song = None

        # GUI
        self.create_widgets()

    def create_widgets(self):
        # Välj mapp-knapp
        self.folder_btn = tk.Button(self.root, text='Välj musikmapp', command=self.choose_folder)
        self.folder_btn.pack(pady=5)

        # Sökfält
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.update_filter)
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var, width=40)
        self.search_entry.pack(pady=5)

        # Lista med låtar
        self.song_listbox = Listbox(self.root, width=50, height=15)
        self.song_listbox.pack(pady=5)
        self.song_listbox.bind('<Double-Button-1>', self.play_selected_song)

        # Spela-knapp
        self.play_btn = tk.Button(self.root, text='Spela vald låt', command=self.play_selected_song)
        self.play_btn.pack(pady=5)

        # Spellistor
        self.playlist_frame = tk.Frame(self.root)
        self.playlist_frame.pack(pady=5)
        self.playlist_label = tk.Label(self.playlist_frame, text='Spellistor:')
        self.playlist_label.pack(side=tk.LEFT)
        self.playlist_listbox = Listbox(self.playlist_frame, width=20, height=5)
        self.playlist_listbox.pack(side=tk.LEFT)
        self.playlist_listbox.bind('<<ListboxSelect>>', self.select_playlist)
        self.add_playlist_btn = tk.Button(self.playlist_frame, text='+', command=self.add_playlist)
        self.add_playlist_btn.pack(side=tk.LEFT, padx=5)
        self.add_to_playlist_btn = tk.Button(self.playlist_frame, text='Lägg till i spellista', command=self.add_to_playlist)
        self.add_to_playlist_btn.pack(side=tk.LEFT)

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.music_folder = folder
            self.load_songs()

    def load_songs(self):
        self.songs = [f for f in os.listdir(self.music_folder) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
        self.songs.sort()
        self.update_filter()

    def update_filter(self, *args):
        query = self.search_var.get().lower()
        self.filtered_songs = [s for s in self.songs if query in s.lower()]
        self.song_listbox.delete(0, END)
        for song in self.filtered_songs:
            self.song_listbox.insert(END, song)

    def play_selected_song(self, event=None):
        selection = self.song_listbox.curselection()
        if not selection:
            messagebox.showinfo('Info', 'Välj en låt att spela!')
            return
        song = self.filtered_songs[selection[0]]
        song_path = os.path.join(self.music_folder, song)
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.current_song = song
        except Exception as e:
            messagebox.showerror('Fel', f'Kunde inte spela låten: {e}')

    def add_playlist(self):
        name = simpledialog.askstring('Ny spellista', 'Namn på spellista:')
        if name and name not in self.playlists:
            self.playlists[name] = []
            self.playlist_listbox.insert(END, name)

    def select_playlist(self, event=None):
        selection = self.playlist_listbox.curselection()
        if selection:
            name = self.playlist_listbox.get(selection[0])
            self.current_playlist = name
            self.show_playlist(name)

    def show_playlist(self, name):
        self.song_listbox.delete(0, END)
        for song in self.playlists[name]:
            self.song_listbox.insert(END, song)
        self.filtered_songs = self.playlists[name]

    def add_to_playlist(self):
        if not self.current_playlist:
            messagebox.showinfo('Info', 'Välj en spellista först!')
            return
        selection = self.song_listbox.curselection()
        if not selection:
            messagebox.showinfo('Info', 'Välj en låt att lägga till!')
            return
        song = self.filtered_songs[selection[0]]
        if song not in self.playlists[self.current_playlist]:
            self.playlists[self.current_playlist].append(song)
            messagebox.showinfo('Info', f'Lade till {song} i {self.current_playlist}!')

if __name__ == '__main__':
    root = tk.Tk()
    app = SimpleSpotify(root)
    root.mainloop() 