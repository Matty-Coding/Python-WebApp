# Frontend HTML CSS e JavaScript (No Framework)

## Descrizione

Pagina Web statica che mostra dati relativi al gioco League of Legends di [Riot Games](https://www.riotgames.com/it).

I dati sono stati precedentemente lavorati (per maggiori info [cliccare qui](/scripting/README.md)), fino all'ottenimento di un `JSON` personalizzato visualizzabile in [assets](/frontend/assets/united_kingdom_data.json).

La struttura `HTML` è scritta in modo semanticamente strutturato e minimale, lasciando tutto il caricamento dinamico esclusivamente ai vari script scritti in `JavaScript`.

Nel `<footer>` sono presenti dei link di riferimento all'autore della pagina e all'azienda che mette a disposizione i dati rispettando la loro privacy e riservando a loro i diritti dei contenuti. Tali link hanno due attributi:
- `noopener` che impedisce alla nuova pagina aperta di accedere e manipolare il `DOM`;
- `noreferrer` che non invia informazioni sulla pagina originaria.

Entrambi garantiscono _privacy_ e _sicurezza_ poichè i link portano a delle pagine esterne con l'attributo `_blank`.

Gli `<script>` vengono importati come file esterni con l'attributo `defer`, esso garantisce che vengano eseguiti in modo parallelo al _loading_ del DOM evitando che i vari `querySelector` non trovino gli elementi.

La pagina presenta la possibilità di interagire in vario modo; tema dark (default) e light, filtri di ricerca, panelli informativi, il tutto ottimizzato su ogni fronte da cui deriva un'esperienza `UI`/`UX` coinvolgente, fluida e gradevole.

I dati sono disposti in un template di tipo `grid`, ogni campione ha una _card_ personalizzata con cui può interagire per visualizzare un ulteriore pannello.

Inoltre, è stata integrata una _search bar_ per filtrare rapidamente i nomi dei campioni. L'interazione con il filtro delle ricerche è possibile come segue:

- __Mouse__: 
    - _hover_ + _click_;
    - _click_ sul `<button>` di tipo _submit_ rappresentato da un'icona di una lente per inviare il _form_. 

- __Tastiera__:
    - _frecce direzionali_ + _focus_ sull'elemento e successivo _Invio/Enter_ per invio del form;
    - _Invio/Enter_ per selezione automatica del primo risultato trovato;

Il submit del form viene intercettato e gestito con `preventDefault()`, impedendo che la pagina si ricarichi e mantenendo la reattività della stessa.

L'input inserito viene pulito quando si seleziona un elemento o si annulla tutto con `Escape`.
Se la pagina non si trova sull'elemento selezionato, verrà scrollata fino alla corrispondenza e per un'ulteriore semplicità il pannello di dettagli aggiuntivi viene aperto automaticamente in contemporanea.

L'apertura del pannello comporta anche un contrasto di opacità, migliorando la concentrazione visiva sull'elemento con cui si sta interagendo.

È previsto uno scroll dei campioni adiacenti senza la necessità di chiudere e riaprire il pannello.

Infine le abilità sono caricate utilizzando degli _accordion_ per mostrare ulteriori informazioni.


## Obiettivi
- Scrivere `HTML` semantico (tag `<head>` incluso) per migliorare la pagina lato `SEO` (Search Engine Optimization).
- Ridurre al minimo il codice:
    - `HTML`: pochi tag, niente `<div>` inutili, layout ben strutturato con i rispettivi tag `<header>` `<main>` `<footer>`.
    - `CSS`: utilizzo di variabili per gestire facilmente colori/dimensioni uniformate per tutta la pagina, evitare di scrivere regole che di default risulterebbero identiche.
    - `JavaScript`: Centralizzare le varie logiche in delle _classi_ da cui parte tutto.

- Creare un _Layout_ di tipo _Responsive_ seguendo un approccio _Mobile First_, utilizzando `CSS` puro, senza utilizzo di Framework se non per il caricamento delle icone tramite [`Bootstrap Icon`](https://icons.getbootstrap.com/), importato via `CDN`.
- Importare un _font_ specifico preso dal servizio [`Google Fonts`](https://fonts.google.com/) per usarlo in tutta la pagina, per separare la logica ho deciso di importarlo direttamente nel file [_style.css_](/frontend/style.css) ed applicarlo poi a tutta la pagina.
- Utilizzare _OOP_ in `JavaScript` e diversi file per sezionare le interazioni necessarie al funzionamento completo della pagina. Implementazione di mobilità tramite `keyboard` e `touch` per semplificare l'interazione dell'utente.
- Ottimizzare le risorse utilizzando metodi di _storage_ (`sessionStorage` in questo caso), `CustomEvent` per comunicare le risposte di `async function`e quando sfruttare `Event Delegation` per evitare di aggiungere dei _Listener_ ovunque.

## Tecnologie

- `HTML`
- `CSS`
- `JavaScript`
- `Bootstrap Icon`

## Come usarlo

Visitare il sito [Frontend-Project](https://matty-coding.github.io/Aphelyah/)
