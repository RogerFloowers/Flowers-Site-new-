#!/usr/bin/env python3
"""
Rode dentro de ~/Downloads/flowers_site
python3 novo_hero.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── NOVO base.html ────────────────────────────────────────────────────────────
BASE_HTML = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}Flowers Films{% endblock %}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
{% block extra_css %}{% endblock %}
</head>
<body>

<nav id="nav">
  <a href="{{ url_for('index') }}" class="nav-logo-link">
    {% if cfg is defined and cfg.logo %}
      <img src="{{ url_for('static', filename='img/' + cfg.logo) }}" alt="Flowers Films" class="nav-logo-img">
    {% else %}
      <img src="{{ url_for('static', filename='img/logo.png') }}" alt="Flowers Films" class="nav-logo-img" onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
      <div class="nav-logo-txt" style="display:none">FL<span>✿</span>WERS</div>
    {% endif %}
  </a>

  <div class="nav-center">
    <div class="nav-pill">
      <a href="{{ url_for('portfolio_videos') }}" class="nav-pill-link">Portfólio</a>
      <div class="nav-pill-divider"></div>
      <a href="{{ url_for('index') }}#contato" class="nav-pill-link">Contato</a>
      <div class="nav-pill-divider"></div>
      <a href="{{ url_for('cursos') }}" class="nav-pill-link">Cursos</a>
    </div>
  </div>

  <div class="nav-right">
    {% if session.get('admin') %}
      <a href="{{ url_for('admin') }}" class="nav-admin-btn">Admin</a>
      <a href="{{ url_for('logout') }}" class="nav-sair">Sair</a>
    {% else %}
      <a href="{{ url_for('login') }}" class="nav-admin-btn">Entrar</a>
    {% endif %}
    <button class="nav-hamburger" onclick="toggleNav()" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>

  <div class="nav-mobile-menu" id="nav-mobile">
    <a href="{{ url_for('portfolio_videos') }}" onclick="toggleNav()">Portfólio</a>
    <a href="{{ url_for('index') }}#contato" onclick="toggleNav()">Contato</a>
    <a href="{{ url_for('cursos') }}" onclick="toggleNav()">Cursos</a>
    {% if session.get('admin') %}
    <a href="{{ url_for('admin') }}">Admin</a>
    <a href="{{ url_for('logout') }}">Sair</a>
    {% else %}
    <a href="{{ url_for('login') }}">Entrar</a>
    {% endif %}
  </div>
</nav>

{% block content %}{% endblock %}

<footer>
  <div class="footer-inner">
    <div class="footer-logo">Flowers <em>Films</em></div>
    <div class="footer-links">
      <a href="{{ url_for('portfolio_videos') }}">Portfólio</a>
      <a href="{{ url_for('index') }}#contato">Contato</a>
      <a href="{{ url_for('cursos') }}">Cursos</a>
    </div>
    <div class="footer-txt">© 2026 Flowers Films — Roger Flores</div>
  </div>
</footer>

<script src="{{ url_for('static', filename='js/main.js') }}"></script>
{% block extra_js %}{% endblock %}
</body>
</html>
'''

# ── NOVO HERO no index.html ───────────────────────────────────────────────────
HERO_BLOCK = '''{% extends "base.html" %}
{% block title %}Flowers Films — Videomaker & Produtor Visual{% endblock %}

{% block content %}

<!-- HERO -->
<section class="hero-new">

  <!-- Foto de fundo -->
  <div class="hero-foto-wrap">
    {% if cfg.banner.bg %}
      <img src="{{ url_for('static', filename='img/' + cfg.banner.bg) }}" alt="Hero" class="hero-foto">
    {% else %}
      <img src="{{ url_for('static', filename='img/hero_foto.jpg') }}" alt="Hero" class="hero-foto" onerror="this.style.display='none'">
    {% endif %}
    <div class="hero-foto-overlay"></div>
  </div>

  <!-- FLOWERS gigante de fundo -->
  <div class="hero-bg-txt" aria-hidden="true">FLOWERS</div>

  <!-- Logo pequena lateral esquerda -->
  <div class="hero-logo-side">
    {% if cfg.logo %}
      <img src="{{ url_for('static', filename='img/' + cfg.logo) }}" alt="Logo" class="hero-logo-side-img">
    {% endif %}
  </div>

  <!-- Texto principal embaixo à esquerda -->
  <div class="hero-content">
    <h1 class="hero-main-title">
      Transformando <strong>tudo em Cinema.</strong><br>
      <span class="hero-sub-line">e criando um legado absurdo para os clientes</span>
    </h1>

    <div class="hero-bottom-row">
      <div class="hero-desc-left">
        <p>Uma produtora audiovisual que impacta<br>absurdamente seu potêncial</p>
      </div>
      <div class="hero-divider-v"></div>
      <div class="hero-desc-right">
        <p>Especialistas em transformar momentos em obras cinematográficas que emocionam, conectam e deixam marcas eternas nos seus clientes.</p>
      </div>
    </div>
  </div>

</section>

<!-- VÍDEOS -->
<section class="sec-videos" id="videos">
  <div class="sec-header reveal">
    <div class="sec-left">
      <div class="sec-tag">Portfólio</div>
      <h2 class="sec-title">Produções em vídeo</h2>
    </div>
    <a href="{{ url_for('portfolio_videos') }}" class="btn-more">
      Ver todos
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>

  {% if cfg.videos %}
  <div class="videos-compact reveal">
    {% for v in cfg.videos[:4] %}
    <div class="vc-card" onclick="playVideo(this, '{{ v.id }}')">
      {% if v.capa %}
        <img src="{{ url_for('static', filename='img/capas/' + v.capa) }}" alt="Vídeo {{ loop.index }}" class="video-thumb">
      {% else %}
        <img src="https://img.youtube.com/vi/{{ v.id }}/hqdefault.jpg" alt="Vídeo {{ loop.index }}" class="video-thumb">
      {% endif %}
      <div class="vc-overlay">
        <div class="vc-play">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M4 2l10 6-10 6V2z" fill="#fff"/></svg>
        </div>
      </div>
      <div class="vc-num">{{ '%02d'|format(loop.index) }}</div>
    </div>
    {% endfor %}
  </div>
  {% else %}
  <div class="empty-state reveal">Nenhum vídeo cadastrado ainda.</div>
  {% endif %}

  <div class="sec-footer reveal">
    <a href="{{ url_for('portfolio_videos') }}" class="btn-more-center">
      Ver mais vídeos
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>
</section>

<!-- FOTOS -->
<section class="sec-fotos" id="fotos">
  <div class="sec-header reveal">
    <div class="sec-left">
      <div class="sec-tag">Fotografia</div>
      <h2 class="sec-title">Ensaios & eventos</h2>
    </div>
    <a href="{{ url_for('portfolio_fotos') }}" class="btn-more">
      Ver todas
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>
  <div class="fotos-grid reveal">
    {% if fotos %}
      {% for foto in fotos %}
      <div class="foto-card">
        <img src="{{ url_for('foto', filename=foto) }}" alt="Foto {{ loop.index }}" loading="lazy">
        <div class="foto-hover"><div class="foto-plus">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M8 2v12M2 8h12" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>
        </div></div>
      </div>
      {% endfor %}
    {% else %}
      {% for i in range(8) %}
      <div class="foto-card foto-placeholder">
        <div class="foto-ph-inner">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="2" y="4" width="20" height="16" rx="3" stroke="#333" stroke-width="1.5"/><circle cx="12" cy="12" r="4" stroke="#333" stroke-width="1.5"/></svg>
          <span>Foto</span>
        </div>
      </div>
      {% endfor %}
    {% endif %}
  </div>
  <div class="sec-footer reveal">
    <a href="{{ url_for('portfolio_fotos') }}" class="btn-more-center">
      Ver mais fotos
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>
</section>

<!-- INSTAGRAM -->
<section class="sec-instagram">
  <div class="insta-card reveal">
    <div class="insta-left">
      <div class="insta-profile">
        <div class="insta-av"><div class="insta-av-inner">RF</div></div>
        <div>
          <div class="insta-handle">@roogerflores</div>
          <div class="insta-sub">Roger Flores · Flowers Films</div>
        </div>
      </div>
      <p class="insta-bio">Bastidores, lançamentos e conteúdo exclusivo sobre videomaking e produção audiovisual.</p>
      <a href="{{ cfg.contato.instagram }}" target="_blank" rel="noopener" class="btn-insta">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="5" stroke="#fff" stroke-width="2"/><circle cx="12" cy="12" r="5" stroke="#fff" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.2" fill="#fff"/></svg>
        Seguir no Instagram
      </a>
    </div>
    <div class="insta-thumbs">
      {% for i in range(6) %}
      <a href="{{ cfg.contato.instagram }}" target="_blank" class="insta-thumb">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="1" y="1" width="18" height="18" rx="4" stroke="#2a2a2a" stroke-width="1.2"/><circle cx="10" cy="10" r="4" stroke="#2a2a2a" stroke-width="1.2"/></svg>
      </a>
      {% endfor %}
    </div>
  </div>
</section>

<!-- CONTATO -->
<section class="sec-contato" id="contato">
  <div class="sec-header reveal">
    <div class="sec-left">
      <div class="sec-tag">Contato</div>
      <h2 class="sec-title">Vamos criar juntos?</h2>
    </div>
  </div>
  <div class="contato-grid">
    <div class="contato-info reveal">
      <p class="contato-desc">Conte sobre seu projeto e vamos transformar sua ideia em realidade visual. Respondo em até 24h.</p>
      <div class="contact-cards">
        {% if cfg.contato.instagram %}
        <a href="{{ cfg.contato.instagram }}" target="_blank" class="contact-card">
          <div class="cc-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="2" y="2" width="20" height="20" rx="5" stroke="#D4537E" stroke-width="1.8"/><circle cx="12" cy="12" r="5" stroke="#D4537E" stroke-width="1.8"/><circle cx="17.5" cy="6.5" r="1.2" fill="#D4537E"/></svg></div>
          <div><div class="cc-main">Instagram</div><div class="cc-sub">@roogerflores</div></div>
        </a>
        {% endif %}
        {% if cfg.contato.email %}
        <a href="mailto:{{ cfg.contato.email }}" class="contact-card">
          <div class="cc-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 5h18v14H3V5z" stroke="#D4537E" stroke-width="1.8" stroke-linejoin="round"/><path d="M3 5l9 8 9-8" stroke="#D4537E" stroke-width="1.8" stroke-linecap="round"/></svg></div>
          <div><div class="cc-main">E-mail</div><div class="cc-sub">{{ cfg.contato.email }}</div></div>
        </a>
        {% endif %}
        {% if cfg.contato.whatsapp %}
        <a href="https://wa.me/{{ cfg.contato.whatsapp }}" target="_blank" class="contact-card">
          <div class="cc-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M3 21l1.65-4.88A8.5 8.5 0 1 1 12 20.5a8.46 8.46 0 0 1-4.12-1.07L3 21z" stroke="#D4537E" stroke-width="1.8" stroke-linejoin="round"/></svg></div>
          <div><div class="cc-main">WhatsApp</div><div class="cc-sub">Chamar agora</div></div>
        </a>
        {% endif %}
      </div>
    </div>
    <div class="contato-form reveal">
      <h3>Envie uma mensagem</h3>
      <form action="mailto:{{ cfg.contato.email }}" method="get">
        <div class="form-row">
          <div class="fg"><input type="text" name="nome" placeholder="Seu nome" required></div>
          <div class="fg"><input type="email" name="email" placeholder="Seu e-mail"></div>
        </div>
        <div class="fg"><input type="text" name="assunto" placeholder="Assunto do projeto"></div>
        <div class="fg"><textarea name="mensagem" placeholder="Conte sobre seu projeto..." rows="4"></textarea></div>
        <button type="submit" class="btn-pk btn-full">Enviar mensagem</button>
      </form>
    </div>
  </div>
</section>

{% endblock %}
'''

# ── CSS DO NOVO HERO ──────────────────────────────────────────────────────────
CSS_HERO = '''
/* ═══════════════════════════════════════
   NOVO NAV
═══════════════════════════════════════ */
#nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 72px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 5%;
  z-index: 200;
  transition: background .4s;
}
#nav.scrolled { background: rgba(8,8,8,.96); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(255,255,255,.06); }

.nav-logo-link { display:flex; align-items:center; text-decoration:none; flex-shrink:0; }
.nav-logo-img  { height: 44px; width: auto; object-fit: contain; }
.nav-logo-txt  { font-family:'Archivo',sans-serif; font-size:18px; font-weight:900; color:#fff; letter-spacing:-.3px; }
.nav-logo-txt span { color: var(--pk); }

/* PILL central */
.nav-center { flex: 1; display: flex; justify-content: center; }
.nav-pill {
  display: flex;
  align-items: center;
  background: rgba(100,20,50,.75);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212,83,126,.3);
  border-radius: 50px;
  padding: 6px 8px;
  gap: 0;
}
.nav-pill-link {
  color: rgba(255,255,255,.85);
  font-size: 13px;
  font-weight: 600;
  padding: 8px 22px;
  border-radius: 40px;
  transition: all .2s;
  text-decoration: none;
  letter-spacing: .3px;
}
.nav-pill-link:hover { color: #fff; background: rgba(212,83,126,.25); }
.nav-pill-divider { width: 1px; height: 16px; background: rgba(212,83,126,.35); }

.nav-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.nav-admin-btn {
  background: transparent; border: 1px solid rgba(212,83,126,.45);
  color: var(--pk); border-radius: 20px; padding: 7px 18px;
  font-size: 11px; font-weight: 700; cursor: pointer;
  font-family: 'Archivo',sans-serif; transition: all .2s;
  letter-spacing: .5px; text-transform: uppercase; text-decoration: none;
}
.nav-admin-btn:hover { background: var(--pk); color: #fff; }
.nav-sair { font-size: 11px; color: var(--txt3); text-decoration: none; }
.nav-sair:hover { color: var(--txt2); }

.nav-hamburger { display:none; flex-direction:column; gap:5px; background:none; border:none; cursor:pointer; padding:4px; }
.nav-hamburger span { display:block; width:22px; height:2px; background:rgba(255,255,255,.7); border-radius:2px; }

.nav-mobile-menu {
  display: none;
  position: fixed;
  top: 72px; left: 0; right: 0;
  background: rgba(8,8,8,.98);
  border-bottom: 1px solid rgba(255,255,255,.06);
  padding: 20px 5%;
  flex-direction: column;
  gap: 16px;
  z-index: 199;
}
.nav-mobile-menu.open { display: flex; }
.nav-mobile-menu a { color: var(--txt2); font-size: 15px; font-weight: 600; text-decoration: none; }
.nav-mobile-menu a:hover { color: var(--pk); }

/* ═══════════════════════════════════════
   NOVO HERO
═══════════════════════════════════════ */
.hero-new {
  position: relative;
  width: 100%;
  height: 100vh;
  min-height: 600px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0 5% 52px;
}

/* Foto de fundo */
.hero-foto-wrap { position: absolute; inset: 0; z-index: 0; }
.hero-foto { width: 100%; height: 100%; object-fit: cover; object-position: center top; display: block; filter: grayscale(20%); }
.hero-foto-overlay {
  position: absolute; inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(8,8,8,.3) 0%,
    rgba(8,8,8,.1) 30%,
    rgba(8,8,8,.55) 70%,
    rgba(8,8,8,.92) 100%
  );
}

/* FLOWERS gigante de fundo */
.hero-bg-txt {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  font-family: 'Archivo', sans-serif;
  font-size: clamp(120px, 22vw, 320px);
  font-weight: 900;
  color: rgba(255,255,255,.06);
  white-space: nowrap;
  letter-spacing: -8px;
  pointer-events: none;
  z-index: 1;
  user-select: none;
}

/* Logo lateral */
.hero-logo-side {
  position: absolute;
  left: 5%;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
}
.hero-logo-side-img { width: 90px; height: 90px; object-fit: contain; opacity: .9; }

/* Conteúdo principal */
.hero-content { position: relative; z-index: 3; max-width: 1200px; width: 100%; }

.hero-main-title {
  font-family: 'Archivo', sans-serif;
  font-size: clamp(28px, 4.5vw, 62px);
  font-weight: 400;
  color: #fff;
  line-height: 1.15;
  letter-spacing: -.5px;
  margin-bottom: 32px;
}
.hero-main-title strong { font-weight: 900; }
.hero-sub-line { font-size: clamp(18px, 2.8vw, 38px); font-weight: 300; color: rgba(255,255,255,.8); }

.hero-bottom-row {
  display: flex;
  align-items: flex-start;
  gap: 32px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,.18);
  max-width: 900px;
}
.hero-desc-left, .hero-desc-right {
  font-size: clamp(12px, 1.2vw, 14px);
  color: rgba(255,255,255,.55);
  line-height: 1.65;
  flex: 1;
}
.hero-divider-v { width: 1px; height: 48px; background: rgba(255,255,255,.2); flex-shrink: 0; margin-top: 4px; }

/* ═══════════════════════════════════════
   VÍDEOS COMPACTOS
═══════════════════════════════════════ */
.videos-compact {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0;
  border: 1px solid rgba(255,255,255,.1);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 32px;
}
.vc-card {
  position: relative;
  aspect-ratio: 16/9;
  cursor: pointer;
  overflow: hidden;
  border-right: 1px solid rgba(255,255,255,.08);
}
.vc-card:last-child { border-right: none; }
.vc-card .video-thumb { width:100%; height:100%; object-fit:cover; display:block; transition: transform .4s; }
.vc-card:hover .video-thumb { transform: scale(1.07); }
.vc-overlay {
  position: absolute; inset: 0;
  background: rgba(0,0,0,.4);
  display: flex; align-items: center; justify-content: center;
  transition: background .25s;
}
.vc-card:hover .vc-overlay { background: rgba(0,0,0,.15); }
.vc-play {
  width: 40px; height: 40px; border-radius: 50%;
  background: rgba(212,83,126,.88);
  display: flex; align-items: center; justify-content: center;
  transition: transform .2s;
  box-shadow: 0 0 0 6px rgba(212,83,126,.2);
}
.vc-card:hover .vc-play { transform: scale(1.15); }
.vc-num {
  position: absolute; top: 8px; left: 10px;
  font-size: 10px; font-weight: 700;
  color: rgba(255,255,255,.6);
  background: rgba(0,0,0,.5);
  padding: 2px 7px; border-radius: 4px;
  letter-spacing: 1px;
}

/* ═══════════════════════════════════════
   RESPONSIVO
═══════════════════════════════════════ */
@media (max-width: 900px) {
  .nav-center { display: none; }
  .nav-hamburger { display: flex; }
  .nav-admin-btn { display: none; }
  .hero-logo-side { display: none; }
  .videos-compact { grid-template-columns: repeat(2,1fr); }
  .vc-card { border-right: 1px solid rgba(255,255,255,.08); border-bottom: 1px solid rgba(255,255,255,.08); }
  .vc-card:nth-child(2n) { border-right: none; }
  .vc-card:nth-last-child(-n+2) { border-bottom: none; }
  .hero-bottom-row { flex-direction: column; gap: 14px; }
  .hero-divider-v { display: none; }
}
@media (max-width: 600px) {
  .hero-new { padding: 0 5% 40px; }
  .hero-main-title { margin-bottom: 20px; }
  .videos-compact { grid-template-columns: repeat(2,1fr); border-radius: 8px; }
  section { padding: 56px 5%; }
}
'''

# ── APLICA ────────────────────────────────────────────────────────────────────
print('Escrevendo templates/base.html ...')
open(os.path.join(BASE, 'templates', 'base.html'), 'w', encoding='utf-8').write(BASE_HTML)
print('  OK')

print('Escrevendo templates/index.html ...')
open(os.path.join(BASE, 'templates', 'index.html'), 'w', encoding='utf-8').write(HERO_BLOCK)
print('  OK')

print('Adicionando CSS do novo hero ...')
css_path = os.path.join(BASE, 'static', 'css', 'style.css')
css = open(css_path, encoding='utf-8').read()
marker = '/* ═══════════════════════════════════════\n   NOVO NAV'
if marker not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + CSS_HERO)
    print('  OK (CSS adicionado)')
else:
    start = css.find(marker)
    open(css_path, 'w', encoding='utf-8').write(css[:start] + CSS_HERO.strip())
    print('  OK (CSS atualizado)')

# Atualiza main.js para scroll do nav
js_path = os.path.join(BASE, 'static', 'js', 'main.js')
js = open(js_path, encoding='utf-8').read()
scroll_code = '''
// Nav scroll effect
window.addEventListener('scroll', () => {
  const nav = document.getElementById('nav');
  if(nav) nav.classList.toggle('scrolled', window.scrollY > 60);
});
function toggleNav(){
  document.getElementById('nav-mobile').classList.toggle('open');
}
'''
if 'nav.classList.toggle' not in js:
    # Remove versão antiga do toggleNav e scroll
    import re
    js = re.sub(r'function toggleNav\(\).*?\n\}', '', js, flags=re.DOTALL)
    js = re.sub(r'window\.addEventListener\(\'scroll\'.*?\}\);', '', js, flags=re.DOTALL)
    js = js.strip() + '\n' + scroll_code
    open(js_path, 'w', encoding='utf-8').write(js)
    print('main.js: scroll nav atualizado')

print('\n✅  Pronto! Agora:')
print('   1. Coloque uma foto sua em: static/img/hero_foto.jpg')
print('   2. Rode: python app.py')
print('   3. Acesse: http://localhost:5000\n')
print('   Dica: no admin, em Banner principal, suba uma foto no campo "Foto de fundo" para substituir a hero_foto.jpg\n')
