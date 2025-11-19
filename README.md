# Tudù

**Tudù** è una semplice applicazione di **ToDo List** composta da due servizi: un **Backend API** e un **Frontend Web**.

| Componente | Tecnologia | Porta |
| :--- | :--- | :--- |
| **Backend** | FastAPI (Python) + SQLAlchemy (SQLite) | `8000` |
| **Frontend** | Vue.js 3 + Nginx (Static Site) | `8080` |

-----

L'applicazione permette di gestire una lista di attività (tasks):

  * **Aggiungi Task:** Creazione di nuovi task con titolo (obbligatorio) e descrizione (opzionale).
  * **Visualizza Tasks:** Recupero di tutti i task o filtrati per stato di completamento (attivi/completati).
  * **Modifica Task:** Aggiornamento dello stato di completamento (toggle).
  * **Elimina Task:** Rimozione di un task specifico.
  * **Persistenza Dati:** I task vengono salvati in un database **SQLite** (`tudu.db`) gestito da SQLAlchemy.

-----

## Documentazione API

Il backend è sviluppato con **FastAPI** e fornisce automaticamente la documentazione interattiva (OpenAPI/Swagger UI).

Dopo aver avviato il backend (vedi istruzioni sotto), puoi accedere alla documentazione completa:

  * **Swagger UI (Interattiva):** `http://localhost:8000/docs`

-----

## Esecuzione con Docker Compose (Consigliato)

Il modo più rapido per avviare l'intera applicazione completa (sia backend che frontend) è utilizzare **Docker Compose**.

Il file `docker-compose.yaml` definisce due servizi: `api` e `frontend`.

### 1\. Prerequisiti

Assicurati di avere **Docker** e **Docker Compose** installati sul tuo sistema.

### 2\. Avvio

Esegui il comando dalla directory principale del progetto (dove si trova `docker-compose.yaml`):

```bash
docker compose up --build
```

### 3\. Accesso all'Applicazione

  * **Frontend:** `http://localhost:8080`
  * **Backend API (Documentazione):** `http://localhost:8000/docs`

### 4\. Pulizia

Per fermare ed eliminare i container:

```bash
docker compose down
```

-----

## Esecuzione Locale con Virtualenv

Se si preferisce eseguire solo il backend FastAPI in locale (ad esempio per lo sviluppo), si può utilizzare un ambiente virtuale Python.

### 1\. Crea e attiva un Virtual Environment

Dalla cartella principale, crea l'ambiente:

```bash
cd tudu/backend
python -m venv venv
source venv/bin/activate (per Linux o MacOS)
venv\Scripts\activate (per Windows)
```

### 2\. Installa le Dipendenze

Installa i pacchetti necessari per FastAPI e SQLAlchemy:

```bash
pip install -r backend/requirements.txt
```

### 3\. Avvia l'API Backend

```bash
# Avvia il server su http://0.0.0.0:8000
fastapi dev backend/app.py
```

L'API sarà ora accessibile all'indirizzo `http://localhost:8000`.

### 4\. Disattiva l'Ambiente

Quando hai finito, disattiva l'ambiente virtuale:

```bash
deactivate
```

-----

## Esecuzione dei test

Dopo ogni sviluppo è consigliata l'esecuzione dei test per evitare regressioni.

### 1\. Attiva il Virtual Environment

```bash
```
source venv/bin/activate (per Linux o MacOS)
venv\Scripts\activate (per Windows)
```

### 2\. Eseguire i test

```bash
./venv/bin/pytest
```
```
```

