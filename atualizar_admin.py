#!/usr/bin/env python3
"""
Roda dentro de ~/Downloads/flowers_site
Atualiza: app.py + templates/admin.html + static/css/style.css (append)
"""
import os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

# ── APP.PY ────────────────────────────────────────────────────────────────────
APP = '''from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os, json
from functools import wraps
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'flowers-films-secret-2026'

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
FOTOS_DIR   = os.path.join(BASE_DIR, 'uploads', 'fotos')
CAPAS_DIR   = os.path.join(BASE_DIR, 'static', 'img', 'capas')
STATIC_DIR  = os.path.join(BASE_DIR, 'static')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')

for d in [FOTOS_DIR, CAPAS_DIR]:
    os.makedirs(d, exist_ok=True)

ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
ADMIN_USER  = 'roger'
ADMIN_PASS  = 'flowers2026'

DEFAULT_CONFIG = {
    "banner": {
        "linha1":   "CRIANDO",
        "linha2":   "HISTÓRIAS",
        "linha3":   "VISUAIS.",
        "subtitulo":"Vídeos, fotos e produções audiovisuais que conectam marcas ao seu público.",
        "tag":      "Videomaker & Produtor Visual",
        "bg":       ""
    },
    "logo": "",
    "stats": [
        {"num": "+80",    "label": "Projetos entregues"},
        {"num": "5 anos", "label": "De experiência"},
        {"num": "100%",   "label": "Clientes satisfeitos"}
    ],
    "videos": [
        {"id": "hTybgrnpgbw", "titulo": "", "capa": ""},
        {"id": "icyz7ohnRWI", "titulo": "", "capa": ""},
        {"id": "jOqiZbiyRGg", "titulo": "", "capa": ""},
        {"id": "5DvED73NII4", "titulo": "", "capa": ""}
    ],
    "contato": {
        "email":     "contato@flowersfilms.com.br",
        "whatsapp":  "",
        "instagram": "https://www.instagram.com/roogerflores"
    },
    "cursos": []
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            return json.load(open(CONFIG_FILE, encoding='utf-8'))
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(cfg):
    json.dump(cfg, open(CONFIG_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

def get_fotos():
    return [f for f in sorted(os.listdir(FOTOS_DIR))
            if f.rsplit('.', 1)[-1].lower() in ALLOWED_EXT]

def allowed(fn):
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def login_required(f):
    @wraps(f)
    def dec(*a, **kw):
        if not session.get('admin'):
            return redirect(url_for('login'))
        return f(*a, **kw)
    return dec

def save_upload(file_obj, folder, prefix=''):
    if file_obj and file_obj.filename and allowed(file_obj.filename):
        fn = secure_filename(prefix + file_obj.filename)
        file_obj.save(os.path.join(folder, fn))
        return fn
    return None

# ── PÚBLICO ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    cfg = load_config()
    return render_template('index.html', cfg=cfg, fotos=get_fotos()[:8])

@app.route('/portfolio/videos')
def portfolio_videos():
    return render_template('portfolio_videos.html', cfg=load_config())

@app.route('/portfolio/fotos')
def portfolio_fotos():
    return render_template('portfolio_fotos.html', fotos=get_fotos())

@app.route('/cursos')
def cursos():
    return render_template('cursos.html', cfg=load_config())

@app.route('/uploads/fotos/<filename>')
def foto(filename):
    return send_from_directory(FOTOS_DIR, filename)

# ── LOGIN ─────────────────────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        if request.form.get('usuario','').strip() == ADMIN_USER and \\
           request.form.get('senha','').strip()   == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin'))
        erro = 'Usuário ou senha incorretos.'
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ── ADMIN ─────────────────────────────────────────────────────────────────────
@app.route('/admin')
@login_required
def admin():
    cfg = load_config()
    return render_template('admin.html', cfg=cfg,
                           fotos=get_fotos(),
                           total_fotos=len(get_fotos()),
                           total_videos=len(cfg.get('videos', [])))

@app.route('/admin/salvar-banner', methods=['POST'])
@login_required
def salvar_banner():
    cfg = load_config()
    cfg['banner']['linha1']    = request.form.get('linha1','').strip().upper()
    cfg['banner']['linha2']    = request.form.get('linha2','').strip().upper()
    cfg['banner']['linha3']    = request.form.get('linha3','').strip().upper()
    cfg['banner']['subtitulo'] = request.form.get('subtitulo','').strip()
    cfg['banner']['tag']       = request.form.get('tag','').strip()
    # Upload foto de fundo
    fn = save_upload(request.files.get('banner_bg'),
                     os.path.join(STATIC_DIR, 'img'), 'bg_')
    if fn:
        cfg['banner']['bg'] = fn
    save_config(cfg)
    return redirect(url_for('admin') + '#banner')

@app.route('/admin/salvar-logo', methods=['POST'])
@login_required
def salvar_logo():
    cfg = load_config()
    fn = save_upload(request.files.get('logo'),
                     os.path.join(STATIC_DIR, 'img'), '')
    if fn:
        cfg['logo'] = fn
    save_config(cfg)
    return redirect(url_for('admin') + '#logo')

@app.route('/admin/salvar-videos', methods=['POST'])
@login_required
def salvar_videos():
    cfg    = load_config()
    old_map = {v['id']: v for v in cfg.get('videos', [])}
    ids     = request.form.getlist('video_id')
    titulos = request.form.getlist('video_titulo')
    videos  = []
    for i, (vid_id, titulo) in enumerate(zip(ids, titulos)):
        vid_id = vid_id.strip()
        if not vid_id:
            continue
        if 'youtube.com/watch?v=' in vid_id:
            vid_id = vid_id.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in vid_id:
            vid_id = vid_id.split('youtu.be/')[1].split('?')[0]
        capa = old_map.get(vid_id, {}).get('capa', '')
        fn = save_upload(request.files.get(f'video_capa_{i}'),
                         CAPAS_DIR, f'capa_{vid_id}_')
        if fn:
            capa = fn
        videos.append({'id': vid_id, 'titulo': titulo.strip(), 'capa': capa})
    cfg['videos'] = videos
    save_config(cfg)
    return redirect(url_for('admin') + '#videos')

@app.route('/admin/upload-foto', methods=['POST'])
@login_required
def upload_foto():
    for f in request.files.getlist('fotos'):
        if f and allowed(f.filename):
            f.save(os.path.join(FOTOS_DIR, secure_filename(f.filename)))
    return redirect(url_for('admin') + '#fotos')

@app.route('/admin/deletar-foto/<filename>', methods=['POST'])
@login_required
def deletar_foto(filename):
    path = os.path.join(FOTOS_DIR, secure_filename(filename))
    if os.path.exists(path):
        os.remove(path)
    return redirect(url_for('admin') + '#fotos')

@app.route('/admin/salvar-contato', methods=['POST'])
@login_required
def salvar_contato():
    cfg = load_config()
    cfg['contato']['email']     = request.form.get('email','').strip()
    cfg['contato']['whatsapp']  = request.form.get('whatsapp','').strip()
    cfg['contato']['instagram'] = request.form.get('instagram','').strip()
    save_config(cfg)
    return redirect(url_for('admin') + '#contato')

@app.route('/admin/salvar-stats', methods=['POST'])
@login_required
def salvar_stats():
    cfg = load_config()
    nums   = request.form.getlist('stat_num')
    labels = request.form.getlist('stat_label')
    cfg['stats'] = [{'num': n.strip(), 'label': l.strip()}
                    for n, l in zip(nums, labels) if n.strip()]
    save_config(cfg)
    return redirect(url_for('admin') + '#stats')

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    print('\\n  ✦  FLOWERS FILMS — Site Público')
    print('  →  http://localhost:5000\\n')
    app.run(debug=True, port=5000)
'''

# ── ADMIN.HTML ────────────────────────────────────────────────────────────────
ADMIN_HTML = '''{% extends "base.html" %}
{% block title %}Admin — Flowers Films{% endblock %}
{% block content %}
<div class="adm-wrap">

  <!-- HEADER -->
  <div class="adm-topbar">
    <div>
      <div class="adm-eyebrow">Painel administrativo</div>
      <h1 class="adm-h1">Olá, Roger 👋</h1>
    </div>
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
      <a href="{{ url_for('index') }}" target="_blank" class="adm-btn-ghost">
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2 7h10M7 3l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Ver site
      </a>
      <a href="{{ url_for('logout') }}" class="adm-btn-danger">Sair</a>
    </div>
  </div>

  <!-- DASHBOARD CARDS -->
  <div class="adm-dashboard">
    <div class="adm-dash-card">
      <div class="adm-dash-icon" style="background:rgba(212,83,126,.15)">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M3 4h14v12H3V4z" stroke="#D4537E" stroke-width="1.5" stroke-linejoin="round"/><path d="M3 8h14" stroke="#D4537E" stroke-width="1.5"/><circle cx="7" cy="12" r="1.5" fill="#D4537E"/></svg>
      </div>
      <div class="adm-dash-num">{{ total_videos }}</div>
      <div class="adm-dash-lbl">Vídeos</div>
    </div>
    <div class="adm-dash-card">
      <div class="adm-dash-icon" style="background:rgba(34,197,94,.12)">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="3" width="16" height="14" rx="2" stroke="#22c55e" stroke-width="1.5"/><circle cx="10" cy="10" r="3" stroke="#22c55e" stroke-width="1.5"/></svg>
      </div>
      <div class="adm-dash-num">{{ total_fotos }}</div>
      <div class="adm-dash-lbl">Fotos</div>
    </div>
    <div class="adm-dash-card">
      <div class="adm-dash-icon" style="background:rgba(96,165,250,.12)">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="7" stroke="#60a5fa" stroke-width="1.5"/><path d="M10 6v4l3 2" stroke="#60a5fa" stroke-width="1.5" stroke-linecap="round"/></svg>
      </div>
      <div class="adm-dash-num">Ativo</div>
      <div class="adm-dash-lbl">Site online</div>
    </div>
    <div class="adm-dash-card">
      <div class="adm-dash-icon" style="background:rgba(245,158,11,.12)">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 2l2.4 5.4 5.6.8-4 4 .9 5.8L10 15.4l-4.9 2.6.9-5.8-4-4 5.6-.8L10 2z" stroke="#f59e0b" stroke-width="1.5" stroke-linejoin="round"/></svg>
      </div>
      <div class="adm-dash-num">PRO</div>
      <div class="adm-dash-lbl">Plano</div>
    </div>
  </div>

  <!-- ATALHOS RÁPIDOS -->
  <div class="adm-shortcuts">
    <a href="#logo"    class="adm-shortcut">🖼 Logo</a>
    <a href="#banner"  class="adm-shortcut">🎨 Banner</a>
    <a href="#videos"  class="adm-shortcut">▶ Vídeos</a>
    <a href="#fotos"   class="adm-shortcut">📷 Fotos</a>
    <a href="#contato" class="adm-shortcut">📬 Contato</a>
    <a href="#stats"   class="adm-shortcut">📊 Stats</a>
  </div>

  <!-- LOGO -->
  <div class="adm-section" id="logo">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Identidade</div>
        <h2 class="adm-sec-title">Logo do site</h2>
      </div>
    </div>
    <div class="adm-two-col">
      <div>
        <div class="adm-preview-logo">
          {% if cfg.logo %}
            <img src="{{ url_for('static', filename='img/' + cfg.logo) }}" alt="Logo atual" style="max-height:100px;max-width:200px;object-fit:contain">
            <div class="adm-preview-lbl">Logo atual</div>
          {% else %}
            <div style="color:var(--txt3);font-size:13px;text-align:center">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" style="opacity:.3;margin-bottom:8px"><rect x="2" y="2" width="28" height="28" rx="4" stroke="#fff" stroke-width="1.5"/><path d="M8 24l6-8 4 5 3-3 5 6" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="11" cy="12" r="2" stroke="#fff" stroke-width="1.5"/></svg>
              <br>Nenhuma logo enviada
            </div>
          {% endif %}
        </div>
      </div>
      <div>
        <form action="{{ url_for('salvar_logo') }}" method="POST" enctype="multipart/form-data">
          <div class="af" style="margin-bottom:14px">
            <label>Enviar nova logo (PNG transparente recomendado)</label>
            <input type="file" name="logo" accept="image/*" class="adm-file-input">
          </div>
          <button type="submit" class="adm-btn-save">Salvar logo</button>
        </form>
        <p class="adm-hint">A logo aparece no cabeçalho do site e no hero. Use PNG com fundo transparente para melhor resultado.</p>
      </div>
    </div>
  </div>

  <!-- BANNER -->
  <div class="adm-section" id="banner">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Início do site</div>
        <h2 class="adm-sec-title">Banner principal</h2>
      </div>
    </div>

    <!-- PREVIEW DO BANNER -->
    <div class="adm-banner-preview" {% if cfg.banner.bg %}style="background-image:url(\'{{ url_for('static', filename='img/' + cfg.banner.bg) }}\');background-size:cover;background-position:center"{% endif %}>
      <div class="adm-banner-overlay"></div>
      <div class="adm-banner-content">
        <div class="adm-banner-tag">{{ cfg.banner.tag }}</div>
        <div class="adm-banner-title">
          <span>{{ cfg.banner.linha1 }}</span>
          <span style="color:#D4537E;font-style:italic">{{ cfg.banner.linha2 }}</span>
          <span>{{ cfg.banner.linha3 }}</span>
        </div>
        <div class="adm-banner-sub">{{ cfg.banner.subtitulo }}</div>
      </div>
    </div>

    <form action="{{ url_for('salvar_banner') }}" method="POST" enctype="multipart/form-data">
      <div class="adm-grid-3">
        <div class="af"><label>Linha 1 — branca</label><input name="linha1" value="{{ cfg.banner.linha1 }}" placeholder="CRIANDO"></div>
        <div class="af"><label>Linha 2 — rosa itálico</label><input name="linha2" value="{{ cfg.banner.linha2 }}" placeholder="HISTÓRIAS"></div>
        <div class="af"><label>Linha 3 — branca</label><input name="linha3" value="{{ cfg.banner.linha3 }}" placeholder="VISUAIS."></div>
        <div class="af full"><label>Tag (linha pequena acima do título)</label><input name="tag" value="{{ cfg.banner.tag }}" placeholder="Videomaker & Produtor Visual"></div>
        <div class="af full"><label>Subtítulo</label><input name="subtitulo" value="{{ cfg.banner.subtitulo }}" placeholder="Vídeos, fotos e produções..."></div>
        <div class="af full">
          <label>Foto de fundo do banner</label>
          <input type="file" name="banner_bg" accept="image/*" class="adm-file-input">
          {% if cfg.banner.bg %}
          <div style="margin-top:8px;display:flex;align-items:center;gap:10px">
            <img src="{{ url_for('static', filename='img/' + cfg.banner.bg) }}" style="height:44px;border-radius:6px;object-fit:cover;border:1px solid rgba(255,255,255,.1)">
            <span style="font-size:11px;color:var(--txt2)">Fundo atual — envie outro para substituir</span>
          </div>
          {% endif %}
        </div>
      </div>
      <button type="submit" class="adm-btn-save">Salvar banner</button>
    </form>
  </div>

  <!-- VÍDEOS -->
  <div class="adm-section" id="videos">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Portfólio</div>
        <h2 class="adm-sec-title">Vídeos</h2>
      </div>
    </div>
    <form action="{{ url_for('salvar_videos') }}" method="POST" enctype="multipart/form-data">
      <div id="videos-wrap">
        {% for v in cfg.videos %}
        <div class="adm-video-row">
          <div class="adm-video-thumb">
            {% if v.capa %}
              <img src="{{ url_for('static', filename='img/capas/' + v.capa) }}" alt="capa">
            {% else %}
              <img src="https://img.youtube.com/vi/{{ v.id }}/hqdefault.jpg" alt="thumb" onerror="this.src=''">
            {% endif %}
            <div class="adm-video-num">{{ loop.index }}</div>
          </div>
          <div class="adm-video-fields">
            <div class="af"><label>Link ou ID do YouTube</label><input type="text" name="video_id" value="{{ v.id }}" placeholder="https://youtu.be/..."></div>
            <div class="af"><label>Título (opcional)</label><input type="text" name="video_titulo" value="{{ v.titulo }}" placeholder="Nome do projeto"></div>
            <div class="af">
              <label>Capa personalizada</label>
              <input type="file" name="video_capa_{{ loop.index0 }}" accept="image/*" class="adm-file-input">
            </div>
          </div>
          <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-video-row').remove()">✕</button>
        </div>
        {% endfor %}
      </div>
      <button type="button" class="adm-btn-add" onclick="addVideoRow()">+ Adicionar vídeo</button>
      <br><br>
      <button type="submit" class="adm-btn-save">Salvar vídeos</button>
    </form>
  </div>

  <!-- FOTOS -->
  <div class="adm-section" id="fotos">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Portfólio</div>
        <h2 class="adm-sec-title">Fotos</h2>
      </div>
    </div>
    {% if fotos %}
    <div class="adm-fotos-grid">
      {% for ft in fotos %}
      <div class="adm-foto">
        <img src="{{ url_for('foto', filename=ft) }}" alt="{{ ft }}">
        <form action="{{ url_for('deletar_foto', filename=ft) }}" method="POST">
          <button type="submit" class="adm-foto-del" onclick="return confirm('Deletar?')">✕</button>
        </form>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <p class="adm-hint" style="margin-bottom:16px">Nenhuma foto ainda. Faça upload abaixo.</p>
    {% endif %}
    <form action="{{ url_for('upload_foto') }}" method="POST" enctype="multipart/form-data">
      <div class="af" style="margin-bottom:12px">
        <label>Enviar fotos (JPG, PNG, WEBP — múltiplas)</label>
        <input type="file" name="fotos" multiple accept="image/*" class="adm-file-input">
      </div>
      <button type="submit" class="adm-btn-save">Fazer upload</button>
    </form>
  </div>

  <!-- CONTATO -->
  <div class="adm-section" id="contato">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Contato</div>
        <h2 class="adm-sec-title">Informações de contato</h2>
      </div>
    </div>
    <form action="{{ url_for('salvar_contato') }}" method="POST">
      <div class="adm-grid-3">
        <div class="af"><label>E-mail</label><input name="email" value="{{ cfg.contato.email }}" placeholder="contato@flowersfilms.com.br"></div>
        <div class="af"><label>WhatsApp (só números)</label><input name="whatsapp" value="{{ cfg.contato.whatsapp }}" placeholder="5544999999999"></div>
        <div class="af"><label>Instagram (URL)</label><input name="instagram" value="{{ cfg.contato.instagram }}" placeholder="https://instagram.com/..."></div>
      </div>
      <button type="submit" class="adm-btn-save">Salvar contato</button>
    </form>
  </div>

  <!-- STATS -->
  <div class="adm-section" id="stats">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Números</div>
        <h2 class="adm-sec-title">Stats do banner</h2>
      </div>
    </div>
    <form action="{{ url_for('salvar_stats') }}" method="POST">
      {% for s in cfg.stats %}
      <div class="adm-stat-row">
        <div class="af"><label>Número</label><input name="stat_num" value="{{ s.num }}" placeholder="+80"></div>
        <div class="af"><label>Descrição</label><input name="stat_label" value="{{ s.label }}" placeholder="Projetos entregues"></div>
      </div>
      {% endfor %}
      <button type="submit" class="adm-btn-save">Salvar stats</button>
    </form>
  </div>

</div>
{% endblock %}
'''

# ── CSS ADMIN ─────────────────────────────────────────────────────────────────
CSS_ADMIN = '''
/* ═══════════════════════════════════════════════
   ADMIN — estilos
═══════════════════════════════════════════════ */
.adm-wrap { max-width: 960px; margin: 0 auto; padding: 36px 5% 60px; }

.adm-topbar { display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:28px; flex-wrap:wrap; gap:14px; }
.adm-eyebrow { font-size:10px; text-transform:uppercase; letter-spacing:1.5px; color:var(--pk); font-weight:700; margin-bottom:6px; }
.adm-h1 { font-size:28px; font-weight:900; color:#fff; letter-spacing:-1px; }

/* Dashboard cards */
.adm-dashboard { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:20px; }
.adm-dash-card { background:var(--bg2); border:1px solid rgba(255,255,255,.07); border-radius:12px; padding:18px; display:flex; flex-direction:column; gap:8px; }
.adm-dash-icon { width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; }
.adm-dash-num { font-size:24px; font-weight:900; color:#fff; letter-spacing:-1px; line-height:1; }
.adm-dash-lbl { font-size:11px; color:var(--txt2); text-transform:uppercase; letter-spacing:.5px; }

/* Atalhos */
.adm-shortcuts { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:28px; }
.adm-shortcut { background:var(--bg2); border:1px solid rgba(255,255,255,.07); border-radius:8px; padding:8px 16px; font-size:12px; font-weight:600; color:var(--txt2); transition:all .18s; cursor:pointer; }
.adm-shortcut:hover { border-color:var(--pk); color:var(--pk); background:rgba(212,83,126,.07); }

/* Seções */
.adm-section { background:var(--bg2); border:1px solid rgba(255,255,255,.07); border-radius:14px; padding:26px; margin-bottom:18px; }
.adm-sec-head { margin-bottom:20px; padding-bottom:16px; border-bottom:1px solid rgba(255,255,255,.06); }
.adm-sec-tag { font-size:10px; text-transform:uppercase; letter-spacing:1.5px; color:var(--pk); font-weight:700; margin-bottom:5px; }
.adm-sec-title { font-size:18px; font-weight:800; color:#fff; letter-spacing:-.5px; }

/* Banner preview */
.adm-banner-preview { border-radius:12px; overflow:hidden; min-height:180px; background:var(--bg3); position:relative; margin-bottom:22px; display:flex; align-items:center; padding:32px; }
.adm-banner-overlay { position:absolute; inset:0; background:rgba(0,0,0,.55); }
.adm-banner-content { position:relative; z-index:1; }
.adm-banner-tag { font-size:10px; font-weight:700; color:var(--pk); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px; }
.adm-banner-title { font-size:clamp(24px,4vw,40px); font-weight:900; color:#fff; letter-spacing:-1.5px; line-height:1; display:flex; flex-direction:column; margin-bottom:10px; }
.adm-banner-sub { font-size:13px; color:rgba(255,255,255,.6); max-width:400px; line-height:1.6; }

/* Grid forms */
.adm-grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:14px; }
.adm-grid-3 .full { grid-column:1/-1; }
.adm-two-col { display:grid; grid-template-columns:160px 1fr; gap:22px; align-items:start; margin-bottom:0; }
.adm-stat-row { display:grid; grid-template-columns:1fr 2fr; gap:10px; margin-bottom:10px; }

/* Fields */
.af { display:flex; flex-direction:column; gap:5px; }
.af label { font-size:10px; text-transform:uppercase; letter-spacing:.6px; color:var(--txt2); font-weight:600; }
.af input, .af textarea {
  background:var(--bg3); border:1px solid rgba(255,255,255,.08); border-radius:8px;
  color:var(--txt); padding:9px 12px; font-size:13px;
  font-family:'Archivo',sans-serif; outline:none; transition:border .15s; width:100%;
}
.af input:focus, .af textarea:focus { border-color:var(--pk); }
.adm-file-input {
  background:var(--bg3); border:1px dashed rgba(255,255,255,.15); border-radius:8px;
  color:var(--txt2); padding:10px 12px; font-size:12px; width:100%; cursor:pointer;
  transition:border .15s;
}
.adm-file-input:hover { border-color:var(--pk); }
.adm-hint { font-size:12px; color:var(--txt3); line-height:1.6; margin-top:10px; }

/* Botões */
.adm-btn-save { background:var(--pk); color:#fff; border:none; border-radius:8px; padding:10px 24px; font-size:13px; font-weight:700; cursor:pointer; font-family:'Archivo',sans-serif; transition:opacity .15s; }
.adm-btn-save:hover { opacity:.86; }
.adm-btn-ghost { display:inline-flex; align-items:center; gap:7px; background:transparent; color:var(--txt2); border:1px solid rgba(255,255,255,.1); border-radius:8px; padding:9px 18px; font-size:12px; font-weight:600; cursor:pointer; font-family:'Archivo',sans-serif; transition:all .15s; }
.adm-btn-ghost:hover { border-color:var(--pk); color:var(--pk); }
.adm-btn-danger { background:transparent; color:#f87171; border:1px solid rgba(248,113,113,.25); border-radius:8px; padding:9px 18px; font-size:12px; font-weight:600; cursor:pointer; font-family:'Archivo',sans-serif; transition:all .15s; }
.adm-btn-danger:hover { background:rgba(248,113,113,.1); }
.adm-btn-add { background:transparent; border:1px dashed rgba(212,83,126,.4); color:var(--pk); border-radius:8px; padding:9px 18px; font-size:12px; font-weight:600; cursor:pointer; font-family:'Archivo',sans-serif; transition:all .18s; }
.adm-btn-add:hover { background:rgba(212,83,126,.08); }
.adm-btn-rm { background:none; border:none; color:var(--txt3); cursor:pointer; font-size:18px; padding:6px; border-radius:6px; flex-shrink:0; transition:all .15s; line-height:1; align-self:flex-start; margin-top:22px; }
.adm-btn-rm:hover { color:#f87171; background:rgba(248,113,113,.1); }

/* Preview logo */
.adm-preview-logo { background:var(--bg3); border:1px solid rgba(255,255,255,.07); border-radius:10px; min-height:120px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px; padding:16px; }
.adm-preview-lbl { font-size:10px; color:var(--txt3); text-transform:uppercase; letter-spacing:1px; }

/* Vídeo rows */
.adm-video-row { display:grid; grid-template-columns:80px 1fr auto; gap:14px; align-items:start; background:var(--bg3); border:1px solid rgba(255,255,255,.06); border-radius:10px; padding:14px; margin-bottom:10px; }
.adm-video-thumb { width:80px; aspect-ratio:16/9; border-radius:6px; overflow:hidden; position:relative; background:#000; flex-shrink:0; }
.adm-video-thumb img { width:100%; height:100%; object-fit:cover; display:block; }
.adm-video-num { position:absolute; top:4px; left:4px; font-size:9px; font-weight:700; color:rgba(255,255,255,.7); background:rgba(0,0,0,.6); padding:2px 6px; border-radius:3px; }
.adm-video-fields { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; }

/* Fotos grid */
.adm-fotos-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(100px,1fr)); gap:8px; margin-bottom:18px; }
.adm-foto { position:relative; aspect-ratio:1; border-radius:6px; overflow:hidden; }
.adm-foto img { width:100%; height:100%; object-fit:cover; display:block; }
.adm-foto-del { position:absolute; top:4px; right:4px; background:rgba(0,0,0,.75); color:#f87171; border:none; border-radius:4px; width:22px; height:22px; font-size:12px; cursor:pointer; display:flex; align-items:center; justify-content:center; }

/* Responsive */
@media(max-width:768px){
  .adm-dashboard { grid-template-columns:repeat(2,1fr); }
  .adm-grid-3 { grid-template-columns:1fr 1fr; }
  .adm-two-col { grid-template-columns:1fr; }
  .adm-video-fields { grid-template-columns:1fr; }
  .adm-video-row { grid-template-columns:60px 1fr auto; }
}
@media(max-width:500px){
  .adm-dashboard { grid-template-columns:1fr 1fr; }
  .adm-grid-3 { grid-template-columns:1fr; }
}
'''

# ── MAIN.JS addVideoRow atualizado ────────────────────────────────────────────
JS_EXTRA = '''
function addVideoRow() {
  const wrap = document.getElementById('videos-wrap');
  if (!wrap) return;
  const i = wrap.querySelectorAll('.adm-video-row').length;
  const row = document.createElement('div');
  row.className = 'adm-video-row';
  row.innerHTML = `
    <div class="adm-video-thumb">
      <div style="width:100%;height:100%;background:#111;display:flex;align-items:center;justify-content:center;font-size:9px;color:#444">Novo</div>
      <div class="adm-video-num">${i+1}</div>
    </div>
    <div class="adm-video-fields">
      <div class="af"><label>Link ou ID YouTube</label><input type="text" name="video_id" placeholder="https://youtu.be/..."></div>
      <div class="af"><label>Título</label><input type="text" name="video_titulo" placeholder="Nome do projeto"></div>
      <div class="af"><label>Capa</label><input type="file" name="video_capa_${i}" accept="image/*" class="adm-file-input"></div>
    </div>
    <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-video-row').remove()">✕</button>`;
  wrap.appendChild(row);
}
'''

# ── APLICA ────────────────────────────────────────────────────────────────────
print('Escrevendo app.py ...')
open(os.path.join(BASE, 'app.py'), 'w', encoding='utf-8').write(APP)
print('  OK')

print('Escrevendo templates/admin.html ...')
open(os.path.join(BASE, 'templates', 'admin.html'), 'w', encoding='utf-8').write(ADMIN_HTML)
print('  OK')

print('Adicionando CSS do admin em static/css/style.css ...')
css_path = os.path.join(BASE, 'static', 'css', 'style.css')
current_css = open(css_path, encoding='utf-8').read()
marker = '/* ═══════════════════════════════════════════════\n   ADMIN — estilos'
if marker not in current_css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write(CSS_ADMIN)
    print('  OK (CSS adicionado)')
else:
    # Substitui bloco existente
    start = current_css.find(marker)
    open(css_path, 'w', encoding='utf-8').write(current_css[:start] + CSS_ADMIN.strip())
    print('  OK (CSS atualizado)')

print('Atualizando static/js/main.js ...')
js_path = os.path.join(BASE, 'static', 'js', 'main.js')
js = open(js_path, encoding='utf-8').read()
if 'adm-video-row' not in js:
    # Remove função addVideoRow antiga e adiciona nova
    if 'function addVideoRow' in js:
        start = js.find('function addVideoRow')
        end   = js.find('\n}', start) + 2
        js    = js[:start] + js[end:]
    js += '\n' + JS_EXTRA
    open(js_path, 'w', encoding='utf-8').write(js)
    print('  OK')
else:
    print('  JS já atualizado')

print('\n✅  Tudo pronto! Reinicie com: python app.py\n')
PYEOF
