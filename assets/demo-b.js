// Sezione guidata dallo scroll: il racconto avanza con lo scorrimento della pagina
(() => {
  const sez = document.querySelector('[data-storia]');
  if (!sez) return;
  const st = Strati(sez.querySelector('svg'));
  const passi = sez.querySelectorAll('.passo');
  const barre = sez.querySelectorAll('.avanzamento li');
  const soglie = [0, .14, .36, .58, .84];
  const seg = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
  let attivo = -1, tick = false;

  function render() {
    tick = false;
    const r = sez.getBoundingClientRect();
    const t = seg(-r.top, 0, sez.offsetHeight - innerHeight);
    let p = 0; soglie.forEach((s, i) => { if (t >= s) p = i; });
    if (p !== attivo) {
      passi.forEach((el, i) => el.classList.toggle('attivo', i === p));
      barre.forEach((el, i) => el.classList.toggle('fatto', i <= p));
      attivo = p;
    }
    if (p === 0) { st.modo2D(); st.tubo(0, 0); }
    else if (p === 1) { st.modo2D(); st.tubo(seg(t, .14, .34), 1); }
    else if (p === 2) { st.tubo(1, 0); st.apri(seg(t, .36, .52)); }
    else if (p === 3) { st.tubo(1, 0); st.mostraStrato(seg(t, .6, .82) * st.strato); }
    else { st.tubo(1, 0); st.mostraStrato(st.strato); }
  }
  addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(render); } }, { passive: true });
  addEventListener('resize', render);
  render();
})();
