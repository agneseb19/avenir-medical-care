#!/usr/bin/env python3
"""Genera le sottopagine di Avenir riusando barra e piè di pagina della Home.
Uso: python3 build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
home = (ROOT / 'index.html').read_text()
TESTA = home[:home.index('<main id="contenuto">')]
CODA = home[home.index('</main>') + len('</main>'):]
TEL, TEL_HREF, EMAIL = '06 0000 0000', 'tel:+390600000000', 'info@example.com'


def ico(nome, w=''):
    return f'<svg{w}><use href="#i-{nome}"/></svg>'


def btn(testo, href, cls='', ico_n='freccia', extra=''):
    return f'<a class="btn {cls}" href="{href}"{extra}>{testo}<span class="ico">{ico(ico_n)}</span></a>'


def pagina(nome, titolo, descr, sezione, corpo):
    t = TESTA.replace('<title>Avenir Medical Care · Senologia a Roma</title>', f'<title>{titolo}</title>')
    t = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{descr}">', t)
    t = t.replace('<a href="index.html" aria-current="page">Home</a>', '<a href="index.html">Home</a>')
    if sezione == 'Servizi':
        t = t.replace('<button aria-expanded="false" aria-controls="mega">', '<button class="corrente" aria-expanded="false" aria-controls="mega">')
    elif sezione:
        t = t.replace(f'<a href="{sezione}">', f'<a href="{sezione}" aria-current="page">', 1)
    (ROOT / nome).write_text(t + '<main id="contenuto">\n' + corpo + '\n</main>' + CODA)


def hero(briciole, h1, lead, foto=None, alt='', azioni=True):
    bri = '<nav class="briciole" aria-label="Sei qui" data-h>' + f' {ico("giu")} '.join(f'<a href="{h}">{t}</a>' if h else f'<span>{t}</span>' for t, h in briciole) + '</nav>'
    media = ''
    if foto:
        media = f'''<div class="hero-media">
          <svg class="hero-arco" viewBox="0 0 100 60" aria-hidden="true"><path d="M3 58 C 8 4, 92 4, 97 58" fill="none" stroke="#c98a8f" stroke-width=".7" stroke-linecap="round"/></svg>
          <div class="hero-foto"><img src="assets/img/{foto}" alt="{alt}" fetchpriority="high"></div>
        </div>'''
    az = f'''<div class="hero-azioni" data-h>{btn('Prenota una visita', 'contatti.html#prenota', extra=' data-magnete')}<a class="btn btn-vuoto" href="{TEL_HREF}">{ico('tel', ' width="18" height="18"')}{TEL}</a></div>''' if azioni else ''
    return f'''<section class="hero hero-pag{'' if foto else ' senza-media'}">
    <div class="hero-box"><div class="hero-grid">
      <div>{bri}<h1 data-split>{h1}</h1><p class="lead" data-h>{lead}</p>{az}</div>
      {media}
    </div></div>
  </section>'''


def testa(sopra, titolo, testo=''):
    p = f'<p class="lead" data-su>{testo}</p>' if testo else ''
    return f'<div class="testa"><div><span class="sopra" data-su>{sopra}</span><h2 class="h2" data-split>{titolo}</h2></div>{p}</div>'


def faq(voci):
    return '<div class="faq">' + ''.join(f'<details><summary>{q}</summary><p class="risp">{a}</p></details>' for q, a in voci) + '</div>'


def sez_faq(voci):
    return f'''<section class="sez"><div class="wrap faq-grid">
    <div><span class="sopra" data-su>Domande</span><h2 class="h2" data-split>Domande frequenti</h2><p class="lead" data-su style="margin-top:16px">Non trovi la risposta? Chiama la segreteria al <a href="{TEL_HREF}" style="color:var(--blu);font-weight:600">{TEL}</a>.</p></div>
    {faq(voci)}
  </div></section>'''


def fasi(voci):
    return '<div class="fasi">' + ''.join(f'<div class="fase"><h3>{t}</h3><p>{p}</p></div>' for t, p in voci) + '</div>'


def dati(voci, cls='dati4'):
    return f'<div class="{cls}">' + ''.join(f'<div class="dato">{ico(i)}<b>{t}</b><small>{s}</small></div>' for i, t, s in voci) + '</div>'


def riga(ico_n, titolo, sotto='', href=None):
    tag, h = ('a', f' href="{href}"') if href else ('div', '')
    fr = ico('freccia') if href else ''
    s = f'<small>{sotto}</small>' if sotto else ''
    return f'<{tag} class="riga"{h}><span class="riga-ico">{ico(ico_n)}</span><span><b>{titolo}</b>{s}</span>{fr}</{tag}>'


def prep(si, no, titolo_si='Da fare', titolo_no='Da evitare'):
    li = lambda v: ''.join(f'<li>{x}</li>' for x in v)
    return f'<div class="prep"><div class="prep-col"><h3><i>✓</i>{titolo_si}</h3><ul>{li(si)}</ul></div><div class="prep-col no"><h3><i>✕</i>{titolo_no}</h3><ul>{li(no)}</ul></div></div>'


def card(foto, titolo, testo, href, alt=''):
    return f'<a class="card" href="{href}"><div class="card-f"><img src="assets/img/{foto}" alt="{alt}" loading="lazy"></div><div class="card-t"><h3>{titolo}</h3><p>{testo}</p><span class="vai">Scopri {ico("freccia")}</span></div></a>'


def cta(titolo, testo, foto='donna5.jpg'):
    return f'''<section class="cta" style="margin-top:clamp(40px,5vw,80px)">
    <div class="cta-bg" data-par="-10"><img src="assets/img/{foto}" alt="" loading="lazy"></div>
    <div class="wrap">
      <h2 data-split>{titolo}</h2>
      <p data-su>{testo}</p>
      <div class="cta-azioni" data-su>{btn('Prenota una visita', 'contatti.html#prenota', 'btn-chiaro', extra=' data-magnete')}<a class="btn btn-vuoto" href="{TEL_HREF}">{ico('tel', ' width="18" height="18"')}{TEL}</a></div>
    </div>
  </section>'''


ALTRI = {
    'visita': card('donna7.jpg', 'Visita senologica', 'Colloquio, esame clinico e lettura dei tuoi esami.', 'visita-senologica.html'),
    'eco': card('medico2.jpg', 'Ecografia mammaria', 'Ultrasuoni, senza radiazioni e indolore.', 'ecografia-mammaria.html'),
    'tomo': card('pm-tomo.jpg', 'Mammografia 3D', 'Il seno ricostruito in strati sottili.', 'mammografia-3d.html'),
    'gin': card('donna4.jpg', 'Ginecologia', 'Visita, Pap test, HPV test ed ecografia pelvica.', 'ginecologia.html', 'Una donna sorride'),
    'rad': card('pm-moc.jpg', 'Radiologia', 'Densitometria ossea (MOC) e radiografie.', 'radiologia.html'),
}


def correlati(*chiavi):
    return f'''<section class="sez correlati" style="padding-top:0"><div class="wrap">
    {testa('Altri esami', 'Potrebbe interessarti anche')}
    <div class="griglia">{''.join(ALTRI[k] for k in chiavi)}</div>
  </div></section>'''


# =============================================================== PRESTAZIONI
prestazioni = f"""
  {hero([('Home', 'index.html'), ('Prestazioni', None)], 'Le prestazioni', 'Senologia, ginecologia e radiologia in un unico poliambulatorio a Roma. Scegli l’area che ti interessa.', 'pm-tomo.jpg', 'La sala mammografia con la postazione di refertazione')}

  <section class="sez"><div class="wrap">
    {testa('Le aree', 'Tre aree, un solo centro', 'Ogni area ha la sua pagina con le visite e gli esami, e ogni esame spiega come si svolge e come prepararsi.')}
    <div class="griglia">
      {card('donna7.jpg', 'Senologia', 'Visita senologica, ecografia mammaria e mammografia 3D con tomosintesi.', 'senologia.html', 'Una donna sorride')}
      {card('donna4.jpg', 'Ginecologia', 'Visita ginecologica, visita di controllo, Pap test, HPV test ed ecografia pelvica.', 'ginecologia.html', 'Una donna sorride seduta a un tavolo')}
      {card('pm-moc.jpg', 'Radiologia', 'Densitometria ossea (MOC) e radiografie.', 'radiologia.html', 'Il densitometro per la MOC')}
    </div>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap split">
    <div class="split-foto"><img src="assets/img/pm-tomo2.jpg" alt="Il mammografo con tomosintesi" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>In evidenza</span>
      <h2 class="h2" data-split>Mammografia 3D con tomosintesi</h2>
      <p class="lead" data-su>Il seno ricostruito in strati sottili, letti uno alla volta: immagini più chiare, soprattutto con il seno denso. Per te si svolge come una normale mammografia.</p>
      <div style="margin-top:28px" data-su>{btn('Scopri come funziona', 'mammografia-3d.html')}</div>
    </div>
  </div></section>

  {cta('Non sai quale esame ti serve?', 'Chiama la segreteria: ti aiutiamo a scegliere e ti proponiamo la prima data libera.')}
"""
pagina('prestazioni.html', 'Prestazioni · Avenir Medical Care', 'Senologia, ginecologia e radiologia a Roma.', 'Servizi', prestazioni)

# il vecchio indirizzo rimanda alla pagina nuova
(ROOT / 'servizi.html').write_text('<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Prestazioni · Avenir Medical Care</title><meta http-equiv="refresh" content="0; url=prestazioni.html"><link rel="canonical" href="prestazioni.html"></head><body><p><a href="prestazioni.html">Vai alle prestazioni</a></p></body></html>')

# =============================================================== SENOLOGIA
senologia = f"""
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Senologia', None)], 'Senologia', 'La salute del seno, dalla visita alla mammografia 3D. Le prestazioni di senologia sono a cura della dottoressa Francesca Svegliati.', 'donna7.jpg', 'Una donna sorride')}

  <section class="sez"><div class="wrap">
    {testa('Le prestazioni', 'Visite ed esami', 'Tre prestazioni che si possono fare anche nella stessa mattina. Apri quella che ti interessa per sapere come si svolge.')}
    <div class="griglia">
      {card('donna6.jpg', 'Visita senologica', 'Il colloquio, l’esame clinico del seno e la lettura degli esami che hai già fatto. Esci sapendo cosa fare e quando tornare.', 'visita-senologica.html', 'Una donna sorridente')}
      {card('medico2.jpg', 'Ecografia mammaria', 'Un esame con ultrasuoni, senza radiazioni e indolore. Spesso affianca la mammografia, soprattutto con il seno denso.', 'ecografia-mammaria.html', 'Una mano tiene uno stetoscopio')}
      {card('pm-tomo2.jpg', 'Mammografia 3D con tomosintesi', 'Il seno ricostruito in strati sottili, letti uno alla volta. Per te si svolge come una normale mammografia.', 'mammografia-3d.html', 'Il mammografo con tomosintesi')}
    </div>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Percorsi combinati</span>
      <h2 class="h2" data-split>Più esami, una sola mattina</h2>
      <p class="lead" data-su>Quando serve, visita ed esami si fanno insieme: così esci con un quadro completo.</p>
      <div class="righe">
        {riga('cuore', 'Visita senologica + Mammografia 3D', 'Il controllo completo', 'mammografia-3d.html')}
        {riga('cuore', 'Visita senologica + Ecografia mammaria', 'Spesso indicata prima dei 40 anni', 'ecografia-mammaria.html')}
        {riga('strati', 'Visita + Mammografia 3D + Ecografia', 'Il percorso più approfondito', 'mammografia-3d.html')}
      </div>
    </div>
    <div class="split-foto"><img src="assets/img/fiore1.jpg" alt="Una rosa su fondo rosa" loading="lazy"></div>
  </div></section>

  <section class="sez" id="dottoressa" style="background:var(--cipria)"><div class="wrap dott-grid">
    <div class="dott-foto" data-par="-6"><img src="assets/img/svegliati-ritratto.jpg" alt="La dottoressa Francesca Svegliati, in camice bianco, alla scrivania dello studio" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>A cura di</span>
      <h2 class="h2" data-split>Dott.ssa Francesca Svegliati</h2>
      <p class="lead" data-su style="margin-top:12px">Le prestazioni di senologia di Avenir sono seguite dalla dottoressa Svegliati, medico specialista in Diagnostica per Immagini con una consolidata esperienza in senologia.</p>
      <p data-su style="margin-top:18px;color:var(--grigio);max-width:56ch">Fino ad agosto 2026 ha guidato la Diagnostica per Immagini in Senologia e la Breast Unit del San Camillo Forlanini, lavorando ogni giorno insieme a chirurghi, oncologi e radioterapisti. Ha organizzato i percorsi diagnostico-terapeutici della Breast Unit e porta avanti l’attività di divulgazione con seminari e conferenze sulla prevenzione.</p>
      <ul class="cred">
        <li data-su><svg><use href="#i-check"/></svg><span><b>Formazione</b> · Laurea in Medicina alla Sapienza di Roma, specializzazione in Radiologia</span></li>
        <li data-su><svg><use href="#i-check"/></svg><span><b>San Camillo Forlanini</b> · Primario di Diagnostica per Immagini in Senologia e Responsabile della Breast Unit</span></li>
        <li data-su><svg><use href="#i-check"/></svg><span><b>Villa Benedetta</b> · Direzione scientifica del Centro di Senologia</span></li>
      </ul>
      <div data-su style="display:flex;flex-wrap:wrap;gap:12px;margin-top:30px">{btn('Prenota una visita senologica', 'contatti.html#prenota')}<a class="btn btn-vuoto" href="https://www.francescasvegliati.it" target="_blank" rel="noopener">Il suo sito personale</a></div>
    </div>
  </div></section>

  {cta('Prenota il tuo controllo senologico', 'Chiama la segreteria o lascia il tuo numero: ti richiamiamo noi.')}
"""
pagina('senologia.html', 'Senologia · Avenir Medical Care', 'Senologia a Roma: visita senologica, ecografia mammaria e mammografia 3D con tomosintesi, a cura della dottoressa Francesca Svegliati.', 'Servizi', senologia)

# =============================================================== MEDICI
medici = f"""
  {hero([('Home', 'index.html'), ('Medici', None)], 'I nostri medici', 'Stiamo completando la squadra di specialisti di Avenir. Presto qui troverai i profili dei medici di ogni area.', azioni=False)}

  <section class="sez" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap">
    <div class="medici-vuoto">
      <a class="medico-area" href="senologia.html"><span class="riga-ico">{ico('cuore')}</span><b>Senologia</b><small>Profili in arrivo</small></a>
      <a class="medico-area" href="ginecologia.html"><span class="riga-ico">{ico('scintilla')}</span><b>Ginecologia</b><small>Profili in arrivo</small></a>
      <a class="medico-area" href="radiologia.html"><span class="riga-ico">{ico('doc')}</span><b>Radiologia</b><small>Profili in arrivo</small></a>
    </div>
    <p class="medici-nota" data-su>Vuoi sapere quale specialista ti visiterà? Chiama la segreteria al <a href="{TEL_HREF}">{TEL}</a>.</p>
  </div></section>
"""
pagina('medici.html', 'Medici · Avenir Medical Care', 'I medici specialisti di Avenir Medical Care a Roma.', 'medici.html', medici)

# =============================================================== MAMMOGRAFIA 3D
mammo = f'''
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Senologia', 'senologia.html'), ('Mammografia 3D', None)], 'Mammografia 3D con tomosintesi', 'Il seno ricostruito in strati sottili, letti uno alla volta. Per te si svolge come una normale mammografia.', 'pm-tomo2.jpg', 'Il mammografo con tomosintesi')}

  <section class="storia" data-storia aria-label="Come funziona la tomosintesi">
    <div class="storia-box"><div class="storia-in"><div class="wrap storia-grid">
      <div>
        <span class="sopra">Come funziona</span>
        <h2 class="h2">Dall’immagine unica agli strati</h2>
        <div class="storia-passi" aria-live="polite">
          <div class="storia-passo attivo"><h3>Un’unica immagine</h3><p>Nella mammografia tradizionale tutti i tessuti finiscono sovrapposti nella stessa immagine.</p></div>
          <div class="storia-passo"><h3>Il tubo si muove ad arco</h3><p>Con la tomosintesi il tubo radiogeno percorre un breve arco e acquisisce più immagini da angolazioni diverse.</p></div>
          <div class="storia-passo"><h3>Le immagini diventano strati</h3><p>Il computer ricostruisce il seno in strati sottili, come le pagine di un libro.</p></div>
          <div class="storia-passo"><h3>La radiologa li sfoglia</h3><p>Uno strato alla volta, senza i tessuti che stanno sopra e sotto.</p></div>
          <div class="storia-passo"><h3>Ciò che era coperto si vede</h3><p>Per questo la tomosintesi è particolarmente utile con il seno denso.</p>{btn('Prenota la mammografia 3D', 'contatti.html#prenota')}</div>
        </div>
        <div class="storia-barre" aria-hidden="true"><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i><i><b></b></i></div>
      </div>
      <figure class="storia-fig"><svg role="img" aria-label="Schema della tomosintesi: il tubo si muove ad arco, gli strati si separano e un piccolo reperto diventa visibile."></svg><figcaption>Schema illustrativo, non un’immagine clinica.</figcaption></figure>
    </div></div></div>
  </section>

  <section class="sez"><div class="wrap">
    {testa('I vantaggi', 'Perché scegliere la tomosintesi')}
    {dati([('strati', 'Maggiore precisione', 'Gli strati riducono le sovrapposizioni dei tessuti.'), ('scudo', 'Meno falsi allarmi', 'Meno falsi positivi e falsi negativi rispetto al 2D.'), ('cuore', 'Ideale con seno denso', 'Dove la mammografia tradizionale fa più fatica.'), ('scintilla', 'Diagnosi precoce', 'Aiuta a riconoscere lesioni piccole.')], 'valori')}
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap split">
    <div class="split-foto"><img src="assets/img/pm-tomo.jpg" alt="La sala mammografia con la postazione di refertazione" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>Prima dell’esame</span>
      <h2 class="h2" data-split>Come prepararti</h2>
      <p class="lead" data-su>L’esame dura pochi minuti e non richiede digiuno. Bastano poche attenzioni.</p>
      {prep(['Indossa un abito a due pezzi: ti spogli solo dalla vita in su', 'Porta mammografie ed ecografie precedenti, anche su CD', 'Avvisa se sei in gravidanza, allatti o hai protesi al seno'], ['Deodorante, talco e creme su seno e ascelle', 'Collane e orecchini lunghi', 'Se il seno è molto sensibile, i giorni subito prima del ciclo'])}
    </div>
  </div></section>

  {sez_faq([
    ('Fa male?', 'La compressione è la stessa della mammografia tradizionale: può dare fastidio per qualche secondo. Serve per avere immagini nitide.'),
    ('Quanto dura?', 'Pochi minuti in tutto. La compressione dura qualche secondo per ogni immagine.'),
    ('È diversa da una mammografia normale?', 'Per te no: stessa posizione e stessa compressione. Cambia il modo in cui vengono acquisite e lette le immagini.'),
    ('Ho le protesi al seno. Posso farla?', 'Dillo alla segreteria quando prenoti: la radiologa valuterà l’esame più adatto a te.'),
    ('Serve l’impegnativa?', '<span class="segnaposto">Risposta da definire con lo studio</span>'),
  ])}

  {correlati('visita', 'eco', 'rad')}
  {cta('Prenota la tua mammografia 3D', 'Chiama la segreteria: ti diciamo la prima data libera e come prepararti.')}
'''
pagina('mammografia-3d.html', 'Mammografia 3D con tomosintesi · Avenir Medical Care', 'Mammografia 3D con tomosintesi a Roma con la dottoressa Francesca Svegliati.', 'Servizi', mammo)

# =============================================================== VISITA SENOLOGICA
visita = f'''
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Senologia', 'senologia.html'), ('Visita senologica', None)], 'Visita senologica', "Un colloquio, l'esame clinico del seno e la lettura dei tuoi esami. Esci sapendo cosa fare e quando tornare.", 'donna7.jpg', 'Una donna sorride')}
  <section class="sez"><div class="wrap">
    {testa('Come si svolge', 'La visita, passo dopo passo')}
    {fasi([('Il colloquio', 'La dottoressa ti chiede della tua storia, dei tuoi familiari e di eventuali disturbi.'), ("L'esame clinico", 'Osservazione e palpazione del seno e delle ascelle, con delicatezza.'), ('I tuoi esami', 'Mammografie ed ecografie già fatte vengono rilette e confrontate.'), ('Il piano', 'Ti spiega se servono altri esami e quando fare il prossimo controllo.')])}
  </div></section>
  <section class="sez" style="padding-top:0"><div class="wrap split inverti">
    <div class="split-foto largo"><img src="assets/img/fiore1.jpg" alt="Una rosa su fondo rosa" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>Con chi</span>
      <h2 class="h2" data-split>Ti visita la dottoressa Francesca Svegliati</h2>
      <p class="lead" data-su>Fino ad agosto 2026 ha guidato la Diagnostica per Immagini in Senologia del San Camillo Forlanini. La visita può essere completata subito con ecografia o mammografia 3D.</p>
      <div style="margin-top:28px" data-su>{btn('Conosci la dottoressa', 'senologia.html#dottoressa')}</div>
    </div>
  </div></section>
  <section class="sez" style="padding-top:0"><div class="wrap">
    {testa('Prima della visita', 'Cosa sapere')}
    {dati([('cal', 'Circa 30 minuti', '<span class="segnaposto">da confermare</span>'), ('cuore', 'Nessuna preparazione', 'Non servono esami o digiuno.'), ('doc', 'Porta i referti', 'Esami precedenti, anche su CD.'), ('strati', 'Anche con esami', 'Si può abbinare a ecografia e mammografia 3D.')])}
  </div></section>
  {sez_faq([('Ogni quanto devo farla?', 'Dipende dalla tua età e dalla tua storia: te lo dice la dottoressa alla fine della visita.'), ('Posso fare ecografia o mammografia lo stesso giorno?', 'Sì, quando possibile. Chiedilo alla segreteria quando prenoti.'), ('Serve l’impegnativa?', '<span class="segnaposto">Risposta da definire con lo studio</span>')])}
  {correlati('tomo', 'eco', 'gin')}
  {cta('Prenota la tua visita senologica', 'Chiama la segreteria o lascia il tuo numero: ti richiamiamo noi.')}
'''
pagina('visita-senologica.html', 'Visita senologica · Avenir Medical Care', 'Visita senologica a Roma con la dottoressa Francesca Svegliati.', 'Servizi', visita)

# =============================================================== ECOGRAFIA
eco = f'''
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Senologia', 'senologia.html'), ('Ecografia mammaria', None)], 'Ecografia mammaria', 'Un esame con ultrasuoni: senza radiazioni, indolore, in pochi minuti. Spesso affianca la mammografia.', 'medico2.jpg', 'Una mano tiene uno stetoscopio')}
  <section class="sez"><div class="wrap">
    {testa('Come si svolge', "L'esame, passo dopo passo")}
    {fasi([('Ti sdrai', 'Sul lettino, con il braccio sollevato dietro la testa.'), ('Il gel e la sonda', 'Un gel trasparente e una sonda che scorre sulla pelle. Non fa male.'), ('Le immagini', 'La dottoressa osserva il tessuto in tempo reale sullo schermo.'), ('Il risultato', "Ti spiega cosa ha visto e se l'ecografia va affiancata da altri esami.")])}
  </div></section>
  <section class="sez" style="padding-top:0"><div class="wrap split inverti">
    <div class="split-foto largo"><img src="assets/img/fiore2.jpg" alt="Rami di magnolia in fiore" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>Quando è indicata</span>
      <h2 class="h2" data-split>Ecografia o mammografia?</h2>
      <p class="lead" data-su>Sono esami diversi che spesso si completano. L’ecografia è utile soprattutto con il seno denso e prima dei 40 anni; la dottoressa ti dice quale serve a te.</p>
      <div class="righe">
        {riga('strati', 'Ecografia mammaria bilaterale', 'Entrambi i seni')}
        {riga('scudo', 'Ecografia mammaria + linfonodi', 'Su indicazione della dottoressa')}
        {riga('cuore', 'Con visita senologica', 'Il controllo completo', 'visita-senologica.html')}
      </div>
    </div>
  </div></section>
  <section class="sez" style="padding-top:0"><div class="wrap">
    {testa("Prima dell'esame", 'Cosa sapere')}
    {dati([('cal', 'Pochi minuti', 'Un esame rapido.'), ('scudo', 'Nessuna radiazione', 'Si può fare anche in gravidanza.'), ('cuore', 'Nessuna preparazione', 'Non serve il digiuno.'), ('doc', 'Porta i tuoi esami', 'Ecografie e mammografie precedenti.')])}
  </div></section>
  {sez_faq([("L'ecografia sostituisce la mammografia?", 'No: sono esami diversi che spesso si completano. La dottoressa ti dice quale serve a te.'), ('Si può fare in gravidanza?', 'Sì, gli ultrasuoni non usano radiazioni.'), ('Serve l’impegnativa?', '<span class="segnaposto">Risposta da definire con lo studio</span>')])}
  {correlati('visita', 'tomo', 'gin')}
  {cta('Prenota la tua ecografia', 'Chiama la segreteria: ti proponiamo la prima data libera.')}
'''
pagina('ecografia-mammaria.html', 'Ecografia mammaria · Avenir Medical Care', 'Ecografia mammaria a Roma con la dottoressa Francesca Svegliati.', 'Servizi', eco)

# =============================================================== GINECOLOGIA
gin = f'''
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Ginecologia', None)], 'Ginecologia', 'Prevenzione e controlli per la salute della donna, nello stesso studio della senologia.', 'donna4.jpg', 'Una donna sorride seduta a un tavolo')}

  <section class="sez"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Le prestazioni</span>
      <h2 class="h2" data-split>Cosa puoi fare da noi</h2>
      <p class="lead" data-su>Una visita ginecologica almeno una volta all’anno, anche senza sintomi, è il modo più semplice per prendersi cura di sé.</p>
      <div class="righe">
        {riga('cuore', 'Visita ginecologica', 'Colloquio, esame clinico e consigli personalizzati')}
        {riga('cal', 'Visita di controllo', 'Per seguire nel tempo una situazione già nota')}
        {riga('scudo', 'Pap test', 'Prelievo di cellule dal collo dell’utero, rapido e indolore')}
        {riga('scudo', 'HPV test', 'Ricerca del papillomavirus, responsabile di quasi tutti i tumori del collo dell’utero')}
        {riga('strati', 'Ecografia pelvica', 'Valuta utero e ovaie, senza radiazioni')}
      </div>
      <p style="margin-top:16px;font-size:13px"><span class="segnaposto">Prestazioni e specialiste da confermare</span></p>
    </div>
    <div class="split-foto"><img src="assets/img/fiore2.jpg" alt="Rami di magnolia in fiore" loading="lazy"></div>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap">
    {testa('Ogni quanto', 'I controlli nel tempo', 'Indicazioni generali dei programmi di screening italiani: la ginecologa le adatta alla tua storia.')}
    {dati([('cal', 'Visita ginecologica', 'Una volta all’anno, anche senza disturbi.'), ('scudo', 'Pap test', 'Ogni 3 anni, dai 25 ai 29 anni.'), ('scudo', 'HPV test', 'Ogni 5 anni, dai 30 ai 64 anni.'), ('strati', 'Ecografia pelvica', 'Insieme alla visita annuale, se indicata.')])}
  </div></section>

  <section class="scuro"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Pap test e HPV test</span>
      <h2 class="h2" data-split>Come prepararti</h2>
      <p class="lead" data-su>Il prelievo dura pochi secondi. Per un risultato affidabile servono poche attenzioni nei giorni prima.</p>
    </div>
    {prep(['Prenota lontano dal ciclo: l’ideale è a metà tra una mestruazione e l’altra', 'Porta i risultati dei Pap test precedenti', 'Avvisa se sei in gravidanza'], ['Rapporti sessuali nelle 48 ore prima', 'Lavande, ovuli e creme vaginali nei 3 giorni prima', 'Il test durante il ciclo'])}
  </div></section>

  {sez_faq([('Pap test o HPV test: qual è la differenza?', 'Il Pap test cerca cellule alterate; l’HPV test cerca il virus che può causarle. Dai 30 anni l’HPV test è l’esame di screening consigliato.'), ('Fa male?', 'No. Il prelievo può dare un leggero fastidio per pochi secondi.'), ('Posso fare visita e Pap test insieme?', 'Sì, di solito si fanno nello stesso appuntamento.'), ('Serve l’impegnativa?', '<span class="segnaposto">Risposta da definire con lo studio</span>')])}
  {correlati('visita', 'tomo', 'eco')}
  {cta('Prenota la tua visita ginecologica', 'Chiama la segreteria: ti proponiamo la prima data libera.', 'donna6.jpg')}
'''
pagina('ginecologia.html', 'Ginecologia · Avenir Medical Care', 'Visita ginecologica, Pap test, HPV test ed ecografia pelvica a Roma.', 'Servizi', gin)

# =============================================================== RADIOLOGIA
rad = f'''
  {hero([('Home', 'index.html'), ('Prestazioni', 'prestazioni.html'), ('Radiologia', None)], 'Radiologia', 'Densitometria ossea, radiografie e mammografia 3D: la diagnostica per immagini dello studio.', 'pm-rx.jpg', 'Il macchinario per le radiografie')}

  <section class="sez"><div class="wrap">
    {testa('Gli esami', 'Diagnostica per immagini', 'L’elenco definitivo sarà pubblicato prima dell’apertura.')}
    <div class="griglia">
      <div class="card"><div class="card-f"><img src="assets/img/pm-moc.jpg" alt="Il densitometro per la MOC" loading="lazy"></div><div class="card-t"><h3>Densitometria ossea (MOC)</h3><p>Total body, lombare, femorale, lombare e femorale, ultradistale.</p></div></div>
      <div class="card"><div class="card-f"><img src="assets/img/pm-rx.jpg" alt="Il macchinario per le radiografie" loading="lazy"></div><div class="card-t"><h3>Radiografie</h3><p>Torace, colonna, bacino e anca, spalla, ginocchio, gomito, mano e piede, cranio.</p></div></div>
      <a class="card" href="mammografia-3d.html"><div class="card-f"><img src="assets/img/pm-tomo2.jpg" alt="Il mammografo con tomosintesi" loading="lazy"></div><div class="card-t"><h3>Mammografia 3D</h3><p>Bilaterale in tomosintesi, anche con ecografia e visita senologica.</p><span class="vai">Scopri {ico('freccia')}</span></div></a>
    </div>
    <p style="margin-top:16px;font-size:13px"><span class="segnaposto">Elenco da confermare</span></p>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap split inverti">
    <div class="split-foto largo"><img src="assets/img/pm-moc.jpg" alt="Il densitometro per la MOC" loading="lazy"></div>
    <div>
      <span class="sopra" data-su>In evidenza</span>
      <h2 class="h2" data-split>La MOC, per ossa forti dopo la menopausa</h2>
      <p class="lead" data-su>La densitometria ossea misura quanto sono dense le ossa, con una dose di raggi X molto bassa. È l’esame di riferimento per scoprire e seguire l’osteoporosi.</p>
      <div class="righe">
        {riga('cal', 'Dura pochi minuti', 'Resti sdraiata sul lettino, vestita')}
        {riga('scudo', 'Dose molto bassa', 'Molto inferiore a una radiografia del torace')}
        {riga('cuore', 'Non fa male', 'Nessun contatto con il macchinario')}
      </div>
    </div>
  </div></section>

  <section class="scuro"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Prima dell’esame</span>
      <h2 class="h2" data-split>Come prepararti</h2>
      <p class="lead" data-su>Radiografie e MOC non richiedono digiuno. Ecco cosa tenere a mente.</p>
    </div>
    {prep(['Avvisa sempre se sei o potresti essere in gravidanza', 'Indossa abiti comodi, senza bottoni o parti metalliche', 'Porta radiografie e MOC precedenti per il confronto'], ['Integratori di calcio nelle 24 ore prima della MOC', 'Esami con mezzo di contrasto nei giorni prima della MOC', 'Gioielli, piercing e oggetti metallici nella zona da esaminare'])}
  </div></section>

  {sez_faq([('Ogni quanto si ripete la MOC?', 'Di solito ogni 18–24 mesi, ma lo decide il medico in base al primo risultato.'), ('Le radiografie sono pericolose?', 'Le dosi sono basse e controllate. Avvisa sempre se sei in gravidanza.'), ('Serve l’impegnativa?', '<span class="segnaposto">Risposta da definire con lo studio</span>')])}
  {correlati('tomo', 'gin', 'visita')}
  {cta('Prenota il tuo esame', 'Chiama la segreteria: ti diciamo come prepararti e la prima data libera.', 'donna1.jpg')}
'''
pagina('radiologia.html', 'Radiologia · Avenir Medical Care', 'Densitometria ossea (MOC), radiografie e mammografia 3D a Roma.', 'Servizi', rad)

# =============================================================== CHI SIAMO
LOGO_GRANDE = '''<svg viewBox="0 0 220 150" role="img" aria-label="Il logo Avenir: una A blu attraversata da una curva rosa">
  <path d="M60 128 L110 18 L160 128" fill="none" stroke="#1f3a5f" stroke-width="9" data-disegna/>
  <path d="M66 117 C 82 82, 124 70, 151 95" fill="none" stroke="#c98a8f" stroke-width="6" stroke-linecap="round" data-disegna/>
  <text x="110" y="148" text-anchor="middle" font-family="Plus Jakarta Sans, sans-serif" font-size="13" letter-spacing="6" fill="#1f3a5f">AVENIR</text>
</svg>'''
ARCO_TOMO = '''<svg viewBox="0 0 220 150" role="img" aria-label="Schema della tomosintesi: il tubo radiogeno si sposta lungo un arco sopra il seno">
  <path d="M30 70 C 60 18, 160 18, 190 70" fill="none" stroke="#c98a8f" stroke-width="6" stroke-linecap="round" data-disegna/>
  <g fill="#1f3a5f"><circle cx="38" cy="58" r="5"/><circle cx="72" cy="32" r="5"/><circle cx="110" cy="25" r="6"/><circle cx="148" cy="32" r="5"/><circle cx="182" cy="58" r="5"/></g>
  <g stroke="#c98a8f" stroke-width="1" stroke-dasharray="3 4" opacity=".8"><path d="M110 31 L70 112"/><path d="M110 31 L150 112"/></g>
  <path d="M70 112 C 70 92, 150 92, 150 112 Z" fill="#fff" stroke="#1f3a5f" stroke-width="1.5"/>
  <g stroke="#1f3a5f" stroke-width="1" opacity=".35"><path d="M78 106 H142"/><path d="M84 100 H136"/></g>
  <rect x="55" y="114" width="110" height="10" rx="3" fill="#1f3a5f"/>
</svg>'''

chi = f"""
  {hero([('Home', 'index.html'), ('Chi siamo', None)], 'Chi siamo', 'Un poliambulatorio nuovo a Roma, nato per offrire alle donne un unico punto di riferimento per la prevenzione e la diagnosi.', 'pm-tomo.jpg', 'La sala mammografia con la postazione di refertazione')}

  <section class="sez"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Com’è nato</span>
      <h2 class="h2" data-split>Un solo centro per la salute della donna</h2>
      <p class="lead" data-su>Avenir nasce dall’idea di riunire in un unico luogo le visite e gli esami di cui una donna ha bisogno nel corso della vita: senologia, ginecologia e radiologia.</p>
      <p data-su style="margin-top:18px;color:var(--grigio);max-width:56ch">Medici specialisti con esperienza ospedaliera e tecnologia di ultima generazione, a partire dalla mammografia 3D con tomosintesi, per una prevenzione accurata, senza lunghe attese e con il tempo di spiegare ogni risultato.</p>
      <div class="righe">
        {riga('scudo', 'Prevenzione accurata', 'Esami di qualità e medici esperti')}
        {riga('cal', 'Tutto in una mattina', 'Visita ed esami nello stesso appuntamento, quando possibile')}
        {riga('cuore', 'Il tempo che serve', 'Ogni risultato spiegato con calma')}
      </div>
    </div>
    <div class="split-foto"><img src="assets/img/donna1.jpg" alt="Ritratto di una donna al tramonto" loading="lazy"></div>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap split">
    <div>
      <span class="sopra" data-su>Il nome e il logo</span>
      <h2 class="h2" data-split>Avenir vuol dire futuro</h2>
      <p class="citazione" data-scrub style="margin-top:24px">In francese avenir è il futuro. La curva rosa che attraversa la A è l’arco che il mammografo percorre durante la tomosintesi: guardare avanti, uno strato alla volta.</p>
    </div>
    <div class="logo-storia">
      <div class="logo-pannello">{LOGO_GRANDE}<small>Il logo: la A e la curva</small></div>
      <div class="logo-pannello cipria">{ARCO_TOMO}<small>La tomosintesi: il tubo scatta lungo un arco</small></div>
    </div>
  </div></section>

  <section class="sez" id="dove" style="padding-top:0"><div class="wrap split" style="align-items:stretch">
    <div>
      <span class="sopra" data-su>Dove siamo</span>
      <h2 class="h2" data-split>Nel cuore di Roma</h2>
      <p class="lead" data-su>Siamo in Viale Giuseppe Mazzini 142, nel quartiere Della Vittoria, a pochi minuti da Piazza Mazzini e dal quartiere Prati.</p>
      <div class="righe">
        {riga('pin', 'Viale Giuseppe Mazzini 142, Roma', 'Indirizzo da confermare')}
        {riga('scintilla', 'Con i mezzi', 'Metro A e autobus nelle vicinanze: indicazioni da completare')}
        {riga('cal', 'Orari e contatti', 'Telefono, WhatsApp e orari della segreteria', 'contatti.html')}
      </div>
    </div>
    <iframe class="mappa" title="Mappa: Viale Giuseppe Mazzini 142, Roma" src="https://maps.google.com/maps?q=Viale%20Giuseppe%20Mazzini%20142%20Roma&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div></section>

  <section class="sez" style="padding-top:0"><div class="wrap">
    {testa('I nostri valori', 'Quello in cui crediamo')}
    <div class="valori">
      <div class="dato" data-su>{ico('scudo')}<b>Esperienza</b><small>Medici specialisti con anni di attività ospedaliera.</small></div>
      <div class="dato" data-su>{ico('strati')}<b>Tecnologia</b><small>Strumenti di nuova generazione per immagini più chiare.</small></div>
      <div class="dato" data-su>{ico('cuore')}<b>Ascolto</b><small>Il tempo di spiegare, rispondere e rassicurare.</small></div>
      <div class="dato" data-su>{ico('scintilla')}<b>Prevenzione</b><small>Controlli regolari, per guardare avanti con serenità.</small></div>
    </div>
  </div></section>

  {cta('Vieni a conoscerci', 'Chiama la segreteria per fissare la tua prima visita.', 'donna4.jpg')}
"""
pagina('chi-siamo.html', 'Chi siamo · Avenir Medical Care', 'Avenir Medical Care: un poliambulatorio a Roma dedicato alla salute della donna.', 'chi-siamo.html', chi)

# =============================================================== CONTATTI
opzioni = ''.join(f'<option>{o}</option>' for o in ['Visita senologica', 'Mammografia 3D con tomosintesi', 'Ecografia mammaria', 'Visita + esami senologici', 'Visita ginecologica', 'Pap test / HPV test', 'Radiologia', 'Non lo so, ho bisogno di un consiglio'])
contatti = f'''
  {hero([('Home', 'index.html'), ('Contatti', None)], 'Contatti', 'Chiama, scrivi su WhatsApp o lascia il tuo numero: ti richiamiamo noi per fissare la visita.', azioni=False)}

  <section class="sez" style="padding-top:clamp(48px,6vw,80px)"><div class="wrap split" style="align-items:stretch">
    <div class="contatti-col">
      <div class="contatti-grid">
        <a class="contatto" href="{TEL_HREF}"><span class="riga-ico">{ico('tel')}</span><small>Telefono</small><b>{TEL}</b></a>
        <a class="contatto" href="#"><span class="riga-ico">{ico('msg')}</span><small>WhatsApp</small><b>000 000 0000</b></a>
        <a class="contatto" href="mailto:{EMAIL}"><span class="riga-ico">{ico('doc')}</span><small>Email</small><b>{EMAIL}</b></a>
        <div class="contatto"><span class="riga-ico">{ico('pin')}</span><small>Indirizzo</small><b>Viale Giuseppe Mazzini 142, Roma</b></div>
      </div>
      <div class="contatto"><span class="riga-ico">{ico('cal')}</span><small>Orari <span class="segnaposto">da confermare</span></small>
        <table class="orari"><tr><td>Lunedì – venerdì</td><td>9:00 – 19:00</td></tr><tr><td>Sabato</td><td>9:00 – 13:00</td></tr><tr><td>Domenica</td><td>Chiuso</td></tr></table></div>
      <p style="font-size:13px"><span class="segnaposto">Telefono, WhatsApp, email e orari sono segnaposto</span></p>
    </div>
    <iframe class="mappa" title="Mappa: Viale Giuseppe Mazzini 142, Roma" src="https://maps.google.com/maps?q=Viale%20Giuseppe%20Mazzini%20142%20Roma&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div></section>

  <section class="sez" id="prenota" style="padding-top:0"><div class="wrap split" style="align-items:start">
    <div>
      <span class="sopra" data-su>Prenota</span>
      <h2 class="h2" data-split>Ti richiamiamo noi</h2>
      <p class="lead" data-su>Lascia nome, telefono e l’esame che ti interessa: la segreteria ti richiama per fissare giorno e orario.</p>
      <div class="righe" style="margin-top:28px">
        {riga('tel', 'Preferisci chiamare?', TEL, TEL_HREF)}
        {riga('doc', 'Ricordati gli esami precedenti', 'Mammografie ed ecografie, anche su CD')}
      </div>
    </div>
    <form class="modulo" data-richiamo="{EMAIL}" data-su>
      <div class="campo"><label for="f-nome">Nome e cognome</label><input id="f-nome" name="nome" autocomplete="name" required></div>
      <div class="campo"><label for="f-tel">Telefono</label><input id="f-tel" name="telefono" type="tel" autocomplete="tel" required></div>
      <div class="campo pieno"><label for="f-esame">Esame</label><select id="f-esame" name="esame">{opzioni}</select></div>
      <div class="campo pieno"><label for="f-note">Note (facoltative)</label><textarea id="f-note" name="note" placeholder="Per esempio: preferisco il mattino"></textarea></div>
      <button class="btn" type="submit">Richiamami<span class="ico">{ico('freccia')}</span></button>
      <p class="nota">Si apre un’email già compilata per lo studio. <span class="segnaposto">Da collegare al sistema di prenotazione</span></p>
    </form>
  </div></section>
'''
pagina('contatti.html', 'Contatti · Avenir Medical Care', 'Telefono, indirizzo e orari di Avenir Medical Care a Roma.', 'contatti.html', contatti)
print('ok')
