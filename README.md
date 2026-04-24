# 🌸 Flowers Films — Site Público

Site público completo com painel admin integrado.

---

## Instalação e execução

```bash
# 1. Entre na pasta
cd flowers_site

# 2. Crie o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install flask werkzeug

# 4. Copie sua logo para a pasta certa
cp sua_logo.png static/img/logo.png

# 5. Rode o servidor
python app.py
```

Acesse: **http://localhost:5000**

---

## Acesso admin

- URL: `http://localhost:5000/login`
- Usuário: `roger`
- Senha: `flowers2026`

> Para mudar usuário/senha, edite as linhas no `app.py`:
> ```python
> ADMIN_USER = 'roger'
> ADMIN_PASS = 'flowers2026'
> ```

---

## O que você gerencia pelo painel admin

| Seção | O que faz |
|-------|-----------|
| Banner | Edita as 3 linhas do título, subtítulo e tag |
| Stats | Edita os 3 números da barra (projetos, anos, etc.) |
| Vídeos | Adiciona/remove vídeos do YouTube por link ou ID |
| Fotos | Upload e exclusão de fotos do portfólio |
| Contato | E-mail, WhatsApp, Instagram |

---

## Estrutura de arquivos

```
flowers_site/
├── app.py                   ← Backend Flask
├── config.json              ← Configurações do site (gerado automaticamente)
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html            ← Layout base (nav + footer)
│   ├── index.html           ← Página principal
│   ├── portfolio_videos.html
│   ├── portfolio_fotos.html
│   ├── cursos.html
│   ├── login.html
│   └── admin.html
├── static/
│   ├── css/style.css        ← Todo o visual do site
│   ├── js/main.js           ← JavaScript
│   └── img/
│       └── logo.png         ← ← COLOQUE SUA LOGO AQUI
└── uploads/
    └── fotos/               ← Fotos enviadas pelo admin
```

---

## Próximos passos

- [ ] Integrar com o sistema de orçamento (flowers_orcamento)
- [ ] Adicionar seção de Cursos com links
- [ ] Hospedar online no seu domínio
- [ ] Formulário de contato com envio de e-mail real

---

*Flowers Films © 2026 — Roger Flores*
