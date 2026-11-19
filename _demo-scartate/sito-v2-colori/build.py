#!/usr/bin/env python3
"""Genera il sito Avenir Medical Care. Uso: python3 build.py"""
from pathlib import Path

ROOT = Path(__file__).parent
TEL, TEL_HREF = '06 0000 0000', 'tel:+390600000000'
EMAIL = 'info@example.com'
INDIRIZZO = 'Viale Giuseppe Mazzini 142, Roma'

ICO_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
LOGO_SVG = '<svg viewBox="0 0 40 36" aria-hidden="true"><path d="M3 34 L20 2.6 L37 34" fill="none" stroke="currentColor" stroke-width="3.4"/><path d="M5.2 30.6 C10 20 23 16.5 31.3 23.6" fill="none" stroke="var(--arco)" stroke-width="2.4" stroke-linecap="round"/></svg>'
MARCHIO = f'<a class="marchio" href="index.html" aria-label="Avenir Medical Care, home">{LOGO_SVG}<span class="nome">AVENIR</span></a>'

NAV = [('Home', 'index.html'), ('Servizi', 'servizi.html'), ('Chi siamo', 'chi-siamo.html'), ('Contatti', 'contatti.html')]

FOTO = {  # file: (titolo, autore, pagina)
    'donna1.jpg': ('Ritratto al tramonto', 'Štefan Štefančík', 'https://unsplash.com/photos/QXevDflbl8A'),
    'donna4.jpg': ('Donna sorridente', 'Nolan Manning', 'https://unsplash.com/photos/Ll9YOG20UFI'),
    'donna5.jpg': ('Donna che ride al sole', 'gaspar zaldo', 'https://unsplash.com/photos/SWcKBBRjEIM'),
    'donna6.jpg': ('Ritratto di donna', 'Maria Lupan', 'https://unsplash.com/photos/RBtFAZXlJDA'),
    'donna7.jpg': ('Donna sorridente', 'Jonathan Borba', 'https://unsplash.com/photos/5rQG1mib90I'),
    'fiore1.jpg': ('Rosa su fondo rosa', 'Annie Spratt', 'https://unsplash.com/photos/HB-Kf9WLy_0'),
    'fiore2.jpg': ('Magnolia', 'Anastasia Krachkovskaya', 'https://unsplash.com/photos/384sfGxn6dA'),
    'medico2.jpg': ('Stetoscopio', 'Alexandr Podvalny', 'https://unsplash.com/photos/tE7_jvK-_YU'),
}


def img(nome, alt, w=1200, h=1500, lazy=True, extra=''):
    l = ' loading="lazy"' if lazy else ' fetchpriority="high"'
    return f'<img src="assets/img/{nome}" alt="{alt}" width="{w}" height="{h}"{l}{extra}>'


def righe(*linee):
    return ''.join(f'<span class="riga"><span style="--i:{i}">{t}</span></span>' for i, t in enumerate(linee))


def barra(attiva):
    links = ''.join(f'<a href="{h}"' + (' aria-current="page"' if t == attiva else '') + f'>{t}</a>' for t, h in NAV)
    mob = ''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)
    return f'''<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="bar f-bianco" data-base="bianco"><div class="wrap bar-in">
  {MARCHIO}
  <nav aria-label="Principale">{links}</nav>
  <a class="btn" href="contatti.html#prenota">Prenota</a>
  <button class="menu-btn" data-menu aria-expanded="false" aria-controls="menu">Menu</button>
</div></header>
<div class="menu f-blu" id="menu">
  <div class="bar-in">{MARCHIO}<button class="menu-btn" data-menu aria-expanded="false" style="display:block">Chiudi</button></div>
  <nav aria-label="Menu">{mob}</nav>
  <a class="btn" href="{TEL_HREF}">{ICO_TEL} Chiama {TEL}</a>
</div>'''


def piede():
    cred = '; '.join(f'{t}, foto di {a} (<a class="lnk" href="{u}">Unsplash</a>)' for t, a, u in FOTO.values())
    return f'''<footer class="piede f-notte" data-campo="notte"><div class="wrap">
  <p class="nome-grande" aria-hidden="true">AVENIR</p>
  <div class="grid">
    <div class="luoghi"><p><span>{INDIRIZZO}</span></p><p><a href="{TEL_HREF}">{TEL}</a></p><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
    <div class="col"><b>Servizi</b><a href="visita-senologica.html">Visita senologica</a><a href="ecografia-mammaria.html">Ecografia mammaria</a><a href="mammografia-3d.html">Mammografia 3D</a><a href="servizi.html#ginecologia">Ginecologia</a><a href="servizi.html#radiologia">Radiologia</a></div>
    <div class="col"><b>Studio</b><a href="chi-siamo.html">Chi siamo</a><a href="contatti.html">Contatti</a><a href="contatti.html#prenota">Prenota</a></div>
    <div class="col"><b>Orari</b><span>Lun–Ven 9–19</span><span>Sabato 9–13</span><span class="segnaposto">da confermare</span></div>
  </div>
  <div class="legale"><span>Avenir Medical Care, Roma. Direttore sanitario <span class="segnaposto">da inserire</span></span><span><a class="lnk" href="#">Privacy</a> &nbsp; <a class="lnk" href="#">Cookie</a> &nbsp; <a class="lnk" href="#contenuto">Torna su</a></span></div>
  <p class="crediti">Fotografie: {cred}. Il mammografo è dello studio.</p>
</div></footer>'''


def invito(campo, titolo1, titolo2, frase):
    return f'''<section class="invito f-{campo}" data-campo="{campo}" aria-labelledby="t-invito"><div class="wrap">
  <h2 id="t-invito" data-rivela>{titolo1}<br>{titolo2}</h2>
  <div class="base"><p data-rivela style="--i:1">{frase}</p><a class="btn" data-rivela style="--i:2" href="{TEL_HREF}">{ICO_TEL} Chiama {TEL}</a></div>
</div></section>'''


def richiamo(campo, con_striscia=True):
    foto = ['donna6.jpg', 'fiore1.jpg', 'mammografo.jpg', 'donna4.jpg', 'fiore2.jpg', 'donna7.jpg', 'medico2.jpg', 'donna5.jpg', 'donna1.jpg']
    strip = ''.join(f'<img src="assets/img/{f}" alt="" width="400" height="400" loading="lazy">' for f in foto)
    striscia = f'<div class="striscia" aria-hidden="true"><div class="striscia-traccia">{strip}{strip}</div></div>' if con_striscia else ''
    return f'''<section class="f-{campo}" data-campo="{campo}" id="prenota" aria-labelledby="t-richiamo">
  {striscia}
  <div class="wrap richiamo">
    <h2 id="t-richiamo" data-rivela>Ti richiamiamo noi</h2>
    <p class="sotto lead" data-rivela style="--i:1">Lascia nome e telefono: la segreteria ti chiama per fissare la visita.</p>
    <form class="tre-celle" data-richiamo="{EMAIL}" data-rivela style="--i:2">
      <label class="vh" for="r-nome">Nome e cognome</label><input id="r-nome" name="nome" placeholder="Nome e cognome" autocomplete="name" required>
      <label class="vh" for="r-tel">Telefono</label><input id="r-tel" name="telefono" type="tel" placeholder="Telefono" autocomplete="tel" required>
      <button type="submit">Richiamami</button>
      <p class="nota">Si apre un'email già compilata per lo studio. Oppure chiama il <a class="lnk" href="{TEL_HREF}">{TEL}</a>.</p>
    </form>
  </div>
</section>'''


def pagina(nome, titolo, descr, attiva, corpo, extra_js=''):
    html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo}</title>
<meta name="description" content="{descr}">
<script>document.documentElement.classList.add('js')</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Stack+Sans+Headline:wght@300&family=Stack+Sans+Text:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
{extra_js}
<script src="assets/site.js" defer></script>
</head>
<body>
{barra(attiva)}
<main id="contenuto">
{corpo}
</main>
{piede()}
</body>
</html>'''
    (ROOT / nome).write_text(html)


# ---------------------------------------------------------------- HOME
home = f'''
<section class="hero f-bianco" data-campo="bianco" aria-labelledby="t-hero">
  <div class="arco" aria-hidden="true"><div class="arco-forma"></div><div class="arco-foto">{img('donna6.jpg', '', lazy=False)}</div></div>
  <div class="wrap grid">
    <div class="hero-testo">
      <h1 id="t-hero" class="righe">{righe('Prenditi cura', 'del tuo seno')}</h1>
      <p class="frase" data-load style="--d:380ms">Avenir è il nuovo poliambulatorio di Roma dove riceve la senologa Francesca Svegliati: visita, ecografia e mammografia 3D con tomosintesi.</p>
      <div class="azioni" data-load style="--d:480ms">
        <a class="btn" href="contatti.html#prenota">Prenota una visita</a>
        <a class="tel lnk" href="{TEL_HREF}">{ICO_TEL} {TEL}</a>
      </div>
    </div>
  </div>
</section>

<section class="cap cap-alto intro f-blu" data-campo="blu" aria-labelledby="t-intro">
  <div class="wrap grid">
    <h2 id="t-intro" class="vh">La dottoressa</h2>
    <p class="enunciato riempi">Fino ad agosto 2026 ha diretto la Senologia diagnostica e la Breast Unit del San Camillo Forlanini. Oggi la dottoressa Francesca Svegliati riceve qui.</p>
    <div class="firma" data-rivela><a class="btn" href="chi-siamo.html">Conosci la dottoressa</a></div>
    <figure class="chip parallasse" style="margin:0">{img('fiore1.jpg', 'Rosa su fondo rosa')}</figure>
  </div>
</section>

<section class="finestra" aria-labelledby="t-finestra">
  <div class="finestra-palco">
    {img('donna5.jpg', 'Una donna ride al sole, seduta su una sdraio', 1400, 2100)}
    <h2 id="t-finestra" class="finestra-testo">Un'ora per te, una volta all'anno</h2>
  </div>
</section>

<section class="vetrina f-cipria" data-campo="cipria" aria-labelledby="t-vetrina" data-schede>
  <div class="wrap grid">
    <div class="piatto" data-apri>
      {img('donna7.jpg', 'Una donna sorride', extra='')}
      {img('medico2.jpg', 'Una mano tiene uno stetoscopio')}
      <img class="attiva" src="assets/img/mammografo.jpg" alt="Il mammografo con tomosintesi dello studio" width="819" height="1024" loading="lazy">
      <svg viewBox="0 0 100 40" aria-hidden="true"><path d="M2 40 C 14 6, 86 6, 98 40" fill="none" stroke="var(--rosa)" stroke-width="1.6"/></svg>
    </div>
    <div class="vetrina-lato">
      <div>
        <h2 id="t-vetrina" class="titolo" data-rivela>Tre esami, un solo studio</h2>
        <div class="schede" role="tablist" aria-label="Esami di senologia" data-rivela style="--i:1;margin-top:28px">
          <button role="tab" id="tab-visita" aria-controls="p-visita" aria-selected="false" tabindex="-1">Visita senologica</button>
          <button role="tab" id="tab-eco" aria-controls="p-eco" aria-selected="false" tabindex="-1">Ecografia mammaria</button>
          <button role="tab" id="tab-tomo" aria-controls="p-tomo" aria-selected="true">Mammografia 3D</button>
        </div>
      </div>
      <div>
        <div class="pannello-sch" id="p-visita" role="tabpanel" aria-labelledby="tab-visita" hidden>
          <h3>Visita senologica</h3>
          <p>Il colloquio, l'esame clinico del seno e la lettura degli esami che hai già fatto. Esci sapendo cosa fare e quando tornare.</p>
        </div>
        <div class="pannello-sch" id="p-eco" role="tabpanel" aria-labelledby="tab-eco" hidden>
          <h3>Ecografia mammaria</h3>
          <p>Un esame con ultrasuoni, senza radiazioni e indolore. Spesso affianca la mammografia, soprattutto con il seno denso o prima dei 40 anni.</p>
        </div>
        <div class="pannello-sch" id="p-tomo" role="tabpanel" aria-labelledby="tab-tomo">
          <h3>Mammografia 3D con tomosintesi</h3>
          <p>Il seno viene ricostruito in strati sottili che la radiologa sfoglia uno a uno. Per te si svolge come una normale mammografia.</p>
        </div>
      </div>
      <div class="celle"><a class="btn" href="contatti.html#prenota">Prenota</a><a class="btn btn-tono" href="mammografia-3d.html">Come funziona</a></div>
    </div>
  </div>
</section>

<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-servizi">
  <div class="wrap">
    <div class="servizi-head"><h2 id="t-servizi" class="titolo" data-rivela>Tutto in un unico studio</h2></div>
    <ol class="righe-serv">
      <li class="riga-serv">
        <div class="testo" data-riga><h3><a href="servizi.html#senologia">Senologia</a></h3><p>Visita, ecografia e mammografia 3D con tomosintesi, con la dottoressa Francesca Svegliati.</p>
          <ul><li><a href="visita-senologica.html">Visita senologica</a></li><li><a href="ecografia-mammaria.html">Ecografia mammaria</a></li><li><a href="mammografia-3d.html">Mammografia 3D</a></li></ul></div>
        <figure data-apri>{img('donna4.jpg', 'Una donna sorride seduta a un tavolo')}</figure>
      </li>
      <li class="riga-serv">
        <div class="testo" data-riga><h3><a href="servizi.html#ginecologia">Ginecologia</a></h3><p>Controlli e prevenzione, dalla visita al Pap test.</p>
          <ul><li><span>Visita ginecologica</span></li><li><span>Pap test</span></li><li><span>HPV test</span></li><li><span>Ecografia pelvica</span></li></ul></div>
        <figure data-apri>{img('fiore2.jpg', 'Rami di magnolia in fiore', 1400, 933)}</figure>
      </li>
      <li class="riga-serv">
        <div class="testo" data-riga><h3><a href="servizi.html#radiologia">Radiologia</a></h3><p>Gli esami di diagnostica per immagini saranno pubblicati prima dell'apertura.</p></div>
        <figure data-apri>{img('mammografo.jpg', 'Il mammografo dello studio', 819, 1024)}</figure>
      </li>
    </ol>
  </div>
</section>

<section class="f-bianco" data-campo="bianco" aria-labelledby="t-dott">
  <div class="pannello-dott f-notte" data-campo="notte">
    <div class="sx">
      <h2 id="t-dott" data-rivela>Ti visita Francesca Svegliati</h2>
      <div class="arco-ritratto parallasse">{img('mammografo.jpg', 'Il mammografo con tomosintesi dello studio', 819, 1024)}</div>
    </div>
    <div class="dx">
      <div data-rivela><h3>Da dove viene</h3><p>Medico specialista in Diagnostica per Immagini. Fino ad agosto 2026 Primario di Diagnostica per Immagini in Senologia e Responsabile della Breast Unit del San Camillo Forlanini.</p></div>
      <div data-rivela style="--i:1"><h3>Come lavora</h3><p>Per anni in squadra con chirurghi, oncologi e radioterapisti. Ha organizzato i percorsi diagnostico-terapeutici della Breast Unit.</p></div>
      <a class="btn" data-rivela style="--i:2" href="chi-siamo.html">Chi siamo</a>
    </div>
  </div>
</section>

<section class="sez f-cipria" data-campo="cipria" aria-labelledby="t-passi">
  <div class="wrap">
    <div class="passi-intro"><h2 id="t-passi" data-rivela>Prenotare è semplice</h2><p class="lead" data-rivela style="--i:1">Dalla telefonata al giorno della visita, ecco cosa succede.</p></div>
    <div class="fisa" data-fisa>
      <div class="fisa-voce aperta"><button aria-expanded="true"><span class="vh">Chiama o scrivi</span></button><span class="fisa-nome" aria-hidden="true">Chiama o scrivi</span>
        <div class="fisa-corpo"><h3>Chiama o scrivi</h3><p>Al <a href="{TEL_HREF}">{TEL}</a> o su WhatsApp. La segreteria ti propone la prima data libera.</p></div></div>
      <div class="fisa-voce"><button aria-expanded="false"><span class="vh">Scegli il giorno</span></button><span class="fisa-nome" aria-hidden="true">Scegli il giorno</span>
        <div class="fisa-corpo"><h3>Scegli il giorno</h3><p>Concordi giorno e orario. Se servono più esami, quando possibile li mettiamo nella stessa mattina.</p></div></div>
      <div class="fisa-voce"><button aria-expanded="false"><span class="vh">Prepara gli esami</span></button><span class="fisa-nome" aria-hidden="true">Prepara gli esami</span>
        <div class="fisa-corpo"><h3>Prepara gli esami</h3><p>Porta mammografie ed ecografie precedenti, anche su CD. Il giorno dell'esame evita creme, talco e deodorante.</p></div></div>
      <div class="fisa-voce"><button aria-expanded="false"><span class="vh">Il giorno della visita</span></button><span class="fisa-nome" aria-hidden="true">Il giorno della visita</span>
        <div class="fisa-corpo"><h3>Il giorno della visita</h3><p>La dottoressa ti spiega cosa ha visto e quali sono i passi successivi, con calma.</p></div></div>
    </div>
  </div>
</section>

{invito('blu', 'Prenota il tuo', 'controllo', 'Chiama la segreteria o lascia il tuo numero qui sotto: ti richiamiamo noi.')}
{richiamo('rosa')}
'''
pagina('index.html', 'Avenir Medical Care, senologia a Roma', 'Poliambulatorio a Roma: senologia con la dottoressa Francesca Svegliati, mammografia 3D con tomosintesi, ginecologia e radiologia.', 'Home', home)


# ---------------------------------------------------------------- SERVIZI
servizi = f'''
<section class="testata f-cipria" data-campo="cipria" aria-labelledby="t-top">
  <div class="arco-piccolo" aria-hidden="true"></div>
  <div class="wrap grid">
    <h1 id="t-top" class="righe">{righe('Servizi')}</h1>
    <p class="frase" data-load style="--d:300ms">Senologia, ginecologia e radiologia. Ogni esame ha la sua pagina: come si svolge, come prepararsi, cosa portare.</p>
  </div>
</section>

<section class="sez f-blu" data-campo="blu" id="senologia" aria-labelledby="t-sen">
  <div class="wrap due">
    <div class="a">
      <h2 id="t-sen" class="titolo" data-rivela>Senologia</h2>
      <p class="lead" data-rivela style="--i:1;margin-top:24px">Con la dottoressa Francesca Svegliati, già Primario di Diagnostica per Immagini in Senologia al San Camillo Forlanini.</p>
      <figure data-apri style="margin:48px 0 0;aspect-ratio:4/5;overflow:hidden;border-radius:999px 999px 0 0;max-width:420px">{img('donna7.jpg', 'Una donna sorride')}</figure>
    </div>
    <ul class="b elenco">
      <li data-riga><a class="voce-link" href="visita-senologica.html"><h3>Visita senologica</h3></a><a class="vai" href="visita-senologica.html" aria-hidden="true" tabindex="-1">Dettagli</a><p>Colloquio, esame clinico del seno e lettura degli esami che hai già fatto.</p></li>
      <li data-riga style="--i:1"><a class="voce-link" href="ecografia-mammaria.html"><h3>Ecografia mammaria</h3></a><a class="vai" href="ecografia-mammaria.html" aria-hidden="true" tabindex="-1">Dettagli</a><p>Ultrasuoni, senza radiazioni. Spesso affianca la mammografia.</p></li>
      <li data-riga style="--i:2"><a class="voce-link" href="mammografia-3d.html"><h3>Mammografia 3D con tomosintesi</h3></a><a class="vai" href="mammografia-3d.html" aria-hidden="true" tabindex="-1">Dettagli</a><p>Il seno ricostruito in strati sottili, letti uno alla volta.</p></li>
    </ul>
  </div>
</section>

<section class="sez f-bianco" data-campo="bianco" id="ginecologia" aria-labelledby="t-gin">
  <div class="wrap due">
    <ul class="a elenco" style="grid-row:1">
      <li data-riga><h3>Visita ginecologica</h3><p>Il controllo periodico, con colloquio ed esame clinico.</p></li>
      <li data-riga style="--i:1"><h3>Visita di controllo</h3><p>Per seguire nel tempo una situazione già nota.</p></li>
      <li data-riga style="--i:2"><h3>Pap test e HPV test</h3><p>Gli esami di prevenzione del tumore del collo dell'utero.</p></li>
      <li data-riga style="--i:3"><h3>Ecografia pelvica</h3><p>Per valutare utero e ovaie, almeno una volta all'anno.</p></li>
    </ul>
    <div class="b">
      <h2 id="t-gin" class="titolo" data-rivela>Ginecologia</h2>
      <p class="lead" data-rivela style="--i:1;margin-top:24px">Prevenzione e controlli nello stesso studio della senologia. <span class="segnaposto">Elenco da confermare</span></p>
      <figure data-apri style="margin:48px 0 0;aspect-ratio:3/2;overflow:hidden">{img('fiore2.jpg', 'Rami di magnolia in fiore', 1400, 933)}</figure>
    </div>
  </div>
</section>

<section class="cap cap-alto f-rosa" data-campo="rosa" id="radiologia" aria-labelledby="t-rad">
  <div class="wrap due" style="align-items:center">
    <div class="a"><h2 id="t-rad" class="titolo" data-rivela>Radiologia</h2><p class="lead" data-rivela style="--i:1;margin-top:24px">Gli esami di diagnostica per immagini saranno pubblicati prima dell'apertura. Per informazioni chiama la segreteria.</p>
      <p data-rivela style="--i:2;margin-top:36px"><a class="btn" href="{TEL_HREF}">{ICO_TEL} Chiama {TEL}</a></p></div>
    <figure class="b parallasse" style="margin:0;aspect-ratio:1;overflow:hidden">{img('fiore1.jpg', 'Rosa su fondo rosa')}</figure>
  </div>
</section>

{invito('notte', 'Non sai quale', 'esame ti serve?', 'Chiamaci: la segreteria ti aiuta a scegliere e ti propone la prima data libera.')}
'''
pagina('servizi.html', 'Servizi, Avenir Medical Care', 'Senologia, ginecologia e radiologia a Roma.', 'Servizi', servizi)


# ---------------------------------------------------------------- PAGINE ESAME
def faq(voci):
    return '<div class="faq">' + ''.join(f'<details data-riga style="--i:{i}"><summary>{q}</summary><div class="risposta"><div><p>{a}</p></div></div></details>' for i, (q, a) in enumerate(voci)) + '</div>'


def fatti(voci):
    return '<dl class="fatti">' + ''.join(f'<div data-riga style="--i:{i}"><dt>{k}</dt><dd>{v}</dd></div>' for i, (k, v) in enumerate(voci)) + '</dl>'


def testata_esame(h1a, h1b, frase, foto, alt, w=1200, h=1500):
    return f'''<section class="testata con-foto f-bianco" data-campo="bianco" aria-labelledby="t-top">
  <div class="wrap grid">
    <nav class="briciole" aria-label="Sei qui" data-load style="--d:100ms"><a href="servizi.html">Servizi</a><span aria-hidden="true">/</span><a href="servizi.html#senologia">Senologia</a></nav>
    <h1 id="t-top" class="righe">{righe(h1a, h1b) if h1b else righe(h1a)}</h1>
    <p class="frase" data-load style="--d:380ms">{frase}</p>
    <figure>{img(foto, alt, w, h, lazy=False)}</figure>
  </div>
</section>'''


def passi_esame(titolo, passi, campo='cipria'):
    li = ''.join(f'<li data-riga style="--i:{i}"><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(passi))
    return f'''<section class="sez f-{campo}" data-campo="{campo}" aria-labelledby="t-passi"><div class="wrap due">
  <div class="a"><h2 id="t-passi" class="titolo" data-rivela>{titolo}</h2></div>
  <ol class="b elenco">{li}</ol>
</div></section>'''


# mammografia 3D: la storia a scorrimento
mammo = f'''
{testata_esame('Mammografia 3D', 'con tomosintesi', 'Il seno ricostruito in strati sottili, letti uno alla volta. Per te si svolge come una normale mammografia.', 'mammografo.jpg', 'Il mammografo con tomosintesi dello studio', 819, 1024)}

<section class="storia f-cipria" data-campo="cipria" data-storia aria-labelledby="t-storia">
  <div class="storia-palco">
    <div class="wrap grid">
      <div class="storia-testo">
        <h2 id="t-storia">Come funziona</h2>
        <div class="storia-passi" aria-live="polite">
          <div class="storia-passo attivo"><h3>Un'unica immagine</h3><p>Nella mammografia tradizionale tutti i tessuti finiscono sovrapposti nella stessa immagine.</p></div>
          <div class="storia-passo"><h3>Il tubo si muove ad arco</h3><p>Con la tomosintesi il tubo radiogeno percorre un breve arco e acquisisce più immagini da angolazioni diverse.</p></div>
          <div class="storia-passo"><h3>Le immagini diventano strati</h3><p>Il computer ricostruisce il seno in strati sottili, come le pagine di un libro.</p></div>
          <div class="storia-passo"><h3>La radiologa li sfoglia</h3><p>Uno strato alla volta, senza i tessuti che stanno sopra e sotto.</p></div>
          <div class="storia-passo"><h3>Ciò che era coperto si vede</h3><p>È particolarmente utile con il seno denso.</p><a class="btn" href="contatti.html#prenota">Prenota la mammografia 3D</a></div>
        </div>
        <p class="storia-conta" aria-hidden="true">1 di 5</p>
      </div>
      <figure class="storia-fig">
        <svg role="img" aria-label="Schema della tomosintesi: il tubo si muove ad arco, gli strati si separano e un piccolo reperto diventa visibile."></svg>
        <figcaption>Schema illustrativo, non un'immagine clinica.</figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="sez f-blu" data-campo="blu" aria-labelledby="t-prima"><div class="wrap">
  <h2 id="t-prima" class="titolo" data-rivela>Prima dell'esame</h2>
  {fatti([('Durata', 'Pochi minuti'), ('Preparazione', 'Niente creme, talco o deodorante'), ('Da portare', 'Esami precedenti, anche su CD'), ('Chi la legge', 'Dott.ssa Francesca Svegliati')])}
</div></section>

<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-faq"><div class="wrap due">
  <div class="a"><h2 id="t-faq" class="titolo" data-rivela>Domande frequenti</h2></div>
  <div class="b">{faq([
    ('Fa male?', "La compressione è la stessa della mammografia tradizionale: può dare fastidio per qualche secondo. Serve per avere immagini nitide."),
    ('Quanto dura?', 'Pochi minuti in tutto. La compressione dura qualche secondo per ogni immagine.'),
    ('Ho le protesi al seno. Posso farla?', "Dillo alla segreteria quando prenoti: la radiologa valuterà l'esame più adatto a te."),
    ('Sono incinta o potrei esserlo.', "Avvisa prima dell'esame: la radiologa ti indicherà come procedere."),
    ("Serve l'impegnativa?", '<span class="segnaposto">Risposta da definire con lo studio</span>'),
  ])}</div>
</div></section>

{invito('rosa', 'Prenota la tua', 'mammografia 3D', 'Chiama la segreteria: ti diciamo la prima data libera e come prepararti.')}
'''
pagina('mammografia-3d.html', 'Mammografia 3D con tomosintesi, Avenir Medical Care', 'Mammografia 3D con tomosintesi a Roma con la dottoressa Francesca Svegliati.', 'Servizi', mammo, '<script src="assets/strati.js" defer></script>')

visita = f'''
{testata_esame('Visita', 'senologica', "Un colloquio, l'esame clinico del seno e la lettura dei tuoi esami. Esci sapendo cosa fare e quando tornare.", 'donna6.jpg', 'Ritratto di una donna sorridente')}
{passi_esame('Come si svolge', [('Il colloquio', 'La dottoressa ti chiede della tua storia, dei tuoi familiari e di eventuali disturbi.'), ("L'esame clinico", 'Osservazione e palpazione del seno e delle ascelle, con delicatezza.'), ('Gli esami precedenti', 'Mammografie ed ecografie che hai già fatto vengono rilette e confrontate.'), ('Il piano', 'Ti dice se servono altri esami e quando fare il prossimo controllo.')])}
<section class="sez f-blu" data-campo="blu" aria-labelledby="t-prima"><div class="wrap">
  <h2 id="t-prima" class="titolo" data-rivela>Prima della visita</h2>
  {fatti([('Durata', 'Circa mezz’ora <span class="segnaposto">da confermare</span>'), ('Preparazione', 'Nessuna'), ('Da portare', 'Esami precedenti e referti'), ('Con chi', 'Dott.ssa Francesca Svegliati')])}
</div></section>
<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-faq"><div class="wrap due">
  <div class="a"><h2 id="t-faq" class="titolo" data-rivela>Domande frequenti</h2></div>
  <div class="b">{faq([('Ogni quanto devo farla?', 'Dipende dalla tua età e dalla tua storia: te lo dice la dottoressa alla fine della visita.'), ('Posso fare anche ecografia o mammografia lo stesso giorno?', 'Quando possibile sì. Chiedilo alla segreteria quando prenoti.'), ("Serve l'impegnativa?", '<span class="segnaposto">Risposta da definire con lo studio</span>')])}</div>
</div></section>
{invito('rosa', 'Prenota la tua', 'visita', 'Chiama la segreteria: ti proponiamo la prima data libera.')}
'''
pagina('visita-senologica.html', 'Visita senologica, Avenir Medical Care', 'Visita senologica a Roma con la dottoressa Francesca Svegliati.', 'Servizi', visita)

eco = f'''
{testata_esame('Ecografia', 'mammaria', 'Un esame con ultrasuoni: senza radiazioni, indolore, in pochi minuti.', 'medico2.jpg', 'Una mano tiene uno stetoscopio')}
{passi_esame('Come si svolge', [('Ti sdrai', 'Sul lettino, con il braccio sollevato dietro la testa.'), ('Il gel e la sonda', 'Un gel trasparente e una sonda che scorre sulla pelle. Non fa male.'), ('Le immagini', 'La dottoressa osserva il tessuto in tempo reale sullo schermo.'), ('Il risultato', "Ti spiega cosa ha visto e se l'ecografia va affiancata da altri esami.")])}
<section class="sez f-blu" data-campo="blu" aria-labelledby="t-prima"><div class="wrap">
  <h2 id="t-prima" class="titolo" data-rivela>Prima dell'esame</h2>
  {fatti([('Durata', 'Pochi minuti'), ('Radiazioni', 'Nessuna'), ('Preparazione', 'Nessuna'), ('Da portare', 'Esami precedenti, anche su CD')])}
</div></section>
<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-faq"><div class="wrap due">
  <div class="a"><h2 id="t-faq" class="titolo" data-rivela>Domande frequenti</h2></div>
  <div class="b">{faq([("L'ecografia sostituisce la mammografia?", 'No: sono esami diversi che spesso si completano. La dottoressa ti dice quale serve a te.'), ('Si può fare in gravidanza?', 'Sì, gli ultrasuoni non usano radiazioni.'), ("Serve l'impegnativa?", '<span class="segnaposto">Risposta da definire con lo studio</span>')])}</div>
</div></section>
{invito('rosa', "Prenota la tua", 'ecografia', 'Chiama la segreteria: ti proponiamo la prima data libera.')}
'''
pagina('ecografia-mammaria.html', 'Ecografia mammaria, Avenir Medical Care', 'Ecografia mammaria a Roma con la dottoressa Francesca Svegliati.', 'Servizi', eco)


# ---------------------------------------------------------------- CHI SIAMO
chi = f'''
<section class="testata f-blu" data-campo="blu" aria-labelledby="t-top">
  <div class="arco-piccolo" aria-hidden="true"></div>
  <div class="wrap grid">
    <h1 id="t-top" class="righe">{righe('Chi siamo')}</h1>
    <p class="frase" data-load style="--d:300ms">Avenir nasce dalla collaborazione tra Praemedica e la dottoressa Francesca Svegliati.</p>
  </div>
</section>

<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-dott"><div class="wrap due">
  <figure class="a" data-apri style="margin:0;aspect-ratio:4/5;overflow:hidden;border-radius:999px 999px 0 0;background:var(--cipria)">
    <div style="display:grid;place-items:center;height:100%;padding:24px;text-align:center"><span class="segnaposto">Qui la foto della dottoressa</span></div>
  </figure>
  <div class="b">
    <h2 id="t-dott" class="titolo" data-rivela>Francesca Svegliati</h2>
    <p class="lead" data-rivela style="--i:1;margin-top:28px">Medico specialista in Diagnostica per Immagini, con una consolidata esperienza in senologia.</p>
    <p data-rivela style="--i:2;margin-top:24px;max-width:52ch">Fino ad agosto 2026 è stata Primario di Diagnostica per Immagini in Senologia e Responsabile della Breast Unit del San Camillo Forlanini, dove ha lavorato insieme a chirurgia oncologica, oncologia medica e radioterapia. Si è occupata dell'organizzazione dei percorsi diagnostico-terapeutici e partecipa a seminari e conferenze di divulgazione scientifica.</p>
    {fatti([('Specializzazione', 'Diagnostica per Immagini'), ('Ambito', 'Senologia'), ('Ruolo precedente', 'Primario, San Camillo Forlanini'), ('Esami', 'Visita, ecografia, mammografia 3D')])}
  </div>
</div></section>

<section class="cap cap-alto f-cipria" data-campo="cipria" aria-labelledby="t-nome"><div class="wrap due" style="align-items:center">
  <div class="a"><h2 id="t-nome" class="titolo" data-rivela>Avenir vuol dire futuro</h2></div>
  <div class="b"><p class="enunciato riempi" style="font:300 clamp(1.5rem,1rem+1.6vw,2.1rem)/1.3 var(--f-head);max-width:30ch">In francese avenir è il futuro. La curva del nostro logo è l'arco che il mammografo percorre durante la tomosintesi: guardare avanti, uno strato alla volta.</p></div>
</div></section>

<section class="sez f-rosa" data-campo="rosa" aria-labelledby="t-studio"><div class="wrap due" style="align-items:center">
  <figure class="a" data-apri style="margin:0;aspect-ratio:4/5;overflow:hidden">{img('mammografo.jpg', 'Il mammografo con tomosintesi dello studio', 819, 1024)}</figure>
  <div class="b">
    <h2 id="t-studio" class="titolo" data-rivela>Lo studio</h2>
    <p class="lead" data-rivela style="--i:1;margin-top:28px">Un poliambulatorio nuovo a Roma, in Viale Mazzini, con un mammografo di ultima generazione per la tomosintesi.</p>
    <p data-rivela style="--i:2;margin-top:24px;max-width:48ch">L'esperienza organizzativa di Praemedica e quella clinica della dottoressa Svegliati, per avere senologia, ginecologia e radiologia nello stesso posto. <span class="segnaposto">Testo da completare con lo studio</span></p>
  </div>
</div></section>

{invito('notte', 'Vieni a', 'conoscerci', 'Chiama la segreteria per fissare la tua prima visita.')}
'''
pagina('chi-siamo.html', 'Chi siamo, Avenir Medical Care', 'Avenir Medical Care: la dottoressa Francesca Svegliati e lo studio.', 'Chi siamo', chi)


# ---------------------------------------------------------------- CONTATTI
contatti = f'''
<section class="testata f-rosa" data-campo="rosa" aria-labelledby="t-top">
  <div class="wrap grid">
    <h1 id="t-top" class="righe">{righe('Contatti')}</h1>
    <p class="frase" data-load style="--d:300ms">Chiama, scrivi su WhatsApp o lascia il tuo numero: ti richiamiamo noi.</p>
  </div>
</section>

<section class="sez f-bianco" data-campo="bianco" aria-labelledby="t-dove"><div class="wrap due">
  <div class="a">
    <h2 id="t-dove" class="vh">Recapiti</h2>
    <a class="grande-tel lnk" href="{TEL_HREF}" data-rivela>{TEL}</a>
    <dl style="margin:48px 0 0;display:grid;gap:28px">
      <div data-riga><dt class="muted" style="font-size:var(--step-small);font-weight:500">Indirizzo</dt><dd style="margin:6px 0 0;font-size:var(--step-lead)">{INDIRIZZO} <span class="segnaposto">da confermare</span></dd></div>
      <div data-riga style="--i:1"><dt style="font-size:var(--step-small);font-weight:500">WhatsApp</dt><dd style="margin:6px 0 0;font-size:var(--step-lead)"><a class="lnk" href="#">000 000 0000</a> <span class="segnaposto">segnaposto</span></dd></div>
      <div data-riga style="--i:2"><dt style="font-size:var(--step-small);font-weight:500">Email</dt><dd style="margin:6px 0 0;font-size:var(--step-lead)"><a class="lnk" href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
    </dl>
    <h3 style="font:500 1.25rem/1.2 var(--f-text);margin-top:56px" data-rivela>Orari <span class="segnaposto">da confermare</span></h3>
    <table class="orari" style="margin-top:12px" data-rivela><tr><td>Lunedì – venerdì</td><td>9:00 – 19:00</td></tr><tr><td>Sabato</td><td>9:00 – 13:00</td></tr><tr><td>Domenica</td><td>Chiuso</td></tr></table>
  </div>
  <div class="b" data-apri><iframe class="mappa" title="Mappa: {INDIRIZZO}" src="https://maps.google.com/maps?q=Viale%20Giuseppe%20Mazzini%20142%20Roma&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>

{richiamo('cipria', con_striscia=False)}
'''
pagina('contatti.html', 'Contatti, Avenir Medical Care', 'Telefono, indirizzo e orari di Avenir Medical Care a Roma.', 'Contatti', contatti)
print('ok')
