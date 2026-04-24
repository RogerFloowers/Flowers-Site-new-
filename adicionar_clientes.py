#!/usr/bin/env python3
"""
Rode dentro de ~/Downloads/flowers_site
python3 adicionar_clientes.py
"""
import os, json

BASE = os.path.dirname(os.path.abspath(__file__))

# ── 1. ATUALIZA config.json ───────────────────────────────────────────────────
cfg_path = os.path.join(BASE, 'config.json')
cfg = json.load(open(cfg_path, encoding='utf-8')) if os.path.exists(cfg_path) else {}

if 'clientes' not in cfg:
    cfg['clientes'] = [
        {"nome": "Felipe Titto",    "cargo": "Ator e empresário",  "foto": ""},
        {"nome": "João Kepler",     "cargo": "Empresário",          "foto": ""},
        {"nome": "Danilo Gentili",  "cargo": "Apresentador",        "foto": ""},
        {"nome": "Natalia Beauty",  "cargo": "Influenciadora",      "foto": ""},
    ]

if 'empresas' not in cfg:
    cfg['empresas'] = [
        {"nome": "Sicredi",   "logo": ""},
        {"nome": "X Business","logo": ""},
        {"nome": "Agrotork",  "logo": ""},
        {"nome": "SEBRAE",    "logo": ""},
    ]

json.dump(cfg, open(cfg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('config.json OK')

# ── 2. CRIA PASTAS ────────────────────────────────────────────────────────────
for d in ['clientes', 'empresas']:
    os.makedirs(os.path.join(BASE, 'static', 'img', d), exist_ok=True)
print('Pastas criadas OK')

# ── 3. ROTAS NO app.py ───────────────────────────────────────────────────────
app_path = os.path.join(BASE, 'app.py')
app = open(app_path, encoding='utf-8').read()

ROTAS = '''
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
'''

if 'salvar_clientes' not in app:
    app = app.replace("if __name__ == '__main__':", ROTAS + "\nif __name__ == '__main__':")
    open(app_path, 'w', encoding='utf-8').write(app)
    print('app.py: rotas adicionadas OK')
else:
    print('app.py: rotas já existem')

# ── 4. HTML DA SEÇÃO (inserir no index.html após hero) ───────────────────────
SECAO_HTML = '''
<!-- CLIENTES ↓ inserido automaticamente -->
<section class="sec-clientes" id="clientes">
  <div class="sec-clientes-inner">
    <div class="sec-clientes-header reveal-left">
      <h2 class="sec-clientes-title">Parceiros que a <span>produtora</span> já gravou 🎬</h2>
      <p class="sec-clientes-sub">Eventos empresariais em todo o Brasil 🇧🇷</p>
    </div>

    {% if cfg.clientes %}
    <div class="carrossel-wrap">
      <div class="carrossel-track" id="carrossel-clientes">
        {% for c in cfg.clientes %}
        <div class="carrossel-slide reveal-scale">
          <div class="cli-card">
            <div class="cli-avatar">
              {% if c.foto %}
                <img src="{{ url_for('static', filename='img/clientes/' + c.foto) }}" alt="{{ c.nome }}">
              {% else %}
                <div class="cli-avatar-ph">{{ c.nome[0] }}</div>
              {% endif %}
            </div>
            <div class="cli-info">
              <div class="cli-nome">{{ c.nome }} <span class="cli-check">✓</span></div>
              <div class="cli-cargo">{{ c.cargo }}</div>
            </div>
          </div>
        </div>
        {% endfor %}
      </div>
      <div class="carrossel-dots" id="carrossel-dots"></div>
    </div>
    {% endif %}

    <!-- EMPRESAS -->
    {% if cfg.empresas %}
    <div class="empresas-strip reveal">
      <div class="empresas-inner">
        {% for e in cfg.empresas[:6] %}
        <div class="empresa-item">
          {% if e.logo %}
            <img src="{{ url_for('static', filename='img/empresas/' + e.logo) }}" alt="{{ e.nome }}" class="empresa-logo">
          {% else %}
            <span class="empresa-nome-txt">{{ e.nome }}</span>
          {% endif %}
        </div>
        {% if not loop.last %}
        <div class="empresa-sep">|</div>
        {% endif %}
        {% endfor %}
      </div>
    </div>
    {% endif %}
  </div>
</section>
<!-- FIM CLIENTES -->
'''

idx_path = os.path.join(BASE, 'templates', 'index.html')
idx = open(idx_path, encoding='utf-8').read()

if 'sec-clientes' not in idx:
    # Insere logo após o fechamento do hero
    idx = idx.replace('<!-- VÍDEOS -->', SECAO_HTML + '\n<!-- VÍDEOS -->')
    open(idx_path, 'w', encoding='utf-8').write(idx)
    print('index.html: seção clientes adicionada OK')
else:
    print('index.html: seção já existe')

# ── 5. ADMIN HTML — adicionar seções de clientes e empresas ──────────────────
ADMIN_CLIENTES = '''
  <!-- CLIENTES -->
  <div class="adm-section" id="clientes">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Portfólio de clientes</div>
        <h2 class="adm-sec-title">Clientes & parceiros</h2>
      </div>
    </div>
    <p class="adm-hint" style="margin-bottom:16px">
      Foto recomendada: <strong>200×200px</strong> (quadrada, rosto centralizado). PNG ou JPG.
    </p>
    <form action="{{ url_for('salvar_clientes') }}" method="POST" enctype="multipart/form-data">
      <div id="clientes-wrap">
        {% for c in cfg.clientes %}
        <div class="adm-cli-row">
          <div class="adm-cli-avatar">
            {% if c.foto %}
              <img src="{{ url_for('static', filename='img/clientes/' + c.foto) }}" alt="{{ c.nome }}">
            {% else %}
              <div class="adm-cli-ph">{{ c.nome[0] if c.nome else '?' }}</div>
            {% endif %}
          </div>
          <div class="adm-cli-fields">
            <div class="af"><label>Nome</label><input type="text" name="cli_nome" value="{{ c.nome }}" placeholder="Nome do cliente"></div>
            <div class="af"><label>Cargo / descrição</label><input type="text" name="cli_cargo" value="{{ c.cargo }}" placeholder="Ex: Empresário"></div>
            <div class="af"><label>Foto (200×200px)</label><input type="file" name="cli_foto_{{ loop.index0 }}" accept="image/*" class="adm-file-input"></div>
          </div>
          <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-cli-row').remove()">✕</button>
        </div>
        {% endfor %}
      </div>
      <button type="button" class="adm-btn-add" onclick="addClienteRow()" style="margin-bottom:14px">+ Adicionar cliente</button>
      <br>
      <button type="submit" class="adm-btn-save">Salvar clientes</button>
    </form>
  </div>

  <!-- EMPRESAS -->
  <div class="adm-section" id="empresas">
    <div class="adm-sec-head">
      <div>
        <div class="adm-sec-tag">Empresas parceiras</div>
        <h2 class="adm-sec-title">Logos de empresas</h2>
      </div>
    </div>
    <p class="adm-hint" style="margin-bottom:16px">
      Logo recomendada: <strong>200×80px</strong> (horizontal, fundo transparente). PNG preferencialmente.<br>
      Máximo de <strong>6 logos</strong> exibidas no site.
    </p>
    <form action="{{ url_for('salvar_empresas') }}" method="POST" enctype="multipart/form-data">
      <div id="empresas-wrap">
        {% for e in cfg.empresas %}
        <div class="adm-emp-row">
          <div class="adm-emp-logo-prev">
            {% if e.logo %}
              <img src="{{ url_for('static', filename='img/empresas/' + e.logo) }}" alt="{{ e.nome }}">
            {% else %}
              <span>{{ e.nome }}</span>
            {% endif %}
          </div>
          <div class="adm-cli-fields">
            <div class="af"><label>Nome da empresa</label><input type="text" name="emp_nome" value="{{ e.nome }}" placeholder="Ex: Sicredi"></div>
            <div class="af"><label>Logo (200×80px PNG)</label><input type="file" name="emp_logo_{{ loop.index0 }}" accept="image/*" class="adm-file-input"></div>
          </div>
          <button type="button" class="adm-btn-rm" onclick="this.closest('.adm-emp-row').remove()">✕</button>
        </div>
        {% endfor %}
      </div>
      <button type="button" class="adm-btn-add" onclick="addEmpresaRow()" style="margin-bottom:14px">+ Adicionar empresa</button>
      <br>
      <button type="submit" class="adm-btn-save">Salvar empresas</button>
    </form>
  </div>
'''

adm_path = os.path.join(BASE, 'templates', 'admin.html')
adm = open(adm_path, encoding='utf-8').read()

if 'sec-clientes' not in adm and 'id="clientes"' not in adm:
    # Insere antes do fechamento do adm-wrap
    adm = adm.replace('</div>\n{% endblock %}', ADMIN_CLIENTES + '\n</div>\n{% endblock %}')
    open(adm_path, 'w', encoding='utf-8').write(adm)
    print('admin.html: seções clientes/empresas adicionadas OK')
else:
    print('admin.html: seções já existem')

# Atualiza atalhos no admin
adm = open(adm_path, encoding='utf-8').read()
if 'Clientes' not in adm:
    adm = adm.replace(
        '<a href="#stats"   class="adm-shortcut">📊 Stats</a>',
        '<a href="#stats"   class="adm-shortcut">📊 Stats</a>\n    <a href="#clientes" class="adm-shortcut">👥 Clientes</a>\n    <a href="#empresas" class="adm-shortcut">🏢 Empresas</a>'
    )
    open(adm_path, 'w', encoding='utf-8').write(adm)
    print('admin.html: atalhos atualizados OK')

# ── 6. CSS ────────────────────────────────────────────────────────────────────
CSS = '''
/* ═══════════════════════════════════════
   CLIENTES & EMPRESAS
═══════════════════════════════════════ */
.sec-clientes {
  background: var(--bg);
  padding: 80px 0 60px;
  overflow: hidden;
}
.sec-clientes-inner { max-width: 1200px; margin: 0 auto; padding: 0 6%; }

.sec-clientes-header { margin-bottom: 44px; }
.sec-clientes-title {
  font-size: clamp(24px, 4vw, 44px);
  font-weight: 900;
  color: #fff;
  letter-spacing: -1.5px;
  line-height: 1.15;
  margin-bottom: 8px;
}
.sec-clientes-title span { color: var(--pk); }
.sec-clientes-sub { font-size: 14px; color: var(--txt2); }

/* CARROSSEL */
.carrossel-wrap { position: relative; margin-bottom: 44px; overflow: hidden; }
.carrossel-track {
  display: flex;
  gap: 0;
  transition: transform .5s cubic-bezier(.4,0,.2,1);
}
.carrossel-slide {
  min-width: 25%;
  padding: 0 12px;
  flex-shrink: 0;
}
.cli-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px 0;
  border-right: 1px solid rgba(255,255,255,.08);
}
.carrossel-slide:last-child .cli-card { border-right: none; }

.cli-avatar {
  width: 52px; height: 52px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--bg3);
  border: 2px solid rgba(212,83,126,.3);
}
.cli-avatar img { width:100%; height:100%; object-fit:cover; display:block; }
.cli-avatar-ph {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 900; color: var(--pk);
  background: var(--bg3);
}
.cli-nome {
  font-size: 14px; font-weight: 700; color: #fff;
  display: flex; align-items: center; gap: 5px;
  margin-bottom: 3px;
}
.cli-check {
  width: 16px; height: 16px; border-radius: 50%;
  background: #1d9bf0;
  color: #fff; font-size: 9px;
  display: inline-flex; align-items: center; justify-content: center;
  font-weight: 900; flex-shrink: 0;
}
.cli-cargo { font-size: 11px; color: var(--txt2); }

.carrossel-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 24px;
}
.carrossel-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: rgba(255,255,255,.2);
  cursor: pointer; transition: all .25s;
}
.carrossel-dot.active { background: var(--pk); transform: scale(1.3); }

/* EMPRESAS STRIP */
.empresas-strip {
  background: var(--bg3);
  border: 1px solid rgba(255,255,255,.07);
  border-radius: 50px;
  padding: 0 24px;
}
.empresas-inner {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80px;
  flex-wrap: wrap;
  gap: 0;
}
.empresa-item {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px 32px;
  flex: 1;
  min-width: 120px;
}
.empresa-logo {
  height: 36px;
  width: auto;
  max-width: 140px;
  object-fit: contain;
  filter: brightness(0) invert(1);
  opacity: .7;
  transition: opacity .2s, filter .2s;
}
.empresa-logo:hover { opacity: 1; filter: brightness(0) invert(1) sepia(1) hue-rotate(290deg) saturate(3); }
.empresa-nome-txt {
  font-size: 16px; font-weight: 800; color: rgba(255,255,255,.6);
  letter-spacing: -.3px;
}
.empresa-sep { color: rgba(255,255,255,.1); font-size: 28px; font-weight: 100; }

/* ADMIN — clientes e empresas */
.adm-cli-row, .adm-emp-row {
  display: grid;
  grid-template-columns: 60px 1fr auto;
  gap: 14px;
  align-items: start;
  background: var(--bg3);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 10px;
  padding: 14px;
  margin-bottom: 10px;
}
.adm-cli-avatar, .adm-emp-logo-prev {
  width: 56px; height: 56px;
  border-radius: 50%;
  overflow: hidden;
  background: var(--bg4);
  border: 1px solid rgba(255,255,255,.08);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.adm-emp-logo-prev {
  border-radius: 8px;
  width: 80px; height: 40px;
}
.adm-cli-avatar img, .adm-emp-logo-prev img { width:100%; height:100%; object-fit:cover; }
.adm-cli-ph { font-size: 22px; font-weight: 900; color: var(--pk); }
.adm-emp-logo-prev span { font-size: 11px; color: var(--txt3); font-weight: 600; }
.adm-cli-fields { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }

/* ANIMAÇÕES SCROLL */
.reveal-left {
  opacity: 0;
  transform: translateX(-40px);
  transition: opacity .7s ease, transform .7s ease;
}
.reveal-left.visible { opacity: 1; transform: none; }

.reveal-scale {
  opacity: 0;
  transform: scale(.94) translateY(16px);
  transition: opacity .6s ease, transform .6s ease;
}
.reveal-scale.visible { opacity: 1; transform: none; }

/* RESPONSIVE */
@media (max-width: 900px) {
  .carrossel-slide { min-width: 50%; }
  .adm-cli-fields { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 600px) {
  .carrossel-slide { min-width: 100%; }
  .empresas-strip { border-radius: 16px; padding: 0 12px; }
  .empresa-item { padding: 12px 16px; }
  .adm-cli-row, .adm-emp-row { grid-template-columns: 50px 1fr auto; }
  .adm-cli-fields { grid-template-columns: 1fr; }
}
'''

css_path = os.path.join(BASE, 'static', 'css', 'style.css')
css = open(css_path, encoding='utf-8').read()
marker = '/* ═══════════════════════════════════════\n   CLIENTES & EMPRESAS'
if marker not in css:
    with open(css_path, 'a', encoding='utf-8') as f:
        f.write('\n' + CSS)
    print('style.css: CSS adicionado OK')
else:
    print('style.css: CSS já existe')

# ── 7. JS — carrossel + reveal ───────────────────────────────────────────────
JS = '''
// ── CARROSSEL CLIENTES ────────────────────────────────────────────────────────
(function(){
  const track = document.getElementById('carrossel-clientes');
  if(!track) return;

  const slides     = track.querySelectorAll('.carrossel-slide');
  const dotsWrap   = document.getElementById('carrossel-dots');
  const perView    = () => window.innerWidth < 600 ? 1 : window.innerWidth < 900 ? 2 : 4;
  let current      = 0;
  let autoTimer    = null;
  let totalPages   = 0;

  function buildDots(){
    dotsWrap.innerHTML = '';
    totalPages = Math.ceil(slides.length / perView());
    for(let i=0;i<totalPages;i++){
      const d = document.createElement('span');
      d.className = 'carrossel-dot' + (i===0?' active':'');
      d.onclick = () => goTo(i);
      dotsWrap.appendChild(d);
    }
  }

  function goTo(page){
    current = Math.max(0, Math.min(page, totalPages-1));
    const offset = current * perView() * (100 / slides.length);
    track.style.transform = `translateX(-${offset}%)`;
    dotsWrap.querySelectorAll('.carrossel-dot').forEach((d,i)=>{
      d.classList.toggle('active', i===current);
    });
  }

  function next(){ goTo(current < totalPages-1 ? current+1 : 0); }

  function startAuto(){ autoTimer = setInterval(next, 3500); }
  function stopAuto() { clearInterval(autoTimer); }

  track.addEventListener('mouseenter', stopAuto);
  track.addEventListener('mouseleave', startAuto);

  // Touch swipe
  let tx = 0;
  track.addEventListener('touchstart', e=>{ tx=e.touches[0].clientX; stopAuto(); },{passive:true});
  track.addEventListener('touchend',   e=>{
    const dx = e.changedTouches[0].clientX - tx;
    if(Math.abs(dx)>40){ dx<0 ? next() : goTo(current>0?current-1:totalPages-1); }
    startAuto();
  },{passive:true});

  window.addEventListener('resize', ()=>{ buildDots(); goTo(0); });
  buildDots();
  startAuto();
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
'''

js_path = os.path.join(BASE, 'static', 'js', 'main.js')
js = open(js_path, encoding='utf-8').read()
if 'carrossel-clientes' not in js:
    with open(js_path, 'a', encoding='utf-8') as f:
        f.write('\n' + JS)
    print('main.js: JS do carrossel adicionado OK')
else:
    print('main.js: JS já existe')

print('\n✅  Tudo pronto!')
print('   Rode: python app.py')
print('   No admin acesse as seções: 👥 Clientes e 🏢 Empresas\n')
print('   Tamanhos recomendados:')
print('   - Foto de cliente: 200×200px (quadrada)')
print('   - Logo de empresa: 200×80px  (horizontal, PNG transparente)\n')
