// Avenir: interazioni e animazioni (GSAP + ScrollTrigger + Lenis)
(() => {
  const riduci = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- navbar ---------- */
  const nav = $('#nav');
  const compatta = () => nav && nav.classList.toggle('compatta', scrollY > 40);
  addEventListener('scroll', compatta, { passive: true }); compatta();

  $$('[data-tendina]').forEach(t => {
    const b = $('button', t);
    let timer;
    const set = v => { t.classList.toggle('aperto', v); b.setAttribute('aria-expanded', v); };
    b.addEventListener('click', e => { e.stopPropagation(); set(!t.classList.contains('aperto')); });
    t.addEventListener('mouseenter', () => { clearTimeout(timer); set(true); });
    t.addEventListener('mouseleave', () => { timer = setTimeout(() => set(false), 180); });
    document.addEventListener('click', e => { if (!t.contains(e.target)) set(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
  });

  const burger = $('.burger'), menu = $('#menu-mob');
  if (burger) burger.addEventListener('click', () => {
    const v = !menu.classList.contains('aperto');
    menu.classList.toggle('aperto', v);
    burger.setAttribute('aria-expanded', v);
    burger.setAttribute('aria-label', v ? 'Chiudi il menu' : 'Apri il menu');
    document.documentElement.style.overflow = v ? 'hidden' : '';
    if (v && window.gsap && !riduci) gsap.from($$('nav a', menu), { y: 40, opacity: 0, stagger: .06, duration: .7, ease: 'expo.out', delay: .2 });
  });

  /* ---------- prova 2D / 3D ---------- */
  $$('[data-prova]').forEach(box => {
    if (!window.Strati) return;
    const st = Strati($('svg', box));
    const tabs = $$('[data-modo]', box), wrapTab = $('.prova-tab', box);
    const cur = $('[data-cursore]', box), testo = $('[data-testo2d]', box);
    const range = $('input', cur), out = $('[data-out]', cur);
    const aggiorna = () => { const k = +range.value; st.mostraStrato(k - 1); out.textContent = k - 1 === st.strato ? `Strato ${k} di 9: eccolo` : `Strato ${k} di 9`; };
    tabs.forEach(t => t.addEventListener('click', () => {
      const tre = t.dataset.modo === '3d';
      tabs.forEach(x => x.setAttribute('aria-selected', x === t));
      wrapTab.classList.toggle('tre', tre);
      cur.hidden = !tre; testo.hidden = tre;
      if (tre) { range.value = 1; aggiorna(); } else st.modo2D();
    }));
    range.addEventListener('input', aggiorna);
  });

  /* ---------- storia della tomosintesi (pagina mammografia) ---------- */
  const storia = $('[data-storia]');
  if (storia && window.Strati) {
    const st = Strati($('.storia-fig svg', storia));
    const passi = $$('.storia-passo', storia), barre = $$('.storia-barre b', storia);
    const soglie = [0, .16, .38, .6, .84];
    const seg = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
    let attivo = -1, coda = false;
    const disegna = () => {
      coda = false;
      const r = storia.getBoundingClientRect();
      const t = seg(-r.top, 0, storia.offsetHeight - innerHeight);
      let p = 0; soglie.forEach((s, i) => { if (t >= s) p = i; });
      if (p !== attivo) { passi.forEach((el, i) => el.classList.toggle('attivo', i === p)); attivo = p; }
      barre.forEach((b, i) => { const a = soglie[i], z = soglie[i + 1] ?? 1; b.style.transform = `scaleX(${seg(t, a, z)})`; });
      if (p === 0) { st.modo2D(); st.tubo(0, 0); }
      else if (p === 1) { st.modo2D(); st.tubo(seg(t, .16, .36), 1); }
      else if (p === 2) { st.tubo(1, 0); st.apri(seg(t, .38, .54)); }
      else if (p === 3) { st.tubo(1, 0); st.mostraStrato(seg(t, .62, .82) * st.strato); }
      else { st.tubo(1, 0); st.mostraStrato(st.strato); }
    };
    addEventListener('scroll', () => { if (!coda) { coda = true; requestAnimationFrame(disegna); } }, { passive: true });
    addEventListener('resize', disegna); disegna();
  }

  /* ---------- modulo: prepara un'email per lo studio ---------- */
  $$('[data-richiamo]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const d = new FormData(f);
    const corpo = `Buongiorno,\nvorrei essere richiamata per prenotare.\n\nNome: ${d.get('nome')}\nTelefono: ${d.get('telefono')}\nEsame: ${d.get('esame')}\nNote: ${d.get('note') || '-'}`;
    location.href = `mailto:${f.dataset.richiamo}?subject=${encodeURIComponent('Richiesta di appuntamento')}&body=${encodeURIComponent(corpo)}`;
  }));

  if (!window.gsap || riduci) return;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- scroll morbido ---------- */
  if (window.Lenis && !matchMedia('(pointer: coarse)').matches) {
    const lenis = new Lenis({ lerp: 0.1 });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(t => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => { const id = a.getAttribute('href'); if (id.length > 1 && $(id)) { e.preventDefault(); lenis.scrollTo(id, { offset: -100 }); } }));
  }

  /* ---------- titoli: parole che salgono ---------- */
  $$('[data-split]').forEach(el => {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(w => `<span class="parola"><span>${w}</span></span>`).join(' ');
  });

  /* ---------- hero ---------- */
  const R = matchMedia('(max-width: 760px)').matches ? '0px' : '999px 999px 28px 28px';
  const tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  tl.from('.hero-box', { scale: .965, opacity: 0, duration: 1.2 })
    .from('.hero [data-split] .parola > span', { yPercent: 110, duration: 1.1, stagger: .045 }, .25)
    .from('.hero [data-h]', { y: 22, opacity: 0, duration: .9, stagger: .09 }, .45)
    .fromTo('.hero-foto', { clipPath: `inset(100% 0% 0% 0% round ${R})` }, { clipPath: `inset(0% 0% 0% 0% round ${R})`, duration: 1.4, ease: 'power4.inOut' }, .2)
    .from('.hero-foto img', { scale: 1.3, duration: 1.8 }, .2)
    ;
  const arco = $('.hero-arco path');
  if (arco) { const L = arco.getTotalLength(); gsap.fromTo(arco, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, duration: 2, ease: 'power2.inOut', delay: .6 }); }

  $$('[data-fluttua]').forEach((el, i) => gsap.to(el, { y: i ? -10 : 10, duration: 3 + i, ease: 'sine.inOut', repeat: -1, yoyo: true, delay: 2 }));
  gsap.to('.hero-foto img', { yPercent: -12, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
  gsap.to('.hero-box', { scale: .97, borderRadius: 56, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });

  /* ---------- titoli fuori dall'hero ---------- */
  $$('[data-split]').forEach(el => {
    if (el.closest('.hero')) return;
    gsap.from($$('.parola > span', el), { yPercent: 110, duration: 1, ease: 'expo.out', stagger: .05, scrollTrigger: { trigger: el, start: 'top 88%' } });
  });

  /* ---------- entrate ---------- */
  ScrollTrigger.batch($$('[data-su]').filter(el => !el.closest('.hero') && !el.matches('.card, .fase, .riga, .gruppo, .contatto, .dato')), {
    start: 'top 90%', once: true,
    onEnter: b => gsap.fromTo(b, { y: 34, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'expo.out', stagger: .08, overwrite: 'auto', clearProps: 'transform,opacity' })
  });

  /* ---------- frase che si accende parola per parola ---------- */
  $$('[data-scrub]').forEach(el => {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(w => `<span class="p">${w}</span>`).join(' ');
    gsap.fromTo($$('.p', el), { opacity: .15 }, { opacity: 1, stagger: .1, ease: 'none', scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 45%', scrub: true } });
  });

  /* ---------- parallasse ---------- */
  $$('[data-par]').forEach(el => {
    const v = +el.dataset.par;
    const img = $('img', el) || el;
    gsap.fromTo(img, { yPercent: -v }, { yPercent: v, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
  });
  $$('.intro-foto figure').forEach((f, i) => gsap.from(f, { clipPath: 'inset(0 0 100% 0)', duration: 1.4, ease: 'power4.inOut', delay: i * .2, scrollTrigger: { trigger: '.intro-foto', start: 'top 80%' } }));

  /* ---------- servizi: scorrimento orizzontale bloccato ---------- */
  const oriz = $('.oriz');
  if (oriz && matchMedia('(min-width: 861px)').matches) {
    oriz.classList.add('pinnato');
    const track = $('.oriz-track', oriz);
    const dist = () => Math.max(0, track.scrollWidth - innerWidth);
    const corsa = gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: { trigger: oriz, pin: true, scrub: .8, start: 'top top', end: () => '+=' + dist(), invalidateOnRefresh: true, onUpdate: s => gsap.set('.oriz-barra i', { scaleX: s.progress }) } });
    $$('.oc', track).forEach(card => {
      gsap.from(card, { rotate: 5, y: 70, scale: .92, ease: 'none', scrollTrigger: { containerAnimation: corsa, trigger: card, start: 'left 105%', end: 'left 65%', scrub: true } });
      const img = $('.oc-f img', card);
      if (img) gsap.fromTo(img, { xPercent: 7 }, { xPercent: -7, ease: 'none', scrollTrigger: { containerAnimation: corsa, trigger: card, start: 'left right', end: 'right left', scrub: true } });
    });
  } else if (oriz) {
    gsap.from($$('.oc', oriz), { x: 80, opacity: 0, duration: 1.1, ease: 'expo.out', stagger: .1, scrollTrigger: { trigger: oriz, start: 'top 75%' } });
  }

  /* ---------- tomosintesi ---------- */
  gsap.from('.tomo', { clipPath: 'inset(8% 6% 8% 6% round 40px)', ease: 'none', scrollTrigger: { trigger: '.tomo', start: 'top bottom', end: 'top 35%', scrub: true } });

  /* ---------- passi: la linea si riempie ---------- */
  const linea = $('.passi-linea i');
  if (linea) gsap.to(linea, { scaleX: 1, ease: 'none', scrollTrigger: { trigger: '[data-passi]', start: 'top 75%', end: 'bottom 60%', scrub: true } });

  /* ---------- CTA ---------- */
  gsap.from('.cta', { scale: .94, borderRadius: 80, ease: 'none', scrollTrigger: { trigger: '.cta', start: 'top bottom', end: 'top 40%', scrub: true } });

  /* ---------- nome nel footer, lettera per lettera ---------- */
  const g = $('[data-gigante]');
  if (g) {
    g.innerHTML = [...g.textContent].map(l => `<span style="display:inline-block">${l}</span>`).join('');
    gsap.from($$('span', g), { yPercent: 100, opacity: 0, duration: 1.2, ease: 'expo.out', stagger: .06, scrollTrigger: { trigger: g, start: 'top 95%' } });
  }

  /* ---------- pulsanti magnetici ---------- */
  if (matchMedia('(pointer: fine)').matches) $$('[data-magnete]').forEach(b => {
    const xTo = gsap.quickTo(b, 'x', { duration: .5, ease: 'power3' }), yTo = gsap.quickTo(b, 'y', { duration: .5, ease: 'power3' });
    b.addEventListener('mousemove', e => { const r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * .25); yTo((e.clientY - r.top - r.height / 2) * .35); });
    b.addEventListener('mouseleave', () => { xTo(0); yTo(0); });
  });

  /* ---------- logo e arco che si disegnano ---------- */
  $$('[data-disegna]').forEach((p, i) => {
    const L = p.getTotalLength();
    gsap.fromTo(p, { strokeDasharray: L, strokeDashoffset: L }, { strokeDashoffset: 0, ease: 'none', scrollTrigger: { trigger: p.closest('svg'), start: 'top 85%', end: 'top 35%', scrub: true } });
  });
  $$('.logo-storia circle').forEach((c, i) => gsap.from(c, { scale: 0, transformOrigin: 'center', duration: .6, ease: 'back.out(2)', delay: i * .12, scrollTrigger: { trigger: c.closest('svg'), start: 'top 60%' } }));

  /* ---------- linea del tempo che si riempie ---------- */
  const tempo = $('[data-tempo]');
  if (tempo) gsap.to('.tempo-linea i', { scaleY: 1, ease: 'none', scrollTrigger: { trigger: tempo, start: 'top 70%', end: 'bottom 60%', scrub: true } });

  /* ---------- entrate per griglie e righe ---------- */
  ScrollTrigger.batch('.card, .fase, .riga, .gruppo, .contatto, .dato, .faq details, .tappa', { start: 'top 92%', once: true, onEnter: b => gsap.fromTo(b, { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 1, ease: 'expo.out', stagger: .08, overwrite: 'auto', clearProps: 'transform,opacity' }) });
  $$('.split-foto, .card-f').forEach(f => gsap.fromTo($('img', f), { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: f, start: 'top bottom', end: 'bottom top', scrub: true } }));
  $$('.split-foto').forEach(f => gsap.from(f, { clipPath: 'inset(100% 0 0 0 round 32px)', duration: 1.4, ease: 'power4.inOut', scrollTrigger: { trigger: f, start: 'top 85%' } }));
  if ($('.scuro')) gsap.from('.scuro', { clipPath: 'inset(6% 5% 6% 5% round 40px)', ease: 'none', scrollTrigger: { trigger: '.scuro', start: 'top bottom', end: 'top 40%', scrub: true } });

  addEventListener('load', () => ScrollTrigger.refresh());
})();
