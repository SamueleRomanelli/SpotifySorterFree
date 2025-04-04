import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import os

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

credentials_file = r'C:\Users\Samu\Desktop\Bot_Spotify\Spotify_App\apikey_spotify.txt'

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

# Caricamento delle credenziali
credentials = load_credentials(credentials_file)
client_id_key = credentials.get('client_id')
client_secret_key = credentials.get('client_secret')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id_key,
    client_secret=client_secret_key,
    redirect_uri="http://localhost:8888/callback",
    scope="user-top-read playlist-modify-public playlist-modify-private",
    requests_timeout=30
))

# Funzione per recuperare le canzoni più ascoltate
def get_top_tracks(sp, limit=50):
    try:
        log_print("Recupero delle canzoni più ascoltate...")
        top_tracks = sp.current_user_top_tracks(limit=limit, time_range='short_term')
        track_uris = [track['uri'] for track in top_tracks['items']]
        success_print("Canzoni più ascoltate recuperate con successo.")
        return track_uris
    except Exception as e:
        error_print(f"Errore durante il recupero delle canzoni più ascoltate: {e}")
        return []

# Funzione per creare una playlist
def create_playlist(sp, user_id, playlist_name, track_uris):
    try:
        log_print(f"Creazione della playlist '{playlist_name}'...")
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_uris)
        success_print(f"Playlist '{playlist_name}' creata e popolata con successo!")
    except Exception as e:
        error_print(f"Errore durante la creazione della playlist: {e}")

# Funzione per aggiornare una playlist esistente
def update_playlist(sp, playlist_name, track_uris):
    try:
        # Recupera la lista delle playlist dell'utente
        log_print(f"Controllo della playlist '{playlist_name}'...")
        playlists = sp.current_user_playlists(limit=50)
        playlist_id = None
        
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break
        
        if playlist_id:
            log_print(f"Playlist trovata, aggiornamento in corso...")
            sp.playlist_replace_items(playlist_id=playlist_id, items=track_uris)
            success_print(f"Playlist '{playlist_name}' aggiornata con successo!")
        else:
            error_print(f"Playlist '{playlist_name}' non trovata. Creazione nuova playlist...")
            user_id = sp.current_user()['id']
            create_playlist(sp, user_id, playlist_name, track_uris)
    except Exception as e:
        error_print(f"Errore durante l'aggiornamento della playlist: {e}")

# Flusso principale
def main():
    playlist_name = input("Inserisci il nome della playlist da creare o aggiornare: ").strip()
    if not playlist_name:
        error_print("Il nome della playlist non può essere vuoto.")
        return
    
    # Recupera le canzoni più ascoltate
    track_uris = get_top_tracks(sp)

    # Crea e popola la playlist
    if track_uris:
        update_playlist(sp, playlist_name, track_uris)
    else:
        error_print("Nessuna canzone trovata da aggiungere alla playlist.")
    
    log_print("Playlist creata o aggiornata con successo.")

if __name__ == "__main__":
    main()
