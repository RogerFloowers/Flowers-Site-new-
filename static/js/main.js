
// ── INTRO SPLASH ─────────────────────────────────────────────────────────────
(function(){
  document.body.classList.add('intro-active');

  const splash = document.getElementById('intro-splash');

  setTimeout(()=>{
    if(splash) splash.classList.add('hide');
    document.body.classList.remove('intro-active');
    document.body.classList.add('intro-done');
    document.querySelectorAll('.hero-main-title, .hero-content').forEach(el=>{
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity .9s ease, transform .9s ease';
      setTimeout(()=>{ el.style.opacity='1'; el.style.transform='none'; }, 80);
    });
  }, 3000);
})();


// ── LIGHTBOX ──────────────────────────────────────────────
let lbPhotos = [];
let lbIndex  = 0;

function buildPhotoList() {
  lbPhotos = Array.from(document.querySelectorAll('.fotos-grid .foto-card img'))
                  .map(img => img.src);
}

function openLightbox(src, idx) {
  buildPhotoList();
  lbIndex = idx;
  document.getElementById('lightbox').classList.add('open');
  document.getElementById('lightbox-img').src = lbPhotos[lbIndex] || src;
  updateCounter();
  document.body.style.overflow = 'hidden';
}

function closeLightbox(e) {
  if (e && e.target !== document.getElementById('lightbox') &&
      e.target !== document.querySelector('.lightbox-close')) return;
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}

function lbMove(dir) {
  lbIndex = (lbIndex + dir + lbPhotos.length) % lbPhotos.length;
  const img = document.getElementById('lightbox-img');
  img.style.opacity = '0';
  setTimeout(() => {
    img.src = lbPhotos[lbIndex];
    img.style.opacity = '1';
    updateCounter();
  }, 150);
}

function updateCounter() {
  document.getElementById('lightbox-counter').textContent =
    (lbIndex + 1) + ' / ' + lbPhotos.length;
}

document.addEventListener('keydown', e => {
  const lb = document.getElementById('lightbox');
  if (!lb || !lb.classList.contains('open')) return;
  if (e.key === 'ArrowRight') lbMove(1);
  if (e.key === 'ArrowLeft')  lbMove(-1);
  if (e.key === 'Escape')     { lb.classList.remove('open'); document.body.style.overflow = ''; }
});


// ── CARROSSEL INFINITO CLIENTES ──────────────────────────────────────────────
(function(){
  const track = document.getElementById('carrossel-clientes');
  if(!track) return;

  const dotsWrap = document.getElementById('carrossel-dots');
  if(dotsWrap) dotsWrap.style.display = 'none';

  // Clona os slides para criar loop infinito
  const slides = Array.from(track.querySelectorAll('.carrossel-slide'));
  if(slides.length === 0) return;

  // Duplica 3x para garantir loop suave
  slides.forEach(s => track.appendChild(s.cloneNode(true)));
  slides.forEach(s => track.appendChild(s.cloneNode(true)));

  const perView  = () => window.innerWidth < 600 ? 3 : window.innerWidth < 900 ? 2 : 4;
  const slideW   = () => 100 / (slides.length * 3) * perView();
  let pos        = 0;
  let rafId      = null;
  let paused     = false;
  const SPEED    = 0.045; // menor = mais lento

  // Largura de um slide em %
  const totalSlides = () => track.querySelectorAll('.carrossel-slide').length;

  function step(){
    if(!paused){
      pos += SPEED;
      // Quando chegou ao fim do primeiro grupo, volta pro começo sem transição
      const oneGroup = (slides.length / totalSlides()) * 100 / perView() * slides.length;
      const reset    = 100 / perView() * slides.length;
      if(pos >= reset){
        pos = 0;
      }
      track.style.transform = `translateX(-${pos}%)`;
    }
    rafId = requestAnimationFrame(step);
  }

  // ── DRAG (desktop) ──
  let dragging = false;
  let dragStartX = 0;
  let dragStartPos = 0;

  track.addEventListener('mousedown', e=>{
    dragging    = true;
    paused      = true;
    dragStartX  = e.clientX;
    dragStartPos= pos;
    track.style.cursor = 'grabbing';
    e.preventDefault();
  });
  window.addEventListener('mousemove', e=>{
    if(!dragging) return;
    const dx    = e.clientX - dragStartX;
    const pxPer = track.parentElement.offsetWidth;
    pos = dragStartPos - (dx / pxPer) * perView() * (100 / slides.length / 3) * slides.length;
    // Mantém dentro do range
    const reset = 100 / perView() * slides.length;
    if(pos < 0)     pos += reset;
    if(pos >= reset) pos -= reset;
    track.style.transform = `translateX(-${pos}%)`;
  });
  window.addEventListener('mouseup', ()=>{
    if(!dragging) return;
    dragging = false;
    paused   = false;
    track.style.cursor = 'grab';
  });
  track.style.cursor = 'grab';

  // ── SWIPE (mobile) ──
  let tx = 0, ty = 0, tStartPos = 0, isSwiping = false;

  track.addEventListener('touchstart', e=>{
    tx        = e.touches[0].clientX;
    ty        = e.touches[0].clientY;
    tStartPos = pos;
    isSwiping = false;
    paused    = true;
  },{passive:true});

  track.addEventListener('touchmove', e=>{
    const dx = e.touches[0].clientX - tx;
    const dy = e.touches[0].clientY - ty;

    // Detecta se é swipe horizontal (ignora scroll vertical)
    if(!isSwiping && Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 6){
      isSwiping = true;
    }
    if(!isSwiping) return;

    // Previne scroll da página durante swipe horizontal
    e.preventDefault();

    const pxPer  = track.parentElement.offsetWidth;
    const factor = (100 / slides.length) * 1.5; // mais sensível
    pos = tStartPos - (dx / pxPer) * factor;
    const reset  = 100 / perView() * slides.length;
    if(pos < 0)      pos += reset;
    if(pos >= reset) pos -= reset;
    track.style.transform = `translateX(-${pos}%)`;
  },{passive:false});

  track.addEventListener('touchend', ()=>{
    isSwiping = false;
    setTimeout(()=>{ paused = false; }, 600);
  },{passive:true});

  track.addEventListener('mouseenter', ()=>{ if(!dragging) paused = true; });
  track.addEventListener('mouseleave', ()=>{ if(!dragging) paused = false; });

  // Garante que cada slide ocupa a largura certa
  function setWidths(){
    const pv = perView();
    const allSlides = track.querySelectorAll('.carrossel-slide');
    allSlides.forEach(s => s.style.minWidth = (100 / pv / 3) + '%');
  }

  window.addEventListener('resize', ()=>{ setWidths(); pos=0; });
  setWidths();

  // Remove transição CSS para movimento contínuo
  track.style.transition = 'none';
  step();
})();

// ── REVEAL LEFT & SCALE ──────────────────────────────────────────────────────
const revealObs2 = new IntersectionObserver((entries)=>{
  entries.forEach((e,i)=>{
    if(e.isIntersecting){
      setTimeout(()=>e.target.classList.add('visible'), e.target.dataset.delay||0);
      revealObs2.unobserve(e.target);
    }
  });
},{threshold:0.12});

document.querySelectorAll('.reveal-left, .reveal-scale').forEach((el,i)=>{
  el.dataset.delay = (i % 4) * 100;
  revealObs2.observe(el);
});

// ── ADMIN: adicionar rows dinâmicos ──────────────────────────────────────────
function addClienteRow(){
  const wrap = document.getElementById('clientes-wrap');
  if(!wrap) return;
  const i = wrap.querySelectorAll('.adm-cli-row').length;
  const row = document.createElement('div');
  row.className = 'adm-cli-row';
  row.innerHTML = `
    <div class="adm-cli-avatar"><div class="adm-cli-ph">?</div></div>
    <div class="adm-cli-fields">
      <div class="af"><label>Nome</label><input type="text" name="cli_nome" placeholder="Nome do cliente"></div>
      <div class="af"><label>Cargo / descrição</label><input type="text" name="cli_cargo" placeholder="Ex: Empresário"></div>
      <div class="af"><label>Foto (200×200px)</label><input type="file" name="cli_foto_${i}" accept="image/*" class="adm-file-input"></div>
    </div>
    <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-cli-row').remove()">✕</button>`;
  wrap.appendChild(row);
}

function addEmpresaRow(){
  const wrap = document.getElementById('empresas-wrap');
  if(!wrap) return;
  const i = wrap.querySelectorAll('.adm-emp-row').length;
  const row = document.createElement('div');
  row.className = 'adm-emp-row';
  row.innerHTML = `
    <div class="adm-emp-logo-prev"><span>Logo</span></div>
    <div class="adm-cli-fields">
      <div class="af"><label>Nome da empresa</label><input type="text" name="emp_nome" placeholder="Ex: Sicredi"></div>
      <div class="af"><label>Logo (200×80px PNG)</label><input type="file" name="emp_logo_${i}" accept="image/*" class="adm-file-input"></div>
    </div>
    <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-emp-row').remove()">✕</button>`;
  wrap.appendChild(row);
}

// ── VIDEO APRESENTAÇÃO ───────────────────────────────────────────────────────
function playVideoApres() {
  const iframe = document.getElementById('video-apres-iframe');
  const thumb  = document.getElementById('video-apres-thumb');
  const play   = document.getElementById('video-apres-play');
  if (!iframe) return;
  iframe.src = iframe.dataset.src;
  iframe.style.display = 'block';
  if (thumb) thumb.style.display = 'none';
  if (play)  play.style.display  = 'none';
  document.getElementById('video-apres-wrap').onclick = null;
  document.getElementById('video-apres-wrap').style.cursor = 'default';
}

// ── NAV MOBILE — abre automaticamente em telas pequenas ─────────────────────
function openMobileNav(){
  if(window.innerWidth <= 900){
    const m = document.getElementById('nav-mobile');
    if(m) m.classList.add('open');
  }
}
window.addEventListener('load', openMobileNav);
window.addEventListener('resize', openMobileNav);
