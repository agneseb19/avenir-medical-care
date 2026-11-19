// Illustrazione schematica della tomosintesi: N strati di tessuto, un piccolo reperto
// visibile chiaramente solo nel suo strato. In 2D gli strati si sommano e lo nascondono.
// Non è un'immagine clinica: è uno schema didattico.
window.Strati = function (svg, { n = 9, strato = 5, seed = 7 } = {}) {
  const NS = 'http://www.w3.org/2000/svg';
  const el = (t, a = {}) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; };
  let s = seed;
  const rnd = () => { s |= 0; s = s + 0x6D2B79F5 | 0; let t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };

  svg.setAttribute('viewBox', '0 0 400 400');
  const DOME = 'M34 384 C34 196 112 116 200 112 C288 116 366 196 366 384 Z';
  const R = { x: 236, y: 250 }; // posizione del reperto

  const defs = el('defs');
  const clip = el('clipPath', { id: 'dome-clip' });
  clip.appendChild(el('path', { d: DOME }));
  defs.appendChild(clip);
  const blur = el('filter', { id: 'morbido', x: '-20%', y: '-20%', width: '140%', height: '140%' });
  blur.appendChild(el('feGaussianBlur', { stdDeviation: '1.4' }));
  defs.appendChild(blur);
  svg.appendChild(defs);

  // arco del tubo radiogeno (stessa curva del logo)
  const arco = el('path', { d: 'M60.5 81 A330 330 0 0 1 339.5 81', fill: 'none', stroke: 'var(--rosa)', 'stroke-width': 4, 'stroke-linecap': 'round', class: 'st-arco' });
  const raggi = el('g', { class: 'st-raggi', opacity: 0 });
  const r1 = el('line', { stroke: 'var(--rosa)', 'stroke-width': 1.2, 'stroke-dasharray': '3 5' });
  const r2 = r1.cloneNode();
  raggi.append(r1, r2);
  const tubo = el('circle', { r: 9, fill: 'var(--blu)', class: 'st-tubo', opacity: 0 });

  const base = el('path', { d: DOME, fill: '#fff', stroke: 'var(--linea)', 'stroke-width': 1.5 });
  svg.append(arco, raggi, base);

  const layers = [];
  for (let i = 0; i < n; i++) {
    const g = el('g', { class: 'st-layer' });
    const plate = el('path', { d: DOME, fill: '#fff', 'fill-opacity': 0, stroke: 'var(--blu)', 'stroke-opacity': 0, 'stroke-width': 1.2 });
    const content = el('g', { 'clip-path': 'url(#dome-clip)', filter: 'url(#morbido)' });
    // fibre che dalla parete toracica convergono verso l'alto
    for (let k = 0; k < 7; k++) {
      const x0 = 50 + rnd() * 300, x1 = 170 + rnd() * 60, cx = x0 + (rnd() - .5) * 120;
      content.appendChild(el('path', {
        d: `M${x0} 390 C${cx} ${300 - rnd() * 60} ${x1 + (rnd() - .5) * 80} ${200 - rnd() * 40} ${x1} ${128 + rnd() * 30}`,
        fill: 'none', stroke: 'var(--blu)', 'stroke-width': 6 + rnd() * 12, 'stroke-opacity': .1, 'stroke-linecap': 'round'
      }));
    }
    // lobuli
    for (let k = 0; k < 4; k++) {
      content.appendChild(el('ellipse', { cx: 80 + rnd() * 240, cy: 180 + rnd() * 180, rx: 18 + rnd() * 34, ry: 12 + rnd() * 26, fill: 'var(--blu)', 'fill-opacity': .09, transform: `rotate(${rnd() * 180} 200 260)` }));
    }
    // ogni strato tranne quello del reperto passa sopra il reperto: in 2D lo copre
    if (i !== strato) content.appendChild(el('ellipse', { cx: R.x + (rnd() - .5) * 30, cy: R.y + (rnd() - .5) * 30, rx: 22 + rnd() * 14, ry: 16 + rnd() * 10, fill: 'var(--blu)', 'fill-opacity': .14 }));
    g.append(plate, content);
    g._plate = plate;
    layers.push(g);
    svg.appendChild(g);
  }

  const reperto = el('g', { class: 'st-reperto' });
  reperto.append(
    el('circle', { cx: R.x, cy: R.y, r: 8, fill: 'var(--rosa-testo)' }),
    el('circle', { cx: R.x, cy: R.y, r: 20, fill: 'none', stroke: 'var(--rosa-testo)', 'stroke-width': 2, class: 'st-anello', opacity: 0 })
  );
  layers[strato].appendChild(reperto);
  svg.append(tubo);

  const api = {
    layers, reperto, strato, n,
    // tutti gli strati sommati: l'immagine 2D
    modo2D() {
      layers.forEach(g => { g.style.opacity = 1; g.style.transform = ''; g._plate.setAttribute('fill-opacity', 0); g._plate.setAttribute('stroke-opacity', 0); });
      reperto.style.opacity = .55;
      reperto.querySelector('.st-anello').setAttribute('opacity', 0);
    },
    // un solo strato visibile (k può essere decimale per lo scrub)
    mostraStrato(k) {
      layers.forEach((g, i) => {
        const d = Math.abs(i - k);
        g.style.opacity = Math.max(0, 1 - d * 1.1);
        g.style.transform = '';
        g._plate.setAttribute('fill-opacity', 0); g._plate.setAttribute('stroke-opacity', 0);
      });
      const vicino = Math.max(0, 1 - Math.abs(k - strato) * 1.4);
      reperto.style.opacity = 1;
      reperto.querySelector('.st-anello').setAttribute('opacity', vicino);
    },
    // strati separati come lastre (t: 0 impilati → 1 aperti)
    apri(t) {
      layers.forEach((g, i) => {
        const c = i - (n - 1) / 2;
        g.style.opacity = 1;
        g.style.transformOrigin = '200px 250px';
        g.style.transform = `translate(${c * 15 * t}px, ${-c * 13 * t}px) scale(${1 - .38 * t})`;
        g._plate.setAttribute('fill-opacity', .82 * t);
        g._plate.setAttribute('stroke-opacity', .35 * t);
      });
      reperto.style.opacity = .55 + .45 * t;
    },
    // posizione del tubo lungo l'arco (p: 0 → 1)
    tubo(p, visibile = 1) {
      const th = (-25 + 50 * p) * Math.PI / 180;
      const x = 200 + 330 * Math.sin(th), y = 380 - 330 * Math.cos(th);
      tubo.setAttribute('cx', x); tubo.setAttribute('cy', y); tubo.setAttribute('opacity', visibile);
      [[r1, 34], [r2, 366]].forEach(([l, bx]) => { l.setAttribute('x1', x); l.setAttribute('y1', y); l.setAttribute('x2', bx); l.setAttribute('y2', 384); });
      raggi.setAttribute('opacity', visibile * .9);
    }
  };
  api.modo2D();
  return api;
};
