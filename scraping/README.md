# League of Legends Data Extraction (API + Scraping)

## Descrizione

Script Python per l'estrazione, filtraggio, normalizzazione, formattazione ed esportazione dei dati relativi ai campioni di League of Legends, tramite API ufficiali dell'azienda Riot Games e scraping di tipo statico.

Il codice è stato volutamente unito in un solo file per mostrare lo script. Realisticamente parlando i singoli blocchi di codice come le classi o la funzione che crea il logger verrebbero inserite in file separati e, successivamente, importati come moduli per una miglior scalabilità, manutenzione e leggibilità.

## Obiettivi

- centralizzare l'accesso ai dati tramite sessione per gestire richieste HTTP in modo persistente
- gestire una o più lingue contemporaneamente
- consentire l'estrazione anche di dati relativi a versioni precedenti del gioco
- pulire i dati ottenuti in risposta dalle richieste
- esportazione finale dei dati in file JSON strutturati per riusabilità degli stessi
- log dettagliato di tutto in un file esterno e in console solo errori per una revisione più rapida del problema

Lo script è pensato per essere utilizzato poche volte e in modo completo, per questo motivo alcune parti possono risultare molto specifiche e poco scalabili.

## Tecnologie 

- requests
- BeautifulSoup
- logging 
- pathlib 
- json
- re

## Come usarlo

Scaricare la cartella o clonare repository nella propria cartella di lavoro con il seguente comando:

``` bash
git clone https://github.com/Matty-Coding/Python-WebApp
```

Creare virtualenv nella cartella di lavoro:

``` bash
# con virtualenv (pip install virtualenv) 
virtualenv <nome virtualenv>

# con venv di python default
venv <nome virtualenv>
```

Installare i pacchetti necessari al funzionamento dello script:
``` bash
pip install -r requirements.txt
```

### Eseguire

Creare un nuovo file nella cartella scraping clonata/scaricata e scrivere il seguente blocco di codice.
``` python
from scraping.extracting import Extract

api = Extract()
api.data_champs_to_json(countries=("italy",))
```

Il file di log è consultabile in scraping/logs.
---

### Lingua

Per scegliere la lingua in cui scaricare i dati consultare il file [languages.json](/scraping/data/languages.json) situato in scraping/data, in particolar modo la sezione sotto la voce `language`.

Inserire le lingue desiderate come mostrate nel codice soprastante.

--- 

### Versione 

Di default vengono scaricati i dati relativi all'ultima versione del gioco presente nelle API ufficiali di Riot Games.

Per visualizzare le versioni del gioco utilizzare il metodo `get_versions` senza parametri. 
Per cambiare la versione sceglierne una e cambiare l'attributo della classe come segue:
```python
api._patch = "15.24.1"
```

Eseguire nuovamente lo script.
