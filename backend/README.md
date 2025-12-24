# Database - Server - Sessioni - Sicurezza 

## Descrizione

### Database

Per il Database, è stato scelto di utilizzare `SQLite` per un progetto locale facilmente estendibile per una produzione ad altri database come `MySQL`.
La creazione del database e successivi aggiornamenti vengono effettuati con il pacchetto `Flask-Migrate`. 

Progettato interamente con __ORM__ (Object-Relational Mapping), in particolare `SQLAlchemy` integrato ai pacchetti del Framework in uso per questo progetto, `Flask`. 

Il database ha la seguente struttura [apri immagine](/app/database/db_structure.png).

La tabella _sessions_ è interamente gestista da `Flask-Session`, le altre sono create tramite `Flask-SQLAlchemy`.
Presentano delle relazioni tra loro e la gestione degli utenti è strettamente collegata grazie al pacchetto `Flask-Login` e la sua classe `UserMixin`.

La tabella _users_ viene creata con campi di ogni tipo, alcuni impostati con valori di default, come la colonna associata alla creazione dell'utente o della sua autenticazione impostata a `False` di default.

La tabella _email\_tokens_ è pensata per gestire l'autenticazione a due fattori tramite codice inviato via mail (Servizio di [`SendGrid`](https://sendgrid.com/en-us) implementato nel progetto con l'omonimo pacchetto Python e API KEY).
Per semplicità di lettura e presentazione viene utilizzata solamente per il _forgot password_.
(In casi reali sarebbe auspicabile gestire in una tabella separata i reset della password.)

### Server
I dati sensibili come token, secretkey e path database vengono gestiti tramite il flusso di `.env`, `python-dotenv`, `config.py`e successivo caricamento della configurazione all'interno dell'oggetto `Flask`.

Non sono caricati da `Git` grazie alla presenza di un file `.gitignore` e di conseguenza non presenti neanche su `GitHub`.
Per una rappresentazione visiva di com'è strutturato il `.env` è caricato nel repository un file `.env.sample` contenente dati fittizi per rendere l'idea.

Il progetto presenta un template di base che viene esteso a tutte le pagine HTML presenti con `Jinja2`.
Lo stile è approssimativo e di poco peso, sviluppato con Bootstrap CDN per un risultato presentabile e poco sforzo, risaltando il __Backend__ effettivo.

Diviso con diverse Blueprint e cartelle/file per una migliore leggibilità, scalabilità e manutenzione.

### Sessioni

Le sessioni vengono gestite da `Flask-Session` che firma i cookie tramite secretkey e memorizza i dati dell'utente in modo criptato.
Non viene gestita la rimozione dei cookie dal browser o la rimozione delle sessioni scadute nel database.
Consigliabile la pulizia tramite linea di comando come da documentazione:

```bash
flask session_cleanup
```



### Sicurezza
La sicurezza copre gli attacchi più comuni:
- __Injection__: Regex nei form di autenticazione, validati esclusivamente lato server (attributo `novalidate`) + ORM (conseguente assenza di query hard-codificate).

- __CSRF__: `Flask-WTF` per gestire i token caricati in ogni form.

- __XSS__: `Jinja2` non ammette autoescaping nei template + `Flask-Talisman` per gestire Content-Security-Policy in modo molto rigido.

- __SSRF__: Il server non presenta possibilità di interagire con URL passati dall'utente e che puntino altrove, pertanto questo tipo di attacco non è possibile.

- __DoS/Brute Force__: `Flask-Limiter` applica dei blocchi generali ad ogni rotta del server e protegge le più delicate come login/reset password con restrizioni severe. (Gestisto tramite cache locale del server, in produzioni si può scalare facilmente a backend come Redis per una persistenza costante.)

Il sistema di blocco limitato è pensato per mostrare all'indirizzo ip bloccato solo la rispettiva pagina con timer di attesa, anche se prova a visualizzare altre rotte manualmente. In modo analogo l'accesso a questa pagina è impedito da qualsiasi ip non risulti bloccato.

## Obiettivi

Backend completo, sicuro e funzionale.

- Database + operazioni CRUD che includono (OOP con Inheritance, Polymorphism, Encapsulation).
- Server con Configurazione anche con dati sensibili, Blueprint separate, Template Base per tutte le pagine.
- Sessioni gestite con facilità sfruttando i pacchetti esistenti approfondendo e configurando il tutto.
- Sicurezza per difendere il server dagli attacchi più comuni integrando e facendo coesistere diverse tecnologie.

Il progetto presenta alcuni punti volutamente non utilizzati, come l'autenticazione dell'utente tramite mail e il reset della password, presentano lo stesso sviluppo, ridondante per un progetto di sola presentazione.

## Tecnologie 

- `python-dotenv`
- `Flask` 
- `Flask-Limiter`
- `Flask-SQLAlchemy` e `SQLAlchemy`
- `Flask-Talisman`
- `Flask-WTF`
- `Flask-Login`
- `Flask-Session`
- `Flask-Migrate`
- `Werzeug`
- `Secrets`
- `Jinja2`
- `HTML`
- `CSS` (`Bootstrap`)
- `JavaScript` (`Bootstrp`)
- `JavaScript`
- `Black` (formattazione)

## Come usarlo

Scaricare la cartella o clonare repository nella propria cartella di lavoro con il seguente comando:

``` bash
git clone https://github.com/Matty-Coding/Python-WebApp
```

Creare un ambiente virtuale nella cartella `backend` con uno dei seguenti comandi:
``` bash
# con virtualenv (pip install virtualenv) 
virtualenv <nome ambiente>

# con venv di python default
python -m venv <nome ambiente>
```

Attivare l'ambiente virtuale:
``` bash
<nome ambiente>\Scripts\activate
```

Installare i pacchetti necessari al funzionamento dello script nell'ambiente virtuale:
``` bash
pip install -r requirements.txt
```

Creare file `.env` con i relativi dati annessi come mostrato nel file [`.env.sample`](/backend/.env.sample).

Inizializzare il database:
``` bash
flask db init
```
``` bash
flask db migrate -m "inizializzazione database"
```
``` bash
flask db upgrade
```

Avviare il server tramite file Python di avvio:
``` bash
python main.py
``` 












