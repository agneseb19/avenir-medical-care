# Avenir Medical Care

Sito del poliambulatorio Avenir Medical Care (Roma): senologia con la dott.ssa Francesca Svegliati, mammografia 3D con tomosintesi, ginecologia e radiologia, in collaborazione con Praemedica.

## Struttura

- `sito/`: il sito.
  - `index.html`: la Home. Barra di navigazione e piè di pagina si modificano qui.
  - `build.py`: genera tutte le altre pagine (servizi, mammografia 3D, visita senologica, ecografia mammaria, ginecologia, radiologia, chi siamo, contatti) riusando barra e piè di pagina della Home. Dopo ogni modifica: `python3 build.py`.
  - `assets/style.css`: gli stili.
  - `assets/main.js`: animazioni (GSAP + ScrollTrigger + Lenis) e interazioni.
  - `assets/strati.js`: lo schema animato della tomosintesi.
  - `assets/img/`: le immagini.
- `_demo-scartate/`: le versioni precedenti, conservate come archivio.

## Vederlo in locale

```bash
cd sito
python3 -m http.server 8000
```

Poi apri http://localhost:8000.

## Da completare prima della pubblicazione

- Telefono, WhatsApp, email, orari e direttore sanitario (sono evidenziati in giallo nelle pagine).
- Elenco definitivo delle prestazioni di ginecologia e radiologia.
- Foto della dottoressa ad alta risoluzione e foto della sede di Roma.
- Collegare il modulo "Ti richiamiamo noi" al sistema di prenotazione (oggi apre un'email).

## Crediti fotografici

Ritratti e fiori da Unsplash: Maria Lupan, Nolan Manning, Jonathan Borba, gaspar zaldo, Štefan Štefančík, Annie Spratt, Anastasia Krachkovskaya, Alexandr Podvalny. Le foto dei macchinari e della dottoressa provengono da Praemedica e dal sito della dott.ssa Svegliati.
