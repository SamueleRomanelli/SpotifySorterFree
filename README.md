# 🎵 SpotifySorterFree

**SpotifySorterFree** è uno script **totalmente gratuito** creato da **Samuele Romanelli** che ti permette di creare, aggiornare e ordinare facilmente le playlist pubbliche di **Spotify**. Con questo script, puoi organizzare le tue playlist in modo rapido ed efficiente direttamente dalla tua shell di comando! 🚀

⚠️ **Nota importante:** Attualmente potrebbe essere necessario un **account Spotify Premium** per il corretto funzionamento. Inoltre, è possibile che alcune parti del codice debbano essere aggiornate per funzionare con le ultime modifiche delle API (non è garantito al 100%).

## ✨ Caratteristiche principali
- ✅ **Ordina automaticamente** le playlist pubbliche in base a **artista** e **album**.
- ✅ **Creazione e Aggiornamento** di playlist con la Top 50 dei brani più ascoltati nelle ultime 4 settimane.
- ✅ **Completamente gratuito e open source**.
- ✅ **Facile da usare** grazie alla semplice interfaccia a riga di comando (CLI).
- ✅ **Non modifica i tuoi dati di Spotify**, ma organizza le playlist in modo ordinato.
- ✅ **Configurabile** grazie al file `config.json`.

## 🛠️ Requisiti
- **Python 3.x** installato nel sistema.
- **Un account Spotify** per generare le API Key.
- ⚠️ **Account Spotify Premium (consigliato/attualmente necessario in alcuni casi)**.
- ⚠️ **Possibili aggiornamenti manuali al codice** necessari per compatibilità con le API.
- **Chiavi API di Spotify (Client ID & Client Secret)**.

## ℹ️ Versione Attuale = 2.0.0

---

## 📥 Installazione

**Nota:** Se hai già la versione 1.0.0 prova a installare la v.2.0.0 utilizzando il seguente collegamento:
[Vai al branch v2.0.0](https://github.com/SamueleRomanelli/SpotifySorterFree/tree/v2.0.0)

### 1️⃣ Creare una cartella e clonare il repository

1. Crea una nuova cartella dove vuoi salvare il progetto.

2. Apri il terminale e spostati nella cartella appena creata:

   ```bash
   cd "/percorso/della/cartella/appena/creata"
   ```

3. Clona il repository con il comando:

   ```bash
   git clone https://github.com/SamueleRomanelli/SpotifySorterFree.git
   ```

### 2️⃣ Crea e configura le API di Spotify 🔑

1. Vai su **[Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications)**.

2. Accedi con il tuo account e clicca su **Create an App**.

3. Durante la configurazione dell'app, Assicurati che il **Redirect URI** sia impostato su:
   ```
   http://localhost:8888/callback
   ```

4. Successivamente seleziona che ti serve per **Web Api** e salva app.

5. Dopo aver creato l'app, poi copia **Client ID** e **Client Secret**.

6. Modifica il file `apikey_spotify.txt` e incolla i valori in questo formato:

```txt
client_id=TUO_CLIENT_ID
client_secret=TUO_CLIENT_SECRET
```

### 3️⃣ Installa le dipendenze 📦

Nel Terminale devi essere nella cartella dove si trova il progetto facendo:

```bash
cd /percorso/della/cartella/creata/al/punto1/SpotifySorterFree
```

_per copiare i percorsi giusti conviene fare `tasto destro` sulla cartella in questo caso: `SpotifySorterFree` e cliccare `copia come percorso` infine incollare nel posto indicato:_

Una volta dentro usa il seguente comando per installare le dipendenze richieste:

```bash
pip install -r requirements.txt
```

### 4️⃣ Configura il file `config.json` 🛠

Successivamente devi personalizzare i percorsi dei file necessari modificando `config.json`:

_per copiare i percorsi giusti conviene fare `tasto destro` su per esempio: `apikey_spotify.txt` e cliccare `copia come percorso` infine incollare nel posto indicato:_

```json
{
  "credentials_file": "/percorso/del/file/apikey_spotify.txt",
  "backup_path": "/percorso/del/file/playlist_backup.json"
}
```

Se desideri salvare il backup in una posizione diversa, cambia `backup_path` con il percorso desiderato.

**Nota**: _Inoltre all'interno del file `playlist_backup.json` ci sono gli id delle canzoni della playlist, in modo tale che se lo script dovesse avere conflitti puoi ripristinare il tutto!_

### 5️⃣ Esegui lo script 🎬

Nel Terminale devi essere nella cartella dove si trova lo script facendo:

```bash
cd /percorso/della/cartella/creata/al/punto1/SpotifySorterFree
```

_per copiare i percorsi giusti conviene fare `tasto destro` sulla cartella in questo caso: `SpotifySorterFree` e cliccare `copia come percorso` infine incollare nel posto indicato:_

Una volta dentro avvia lo script con:

```bash
python3 ordina_playlist.py
```
Inserisci l'ID della playlist quando richiesto e lascia che lo script faccia il resto! 🎵

Dalla versione [v2.0.0](https://github.com/SamueleRomanelli/SpotifySorterFree/tree/v2.0.0) puoi usare anche questo script per creare o aggiornare le tue playlist:

```bash
python3 create_playlist.py
```

---

## ❓ Supporto e Feedback
- 📩 **Hai problemi?** Apri un'issue su [GitHub](https://github.com/SamueleRomanelli/SpotifySorterFree/issues).
- ⭐ **Ti piace il progetto?** Lascia una **stella** su GitHub!

---

## 🏆 Badge di Compatibilità
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![CLI Tool](https://img.shields.io/badge/CLI-Tool-informational?logo=terminal&logoColor=white)
![Standalone](https://img.shields.io/badge/Standalone-Yes-green)

