import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

// ---- menu "Servizi" a tendina ----
const tBtn = document.querySelector('[data-tendina]');
if (tBtn) {
  const pan = document.getElementById(tBtn.getAttribute('aria-controls'));
  const set = v => { tBtn.setAttribute('aria-expanded', v); pan.hidden = !v; };
  tBtn.addEventListener('click', e => { e.stopPropagation(); set(pan.hidden); });
  document.addEventListener('click', e => { if (!pan.contains(e.target)) set(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !pan.hidden) { set(false); tBtn.focus(); } });
}

// ---- scena 3D ----
const sez = document.querySelector('[data-imm]');
const canvas = sez.querySelector('canvas');
const riduci = matchMedia('(prefers-reduced-motion: reduce)').matches;

let renderer;
try { renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true }); }
catch (e) {
  canvas.hidden = true;
  const fb = sez.querySelector('.imm-fallback'); fb.hidden = false;
  window.Strati(fb.querySelector('svg')).apri(1);
}

if (renderer) {
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  const gruppo = new THREE.Group(); scene.add(gruppo);

  const BLU = 0x1f3a5f, ROSA = 0xc4877c;
  const N = 11, TARGET = 6;

  // forma a cupola (vista dall'alto della mammella sul detettore)
  const forma = new THREE.Shape();
  forma.moveTo(-1.7, 0);
  forma.bezierCurveTo(-1.7, 1.6, -0.75, 2.2, 0, 2.25);
  forma.bezierCurveTo(0.75, 2.2, 1.7, 1.6, 1.7, 0);
  forma.lineTo(-1.7, 0);
  const geo = new THREE.ShapeGeometry(forma, 40);
  geo.rotateX(-Math.PI / 2); geo.translate(0, 0, 1.12);
  const contorno = new THREE.BufferGeometry().setFromPoints(forma.getPoints(60).map(p => new THREE.Vector3(p.x, 0, -p.y + 1.12)));

  let seed = 11;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  function texturaStrato(i) {
    const c = document.createElement('canvas'); c.width = c.height = 512;
    const g = c.getContext('2d');
    g.fillStyle = 'rgba(255,255,255,0.55)'; g.fillRect(0, 0, 512, 512);
    g.filter = 'blur(3px)'; g.lineCap = 'round';
    for (let k = 0; k < 8; k++) {
      const x0 = 40 + rnd() * 432, x1 = 220 + rnd() * 72;
      g.strokeStyle = `rgba(31,58,95,${0.1 + rnd() * 0.12})`; g.lineWidth = 10 + rnd() * 22;
      g.beginPath(); g.moveTo(x0, 520);
      g.bezierCurveTo(x0 + (rnd() - .5) * 160, 360 - rnd() * 80, x1 + (rnd() - .5) * 100, 160, x1, 30 + rnd() * 40); g.stroke();
    }
    for (let k = 0; k < 4; k++) {
      g.fillStyle = `rgba(31,58,95,${0.08 + rnd() * 0.1})`;
      g.beginPath(); g.ellipse(80 + rnd() * 350, 150 + rnd() * 300, 24 + rnd() * 40, 16 + rnd() * 30, rnd() * 3, 0, 7); g.fill();
    }
    const t = new THREE.CanvasTexture(c);
    t.colorSpace = THREE.SRGBColorSpace;
    t.repeat.set(1 / 3.4, 1 / 2.25); t.offset.set(0.5, 0);
    return t;
  }

  const strati = [];
  for (let i = 0; i < N; i++) {
    const m = new THREE.MeshBasicMaterial({ map: texturaStrato(i), transparent: true, opacity: .6, depthWrite: false, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geo, m);
    const linea = new THREE.Line(contorno, new THREE.LineBasicMaterial({ color: BLU, transparent: true, opacity: .25 }));
    const g = new THREE.Group(); g.add(mesh, linea); g.renderOrder = i;
    gruppo.add(g); strati.push({ g, m, l: linea.material });
  }
  // reperto sullo strato bersaglio
  const reperto = new THREE.Mesh(new THREE.SphereGeometry(.09, 24, 16), new THREE.MeshBasicMaterial({ color: 0x9a564c, transparent: true }));
  reperto.position.set(.45, .05, -.15);
  const anello = new THREE.Mesh(new THREE.RingGeometry(.2, .235, 48), new THREE.MeshBasicMaterial({ color: 0x9a564c, transparent: true, opacity: 0, side: THREE.DoubleSide }));
  anello.rotation.x = -Math.PI / 2; anello.position.copy(reperto.position);
  strati[TARGET].g.add(reperto, anello);

  // detettore (il piano nero del mammografo)
  const det = new THREE.Mesh(new THREE.BoxGeometry(3.9, .14, 2.6), new THREE.MeshBasicMaterial({ color: 0x2c3a4b }));
  det.position.set(0, -.16, 0); gruppo.add(det);
  const detBordo = new THREE.LineSegments(new THREE.EdgesGeometry(det.geometry), new THREE.LineBasicMaterial({ color: 0x3e5065 }));
  detBordo.position.copy(det.position); gruppo.add(detBordo);

  // arco del tubo: la curva del logo
  const R = 3.7, ARCO = 50 * Math.PI / 180, CY = -.3;
  const arco = new THREE.Mesh(new THREE.TorusGeometry(R, .028, 8, 140, ARCO), new THREE.MeshBasicMaterial({ color: ROSA }));
  arco.rotation.z = Math.PI / 2 - ARCO / 2; arco.position.y = CY; gruppo.add(arco);
  const tubo = new THREE.Mesh(new THREE.SphereGeometry(.13, 24, 16), new THREE.MeshBasicMaterial({ color: BLU }));
  gruppo.add(tubo);
  const raggiGeo = new THREE.BufferGeometry().setAttribute('position', new THREE.Float32BufferAttribute(new Array(12).fill(0), 3));
  const raggi = new THREE.LineSegments(raggiGeo, new THREE.LineBasicMaterial({ color: ROSA, transparent: true, opacity: 0 }));
  gruppo.add(raggi);

  // stato animato con smorzamento
  const S = { gap: .02, sweep: .5, raggi: 0, focus: 0, theta: .6, el: .5, r: 12.5 };
  const T = { ...S };
  const seg = (t, a, b) => Math.min(1, Math.max(0, (t - a) / (b - a)));
  const mix = (a, b, t) => a + (b - a) * t;
  const ease = t => t * t * (3 - 2 * t);

  function obiettivi(time) {
    const r = sez.getBoundingClientRect();
    const t = seg(-r.top, 0, sez.offsetHeight - innerHeight);
    const a = ease(seg(t, .12, .36)), b = ease(seg(t, .4, .62)), c = ease(seg(t, .68, .86));
    const idle = riduci ? .5 : .5 + Math.sin(time * .0006) * .5;
    T.sweep = t < .12 ? idle : (t < .36 ? a : 1 - b * .5);
    T.raggi = t < .12 ? .35 : (t < .4 ? .9 : .9 * (1 - b));
    T.gap = mix(.025, .3, b);
    T.focus = c;
    T.theta = mix(mix(.6, .15, a), -.45, b);
    T.el = mix(.5, .36, b) + c * .12;
    T.r = mix(12.5, 11.8, b) - c * .8;
  }

  let zoom = 1;
  function dimensiona() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    // su schermi larghi la scena sta a destra del testo; su telefono sta in alto
    const largo = w / h > 1.1;
    zoom = largo ? 1 : Math.min(2.1, 1.25 / (w / h));
    if (largo) camera.setViewOffset(w, h, -w * 0.22, 0, w, h);
    else camera.setViewOffset(w, h, 0, h * 0.16, w, h);
  }
  addEventListener('resize', dimensiona); dimensiona();

  const pos = raggiGeo.attributes.position;
  function frame(time) {
    obiettivi(time);
    const k = riduci ? 1 : .09;
    for (const key in S) S[key] += (T[key] - S[key]) * k;

    const ang = Math.PI / 2 + (S.sweep - .5) * ARCO;
    tubo.position.set(R * Math.cos(ang), CY + R * Math.sin(ang), 0);
    const top = (N - 1) * S.gap;
    [[-1.7, 1.12], [1.7, 1.12]].forEach(([x, z], i) => {
      pos.setXYZ(i * 2, tubo.position.x, tubo.position.y, 0);
      pos.setXYZ(i * 2 + 1, x, top, i ? -1.1 : z);
    });
    pos.needsUpdate = true;
    raggi.material.opacity = S.raggi * .8;

    strati.forEach((s, i) => {
      const isT = i === TARGET;
      s.g.position.y = i * S.gap + (isT ? S.focus * .25 : 0);
      s.m.opacity = isT ? mix(.6, 1, S.focus) : mix(.6, .05, S.focus);
      s.l.opacity = isT ? mix(.25, .9, S.focus) : mix(.25, .03, S.focus);
    });
    reperto.material.opacity = mix(.5, 1, S.focus);
    anello.material.opacity = S.focus;
    anello.scale.setScalar(1 + (riduci ? 0 : Math.sin(time * .004) * .08 * S.focus));

    const rr = S.r * zoom;
    const cx = rr * Math.sin(S.theta) * Math.cos(S.el), cy = rr * Math.sin(S.el), cz = rr * Math.cos(S.theta) * Math.cos(S.el);
    const tgt = new THREE.Vector3(0, 1.3, 0);
    camera.position.set(tgt.x + cx, tgt.y + cy, cz);
    camera.lookAt(tgt);
    renderer.render(scene, camera);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}
