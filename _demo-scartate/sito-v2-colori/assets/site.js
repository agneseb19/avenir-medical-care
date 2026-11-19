// Avenir: livello di movimento e interazioni
(() => {
  const riduci = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const touch = matchMedia('(pointer: coarse)').matches;

  // scorrimento morbido, solo con mouse e movimento consentito
  if (window.Lenis && !riduci && !touch) {
    const lenis = new Lenis({ lerp: 0.12 });
    const raf = t => { lenis.raf(t); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }

  // barra: prende il colore del capitolo sotto di sé, si nasconde scendendo
  const bar = document.querySelector('.bar');
  const campi = [...document.querySelectorAll('[data-campo]')];
  let ultimoY = scrollY, inCoda = false;
  const aggiornaBar = () => {
    inCoda = false;
    const y = scrollY;
    if (bar) {
      bar.classList.toggle('nascosta', y > 160 && y > ultimoY && !document.querySelector('.menu.aperto'));
      const sotto = campi.find(c => { const r = c.getBoundingClientRect(); return r.top <= 42 && r.bottom > 42; });
      const campo = sotto ? sotto.dataset.campo : bar.dataset.base;
      if (bar.dataset.ora !== campo) {
        bar.classList.remove('f-bianco', 'f-cipria', 'f-rosa', 'f-blu', 'f-notte');
        bar.classList.add('f-' + campo);
        bar.dataset.ora = campo;
      }
    }
    ultimoY = y;
  };
  addEventListener('scroll', () => { if (!inCoda) { inCoda = true; requestAnimationFrame(aggiornaBar); } }, { passive: true });
  aggiornaBar();

  // menu su telefono
  const menu = document.querySelector('.menu');
  document.querySelectorAll('[data-menu]').forEach(b => b.addEventListener('click', () => {
    const apri = !menu.classList.contains('aperto');
    menu.classList.toggle('aperto', apri);
    document.querySelectorAll('[data-menu]').forEach(x => x.setAttribute('aria-expanded', apri));
    document.body.style.overflow = apri ? 'hidden' : '';
    if (apri) menu.querySelector('a').focus();
  }));
  addEventListener('keydown', e => { if (e.key === 'Escape' && menu?.classList.contains('aperto')) document.querySelector('.menu [data-menu]').click(); });

  // entrate al passaggio, una volta sola
  // un elemento chiuso da clip-path non risulta mai visibile: per quelli si osserva il contenitore
  const bersagli = new Map();
  const io = new IntersectionObserver(voci => voci.forEach(v => {
    if (!v.isIntersecting) return;
    (bersagli.get(v.target) || [v.target]).forEach(el => el.classList.add('dentro'));
    io.unobserve(v.target);
  }), { rootMargin: '0px 0px -10% 0px', threshold: 0.05 });
  document.querySelectorAll('[data-rivela], [data-riga]').forEach(el => io.observe(el));
  document.querySelectorAll('[data-apri]').forEach(el => {
    const c = el.parentElement;
    if (!bersagli.has(c)) { bersagli.set(c, []); io.observe(c); }
    bersagli.get(c).push(el);
  });

  // enunciato che si riempie parola per parola
  if (CSS.supports('animation-timeline: view()') && !riduci) {
    document.querySelectorAll('.riempi').forEach(el => {
      const parole = el.textContent.trim().split(/\s+/);
      el.textContent = '';
      parole.forEach((p, i) => { const s = document.createElement('span'); s.textContent = p; el.append(s, i < parole.length - 1 ? ' ' : ''); });
      el.classList.add('pronto');
    });
  }

  // schede degli esami
  document.querySelectorAll('[data-schede]').forEach(box => {
    const tabs = [...box.querySelectorAll('[role="tab"]')];
    const imgs = [...box.querySelectorAll('.piatto img')];
    const scegli = (t, focus) => {
      tabs.forEach((x, i) => {
        const on = x === t;
        x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1;
        document.getElementById(x.getAttribute('aria-controls')).hidden = !on;
        imgs[i]?.classList.toggle('attiva', on);
      });
      if (focus) t.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => scegli(t));
      t.addEventListener('keydown', e => {
        const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) scegli(tabs[(i + d + tabs.length) % tabs.length], true);
      });
    });
  });

  // fisarmonica dei passi
  document.querySelectorAll('[data-fisa]').forEach(f => {
    const voci = [...f.querySelectorAll('.fisa-voce')];
    voci.forEach(v => v.querySelector('button').addEventListener('click', () => {
      voci.forEach(x => { const on = x === v; x.classList.toggle('aperta', on); x.querySelector('button').setAttribute('aria-expanded', on); });
    }));
  });

  // striscia di foto: ferma quando non si vede
  document.querySelectorAll('.striscia-traccia').forEach(t => {
    new IntersectionObserver(([e]) => { t.style.animationPlayState = e.isIntersecting ? '' : 'paused'; }).observe(t);
  });

  // "ti richiamiamo noi": prepara un'email con i dati inseriti
  document.querySelectorAll('[data-richiamo]').forEach(form => form.addEventListener('submit', e => {
    e.preventDefault();
    const d = new FormData(form);
    const corpo = `Buongiorno, vorrei essere richiamata per prenotare una visita.\n\nNome: ${d.get('nome')}\nTelefono: ${d.get('telefono')}`;
    location.href = `mailto:${form.dataset.richiamo}?subject=${encodeURIComponent('Richiesta di appuntamento')}&body=${encodeURIComponent(corpo)}`;
  }));

  // storia della tomosintesi guidata dallo scroll
  const storia = document.querySelector('[data-storia]');
  if (storia && window.Strati) {
    const st = Strati(storia.querySelector('svg'));
    const passi = storia.querySelectorAll('.storia-passo');
    const conta = storia.querySelector('.storia-conta');
    const soglie = [0, .14, .36, .58, .84];
    const seg = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
    let attivo = -1, coda = false;
    const disegna = () => {
      coda = false;
      const r = storia.getBoundingClientRect();
      const t = seg(-r.top, 0, storia.offsetHeight - innerHeight);
      let p = 0; soglie.forEach((s, i) => { if (t >= s) p = i; });
      if (p !== attivo) {
        passi.forEach((el, i) => el.classList.toggle('attivo', i === p));
        if (conta) conta.textContent = `${p + 1} di ${passi.length}`;
        attivo = p;
      }
      if (p === 0) { st.modo2D(); st.tubo(0, 0); }
      else if (p === 1) { st.modo2D(); st.tubo(seg(t, .14, .34), 1); }
      else if (p === 2) { st.tubo(1, 0); st.apri(seg(t, .36, .52)); }
      else if (p === 3) { st.tubo(1, 0); st.mostraStrato(seg(t, .6, .82) * st.strato); }
      else { st.tubo(1, 0); st.mostraStrato(st.strato); }
    };
    addEventListener('scroll', () => { if (!coda) { coda = true; requestAnimationFrame(disegna); } }, { passive: true });
    addEventListener('resize', disegna);
    disegna();
  }
})();
