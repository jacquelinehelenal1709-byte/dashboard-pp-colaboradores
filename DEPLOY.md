# DEPLOY — Dashboard PP Colaboradores V2

## ETAPA 1 — GitHub (execute o script)

1. Abra a pasta `PROJETOS\dashboard_pp_colaboradores\`
2. Clique com o botão direito em **publicar.ps1**
3. Selecione **"Executar com PowerShell"**
4. Uma janela do navegador vai abrir — faça login no GitHub e autorize
5. O script cria o repositório privado e faz o push automaticamente
6. Anote a URL do repositório que aparece no final (ex: `https://github.com/seu-usuario/dashboard-pp-colaboradores`)

---

## ETAPA 2 — Render (deploy na internet)

### 2.1 — Criar conta
- Acesse **render.com**
- Clique em **"Get Started for Free"**
- Cadastre com o e-mail `jacqueline.helenal1709@gmail.com` ou com a conta GitHub

### 2.2 — Criar o Web Service
1. No painel do Render, clique em **"New +"** → **"Web Service"**
2. Conecte sua conta GitHub (botão "Connect GitHub")
3. Selecione o repositório **dashboard-pp-colaboradores**
4. Configure:

| Campo | Valor |
|-------|-------|
| Name | `farmanello-pp` |
| Region | `Oregon (US West)` |
| Branch | `master` |
| Runtime | `Python 3` |
| Build Command | `pip install -r requirements.txt && python seed.py` |
| Start Command | `gunicorn app:app` |

### 2.3 — Variáveis de ambiente
Na seção **"Environment Variables"**, adicione:

| Chave | Valor |
|-------|-------|
| `SECRET_KEY` | *(gerada localmente — ver arquivo `.env`)* |
| `FLASK_ENV` | `production` |
| `DADOS_JSON_PATH` | `/opt/render/project/src/dados_dashboard.json` |

### 2.4 — Criar o serviço
- Clique em **"Create Web Service"**
- Aguarde o deploy (3–5 minutos)
- Ao terminar, o Render exibe uma URL como: `https://farmanello-pp.onrender.com`
- **Teste o login** com: `jacqueline` / `Farmanello@2026`

---

## ETAPA 3 — Domínio e HTTPS

### 3.1 — Adicionar domínio no Render
1. No painel do serviço no Render, clique em **"Settings"** → **"Custom Domains"**
2. Clique em **"Add Custom Domain"**
3. Digite: `painel.farmanello.com.br`
4. O Render vai mostrar um registro DNS para você configurar

### 3.2 — Configurar DNS no Registro.br
1. Acesse **registro.br** e faça login
2. Clique no domínio `farmanello.com.br`
3. Vá em **"Editar zona DNS"**
4. Adicione um registro **CNAME**:
   - Nome: `painel`
   - Valor: (copie a URL do Render, ex: `farmanello-pp.onrender.com`)
5. Salve — a propagação leva até 24 horas (geralmente menos de 1 hora)

### 3.3 — HTTPS
O Render ativa o HTTPS automaticamente via Let's Encrypt.
Nenhuma configuração adicional necessária.

---

## Após o deploy — Upload dos dados reais

Cada vez que a Isabelly executar a V1:
1. O arquivo `dados_dashboard.json` é gerado em `pp_colaboradores\saida\`
2. Faça upload deste arquivo para o servidor via Git:

```powershell
# Na pasta dashboard_pp_colaboradores:
copy "..\pp_colaboradores\saida\dados_dashboard.json" "dados_dashboard.json"
git add dados_dashboard.json
git commit -m "dados: atualiza painel junho/2026"
git push
```

O Render detecta o push e atualiza automaticamente o servidor.

---

## Credenciais iniciais

Todos os usuários foram criados com a senha: **`Farmanello@2026`**

| Login | Perfil | Loja |
|-------|--------|------|
| jacqueline | Admin | — |
| diretor | Diretoria | — |
| gestor.matriz | Gestor | Matriz |
| gestor.pira1 | Gestor | Piraquara I |
| gestor.pira2 | Gestor | Piraquara II |
| gestor.maria | Gestor | Maria Antonieta |

**Altere as senhas em produção** via `https://painel.farmanello.com.br/admin`
