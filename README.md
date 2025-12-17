# Backend

## Database

Gestione del database e operazioni CRUD, partendo da query SQL raw fino all’uso di ORM.

* Linguaggio SQL e query manuali
* Query tramite cursore (`sqlite3`)
* Modellazione e manipolazione dei dati tramite ORM (`SQLAlchemy`, `Flask_SQLAlchemy`)
* Gestione delle migrazioni del database (`Flask_Migrate`)

---

## Server e Autenticazione

Gestione della logica server-side e dei flussi di autenticazione utenti.

* Gestione utenti integrata con database
* Sessioni e autenticazione (`Flask`, `Flask_Login`, `Flask_Session`)

---

## Server e Sicurezza

Implementazione di misure di sicurezza di base per applicazioni web.

* Protezione da attacchi comuni e abuso delle richieste (`Flask_Limiter`, `Flask_Wtf`)
* Gestione sicura delle password e delle utility critiche (`Werkzeug`)

---

## Web Scraping

Estrazione di dati da fonti esterne tramite scraping statico e dinamico.

* Scraping statico con `requests` e `BeautifulSoup`
* Scraping dinamico tramite `Selenium` e browser driver

---

## File Handling

Gestione, trasformazione ed esportazione dei dati.

* Lettura e scrittura di file (`CSV`, `JSON`)
* Interazione con il file system (`os`, `sys`, `pathlib`)

---

## Gestione delle variabili d’ambiente

Configurazione e utilizzo sicuro di chiavi sensibili (es. API_KEY).

* Utilizzo di file `.env`
* Caricamento delle variabili tramite file di configurazione (`python-dotenv`, `config.py`)

---

# Frontend

## HTML

Struttura dei template e rendering server-side.

* HTML semantico e accessibilità di base
* Rendering dei dati dal backend (`Jinja2`)
* Integrazione con JavaScript per contenuti dinamici

---

## CSS

Costruzione di interfacce moderne e responsive.

* Approccio mobile-first
* Layout responsivi
* Utilizzo di CSS utility-first tramite `Tailwind`

---

## JavaScript

Interazione client-side e comunicazione con il backend.

* Manipolazione del DOM (es. toggle di classi, interazioni UI)
* Fetch di dati dal server tramite API
