// Header con bordo allo scroll + menu mobile accessibile
(() => {
  const header = document.querySelector('.header');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  const apri = document.querySelector('[data-menu-apri]');
  const menu = document.querySelector('.menu-mobile');
  if (apri && menu) {
    const chiudi = menu.querySelector('[data-menu-chiudi]');
    const open = () => { menu.hidden = false; apri.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; chiudi.focus(); };
    const close = () => { menu.hidden = true; apri.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; apri.focus(); };
    apri.addEventListener('click', open);
    chiudi.addEventListener('click', close);
    menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.hidden = true; document.body.style.overflow = ''; }));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !menu.hidden) close(); });
  }
})();
