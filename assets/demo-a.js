// Confronto 2D / strati 3D: interazione attivata dall'utente
document.querySelectorAll('[data-confronto]').forEach(box => {
  const st = Strati(box.querySelector('svg'));
  const tabs = box.querySelectorAll('[data-modo]');
  const cur = box.querySelector('[data-cursore]');
  const did = box.querySelector('[data-did-2d]');
  const range = cur.querySelector('input');
  const out = cur.querySelector('[data-out]');
  const aggiorna = () => {
    const k = +range.value;
    st.mostraStrato(k - 1);
    out.textContent = k - 1 === st.strato ? `Strato ${k} di 9: eccolo` : `Strato ${k} di 9`;
  };
  tabs.forEach(t => t.addEventListener('click', () => {
    const tre = t.dataset.modo === '3d';
    tabs.forEach(x => x.setAttribute('aria-selected', x === t));
    cur.hidden = !tre; did.hidden = tre;
    tre ? aggiorna() : st.modo2D();
  }));
  range.addEventListener('input', aggiorna);
});
