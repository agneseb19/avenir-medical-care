#!/usr/bin/env python3
"""Genera le demo di Avenir Medical Care da parti comuni.
Uso: python3 build.py  → scrive demo-a.html, demo-b.html, demo-c.html, servizio-mammografia-3d.html
"""
from pathlib import Path

ROOT = Path(__file__).parent

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700&family=Urbanist:wght@300;400;500;600&display=swap" rel="stylesheet">'

LOGO_SVG = '<svg viewBox="0 0 40 36" aria-hidden="true"><path d="M3 34 L20 2.6 L37 34" fill="none" stroke="currentColor" stroke-width="4.2"/><path d="M5.2 30.6 C10 20 23 16.5 31.3 23.6" fill="none" stroke="#c4877c" stroke-width="2.6" stroke-linecap="round"/></svg>'
LOGO = f'<a class="logo" href="{{{{HOME}}}}" aria-label="Avenir Medical Care, pagina iniziale">{LOGO_SVG}<span class="logo-testo"><span class="logo-nome">AVENIR</span><span class="logo-sub">MEDICAL CARE</span></span></a>'

ICO_TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'

TEL = '06 0000 0000'
TEL_HREF = 'tel:+390600000000'

NAV = {
    'a': [('Chi siamo', '#chi-siamo'), ('Contatti', '#contatti')],
    'b': [('Senologia', '#servizi'), ('Ginecologia', '#ginecologia'), ('Radiologia', '#radiologia'), ('Chi siamo', '#chi-siamo'), ('Contatti', '#contatti')],
    'c': None,  # menu a tendina "Servizi", definito sotto
}

NAV_C = '''<nav class="nav" aria-label="Principale">
  <div class="tendina">
    <button class="nav-voce" aria-expanded="false" aria-controls="pannello-servizi" data-tendina>Servizi <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
    <div class="pannello" id="pannello-servizi" hidden>
      <div><h3>Senologia</h3><a href="servizio-mammografia-3d.html">Visita senologica</a><a href="servizio-mammografia-3d.html">Ecografia mammaria</a><a href="servizio-mammografia-3d.html">Mammografia 3D con tomosintesi</a></div>
      <div><h3>Ginecologia</h3><a href="#ginecologia">Visita ginecologica</a><a href="#ginecologia">Pap test e HPV test</a><a href="#ginecologia">Ecografia pelvica</a></div>
      <div><h3>Radiologia</h3><p class="muted">Elenco degli esami in arrivo</p></div>
    </div>
  </div>
  <a href="#chi-siamo">Chi siamo</a><a href="#contatti">Contatti</a>
</nav>'''


def nav_html(key):
    if key == 'c':
        return NAV_C
    links = ''.join(f'<a href="{h}">{t}</a>' for t, h in NAV[key])
    return f'<nav class="nav" aria-label="Principale">{links}</nav>'


def mobile_menu(key):
    if key == 'b':
        voci = [('Senologia', '#servizi', 'Visita, ecografia, mammografia 3D'), ('Ginecologia', '#ginecologia', None), ('Radiologia', '#radiologia', None), ('Chi siamo', '#chi-siamo', None), ('Contatti', '#contatti', None)]
    else:
        voci = [('Servizi', '#servizi', 'Senologia, ginecologia, radiologia'), ('Chi siamo', '#chi-siamo', None), ('Contatti', '#contatti', None)]
    links = ''.join(f'<a href="{h}">{t}' + (f'<span class="menu-sub">{s}</span>' if s else '') + '</a>' for t, h, s in voci)
    return f'''<div class="menu-mobile" hidden id="menu-mobile" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="menu-top">{LOGO}<button class="menu-btn" data-menu-chiudi>Chiudi</button></div>
  <nav>{links}</nav>
  <a class="btn btn-pieno" href="{TEL_HREF}">{ICO_TEL} Chiama {TEL}</a>
  <a class="btn btn-vuoto" href="#prenota">Come prenotare</a>
</div>'''


def header(key):
    return f'''<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="header"><div class="wrap header-in">
  {LOGO}
  {nav_html(key)}
  <div class="header-azioni">
    <a class="tel" href="{TEL_HREF}" aria-label="Chiama {TEL}">{ICO_TEL} <span>{TEL}</span></a>
    <a class="btn btn-pieno" href="#prenota">Prenota</a>
    <button class="menu-btn" data-menu-apri aria-expanded="false" aria-controls="menu-mobile">Menu</button>
  </div>
</div></header>
{mobile_menu(key)}'''


SERVIZI = '''<section class="sez" id="servizi" aria-labelledby="t-servizi"><div class="wrap">
  <div class="sez-titolo"><h2 id="t-servizi">Servizi</h2><p class="muted">Tre branche, con la senologia al centro. Ogni esame ha una pagina con come si svolge, come prepararsi e cosa portare.</p></div>
  <div class="branche">
    <div class="branca">
      <div class="branca-nome"><h3>Senologia</h3><span class="stato">Con la dott.ssa Francesca Svegliati</span></div>
      <ul class="prestazioni">
        <li><a href="servizio-mammografia-3d.html"><span>Visita senologica</span><span class="vai">Dettagli</span></a></li>
        <li><a href="servizio-mammografia-3d.html"><span>Ecografia mammaria</span><span class="vai">Dettagli</span></a></li>
        <li><a href="servizio-mammografia-3d.html"><span>Mammografia 3D con tomosintesi <span class="tag3d">Nuova tecnologia</span></span><span class="vai">Dettagli</span></a></li>
      </ul>
    </div>
    <div class="branca" id="ginecologia">
      <div class="branca-nome"><h3>Ginecologia</h3><span class="stato">Elenco in definizione</span></div>
      <ul class="prestazioni">
        <li><span class="voce">Visita ginecologica</span></li>
        <li><span class="voce">Visita di controllo</span></li>
        <li><span class="voce">Pap test</span></li>
        <li><span class="voce">HPV test</span></li>
        <li><span class="voce">Ecografia pelvica</span></li>
      </ul>
    </div>
    <div class="branca" id="radiologia">
      <div class="branca-nome"><h3>Radiologia</h3><span class="stato">In arrivo</span></div>
      <ul class="prestazioni"><li><span class="voce nota">L'elenco degli esami sarà pubblicato prima dell'apertura.</span></li></ul>
    </div>
  </div>
</div></section>'''

DOTTORESSA = '''<section class="sez" id="chi-siamo" aria-labelledby="t-dott" style="background:var(--nebbia)"><div class="wrap">
  <p class="muted" style="margin-bottom:40px;font-size:1.25rem;max-width:44ch">Avenir Medical Care è un nuovo poliambulatorio a Roma, nato dalla collaborazione tra Praemedica e la dottoressa Francesca Svegliati.</p>
  <div class="dott">
    <div class="ritratto" role="img" aria-label="Spazio per la foto della dottoressa">
      <svg viewBox="0 0 40 36" aria-hidden="true"><path d="M5.2 30.6 C10 20 23 16.5 31.3 23.6" fill="none" stroke="#c4877c" stroke-width="1.2" stroke-linecap="round"/></svg>
      <span>Foto della dottoressa</span>
    </div>
    <div class="dott-testo">
      <h2 id="t-dott">Dott.ssa Francesca Svegliati</h2>
      <p class="dott-ruolo">Medico specialista in Diagnostica per Immagini, con una consolidata esperienza in senologia.</p>
      <p>Fino ad agosto 2026 è stata Primario di Diagnostica per Immagini in Senologia e Responsabile della Breast Unit del San Camillo Forlanini, dove ha lavorato insieme a chirurgia oncologica, oncologia medica e radioterapia.</p>
      <p>Si è occupata dell'organizzazione dei percorsi diagnostico-terapeutici e partecipa a seminari e conferenze di divulgazione scientifica.</p>
      <ul class="fatti">
        <li><b>Specializzazione</b><span>Diagnostica per Immagini</span></li>
        <li><b>Ambito</b><span>Senologia</span></li>
        <li><b>Ruolo precedente</b><span>Primario e Responsabile Breast Unit, San Camillo Forlanini</span></li>
      </ul>
    </div>
  </div>
</div></section>'''

PRENOTA = f'''<section class="sez" id="prenota" aria-labelledby="t-prenota"><div class="wrap">
  <div class="sez-titolo"><h2 id="t-prenota">Come prenotare</h2></div>
  <ol class="passi">
    <li><h3>Chiama o scrivi</h3><p>Al numero <a href="{TEL_HREF}"><b>{TEL}</b></a> o su WhatsApp. Ti risponde la segreteria, non un risponditore automatico.</p></li>
    <li><h3>Scegli giorno e orario</h3><p>Ti diciamo la prima data libera e come prepararti all'esame.</p></li>
    <li><h3>Porta gli esami precedenti</h3><p>Mammografie ed ecografie già fatte, anche su CD, servono per il confronto.</p></li>
  </ol>
  <p style="margin-top:48px"><a class="btn btn-pieno" href="{TEL_HREF}">{ICO_TEL} Chiama {TEL}</a></p>
</div></section>'''

CONTATTI = f'''<section class="sez" id="contatti" aria-labelledby="t-contatti" style="background:var(--rosa-velo)"><div class="wrap">
  <div class="sez-titolo"><h2 id="t-contatti">Contatti e orari</h2></div>
  <div class="contatti">
    <dl>
      <div><dt>Indirizzo</dt><dd>Viale Giuseppe Mazzini 142<br>00195 Roma <span class="placeholder">da confermare</span></dd></div>
      <div><dt>Telefono</dt><dd><a href="{TEL_HREF}">{TEL}</a> <span class="placeholder">segnaposto</span></dd></div>
      <div><dt>WhatsApp</dt><dd><a href="#">000 000 0000</a> <span class="placeholder">segnaposto</span></dd></div>
      <div><dt>Email</dt><dd><a href="mailto:info@example.com">info@example.com</a> <span class="placeholder">segnaposto</span></dd></div>
    </dl>
    <div>
      <table class="orari"><caption class="muted" style="text-align:left;font-weight:700;font-size:1rem;padding-bottom:6px">Orari <span class="placeholder">da confermare</span></caption>
        <tr><td>Lunedì – Venerdì</td><td>9:00 – 19:00</td></tr>
        <tr><td>Sabato</td><td>9:00 – 13:00</td></tr>
        <tr><td>Domenica</td><td>Chiuso</td></tr>
      </table>
      <div class="mappa">Mappa</div>
    </div>
  </div>
</div></section>'''

FOOTER = f'''<footer class="footer"><div class="wrap footer-in">
  {LOGO}
  <p>Avenir Medical Care, Roma<br>Direttore sanitario: <span class="placeholder" style="color:#333">da inserire</span></p>
  <p><a href="#">Privacy</a> &nbsp; <a href="#">Cookie</a></p>
</div></footer>'''


def demo_bar(nome, descr):
    return f'<div class="demo-bar" role="note"><strong>{nome}</strong><span>{descr}</span><a href="index.html">Tutte le demo</a></div>'


def page(title, key, body, extra_head='', extra_js='', home='#'):
    html = f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{FONTS}
<link rel="stylesheet" href="assets/shared.css">
{extra_head}
</head>
<body>
{body}
<script src="assets/shared.js"></script>
{extra_js}
</body>
</html>'''
    return html.replace('{{HOME}}', home)


def main():
    parts = {k: (ROOT / 'parts' / f'{k}.html').read_text() for k in ['hero-a', 'feat-a', 'hero-b', 'feat-b', 'hero-c', 'servizio']}
    comuni = SERVIZI + DOTTORESSA + PRENOTA + CONTATTI

    demos = {
        'a': ('Demo A · Essenziale', 'Movimento leggero. Servizi in home, navigazione ridotta a Chi siamo e Contatti.', parts['hero-a'] + parts['feat-a'] + comuni, '', '<script src="assets/strati.js"></script><script src="assets/demo-a.js"></script>'),
        'b': ('Demo B · Via di mezzo', 'Una sola sezione guidata dallo scroll. Le tre branche direttamente nella barra.', parts['hero-b'] + parts['feat-b'] + comuni, '<link rel="stylesheet" href="assets/demo-b.css">', '<script src="assets/strati.js"></script><script src="assets/demo-b.js"></script>'),
        'c': ('Demo C · Immersiva', 'Scena 3D in WebGL guidata dallo scroll. Menu "Servizi" a tendina.', parts['hero-c'] + comuni, '<link rel="stylesheet" href="assets/demo-c.css">', '<script src="assets/strati.js"></script><script type="module" src="assets/demo-c.js"></script>'),
    }
    for k, (nome, descr, main_html, head, js) in demos.items():
        body = demo_bar(nome, descr) + header(k) + f'<main id="contenuto">{main_html}</main>' + FOOTER
        (ROOT / f'demo-{k}.html').write_text(page(f'Avenir Medical Care, {nome}', k, body, head, js, home=f'demo-{k}.html'))

    # pagina singolo servizio (navigazione della demo B, quella consigliata)
    sv_header = header('b').replace('<a href="#servizi">Senologia</a>', '<a href="#servizi" aria-current="page">Senologia</a>').replace('href="#servizi"', 'href="demo-b.html#servizi"').replace('href="#ginecologia"', 'href="demo-b.html#ginecologia"').replace('href="#radiologia"', 'href="demo-b.html#radiologia"').replace('href="#chi-siamo"', 'href="demo-b.html#chi-siamo"').replace('href="#contatti"', 'href="demo-b.html#contatti"')
    body = demo_bar('Pagina servizio', 'Esempio di pagina dedicata a un singolo esame. Stessa struttura per tutti i servizi.') + sv_header + f'<main id="contenuto">{parts["servizio"]}{PRENOTA}</main>' + FOOTER
    (ROOT / 'servizio-mammografia-3d.html').write_text(page('Mammografia 3D con tomosintesi, Avenir Medical Care', 'b', body, '<link rel="stylesheet" href="assets/servizio.css">', '<script src="assets/strati.js"></script><script src="assets/demo-a.js"></script>', home='demo-b.html'))
    print('ok')


if __name__ == '__main__':
    main()
