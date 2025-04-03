import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import os
import json
import time  # Importing time for potential delay in track addition

# Definizione della classe `colors` per il colore del testo
class colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'

    @staticmethod
    def enable_windows_ansi():
        if os.name == 'nt':
            os.system('')

# Abilita ANSI se su Windows
colors.enable_windows_ansi()

# Funzioni per la gestione dei log
def log_print(message):
    print(f"{colors.CYAN}[LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}{colors.RESET}")

def success_print(message):
    print(f"{colors.GREEN}[SUCCESSO] {message}{colors.RESET}")

def error_print(message):
    print(f"{colors.RED}[ERRORE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}{colors.RESET}")

# Caricamento configurazione da file JSON
CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        error_print(f"Errore nel caricamento del file di configurazione: {e}")
        return {}

config = load_config()
credentials_file = config.get("credentials_file", "apikey_spotify.txt")  # Percorso predefinito
backup_path = config.get("backup_path", "playlist_backup.json")  # Percorso predefinito

def load_credentials(filename):
    try:
        credentials = {}
        with open(filename, 'r') as file:
            for line in file:
                name, value = line.strip().split('=')
                credentials[name] = value
        success_print("Credenziali caricate correttamente.")
        return credentials
    except Exception as e:
        error_print(f"Errore durante il caricamento delle credenziali: {e}")
        return {}

credentials = load_credentials(credentials_file)
client_id_key = credentials.get('client_id')
client_secret_key = credentials.get('client_secret')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id_key,
    client_secret=client_secret_key,
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-public playlist-modify-private",
    requests_timeout=30
))

def get_playlist_tracks(playlist_id):
    try:
        log_print("Recupero dei brani della playlist in corso...")
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
            
        success_print("Brani della playlist recuperati con successo.")
        return tracks
    except Exception as e:
        error_print(f"Errore durante il recupero della playlist: {e}")
        return None

def save_track_ids_to_json(tracks, filename=backup_path):
    try:
        if os.path.exists(filename):
            os.remove(filename)
            log_print(f"File di backup esistente '{filename}' rimosso.")

        track_ids = [track['track']['id'] for track in tracks]
        with open(filename, 'w') as file:
            json.dump(track_ids, file)
        
        success_print(f"Backup degli ID delle tracce salvato in '{filename}'")
    except Exception as e:
        error_print(f"Errore durante il salvataggio degli ID delle tracce: {e}")

def remove_duplicates(tracks):
    log_print("Rimozione dei duplicati dalla playlist...")
    unique_tracks = []
    seen = set()
    for track in tracks:
        artist = track['track']['artists'][0]['name']
        album = track['track']['album']['name']
        title = track['track']['name']
        track_id = (artist, album, title)
        if track_id not in seen:
            seen.add(track_id)
            unique_tracks.append(track)
    success_print("Duplicati rimossi.")
    return unique_tracks

def sort_tracks_by_artist_album(tracks):
    log_print("Ordinamento dei brani in base ad artista e album...")
    sorted_tracks = sorted(tracks, key=lambda track: (track['track']['artists'][0]['name'], track['track']['album']['name']))
    success_print("Brani ordinati con successo.")
    return sorted_tracks

def clear_playlist(playlist_id):
    try:
        sp.playlist_replace_items(playlist_id, [])  # Svuota la playlist sostituendo i brani con un elenco vuoto
        success_print("Playlist svuotata con successo.")
    except Exception as e:
        error_print(f"Errore durante la pulizia della playlist: {e}")

def update_playlist(playlist_id, sorted_tracks):
    try:
        for track in sorted_tracks:
            track_id = track['track']['id']
            sp.playlist_add_items(playlist_id, [track_id])  # Aggiungi un brano alla volta
            log_print(f"Brano aggiunto: {track['track']['name']} di {track['track']['artists'][0]['name']}")
            time.sleep(1)  # Aggiungi un piccolo ritardo tra le aggiunte per rispettare i limiti di richiesta
        success_print("Playlist aggiornata con i brani ordinati.")
    except Exception as e:
        error_print(f"Errore durante l'aggiornamento della playlist: {e}")

def display_sorted_playlist(tracks):
    for track in tracks:
        artist = track['track']['artists'][0]['name']
        album = track['track']['album']['name']
        title = track['track']['name']
        print(f"Artista: {artist} | Album: {album} | Titolo: {title}")

def main():
    playlist_id = input("Inserisci il codice ID della playlist: ")
    tracks = get_playlist_tracks(playlist_id)
    
    if tracks is None:
        error_print("Playlist non trovata o errore di connessione.")
        return

    save_track_ids_to_json(tracks)
    tracks = remove_duplicates(tracks)
    sorted_tracks = sort_tracks_by_artist_album(tracks)
    display_sorted_playlist(sorted_tracks)
    clear_playlist(playlist_id)
    update_playlist(playlist_id, sorted_tracks)  # Aggiorna la playlist uno per uno
    print("\nOrdinamento e aggiornamento della playlist completati!")

if __name__ == "__main__":
    main()
