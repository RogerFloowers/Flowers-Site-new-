from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
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
        if request.form.get('usuario','').strip() == ADMIN_USER and \
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
    # Textos do hero
    if 'hero_texto' not in cfg:
        cfg['hero_texto'] = {}
    cfg['hero_texto']['titulo_normal'] = request.form.get('titulo_normal','').strip()
    cfg['hero_texto']['titulo_bold']   = request.form.get('titulo_bold','').strip()
    cfg['hero_texto']['subtitulo']     = request.form.get('subtitulo','').strip()
    cfg['hero_texto']['desc_esquerda'] = request.form.get('desc_esquerda','').strip()
    cfg['hero_texto']['desc_direita']  = request.form.get('desc_direita','').strip()
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


@app.route('/admin/salvar-clientes', methods=['POST'])
@login_required
def salvar_clientes():
    cfg = load_config()
    cli_dir = os.path.join(STATIC_DIR, 'img', 'clientes')
    os.makedirs(cli_dir, exist_ok=True)
    nomes  = request.form.getlist('cli_nome')
    cargos = request.form.getlist('cli_cargo')
    fotos_atuais = {c['nome']: c.get('foto','') for c in cfg.get('clientes',[])}
    clientes = []
    for i, (nome, cargo) in enumerate(zip(nomes, cargos)):
        nome = nome.strip()
        if not nome: continue
        foto = fotos_atuais.get(nome, '')
        f = request.files.get(f'cli_foto_{i}')
        if f and f.filename and allowed(f.filename):
            fn = secure_filename(f'cli_{i}_{f.filename}')
            f.save(os.path.join(cli_dir, fn))
            foto = fn
        clientes.append({'nome': nome, 'cargo': cargo.strip(), 'foto': foto})
    cfg['clientes'] = clientes
    save_config(cfg)
    return redirect(url_for('admin') + '#clientes')

@app.route('/admin/salvar-empresas', methods=['POST'])
@login_required
def salvar_empresas():
    cfg = load_config()
    emp_dir = os.path.join(STATIC_DIR, 'img', 'empresas')
    os.makedirs(emp_dir, exist_ok=True)
    nomes = request.form.getlist('emp_nome')
    logos_atuais = {e['nome']: e.get('logo','') for e in cfg.get('empresas',[])}
    empresas = []
    for i, nome in enumerate(nomes):
        nome = nome.strip()
        if not nome: continue
        logo = logos_atuais.get(nome, '')
        f = request.files.get(f'emp_logo_{i}')
        if f and f.filename and allowed(f.filename):
            fn = secure_filename(f'emp_{i}_{f.filename}')
            f.save(os.path.join(emp_dir, fn))
            logo = fn
        empresas.append({'nome': nome, 'logo': logo})
    cfg['empresas'] = empresas
    save_config(cfg)
    return redirect(url_for('admin') + '#empresas')


@app.route('/admin/salvar-video-apres', methods=['POST'])
@login_required
def salvar_video_apres():
    cfg = load_config()
    raw = request.form.get('video_apres', '').strip()
    if 'youtube.com/watch?v=' in raw:
        raw = raw.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in raw:
        raw = raw.split('youtu.be/')[1].split('?')[0]
    cfg['video_apresentacao'] = raw
    # Thumbnail personalizada
    thumb = request.files.get('video_apres_thumb')
    if thumb and thumb.filename and allowed(thumb.filename):
        fn = secure_filename('video_apres_thumb_' + thumb.filename)
        thumb.save(os.path.join(STATIC_DIR, 'img', fn))
        cfg['video_apres_thumb'] = fn
    save_config(cfg)
    return redirect(url_for('admin') + '#video-apres')

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
    print('\n  ✦  FLOWERS FILMS — Site Público')
    print('  →  http://localhost:5051\n')
    app.run(debug=True, port=5051, host="0.0.0.0")
